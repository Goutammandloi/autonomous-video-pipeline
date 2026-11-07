"""
Autonomous AI Video Pipeline: Stage 5 Test Suite
Tests programmatic timeline assembly, kinetic subtitle burning,
audio muxing, and multi-vector master video QA evaluation.
"""

import json
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import ProductionShotDeck
from src.audio import TTSEngine
from src.assembly import (
    AssemblyConfig,
    SubtitleStyleConfig,
    SubtitleBurner,
    TimelineAssembler,
    AssemblyQAEvaluator
)


def run_test():
    print("=== Testing Feature 5: Timeline Assembly, Kinetic Subtitles & Video Master QA ===")

    deck_path = root_dir / "data" / "shot_decks" / "project_origin_ep01_shot_deck.json"
    assert deck_path.exists(), f"Shot deck file not found: {deck_path}"

    with open(deck_path, "r", encoding="utf-8") as f:
        deck_data = json.load(f)
    shot_deck = ProductionShotDeck.model_validate(deck_data)

    video_clips_dir = root_dir / "data" / "video_clips" / "ep01"
    clip_paths = [
        str(video_clips_dir / f"shot_{i}_clip.mp4")
        for i in range(1, 14)
    ]
    for p in clip_paths:
        assert Path(p).exists(), f"Video clip missing: {p}"

    master_audio_path = root_dir / "data" / "audio" / "project_origin_ep01_soundtrack.wav"
    assert master_audio_path.exists(), f"Master audio missing: {master_audio_path}"

    final_dir = root_dir / "data" / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    output_video_path = str(final_dir / "project_origin_ep01_master_9x16.mp4")

    # 1. Build Subtitle Segments
    audio_dir = root_dir / "data" / "audio"
    tts = TTSEngine(output_dir=str(audio_dir))
    dialogue_tracks = tts.synthesize_deck_dialogues(shot_deck)

    subtitle_segments = SubtitleBurner.segments_from_shot_deck_and_tracks(
        shot_deck=shot_deck,
        dialogue_tracks=dialogue_tracks
    )
    print(f"\n[Result] Constructed {len(subtitle_segments)} Kinetic Subtitle Segments:")
    for seg in subtitle_segments:
        print(f"  Shot {seg.shot_id} [{seg.speaker}]: {seg.start_time_sec}s -> {seg.end_time_sec}s ({len(seg.words)} words)")
        print(f"    Line: \"{seg.full_text[:40]}...\"")

    # 2. Assemble Master Video with Synchronized AAC Audio & Subtitle Overlays
    style = SubtitleStyleConfig(
        font_size=54,
        primary_color=(255, 255, 255),
        highlight_color=(255, 220, 0),    # Vibrant Yellow Pop
        speaker_color=(0, 230, 255),      # Neon Cyan
        stroke_color=(10, 10, 10),
        stroke_width=5,
        bg_pill_color=(15, 15, 15, 185),
        position_y_ratio=0.74
    )
    burner = SubtitleBurner(style_config=style)

    config = AssemblyConfig(
        resolution=(1080, 1920),
        fps=30.0,
        video_codec="libx264",
        preset="fast",
        crf=18,
        pixel_format="yuv420p",
        audio_codec="aac",
        audio_bitrate="192k",
        burn_subtitles=True
    )
    assembler = TimelineAssembler(config=config, subtitle_burner=burner)

    assembled_path = assembler.assemble_master_video(
        clip_paths=clip_paths,
        master_audio_path=str(master_audio_path),
        output_video_path=output_video_path,
        subtitle_segments=subtitle_segments
    )
    assert Path(assembled_path).exists(), "Master video file was not created!"

    # 3. Autonomous QA Audit & Gatekeeper Evaluation
    evaluator = AssemblyQAEvaluator()
    report = evaluator.evaluate_master_video(assembled_path, target_duration_sec=shot_deck.target_total_duration_sec)

    print("\n[Result] Master Video QA Evaluation Report:")
    print(f"  Master Video File: {report.video_path}")
    print(f"  File Size: {report.metrics.get('file_size_mb')} MB")
    print(f"  Resolution: {report.resolution[0]}x{report.resolution[1]} (Aspect Ratio: 9:16)")
    print(f"  Framerate: {report.fps} FPS (Total Frames: {report.total_frames})")
    print(f"  Video Duration: {report.total_duration_sec}s | Audio Duration: {report.audio_duration_sec}s")
    print(f"  A/V Sync Delta: {report.av_sync_delta_ms} ms (Single-frame threshold <= 33.3ms)")
    print(f"  QA Score: {report.qa_score}/10.0")
    print(f"  QA Gate Passed: {report.qa_passed}")
    print("  QA Findings:")
    for note in report.qa_notes:
        print(f"    {note}")

    assert report.qa_passed, f"Master video failed QA evaluation (Score: {report.qa_score}/10.0)"
    print("\n🎯 STAGE 5 VERIFICATION COMPLETE: Master 9:16 vertical video produced and verified.")


if __name__ == "__main__":
    run_test()
