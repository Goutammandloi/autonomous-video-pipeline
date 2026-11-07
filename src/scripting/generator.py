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
                "Rajat": "20-year-old Indian college student, messy textured fade haircut, navy blue oversized hoodie, expressive comedic delivery",
                "Didi": "24-year-old Indian elder sister, neat high ponytail, mustard-yellow embroidered kurti, authoritative, expressive eyes",
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
        High-fidelity template generator calibrated for viral collegiate Hinglish ads (Appin benchmark).
        Ensures deterministic testing when offline or during zero-API unit test runs.
        """
        # Trim hook words if previously critiqued
        hook_line = "Rajat! Phir se Netflix? Placement season chal raha hai!"
        if any("trim" in c.lower() or "verbose" in c.lower() for c in critique_feedback):
            hook_line = "Rajat! Phir se Netflix? Placement season hai!"

        shots = [
            ProductionShot(
                shot_id=1,
                start_time_sec=0.0,
                end_time_sec=3.0,
                duration_sec=3.0,
                narrative_beat="Hook / Conflict",
                visual=VisualCue(
                    camera_angle=CameraAngle.MEDIUM_TWO_SHOT,
                    camera_movement=CameraMovement.SLOW_PUSH_IN,
                    characters_present=["Didi", "Rajat"],
                    scene_environment="Indian bedroom study, wooden desk, fairy lights in background",
                    foreground_action="Didi rips off Rajat's headphones while he sits with Netflix open and a packet of chips",
                    background_details="Messy books on shelf, warm 3200K study lamp, framed graduation photo",
                    image_prompt="A medium two-shot inside an Indian bedroom study. A 24-year-old Indian female with hair tied in a loose ponytail, wearing a mustard-yellow embroidered kurti, angrily confronting a 20-year-old Indian boy in navy blue hoodie who is distracted with laptop and snacks. Warm cinematic lighting, 9:16 vertical framing.",
                    motion_prompt="Camera pushes in slowly. The elder sister reaches down abruptly, pulling off the black headphones from the boy's head. The boy flinches in surprise.",
                ),
                dialogue=DialogueCue(
                    speaker="Didi",
                    line=hook_line,
                    emotion="authoritative, confrontational",
                    audio_ducking=True,
                    estimated_duration_sec=2.8,
                ),
                audio=AudioCue(
                    bgm_mood="tense comedic percussion",
                    bgm_intensity=0.4,
                    sfx=["record_scratch", "headphone_yank"],
                ),
                character_anchor_tokens=[
                    character_bible.get("Didi", ""),
                    character_bible.get("Rajat", ""),
                ],
            ),
            ProductionShot(
                shot_id=2,
                start_time_sec=3.0,
                end_time_sec=6.5,
                duration_sec=3.5,
                narrative_beat="Agitation / Dismissal",
                visual=VisualCue(
                    camera_angle=CameraAngle.OVER_THE_SHOULDER,
                    camera_movement=CameraMovement.HANDHELD_ORGANIC,
                    characters_present=["Rajat"],
                    scene_environment="Indian bedroom study desk",
                    foreground_action="Rajat smirks confidently, leaning back in his ergonomic chair, gesturing dismissively",
                    background_details="Sister's shoulder visible in extreme foreground, room ambient light",
                    image_prompt="Over-the-shoulder medium shot from behind the elder sister. A 20-year-old Indian boy in navy blue hoodie smirks confidently, making an easy dismissive hand wave. Photorealistic, 9:16 vertical portrait, shallow depth of field.",
                    motion_prompt="Subtle handheld camera float. The boy laughs lightly, waves his hand, and tilts his head with relaxed self-assurance.",
                ),
                dialogue=DialogueCue(
                    speaker="Rajat",
                    line="Arey tension kyun le rahi ho Didi, chill karo na!",
                    emotion="smirking, overly relaxed",
                    audio_ducking=True,
                    estimated_duration_sec=3.0,
                ),
                audio=AudioCue(
                    bgm_mood="bouncy comedic synth",
                    bgm_intensity=0.35,
                    sfx=["pop_click"],
                ),
                character_anchor_tokens=[character_bible.get("Rajat", "")],
            ),
            ProductionShot(
                shot_id=3,
                start_time_sec=6.5,
                end_time_sec=10.5,
                duration_sec=4.0,
                narrative_beat="The Twist / Screen Reveal",
                visual=VisualCue(
                    camera_angle=CameraAngle.POV,
                    camera_movement=CameraMovement.TRACKING_FOLLOW,
                    characters_present=["Rajat"],
                    scene_environment="Laptop screen on wooden desk",
                    foreground_action="Rajat spins his laptop around to show Didi. The screen shows the modern Appin Technology Cyber Security Lab terminal with live code",
                    background_details="Hands holding laptop chassis, blurred warm bedroom in background",
                    image_prompt="A cinematic vertical 9:16 first-person POV shot of a modern laptop screen being turned toward the viewer. The screen displays a sleek, glowing dark-mode terminal dashboard with 'Appin Technology Cyber Security Lab' branding, vulnerability scanner, and live code.",
                    motion_prompt="First-person POV smooth motion. The hands firmly hold the laptop chassis, tilting and pivoting the screen smoothly 90 degrees directly toward the camera lens.",
                ),
                dialogue=DialogueCue(
                    speaker="Rajat",
                    line="Netflix nahi, Appin Technology ka live cyber lab chal raha hai!",
                    emotion="triumphant, confident",
                    audio_ducking=True,
                    estimated_duration_sec=3.5,
                ),
                audio=AudioCue(
                    bgm_mood="high-energy futuristic synth riser",
                    bgm_intensity=0.5,
                    sfx=["laptop_swivel", "tech_whoosh"],
                ),
                character_anchor_tokens=[character_bible.get("Rajat", "")],
            ),
            ProductionShot(
                shot_id=4,
                start_time_sec=10.5,
                end_time_sec=14.5,
                duration_sec=4.0,
                narrative_beat="Climax / Sister Reaction",
                visual=VisualCue(
                    camera_angle=CameraAngle.CLOSE_UP,
                    camera_movement=CameraMovement.SLOW_PUSH_IN,
                    characters_present=["Didi"],
                    scene_environment="Indian bedroom study",
                    foreground_action="Didi bends down closer to the screen, her skepticism transforming into genuine awe and excitement",
                    background_details="Reflected green code glow on her face, mustard kurti visible",
                    image_prompt="A close-up shot of the 24-year-old Indian female with expressive eyes, her skepticism turning into genuine surprise and curiosity as she inspects the screen. Soft green and cyan ambient terminal reflection on her cheek. 9:16 vertical framing.",
                    motion_prompt="Camera inches closer in a subtle push-in. The sister's eyes widen, her mouth slightly parts in amazement, and she leans forward.",
                ),
                dialogue=DialogueCue(
                    speaker="Didi",
                    line="Wait... practical training aur 100% placement support?",
                    emotion="shocked, impressed",
                    audio_ducking=True,
                    estimated_duration_sec=3.5,
                ),
                audio=AudioCue(
                    bgm_mood="triumphant upbeat corporate tech",
                    bgm_intensity=0.45,
                    sfx=["lightbulb_ding"],
                ),
                character_anchor_tokens=[character_bible.get("Didi", "")],
            ),
            ProductionShot(
                shot_id=5,
                start_time_sec=14.5,
                end_time_sec=18.5,
                duration_sec=4.0,
                narrative_beat="Call to Action (CTA)",
                visual=VisualCue(
                    camera_angle=CameraAngle.MEDIUM_CLOSE_UP,
                    camera_movement=CameraMovement.STATIC,
                    characters_present=["Rajat"],
                    scene_environment="Study room with Appin Technology banner graphic overlay",
                    foreground_action="Rajat gives a confident wink and thumbs-up to the camera while Didi pulls the laptop to book a demo session",
                    background_details="Appin Technology logo overlay and 'Book Free Demo' CTA card",
                    image_prompt="A punchy medium close-up of the 20-year-old Indian boy looking directly at the camera, giving a charismatic wink and a thumbs up, smirking playfully. In the blurred background, his sister aggressively types on the laptop. 9:16 vertical frame.",
                    motion_prompt="The boy winks smoothly, points finger gun or thumbs up to the camera. Background sister furiously types and clicks the mouse.",
                ),
                dialogue=DialogueCue(
                    speaker="Rajat",
                    line="Toh career mein upgrade chahiye? Abhi bio ke link se free demo book karo!",
                    emotion="charismatic, energetic CTA",
                    audio_ducking=True,
                    estimated_duration_sec=3.8,
                ),
                audio=AudioCue(
                    bgm_mood="high-energy upbeat outro",
                    bgm_intensity=0.55,
                    sfx=["camera_shutter", "bass_drop"],
                ),
                character_anchor_tokens=[character_bible.get("Rajat", "")],
            ),
        ]

        return ProductionShotDeck(
            title="Appin Career Ka Asli Netflix",
            target_platform="YouTube Shorts / Instagram Reels",
            aspect_ratio=AspectRatio.VERTICAL_9_16,
            target_total_duration_sec=18.5,
            hook_thesis="Elder sister catches brother distracted during placement season, discovering he is actually mastering cybersecurity hands-on",
            call_to_action="Book a free demo session via the link in bio",
            character_bible=character_bible,
            shots=shots,
        )
