# 📦 PROJECT ORIGIN: THE SHATTERED CROWN — EPISODE 01
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
