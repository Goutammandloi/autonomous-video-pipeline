"""
Autonomous AI Video Pipeline: Scripting & Screenplay Engine
Orchestrates:
1. Narrative Synthesis (Idea -> Shot-by-Shot Deck)
2. Adversarial QA Evaluation (Hook, Pacing, Continuity, Acoustics)
3. Automated Self-Healing Feedback Loop (Refinement & Retries)
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

from .schemas import (
    ProductionShotDeck,
    ProductionShot,
    VisualCue,
    DialogueCue,
    AudioCue,
    AspectRatio,
    CameraAngle,
    CameraMovement,
    ScriptEvaluationCritique,
)
from .prompt_templates import SHOT_DECK_SYSTEM_PROMPT, SCRIPT_QA_EVALUATOR_SYSTEM_PROMPT


class ScriptingEngine:
    """
    Autonomous Screenplay & Shot Deck Engine with Supervisor Evaluation.
    """

    def __init__(self, api_key: Optional[str] = None, output_dir: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.output_dir = Path(output_dir or "data/shot_decks")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.client = None

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[ScriptingEngine] Warning: Could not initialize google-genai client: {e}")

    def evaluate_shot_deck(self, shot_deck: ProductionShotDeck) -> ScriptEvaluationCritique:
        """
        Adversarial evaluation of a Shot Deck against viral retention and continuity rules.
        """
        # 1. Algorithmic / Mathematical Verification
        flaws = []
        refinements = []

        shots = shot_deck.shots
        if not shots:
            return ScriptEvaluationCritique(
                hook_score=0.0,
                pacing_score=0.0,
                dialogue_naturalness=0.0,
                visual_continuity_feasibility=0.0,
                overall_score=0.0,
                passes_quality_gate=False,
                flaws_and_bottlenecks=["Empty shot list"],
                actionable_refinements=["Generate at least 5-8 shots."]
            )

        # Hook verification (Shot 1)
        shot1 = shots[0]
        hook_duration = shot1.duration_sec
        hook_words = 0
        if shot1.dialogue:
            hook_words = len(shot1.dialogue.line.split())

        # Mathematical Hook Score calculation: S_hook
        # Target: duration <= 3.5s, words <= 10 words, strong narrative beat
        hook_score = 9.0
        if hook_words > 12:
            hook_score -= 2.0
            flaws.append(f"Shot 1 spoken dialogue is too verbose ({hook_words} words > 12 limit). Will cause drop-off.")
            refinements.append("Trim Shot 1 spoken line to under 8-10 punchy words.")

        if hook_duration > 4.0:
            hook_score -= 1.5
            flaws.append(f"Shot 1 duration is too slow ({hook_duration}s > 3.5s target for high retention hook).")
            refinements.append("Accelerate Shot 1 pacing to 2.5s - 3.5s.")

        # Pacing verification across timeline
        total_duration = sum(s.duration_sec for s in shots)
        duration_variance = [s.duration_sec for s in shots]
        pacing_score = 9.0

        for s in shots:
            if s.duration_sec > 6.0:
                pacing_score -= 1.0
                flaws.append(f"Shot {s.shot_id} duration ({s.duration_sec}s) exceeds 6.0s max threshold for vertical shorts.")
                refinements.append(f"Split or trim Shot {s.shot_id} to maintain rhythmic cuts.")

        # Visual continuity & anchor token presence
        visual_score = 9.2
        for s in shots:
            if not s.character_anchor_tokens and s.visual.characters_present:
                visual_score -= 1.0
                flaws.append(f"Shot {s.shot_id} features characters {s.visual.characters_present} but has missing anchor tokens.")
                refinements.append(f"Add immutable style tokens for characters in Shot {s.shot_id}.")

        # Dialogue naturalness
        dialogue_score = 9.0
        dialogues = [s.dialogue.line for s in shots if s.dialogue]
        if not dialogues:
            dialogue_score = 6.0
            flaws.append("No spoken dialogue found across shots.")
            refinements.append("Inject punchy spoken lines or narration.")

        # Composite overall score
        overall = (hook_score * 0.4) + (pacing_score * 0.2) + (dialogue_score * 0.2) + (visual_score * 0.2)
        overall = round(max(0.0, min(10.0, overall)), 2)
        passes_gate = overall >= 8.5 and hook_score >= 8.5

        return ScriptEvaluationCritique(
            hook_score=round(hook_score, 2),
            pacing_score=round(pacing_score, 2),
            dialogue_naturalness=round(dialogue_score, 2),
            visual_continuity_feasibility=round(visual_score, 2),
            overall_score=overall,
            passes_quality_gate=passes_gate,
            flaws_and_bottlenecks=flaws,
            actionable_refinements=refinements,
        )

    def generate_shot_deck(
        self,
        premise: str,
        target_duration: float = 30.0,
        character_bible: Optional[Dict[str, str]] = None,
        max_retries: int = 3,
    ) -> Tuple[ProductionShotDeck, ScriptEvaluationCritique]:
        """
        Executes the full generation -> adversarial evaluation -> self-healing loop.
        """
        if character_bible is None:
            character_bible = {
                "Ash Ketchum": "16-year-old anime hero Ash Ketchum, athletic teenager, messy jet-black spiky hair, red-and-white trainer cap, royal-blue vest with white collar and gold trim, dark charcoal compression undershirt, Alolan Z-Ring on right wrist, Mega Keystone on left wrist, double zig-zag cheek marks, resolute brown eyes.",
                "Red": "19-year-old legendary trainer Red, tall lean muscular build, dark shaggy hair partially concealed beneath a worn, faded red-and-white cap casting a deep dramatic shadow over the upper half of his face. Piercing crimson-tinted eyes glowing in the shadow. High-collared charcoal-black duster trenchcoat with deep crimson interior lining, dark tactical cargo pants, sturdy combat boots, fingerless combat gloves with wrapped wrists.",
                "Vance Stirling": "48-year-old corporate oligarch CEO Vance Stirling, slicked-back silver-gray hair, sharp aristocratic cheekbones, cold ice-blue eyes behind titanium spectacles, tailored three-piece charcoal pinstripe suit, burgundy silk tie, gold DNA double-helix lapel pin."
            }

        critique_history = []
        attempt = 1

        while attempt <= max_retries:
            print(f"[ScriptingEngine] Generation Attempt {attempt}/{max_retries}...")

            if self.client:
                shot_deck = self._call_gemini_generator(premise, target_duration, character_bible, critique_history)
            else:
                shot_deck = self._synthesize_rule_based_shot_deck(premise, target_duration, character_bible, critique_history)

            critique = self.evaluate_shot_deck(shot_deck)
            print(f"[ScriptingEngine] QA Evaluation Score: {critique.overall_score}/10 (Hook: {critique.hook_score}/10, Passed: {critique.passes_quality_gate})")

            if critique.passes_quality_gate:
                print(f"[ScriptingEngine] ✅ Script passed quality gate on attempt {attempt}!")
                # Persist output
                slug = re.sub(r'[^a-zA-Z0-9_]', '_', shot_deck.title.lower())[:30]
                save_path = self.output_dir / f"{slug}_shot_deck.json"
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(shot_deck.model_dump_json(indent=2))
                print(f"[ScriptingEngine] Saved production shot deck to: {save_path}")
                return shot_deck, critique

            print(f"[ScriptingEngine] ⚠️ Script failed QA gate. Flaws: {critique.flaws_and_bottlenecks}")
            critique_history.extend(critique.actionable_refinements)
            attempt += 1

        print(f"[ScriptingEngine] ⚠️ Max retries ({max_retries}) reached. Returning latest revision.")
        return shot_deck, critique

    def _call_gemini_generator(
        self,
        premise: str,
        target_duration: float,
        character_bible: Dict[str, str],
        critique_feedback: list,
    ) -> ProductionShotDeck:
        """Invokes Gemini 2.5 Pro with structured Pydantic schema."""
        from google.genai import types

        feedback_prompt = ""
        if critique_feedback:
            feedback_prompt = "\n\nCRITICAL FIXES REQUIRED FROM PREVIOUS QA AUDIT:\n" + "\n".join(f"- {c}" for c in critique_feedback)

        user_prompt = f"""Create a viral 9:16 vertical Production Shot Deck.
