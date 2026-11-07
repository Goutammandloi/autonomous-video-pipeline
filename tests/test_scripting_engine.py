import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting import ScriptingEngine, AspectRatio

def run_test():
    print("=== Testing Feature 1: Scripting Engine & Supervisor Loop ===")
    engine = ScriptingEngine(output_dir=str(root_dir / "data" / "shot_decks"))

    premise = "Silph-Macro Consortium issues an ultimatum to World Monarch Ash Ketchum to surrender his Pokémon to cybernetic Helix Chips, triggering a skyscraper window blast and rooftop ambush"
    deck, critique = engine.generate_shot_deck(premise=premise, target_duration=60.0)

    print(f"\n[Result] Project: {deck.title}")
    print(f"[Result] Aspect Ratio: {deck.aspect_ratio.value}")
    print(f"[Result] Total Duration: {deck.target_total_duration_sec}s")
    print(f"[Result] Quality Score: {critique.overall_score}/10")
    print(f"[Result] Hook Score: {critique.hook_score}/10")
    print(f"[Result] Passes Gate: {critique.passes_quality_gate}")
    print(f"[Result] Shots Generated: {len(deck.shots)}")

    for shot in deck.shots:
        speaker = shot.dialogue.speaker if shot.dialogue else "None"
        line = f'"{shot.dialogue.line}"' if shot.dialogue else "(no spoken line)"
        print(f"\nShot {shot.shot_id} [{shot.narrative_beat}] ({shot.duration_sec}s):")
        print(f"  Camera: {shot.visual.camera_angle.value} | Motion: {shot.visual.camera_movement.value}")
        print(f"  Speech: {speaker}: {line}")
        print(f"  Image Prompt Preview: {shot.visual.image_prompt[:90]}...")
        print(f"  Motion Prompt Preview: {shot.visual.motion_prompt[:90]}...")
        print(f"  Audio/SFX: Mood={shot.audio.bgm_mood}, SFX={shot.audio.sfx}, Ducking={shot.dialogue.audio_ducking if shot.dialogue else False}")

    assert deck.aspect_ratio == AspectRatio.VERTICAL_9_16, "Aspect ratio must be 9:16 vertical"
    assert critique.passes_quality_gate, "Script must pass adversarial QA gate"
    assert len(deck.shots) >= 4, "Must generate at least 4 shots"
    print("\n✅ All Feature 1 Assertions Passed Successfully!")

if __name__ == "__main__":
    run_test()
