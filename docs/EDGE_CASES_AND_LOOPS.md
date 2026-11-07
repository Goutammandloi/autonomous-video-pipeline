# ⚠️ Edge Cases, Failure Modes & Automated Recovery Loops

In automated AI video generation, naive linear pipelines break down at multiple critical failure points. Below is the comprehensive taxonomy of edge cases and the self-healing programmatic loops designed to neutralize them.

---

## 1. Visual & Continuity Loopholes

| Failure Mode | Root Cause | Automated Mitigations & Recovery Loop |
| :--- | :--- | :--- |
| **Character Identity Mutation** | Prompt drift across subsequent keyframes (face, hair, attire changing). | **Anchor Injection:** Programmatic prefixing of immutable character tokens. Compare embeddings using face recognition / CLIP score against character reference image. If similarity $< 0.82$, reject and re-roll keyframe with higher prompt guidance scale. |
| **Perspective Inversion** | Prompt ambiguity (e.g., prompt requested over-the-shoulder POV but model generated third-person wide shot). | **Multimodal Vision Verification:** Supervisor agent inspects keyframe image using Gemini Flash Vision asking structured boolean questions (`is_pov: true`, `is_facing_screen: true`). Automatic retry with negative prompt (`front angle`, `wide shot`) if violated. |
| **Artifact / Glitch Morphing in Motion** | I2V model hallucinates extra limbs, melting objects, or unnatural rapid morphing. | **Optical Flow / SSIM Anomaly Detection:** Compute frame-by-frame structural similarity (SSIM) and motion vector variance. If sudden sharp pixel dislocation is detected without a camera pan, flag clip as corrupted and regenerate with reduced motion strength parameter. |

---

## 2. Audio & Synchronization Pitfalls

| Failure Mode | Root Cause | Automated Mitigations & Recovery Loop |
| :--- | :--- | :--- |
| **Lip-Sync Desynchronization** | Audio duration mismatch or variable frame rate (VFR) causing audio to drift out of sync with video mouth movement. | **Forced Alignment & CFR Conversion:** Force convert all video clips to strict Constant Frame Rate (CFR, e.g., 30.0 fps) via FFmpeg (`-vsync cfr -r 30`). Use word-level timestamps (WhisperX) to lock phonemes directly to video keyframe time offsets. |
| **Audio Clipping & Dynamic Masking** | Background music (BGM) overwhelms voiceover (VO) or peaks above $0 \text{ dBFS}$. | **Automated Sidechain Ducking:** Apply FFmpeg `sidechaincompress` filter to automatically drop BGM volume by $-12 \text{ dB}$ whenever dialogue is present. Normalize final mix to standard $-14 \text{ LUFS}$ integrated loudness. |
| **Pacing / Dead Air** | TTS model produces awkward pauses between dialog lines. | **Silence Trimming Filter:** Run `silenceremove` filter to trim any silence $> 250\text{ ms}$, ensuring modern short-form viral retention pacing. |

---

## 3. Video Encoding & Timeline Glitches

| Failure Mode | Root Cause | Automated Mitigations & Recovery Loop |
| :--- | :--- | :--- |
| **PTS / DTS Timestamp Drift** | Concatenating video clips with different timebases or non-monotonically increasing timestamps results in frozen frames or black screens. | **Pre-Concat Normalization:** Re-encode every generated clip to identical codec (`h264`), color matrix (`yuv420p`), sample rate (`48000 Hz`), and reset presentation timestamps (`-vf setpts=PTS-STARTPTS -af asetpts=PTS-STARTPTS`). |
| **Aspect Ratio Distortion / Squishing** | Different generators output slightly varying dimensions ($1080\times1920$, $720\times1280$, $1024\times1824$). | **Scale & Pad Filter:** Apply uniform FFmpeg scaling pipeline: `scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black`. |

## 4. API & Orchestration Robustness

