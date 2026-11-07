# 🛡️ PROJECT ORIGIN: THE SHATTERED CROWN
## Master Edge Case Registry, Lore Guardrails & Technical Failure Recovery

This document catalogs every narrative, technical, audio, and visual edge case that must be strictly enforced before producing Episode 1 through Episode 10.

---

### 1. Narrative & Lore Guardrails (Preventing Plot Holes)

| Potential Edge Case / Plot Hole | Narrative Guardrail & Canonical Resolution |
| :--- | :--- |
| **Why doesn't Ash immediately call Professor Oak, Cynthia, or Leon?** | **The Saffron Protocol Jammer:** In Episode 1, the moment Ash enters the executive suite, Vance Stirling activates a localized cellular and Rotom-protocol dead-zone. When Ash escapes, the Consortium flags his Trainer ID as *"Under Active Internal Audit"*, rerouting all outgoing calls to an automated Consortium proxy server. His Rotom Phone is effectively bricked until hacked in Arc 2. |
| **Why can't Pikachu simply one-shot all opponents with a Z-Move?** | **Civilian Collateral Restraint & EMP Counters:** Pikachu possesses World Champion tier output, but Ash is fighting inside Saffron City atop skyscrapers and populated urban zones. Unleashing *10,000,000 Volt Thunderbolt* would collapse the building and cause civilian blackouts. Furthermore, the Consortium deploys specialized Faraday-mesh containment cages and high-frequency acoustic dampeners specifically engineered to neutralize electric types. |
| **Why did Red stay on Mt. Silver instead of acting sooner?** | **The Lack of Physical Evidence:** Red has tracked Consortium front companies for two years. However, without a physical, intact Helix Chip operating in a live specimen, going public would allow the Consortium's PR machine to brand him as an unhinged hermit making false accusations. Ash and the captured chip from Outpost 4 are the undeniable proof Red has been waiting for. |
| **Why don't the League Gym Leaders immediately stop the Consortium?** | **Corporate Privatization:** Over the past 3 years, the Silph-Macro Consortium has bought out the League's infrastructure, funding stadium maintenance, referee salaries, and TV broadcasting rights. Resisting Gym Leaders (like Brock and Sabrina) have had their gym licenses revoked and replaced by automated Consortium battle simulators. |

---

### 2. Audio & Voice AI Edge Cases

| Technical Edge Case | Manifestation / Risk | Architectural Mitigation |
| :--- | :--- | :--- |
| **Phonetic Mispronunciation of Pokémon Terms** | TTS engines (Edge-TTS / SAPI) mispronounce fantasy terms (e.g. *"Pee-ka-khoo"*, *"Char-eye-zard"*). | Implement a **Phonetic Normalization Map** in `src/audio/tts_engine.py` that intercepts and phonetically translates names before synthesis: `{"Pikachu": "Pee-kah-choo", "Charizard": "Char-ih-zard", "Lucario": "Loo-kahr-ee-oh", "Snorlax": "Snor-lax", "Ursaring": "Er-sah-ring"}`. |
| **Dialogue Word-Budget Overflow** | If an episode script has $> 120$ words, spoken dialogue exceeds 50 seconds, leaving zero room for music drops, sound effects, or dramatic pauses. | Enforce a strict **Adversarial Word Budget QA rule**: Maximum **85 spoken words per 60-second episode**. Dialogue cues must be punchy, rhythmic, and leave at least 18 seconds for kinetic sound effects and BGM swelling. |
| **Vocal Timbre Collision between Ash & Red** | Ash and Red sound too similar, confusing mobile viewers watching without subtitles. | Persona voice locking: Ash uses an energetic, bright, youthful tenor model (`hi-pitch / dynamic`); Red uses a low, quiet, gravelly baritone model (`low-pitch / stoic / resonant`). |

---

### 3. Visual Continuity & 9:16 Vertical Framing Edge Cases

| Visual Edge Case | Failure Mode | Mitigation Rule |
| :--- | :--- | :--- |
| **Character Feature Morphing Across Shots** | Ash's jacket or Red's cap morphing color or design between Episode 1 and Episode 10. | Lock immutable character token anchors into `src/visuals/prompt_builder.py`. Prompt builder automatically prepends the exact token string: `Ash Ketchum, unbuttoned World Monarch jacket with gold trim, fingerless gloves, Z-Ring on right wrist` to every visual prompt. |
| **Social Media UI Overlap (Safe Zones)** | Subtitles or key action placed too low, hidden behind TikTok/Reels captions, sound tags, and like buttons. | All critical visual action and kinetic subtitles must be placed strictly within the **Vertical Safe Zone ($Y = 15\%\text{ to } 78\%$ of frame)**. Lower $22\%$ and rightmost $12\%$ of screen space are reserved for UI overlay clearance. |
| **Glitch Detector False Positives on Intentional Fast Cuts** | Rapid anime whip-pans or lightning flashes triggering the $Z_t > 3.5$ optical flow anomaly alarm. | In `src/motion/glitch_detector.py`, mask out and ignore the first 2 frames of intentional scene cuts so velocity spikes at cut boundaries do not trigger false re-renders. |

---

### 4. Episodic Pacing & Binge-Loop Retention Rules

1. **The 3-Second Cold Open Rule:**  
   The first frame of every episode must start with motion or high-contrast audio already in progress (in media res). No black screens, no title cards, no slow establishing pans.
2. **The "Baton-Pass" Continuity Rule:**  
   The cliffhanger frame of Episode $N$ must be the exact physical starting point of Episode $N+1$. A viewer watching on auto-play must experience zero cognitive friction or missing narrative beats between clips.
3. **The 60.00-Second Hard Timestamp Cap:**  
   Total audio-video stream duration must equal $60.00\text{s} \pm 0.05\text{s}$ (1,800 frames at 30.00 FPS CFR). Never allow variable frame rates to cause drift across social media platforms.
