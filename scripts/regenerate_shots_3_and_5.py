"""
Regenerate Shot 3 (Vance Stirling Close-up) and Shot 5 (Consortium Enforcers Standoff)
for Project Origin: The Shattered Crown. Replaces lingering Appin placeholder keyframes.
"""

import sys
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import ProductionShotDeck
from src.visuals.generator import KeyframeGenerator
from src.motion.motion_engine import MotionEngine

def main():
    print("=" * 70)
    print("REGENERATING POKEMON KEYFRAMES & CLIPS FOR SHOT 3 & SHOT 5")
    print("=" * 70)

    deck_path = root_dir / "data" / "shot_decks" / "project_origin_ep01_shot_deck.json"
    with open(deck_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    deck = ProductionShotDeck(**data)

    kf_dir = root_dir / "data" / "keyframes"
    kg = KeyframeGenerator(output_dir=str(kf_dir))

    # Force delete existing shot 3 and shot 5 keyframes
    for s_id in [3, 5]:
        p = kf_dir / f"shot_{s_id}_keyframe.png"
        if p.exists():
            p.unlink()
            print(f"Removed old placeholder keyframe: {p.name}")

    # Render clean Pokemon keyframes for shots 3 and 5
    for shot in deck.shots:
        if shot.shot_id in [3, 5]:
            print(f"\nRendering Shot {shot.shot_id} [{shot.narrative_beat}]...")
            asset = kg.generate_shot_keyframe(shot, deck.character_bible)
            print(f"✅ Generated Pokemon keyframe: {asset.file_path}")

    # Re-render motion clips for shots 3 and 5 in ep01
    clips_dir = root_dir / "data" / "video_clips" / "ep01"
    me = MotionEngine(output_dir=str(clips_dir), fps=30)
    keyframes_map = {
        3: str(kf_dir / "shot_3_keyframe.png"),
        5: str(kf_dir / "shot_5_keyframe.png")
    }

    for shot in deck.shots:
        if shot.shot_id in [3, 5]:
            clip = me.generate_shot_video_clip(shot, keyframes_map[shot.shot_id])
            print(f"✅ Re-rendered motion clip: {clip.file_path} ({clip.total_frames} frames)")

    print("\n✅ Successfully updated Shots 3 & 5 to 100% Pokemon Project Origin!")

if __name__ == "__main__":
    main()