| Failure Mode | Root Cause | Automated Mitigations & Recovery Loop |
| :--- | :--- | :--- |
| **Rate Limiting (HTTP 429)** | Exceeding API requests per minute during batch asset generation. | **Exponential Backoff with Jitter:** Implement token bucket rate limiters and retry loops with exponential backoff ($t = 2^k + \text{rand}(0, 1)$). |
| **Cold Starts & Generation Timeouts** | Video generation APIs taking 60–180 seconds to render clips, leading to hung connections. | **Async Webhook / Polling State Machine:** Never block synchronous worker threads; decouple generation dispatch from status polling using an asynchronous job queue. |
| **Social Media Quota & Auth Expiry** | OAuth2 refresh token invalidation or daily YouTube Shorts upload limits hit. | **Pre-flight Health Checks:** Test API credentials and quota headroom before entering the publishing phase; queue pending uploads in a local SQLite/JSON spool. |

---

## 5. Surgical Hyperparameter Patch Table & Self-Healing State Machine

Rather than costly full-pipeline restarts upon defect detection, the supervisor agent applies surgical remediation to the specific failing node:

| Defect Detected | Trigger Metric | Max Retries | Automated Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **`HOOK_WEAKNESS`** | $S_{hook} < 0.85$ (3s retention) | 2 | Re-prompt hook with `CONTRARIAN_QUESTION` or `PATTERN_INTERRUPT` template ($W_{target} \le 8$ words). |
| **`FACE_IDENTITY_DRIFT`** | Face Cosine Similarity $< 0.68$ | 3 | Increase IP-Adapter weight ($0.65 \to 0.85$), boost Face LoRA scale ($0.75 \to 0.95$), or inject CodeFormer face-swap pass. |
| **`OPTICAL_FLOW_WARP_GLITCH`** | $Z_t = \frac{\|\overline{M}_t - \mu_M\|}{\sigma_M} > 3.5$ | 2 | Clamp `motion_bucket_id` ($127 \to 85$) to dampen violent warp dynamics; reduce `cfg_scale` ($7.0 \to 5.5$). |
| **`PIXEL_DISTORTION_TEAR`** | Inter-frame $\min \operatorname{SSIM} < 0.65$ | 2 | Enable VAE tiling (`vae_tiling = True`); reduce denoise strength ($0.75 \to 0.65$). |
| **`AUDIO_DESYNC`** | SyncNet $\mathcal{C}_{sync} < 3.8$ ($\Delta t > 20\text{ms}$) | 2 | Recalculate lead offset ($-35\text{ms}$ adjustment), pad Wav2Lip mask `[0, 10, 0, 0]`. |
| **`LUFS_OUT_OF_BOUNDS`** | Loudness $\notin [-15.5, -12.5]\text{ LUFS}$ | 1 | Apply ITU-R BS.1770-4 normalization filter (`-14.0 LUFS`, `-1.0 dBTP`). |
| **`SIDECHAIN_DUCKING_FAILURE`** | Ducking attenuation $< 10.0\text{ dB}$ | 1 | Reconfigure FFmpeg sidechain compressor (`-24 dB` threshold, `6:1` ratio, `14 dB` gain reduction). |

### State Transition FSM:
$$\text{IDLE} \longrightarrow \text{GENERATING} \longrightarrow \text{QA\_AUDIT} \begin{cases} \xrightarrow{\text{Passed}} \text{PASSED} \longrightarrow \text{NEXT\_STAGE} \\ \xrightarrow{\text{Failed (retries } \le k)} \text{RETRY\_PATCH} \longrightarrow \text{GENERATING} \\ \xrightarrow{\text{Failed (retries } > k)} \text{ROLLBACK\_REGENERATE} \longrightarrow \text{RESET\_SEED} \\ \xrightarrow{\text{Cycles } \ge 2} \text{FATAL\_ESCALATE} \longrightarrow \text{HUMAN\_REVIEW} \end{cases}$$
