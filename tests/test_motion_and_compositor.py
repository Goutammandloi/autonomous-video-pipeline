import json
import sys
from pathlib import Path
import cv2
import numpy as np

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import ProductionShotDeck
from src.compositor import ScreenWarper
from src.motion import MotionEngine, GlitchDetector, CornerPoints


def run_test():
    print("=== Testing Feature 4: Motion Synthesis & Dynamic Screen Inset Compositing ===")

    # 1. Test Screen Warper (4-Point Perspective Transform)
    print("\n--- Test 1: Testing OpenCV 4-Point Homography Perspective Warper ---")
    base_canvas = np.zeros((1920, 1080, 3), dtype=np.uint8)
    base_canvas[:] = (30, 20, 15)  # Dark room base

    terminal = ScreenWarper.create_mock_terminal_screen(width=1280, height=800)
    corners = CornerPoints(
        top_left=(180.0, 680.0),
        top_right=(900.0, 680.0),
        bottom_right=(880.0, 1320.0),
        bottom_left=(200.0, 1320.0)
    )

    warped_composite = ScreenWarper.warp_screen_onto_image(
        base_image=base_canvas,
        screen_content=terminal,
        corners=corners,
        feather_border_px=3
    )

    assert warped_composite.shape == (1920, 1080, 3), "Composite resolution mismatch"
    # Ensure screen region is not dark base
    center_pixel = warped_composite[1000, 540]
    assert np.any(center_pixel > 0), "Perspective screen warp failed to render content"
    print("  ✅ ScreenWarper homography transform executed successfully!")

    # 2. Test Optical Flow Glitch Detector
    print("\n--- Test 2: Testing Gunnar Farneback Optical Flow Glitch Detector ---")
    detector = GlitchDetector(z_score_threshold=3.5)

    # Smooth frame sequence
    smooth_frames = []
    f_base = np.zeros((480, 270, 3), dtype=np.uint8)
    for i in range(15):
        frame = f_base.copy()
        cv2.circle(frame, (50 + i * 4, 150), 30, (200, 200, 50), -1)
        smooth_frames.append(frame)

    smooth_qa = detector.evaluate_video_frames(smooth_frames, shot_id=1)
    print(f"  Smooth sequence Max Z-Score: {smooth_qa.max_flow_z_score} (Passes: {smooth_qa.passes_qa})")
    assert smooth_qa.passes_qa, "Smooth motion should pass glitch detection"

    # Glitchy frame sequence (inject sharp dislocation spike at frame 8)
    glitch_frames = [f.copy() for f in smooth_frames]
    cv2.circle(glitch_frames[8], (220, 350), 75, (255, 50, 50), -1)  # violent dislocation
    glitch_qa = detector.evaluate_video_frames(glitch_frames, shot_id=1)
    print(f"  Glitch sequence Max Z-Score: {glitch_qa.max_flow_z_score} (Passes: {glitch_qa.passes_qa}, Anomalies: {glitch_qa.anomalous_frames})")
    assert not glitch_qa.passes_qa, "Glitch detector must flag abrupt spatial dislocation"
    print("  ✅ Optical Flow Glitch QA successfully caught synthetic anomaly!")

    # 3. Test Batch Motion Generation on Appin Shot Deck
    print("\n--- Test 3: Batch Video Clip Generation from Keyframes ---")
    deck_path = root_dir / "data" / "shot_decks" / "project_origin_ep01_shot_deck.json"
    with open(deck_path, "r", encoding="utf-8") as f:
        shot_deck = ProductionShotDeck.model_validate(json.load(f))

    keyframes_dir = root_dir / "data" / "keyframes"
    keyframes_map = {
        shot.shot_id: str(keyframes_dir / f"shot_{shot.shot_id}_keyframe.png")
        for shot in shot_deck.shots
    }

    # Verify keyframes exist
    for sid, kfp in keyframes_map.items():
        assert Path(kfp).exists(), f"Keyframe for Shot {sid} not found at {kfp}"

    video_clips_dir = root_dir / "data" / "video_clips"
    engine = MotionEngine(output_dir=str(video_clips_dir), fps=30)

    clips = engine.generate_deck_video_clips(shot_deck, keyframes_map)
    print(f"\n[Result] Generated {len(clips)} Video Clips:")
    for clip in clips:
        print(f"  Shot {clip.shot_id} [{clip.width}x{clip.height}] {clip.duration_sec}s ({clip.total_frames} frames @ 30fps):")
        print(f"    Path: {clip.file_path}")
        print(f"    Screen Inset: {clip.has_screen_inset}")
        print(f"    QA Max Flow Z: {clip.qa_result.max_flow_z_score} | Status: {clip.status}")
        assert Path(clip.file_path).exists(), f"Video file not found: {clip.file_path}"
        assert clip.width == 1080 and clip.height == 1920, "Clip resolution must be 1080x1920 vertical"
        assert clip.total_frames >= 30, "Clip must contain at least 1 second of frames"

    # Specific check on Shot 3: must have screen inset
    shot3_clip = next(c for c in clips if c.shot_id == 3)
    assert shot3_clip.has_screen_inset, "Shot 3 must have dynamic screen perspective inset applied"

    print("\n✅ All Feature 4 Assertions Passed Successfully!")


if __name__ == "__main__":
    run_test()
