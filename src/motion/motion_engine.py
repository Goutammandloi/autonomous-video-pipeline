"""
Autonomous AI Video Pipeline: I2V Motion Engine & Video Synthesizer
Orchestrates:
1. Camera kinematics translation (push-in, tracking, handheld, tilt)
2. Dynamic Screen Inset integration via OpenCV perspective transform
3. Frame generation at strict CFR 30.0 fps (1080x1920 vertical)
4. Optical flow glitch evaluation & self-healing remediation
"""

from pathlib import Path
from typing import List, Optional, Tuple, Dict
import cv2
import numpy as np

from .schemas import MotionVector, VideoClipAsset, CornerPoints
from .glitch_detector import GlitchDetector
from ..compositor.screen_warper import ScreenWarper
from ..scripting.schemas import ProductionShot, ProductionShotDeck, CameraMovement


class MotionEngine:
    """
    Image-to-Video (I2V) motion generation and perspective compositing engine.
    """

    KINEMATICS_PRESETS: Dict[CameraMovement, MotionVector] = {
        CameraMovement.STATIC: MotionVector(pan_x=0.0, pan_y=0.0, zoom_ratio=1.00, rotation_deg=0.0, motion_bucket_id=80),
        CameraMovement.SLOW_PUSH_IN: MotionVector(pan_x=0.0, pan_y=0.0, zoom_ratio=1.06, rotation_deg=0.0, motion_bucket_id=95),
        CameraMovement.PULL_BACK: MotionVector(pan_x=0.0, pan_y=0.0, zoom_ratio=0.95, rotation_deg=0.0, motion_bucket_id=95),
        CameraMovement.HANDHELD_ORGANIC: MotionVector(pan_x=0.02, pan_y=0.015, zoom_ratio=1.02, rotation_deg=0.4, motion_bucket_id=105),
        CameraMovement.TRACKING_FOLLOW: MotionVector(pan_x=0.04, pan_y=0.0, zoom_ratio=1.03, rotation_deg=0.0, motion_bucket_id=110),
        CameraMovement.DUTCH_TILT: MotionVector(pan_x=0.0, pan_y=0.0, zoom_ratio=1.02, rotation_deg=1.8, motion_bucket_id=100),
        CameraMovement.WHIP_PAN: MotionVector(pan_x=0.15, pan_y=0.0, zoom_ratio=1.0, rotation_deg=0.0, motion_bucket_id=130),
    }

    def __init__(self, output_dir: Optional[str] = None, fps: int = 30):
        self.output_dir = Path(output_dir or "data/video_clips")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.fps = fps
        self.glitch_detector = GlitchDetector(z_score_threshold=3.5)

    def generate_shot_video_clip(
        self,
        shot: ProductionShot,
        keyframe_path: str,
        screen_content: Optional[np.ndarray] = None,
        corners: Optional[CornerPoints] = None,
        max_retries: int = 2
    ) -> VideoClipAsset:
        """
        Synthesizes a 30 FPS vertical MP4 video clip from a keyframe with camera kinematics
        and automated optical flow glitch verification.
        """
        out_mp4 = self.output_dir / f"shot_{shot.shot_id}_clip.mp4"
        duration = shot.duration_sec
        total_frames = int(duration * self.fps)

        # 1. Load Base Keyframe (1080x1920)
        base_img = cv2.imread(str(keyframe_path))
        if base_img is None:
            raise FileNotFoundError(f"Keyframe not found at {keyframe_path}")

        h, w = base_img.shape[:2]
        has_screen_inset = False

        # 2. Check if Shot requires screen perspective warping (e.g. Shot 3 Laptop reveal)
        if shot.visual.camera_angle.value == "first_person_pov" or "screen" in shot.narrative_beat.lower():
            if corners is None:
                # Default screen coordinates inside 9:16 vertical laptop frame
                corners = CornerPoints(
                    top_left=(w * 0.16, h * 0.36),
                    top_right=(w * 0.84, h * 0.36),
                    bottom_right=(w * 0.82, h * 0.70),
                    bottom_left=(w * 0.18, h * 0.70)
                )
            if screen_content is None:
                screen_content = ScreenWarper.create_mock_terminal_screen(
                    title="APPIN CYBER LAB - SCANNER"
                )

            # Apply perspective warp
            base_img = ScreenWarper.warp_screen_onto_image(
                base_image=base_img,
                screen_content=screen_content,
                corners=corners,
                feather_border_px=2
            )
            has_screen_inset = True

        # 3. Motion Synthesis & Self-Healing QA Loop
        kinematics = self.KINEMATICS_PRESETS.get(
            shot.visual.camera_movement,
            self.KINEMATICS_PRESETS[CameraMovement.SLOW_PUSH_IN]
        )

        attempt = 1
        current_kinematics = kinematics

        while attempt <= max_retries:
            frames = self._synthesize_kinematic_frames(base_img, current_kinematics, total_frames)

            # Audit through Optical Flow Glitch Detector
            qa_result = self.glitch_detector.evaluate_video_frames(frames, shot_id=shot.shot_id)

            if qa_result.passes_qa:
                # Save MP4 video
                self._write_frames_to_mp4(frames, str(out_mp4))
                return VideoClipAsset(
                    shot_id=shot.shot_id,
                    file_path=str(out_mp4.resolve()),
                    duration_sec=duration,
                    fps=self.fps,
                    width=w,
                    height=h,
                    total_frames=total_frames,
                    has_screen_inset=has_screen_inset,
                    qa_result=qa_result,
                    status="QA_PASSED"
                )

            # Surgical Remediation: Dampen kinematics
            print(f"[MotionEngine] ⚠️ Outlier velocity spike detected in Shot {shot.shot_id}. Applying surgical damping...")
            current_kinematics = MotionVector(
                pan_x=current_kinematics.pan_x * 0.65,
                pan_y=current_kinematics.pan_y * 0.65,
                zoom_ratio=1.0 + (current_kinematics.zoom_ratio - 1.0) * 0.65,
                rotation_deg=current_kinematics.rotation_deg * 0.65,
                motion_bucket_id=85
            )
            attempt += 1

        # Fallback accept with remediation flag
        self._write_frames_to_mp4(frames, str(out_mp4))
        return VideoClipAsset(
            shot_id=shot.shot_id,
            file_path=str(out_mp4.resolve()),
            duration_sec=duration,
            fps=self.fps,
            width=w,
            height=h,
            total_frames=total_frames,
            has_screen_inset=has_screen_inset,
            qa_result=qa_result,
            status="QA_REMEDIATED"
        )

    def generate_deck_video_clips(
        self,
        shot_deck: ProductionShotDeck,
        keyframes_map: Dict[int, str]
    ) -> List[VideoClipAsset]:
        """
        Batch synthesizes video clips for all shots in a ProductionShotDeck.
        """
        clips = []
        print(f"\n🎥 Batch Synthesizing Video Clips for: {shot_deck.title}")
        for shot in shot_deck.shots:
            kf_path = keyframes_map.get(shot.shot_id)
            if not kf_path:
                continue
            print(f"  [Shot {shot.shot_id}] Motion: {shot.visual.camera_movement.value} ({shot.duration_sec}s @ 30fps)...")
            clip = self.generate_shot_video_clip(shot, kf_path)
            clips.append(clip)
            qa = clip.qa_result
            print(f"    ✅ Shot {shot.shot_id} Clip Rendered: {clip.total_frames} frames | Flow Max Z: {qa.max_flow_z_score} (Passes: {qa.passes_qa})")

        return clips

    def _synthesize_kinematic_frames(
        self,
        base_img: np.ndarray,
        kinematics: MotionVector,
        total_frames: int
    ) -> List[np.ndarray]:
        """
        Generates high-precision subpixel camera motion (push, pan, handheld subtle drift).
        """
        h, w = base_img.shape[:2]
        center_x, center_y = w / 2.0, h / 2.0
        frames = []

        for i in range(total_frames):
            progress = i / float(max(1, total_frames - 1))  # 0.0 -> 1.0

            # Scale interpolation
            scale = 1.0 + (kinematics.zoom_ratio - 1.0) * progress

            # Translation interpolation (pixels)
            shift_x = kinematics.pan_x * w * progress
            shift_y = kinematics.pan_y * h * progress

            # Subtle organic handheld micro-jitter if handheld preset
            if kinematics.rotation_deg > 0.1:
                jitter_angle = kinematics.rotation_deg * np.sin(progress * np.pi * 3.0)
                shift_x += 2.0 * np.sin(progress * np.pi * 5.0)
                shift_y += 1.5 * np.cos(progress * np.pi * 4.0)
            else:
                jitter_angle = 0.0

            # Affine transformation matrix
            M = cv2.getRotationMatrix2D((center_x, center_y), jitter_angle, scale)
            M[0, 2] += shift_x
            M[1, 2] += shift_y

            frame = cv2.warpAffine(
                base_img,
                M,
                (w, h),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_REFLECT101
            )
            frames.append(frame)

        return frames

    def _write_frames_to_mp4(self, frames: List[np.ndarray], output_path: str):
        """Encodes frame sequence to standard MP4 using mp4v/h264 codec."""
        h, w = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output_path, fourcc, self.fps, (w, h))

        for f in frames:
            writer.write(f)
        writer.release()
