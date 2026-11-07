"""
Autonomous AI Video Pipeline: Scripting & Shot Deck Schemas
Defines strictly typed Pydantic models for narrative generation,
shot-by-shot continuity tokens, camera motion vectors, and QA evaluation.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class AspectRatio(str, Enum):
    VERTICAL_9_16 = "9:16"
    WIDESCREEN_16_9 = "16:9"
    SQUARE_1_1 = "1:1"


class CameraAngle(str, Enum):
    EXTREME_CLOSE_UP = "extreme_close_up"
    CLOSE_UP = "close_up"
    MEDIUM_CLOSE_UP = "medium_close_up"
    MEDIUM_SHOT = "medium_shot"
    MEDIUM_TWO_SHOT = "medium_two_shot"
    OVER_THE_SHOULDER = "over_the_shoulder"
    POV = "first_person_pov"
    WIDE_SHOT = "wide_shot"


class CameraMovement(str, Enum):
    STATIC = "static"
    SLOW_PUSH_IN = "slow_push_in"
    PULL_BACK = "pull_back"
    WHIP_PAN = "whip_pan"
    HANDHELD_ORGANIC = "handheld_organic"
    DUTCH_TILT = "dutch_tilt"
    TRACKING_FOLLOW = "tracking_follow"


class DialogueCue(BaseModel):
    speaker: str = Field(..., description="Name of the character speaking or 'Narrator'")
    line: str = Field(..., description="Spoken dialogue text (Hinglish, Hindi, or English)")
    emotion: str = Field(..., description="Vocal delivery emotion (e.g. sarcastic, panicked, confident, shocked)")
    audio_ducking: bool = Field(True, description="Whether background music must duck down during this line")
    estimated_duration_sec: float = Field(..., description="Estimated speech duration in seconds")


class AudioCue(BaseModel):
    bgm_mood: str = Field(..., description="Background music energy/mood (e.g. energetic synthwave, tense ambient, comedic bassoon)")
    bgm_intensity: float = Field(0.5, ge=0.0, le=1.0, description="Music volume factor relative to voice (0.0 to 1.0)")
    sfx: Optional[List[str]] = Field(default_factory=list, description="Sound effect cues (e.g. 'record_scratch', 'whoosh', 'keyboard_clicks')")


class VisualCue(BaseModel):
    camera_angle: CameraAngle = Field(..., description="Framing angle for the shot")
    camera_movement: CameraMovement = Field(..., description="Camera motion trajectory")
    characters_present: List[str] = Field(default_factory=list, description="List of character names visible in the frame")
    scene_environment: str = Field(..., description="Setting/environment description (e.g. 'Indian bedroom study, wooden desk, fairy lights')")
    foreground_action: str = Field(..., description="Detailed action taking place in foreground")
    background_details: str = Field(..., description="Lighting, props, and ambient background details")
    image_prompt: str = Field(..., description="Optimized, dense prompt for keyframe generation (Imagen 3 / FLUX)")
    negative_prompt: str = Field("distorted face, extra fingers, blurry, low resolution, warped text, bad anatomy", description="Negative prompt constraints")
    motion_prompt: str = Field(..., description="Motion synthesis prompt for I2V model (e.g. Veo / Kling)")


class ProductionShot(BaseModel):
    shot_id: int = Field(..., description="Sequential index of the shot (1-indexed)")
    start_time_sec: float = Field(..., description="Timeline start timestamp in seconds")
    end_time_sec: float = Field(..., description="Timeline end timestamp in seconds")
    duration_sec: float = Field(..., description="Duration of this specific shot in seconds")
    narrative_beat: str = Field(..., description="Narrative purpose: Hook, Conflict, Agitation, Twist, Climax, CTA")
    visual: VisualCue = Field(..., description="Visual composition and generative prompts")
    dialogue: Optional[DialogueCue] = Field(None, description="Spoken dialogue if someone speaks in this shot")
    audio: AudioCue = Field(..., description="Acoustic and sound design cues")
    character_anchor_tokens: List[str] = Field(
        default_factory=list,
        description="Immutable tokens describing active characters to maintain visual consistency"
    )


class ProductionShotDeck(BaseModel):
    title: str = Field(..., description="Working title of the video project")
    target_platform: str = Field("YouTube Shorts / Instagram Reels", description="Primary release destination")
    aspect_ratio: AspectRatio = Field(AspectRatio.VERTICAL_9_16, description="Output aspect ratio")
    target_total_duration_sec: float = Field(..., description="Target duration (typically 30s to 60s)")
    hook_thesis: str = Field(..., description="The core curiosity trigger or pattern interrupt used in the first 3 seconds")
    call_to_action: str = Field(..., description="Final action prompt for the viewer")
    character_bible: dict = Field(
        default_factory=dict,
        description="Canonical style bible for recurring characters (attire, physical attributes, hair)"
    )
    shots: List[ProductionShot] = Field(..., description="Ordered sequence of production shots")


class ScriptEvaluationCritique(BaseModel):
    hook_score: float = Field(..., ge=0.0, le=10.0, description="Hook strength & retention in first 3s (1-10)")
    pacing_score: float = Field(..., ge=0.0, le=10.0, description="Rhythm, tension escalation and flow (1-10)")
    dialogue_naturalness: float = Field(..., ge=0.0, le=10.0, description="Conversational authenticity (Hinglish/English collegiate tone) (1-10)")
    visual_continuity_feasibility: float = Field(..., ge=0.0, le=10.0, description="Feasibility of generating consistent visual assets (1-10)")
    overall_score: float = Field(..., ge=0.0, le=10.0, description="Composite weighted quality score")
    passes_quality_gate: bool = Field(..., description="True if overall >= 8.5 and hook >= 8.5")
    flaws_and_bottlenecks: List[str] = Field(default_factory=list, description="Specific identified defects or weak points")
    actionable_refinements: List[str] = Field(default_factory=list, description="Concrete adjustments to apply in the next revision")
