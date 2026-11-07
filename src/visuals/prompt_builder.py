"""
Autonomous AI Video Pipeline: Visual Prompt Builder
Applies composition rules from .agents/skills/visual-composition
and quality guardrails from .agents/skills/visual-quality-improver.
Injects immutable character anchor tokens to prevent identity drift.
"""

from typing import Dict, List, Optional
from ..scripting.schemas import ProductionShot, CameraAngle, CameraMovement


class PromptBuilder:
    """
    Expands raw visual prompts into dense, photorealistic, style-anchored prompts
    optimized for Google Imagen 3, FLUX, and SDXL models.
    """

    CINEMATIC_CAMERA_LENS_MAP = {
        CameraAngle.EXTREME_CLOSE_UP: "macro 100mm lens, ultra-shallow depth of field, sharp focus on facial emotion and eyes",
        CameraAngle.CLOSE_UP: "85mm portrait prime lens, f/1.8 aperture, soft cinematic bokeh, crisp facial details",
        CameraAngle.MEDIUM_CLOSE_UP: "50mm prime lens, natural human eye perspective, cinematic lighting balance",
        CameraAngle.MEDIUM_SHOT: "35mm lens, balanced subject and environment, golden ratio vertical framing",
        CameraAngle.MEDIUM_TWO_SHOT: "35mm anamorphic lens, two subjects dynamically framed in 9:16 vertical space, clear spatial interaction",
        CameraAngle.OVER_THE_SHOULDER: "50mm lens, foreground shoulder softly blurred, sharp focus on the reacting subject in midground",
        CameraAngle.POV: "24mm wide angle first-person POV, natural arm/hand perspective reaching into the frame, immersive depth",
        CameraAngle.WIDE_SHOT: "24mm lens, deep depth of field, establishing environmental architecture and mood",
    }

    NEGATIVE_QUALITY_BASE = (
        "distorted face, mutated eyes, asymmetric pupils, unnatural smile, extra fingers, missing limbs, "
        "fused hands, blurry, low resolution, noisy, plastic artificial skin, 3d render look, illustration, "
        "cgi cartoon, watermark, logo, text overlay, black borders, letterboxing, pillarboxing, warped geometry"
    )

    @classmethod
    def build_dense_prompt(
        cls,
        shot: ProductionShot,
        character_bible: Dict[str, str],
        lighting_style: str = "Warm cinematic 3200K tungsten lamp with soft cyan computer screen rim light",
        aesthetic_movement: str = "Contemporary hyper-realistic cinema, 35mm film grain texture, natural pores"
    ) -> str:
        """
        Constructs an immutable-anchored, compositionally sound keyframe prompt.
        """
        vis = shot.visual
        lens_spec = cls.CINEMATIC_CAMERA_LENS_MAP.get(vis.camera_angle, "50mm portrait prime lens")

        # 1. Gather active character anchor tokens
        char_tokens = []
        for char_name in vis.characters_present:
            desc = character_bible.get(char_name)
            if desc:
                char_tokens.append(f"[{char_name}: {desc}]")
            elif char_name in shot.character_anchor_tokens:
                char_tokens.append(f"[{char_name}: {shot.character_anchor_tokens[0]}]")

        char_block = " | ".join(char_tokens) if char_tokens else "Contemporary subject"

        # 2. Build dense cinematic prompt
        dense_prompt = (
            f"Cinematic vertical 9:16 photograph. {vis.image_prompt}. "
            f"Subjects: {char_block}. "
            f"Camera & Optics: {lens_spec}, {vis.camera_angle.value} framing. "
            f"Environment: {vis.scene_environment}, {vis.background_details}. "
            f"Lighting & Atmosphere: {lighting_style}. "
            f"Aesthetic Grade: {aesthetic_movement}, 8k resolution, authentic skin texture, color graded in DaVinci Resolve."
        )

        return dense_prompt.strip()

    @classmethod
    def build_negative_prompt(cls, shot: ProductionShot, additional_negatives: Optional[List[str]] = None) -> str:
        """
        Curates negative constraints based on shot dynamics.
        """
        base = [cls.NEGATIVE_QUALITY_BASE]
        if shot.visual.camera_angle == CameraAngle.POV:
            base.append("third person view, full body showing, floating head")
        elif shot.visual.camera_angle == CameraAngle.CLOSE_UP:
            base.append("full body shot, distant subject, tiny face")

        if additional_negatives:
            base.extend(additional_negatives)

        return ", ".join(base)
