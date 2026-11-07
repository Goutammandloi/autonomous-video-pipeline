"""
Autonomous AI Video Pipeline: Social Distribution & Scheduling Schemas
Defines platform types, metadata models, queue jobs, and batch dispatch reports.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PlatformType(str, Enum):
    """Supported social media destination platforms."""
    YOUTUBE_SHORTS = "youtube_shorts"
    INSTAGRAM_REELS = "instagram_reels"
    TIKTOK = "tiktok"
    LINKEDIN = "linkedin"
    TWITTER_X = "twitter_x"


class PrivacyStatus(str, Enum):
    """Visibility setting for published or scheduled media."""
    PUBLIC = "public"
    UNLISTED = "unlisted"
    PRIVATE = "private"
    SCHEDULED = "scheduled"


class SocialPlatformMetadata(BaseModel):
    """Tailored metadata package for a specific social network."""
    platform: PlatformType
    title: str = Field(description="Platform-optimized title or opening hook line")
    caption_or_description: str = Field(description="Full text caption / description with emojis and CTAs")
    hashtags: List[str] = Field(default_factory=list, description="Targeted SEO and algorithmic hashtags")
    tags: List[str] = Field(default_factory=list, description="Video metadata search tags (for YouTube/SEO)")
    pinned_comment: Optional[str] = Field(default=None, description="Optional high-conversion first comment")
    cta_link: str = Field(default="https://appintechnology.com/cybersecurity-demo", description="Conversion landing URL")


class SchedulingSlot(BaseModel):
    """Audience-optimized publication time window."""
    platform: PlatformType
    target_publish_time_iso: str = Field(description="ISO 8601 UTC timestamp (e.g. 2026-11-08T13:00:00Z)")
    timezone: str = Field(default="Asia/Kolkata", description="Target audience local timezone")
    optimal_reasoning: str = Field(description="Algorithmic rationale for the chosen timing")


class DispatchJob(BaseModel):
    """A scheduled or published dispatch unit for a single platform."""
    job_id: str
    platform: PlatformType
    video_path: str
    metadata: SocialPlatformMetadata
    scheduled_time_iso: str
    privacy_status: PrivacyStatus = PrivacyStatus.SCHEDULED
    status: str = Field(default="PENDING", description="PENDING | DISPATCHING | SCHEDULED | PUBLISHED | FAILED")
    remote_content_id: Optional[str] = None
    remote_url: Optional[str] = None
    retry_count: int = 0
    error_message: Optional[str] = None
    log_history: List[str] = Field(default_factory=list)


class DispatchBatchReport(BaseModel):
    """Summary of multi-platform distribution and scheduling jobs."""
    batch_id: str
    created_at_iso: str
    project_title: str
    total_jobs: int
    scheduled_jobs: int
    published_jobs: int
    failed_jobs: int
    jobs: List[DispatchJob] = Field(default_factory=list)
