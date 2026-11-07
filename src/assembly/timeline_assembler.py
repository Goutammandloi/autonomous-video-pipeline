"""
Autonomous AI Video Pipeline: Programmatic Timeline Assembler
Concatenates sequential video shots, burns kinetic subtitles, and merges
ITU-R BS.1770 mastered audio into a production-grade 9:16 vertical MP4 video.
"""

import subprocess
from typing import List, Optional
from pathlib import Path
import cv2
import imageio_ffmpeg

from .schemas import AssemblyConfig, SubtitleSegment
from .subtitle_burner import SubtitleBurner


class TimelineAssembler:
    """
    Pipes processed frames directly to FFmpeg with synchronous AAC audio muxing.
    """

    def __init__(
        self,
        config: Optional[AssemblyConfig] = None,
        subtitle_burner: Optional[SubtitleBurner] = None
    ):
        self.config = config or AssemblyConfig()
        self.burner = subtitle_burner or SubtitleBurner()
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def assemble_master_video(
        self,
        clip_paths: List[str],
        master_audio_path: str,
        output_video_path: str,
        subtitle_segments: Optional[List[SubtitleSegment]] = None
    ) -> str:
        """
        Executes frame-accurate timeline concatenation and audio multiplexing.
        """
        out_path = Path(output_video_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        audio_path = Path(master_audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(f"Master soundtrack audio not found: {master_audio_path}")

        for p in clip_paths:
            if not Path(p).exists():
                raise FileNotFoundError(f"Input video clip not found: {p}")

        width, height = self.config.resolution
        fps = self.config.fps

        print(f"\n🎬 Assembling Master Video: {out_path.name}")
        print(f"  Clips to Concatenate: {len(clip_paths)}")
        print(f"  Target Resolution: {width}x{height} (9:16)")
        print(f"  Target Framerate: {fps} FPS")
        print(f"  Master Audio Track: {audio_path.name}")
        print(f"  Subtitle Burning: {'Enabled (Kinetic Highlight)' if self.config.burn_subtitles else 'Disabled'}")

        # Build FFmpeg command with rawvideo stdin pipe
        ffmpeg_cmd = [
            self.ffmpeg_exe,
            "-y",  # Overwrite existing
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{width}x{height}",
            "-pix_fmt", "bgr24",
            "-r", str(fps),
            "-i", "-",  # Video frames from stdin
            "-i", str(audio_path.resolve()),  # Audio track
            "-c:v", self.config.video_codec,
            "-preset", self.config.preset,
            "-crf", str(self.config.crf),
            "-pix_fmt", self.config.pixel_format,
            "-c:a", self.config.audio_codec,
            "-b:a", self.config.audio_bitrate,
            "-shortest",  # Align video and audio stream ends
            "-movflags", "+faststart",  # Web / mobile optimization
            str(out_path.resolve())
        ]

        # Launch FFmpeg process with piped stdin
        proc = subprocess.Popen(
            ffmpeg_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        global_frame_idx = 0
        total_expected_frames = 0

        # First pass: calculate total expected frames
        for clip_p in clip_paths:
            cap = cv2.VideoCapture(clip_p)
            total_expected_frames += int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()

        print(f"  Total Video Frames: {total_expected_frames} (~{total_expected_frames / fps:.2f}s)")

        try:
            for clip_idx, clip_p in enumerate(clip_paths, 1):
                cap = cv2.VideoCapture(clip_p)
                clip_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                print(f"  [Processing Shot {clip_idx}/{len(clip_paths)}] {Path(clip_p).name} ({clip_frames} frames)")

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Ensure resolution matches configuration
                    if (frame.shape[1], frame.shape[0]) != (width, height):
                        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_LANCZOS4)

                    timestamp_sec = global_frame_idx / fps

                    # Burn animated kinetic subtitles
                    if self.config.burn_subtitles and subtitle_segments:
                        frame = self.burner.burn_frame(frame, timestamp_sec, subtitle_segments)

                    # Pipe raw BGR bytes to FFmpeg stdin
                    proc.stdin.write(frame.tobytes())
                    global_frame_idx += 1

                cap.release()

            # Close stdin to signal end of stream to FFmpeg
            proc.stdin.close()
            stdout, stderr = proc.communicate(timeout=60)

            if proc.returncode != 0:
                err_msg = stderr.decode("utf-8", errors="replace")
                raise RuntimeError(f"FFmpeg assembly failed (code {proc.returncode}):\n{err_msg[-500:]}")

        except Exception as e:
            if proc.poll() is None:
                proc.kill()
            raise e

        if not out_path.exists() or out_path.stat().st_size < 10000:
            raise RuntimeError(f"Assembly failed: Output video file not found or empty ({out_path})")

        file_size_mb = out_path.stat().st_size / (1024 * 1024)
        print(f"✅ Successfully Assembled Master Video: {out_path} ({file_size_mb:.2f} MB)")
        return str(out_path.resolve())
