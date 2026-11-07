"""
Autonomous AI Video Pipeline: Kinetic Subtitle Burner
Renders high-retention, anti-aliased typography with active word highlights,
stroke outlines, and rounded translucent pill backdrops for 9:16 vertical video.
"""

from typing import List, Optional, Tuple
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .schemas import SubtitleStyleConfig, SubtitleSegment, ActiveWordHighlight
from ..audio.schemas import DialogueAudioTrack
from ..scripting.schemas import ProductionShotDeck


class SubtitleBurner:
    """
    Renders word-synchronized animated subtitles onto video frames.
    """

    def __init__(self, style_config: Optional[SubtitleStyleConfig] = None):
        self.style = style_config or SubtitleStyleConfig()
        self.font = self._load_font(self.style.font_path, self.style.font_size)
        self.speaker_font = self._load_font(self.style.font_path, max(24, int(self.style.font_size * 0.55)))

    def _load_font(self, font_path: str, size: int) -> ImageFont.FreeTypeFont:
        """Loads TTF font or falls back gracefully to default PIL font."""
        p = Path(font_path)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
        
        # Try system fallbacks
        fallbacks = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        ]
        for fb in fallbacks:
            if Path(fb).exists():
                try:
                    return ImageFont.truetype(fb, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    @classmethod
    def segments_from_shot_deck_and_tracks(
        cls,
        shot_deck: ProductionShotDeck,
        dialogue_tracks: List[DialogueAudioTrack]
    ) -> List[SubtitleSegment]:
        """
        Builds synchronized SubtitleSegments matching shot deck timeline bounds.
        Clamps dialogue display to each shot's visual window to prevent cross-shot subtitle collisions.
        """
        segments = []
        track_map = {t.shot_id: t for t in dialogue_tracks}

        for shot in shot_deck.shots:
            if not shot.dialogue:
                continue

            track = track_map.get(shot.shot_id)
            shot_start = shot.start_time_sec
            shot_end = shot.end_time_sec
            full_text = shot.dialogue.line
            speaker = shot.dialogue.speaker

            words_highlight = []
            if track and track.words:
                for w in track.words:
                    # Clip word timings within the shot's active window
                    w_start = max(shot_start, min(shot_end, w.start_time_sec))
                    w_end = max(shot_start, min(shot_end, w.end_time_sec))
                    if w_end > w_start:
                        words_highlight.append(ActiveWordHighlight(
                            word=w.word,
                            start_time_sec=w_start,
                            end_time_sec=w_end
                        ))
            else:
                # Synthesize evenly distributed word timings
                words = full_text.split()
                if words:
                    dur_per_word = (shot_end - shot_start) / len(words)
                    for i, w in enumerate(words):
                        words_highlight.append(ActiveWordHighlight(
                            word=w,
                            start_time_sec=round(shot_start + i * dur_per_word, 3),
                            end_time_sec=round(shot_start + (i + 1) * dur_per_word, 3)
                        ))

            segments.append(SubtitleSegment(
                shot_id=shot.shot_id,
                speaker=speaker,
                full_text=full_text,
                start_time_sec=shot_start,
                end_time_sec=shot_end,
                words=words_highlight
            ))

        return segments

    def burn_frame(self, frame_bgr: np.ndarray, timestamp_sec: float, segments: List[SubtitleSegment]) -> np.ndarray:
        """
        Overlays kinetic subtitle onto a single video frame at the given timestamp.
        Returns the original frame untouched if no subtitle segment is active.
        """
        # Find active segment
        active_seg = next(
            (s for s in segments if s.start_time_sec <= timestamp_sec < s.end_time_sec),
            None
        )
        if not active_seg or not active_seg.words:
            return frame_bgr

        # Find which word is currently active
        words = active_seg.words
        active_idx = 0
        for i, w in enumerate(words):
            if w.start_time_sec <= timestamp_sec <= w.end_time_sec:
                active_idx = i
                break
            elif timestamp_sec > w.end_time_sec:
                active_idx = min(len(words) - 1, i + 1)

        # Group words into chunks of max_words_per_chunk (e.g. 4-5 words)
        chunk_size = max(3, self.style.max_words_per_chunk)
        chunk_idx = active_idx // chunk_size
        chunk_start = chunk_idx * chunk_size
        chunk_words = words[chunk_start:chunk_start + chunk_size]

        if not chunk_words:
            return frame_bgr

        # Render onto frame with RGBA blending
        h, w, _ = frame_bgr.shape
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # 1. Calculate layout dimensions
        speaker_tag = f"• {active_seg.speaker.upper()}"
        speaker_bbox = draw.textbbox((0, 0), speaker_tag, font=self.speaker_font)
        speaker_h = speaker_bbox[3] - speaker_bbox[1]

        # Calculate word widths and spaces
        space_w = draw.textbbox((0, 0), " ", font=self.font)[2]
        word_widths = []
        max_word_h = 0
        for w_item in chunk_words:
            bbox = draw.textbbox((0, 0), w_item.word, font=self.font)
            word_widths.append(bbox[2] - bbox[0])
            max_word_h = max(max_word_h, bbox[3] - bbox[1])

        total_text_w = sum(word_widths) + space_w * (len(chunk_words) - 1)
        
        # Center horizontally, position at lower-third
        center_x = w // 2
        start_x = center_x - (total_text_w // 2)
        base_y = int(h * self.style.position_y_ratio)

        # 2. Draw Translucent Backdrop Pill (if enabled)
        if self.style.bg_pill_color:
            pad_x = 36
            pad_y = 20
            pill_left = max(20, start_x - pad_x)
            pill_right = min(w - 20, start_x + total_text_w + pad_x)
            pill_top = base_y - speaker_h - 14 - pad_y
            pill_bottom = base_y + max_word_h + pad_y
            draw.rounded_rectangle(
                [pill_left, pill_top, pill_right, pill_bottom],
                radius=24,
                fill=self.style.bg_pill_color
            )

        # 3. Draw Speaker Tag
        draw.text(
            (start_x, base_y - speaker_h - 14),
            speaker_tag,
            font=self.speaker_font,
            fill=self.style.speaker_color,
            stroke_width=max(1, self.style.stroke_width - 2),
            stroke_fill=self.style.stroke_color
        )

        # 4. Draw Words with Kinetic Highlight
        curr_x = start_x
        for i, w_item in enumerate(chunk_words):
            global_word_idx = chunk_start + i
            is_active_word = (global_word_idx == active_idx)
            text_color = self.style.highlight_color if is_active_word else self.style.primary_color
            
            draw.text(
                (curr_x, base_y),
                w_item.word,
                font=self.font,
                fill=text_color,
                stroke_width=self.style.stroke_width,
                stroke_fill=self.style.stroke_color
            )
            curr_x += word_widths[i] + space_w

        # 5. Composite overlay with frame
        frame_rgba = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGBA))
        blended = Image.alpha_composite(frame_rgba, overlay)
        return cv2.cvtColor(np.array(blended), cv2.COLOR_RGBA2BGR)
