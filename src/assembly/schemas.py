"""
Autonomous AI Video Pipeline: Assembly & Mastering Data Schemas
Defines configuration, subtitle styling, timeline segments, and mastering quality reports.
"""

from typing import List, Tuple, Optional, Dict, Any
from pydantic import BaseModel, Field


class ActiveWordHighlight(BaseModel):
    """Timing for an individual word in a kinetic caption stream."""
    word: str
    start_time_sec: float
    end_time_sec: float


class SubtitleSegment(BaseModel):
    """A dialogue segment tied to a timeline interval with word-level annotations."""
    shot_id: int
    speaker: str
    full_text: str
    start_time_sec: float
    end_time_sec: float
    words: List[ActiveWordHighlight] = Field(default_factory=list)


class SubtitleStyleConfig(BaseModel):
    """Visual design parameters for social media kinetic typography (9:16 vertical)."""
    font_path: str = Field(default="C:/Windows/Fonts/arialbd.ttf", description="Path to TTF bold font")
    font_size: int = Field(default=56, description="Font point size (optimized for 1080x1920)")
    primary_color: Tuple[int, int, int] = Field(default=(255, 255, 255), description="Standard text color (RGB)")
    highlight_color: Tuple[int, int, int] = Field(default=(255, 225, 0), description="Active spoken word highlight (RGB)")
    speaker_color: Tuple[int, int, int] = Field(default=(0, 235, 255), description="Speaker tag accent color (RGB)")
    stroke_color: Tuple[int, int, int] = Field(default=(10, 10, 10), description="Text outline border color (RGB)")
    stroke_width: int = Field(default=5, description="Border outline width for contrast")
    bg_pill_color: Optional[Tuple[int, int, int, int]] = Field(
        default=(15, 15, 15, 185),
        description="RGBA rounded rectangle container backdrop"
    )
    position_y_ratio: float = Field(
        default=0.74,
        description="Vertical placement ratio from top (0.74 = ~1420px, clear of UI overlays)"
    )
    max_words_per_chunk: int = Field(default=5, description="Max visible words per subtitle line")


class AssemblyConfig(BaseModel):
    """Encoding and layout specification for the master video compilation."""
    resolution: Tuple[int, int] = Field(default=(1080, 1920), description="(width, height)")
    fps: float = Field(default=30.0, description="CFR frame rate")
    video_codec: str = Field(default="libx264", description="H.264 video encoder")
    preset: str = Field(default="fast", description="FFmpeg x264 preset")
    crf: int = Field(default=18, description="Constant Rate Factor (18 = visually lossless)")
    pixel_format: str = Field(default="yuv420p", description="Standard 8-bit YUV for universal compatibility")
    audio_codec: str = Field(default="aac", description="AAC audio encoder")
    audio_bitrate: str = Field(default="192k", description="Audio bitrate")
    burn_subtitles: bool = Field(default=True, description="Whether to render kinetic subtitles onto frames")


class MasterVideoReport(BaseModel):
    """Comprehensive QA evaluation report for the final assembled video master."""
    video_path: str
    total_duration_sec: float
    total_frames: int
    resolution: Tuple[int, int]
    fps: float
    file_size_bytes: int
    has_audio: bool
    audio_duration_sec: float
    av_sync_delta_ms: float
    qa_passed: bool
    qa_score: float = Field(ge=0.0, le=10.0)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    qa_notes: List[str] = Field(default_factory=list)
