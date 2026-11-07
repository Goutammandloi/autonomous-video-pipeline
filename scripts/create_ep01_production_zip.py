"""
Project Origin: The Shattered Crown
Episode 01: "The Gilded Throne" - Visual Production Pack & Zip Flow Generator
Compiles:
  - 1-Click Copy-Paste Prompts for Midjourney v6 / Niji 6
  - Structured FLUX.1 [dev] & SDXL Prompts with LoRA triggers
  - Kling AI / Runway Gen-3 / Luma I2V Motion Prompts
  - Individual Shot Production Cards (1-13)
  - ComfyUI Batch Import JSON
  - Automated Zip Archive packaging
"""

import os
import json
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DECK_PATH = ROOT_DIR / "data" / "shot_decks" / "project_origin_ep01_shot_deck.json"
EXPORT_DIR = ROOT_DIR / "data" / "exports" / "ep01_visual_production_pack"
SHOTS_DIR = EXPORT_DIR / "shots"
ZIP_OUTPUT = ROOT_DIR / "data" / "exports" / "project_origin_ep01_production_pack.zip"

def build_production_pack():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    SHOTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(DECK_PATH, "r", encoding="utf-8") as f:
        deck = json.load(f)

    # 1. Generate master overview JSON
    overview_path = EXPORT_DIR / "00_MASTER_OVERVIEW.json"
    with open(overview_path, "w", encoding="utf-8") as f:
        json.dump(deck, f, indent=2)

    # 2. Midjourney / Niji 6 Ready-to-Paste File
    mj_lines = []
    mj_lines.append("# ======================================================================")
    mj_lines.append("# PROJECT ORIGIN: THE SHATTERED CROWN — EPISODE 01")
    mj_lines.append("# MIDJOURNEY v6 / NIJI 6 READY-TO-PASTE PROMPT SHEET (9:16 VERTICAL)")
    mj_lines.append("# ======================================================================\n")

    # 3. FLUX / SDXL JSON
    flux_dict = {"episode": 1, "aspect_ratio": "9:16", "resolution": "1080x1920", "shots": []}

    # 4. Kling AI / Runway Gen-3 Motion Sheet
    motion_lines = []
    motion_lines.append("# ======================================================================")
    motion_lines.append("# KLING AI / RUNWAY GEN-3 / LUMA DREAM MACHINE I2V MOTION PROMPTS")
    motion_lines.append("# ======================================================================\n")

    # 5. ComfyUI Batch Prompts
    comfy_batch = []

    for shot in deck["shots"]:
        s_id = shot["shot_id"]
        beat = shot["narrative_beat"]
        dur = shot["duration_sec"]
        v = shot["visual"]
        dia = shot["dialogue"]
        aud = shot["audio"]

        # Midjourney format: /imagine prompt: ... --ar 9:16 --style raw --v 6.1 --niji 6
        mj_prompt = f"**Shot {s_id:02d} [{beat}] ({dur}s)**:\n/imagine prompt: {v['image_prompt']} --ar 9:16 --style raw --niji 6\n"
        mj_lines.append(mj_prompt)

        # FLUX / SDXL Entry
        flux_entry = {
            "shot_id": s_id,
            "beat": beat,
            "duration_sec": dur,
            "positive_prompt": v["image_prompt"],
            "negative_prompt": v["negative_prompt"],
            "guidance_scale": 7.5,
            "steps": 35,
            "seed": 42000 + s_id,
            "sampler": "Euler a",
            "width": 1080,
            "height": 1920,
            "characters": v["characters_present"]
        }
        flux_dict["shots"].append(flux_entry)

        # Kling / Runway Motion
        motion_entry = (
            f"**Shot {s_id:02d} ({dur}s) — Camera: {v['camera_movement']} | Framing: {v['camera_angle']}**\n"
            f"Input Keyframe: shot_{s_id:02d}_keyframe.png\n"
            f"Motion Prompt: {v['motion_prompt']}\n"
            f"Motion Intensity: 6 / 10\n"
            f"Camera Vector: {v['camera_movement']}\n"
        )
        motion_lines.append(motion_entry)

        # ComfyUI queue item
        comfy_batch.append({
            "shot_id": s_id,
            "prompt": v["image_prompt"],
            "negative": v["negative_prompt"],
            "width": 1080,
            "height": 1920,
            "seed": 88000 + s_id
        })

        # Individual Shot Markdown Card
        shot_md_path = SHOTS_DIR / f"shot_{s_id:02d}_{beat.lower().replace(' ', '_').replace('/', '_')}.md"
        spoken = f'**{dia["speaker"]}**: "{dia["line"]}" *(Delivery: {dia["emotion"]})*' if dia else "*No spoken dialogue (Action / Ambience)*"
        
        shot_md_content = f"""# 🎬 Episode 01 — Shot {s_id:02d}: {beat}

- **Timeline Window:** `{shot["start_time_sec"]:.1f}s` to `{shot["end_time_sec"]:.1f}s` (`{dur:.1f}s` duration)
- **Framing & Angle:** `{v["camera_angle"]}`
- **Camera Dynamics:** `{v["camera_movement"]}`
- **Characters Present:** `{', '.join(v["characters_present"])}`

---

## 🎨 Visual Generation Prompts (9:16 Vertical: 1080x1920)

### Midjourney v6 / Niji 6 (Ready to Paste)
```text
{v["image_prompt"]} --ar 9:16 --style raw --niji 6
```

### FLUX.1 [dev] / SDXL Prompt
```text
{v["image_prompt"]}
```

### Negative Prompt
```text
{v["negative_prompt"]}
```

---

## 🎥 Motion Synthesis (Kling AI / Runway Gen-3 / Luma I2V)

- **Input Frame:** `shot_{s_id:02d}_keyframe.png`
- **Motion Trajectory:** `{v["camera_movement"]}`
- **I2V Generation Prompt:**
```text
{v["motion_prompt"]}
```

---

## 🎙️ Spoken Audio & SFX Cues

- **Spoken Line:** {spoken}
- **BGM Mood:** `{aud["bgm_mood"]}` (Intensity: `{aud["bgm_intensity"]}`)
- **Sound Effects (SFX):** `{', '.join(aud["sfx"])}`

---

## 🔒 Visual Consistency Anchor Tokens
```text
{chr(10).join(shot["character_anchor_tokens"])}
```
"""
        with open(shot_md_path, "w", encoding="utf-8") as f:
            f.write(shot_md_content)

    # Write Midjourney file
    with open(EXPORT_DIR / "prompts_midjourney_niji.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(mj_lines))

    # Write FLUX / SDXL JSON
    with open(EXPORT_DIR / "prompts_flux_sdxl.json", "w", encoding="utf-8") as f:
        json.dump(flux_dict, f, indent=2)

    # Write Kling / Runway Motion file
    with open(EXPORT_DIR / "prompts_video_i2v.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(motion_lines))

    # Write ComfyUI Batch queue file
    with open(EXPORT_DIR / "comfyui_batch_queue.json", "w", encoding="utf-8") as f:
        json.dump(comfy_batch, f, indent=2)

    # Master README
    readme_content = f"""# 📦 PROJECT ORIGIN: THE SHATTERED CROWN — EPISODE 01
## Master Visual Production & Generation Zip Flow Pack

This production pack contains 100% ready-to-paste prompts, negative constraints, camera motion parameters, and batch queue definitions for the **13 shots** of Episode 01: *"The Gilded Throne"*.

---

### 📂 Directory Structure

```
ep01_visual_production_pack/
├── README.md                      <-- This quick start handbook
├── 00_MASTER_OVERVIEW.json        <-- Full 60.0s timeline metadata & audio design
├── prompts_midjourney_niji.txt    <-- 1-Click ready-to-paste prompts for Midjourney / Niji 6
├── prompts_flux_sdxl.json         <-- Structured prompts, seeds, & samplers for FLUX / SDXL
├── prompts_video_i2v.txt          <-- Image-to-Video motion prompts for Kling AI & Runway Gen-3
├── comfyui_batch_queue.json       <-- Direct API queue payload for local ComfyUI clusters
└── shots/                         <-- Detailed individual production cards for Shots 01 to 13
    ├── shot_01_hook_conflict.md
    ├── shot_02_stakes_threat_exposition.md
    ├── shot_03_stakes_monopolization.md
    ├── shot_04_agitation_moral_outrage.md
    ├── shot_05_conflict_escalation_standoff.md
    ├── shot_06_action_battle_climax_command.md
    ├── shot_07_action_window_breach.md
    ├── shot_08_twist_daring_escape_leap.md
    ├── shot_09_action_kinetic_brake.md
    ├── shot_10_twist_recovery_grounding.md
    ├── shot_11_cliffhanger_laser_ambush.md
    ├── shot_12_cliffhanger_apex_predators.md
    └── shot_13_cliffhanger_baton_pass_hook.md
```

---

### 🚀 How to Use

#### 1. For Midjourney / Niji 6:
Open `prompts_midjourney_niji.txt`, copy any `/imagine prompt: ...` line directly into Discord. All commands already include `--ar 9:16 --style raw --niji 6`.

#### 2. For FLUX.1 [dev] or SDXL:
Load `prompts_flux_sdxl.json` or paste from individual cards in `shots/`. Set resolution to `1080x1920`.

#### 3. For Kling AI / Runway Gen-3 / Luma Dream Machine (I2V):
1. Feed the synthesized keyframe into the Image-to-Video tab.
2. Copy the corresponding motion prompt from `prompts_video_i2v.txt`.
3. Set motion intensity to `5-6` and render in vertical format.

#### 4. For Autonomous Pipeline Execution:
Our pipeline can synthesize this entire 60.0s episode locally using `python run_studio.py` or subagent generation.
"""
    with open(EXPORT_DIR / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 6. Compress into ZIP file
    print(f"\n📦 Compressing production pack into {ZIP_OUTPUT.name}...")
    with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in EXPORT_DIR.rglob("*"):
            if file.is_file():
                rel_path = file.relative_to(EXPORT_DIR.parent)
                zipf.write(file, rel_path)

    print(f"✅ Successfully created production zip: {ZIP_OUTPUT} ({ZIP_OUTPUT.stat().st_size} bytes)")

if __name__ == "__main__":
    build_production_pack()
