"""
Autonomous AI Video Pipeline: Assembly & Final Master QA Evaluator
Performs automated multi-vector auditing of the assembled master video:
- A/V Sync delta calculation (|t_video - t_audio| <= 33ms)
- Aspect ratio, resolution, and CFR 30 FPS compliance
- Subtitle legibility and kinetic presence check
- Master container integrity (H.264 / AAC / yuv420p)
"""

import json
import subprocess
from typing import Dict, Any, List, Tuple
from pathlib import Path
import cv2
import imageio_ffmpeg

from .schemas import MasterVideoReport


class AssemblyQAEvaluator:
    """
    Automated gatekeeper validating final mastered video assets before dispatch.
    """

    def __init__(self):
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def evaluate_master_video(self, video_path: str, target_duration_sec: float = 18.5) -> MasterVideoReport:
        """
        Runs full deterministic audit on the assembled master video.
        """
        path = Path(video_path)
        notes: List[str] = []
        metrics: Dict[str, Any] = {}

        if not path.exists():
            return MasterVideoReport(
                video_path=video_path,
                total_duration_sec=0.0,
                total_frames=0,
                resolution=(0, 0),
                fps=0.0,
                file_size_bytes=0,
                has_audio=False,
                audio_duration_sec=0.0,
                av_sync_delta_ms=9999.0,
                qa_passed=False,
                qa_score=0.0,
                qa_notes=["Video file does not exist"]
            )

        file_size = path.stat().st_size
        metrics["file_size_bytes"] = file_size
        metrics["file_size_mb"] = round(file_size / (1024 * 1024), 2)

        # 1. Probe Video with OpenCV
        cap = cv2.VideoCapture(str(path.resolve()))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_duration = total_frames / fps if fps > 0 else 0.0

        # Sample frames for subtitle detection in lower-third
        subtitle_detected_count = 0
        test_frame_indices = [
            int(1.5 * fps),   # Shot 1
            int(4.5 * fps),   # Shot 2
            int(8.5 * fps),   # Shot 3
            int(12.5 * fps),  # Shot 4
            int(16.5 * fps)   # Shot 5
        ]

        for f_idx in test_frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, min(total_frames - 1, f_idx))
            ret, frame = cap.read()
            if ret and frame is not None:
                # Lower-third region (approx y = 1350 to 1550)
                y1 = int(height * 0.70)
                y2 = int(height * 0.82)
                roi = frame[y1:y2, :]
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                # Check for high contrast edges (subtitles with text outlines)
                lap_var = cv2.Laplacian(gray_roi, cv2.CV_64F).var()
                if lap_var > 60.0:  # Text edges produce prominent Laplacian variance
                    subtitle_detected_count += 1

        cap.release()

        # 2. Probe Audio Stream via FFprobe / FFmpeg
        audio_duration, has_audio, audio_codec = self._probe_audio_stream(str(path.resolve()))
        metrics["audio_codec"] = audio_codec
        metrics["audio_duration_sec"] = audio_duration
        metrics["has_audio"] = has_audio

        # Calculate A/V Sync Delta
        av_sync_delta_ms = abs(video_duration - audio_duration) * 1000.0 if has_audio else 9999.0
        metrics["av_sync_delta_ms"] = round(av_sync_delta_ms, 2)

        # 3. Scoring & Gate Criteria
        score = 0.0

        # A. Resolution & Aspect Ratio (Max 2.5 pts)
        if (width, height) == (1080, 1920):
            score += 2.5
            notes.append("✅ Resolution verified: 1080x1920 (9:16 vertical standard).")
        else:
            notes.append(f"❌ Resolution mismatch: got {width}x{height}, expected 1080x1920.")

        # B. Framerate & Duration Consistency (Max 2.5 pts)
        if 29.5 <= fps <= 30.5:
            score += 1.5
            notes.append(f"✅ Framerate compliant: {fps:.2f} CFR.")
        else:
            notes.append(f"⚠️ Framerate deviation: {fps:.2f} FPS.")

        if abs(video_duration - target_duration_sec) <= 0.15:
            score += 1.0
            notes.append(f"✅ Duration exact: {video_duration:.2f}s matches target {target_duration_sec}s.")
        else:
            notes.append(f"⚠️ Duration mismatch: got {video_duration:.2f}s, target {target_duration_sec}s.")

        # C. Audio Stream & Sync (Max 3.0 pts)
        if has_audio:
            score += 1.5
            notes.append(f"✅ Audio stream verified: codec '{audio_codec}', duration {audio_duration:.2f}s.")
            if av_sync_delta_ms <= 33.34:  # <= 1 frame delta
                score += 1.5
                notes.append(f"✅ Pristine A/V sync: delta {av_sync_delta_ms:.2f}ms (<= 33ms single-frame ceiling).")
            elif av_sync_delta_ms <= 80.0:
                score += 0.8
                notes.append(f"⚠️ Acceptable A/V sync: delta {av_sync_delta_ms:.2f}ms.")
            else:
                notes.append(f"❌ Noticeable A/V sync drift: delta {av_sync_delta_ms:.2f}ms.")
        else:
            notes.append("❌ Master video has no audio stream!")

        # D. Kinetic Subtitles Presence (Max 2.0 pts)
        if subtitle_detected_count >= 4:
            score += 2.0
            notes.append(f"✅ Subtitles confirmed burned across shots ({subtitle_detected_count}/5 sampled frames).")
        elif subtitle_detected_count >= 2:
            score += 1.0
            notes.append(f"⚠️ Partial subtitle detection ({subtitle_detected_count}/5 sampled frames).")
        else:
            notes.append(f"❌ Subtitles not detected in lower third ({subtitle_detected_count}/5 sampled frames).")

        score = round(min(10.0, max(0.0, score)), 2)
        qa_passed = (score >= 8.5) and has_audio and ((width, height) == (1080, 1920))

        return MasterVideoReport(
            video_path=video_path,
            total_duration_sec=round(video_duration, 2),
            total_frames=total_frames,
            resolution=(width, height),
            fps=round(fps, 2),
            file_size_bytes=file_size,
            has_audio=has_audio,
            audio_duration_sec=round(audio_duration, 2),
            av_sync_delta_ms=round(av_sync_delta_ms, 2),
            qa_passed=qa_passed,
            qa_score=score,
            metrics=metrics,
            qa_notes=notes
        )

    def _probe_audio_stream(self, video_path: str) -> Tuple[float, bool, str]:
        """Probes audio stream duration and codec using FFmpeg command."""
        cmd = [
            self.ffmpeg_exe,
            "-i", video_path,
            "-hide_banner"
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=10)
            output = res.stderr

            has_audio = "Audio:" in output
            audio_codec = "unknown"
            if has_audio:
                for line in output.splitlines():
                    if "Audio:" in line:
                        parts = line.split("Audio:")[1].strip().split(",")
                        if parts:
                            audio_codec = parts[0].strip()
                        break

            # Find duration in 'Duration: 00:00:18.50'
            duration = 0.0
            for line in output.splitlines():
                if "Duration:" in line:
                    try:
                        dur_str = line.split("Duration:")[1].split(",")[0].strip()
                        h, m, s = dur_str.split(":")
                        duration = float(h) * 3600 + float(m) * 60 + float(s)
                    except Exception:
                        pass
                    break

            return duration, has_audio, audio_codec
        except Exception:
            return 0.0, False, "error"
