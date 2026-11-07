# 🔍 Research Register: Open Source Repositories, Google APIs & Connectors

This document maintains an evolving registry of open-source tooling, libraries, API specifications, and community techniques integrated into the autonomous video pipeline.

## 0. Knowledge Graphs & Meta-Agent Skills Frameworks

| Tool / Framework | Source / Command | Strategic Value in Video Pipeline |
| :--- | :--- | :--- |
| **[Graphify](https://github.com/Graphify-Labs/graphify)** | `Graphify-Labs/graphify` | Builds queryable AST knowledge graphs of pipeline code, scene dependencies, and multimodal assets. Generates interactive HTML, JSON, and audit trails. |
| **[Qodex AI Agent Skills](https://github.com/qodex-ai/ai-agent-skills)** | `qodex-ai/ai-agent-skills` | Curated skill suites mounted in `.agents/skills`: `multi-agent-orchestration`, `visual-composition`, `visual-quality-improver`, `voice-ai-integration`, `media-transformation`, `validation-first-approach`. |
| **[Vercel Labs Find-Skills](https://skills.sh/)** | `npx skills add vercel-labs/skills@find-skills` | Meta-skill enabling the agent to search, rank, and install community skills dynamically from `skills.sh`. |

---

## 1. Core Open-Source Video & Media Engines

| Tool / Repository | Primary Utility | License | Integration Method |
| :--- | :--- | :--- | :--- |
| **[FFmpeg](https://ffmpeg.org/)** | Universal media encoder, codec normalizer, sidechain ducking, subtitle burning, filtergraphs. | LGPL/GPL | Direct CLI subprocess or `ffmpeg-python` wrapper. |
| **[Remotion](https://www.remotion.dev/)** | Programmatic React-based video creation engine (dynamic overlays, kinetic typography, animations). | Remotion License | Headless Node.js rendering via CLI/API. |
| **[MoviePy](https://zulko.github.io/moviepy/)** | Python video editing library for basic clips, compositing, cuts. | MIT | Python module for fast prototyping. |
| **[OpenCV (cv2)](https://opencv.org/)** | Perspective transformation (homography matrix for screen inserts), frame-level anomaly detection. | Apache 2.0 | Python `opencv-python`. |

---

## 2. Audio & Speech Synthesis

| Engine | GitHub / Model | Hardware Requirements | Hinglish/Hindi Naturalness | Integration Method |
| :--- | :--- | :--- | :--- | :--- |
| **Edge-TTS** | [rany2/edge-tts](https://github.com/rany2/edge-tts) | **Minimal CPU / 0 GPU** (WebSocket API) | **S-Tier**: `hi-IN-MadhurNeural`, `hi-IN-SwaraNeural`, `en-IN-NeerjaNeural` seamlessly parse Romanized Hinglish without custom lexicons. | `edge_tts.Communicate()` async Python stream. |
| **Kokoro-TTS & Goonj-82M** | [hexgrad/kokoro](https://github.com/hexgrad/kokoro) / [BH-Builds/goonj-1-82M](https://huggingface.co/BH-Builds/goonj-1-82M) | **CPU or lightweight GPU** (82M params, RTF < 0.1 on CPU, < 1GB VRAM). Apache 2.0. | **A-Tier**: Ultra fast, local offline inference. Includes 15 Indian persona voicepacks and Romanized-to-Devanagari lexicon. | Native PyTorch / ONNX runtime. |
| **Google Cloud Text-to-Speech** | [google-cloud-texttospeech](https://cloud.google.com/text-to-speech) | Cloud API (Google Cloud Free Tier / Plan) | **S-Tier**: Neural2 & Journey voices with full SSML pause, pitch, and rate control. | `google.cloud.texttospeech_v1` client. |
| **WhisperX** | [m-bain/whisperX](https://github.com/m-bain/whisperX) | NVIDIA GPU or fast CPU | Word-level phoneme and timestamp forced alignment for kinetic subtitles. | `whisperx.load_align_model()`. |

---

## 3. Facial Animation & Lip-Sync

| Model | GitHub Repo | Hardware Requirements | Quality & Resolution Profile |
| :--- | :--- | :--- | :--- |
| **MuseTalk (v1.5)** | [TMElyralab/MuseTalk](https://github.com/TMElyralab/MuseTalk) | **NVIDIA GPU ≥ 8GB–12GB VRAM** | **Real-Time Lip-Sync (>30 FPS)**. VAE latent space inpainting guided by Whisper audio features. 256x256 mouth latent preserves full face texture without blur/jitter. |
| **LivePortrait** | [KwaiVGI/LivePortrait](https://github.com/KwaiVGI/LivePortrait) | **NVIDIA GPU ≥ 8GB–12GB VRAM** | **Photorealistic Holistic Reenactment (30–40+ FPS)**. Seamlessly animates head pose (yaw/pitch/roll), eye gaze, and blinking. |
| **Wav2Lip** | [Rudrabha/Wav2Lip](https://github.com/Rudrabha/Wav2Lip) | Low CPU or 4GB GPU | **Legacy Baseline**. 96x96 resolution crop causes blur; requires GFPGAN/CodeFormer enhancer which slows pipeline. |

---

## 4. Google AI & Ecosystem Utilization

| Service | Specific Capability in Pipeline |
| :--- | :--- |
| **Gemini 2.5 Flash / Pro** | Structured JSON screenplay writing, prompt expansion, supervisor multimodal visual verification. |
| **Google Imagen 3** | Photorealistic keyframe generation, lighting consistency, aspect ratio control. |
| **Google Veo (Vertex AI / VideoFX)** | Cinematic 1080p high-coherence motion synthesis from keyframes. |
| **YouTube Data API v3** | Direct programmatic upload to YouTube Shorts, scheduled release, metadata optimization. |
| **Google Cloud Storage (GCS)** | Object storage for keyframes, audio assets, intermediate render passes. |

---

## 5. Workflow & Orchestration State Machines

| Framework | Role in Pipeline | Advantage |
| :--- | :--- | :--- |
| **Python LangGraph / StateGraph** | Multi-agent DAG with conditional branches and human/agentic review loops. | Native cyclical graphs & checkpointing. |
| **LiteLLM / Instructor** | Strict JSON schema validation for LLM outputs. | Guaranteed structured output adherence. |
| **Celery / Redis / RQ** | Distributed asynchronous task queue for heavy video generation tasks. | High throughput, automatic task retries. |
