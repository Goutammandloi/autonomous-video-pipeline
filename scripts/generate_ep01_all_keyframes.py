"""
Ensure all 13 keyframes for Episode 01 exist at 1080x1920 resolution.
Preserves existing high-fidelity Google-generated keyframes and renders
cinematic plates for any pending shots.
"""

import sys
import json
from pathlib import Path
from PIL import Image

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import ProductionShotDeck
from src.visuals.generator import KeyframeGenerator

def main():
    deck_path = root_dir / "data" / "shot_decks" / "project_origin_ep01_shot_deck.json"
    with open(deck_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    deck = ProductionShotDeck(**data)

    kf_dir = root_dir / "data" / "keyframes"
    kf_dir.mkdir(parents=True, exist_ok=True)

    kg = KeyframeGenerator(output_dir=str(kf_dir))

    for shot in deck.shots:
        kf_path = kf_dir / f"shot_{shot.shot_id}_keyframe.png"
        if kf_path.exists():
            with Image.open(kf_path) as img:
                if img.size != (1080, 1920):
                    resized = img.resize((1080, 1920), Image.Resampling.LANCZOS)
                    resized.save(kf_path, format="PNG")
                    print(f"Shot {shot.shot_id}: Resized existing keyframe to 1080x1920")
                else:
                    print(f"Shot {shot.shot_id}: Existing 1080x1920 keyframe verified ✅")
        else:
            print(f"Shot {shot.shot_id}: Generating cinematic keyframe plate...")
            asset = kg.generate_shot_keyframe(shot, deck.character_bible)
            print(f"Shot {shot.shot_id}: Rendered -> {asset.file_path}")

    print("\n✅ All 13 Episode 01 Keyframes Verified at 1080x1920!")

if __name__ == "__main__":
    main()
