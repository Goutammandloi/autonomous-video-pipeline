"""
Autonomous AI Video Pipeline: Motion & Compositing Schemas
Defines data structures for I2V motion synthesis, camera kinematic vectors,
OpenCV perspective screen warps, and optical flow glitch detection.
"""

from typing import List, Optional, Tuple
from pydantic import BaseModel, Field
from ..compositor.screen_warper import CornerPoints


class MotionVector(BaseModel):
    pan_x: float = Field(0.0, description="Horizontal camera pan velocity (-1.0 to 1.0)")
    pan_y: float = Field(0.0, description="Vertical camera tilt velocity (-1.0 to 1.0)")
    zoom_ratio: float = Field(1.0, description="Scale/zoom factor (>1.0 = push in, <1.0 = pull back)")
    rotation_deg: float = Field(0.0, description="Camera roll angle in degrees")
    motion_bucket_id: int = Field(100, ge=1, le=255, description="Motion strength parameter (standard: 85-127)")


class OpticalFlowQAResult(BaseModel):
    shot_id: int = Field(..., description="Evaluated shot index")
    total_frames_audited: int = Field(..., description="Number of evaluated frame pairs")
    mean_flow_magnitude: float = Field(..., description="Average motion displacement vector magnitude")
    max_flow_z_score: float = Field(..., description="Maximum outlier motion Z-score (threshold <= 3.5)")
    anomalous_frames: List[int] = Field(default_factory=list, description="Frame indices flagged for abrupt distortion")
    passes_qa: bool = Field(..., description="True if max_flow_z_score <= 3.5 and no major warping anomalies")
    remediation_applied: Optional[str] = Field(None, description="Surgical parameter patch applied if defect detected")


class VideoClipAsset(BaseModel):
    shot_id: int = Field(..., description="Shot index")
    file_path: str = Field(..., description="Path to generated MP4 video clip")
    duration_sec: float = Field(..., description="Exact video duration in seconds")
    fps: int = Field(30, description="Frame rate (Constant Frame Rate 30 fps)")
    width: int = Field(1080, description="Width in pixels (9:16 vertical = 1080)")
    height: int = Field(1920, description="Height in pixels (9:16 vertical = 1920)")
    total_frames: int = Field(..., description="Total rendered frames count")
    has_screen_inset: bool = Field(False, description="True if perspective screen warping was applied")
    qa_result: Optional[OpticalFlowQAResult] = Field(None, description="Optical flow glitch evaluation outcome")
    status: str = Field("GENERATED", description="Status: GENERATED, QA_PASSED, QA_REMEDIATED")
