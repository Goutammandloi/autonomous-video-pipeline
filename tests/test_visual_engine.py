import json
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import ProductionShotDeck
from src.visuals import KeyframeGenerator

def run_test():
    print("=== Testing Feature 2: Visual Bible & Keyframe Generation Engine ===")
    
    deck_path = root_dir / "data" / "shot_decks" / "appin_career_ka_asli_netflix_shot_deck.json"
    assert deck_path.exists(), f"Shot deck file not found: {deck_path}"
    
    with open(deck_path, "r", encoding="utf-8") as f:
        deck_data = json.load(f)
    shot_deck = ProductionShotDeck.model_validate(deck_data)
    
    generator = KeyframeGenerator(
        output_dir=str(root_dir / "data" / "keyframes"),
        width=1080,
        height=1920
    )
    
    assets = generator.generate_shot_deck_keyframes(shot_deck)
    
    print(f"\n[Test Result] Generated {len(assets)} Keyframes:")
    for asset in assets:
        qa = asset.qa_result
        print(f"\nShot {asset.shot_id} Keyframe Asset:")
        print(f"  Path: {asset.file_path}")
        print(f"  Resolution: {asset.metadata.width}x{asset.metadata.height} ({asset.metadata.aspect_ratio})")
        print(f"  Status: {asset.status}")
        print(f"  QA Score: {qa.overall_score}/10 (Composition: {qa.composition_score}, Adherence: {qa.prompt_adherence_score})")
        print(f"  Prompt Preview: {asset.metadata.prompt_used[:120]}...")
        assert Path(asset.file_path).exists(), f"File {asset.file_path} was not created!"
        assert qa.passes_qa, f"Shot {asset.shot_id} failed QA!"
        assert asset.metadata.width == 1080 and asset.metadata.height == 1920, "Resolution must be 1080x1920"

    print("\n✅ All Feature 2 Assertions Passed Successfully!")

if __name__ == "__main__":
    run_test()
