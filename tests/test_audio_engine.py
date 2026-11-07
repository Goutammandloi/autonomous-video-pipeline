import json
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import ProductionShotDeck
from src.audio import TTSEngine, AcousticMixer, SubtitleGenerator

def run_test():
    print("=== Testing Feature 3: Voiceover, Sidechain Ducking & Acoustic Mastering ===")

    deck_path = root_dir / "data" / "shot_decks" / "appin_career_ka_asli_netflix_shot_deck.json"
    assert deck_path.exists(), f"Shot deck file not found: {deck_path}"

    with open(deck_path, "r", encoding="utf-8") as f:
        deck_data = json.load(f)
    shot_deck = ProductionShotDeck.model_validate(deck_data)

    audio_dir = root_dir / "data" / "audio"
    tts = TTSEngine(output_dir=str(audio_dir))
    mixer = AcousticMixer(sample_rate=44100)

    # 1. Synthesize Dialogues
    dialogue_tracks = tts.synthesize_deck_dialogues(shot_deck)
    print(f"\n[Result] Synthesized {len(dialogue_tracks)} Dialogue Audio Tracks:")
    for track in dialogue_tracks:
        print(f"  Shot {track.shot_id} ({track.speaker}): {track.duration_sec}s | Words: {len(track.words)}")
        print(f"    Sample Word Timings: {[w.word for w in track.words[:5]]}...")
        assert Path(track.audio_path).exists(), f"File not found: {track.audio_path}"
        assert track.duration_sec > 0.5, "Duration too short"

    # 2. Export Captions / SRT
    srt_path = audio_dir / "subtitles.srt"
    srt_content = SubtitleGenerator.export_srt(dialogue_tracks, str(srt_path))
    print(f"\n[Result] Generated Subtitles SRT ({srt_path}):")
    print("\n".join(srt_content.splitlines()[:12]))
    assert srt_path.exists(), "SRT file was not created"

    # 3. Master Audio Mix with Sidechain Ducking
    master_path = audio_dir / "master_soundtrack.wav"
    report = mixer.mix_soundtrack(
        shot_deck=shot_deck,
        dialogue_tracks=dialogue_tracks,
        output_path=str(master_path),
        ducking_gain_reduction_db=12.0
    )

    print(f"\n[Result] Acoustic Master Report:")
    print(f"  Master File: {report.master_audio_path}")
    print(f"  Duration: {report.total_duration_sec}s")
    print(f"  Integrated Loudness: {report.integrated_lufs} LUFS (Target: -14.0 LUFS)")
    print(f"  True Peak: {report.true_peak_dbtp} dBTP (Target <= -1.0 dBTP)")
    print(f"  Sidechain Ducking Depth: {report.measured_ducking_attenuation_db} dB (Target >= 10.0 dB)")
    print(f"  Passes Acoustic Gate: {report.passes_acoustic_gate}")

    assert Path(report.master_audio_path).exists(), "Master WAV file not created!"
    assert report.passes_acoustic_gate, f"Acoustic QA failed: {report.qa_notes}"
    print("\n✅ All Feature 3 Assertions Passed Successfully!")

if __name__ == "__main__":
    run_test()
