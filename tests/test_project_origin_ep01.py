"""
Unit & Integration Test: Project Origin Episode 01 Production Validation
Asserts duration, word ceiling, vertical safe zone compliance, and QA gate.
"""

import json
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import ProductionShotDeck, AspectRatio
from src.scripting.generator import ScriptingEngine

def test_ep01_shot_deck():
    shot_deck_path = root_dir / "data" / "shot_decks" / "project_origin_ep01_shot_deck.json"
    assert shot_deck_path.exists(), f"Shot deck file does not exist at {shot_deck_path}"

    with open(shot_deck_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    deck = ProductionShotDeck(**data)
    assert deck.aspect_ratio == AspectRatio.VERTICAL_9_16
    assert deck.target_total_duration_sec == 60.0

    total_duration = sum(s.duration_sec for s in deck.shots)
    assert round(total_duration, 2) == 60.0, f"Expected 60.0s total, got {total_duration}s"

    # Verify dialogue word ceiling (85 words max for 60s micro-episode)
    total_words = 0
    for s in deck.shots:
        if s.dialogue:
            words = len(s.dialogue.line.split())
            total_words += words
    assert total_words <= 85, f"Spoken dialogue ({total_words} words) exceeds 85-word ceiling"

    # Verify Hook (Shot 1 <= 3.5s and <= 12 words)
    shot1 = deck.shots[0]
    assert shot1.duration_sec <= 3.5, f"Shot 1 duration ({shot1.duration_sec}s) exceeds 3.5s hook threshold"
    assert shot1.dialogue is not None, "Shot 1 must contain a hook line"
    assert len(shot1.dialogue.line.split()) <= 12, "Shot 1 hook line too verbose"

    # Verify Adversarial QA Score
    engine = ScriptingEngine(output_dir=str(root_dir / "data" / "shot_decks"))
    critique = engine.evaluate_shot_deck(deck)
    assert critique.passes_quality_gate, f"Shot deck failed QA gate: {critique.overall_score}"
    assert critique.overall_score >= 8.5, f"QA score ({critique.overall_score}) below 8.5"

    print(f"✅ test_ep01_shot_deck passed! (Shots: {len(deck.shots)}, Duration: {total_duration}s, Words: {total_words}, QA: {critique.overall_score}/10)")

if __name__ == "__main__":
    test_ep01_shot_deck()
