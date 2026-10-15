"""
render_v8_ai.py
───────────────
AI-Driven Video Editing Engine – Talking Head (9:16, 1080x1920)

What makes this different from v7:
  • 5 distinct visual caption styles – AI picks one per phrase based on content
  • True word-by-word active tracking (gold glow + scale pop on the live word)
  • Motion graphics: animated underlines, side-streak accents, scale-bounce entries
  • Adaptive font sizes/weights per phrase (hook=140px condensed, questions=90px, stats=120px)
  • Uppercase-ALL for hook/close, mixed-case for argument / editorial
  • Lower-third name card animated in at start
  • Callout stat box at "50 wards" moment
  • Full audio: highpass + compressor + loudnorm (-14 LUFS)

AI Style Assignments per phrase:
  HOOK      – One giant uppercase word at a time, 140px Condensed Heavy, gold pop
  QUESTION  – 2 words/line, 90px Bold, white + amber active, italic question mark
  ARGUMENT  – 3-4 words, 68px DemiBold, word-active tracking, left-aligned editorial
  STAT      – Big number centred, 160px Heavy, white over amber stroke; sub-label 56px
  SHOUT     – Full-phrase upper, 100px Heavy Condensed, red accent, slam entry
  CLOSER    – 2 lines, 88px Bold, soft gold fade, centred
"""

import os, sys, subprocess, time, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ── Paths ────────────────────────────────────────────────────────────────────
WORK      = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit'
RAW       = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960.mp4'
FFMPEG    = '/Users/sanskarsaraf/.gemini/antigravity/scratch/social.minpay.in/video_generator/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg'
WORDS_F   = f'{WORK}/skill/words.json'
OVERLAY   = f'{WORK}/overlay_v8.mov'
TEMP_OUT  = f'{WORK}/craft_v8_temp.mp4'
FINAL_OUT = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960_EDITED.mp4'

W, H   = 1080, 1920
FPS    = 30
DUR    = 35.5          # clip total seconds (words end ~34s, add tiny tail)

# ── Font helpers ─────────────────────────────────────────────────────────────
AV   = '/System/Library/Fonts/Avenir Next.ttc'
AVC  = '/System/Library/Fonts/Avenir Next Condensed.ttc'

def FHeavy(sz):       return ImageFont.truetype(AV,  sz, index=8)   # Avenir Next Heavy
def FBold(sz):        return ImageFont.truetype(AV,  sz, index=0)   # Avenir Next Bold
def FDemi(sz):        return ImageFont.truetype(AV,  sz, index=2)   # Avenir Next DemiBold
def FMedium(sz):      return ImageFont.truetype(AV,  sz, index=5)   # Avenir Next Medium
def FCondHeavy(sz):   return ImageFont.truetype(AVC, sz, index=8)   # Condensed Heavy
def FCondBold(sz):    return ImageFont.truetype(AVC, sz, index=0)   # Condensed Bold

# ── Colour palette ────────────────────────────────────────────────────────────
WHITE   = (255, 255, 255, 255)
GOLD    = (255, 215, 45,  255)
AMBER   = (255, 148, 22,  255)
RED_ACC = (230, 50,  60,  255)
MUTED   = (200, 208, 220, 255)
INACT   = (145, 155, 170, 210)
DARK    = (10,  10,  18,  255)
NAVY    = (18,  22,  46,  255)

# ── Load word timings ─────────────────────────────────────────────────────────
with open(WORDS_F, encoding='utf-8') as f:
    WORDS = json.load(f)

def word_at(t):
    """Return index of word being spoken at time t (or -1)."""
    for i, w in enumerate(WORDS):
        if w['start'] <= t <= w['end']:
            return i
    return -1

