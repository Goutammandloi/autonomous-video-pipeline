"""
Autonomous AI Video Pipeline: Assembly & Final Mastering Module
"""

from .schemas import (
    AssemblyConfig,
    SubtitleStyleConfig,
    MasterVideoReport,
    SubtitleSegment,
    ActiveWordHighlight
)
from .subtitle_burner import SubtitleBurner
from .timeline_assembler import TimelineAssembler
from .evaluator import AssemblyQAEvaluator

__all__ = [
    "AssemblyConfig",
    "SubtitleStyleConfig",
    "MasterVideoReport",
    "SubtitleSegment",
    "ActiveWordHighlight",
    "SubtitleBurner",
    "TimelineAssembler",
    "AssemblyQAEvaluator"
]
