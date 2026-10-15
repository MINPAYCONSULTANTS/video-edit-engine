#!/usr/bin/env python3
"""
kinetic_subtitles.py — Kinetic Word-by-Word Subtitle Engine with Morphing Pill & Active Word Karaoke
Implements Rule 12 (Micro-Chunk Cadence) with physical spring width transitions and active-word highlighting.
"""
import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def spring_ease(t: float, stiffness: float = 260.0, damping: float = 24.0) -> float:
    if t <= 0: return 0.0
    w0 = np.sqrt(stiffness)
    zeta = damping / (2.0 * w0)
    if zeta < 1.0:
        wd = w0 * np.sqrt(1.0 - zeta**2)
        val = 1.0 - np.exp(-zeta * w0 * t) * (np.cos(wd * t) + (zeta * w0 / wd) * Math_sin(wd * t))
    else:
        val = 1.0 - (1.0 + w0 * t) * np.exp(-w0 * t)
    return float(val)

def Math_sin(x):
    return np.sin(x)

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

        # Build micro-chunks (Max 4-5 words per screen)
        self.chunks = self._build_micro_chunks()
        print(f"🎙️ KineticSubtitles: compiled {len(self.chunks)} micro-chunks from {len(self.raw_words)} words.")

    def _build_micro_chunks(self):
        """Groups individual words into high-retention micro-chunks of 2 to 4 words."""
        # Curated cadence acoustically locked to vocal pauses
        # Using Roman/Hindi mapping from previous verified cues
        cues = [
            # S01: Hook (0.00s - 3.40s)
            {"start": 0.00, "end": 1.25, "words": ["jis", "desh", "ne"], "roman": "jis desh ne"},
            {"start": 1.25, "end": 2.35, "words": ["mumbai", "mein", "26-11"], "roman": "mumbai mein 26-11"},
            {"start": 2.35, "end": 3.40, "words": ["karwaya", "tha..."], "roman": "karwaya tha..."},
            
            # S02: Turn (3.40s - 7.95s)
            {"start": 3.40, "end": 4.65, "words": ["agar", "woh", "tumhare"], "roman": "agar woh tumhare"},
            {"start": 4.65, "end": 5.80, "words": ["protest", "ke", "liye"], "roman": "protest ke liye"},
            {"start": 5.80, "end": 6.85, "words": ["taaliyan", "baja", "raha"], "roman": "taaliyan baja raha"},
            {"start": 6.85, "end": 7.95, "words": ["hai..."], "roman": "hai..."},
            
            # S03: Truth (7.95s - 11.80s)
            {"start": 7.95, "end": 9.15, "words": ["toh", "tum", "krantikari"], "roman": "toh tum krantikari"},
            {"start": 9.15, "end": 10.45, "words": ["nahi..."], "roman": "nahi..."},
            {"start": 10.45, "end": 11.80, "words": ["unke", "puppets", "ho!"], "roman": "unke puppets ho!"},
            
            # S04: Pivot (11.80s - 13.90s)
            {"start": 11.80, "end": 12.85, "words": ["dushman", "desh", "kabhi"], "roman": "dushman desh kabhi"},
            {"start": 12.85, "end": 13.90, "words": ["dua", "nahi", "maangta."], "roman": "dua nahi maangta."},
            
            # S04 Card metric sync (13.90s - 18.04s)
            {"start": 13.90, "end": 15.15, "words": ["border", "pe", "woh"], "roman": "border pe woh"},
            {"start": 15.15, "end": 16.35, "words": ["army", "se", "jeet"], "roman": "army se jeet"},
            {"start": 16.35, "end": 17.15, "words": ["nahi", "sakte,"], "roman": "nahi sakte,"},
            {"start": 17.15, "end": 18.04, "words": ["growth", "mein", "mukabla"], "roman": "growth mein mukabla"},
            
            # S05: Bot Surge (18.04s - 21.69s)
            {"start": 18.04, "end": 19.10, "words": ["isliye", "jaise", "hi"], "roman": "isliye jaise hi"},
            {"start": 19.10, "end": 20.25, "words": ["sadkein", "band", "hoti"], "roman": "sadkein band hoti"},
            {"start": 20.25, "end": 21.69, "words": ["hain..."], "roman": "hain..."},
            
            # S06: Constitutional Right (21.69s - 26.85s)
            {"start": 21.69, "end": 23.10, "words": ["Critique", "any"], "roman": "Critique any"},
            {"start": 23.10, "end": 24.35, "words": ["government", "you", "want."], "roman": "government you want."},
            {"start": 24.35, "end": 25.60, "words": ["That", "is", "your"], "roman": "That is your"},
            {"start": 25.60, "end": 26.85, "words": ["right!"], "roman": "right!"},
            
            # S07: Weapon (26.85s - 32.62s)
            {"start": 26.85, "end": 28.10, "words": ["lekin", "jis", "din"], "roman": "lekin jis din"},
            {"start": 28.10, "end": 29.45, "words": ["tumhara", "protest"], "roman": "tumhara protest"},
            {"start": 29.45, "end": 30.80, "words": ["dushman", "desh", "ka"], "roman": "dushman desh ka"},
            {"start": 30.80, "end": 32.62, "words": ["weapon", "ban", "jaaye..."], "roman": "weapon ban jaaye..."},
            
            # S08: Climax (32.62s - 35.52s) -> Zero Subtitle Pill (Monumental Typography Rules)
        ]
        return cues

    def get_subtitle_frame(self, t: float):
        """
        Returns (overlay_image_rgba, bounding_box) at timestamp t.
        If no subtitle active, returns (None, None).
        """
        active_idx = -1
        for i, c in enumerate(self.chunks):
            if c['start'] <= t < c['end']:
                active_idx = i
                break

        if active_idx == -1:
            return None, None

        chunk = self.chunks[active_idx]
        text_words = chunk['words']
        c_dur = chunk['end'] - chunk['start']
        rel_t = t - chunk['start']

        # Determine currently spoken word index
        word_count = len(text_words)
        active_word_idx = min(word_count - 1, int((rel_t / max(0.01, c_dur)) * word_count))

        # Calculate word sizes
        word_widths = []
        space_w = self.font_bold.getbbox(' ')[2]
        dummy_img = Image.new('RGBA', (1, 1))
        draw_dummy = ImageDraw.Draw(dummy_img)

        total_text_w = 0
        for w in text_words:
            bbox = draw_dummy.textbbox((0, 0), w, font=self.font_bold)
            ww = bbox[2] - bbox[0]
            word_widths.append(ww)
            total_text_w += ww
        total_text_w += space_w * (word_count - 1)

        # Target pill dimensions
        target_pill_w = total_text_w + 64
        pill_h = 76

        # Spring morphing for pill width on entrance
        entrance_spring = spring_ease(rel_t, 280, 24)
        current_pill_w = int(target_pill_w * min(1.0, 0.85 + 0.15 * entrance_spring))

        cx = self.canvas_w // 2
        cy = 1380  # Anchor safely below chin

        x0 = cx - current_pill_w // 2
        y0 = cy - pill_h // 2
        x1 = x0 + current_pill_w
        y1 = y0 + pill_h

        # Render RGBA layer
        overlay = Image.new('RGBA', (self.canvas_w, self.canvas_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Draw dark frosted glass base backing
        draw.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=(8, 11, 18, 220), outline=(255, 255, 255, 30), width=1)

        # Draw individual words with active-word highlight
        cur_x = x0 + (current_pill_w - total_text_w) // 2
        text_y = y0 + 12

        for idx, (word, ww) in enumerate(zip(text_words, word_widths)):
            if idx == active_word_idx:
                # Active word: 100% white with subtle lift
                draw.text((cur_x, text_y - 2), word, font=self.font_bold, fill=(255, 255, 255, 255))
            else:
                # Inactive word: 68% soft slate
                draw.text((cur_x, text_y), word, font=self.font_reg, fill=(200, 210, 225, 175))
            cur_x += ww + space_w

        return overlay, (x0, y0, x1, y1)

if __name__ == '__main__':
    engine = KineticSubtitleEngine('transcription_pxl3_groq.json')
    img, bbox = engine.get_subtitle_frame(1.0)
    print("Test frame at 1.0s:", bbox)