# ── Phrase definitions (AI-classified) ───────────────────────────────────────
# Each phrase:  id, style, start, end, cy (anchor Y), words (list of word indices)
# style: HOOK | QUESTION | ARGUMENT | STAT | SHOUT | CLOSER
PHRASES = [
    # ── g01: EVM HACK? HO GAYI! ──────────────────────────────────────────────
    {'id':'g01', 'style':'HOOK',     'start':0.0,   'end':2.52,  'cy':1300,
     'chunks': [
         {'words': [0,1],  'label': 'EVM HACK?',  'force_upper': True},
         {'words': [2,3],  'label': 'HO GAYI!',   'force_upper': True},
     ]},
    # ── g02: VOTE CHORI HO GAYA? ─────────────────────────────────────────────
    {'id':'g02', 'style':'HOOK',     'start':2.52,  'end':3.94,  'cy':1300,
     'chunks': [
         {'words': [4,5],  'label': 'VOTE CHORI', 'force_upper': True},
         {'words': [6,7],  'label': 'HO GAYA?',   'force_upper': True},
     ]},
    # ── g03: SAB SUN LIYA... ──────────────────────────────────────────────────
    {'id':'g03', 'style':'SHOUT',    'start':3.94,  'end':4.92,  'cy':1330,
     'chunks': [
         {'words': [8,9,10], 'label': 'SAB SUN LIYA...', 'force_upper': True},
     ]},
    # ── g04: BAS EK / SIMPLE SAWAAL! ─────────────────────────────────────────
    {'id':'g04', 'style':'QUESTION', 'start':4.92,  'end':6.38,  'cy':1340,
     'chunks': [
         {'words': [11,12], 'label': 'bas ek',      'force_upper': False},
         {'words': [13,14], 'label': 'simple sawaal!', 'force_upper': False},
     ]},
    # ── g05: SUPREME COURT KYUN NAHI JA RAHE HO? ─────────────────────────────
    {'id':'g05', 'style':'QUESTION', 'start':6.38,  'end':7.78,  'cy':1340,
     'chunks': [
         {'words': [15,16],        'label': 'Supreme Court', 'force_upper': False},
         {'words': [17,18,19,20,21],'label': 'kyun nahi ja rahe ho?', 'force_upper': False},
     ]},
    # ── g06: SUPREME COURT KE PAAS POORI CONSTITUTIONAL POWER HAI KI ─────────
    {'id':'g06', 'style':'ARGUMENT', 'start':7.78,  'end':10.62, 'cy':1330,
     'chunks': [
         {'words': [22,23,24,25,26],    'label': 'Supreme Court ke paas poori', 'force_upper': False},
         {'words': [27,28,29,30],       'label': 'constitutional power hai ki', 'force_upper': False},
     ]},
    # ── g07: ELECTION CANCEL KARWANE KI! ─────────────────────────────────────
    {'id':'g07', 'style':'SHOUT',    'start':10.62, 'end':12.44, 'cy':1320,
     'chunks': [
         {'words': [31,32,33,34], 'label': 'ELECTION CANCEL KARWANE KI!', 'force_upper': True},
     ]},
    # ── g08: BIHAR MEIN KARWAYA THA ──────────────────────────────────────────
    {'id':'g08', 'style':'ARGUMENT', 'start':12.44, 'end':13.94, 'cy':1335,
     'chunks': [
         {'words': [35,36,37,38], 'label': 'Bihar mein karwaya tha,', 'force_upper': False},
     ]},
    # ── g09: ABHI PUNJAB MEIN / 50 WARDS ─────────────────────────────────────
    {'id':'g09', 'style':'STAT',     'start':13.94, 'end':16.2,  'cy':1200,
     'stat_number': '50', 'stat_label': 'WARDS', 'stat_sub': 'abhi Punjab mein',
     'stat_word_idx': 42,   # word index for "50"
     'chunks': [
         {'words': [39,40,41],        'label': 'abhi Punjab mein', 'force_upper': False},
         {'words': [42,43,44,45,46],  'label': '50 wards mein karwaya hai.', 'force_upper': False},
     ]},
    # ── g10: COURT ISLIYE NAHI JAATE KYUNKI ──────────────────────────────────
    {'id':'g10', 'style':'ARGUMENT', 'start':16.2,  'end':18.38, 'cy':1340,
     'chunks': [
         {'words': [47,48,49,50,51], 'label': 'Court isliye nahi jaate kyunki', 'force_upper': False},
     ]},
    # ── g11: WAHA PE AFFIDAVITS LAGTE HAIN ───────────────────────────────────
    {'id':'g11', 'style':'ARGUMENT', 'start':18.38, 'end':20.3,  'cy':1335,
     'chunks': [
         {'words': [52,53],      'label': 'waha pe', 'force_upper': False},
         {'words': [54,55,56],   'label': 'affidavits lagte hain.', 'force_upper': False},
     ]},
    # ── g12: TWITTER THREADS NAHI! (strikethrough) ───────────────────────────
    {'id':'g12', 'style':'SHOUT',    'start':20.3,  'end':22.12, 'cy':1330,
     'strike': True,
     'chunks': [
         {'words': [57,58,59], 'label': 'TWITTER THREADS NAHI!', 'force_upper': True},
     ]},
    # ── g13: WAHA JHOOTH BOLA TOH RAFALE WALE CASE... MAAFI MAANGNI PADEGI ───
    {'id':'g13', 'style':'ARGUMENT', 'start':22.12, 'end':26.58, 'cy':1330,
     'chunks': [
         {'words': [60,61,62,63],      'label': 'waha jhooth bola toh', 'force_upper': False},
         {'words': [64,65,66,67,68,69],'label': 'Rafale wale case ki tarah phir se', 'force_upper': False},
         {'words': [70,71,72,73],      'label': 'maafi maangni padegi.', 'force_upper': False},
     ]},
    # ── g14: ISLIYE SADAK PAR TAMASHA DE RAHE HO? ────────────────────────────
    {'id':'g14', 'style':'QUESTION', 'start':26.58, 'end':29.98, 'cy':1340,
     'chunks': [
         {'words': [73,74,75,76],  'label': 'isliye sadak par tamasha', 'force_upper': False},
         {'words': [77,78,79],     'label': 'de rahe ho?', 'force_upper': False},
     ]},
    # ── g15: AGAR PROOF HAI TOH JUDGE KE PAAS JAO NA! ───────────────────────
    # 81=agar, 82=proof, 83=hai, 84=toh, 85=judge, 86=ke, 87=paas, 88=jao, 89=na.
    {'id':'g15', 'style':'CLOSER',   'start':29.98, 'end':32.96, 'cy':1340,
     'chunks': [
         {'words': [81,82,83,84],    'label': 'agar proof hai toh', 'force_upper': False},
         {'words': [85,86,87,88,89], 'label': 'judge ke paas jao na.', 'force_upper': False},
     ]},
    # ── g16: DELHI KO BLACKMAIL KYUN KAR RAHE HO? ────────────────────────────
    # 90=Delhi, 91=ko, 92=blackmail, 93=kyun, 94=kar, 95=rahe
    {'id':'g16', 'style':'SHOUT',    'start':32.96, 'end':35.5,  'cy':1320,
     'chunks': [
         {'words': [90,91,92],  'label': 'DELHI KO BLACKMAIL', 'force_upper': True},
         {'words': [93,94,95],  'label': 'KYUN KAR RAHE HO?',  'force_upper': True},
     ]},
]

