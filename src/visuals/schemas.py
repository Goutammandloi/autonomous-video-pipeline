"""
Autonomous AI Video Pipeline: Visuals & Keyframe Schemas
Defines data structures for keyframe generation, resolution constraints,
character style anchoring, and multimodal vision evaluation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class KeyframeMetadata(BaseModel):
    shot_id: int = Field(..., description="Corresponding shot index")
    aspect_ratio: str = Field("9:16", description="Target aspect ratio")
    width: int = Field(1080, description="Width in pixels")
    height: int = Field(1920, description="Height in pixels")
    prompt_used: str = Field(..., description="Final anchored prompt dispatched to image model")
    negative_prompt_used: str = Field(..., description="Negative prompt applied")
    backend_model: str = Field(..., description="Generator model identifier (e.g. imagen-3.0-generate-002)")
    seed: Optional[int] = Field(None, description="Generation seed for reproducibility")


class VisualQAResult(BaseModel):
    shot_id: int = Field(..., description="Evaluated shot index")
    composition_score: float = Field(..., ge=0.0, le=10.0, description="Rule-of-thirds, vertical 9:16 framing (1-10)")
    prompt_adherence_score: float = Field(..., ge=0.0, le=10.0, description="Accuracy of characters, props, actions (1-10)")
    character_consistency_score: float = Field(..., ge=0.0, le=10.0, description="Identity retention against style bible (1-10)")
    artifacts_detected: List[str] = Field(default_factory=list, description="Visual defects (e.g. extra fingers, blurry face, warped text)")
    overall_score: float = Field(..., ge=0.0, le=10.0, description="Composite visual quality score")
    passes_qa: bool = Field(..., description="True if overall >= 8.5 and consistency >= 8.0")
    remediation_suggestions: Optional[str] = Field(None, description="Suggested prompt or hyperparameter tweaks if failed")


class KeyframeAsset(BaseModel):
    shot_id: int = Field(..., description="Shot ID")
    file_path: str = Field(..., description="Local absolute path to rendered keyframe image")
    metadata: KeyframeMetadata = Field(..., description="Generation parameters")
    qa_result: Optional[VisualQAResult] = Field(None, description="Multimodal QA audit outcome")
    status: str = Field("GENERATED", description="Status: GENERATED, QA_PASSED, QA_FAILED, RETRIED")
