#!/usr/bin/env python3
"""
kinetic_subtitles.py — Acoustic-Locked Kinetic Subtitle Engine
Sample-accurate word-level synchrony derived directly from Whisper timestamps.
Implements Rule 12 (Micro-Chunk Cadence <= 4-5 words) and Rule 13 (Zero Redundancy).
"""
import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def spring_ease(t: float, stiffness: float = 260.0, damping: float = 24.0) -> float:
    if t <= 0: return 0.0
    w0 = np.sqrt(stiffness)
    zeta = damping / (2.0 * w0)
    if zeta < 1.0:
        wd = w0 * np.sqrt(1.0 - zeta**2)
        val = 1.0 - np.exp(-zeta * w0 * t) * (np.cos(wd * t) + (zeta * w0 / wd) * np.sin(wd * t))
    else:
        val = 1.0 - (1.0 + w0 * t) * np.exp(-w0 * t)
    return float(val)

class KineticSubtitleEngine:
    def __init__(self, transcription_path: str, canvas_w: int = 1080, canvas_h: int = 1920):
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.font_reg = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 48, index=8)
        self.font_bold = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 50, index=8)
        
        # Load transcript words
        with open(transcription_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.raw_words = data.get('words', [])

        # Build acoustically aligned micro-chunks (Max 4 words per screen)
        self.chunks = self._build_dynamic_chunks()
        print(f"🎙️ KineticSubtitles: compiled {len(self.chunks)} acoustic-locked micro-chunks from {len(self.raw_words)} words.")

    def _build_dynamic_chunks(self):
        """Constructs micro-chunks dynamically aligned with exact Whisper timestamps."""
        # Clean Roman vocabulary for PXL3 video (101 words matching raw transcript)
        roman_words = [
            'jis', 'desh', 'ne', 'mumbai', 'mein', '26-11', 'karwaya', 'tha,',
            'agar', 'woh', 'tumhare', 'protest', 'ke', 'liye', 'taaliyan', 'baja', 'raha', 'hai,',
            'toh', 'tum', 'krantikari', 'nahi,', 'unke', 'puppets', 'ho.',
            'dushman', 'desh', 'kabhi', 'tumhari', 'democracy', 'ke', 'liye', 'dua', 'nahi', 'maangta.',
            'border', 'pe', 'woh', 'humari', 'army', 'se', 'jeet', 'nahi', 'sakte,',
            'economic', 'growth', 'mein', 'woh', 'hamare', 'mukabla', 'kar', 'nahi', 'sakte.',
            'isliye', 'jaise', 'hi', 'dilli', 'mein', 'sadkein', 'band', 'hoti', 'hai,',
            'unke', 'bot', 'farms', 'tumhare', 'hashtag', 'trend', 'karwane', 'lagte', 'hain.',
            'Critique', 'any', 'government', 'you', 'want.',
            'That', 'is', 'your', 'right.',
            'lekin', 'jis', 'din', 'tumhara', 'protest', 'dushman', 'desh', 'ka', 'weapon', 'ban', 'jaaye,',
            'uss', 'din', 'tum', 'deshbhakt', 'nahi,', 'national', 'liability', 'ban', 'jaate', 'ho!'
        ]

        aligned = []
        if len(self.raw_words) == len(roman_words):
            for rw, w in zip(roman_words, self.raw_words):
                aligned.append({'word': rw, 'start': w['start'], 'end': w['end']})
        else:
            # Fallback to direct transcript words
            for w in self.raw_words:
                aligned.append({'word': w.get('word', ''), 'start': w.get('start', 0), 'end': w.get('end', 0)})

        chunks = []
        curr = []
        for i, item in enumerate(aligned):
            curr.append(item)
            has_punct = item['word'].endswith((',', '.', '!', '...'))
            is_max = len(curr) >= 4
            is_last = (i == len(aligned) - 1)

            if (has_punct and len(curr) >= 2) or is_max or is_last:
                c_words = [x['word'] for x in curr]
                c_start = curr[0]['start']
                c_end = curr[-1]['end']
                chunks.append({
                    'start': c_start,
                    'end': c_end,
                    'words': c_words,
                    'word_objs': curr,
                    'phrase': ' '.join(c_words)
                })
                curr = []

        return chunks

    def get_subtitle_frame(self, t: float):
        """
        Returns (overlay_image_rgba, bounding_box) at timestamp t.
        Acoustically locked to spoken syllables.
        """
        active_chunk = None
        for c in self.chunks:
            if c['start'] <= t < c['end']:
                active_chunk = c
                break

        if active_chunk is None:
            return None, None

        text_words = active_chunk['words']
        word_objs = active_chunk['word_objs']
        rel_t = t - active_chunk['start']

        # Determine active spoken word by exact millisecond interval
        active_word_idx = -1
        for idx, w in enumerate(word_objs):
            if w['start'] <= t <= w['end']:
                active_word_idx = idx
                break
        if active_word_idx == -1:
            for idx, w in enumerate(word_objs):
                if t >= w['start']:
                    active_word_idx = idx

        # Compute typography bounding widths
        word_widths = []
        dummy_img = Image.new('RGBA', (1, 1))
        draw_dummy = ImageDraw.Draw(dummy_img)
        space_w = self.font_bold.getbbox(' ')[2]

        total_text_w = 0
        for w in text_words:
            bbox = draw_dummy.textbbox((0, 0), w, font=self.font_bold)
            ww = bbox[2] - bbox[0]
            word_widths.append(ww)
            total_text_w += ww
        total_text_w += space_w * (len(text_words) - 1)

        target_pill_w = total_text_w + 64
        pill_h = 76

        # Spring ease pill expansion
        entrance_spring = spring_ease(rel_t, 280, 24)
        current_pill_w = int(target_pill_w * min(1.0, 0.88 + 0.12 * entrance_spring))

        cx = self.canvas_w // 2
        cy = 1380  # Safe torso placement below beard

        x0 = cx - current_pill_w // 2
        y0 = cy - pill_h // 2
        x1 = x0 + current_pill_w
        y1 = y0 + pill_h

        overlay = Image.new('RGBA', (self.canvas_w, self.canvas_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Draw dark frosted glass base backing
        draw.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=(8, 11, 18, 225), outline=(255, 255, 255, 30), width=1)

        # Draw individual words with active word pop
        cur_x = x0 + (current_pill_w - total_text_w) // 2
        text_y = y0 + 12

        for idx, (word, ww) in enumerate(zip(text_words, word_widths)):
            if idx == active_word_idx:
                # Active word: pure crisp white with -2px karaoke lift
                draw.text((cur_x, text_y - 2), word, font=self.font_bold, fill=(255, 255, 255, 255))
            else:
                # Inactive word: soft slate
                draw.text((cur_x, text_y), word, font=self.font_reg, fill=(200, 210, 225, 175))
            cur_x += ww + space_w

        return overlay, (x0, y0, x1, y1)

if __name__ == '__main__':
    engine = KineticSubtitleEngine('transcription_pxl3_groq.json')
    img, bbox = engine.get_subtitle_frame(6.5)
    print("Test frame at 6.5s:", bbox)
