# 🏛️ Autonomous AI Video Engine: Architecture & System Design

## 1. System Overview & Engineering Philosophy

This system is an **autonomous, self-healing, multi-agent pipeline** designed to transform abstract concepts or unstructured prompts into fully rendered, published short-form/long-form videos.

Unlike fragile prompt-chaining scripts that fail silently or produce drift (inconsistent character faces, jarring scene jumps, audio desync, hallucinatory video artifacts), this architecture is built as a **State Machine with Supervisor-Evaluator Quality Gates**.

```
                           ┌────────────────────────────────────────┐
                           │      Supervisor / Monitoring Agent     │
                           │  (Evaluates Quality, Continuity, Sync) │
                           └────▲───────────────▲──────────────▲────┘
                                │               │              │
                       [Eval & Retry]    [Eval & Retry] [Eval & Retry]
                                │               │              │
┌──────────────┐       ┌────────┴───────┐     ┌─┴────────────┐ ┌┴─────────────────┐     ┌────────────────┐
│  Phase 1     │       │  Phase 2       │     │  Phase 3     │ │  Phase 4         │     │  Phase 5       │
│  Ideation &  ├──────►│  Visual Bible  ├────►│  Motion &    ├►│  Timeline Engine ├────►│  Multi-Network │
│  Screenplay  │       │  & Keyframes   │     │  Acoustic    │ │  & Compositing   │     │  Scheduler     │
└──────────────┘       └────────────────┘     └──────────────┘ └──────────────────┘     └────────────────┘
```

---

## 2. Component Layer Breakdown

### Layer 1: Ingestion & Screenplay Generation (`src/scripting/`)
- **Input:** Raw concept, topic, bullet points, or reference event.
- **Agent Roles:**
  - `ConceptArchitectAgent`: Analyzes narrative hooks, viral pacing, emotional arcs, and target audience retention.
  - `ScreenplayWriterAgent`: Produces a strictly typed **Production Shot Deck (JSON schema)** containing:
    - Scene ID, shot index, start/end timestamps.
    - Spoken dialogue, speaker identity, tone/emotion tag.
    - Visual description (foreground, background, camera framing, lighting).
    - Image prompt & Motion prompt (negative prompts, aspect ratio, camera motion vectors).
    - Acoustic cues (sound effects SFX, background music BGM intensity).
- **Quality Gate:** Schema validator + Gemini 2.5 Pro Evaluator scoring hook strength, dialogue naturalness, and visual executability.

---

### Layer 2: Visual Bible & Keyframe Synthesis (`src/visuals/`)
- **Objective:** Prevent character and environmental hallucination across cut transitions.
- **Techniques:**
  - **Anchor Token Chaining:** Maintaining strict character style tokens (e.g., age, exact attire, hair texture, lighting color palette).
  - **Reference Image Conditioning (IP-Adapter / ControlNet / Gemini Image Gen):** Passing keyframe $N-1$ or canonical character portrait to condition scene $N$.
  - **Automated Aspect Ratio & Resolution Enforcement:** 9:16 vertical ($1080 \times 1920$) or 16:9 widescreen ($1920 \times 1080$).
- **Monitoring Agent Check:** Multimodal visual consistency checker (face similarity metric / CLIP embedding distance between character shots). If score $< \tau$, re-roll keyframe with revised prompt weights.

---

### Layer 3: Voiceover & Acoustic Generation (`src/audio/`)
- **Voiceover Synthesis:** Google Cloud Text-to-Speech (Journey/Studio neural voices) or Edge-TTS with SSML tags for emotional pauses, pitch, and pacing.
- **Lip-Sync & Phoneme Alignment:** Forced alignment (e.g., WhisperX / Gentle) to extract word-level timestamps $\rightarrow$ Wav2Lip / SadTalker / LivePortrait / MuseTalk for visual lip synchronization when characters speak on camera.
- **Audio Dynamic Range & Mixing:** Normalization to $-14 \text{ LUFS}$ standard for YouTube/Reels, automatic ducking of background music during dialogue segments.

---

### Layer 4: Motion Synthesis & Dynamic Compositing (`src/motion/` & `src/compositor/`)
- **Image-to-Video (I2V):** Feeding approved keyframes + motion prompt vectors to video models (Google Veo, Kling, Runway Gen-3, Luma Dream Machine, or local Wan2.1 / CogVideoX).
- **Post-Processing & Screen Replacement:** Programmatic OpenCV / FFmpeg perspective warping (e.g., replacing a laptop screen inside a video with an app demo or terminal capture, as demonstrated in the Appin ad project).
- **Temporal Glitch Detection:** Optical flow variance and frame-to-frame SSIM check to catch unnatural morphing or finger distortions.

---

### Layer 5: Assembly, Typography & Mastering (`src/assembly/`)
- **Timeline Engine:** Headless FFmpeg or Remotion (React-based programmatic video rendering).
- **Kinetic Subtitles:** Auto-generated word-by-word highlighted captions synchronized to speech phonemes.
- **Transitions & Audio Ducking:** Cross-fades, whip zooms, riser sound effects placed on cut points.

---

### Layer 6: Scheduling & Multi-Platform Dispatcher (`src/distribution/`)
- **Endpoints:**
  - YouTube Data API v3 (Shorts upload, tags, thumbnail, category, scheduling).
  - Instagram Graph API (Reels publishing container).
  - TikTok Content Posting API.
- **Metadata Generation Agent:** High-CTR titles, SEO descriptions, hashtag clusters, and optimal posting time calculations.

---

## 3. Technology Stack Mapping

| Layer | Primary Tool / API | Fallback / Alternative | Open-Source Option |
| :--- | :--- | :--- | :--- |
| **Orchestration** | Python State Machine / LangGraph | Celery / Temporal | n8n / Prefect |
| **Reasoning & Planning** | Google Gemini 2.5 Pro / Flash | Claude 3.5 Sonnet | DeepSeek-V3 / Ollama |
| **Image Generation** | Google Imagen 3 API | Midjourney API / FLUX.1 | FLUX Schnell / SDXL ComfyUI |
| **Motion (I2V)** | Google Veo / Kling API | Runway Gen-3 / Luma | Wan2.1 / CogVideoX / Animatediff |
| **Audio (TTS)** | Google Cloud Text-to-Speech | ElevenLabs | Edge-TTS / Kokoro-TTS / XTTS-v2 |
| **Lip-Sync** | LivePortrait / MuseTalk | Wav2Lip | SadTalker |
| **Video Assembly** | FFmpeg (CLI & Python-ffmpeg) | Remotion (Node.js) | MoviePy / Moviepy2 |
| **Multimodal QA** | Gemini 2.5 Flash Multimodal | GPT-4o Vision | Qwen2.5-VL / CLIP |
| **Distribution** | YouTube Data API v3 | Meta Graph API | Late (Buffer / Make.com) |
