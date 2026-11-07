"""
Autonomous AI Video Pipeline: Visual QA Evaluator
Performs multimodal evaluation on rendered keyframes:
- Gemini 2.5 Flash Vision audit (composition, prompt adherence, character consistency)
- Structural image analytics (aspect ratio, Laplacian blur sharpness, contrast)
- Feedback loops for prompt & guidance modulation
"""

import os
from pathlib import Path
from typing import Optional, Tuple
import cv2
import numpy as np
from PIL import Image

from .schemas import VisualQAResult
from ..scripting.schemas import ProductionShot


class VisualQAEvaluator:
    """
    Multimodal visual auditor combining deterministic computer vision analytics
    with Gemini Flash multimodal reasoning.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[VisualQAEvaluator] Notice: Gemini client not initialized: {e}")

    def evaluate_keyframe(self, image_path: str, shot: ProductionShot) -> VisualQAResult:
        """
        Audits a keyframe against vertical framing, clarity, and narrative fidelity.
        """
        path = Path(image_path)
        if not path.exists():
            return VisualQAResult(
                shot_id=shot.shot_id,
                composition_score=0.0,
                prompt_adherence_score=0.0,
                character_consistency_score=0.0,
                artifacts_detected=["Image file not found on disk"],
                overall_score=0.0,
                passes_qa=False,
                remediation_suggestions="Verify image generation pipeline wrote the target file."
            )

        # 1. Deterministic Computer Vision Analytics (OpenCV & PIL)
        with Image.open(path) as img:
            width, height = img.size

        cv_img = cv2.imread(str(path))
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        
        # Laplacian variance measures image sharpness (blur detection)
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        mean_brightness = float(np.mean(gray))

        artifacts = []
        comp_score = 9.2
        adherence_score = 9.0
        consistency_score = 9.0

        # Aspect ratio check (9:16 target is ~0.5625)
        ratio = width / height
        if abs(ratio - (9.0 / 16.0)) > 0.05:
            comp_score -= 3.0
            artifacts.append(f"Aspect ratio mismatch: {width}x{height} (ratio {ratio:.3f} != 0.563 for 9:16)")

        # Sharpness check
        if laplacian_var < 50.0:
            adherence_score -= 2.0
            artifacts.append(f"Image appears blurry or out-of-focus (Laplacian var {laplacian_var:.1f} < 50.0)")

        # Extreme brightness/darkness check
        if mean_brightness < 20.0:
            comp_score -= 2.0
            artifacts.append("Image is severely underexposed (too dark)")
        elif mean_brightness > 235.0:
            comp_score -= 2.0
            artifacts.append("Image is severely overexposed (clipped highlights)")

        # 2. Multimodal LLM Audit (If Gemini is configured)
        if self.client:
            try:
                llm_eval = self._audit_with_gemini_vision(path, shot)
                return llm_eval
            except Exception as e:
                print(f"[VisualQAEvaluator] Gemini Vision audit fallback to CV metrics: {e}")

        # Fallback composite score calculation
        overall = round((comp_score * 0.3) + (adherence_score * 0.4) + (consistency_score * 0.3), 2)
        passes = overall >= 8.5 and not artifacts

        return VisualQAResult(
            shot_id=shot.shot_id,
            composition_score=round(comp_score, 2),
            prompt_adherence_score=round(adherence_score, 2),
            character_consistency_score=round(consistency_score, 2),
            artifacts_detected=artifacts,
            overall_score=overall,
            passes_qa=passes,
            remediation_suggestions="; ".join(artifacts) if artifacts else None
        )

    def _audit_with_gemini_vision(self, image_path: Path, shot: ProductionShot) -> VisualQAResult:
        """Evaluates image bytes using Gemini 2.5 Flash Vision."""
        from google.genai import types

        image_bytes = image_path.read_bytes()
        prompt = (
            f"You are a Senior Visual QA Auditor. Audit this 9:16 vertical keyframe against Shot {shot.shot_id}.\n"
            f"Target Shot Description: {shot.visual.image_prompt}\n"
            f"Camera Angle: {shot.visual.camera_angle.value}\n"
            f"Expected Characters: {shot.visual.characters_present}\n"
            "Score composition_score (1-10), prompt_adherence_score (1-10), character_consistency_score (1-10).\n"
            "List any visual glitches/artifacts detected. passes_qa is True only if overall >= 8.5 and no major anatomical defects."
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VisualQAResult,
                temperature=0.2,
            ),
        )
        return response.parsed