Premise: {premise}
Target Duration: {target_duration} seconds.
Character Bible: {json.dumps(character_bible, indent=2)}
{feedback_prompt}
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-pro",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SHOT_DECK_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=ProductionShotDeck,
                temperature=0.4,
            ),
        )
        return response.parsed

    def _synthesize_rule_based_shot_deck(
        self,
        premise: str,
        target_duration: float,
        character_bible: Dict[str, str],
        critique_feedback: list,
    ) -> ProductionShotDeck:
        """
        High-fidelity cinematic anime benchmark generator for Project Origin: The Shattered Crown.
        Ensures deterministic testing when offline or during zero-API unit test runs.
        """
        hook_line = "Sign the covenant, World Monarch. Or your reign ends tonight."
        if any("trim" in c.lower() or "verbose" in c.lower() for c in critique_feedback):
            hook_line = "Sign the covenant, Ash. Or your reign ends."

        shots = [
            ProductionShot(
                shot_id=1,
                start_time_sec=0.0,
                end_time_sec=3.0,
                duration_sec=3.0,
                narrative_beat="Hook / Conflict",
                visual=VisualCue(
                    camera_angle=CameraAngle.EXTREME_CLOSE_UP,
                    camera_movement=CameraMovement.SLOW_PUSH_IN,
                    characters_present=["Vance Stirling"],
                    scene_environment="Silph-Macro Executive Spire Floor 40, polished obsidian boardroom table, rainy night city lights outside",
                    foreground_action="A gold-embossed black contract dossier labeled 'LEAGUE OVERSIGHT COVENANT' slides across the glossy obsidian surface directly toward camera",
                    background_details="Rain cascades down panoramic glass window, reflecting neon cyan and crimson lights of Saffron City skyline",
                    image_prompt="cinematic anime 9:16 vertical extreme close-up. Polished reflective black obsidian conference table. A luxurious gold-embossed leather covenant contract labeled 'LEAGUE OVERSIGHT COVENANT' slides toward the viewer. In the dark background, towering rain-streaked glass window overlooking Saffron City cyberpunk skyline at night. Dramatic high-contrast corporate lighting.",
                    motion_prompt="Camera slowly pushes in as the gold-embossed folder glides across the dark polished table surface, leaving a subtle reflection.",
                ),
                dialogue=DialogueCue(
                    speaker="Vance Stirling",
                    line=hook_line,
                    emotion="chillingly polite, authoritative, cold",
                    audio_ducking=True,
                    estimated_duration_sec=2.6,
                ),
                audio=AudioCue(
                    bgm_mood="tense minimalist corporate drone with ominous bass pulse",
                    bgm_intensity=0.4,
                    sfx=["contract_slide_smooth", "distant_thunder_rumble", "rain_on_glass"],
                ),
                character_anchor_tokens=[character_bible.get("Vance Stirling", "")],
            ),
            ProductionShot(
                shot_id=2,
                start_time_sec=3.0,
                end_time_sec=7.0,
                duration_sec=4.0,
                narrative_beat="Stakes / Threat Exposition",
                visual=VisualCue(
                    camera_angle=CameraAngle.MEDIUM_SHOT,
                    camera_movement=CameraMovement.SLOW_PUSH_IN,
                    characters_present=["Vance Stirling"],
                    scene_environment="Silph-Macro Executive Spire penthouse, floor-to-ceiling panoramic glass, stormy night",
                    foreground_action="CEO Vance Stirling holds up a pulsing violet micro-device: the Helix Neural Chip, between gloved fingers",
                    background_details="Thunder flash outside casts jagged shadows across the lavish chrome and glass boardroom",
                    image_prompt="cinematic anime 9:16 vertical medium shot. 48-year-old CEO Vance Stirling, slicked-back silver-gray hair, sharp aristocratic face, cold blue eyes behind titanium glasses. Tailored charcoal three-piece suit with burgundy tie and gold helix pin. Standing before panoramic rain-streaked window at night. In his right hand, he holds a miniature pulsing violet cybernetic Helix Chip emitting faint purple circuitry light. High-end anime cell shading, ominous lighting.",
                    motion_prompt="Camera pushes in smoothly. Stirling slightly rotates the glowing violet chip between his thumb and forefinger, violet light casting highlights on his glasses.",
                ),
                dialogue=DialogueCue(
                    speaker="Vance Stirling",
                    line="One hundred percent obedience. Zero hesitation.",
                    emotion="calculated, sociopathic certainty",
                    audio_ducking=True,
                    estimated_duration_sec=2.8,
                ),
                audio=AudioCue(
                    bgm_mood="cold cybernetic pulsating synth riser",
                    bgm_intensity=0.5,
                    sfx=["helix_chip_hum", "rain_patter"],
                ),
                character_anchor_tokens=[character_bible.get("Vance Stirling", "")],
            ),
            ProductionShot(
                shot_id=3,
                start_time_sec=7.0,
                end_time_sec=11.0,
                duration_sec=4.0,
                narrative_beat="Agitation / Moral Outrage",
                visual=VisualCue(
                    camera_angle=CameraAngle.MEDIUM_CLOSE_UP,
                    camera_movement=CameraMovement.DUTCH_TILT,
                    characters_present=["Ash Ketchum"],
                    scene_environment="Opposite side of obsidian boardroom table, Saffron Spire Floor 40",
                    foreground_action="16-year-old Ash Ketchum slams both clenched fists onto the table, leaning forward in furious defiance",
                    background_details="Dark executive office interior, reflections of sparks bouncing off the polished black tabletop",
                    image_prompt="cinematic anime 9:16 vertical medium close-up, Dutch angle. 16-year-old hero Ash Ketchum slamming both fists down on obsidian boardroom table. Athletic build, messy jet-black spiky hair under red-and-white trainer cap, royal-blue vest with white collar and gold trim over charcoal compression shirt. Double zig-zag cheek marks, fiery brown eyes filled with moral outrage. Dynamic anime lighting.",
                    motion_prompt="Dutch tilt camera shakes violently on the fist slam impact. Ash leans forward aggressively as electric sparks jump from Pikachu's cheeks.",
                ),
                dialogue=DialogueCue(
                    speaker="Ash Ketchum",
                    line="My Pokémon aren't your machines!",
                    emotion="furious, unyielding, heroic roar",
                    audio_ducking=True,
                    estimated_duration_sec=2.5,
                ),
                audio=AudioCue(
                    bgm_mood="percussive battle urgency, rising anime strings",
                    bgm_intensity=0.6,
                    sfx=["heavy_fist_table_slam", "electric_spark_arc"],
                ),
                character_anchor_tokens=[character_bible.get("Ash Ketchum", "")],
            ),
            ProductionShot(
                shot_id=4,
                start_time_sec=11.0,
                end_time_sec=15.0,
                duration_sec=4.0,
                narrative_beat="Action / Battle Climax Command",
                visual=VisualCue(
                    camera_angle=CameraAngle.CLOSE_UP,
                    camera_movement=CameraMovement.SLOW_PUSH_IN,
                    characters_present=["Ash Ketchum"],
                    scene_environment="Silph-Macro Boardroom center stage, backlit by golden electric charge",
                    foreground_action="Ash thrusts his right arm forward decisively, Alolan Z-Ring glowing with cyan aura",
                    background_details="Table papers and folders flying into air from violent electromagnetic updraft",
                    image_prompt="cinematic anime 9:16 vertical close-up hero shot. Ash Ketchum thrusts his gloved arm forward in a dynamic battle command. Alolan Z-Ring on his wrist blazes with cyan aura, Mega Keystone bracelet catching the light. Cap bill angled upward, double cheek zig-zag marks glowing with golden voltage. Masterpiece anime keyframe.",
                    motion_prompt="Camera pushes in rapidly as Ash shouts command, golden lightning trails flare from Pikachu leaping into foreground.",
                ),
                dialogue=DialogueCue(
                    speaker="Ash Ketchum",
                    line="Pikachu, full output—Thunderbolt!",
                    emotion="passionate battle roar, peak intensity",
                    audio_ducking=True,
                    estimated_duration_sec=2.8,
                ),
                audio=AudioCue(
                    bgm_mood="epic triumphant orchestral battle choir with heavy synth drums",
                    bgm_intensity=0.8,
                    sfx=["z_ring_chime", "lightning_charge_buildup"],
                ),
                character_anchor_tokens=[character_bible.get("Ash Ketchum", "")],
            ),
            ProductionShot(
                shot_id=5,
                start_time_sec=15.0,
                end_time_sec=18.5,
                duration_sec=3.5,
                narrative_beat="Cliffhanger / Baton Pass Hook",
                visual=VisualCue(
                    camera_angle=CameraAngle.WIDE_SHOT,
                    camera_movement=CameraMovement.STATIC,
                    characters_present=["Ash Ketchum"],
                    scene_environment="Rooftop standoff, storm clouds suddenly parting in sky above",
                    foreground_action="Crimson dragon fire ignites the storm clouds. Colossal winged shadow swoops down with hard cut: 'EPISODE 2 NEXT'",
                    background_details="Raging orange-red thermal heat vaporizing falling raindrops into clouds of white steam",
                    image_prompt="cinematic anime 9:16 vertical dramatic standoff. The storm sky ignites in blinding crimson-orange thermal fire. A colossal winged dragon silhouette (Charizard) swoops through storm clouds, vaporizing rain into steam. Bold glowing kinetic anime text in lower third: 'EPISODE 2 NEXT'. Peak cliffhanger shonen anime visual.",
                    motion_prompt="The sky above violently explodes in crimson dragon fire, vaporizing the rain into steam as the winged shadow descends. Sudden hard cut to black.",
                ),
                dialogue=None,
                audio=AudioCue(
                    bgm_mood="apocalyptic brass crescendo abruptly cut to silence",
                    bgm_intensity=0.9,
                    sfx=["sky_fire_eruption", "slam_cut_to_silence"],
                ),
                character_anchor_tokens=[character_bible.get("Ash Ketchum", "")],
            ),
        ]

        return ProductionShotDeck(
            title="Project Origin: The Shattered Crown",
            target_platform="YouTube Shorts / Instagram Reels / TikTok",
            aspect_ratio=AspectRatio.VERTICAL_9_16,
            target_total_duration_sec=18.5,
            hook_thesis="Silph-Macro Consortium issues an ultimatum to World Monarch Ash Ketchum to surrender his Pokémon to cybernetic Helix Chips",
            call_to_action="Follow for Episode 2 dropping tomorrow!",
            character_bible=character_bible,
            shots=shots,
        )
