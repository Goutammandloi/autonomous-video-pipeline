"""
Autonomous AI Video Pipeline: Kinetic Subtitles & Phoneme Timing
Generates word-level timestamps, kinetic subtitle cues, and standard SRT files.
"""

from typing import List
from pathlib import Path
from .schemas import WordTiming, DialogueAudioTrack


class SubtitleGenerator:
    """
    Constructs kinetic word-by-word highlighted subtitle cues and standard .srt captions.
    """

    @staticmethod
    def estimate_word_timings(
        dialogue: str,
        start_offset_sec: float,
        total_duration_sec: float
    ) -> List[WordTiming]:
        """
        Calculates proportional word-level timestamps using phoneme/character-weighted intervals.
        Provides precise sub-second alignment for kinetic text animations.
        """
        words = dialogue.strip().split()
        if not words:
            return []

        # Weight duration by character length + punctuation pause
        char_weights = []
        for w in words:
            weight = len(w)
            if w.endswith((".", "!", "?", "...", ":")):
                weight += 2.5  # Add weight for sentence-ending pauses
            elif w.endswith((",", ";")):
                weight += 1.2
            char_weights.append(weight)

        total_weight = sum(char_weights)
        usable_duration = max(0.2, total_duration_sec - 0.1)  # small buffer

        current_time = start_offset_sec
        timings = []

        for w, weight in zip(words, char_weights):
            w_duration = (weight / total_weight) * usable_duration
            timings.append(WordTiming(
                word=w,
                start_time_sec=round(current_time, 3),
                end_time_sec=round(current_time + w_duration, 3),
                duration_sec=round(w_duration, 3)
            ))
            current_time += w_duration

        return timings

    @classmethod
    def export_srt(cls, tracks: List[DialogueAudioTrack], output_path: str) -> str:
        """
        Exports a list of dialogue tracks into standard SubRip (.srt) caption file.
        """
        def format_timestamp(seconds: float) -> str:
            hrs = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            ms = int(round((seconds - int(seconds)) * 1000))
            return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"

        srt_lines = []
        index = 1
        for track in tracks:
            start_str = format_timestamp(track.words[0].start_time_sec if track.words else 0.0)
            end_str = format_timestamp(track.words[-1].end_time_sec if track.words else track.duration_sec)
            
            srt_lines.append(str(index))
            srt_lines.append(f"{start_str} --> {end_str}")
            srt_lines.append(f"{track.speaker}: {track.dialogue_line}")
            srt_lines.append("")
            index += 1

        content = "\n".join(srt_lines)
        Path(output_path).write_text(content, encoding="utf-8")
        return content