# Map word index → phrase + chunk for active-word tracking
word_to_phrase = {}
for ph in PHRASES:
    for ck in ph['chunks']:
        for wi in ck['words']:
            if wi < len(WORDS):
                word_to_phrase[wi] = ph['id']

# ── Utility drawing functions ─────────────────────────────────────────────────

def ease_in_out(x):
    """Smooth ease: 3x² − 2x³"""
    return x * x * (3 - 2 * x)

def shadow_text(surf, d, x, y, text, font, fill, stroke_w=3, blur=6, off=5):
    """Draw Gaussian-blurred shadow then main text."""
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((x + off, y + off), text, font=font,
                             fill=(0, 0, 0, 200),
                             stroke_width=stroke_w, stroke_fill=(0, 0, 0, 200))
    surf.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    d.text((x, y), text, font=font, fill=fill,
           stroke_width=stroke_w, stroke_fill=(0, 0, 0, 255))

def text_wh(d, text, font, sw=3):
    b = d.textbbox((0, 0), text, font=font, stroke_width=sw)
    return b[2] - b[0], b[3] - b[1]

def animated_underline(surf, cx, cy, w, progress, color=GOLD, thickness=5):
    """Grows an underline left→right as progress goes 0→1."""
    p = ease_in_out(min(progress, 1.0))
    x0 = cx - w // 2
    x1 = int(x0 + w * p)
    if x1 > x0:
        ImageDraw.Draw(surf).line([x0, cy, x1, cy], fill=color, width=thickness)

def side_streak(surf, y, length, progress, left=True, color=AMBER):
    """Horizontal streak sweeping in from left or right edge."""
    p = ease_in_out(min(progress, 1.0))
    if left:
        x0, x1 = 0, int(length * p)
    else:
        x0, x1 = W - int(length * p), W
    if x1 > x0:
        # gradient: thin lines at different y offsets
        for dy, alpha in [(-2, 80), (-1, 140), (0, 200), (1, 140), (2, 80)]:
            c = color[:3] + (alpha,)
            ImageDraw.Draw(surf).line([x0, y + dy, x1, y + dy], fill=c, width=1)

def draw_entry_scale(surf, overlay_surf, t_in_phrase, entry_dur=0.12):
    """Composite with a slight scale-in for the first entry_dur seconds."""
    # When phrase just entered, we scale the entire overlay up from 96% → 100%
    if t_in_phrase < entry_dur:
        progress = t_in_phrase / entry_dur
        scale = 0.96 + 0.04 * ease_in_out(progress)
        # Scale from centre
        new_w = int(W * scale)
        new_h = int(H * scale)
        scaled = overlay_surf.resize((new_w, new_h), Image.Resampling.LANCZOS)
        ox = (W - new_w) // 2
        oy = (H - new_h) // 2
        surf.alpha_composite(scaled, dest=(ox, oy))
    else:
        surf.alpha_composite(overlay_surf)

# ── Style renderers ────────────────────────────────────────────────────────────

