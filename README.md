# 🎬 Autonomous Multi-Agent AI Video Studio

An autonomous, self-healing, multi-agent AI video production engine designed to transform raw ideas into fully rendered, published short-form and long-form videos.

$$\text{Raw Idea} \xrightarrow{\text{Agent 1}} \text{Story Structure} \xrightarrow{\text{Agent 2}} \text{Production Script} \xrightarrow{\text{Agent 3}} \text{Keyframes \& Visuals} \xrightarrow{\text{Agent 4}} \text{Motion \& Audio Clips} \xrightarrow{\text{Agent 5}} \text{Final Video Master} \xrightarrow{\text{Agent 6}} \text{Multi-Platform Dispatch}$$

---

## 🌟 Key Highlights

- **Adversarial Supervisor-Evaluator Gates**: Automated quality checks at every phase (Hook retention $\le 3\text{s}$, viral pacing, character facial consistency $\ge 0.82$, optical flow glitch detection).
- **Self-Healing State Machine**: Surgical hyperparameter remediation table instead of blind full-pipeline restarts.
- **Knowledge Graph Memory**: GraphRAG-ready AST analysis and visual network graph via Graphify.
- **Multi-Persona Voiceover**: High-fidelity Romanized Hinglish/English neural speech synthesis via Edge-TTS and Google Cloud TTS with automated dynamic sidechain ducking.
- **Strict Pydantic Validation**: All production shot decks, camera vectors, and acoustic cues conform to strict typed schemas.

---

## 📂 Repository Structure

```
autonomous-video-pipeline/
├── .agents/skills/              # 17 mounted agent skills (Google Veo, Remotion, Multi-Agent, etc.)
├── docs/
│   ├── ARCHITECTURE.md          # Full system architecture & DAG specs
│   ├── EDGE_CASES_AND_LOOPS.md  # Taxonomy of 12+ failure modes & self-healing rules
│   └── RESEARCH_REGISTER.md     # Curated open-source repos & Google endpoints
├── src/
│   ├── scripting/               # Narrative engine, shot deck generator & script QA evaluator
│   ├── visuals/                 # Keyframe generator, style anchor builder & CV/LLM evaluator
│   ├── audio/                   # Voiceover synthesis, phoneme alignment & sidechain ducking
│   ├── motion/                  # I2V video dispatch & optical flow glitch checkers
│   ├── assembly/                # Programmatic video composition (FFmpeg / Remotion)
│   └── distribution/            # Multi-platform social media dispatchers
├── tools/
│   └── graphify_pipeline.py     # Project knowledge graph generator & vis.js viewer
├── data/
│   ├── shot_decks/              # Validated production shot decks (JSON)
│   ├── keyframes/               # Generated 1080x1920 (9:16) vertical keyframes
│   ├── audio/                   # Synthesized speech and acoustic tracks
│   └── knowledge_graph/         # Graph report, JSON, and interactive HTML viewer
├── tests/                       # Automated test suites for each feature stage
└── PROJECT_STATE.md             # Living state log & roadmap tracker
```

---

## 🚦 Roadmap

- [x] **Stage 0: Architecture & Research Setup**
- [x] **Stage 1: Narrative & Screenplay Engine with Adversarial QA**
- [x] **Stage 2: Visual Bible & 9:16 Keyframe Synthesis Engine**
- [ ] **Stage 3: Multi-Persona Voiceover & -14 LUFS Sidechain Ducking**
- [ ] **Stage 4: I2V Motion Synthesis & Perspective Screen Warping**
- [ ] **Stage 5: Autonomous Programmatic Video Assembly & QA**
- [ ] **Stage 6: Multi-Platform Social Media Scheduler**

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+
- Dependencies: `pip install pydantic google-genai edge-tts opencv-python pillow networkx`

### 2. Run Test Suites
```bash
# Test Feature 1: Scripting Engine & Adversarial QA
python tests/test_scripting_engine.py

# Test Feature 2: Visual Engine & Keyframe QA
python tests/test_visual_engine.py

# Generate Knowledge Graph & Visual Network
python tools/graphify_pipeline.py
```
Open `data/knowledge_graph/graph_viewer.html` in your browser to inspect the complete pipeline knowledge graph.
