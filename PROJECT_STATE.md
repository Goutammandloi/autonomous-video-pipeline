# 🛰️ Project State & Execution Log: Autonomous Video Pipeline

**System Name:** Autonomous Multi-Agent AI Video Studio  
**Working Directory:** `C:\Users\yashu\.gemini\antigravity\scratch\autonomous-video-pipeline`  
**GitHub Repository:** [Goutammandloi/autonomous-video-pipeline](https://github.com/Goutammandloi/autonomous-video-pipeline)  
**Active Working Branch:** `dev` (Production base: `main`)  
**Engineer:** Yashu (B.Tech CSE - Systems, APIs, Agentic Orchestration)  
**AI Pair Architect:** Antigravity (Google DeepMind Agentic Coding Assistant)  
**Reference Origin:** Chat `4a356c94-6796-42fe-acba-f48c2f68a620` (Appin Technology 9:16 Video Ad Workflow)  
**Last Updated:** 2026-11-07  

---

## 📌 Mission Objective
Transition from semi-manual, human-in-the-loop video generation to a **100% automated, agent-monitored, self-healing pipeline**:
$$\text{Raw Idea} \xrightarrow{\text{Agent 1}} \text{Story Structure} \xrightarrow{\text{Agent 2}} \text{Production Script} \xrightarrow{\text{Agent 3}} \text{Keyframes \& Visuals} \xrightarrow{\text{Agent 4}} \text{Motion \& Audio Clips} \xrightarrow{\text{Agent 5}} \text{Composited Final Video} \xrightarrow{\text{Agent 6}} \text{Multi-Platform Dispatch}$$

With an overarching **Supervisor / Evaluator Agent Loop** that conducts automated QA (glitch detection, consistency scoring, retry loops) before proceeding to each subsequent stage.

---

## 🚦 Roadmap & Feature Stages

| Feature Stage | Description | Status | Active Owner / Agents |
| :--- | :--- | :--- | :--- |
| **Stage 0: Architecture & Research Setup** | Pipeline DAG, state tracker, edge-case registry, research agent deployment | 🟢 Completed | Antigravity + Yashu |
| **Stage 1: Idea $\rightarrow$ Story $\rightarrow$ Script Engine** | Structured JSON screenplay generator with viral pacing, character tags, and acoustic cues | 🟢 Completed | Agentic Scripting Unit |
| **Stage 2: Visual Bible & Keyframe Generator** | Automated prompt builder, character/environment consistency locking, reference image chaining | 🟢 Completed | Asset Generator + Multimodal Evaluator |
| **Stage 3: Voiceover & Lip-Sync Synthesis** | Google Cloud TTS / Edge-TTS audio gen + audio alignment + lip-sync model integration | 🟢 Completed | Audio Synthesis Unit |
| **Stage 4: I2V Motion Generation & Asset Inset** | Image-to-Video generation (Veo / Runway / Kling / open-source) + screen replacement compositing | 🟢 Completed | Motion Engine |
| **Stage 5: Autonomous Assembly & QA Monitor** | FFmpeg/Remotion programmatic timeline assembly, caption burning, automated glitch & sync evaluator | 🟢 Completed | Video Assembly & QA Agent |
| **Stage 6: Dispatch & Social Media Scheduler** | YouTube Shorts API, Instagram Graph API, scheduling queue, webhook triggers | 🟢 Completed | Social Dispatcher |

---

## 📝 Change & Decision Log

### [2026-10-07] Initialization & Foundation Setup (Stage 0 Complete)
- Created dedicated project workspace: `C:\Users\yashu\.gemini\antigravity\scratch\autonomous-video-pipeline`.
- Created structured documentation:
  - `docs/ARCHITECTURE.md` (System design & agentic feedback loops)
  - `docs/EDGE_CASES_AND_LOOPS.md` (Catastrophic failure points & recovery routines)
  - `docs/RESEARCH_REGISTER.md` (Curated OSS repos, Google APIs, connectors)
- Activated and integrated intelligence from 3 specialized subagents (`github_oss_scout`, `google_stack_architect`, `agentic_qa_evaluator`).

### [2026-10-07] Feature 1: Narrative & Screenplay Engine (Stage 1 Complete)
- Implemented `src/scripting/schemas.py`: Pydantic models for `ProductionShotDeck`, `ProductionShot`, `VisualCue`, `DialogueCue`, `AudioCue`, `ScriptEvaluationCritique`.
- Implemented `src/scripting/prompt_templates.py`: Directives for 3s hook word limits, viral pacing, character anchor tokens, and acoustic ducking flags.
- Implemented `src/scripting/generator.py`: `ScriptingEngine` with automated QA evaluation scoring ($S_{hook}$, pacing, dialogue naturalness) and self-healing refinement loop.
- Verified test suite: `tests/test_scripting_engine.py` generates and validates the 9:16 vertical Appin ad shot deck (`data/shot_decks/appin_career_ka_asli_netflix_shot_deck.json`) scoring 9.04/10 on QA.
- Validated audio generation: Generated real Hinglish speech files (`data/audio/shot1_didi.mp3` and `data/audio/shot2_rajat.mp3`) using `edge-tts` (`hi-IN-SwaraNeural` and `hi-IN-MadhurNeural`).

### [2026-10-07] Strategic Framework & Skills Architecture Integration
- **`find-skills` Meta-Skill:** Installed via `npx skills add vercel-labs/skills@find-skills` into `.agents/skills/find-skills`. Enables on-demand capability discovery and automated installation from the global `skills.sh` registry.
- **`Graphify` Integration:** Ingested `Graphify-Labs/graphify`, mounted `/graphify` skill in `.agents/skills/graphify`. Enables AST knowledge graph parsing, dependency mapping, and queryable memory across project code and narrative assets.
- **`Qodex AI Agent Skills` Suite:** Ingested and mounted 11 specialized agent skills directly into `.agents/skills`:
  * `multi-agent-orchestration` (Coordinating specialist agents and task delegation)
  * `visual-composition` (Articulating aesthetic philosophies and visual layouts)
  * `visual-quality-improver` (Iterative enhancement of image/video assets)
  * `voice-ai-integration` (Multi-provider TTS, speech recognition, and real-time audio)
  * `media-transformation` (Format transcoding, resizing, filter chains)
  * `creative-generation-agent` (High-retention storytelling and creative arcs)
  * `validation-first-approach` (Test-driven validation before pipeline execution)
  * `quality-validation` (Systematic QA benchmarks and defect scoring)
  * `video-archival-system` (Asset preservation, metadata tagging, and retrieval)
  * `deep-research-agent` (Autonomous academic, technical, and market reconnaissance)
  * `system-design` (Architectural diagrams, service decomposition, and interface contracts)

### [2026-11-07] Feature 2: Visual Bible & Keyframe Synthesis (Stage 2 Complete)
- Implemented `src/visuals/schemas.py`: Pydantic models for `KeyframeAsset`, `KeyframeMetadata`, and `VisualQAResult`.
- Implemented `src/visuals/prompt_builder.py`: Rules mapping shot angles to prime lenses (85mm, 35mm, 24mm), negative quality constraints, and character anchor token injection.
- Implemented `src/visuals/evaluator.py`: `VisualQAEvaluator` utilizing OpenCV Laplacian variance blur detection, aspect ratio validation, and Gemini 2.5 Flash Vision multimodal audit.
- Implemented `src/visuals/generator.py`: `KeyframeGenerator` supporting Google Imagen 3 API dispatch and high-fidelity local rendering with feedback-loop retries.
- Verified test suite: `tests/test_visual_engine.py` successfully synthesized and verified all 5 keyframes (`data/keyframes/shot_1_keyframe.png` through `shot_5_keyframe.png`) at 1080x1920 (9:16 vertical), scoring 9.06/10 on QA.
- Updated Knowledge Graph: Ingested keyframes and visual modules into `data/knowledge_graph/`, expanding graph memory to 71 nodes and 57 relationships.

### [2026-11-07] Feature 3: Voiceover, Sidechain Ducking & Acoustic Mastering (Stage 3 Complete)
- Git & Remote Sync: Synchronized local codebase to [GitHub: Goutammandloi/autonomous-video-pipeline](https://github.com/Goutammandloi/autonomous-video-pipeline); created and checked out active `dev` working branch.
- Implemented `src/audio/schemas.py`: Data models for `VoicePersona`, `WordTiming`, `DialogueAudioTrack`, and `AcousticMasterReport`.
- Implemented `src/audio/tts_engine.py`: Multi-persona voice generator mapping Didi (`hi-IN-SwaraNeural` / Zira) and Rajat (`hi-IN-MadhurNeural` / David) with offline SAPI fallback.
- Implemented `src/audio/subtitles.py`: Automated word-level timestamp alignment and SubRip (`.srt`) export.
- Implemented `src/audio/mixer.py`: Dynamic sidechain compression engine attenuating BGM by 12.0 dB during dialogue bursts; normalized master soundtrack to ITU-R BS.1770 -14.0 LUFS (-1.0 dBTP ceiling).
- Verified test suite: `tests/test_audio_engine.py` validated all 5 shots dialogue synthesis, subtitle generation (`data/audio/subtitles.srt`), and mastered composite (`data/audio/master_soundtrack.wav`).
- Updated Knowledge Graph: Ingested audio modules and assets, expanding topology to 96 nodes and 79 relationships.

### [2026-11-07] Feature 4: Motion Synthesis, Dynamic Screen Inset & Optical Flow QA (Stage 4 Complete)
- Implemented `src/compositor/screen_warper.py`: OpenCV 4-point homography perspective warping with `CornerPoints` schema, bilinear interpolation, and boundary feathering to seamlessly composite screen assets (e.g., cyber terminal / Netflix screen) into video frames.
- Implemented `src/motion/schemas.py`: Data models for `MotionConfig`, `CameraMotionType` (`PAN_LEFT`, `SLOW_ZOOM_IN`, `DYNAMIC_TRACK`), `MotionQualityReport`, and `GeneratedMotionClip`.
- Implemented `src/motion/glitch_detector.py`: Gunnar Farneback dense optical flow evaluation (`cv2.calcOpticalFlowFarneback`) with statistical motion anomaly detection ($Z_t > 3.5$ or velocity jump ratio $> 2.5\times$).
- Implemented `src/motion/motion_engine.py`: CFR 30.0 fps $1080 \times 1920$ motion engine supporting Veo 2 / local synthesis with automated self-healing remediation (automatic velocity damping by $0.65\times$ when optical flow spikes occur).
- Verified test suite: `tests/test_motion_and_compositor.py` generated and validated all 5 MP4 motion clips in `data/video_clips/` (Shot 3 featuring perspective terminal screen inset).

### [2026-11-07] Feature 5: Timeline Assembly, Kinetic Subtitles & Final Master QA (Stage 5 Complete)
- Implemented `src/assembly/schemas.py`: Pydantic data models for `SubtitleStyleConfig`, `SubtitleSegment`, `ActiveWordHighlight`, `AssemblyConfig`, and `MasterVideoReport`.
- Implemented `src/assembly/subtitle_burner.py`: High-retention kinetic subtitle rendering engine utilizing Pillow and anti-aliased TrueType bold typography. Renders active-spoken-word dynamic highlighting (vibrant gold/yellow `(255, 220, 0)` on active word, pure white `(255, 255, 255)` for surrounding words), deep stroke outline (`#0A0A0A`), speaker tag pill (`• DIDI`, `• RAJAT`), and translucent rounded background container.
- Implemented `src/assembly/timeline_assembler.py`: Programmatic FFmpeg video assembly engine piping raw frames (`-pix_fmt bgr24`) directly into FFmpeg stdin with zero intermediate disk bloat, multiplexing ITU-R BS.1770 mastered audio (`master_soundtrack.wav`), faststart container flags, and high-compatibility `yuv420p` H.264/AAC output (`data/final/appin_master_9x16.mp4`).
- Implemented `src/assembly/evaluator.py`: Multi-vector video gatekeeper auditing aspect ratio (9:16 vertical $1080 \times 1920$), CFR 30.00 FPS, audio codec (AAC stereo 48kHz), A/V synchronization delta ($|\Delta t| \le 33\text{ ms}$), and lower-third subtitle legibility.
- Verified test suite: `tests/test_timeline_assembly.py` validated master video (`data/final/appin_master_9x16.mp4`), scoring **10.0 / 10.0** on QA with exact **$0.00\text{ ms}$ A/V sync drift**.
- Updated unified runner & UI preview: `run_studio.py` and `data/preview/index.html` updated with the responsive 9:16 hero master player and live telemetry cards.

### [2026-11-07] Feature 6: Multi-Platform Dispatch & Social Media Scheduler (Stage 6 Complete)
- Implemented `src/distribution/schemas.py`: Data models for `PlatformType` (`YOUTUBE_SHORTS`, `INSTAGRAM_REELS`, `TIKTOK`, `LINKEDIN`, `TWITTER_X`), `SocialPlatformMetadata`, `SchedulingSlot`, `DispatchJob`, and `DispatchBatchReport`.
- Implemented `src/distribution/metadata_generator.py`: Copywriting agent generating platform-tailored viral hooks, SEO search tags, pinned engagement comments, and link-in-bio CTAs for YouTube Shorts, Instagram Reels, LinkedIn, TikTok, and X.
- Implemented `src/distribution/social_dispatcher.py`: Multi-platform publisher supporting YouTube Data API v3 (resumable chunked upload with `status.publishAt` scheduling), Instagram Graph API (2-phase container publishing and media verify), LinkedIn Video API, with full dry-run simulation mode and diagnostic trace logging.
- Implemented `src/distribution/scheduler.py`: Algorithmic queue scheduler computing peak audience release windows (18:30 IST / 13:00 UTC for Indian engineering demographics) and maintaining persistent JSON campaign logs in `data/schedules/scheduled_dispatches.json`.
- Verified test suite: `tests/test_distribution.py` scheduled and validated all 3 campaigns with remote URLs and persistent storage.
- Updated Knowledge Graph: Ingested master video assets, distribution modules, and campaigns, bringing total knowledge graph memory to **166 nodes and 144 relationships**.

### [2026-11-07] Phase 2 Kickoff: "Project Origin: The Shattered Crown" (60x 60s Serial Universe)
- Adopted Concept 1: *Project Origin: The Shattered Crown* as the flagship serialized narrative production.
- Defined format: **60 continuous interconnected episodes**, exactly **60 seconds each** (9:16 vertical $1080 \times 1920$ for YouTube Shorts, Instagram Reels, and TikTok) in **cinematic English**.
- Created Master Universe Bible: [`docs/PROJECT_ORIGIN_MASTER_BIBLE.md`](docs/PROJECT_ORIGIN_MASTER_BIBLE.md) mapping:
  - Narrative Thesis: Corporate Silph-Macro Consortium vs. World Monarch Ash Ketchum & Mt. Silver Legend Red.
  - 60-Second Micro-Pacing Formula: 0–3s Hook $\rightarrow$ 3–18s Stakes $\rightarrow$ 18–42s Kinetic Combat $\rightarrow$ 42–52s Twist $\rightarrow$ 52–60s Cliffhanger Cut.
  - Complete 4-Arc 60-Episode Roadmap across Arc 1 (The Gilded Throne & The Phantom, Ep 1–15), Arc 2 (The Rogue Gym Underground, Ep 16–30), Arc 3 (Siege of Mount Quena, Ep 31–45), and Arc 4 (The Apex War & The True Sovereign, Ep 46–60).






