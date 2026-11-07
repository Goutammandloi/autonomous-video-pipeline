"""
Autonomous AI Video Pipeline: Audio & Acoustic Mastering Schemas
Defines data structures for voice personas, speech synthesis, word boundaries,
dynamic sidechain ducking, and ITU-R BS.1770 / -14 LUFS mastering.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class VoicePersona(BaseModel):
    persona_name: str = Field(..., description="Character or role name (e.g. 'Didi', 'Rajat', 'Narrator')")
    voice_identifier: str = Field(..., description="TTS voice identifier (e.g. 'hi-IN-SwaraNeural', 'hi-IN-MadhurNeural')")
    gender: str = Field("neutral", description="Gender tag: 'female', 'male', 'neutral'")
    speaking_rate: float = Field(1.0, ge=0.5, le=2.0, description="Speed multiplier (1.0 = normal)")
    pitch_adjustment_hz: int = Field(0, description="Pitch offset in Hz or semitones")
    provider: str = Field("edge-tts", description="Provider: 'edge-tts', 'google-cloud-tts', 'windows-sapi'")


class WordTiming(BaseModel):
    word: str = Field(..., description="Spoken word token")
    start_time_sec: float = Field(..., description="Word start offset on shot timeline")
    end_time_sec: float = Field(..., description="Word end offset on shot timeline")
    duration_sec: float = Field(..., description="Word duration")


class DialogueAudioTrack(BaseModel):
    shot_id: int = Field(..., description="Shot index")
    speaker: str = Field(..., description="Character name")
    dialogue_line: str = Field(..., description="Spoken dialogue text")
    audio_path: str = Field(..., description="Path to generated audio file (WAV/MP3)")
    sample_rate: int = Field(44100, description="Sampling rate in Hz")
    duration_sec: float = Field(..., description="Exact audio duration in seconds")
    audio_ducking_required: bool = Field(True, description="Whether BGM must duck down during this line")
    words: List[WordTiming] = Field(default_factory=list, description="Word-level phoneme/timestamp boundaries")


class AcousticMasterReport(BaseModel):
    project_title: str = Field(..., description="Video project title")
    master_audio_path: str = Field(..., description="Path to mastered composite soundtrack")
    total_duration_sec: float = Field(..., description="Total timeline audio duration")
    integrated_lufs: float = Field(..., description="Measured integrated loudness in LUFS (target: -14.0 LUFS)")
    true_peak_dbtp: float = Field(..., description="Measured true peak level in dBTP (target <= -1.0 dBTP)")
    speech_spans_count: int = Field(..., description="Number of active dialogue sections")
    measured_ducking_attenuation_db: float = Field(..., description="Measured BGM volume drop during speech in dB")
    passes_acoustic_gate: bool = Field(..., description="True if LUFS in [-15.5, -12.5], TruePeak <= -1.0, ducking >= 10dB")
    qa_notes: List[str] = Field(default_factory=list, description="Acoustic audit observations or remediation flags")
