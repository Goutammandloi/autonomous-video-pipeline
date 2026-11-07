"""
Project Origin: The Shattered Crown
Episode 01: "The Gilded Throne" - Master Timeline Assembly & Kinetic Subtitle Burning
Concatenates 13 video clips (1,800 frames), burns golden kinetic subtitles,
multiplexes 44.1kHz AAC stereo audio, and performs multi-vector QA audit.
"""

import sys
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import ProductionShotDeck
from src.audio import TTSEngine, VoicePersona
from src.assembly import (
    TimelineAssembler,
    SubtitleBurner,
    AssemblyQAEvaluator,
    AssemblyConfig,
    SubtitleStyleConfig
)

def main():
    print("=" * 70)
    print("EPISODE 01: MASTER TIMELINE ASSEMBLY & KINETIC SUBTITLE BURNING")
    print("=" * 70)

    deck_path = root_dir / "data" / "shot_decks" / "project_origin_ep01_shot_deck.json"
    with open(deck_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    deck = ProductionShotDeck(**data)

    clips_dir = root_dir / "data" / "video_clips" / "ep01"
    clip_paths = [
        str(clips_dir / f"shot_{shot.shot_id}_clip.mp4")
        for shot in deck.shots
    ]
    for p in clip_paths:
        assert Path(p).exists(), f"Missing required video clip: {p}"

    master_audio = root_dir / "data" / "audio" / "project_origin_ep01_soundtrack.wav"
    assert master_audio.exists(), f"Missing master audio: {master_audio}"

    final_dir = root_dir / "data" / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    output_video = final_dir / "project_origin_ep01_master_9x16.mp4"

    # Reconstruct dialogue tracks for subtitle timing
    tts = TTSEngine(output_dir=str(root_dir / "data" / "audio"))
    tts.register_persona(VoicePersona(persona_name="Ash Ketchum", voice_identifier="en-US-GuyNeural", gender="male", provider="windows-sapi"))
    tts.register_persona(VoicePersona(persona_name="Vance Stirling", voice_identifier="en-GB-RyanNeural", gender="male", provider="windows-sapi"))
    tracks = tts.synthesize_deck_dialogues(deck)

    # Subtitle Burner & Assembler
    burner = SubtitleBurner(style_config=SubtitleStyleConfig(
        font_size=42,
        active_word_color=(255, 220, 0, 255),  # Anime Electric Gold
        inactive_word_color=(255, 255, 255, 255),
        box_color=(15, 23, 42, 220),           # Dark Navy Slate backdrop
        vertical_position_ratio=0.72           # Perfect vertical safe zone (above bottom UI)
    ))
    assembler = TimelineAssembler(
        config=AssemblyConfig(
            target_width=1080,
            target_height=1920,
            target_fps=30.0,
            video_codec="libx264",
            crf=18,
            audio_codec="aac",
            audio_bitrate="192k"
        ),
        subtitle_burner=burner
    )

    subtitle_segments = SubtitleBurner.segments_from_shot_deck_and_tracks(deck, tracks)

    print(f"\n🎬 Assembling 60.0s Master Video from {len(clip_paths)} clips...")
    assembler.assemble_master_video(
        clip_paths=clip_paths,
        master_audio_path=str(master_audio),
        output_video_path=str(output_video),
        subtitle_segments=subtitle_segments
    )

    print(f"\n✅ Assembly Complete: {output_video.name} ({output_video.stat().st_size / (1024*1024):.2f} MB)")

    # Execute Gatekeeper QA Audit
    evaluator = AssemblyQAEvaluator()
    report = evaluator.evaluate_master_video(str(output_video), target_duration_sec=60.0)

    print("\n" + "-" * 50)
    print("📊 MASTER EPISODE 01 QA REPORT")
    print("-" * 50)
    print(f"File Path:       {report.video_path}")
    print(f"File Size:       {report.metrics.get('file_size_mb')} MB")
    print(f"Resolution:      {report.metrics.get('width')}x{report.metrics.get('height')}")
    print(f"Framerate:       {report.metrics.get('fps')} FPS ({report.metrics.get('total_frames')} frames)")
    print(f"Video Duration:  {report.metrics.get('video_duration_sec')}s")
    print(f"Audio Duration:  {report.metrics.get('audio_duration_sec')}s")
    print(f"A/V Sync Delta:  {report.av_sync_delta_ms} ms (Single-frame threshold <= 33.3ms)")
    print(f"QA Score:        {report.qa_score}/10.0")
    print(f"QA Passed:       {report.qa_passed}")
    print("-" * 50)

    assert report.qa_passed, "Master video must pass assembly QA gate!"

if __name__ == "__main__":
    main()