def render_HOOK(surf, d, ph, t):
    """
    One giant uppercase word/pair at a time. 130px Condensed Heavy.
    Active word pops to GOLD + 1.15x scale. Others stay MUTED.
    Vertical stacking of chunks.
    """
    ROW_H = 160
    active_wi = word_at(t)
    t_in = t - ph['start']
    chunks = ph['chunks']
    total_h = len(chunks) * ROW_H
    cur_y = ph['cy'] - total_h // 2

    for ck in chunks:
        word_indices = ck['words']
        label = ck['label']
        force_upper = ck.get('force_upper', True)

        # Is any word in this chunk currently active?
        is_active_chunk = any(
            (wi < len(WORDS) and WORDS[wi]['start'] <= t <= WORDS[wi]['end'])
            for wi in word_indices
        )
        is_spoken_chunk = all(
            (wi < len(WORDS) and t > WORDS[wi]['end'])
            for wi in word_indices if wi < len(WORDS)
        )

        text = label.upper() if force_upper else label.upper()
        if is_active_chunk:
            font = FCondHeavy(135)
            fill = GOLD
            blur_r = 10
        elif is_spoken_chunk:
            font = FCondHeavy(120)
            fill = WHITE
            blur_r = 6
        else:
            font = FCondHeavy(110)
            fill = INACT
            blur_r = 4

        ww, wh = text_wh(d, text, font, sw=4)
        x = W // 2 - ww // 2
        y = cur_y
        shadow_text(surf, d, x, y, text, font, fill, stroke_w=4, blur=blur_r, off=6)

        if is_active_chunk:
            # Pulse animated underline
            ul_progress = (t - max(w['start'] for w_i, w in enumerate(WORDS)
                                   if w_i in word_indices and w_i < len(WORDS)
                                   and w['start'] <= t)) if active_wi in word_indices else 1.0
            animated_underline(surf, W // 2, y + wh + 10, ww, min(ul_progress * 6, 1.0))

        cur_y += ROW_H


def render_QUESTION(surf, d, ph, t):
    """
    2 lines, 90px Bold. Active word glows AMBER. Question structure emphasis.
    Horizontal underline on the question chunk.
    """
    ROW_H = 115
    GAP   = 14
    active_wi = word_at(t)
    chunks = ph['chunks']
    total_h = len(chunks) * ROW_H + GAP * (len(chunks) - 1)
    cur_y = ph['cy'] - total_h // 2

    for ci, ck in enumerate(chunks):
        word_indices = ck['words']
        # Build per-word rendering
        parts = []
        for wi in word_indices:
            if wi >= len(WORDS):
                continue
            w = WORDS[wi]
            is_active = (w['start'] <= t <= w['end'])
            is_spoken = (t > w['end'])
            text = w['word'].upper() if ck.get('force_upper') else w['word'].title()

            if is_active:
                font = FBold(95)
                fill = AMBER
                sw = 4
            elif is_spoken:
                font = FBold(86)
                fill = WHITE
                sw = 3
            else:
                font = FBold(82)
                fill = INACT
                sw = 2
            parts.append((text, font, fill, sw, is_active, wi))

        # Measure line width
        total_w = sum(text_wh(d, tx, fn, sw=sw)[0] + 18 for tx, fn, _, sw, _, _ in parts) - 18
        cur_x = W // 2 - total_w // 2

        line_h = 0
        for tx, fn, fill, sw, is_active, wi in parts:
            ww, wh = text_wh(d, tx, fn, sw=sw)
            line_h = max(line_h, wh)

        for tx, fn, fill, sw, is_active, wi in parts:
            ww, wh = text_wh(d, tx, fn, sw=sw)
            wy = cur_y + (line_h - wh) // 2
            shadow_text(surf, d, cur_x, wy, tx, fn, fill, stroke_w=sw, blur=(8 if is_active else 4))
            if is_active:
                # Word-level underline pop
                animated_underline(surf, cur_x + ww // 2, wy + wh + 6, ww, 1.0, color=AMBER, thickness=4)
            cur_x += ww + 18

        # Decorative streak on question line (last chunk)
        if ci == len(chunks) - 1:
            t_in = t - ph['start']
            side_streak(surf, cur_y + line_h // 2, 120, min(t_in * 5, 1.0), left=True, color=GOLD)

        cur_y += ROW_H + GAP


def render_ARGUMENT(surf, d, ph, t):
    """
    3-4 words per line, 64px DemiBold. Active word is WHITE+bold, inactive is MUTED.
    Left-offset for editorial feel. Subtle leading line on left.
    """
    ROW_H = 82
    GAP   = 10
    LPAD  = 80     # left-of-centre offset for editorial feel
    active_wi = word_at(t)
    chunks = ph['chunks']
    total_h = len(chunks) * ROW_H + GAP * (len(chunks) - 1)
    cur_y = ph['cy'] - total_h // 2

    # Left accent bar
    bar_h = total_h + 20
    bar_x = LPAD - 22
    ImageDraw.Draw(surf).rectangle([bar_x, cur_y - 10, bar_x + 5, cur_y - 10 + bar_h],
                                    fill=GOLD[:3] + (160,))

    for ck in chunks:
        word_indices = ck['words']
        parts = []
        for wi in word_indices:
            if wi >= len(WORDS):
                continue
            w = WORDS[wi]
            is_active = (w['start'] <= t <= w['end'])
            is_spoken = (t > w['end'])
            is_emph   = w.get('emph', False)
            text = w['word'].upper() if ck.get('force_upper') else w['word']

            if is_active:
                font = FBold(72)
                fill = GOLD if is_emph else WHITE
                sw   = 4
            elif is_emph and is_spoken:
                font = FBold(66)
                fill = AMBER
                sw   = 3
            elif is_spoken:
                font = FDemi(64)
                fill = WHITE
                sw   = 2
            else:
                font = FDemi(62)
                fill = INACT
                sw   = 2
            parts.append((text, font, fill, sw, is_active))

        # Left-align from LPAD
        total_w = sum(text_wh(d, tx, fn, sw=sw)[0] + 14 for tx, fn, _, sw, _ in parts) - 14
        cur_x = LPAD
        line_h = 0

        for tx, fn, fill, sw, is_active in parts:
            ww, wh = text_wh(d, tx, fn, sw=sw)
            line_h = max(line_h, wh)

        for tx, fn, fill, sw, is_active in parts:
            ww, wh = text_wh(d, tx, fn, sw=sw)
            wy = cur_y + (line_h - wh) // 2
            shadow_text(surf, d, cur_x, wy, tx, fn, fill, stroke_w=sw, blur=(7 if is_active else 3), off=4)
            cur_x += ww + 14

        cur_y += ROW_H + GAP


def render_STAT(surf, d, ph, t):
    """
    Large number centred (160px Heavy), sub-label below (56px DemiBold).
    Context label above (44px Medium muted).
    Animated amber ring around number as it 'counts in'.
    """
    t_in  = t - ph['start']
    dur   = ph['end'] - ph['start']
    prog  = min(t_in / max(dur * 0.4, 0.5), 1.0)   # animate in over first 40% of phrase

    # Context line above
    ctx = ph.get('stat_sub', '')
    ctx_font = FMedium(48)
    ctx_w, ctx_h = text_wh(d, ctx, ctx_font, sw=2)
    ctx_y = ph['cy'] - 200
    shadow_text(surf, d, W // 2 - ctx_w // 2, ctx_y, ctx, ctx_font, MUTED, stroke_w=2, blur=3, off=3)

    # Number
    num_text = ph.get('stat_number', '?')
    num_font = FCondHeavy(int(120 + 60 * ease_in_out(prog)))
    num_w, num_h = text_wh(d, num_text, num_font, sw=5)
    num_y = ph['cy'] - num_h // 2

    # Amber outline effect (draw slightly larger behind)
    num_font2 = FCondHeavy(int(120 + 60 * ease_in_out(prog)) + 6)
    nw2, nh2 = text_wh(d, num_text, num_font2, sw=6)
    d.text((W // 2 - nw2 // 2, num_y - 3), num_text, font=num_font2,
            fill=(0, 0, 0, 0), stroke_width=8, stroke_fill=AMBER[:3] + (180,))

    shadow_text(surf, d, W // 2 - num_w // 2, num_y, num_text, num_font,
                WHITE, stroke_w=5, blur=12, off=8)

    # Stat label
    lbl = ph.get('stat_label', '')
    lbl_font = FCondBold(72)
    lbl_w, lbl_h = text_wh(d, lbl, lbl_font, sw=3)
    lbl_y = num_y + num_h + 18
    shadow_text(surf, d, W // 2 - lbl_w // 2, lbl_y, lbl, lbl_font,
                GOLD, stroke_w=3, blur=6, off=4)

    # Animated horizontal bars flanking the number
    bar_prog = ease_in_out(min(t_in * 3, 1.0))
    bar_w = int(180 * bar_prog)
    bar_y = num_y + num_h // 2
    pad = num_w // 2 + 28
    centre_x = W // 2
    if bar_w > 0:
        for dy, alpha in [(-1, 100), (0, 200), (1, 100)]:
            c = AMBER[:3] + (alpha,)
            d.line([centre_x - pad - bar_w, bar_y + dy, centre_x - pad, bar_y + dy], fill=c, width=1)
            d.line([centre_x + pad, bar_y + dy, centre_x + pad + bar_w, bar_y + dy], fill=c, width=1)

    # Word-tracking for all words in this phrase (shown below stat label, smaller)
    # Skip chunk 0 (context) since it's already shown as stat_sub above
    word_y = lbl_y + lbl_h + 24
    active_wi = word_at(t)
    chunks_to_show = ph['chunks'][1:]   # skip first chunk (context repeated above)
    for ck in chunks_to_show:
        parts = []
        for wi in ck['words']:
            if wi >= len(WORDS):
                continue
            w = WORDS[wi]
            is_active = (w['start'] <= t <= w['end'])
            is_spoken = (t > w['end'])
            text = w['word'].upper() if ck.get('force_upper') else w['word']
            font = FDemi(54 if is_active else 46)
            fill = GOLD if is_active else (WHITE if is_spoken else INACT)
            parts.append((text, font, fill, is_active))

        if parts:
            total_w = sum(text_wh(d, tx, fn, sw=2)[0] + 12 for tx, fn, _, _ in parts) - 12
            cur_x = W // 2 - total_w // 2
            for tx, fn, fill, is_active in parts:
                ww, wh = text_wh(d, tx, fn, sw=2)
                shadow_text(surf, d, cur_x, word_y, tx, fn, fill, stroke_w=2, blur=4, off=3)
                cur_x += ww + 12
            word_y += 72


def render_SHOUT(surf, d, ph, t):
    """
    All caps, Condensed Heavy, centred. Auto-scales font to fit within safe width.
    Red accent on emphasis words. Optional strikethrough.
    Side streaks burst in at phrase start.
    """
    GAP      = 8
    SAFE_W   = W - 80          # 40px margin each side
    active_wi = word_at(t)
    t_in  = t - ph['start']
    chunks = ph['chunks']

    # Burst streaks on entry
    if t_in < 0.2:
        streak_prog = t_in / 0.2
        side_streak(surf, ph['cy'], 200, streak_prog, left=True,  color=RED_ACC)
        side_streak(surf, ph['cy'], 200, streak_prog, left=False, color=AMBER)

    # Pre-compute each chunk's target font size (auto-shrink to fit SAFE_W)
    chunk_parts_list = []
    for ck in chunks:
        word_indices = ck['words']
        base_sz = 108
        # Try progressively smaller until it fits
        for trial_sz in range(base_sz, 56, -4):
            parts_trial = []
            for wi in word_indices:
                if wi >= len(WORDS): continue
                w = WORDS[wi]
                is_active = (w['start'] <= t <= w['end'])
                is_spoken = (t > w['end'])
                is_emph   = w.get('emph', False)
                text = w['word'].upper()
                sz_active = min(trial_sz + 8, 120)
                if is_active:
                    fn   = FCondHeavy(sz_active)
                    fill = RED_ACC if is_emph else GOLD
                    sw   = 5
                elif is_emph and is_spoken:
                    fn   = FCondHeavy(trial_sz)
                    fill = AMBER; sw = 4
                elif is_spoken:
                    fn   = FCondHeavy(trial_sz - 6)
                    fill = WHITE; sw = 3
                else:
                    fn   = FCondHeavy(trial_sz - 10)
                    fill = INACT; sw = 2
                parts_trial.append((text, fn, fill, sw, is_active))
            total_w = sum(text_wh(d, tx, fn, sw=sw)[0] + 14 for tx, fn, _, sw, _ in parts_trial) - 14
            if total_w <= SAFE_W:
                chunk_parts_list.append((parts_trial, total_w))
                break
        else:
            chunk_parts_list.append((parts_trial, total_w))   # use smallest even if overflow

    # Measure total height
    row_hs = []
    for parts, _ in chunk_parts_list:
        lh = max((text_wh(d, tx, fn, sw=sw)[1] for tx, fn, _, sw, _ in parts), default=80)
        row_hs.append(lh)

    total_h = sum(row_hs) + GAP * (len(chunks) - 1)
    cur_y = ph['cy'] - total_h // 2

    for ci, (parts, total_w) in enumerate(chunk_parts_list):
        cur_x = W // 2 - total_w // 2
        lh = row_hs[ci]

        for tx, fn, fill, sw, is_active in parts:
            ww, wh = text_wh(d, tx, fn, sw=sw)
            wy = cur_y + (lh - wh) // 2
            shadow_text(surf, d, cur_x, wy, tx, fn, fill, stroke_w=sw,
                        blur=(10 if is_active else 5), off=6)
            cur_x += ww + 14

        # Strikethrough line
        if ph.get('strike'):
            mid_y = cur_y + lh // 2
            lx0 = W // 2 - total_w // 2 - 10
            lx1 = W // 2 + total_w // 2 + 10
            d.line([lx0, mid_y, lx1, mid_y], fill=RED_ACC, width=6)

        cur_y += lh + GAP


def render_CLOSER(surf, d, ph, t):
    """
    2 lines, 88px Bold. Warm gold fade-to-white as phrase ages.
    Centred with a thin gold separator between lines.
    """
    ROW_H = 108
    GAP   = 14
    active_wi = word_at(t)
    t_in  = t - ph['start']
    dur   = ph['end'] - ph['start']
    phrase_age = min(t_in / max(dur, 1), 1.0)

    chunks = ph['chunks']
    total_h = len(chunks) * ROW_H + GAP * (len(chunks) - 1)
    cur_y = ph['cy'] - total_h // 2

    for ci, ck in enumerate(chunks):
        word_indices = ck['words']
        parts = []
        for wi in word_indices:
            if wi >= len(WORDS):
                continue
            w = WORDS[wi]
            is_active = (w['start'] <= t <= w['end'])
            is_spoken = (t > w['end'])
            is_emph   = w.get('emph', False)
            text = w['word']

            if is_active:
                font = FBold(92)
                fill = GOLD
                sw   = 4
            elif is_emph and is_spoken:
                font = FBold(86)
                fill = AMBER
                sw   = 3
            elif is_spoken:
                font = FBold(84)
                fill = WHITE
                sw   = 3
            else:
                font = FDemi(80)
                fill = INACT
                sw   = 2
            parts.append((text, font, fill, sw, is_active))

        total_w = sum(text_wh(d, tx, fn, sw=sw)[0] + 14 for tx, fn, _, sw, _ in parts) - 14
        cur_x = W // 2 - total_w // 2
        line_h = 0

        for tx, fn, fill, sw, _ in parts:
            _, wh = text_wh(d, tx, fn, sw=sw)
            line_h = max(line_h, wh)

        for tx, fn, fill, sw, is_active in parts:
            ww, wh = text_wh(d, tx, fn, sw=sw)
            wy = cur_y + (line_h - wh) // 2
            shadow_text(surf, d, cur_x, wy, tx, fn, fill, stroke_w=sw,
                        blur=(8 if is_active else 4), off=5)
            cur_x += ww + 14

        # Thin separator between lines
        if ci < len(chunks) - 1:
            sep_y = cur_y + line_h + GAP // 2
            sep_x0 = W // 2 - 120
            sep_x1 = W // 2 + 120
            sep_alpha = int(100 + 100 * (1 - phrase_age))
            d.line([sep_x0, sep_y, sep_x1, sep_y], fill=GOLD[:3] + (sep_alpha,), width=2)

        cur_y += ROW_H + GAP

# ── Overlay elements ──────────────────────────────────────────────────────────

def render_lower_third(surf, d, t):
    """Name card slides in from left edge at t=0, stays for 3.8s."""
    DUR_IN  = 0.3
    DUR_OUT = 0.25
    HOLD_END = 3.8
    HOLD_START = DUR_IN

    if t > HOLD_END + DUR_OUT or t < 0:
        return

    if t < DUR_IN:
        prog = ease_in_out(t / DUR_IN)
    elif t > HOLD_END:
        prog = 1.0 - ease_in_out((t - HOLD_END) / DUR_OUT)
    else:
        prog = 1.0

    alpha = int(255 * prog)
    x_off = int((1 - prog) * -220)   # slides in from left

    LT_X = 78 + x_off
    LT_Y = 1480

    # Accent bar
    d.rectangle([LT_X, LT_Y, LT_X + 5, LT_Y + 80], fill=GOLD[:3] + (alpha,))

    name_font = FBold(46)
    role_font = FMedium(34)

    # Name
    name_text = 'Adv. Sanskar'
    nw, nh = text_wh(d, name_text, name_font, sw=2)
    d.text((LT_X + 18, LT_Y + 4), name_text, font=name_font,
            fill=WHITE[:3] + (alpha,), stroke_width=2, stroke_fill=(0, 0, 0, alpha))

    # Role
    role_text = 'Legal & Constitutional Analysis'
    d.text((LT_X + 18, LT_Y + nh + 12), role_text, font=role_font,
            fill=MUTED[:3] + (alpha,), stroke_width=1, stroke_fill=(0, 0, 0, int(alpha * 0.6)))


def render_callout(surf, d, t):
    """
    Supreme Court Constitutional power callout: appears at 7.78s to 10.62s.
    Upper-right corner, small badge.
    """
    START, END = 7.78, 10.62
    if not (START <= t <= END):
        return

    DUR_IN  = 0.3
    t_in    = t - START
    t_out   = END - t

    if t_in < DUR_IN:
        alpha = int(255 * ease_in_out(t_in / DUR_IN))
    elif t_out < DUR_IN:
        alpha = int(255 * ease_in_out(t_out / DUR_IN))
    else:
        alpha = 255

    CX, CY = 860, 430
    # Background pill
    pill_w, pill_h = 320, 100
    px0 = CX - pill_w // 2
    py0 = CY - pill_h // 2
    bg = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(bg).rounded_rectangle([px0, py0, px0 + pill_w, py0 + pill_h],
                                          radius=16, fill=(20, 20, 40, int(alpha * 0.85)))
    surf.alpha_composite(bg)

    # Gold top border line
    d.rectangle([px0, py0, px0 + pill_w, py0 + 3], fill=GOLD[:3] + (alpha,))

    top_f = FDemi(32)
    sub_f = FMedium(26)
    line1 = 'Art. 142'
    line2 = 'SC Constitutional Power'

    l1w, l1h = text_wh(d, line1, top_f, sw=1)
    l2w, l2h = text_wh(d, line2, sub_f, sw=1)

    d.text((CX - l1w // 2, py0 + 12), line1, font=top_f,
            fill=GOLD[:3] + (alpha,), stroke_width=1, stroke_fill=(0, 0, 0, alpha))
    d.text((CX - l2w // 2, py0 + 12 + l1h + 6), line2, font=sub_f,
            fill=WHITE[:3] + (int(alpha * 0.8),))


# ── Main frame renderer ───────────────────────────────────────────────────────

STYLE_RENDERERS = {
    'HOOK':     render_HOOK,
    'QUESTION': render_QUESTION,
    'ARGUMENT': render_ARGUMENT,
    'STAT':     render_STAT,
    'SHOUT':    render_SHOUT,
    'CLOSER':   render_CLOSER,
}

def render_frame(t):
    surf = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d    = ImageDraw.Draw(surf)

    # Find active phrase
    active_ph = None
    for ph in PHRASES:
        if ph['start'] <= t < ph['end']:
            active_ph = ph
            break

    if active_ph is not None:
        style = active_ph['style']
        t_in_phrase = t - active_ph['start']

        # Create phrase surface (for scale-entry animation)
        ph_surf = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ph_d    = ImageDraw.Draw(ph_surf)

        STYLE_RENDERERS[style](ph_surf, ph_d, active_ph, t)

        # Entry scale animation (first 120ms)
        ENTRY_DUR = 0.12
        if t_in_phrase < ENTRY_DUR and active_ph['style'] != 'STAT':
            prog  = ease_in_out(t_in_phrase / ENTRY_DUR)
            scale = 0.94 + 0.06 * prog
            new_w = int(W * scale)
            new_h = int(H * scale)
            scaled = ph_surf.resize((new_w, new_h), Image.Resampling.LANCZOS)
            ox = (W - new_w) // 2
            oy = (H - new_h) // 2
            surf.alpha_composite(scaled, dest=(ox, oy))
        else:
            surf.alpha_composite(ph_surf)

    # Always-on overlays
    render_lower_third(surf, d, t)
    render_callout(surf, d, t)

    return np.array(surf, dtype=np.uint8)


# ── Encoding pipeline ─────────────────────────────────────────────────────────

if __name__ == '__main__':
  TOTAL_FRAMES = int(DUR * FPS)

  print(f'render_v8_ai.py – AI-Driven Talking Head Engine')
  print(f'  Styles: HOOK | QUESTION | ARGUMENT | STAT | SHOUT | CLOSER')
  print(f'  Phrases: {len(PHRASES)}  |  Words tracked: {len(WORDS)}')
  print(f'  Total frames: {TOTAL_FRAMES} @ {FPS}fps = {DUR:.1f}s')
  print()
  print('1. Rendering overlay frames...')

  cmd_ov = [
      FFMPEG, '-y',
      '-f', 'rawvideo', '-pix_fmt', 'rgba',
      '-s', f'{W}x{H}', '-r', str(FPS),
      '-i', '-',
      '-c:v', 'qtrle', OVERLAY
  ]
  proc = subprocess.Popen(cmd_ov, stdin=subprocess.PIPE,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  t0 = time.time()

  for f in range(TOTAL_FRAMES):
      t = f / FPS
      frame = render_frame(t)
      proc.stdin.write(frame.tobytes())

      if f % 150 == 0:
          elapsed = time.time() - t0
          fps_est = f / max(elapsed, 0.01)
          rem = (TOTAL_FRAMES - f) / max(fps_est, 0.1)
          print(f'   frame {f}/{TOTAL_FRAMES}  ETA {rem:.0f}s', end='\r')

  proc.stdin.close()
  proc.wait()
  elapsed_ov = time.time() - t0
  print(f'\n✓ Overlay rendered: {elapsed_ov:.1f}s')

  print('2. Final composite + audio mastering...')
  fc = (
      '[0:v]eq=contrast=1.02:brightness=0.005:saturation=1.05,'
      'unsharp=5:5:0.3:5:5:0.0[vb];'
      '[vb][1:v]overlay=0:0[vout]'
  )
  af = 'highpass=f=80,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=9'
  cmd_r = [
      FFMPEG, '-y',
      '-i', RAW, '-i', OVERLAY,
      '-filter_complex', fc,
      '-map', '[vout]', '-map', '0:a',
      '-af', af,
      '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
      '-pix_fmt', 'yuv420p',
      '-c:a', 'aac', '-b:a', '192k',
      '-movflags', '+faststart',
      TEMP_OUT
  ]
  t1 = time.time()
  res = subprocess.run(cmd_r, capture_output=True, text=True)
  if res.returncode != 0:
      print('FFmpeg error:\n', res.stderr[-3000:])
      sys.exit(1)

  if os.path.exists(FINAL_OUT):
      os.remove(FINAL_OUT)
  os.rename(TEMP_OUT, FINAL_OUT)

  mb = os.path.getsize(FINAL_OUT) / 1024 / 1024
  print(f'\n✓ Done: {mb:.1f} MB in {time.time()-t1:.1f}s')
  print(f'  {FINAL_OUT}')
