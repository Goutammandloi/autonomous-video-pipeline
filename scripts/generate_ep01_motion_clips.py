"""
Project Origin: The Shattered Crown
Episode 01: "The Gilded Throne" - Motion Video Clips Synthesis
Synthesizes 13 CFR 30.0 FPS vertical video clips (1080x1920) with optical flow QA.
"""

import sys
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.scripting.schemas import ProductionShotDeck
from src.motion.motion_engine import MotionEngine

def main():
    print("=" * 70)
    print("EPISODE 01: 30 FPS I2V MOTION SYNTHESIS")
    print("=" * 70)

    deck_path = root_dir / "data" / "shot_decks" / "project_origin_ep01_shot_deck.json"
    with open(deck_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    deck = ProductionShotDeck(**data)

    kf_dir = root_dir / "data" / "keyframes"
    clips_dir = root_dir / "data" / "video_clips" / "ep01"
    clips_dir.mkdir(parents=True, exist_ok=True)

    keyframes_map = {
        shot.shot_id: str(kf_dir / f"shot_{shot.shot_id}_keyframe.png")
        for shot in deck.shots
    }

    engine = MotionEngine(output_dir=str(clips_dir), fps=30)
    clips = engine.generate_deck_video_clips(deck, keyframes_map)

    print(f"\n✅ Synthesized {len(clips)} vertical video clips:")
    total_frames = 0
    for c in clips:
        total_frames += c.total_frames
        print(f"  - Shot {c.shot_id:02d} ({c.duration_sec:.1f}s, {c.total_frames} frames): Flow Z={c.qa_result.max_flow_z_score:.2f} -> {c.status}")

    print(f"\nTotal Frames Rendered: {total_frames} frames (Target: 1,800 frames @ 30.00 CFR / 60.0s)")

if __name__ == "__main__":
    main()
