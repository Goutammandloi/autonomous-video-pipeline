"""
Project Origin: The Shattered Crown
Episode 01: "The Gilded Throne" - Audio Synthesis & Acoustic Mastering
Synthesizes English voiceovers for Ash Ketchum and Vance Stirling,
applies -12 dB dynamic sidechain ducking, and masters to -14.0 LUFS.
"""

import sys
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import ProductionShotDeck
from src.audio import TTSEngine, VoicePersona, AcousticMixer, SubtitleGenerator

def main():
    print("=" * 70)
    print("EPISODE 01: ACOUSTIC MASTERING & DIALOGUE SYNTHESIS")
    print("=" * 70)

    deck_path = root_dir / "data" / "shot_decks" / "project_origin_ep01_shot_deck.json"
    with open(deck_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    deck = ProductionShotDeck(**data)

    audio_dir = root_dir / "data" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    tts = TTSEngine(output_dir=str(audio_dir))

    # Register Project Origin voice personas
    tts.register_persona(VoicePersona(
        persona_name="Ash Ketchum",
        voice_identifier="en-US-GuyNeural",
        gender="male",
        speaking_rate=1.05,
        provider="windows-sapi"
    ))
    tts.register_persona(VoicePersona(
        persona_name="Vance Stirling",
        voice_identifier="en-GB-RyanNeural",
        gender="male",
        speaking_rate=0.95,
        provider="windows-sapi"
    ))

    # Synthesize dialogue tracks
    tracks = tts.synthesize_deck_dialogues(deck)
    print(f"\n✅ Synthesized {len(tracks)} dialogue tracks:")
    for t in tracks:
        print(f"  - Shot {t.shot_id} [{t.speaker}]: {t.duration_sec:.2f}s | Line: \"{t.dialogue_line}\"")

    # Export SRT captions
    srt_path = audio_dir / "project_origin_ep01_subtitles.srt"
    SubtitleGenerator.export_srt(tracks, str(srt_path))
    print(f"\n✅ Exported Subtitles to: {srt_path.name}")

    # Mix and master soundtrack
    master_wav = audio_dir / "project_origin_ep01_soundtrack.wav"
    mixer = AcousticMixer(sample_rate=44100)
    report = mixer.mix_soundtrack(
        shot_deck=deck,
        dialogue_tracks=tracks,
        output_path=str(master_wav),
        ducking_gain_reduction_db=12.0
    )

    print("\n" + "-" * 50)
    print("📊 ACOUSTIC MASTER REPORT")
    print("-" * 50)
    print(f"Master File:         {report.master_audio_path}")
    print(f"Total Duration:      {report.total_duration_sec:.2f}s (Target: 60.0s)")
    print(f"Integrated Loudness: {report.integrated_lufs} LUFS (Target: -14.0 LUFS)")
    print(f"True Peak:           {report.true_peak_dbtp} dBTP (Ceiling: -1.0 dBTP)")
    print(f"Sidechain Ducking:   {report.measured_ducking_attenuation_db} dB")
    print(f"Acoustic Gate Pass:  {report.passes_acoustic_gate}")
    print("-" * 50)

if __name__ == "__main__":
    main()
