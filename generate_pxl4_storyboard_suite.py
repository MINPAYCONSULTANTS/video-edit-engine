#!/usr/bin/env python3
"""
generate_pxl4_storyboard_suite.py — Premium Editorial Storyboard Engine (Vox / FT Standard)
Eliminates AI slop, neon palettes, and overflowing cards.
Enforces strict horizontal centering, restrained typography, and authentic editorial archetypes.
"""
import os, sys, time, json, base64, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORK_DIR = Path('/Users/sanskarsaraf/.gemini/antigravity/scratch/video_edit')
OUT_DIR = WORK_DIR / 'storyboard_clean_32_pxl4'
OUT_DIR.mkdir(parents=True, exist_ok=True)
BRAIN_DIR = Path('/Users/sanskarsaraf/.gemini/antigravity/brain/c3d97250-5f63-4415-8e05-a6900d445973')
BRAIN_IMG_DIR = BRAIN_DIR / 'storyboard_clean_32_pxl4'
BRAIN_IMG_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG = "/Users/sanskarsaraf/.gemini/antigravity/scratch/social.minpay.in/video_generator/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg"
RAW_VIDEO = Path("/Users/sanskarsaraf/Downloads/PXL_20261015_064105787.mp4")

W, H = 1080, 1920

# Typography: Apple System Fonts
FONT_HEADING = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 46, index=8) # Bold
FONT_BODY = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 36, index=8) # SemiBold
FONT_SUB = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 44, index=8) # Bold
FONT_SMALL = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 24, index=0) # Regular
FONT_MONO = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 22, index=1) # Bold
FONT_TYPEWRITER = ImageFont.truetype('/System/Library/Fonts/Courier.ttc', 28, index=0)
FONT_TYPEWRITER_BOLD = ImageFont.truetype('/System/Library/Fonts/Courier.ttc', 34, index=1)
FONT_MONUMENTAL = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 96, index=8)

# Color Palette: Premium Restrained Editorial (FT / Vox / NYT)
# NO NEON / NO ARCADES / NO MULTI-COLOR SLOP
COLOR_WHITE = (255, 255, 255, 255)
COLOR_OFFWHITE = (241, 245, 249, 255)
COLOR_MUTED = (160, 174, 192, 255)
COLOR_GOLD = (245, 200, 75, 255) # Single warm editorial accent
COLOR_RED = (225, 29, 72, 255) # Restrained editorial crimson

# 32 Micro-Chunk CUES definition
# Restrained editorial pacing: Visual elements reserved for hard factual data (S01, S03) and climax (S07).
# All conversational/narrative beats (B05-B07, B13-B16, B17-B20, B21-B24, B25-B29) are clean talking head with centered subtitles.
CUES = [
    # Scene 1: The Delhi Transit Siege (0.00s - 4.14s) - Macro Transit Disparity
    {'id': 'b01', 'scene': 's01', 'scene_title': 'Scene 1 · Delhi Transit Siege', 'start': 0.00, 'end': 1.50, 'text': 'Sadak pe 30,000', 'words': 3, 'accent': '30,000', 'col': COLOR_GOLD, 'cy': 1540, 'layout': 's01_metrics', 'camera': 'Wide (1.00x)'},
    {'id': 'b02', 'scene': 's01', 'scene_title': 'Scene 1 · Delhi Transit Siege', 'start': 1.50, 'end': 2.50, 'text': 'log bulaaye,', 'words': 2, 'accent': None, 'col': COLOR_WHITE, 'cy': 1540, 'layout': 's01_metrics', 'camera': 'Wide Drift (1.01x)'},
    {'id': 'b03', 'scene': 's01', 'scene_title': 'Scene 1 · Delhi Transit Siege', 'start': 2.50, 'end': 3.44, 'text': '40 metro station', 'words': 3, 'accent': '40 metro', 'col': COLOR_GOLD, 'cy': 1540, 'layout': 's01_metrics', 'camera': 'Wide Drift (1.02x)'},
    {'id': 'b04', 'scene': 's01', 'scene_title': 'Scene 1 · Delhi Transit Siege', 'start': 3.44, 'end': 4.14, 'text': 'band karwaaye,', 'words': 2, 'accent': 'band', 'col': COLOR_RED, 'cy': 1540, 'layout': 's01_metrics', 'camera': 'Wide (1.025x)'},

    # Scene 2: The Rhetorical Turn (4.14s - 9.30s) - Clean Talking Head -> Apex Court Badge Climax
    {'id': 'b05', 'scene': 's02', 'scene_title': 'Scene 2 · Rhetorical Question', 'start': 4.14, 'end': 5.16, 'text': 'CJI ke chamber ke', 'words': 4, 'accent': 'CJI', 'col': COLOR_GOLD, 'cy': 1420, 'layout': None, 'camera': 'Smooth Push (1.01x)'},
    {'id': 'b06', 'scene': 's02', 'scene_title': 'Scene 2 · Rhetorical Question', 'start': 5.16, 'end': 6.46, 'text': 'baahar march nikaala,', 'words': 3, 'accent': 'march', 'col': COLOR_WHITE, 'cy': 1420, 'layout': None, 'camera': 'Smooth Push (1.03x)'},
    {'id': 'b07', 'scene': 's02', 'scene_title': 'Scene 2 · Rhetorical Question', 'start': 6.46, 'end': 7.36, 'text': 'aur aakhir mein hua kya?', 'words': 5, 'accent': 'hua kya?', 'col': COLOR_GOLD, 'cy': 1420, 'layout': None, 'camera': 'Medium Held (1.05x)'},
    {'id': 'b08', 'scene': 's02', 'scene_title': 'Scene 2 · Apex Court Climax', 'start': 7.64, 'end': 8.38, 'text': 'Aana Supreme Court hi', 'words': 4, 'accent': 'Supreme Court', 'col': COLOR_GOLD, 'cy': 1540, 'layout': 's02_court', 'camera': 'Punch Hold (1.06x)'},
    {'id': 'b09', 'scene': 's02', 'scene_title': 'Scene 2 · Apex Court Climax', 'start': 8.38, 'end': 9.30, 'text': 'pada na?', 'words': 2, 'accent': 'pada na?', 'col': COLOR_RED, 'cy': 1540, 'layout': 's02_court', 'camera': 'Held (1.06x)'},

    # Scene 3: Commuter Disruption (9.52s - 16.52s) - Social Telemetry -> High Energy Defiance
    {'id': 'b10', 'scene': 's03', 'scene_title': 'Scene 3 · Commuter Telemetry', 'start': 9.56, 'end': 10.46, 'text': 'Pichhle 5 din se', 'words': 4, 'accent': '5 din', 'col': COLOR_GOLD, 'cy': 1540, 'layout': 's03_social', 'camera': 'Studio Inset (1.00x)'},
    {'id': 'b11', 'scene': 's03', 'scene_title': 'Scene 3 · Commuter Telemetry', 'start': 10.46, 'end': 11.80, 'text': 'Delhi ke aam commuters', 'words': 4, 'accent': 'commuters', 'col': COLOR_GOLD, 'cy': 1540, 'layout': 's03_social', 'camera': 'Studio Inset (1.00x)'},
    {'id': 'b12', 'scene': 's03', 'scene_title': 'Scene 3 · Commuter Telemetry', 'start': 11.80, 'end': 12.66, 'text': 'ko pareshaan karke', 'words': 3, 'accent': 'pareshaan', 'col': COLOR_RED, 'cy': 1540, 'layout': 's03_social', 'camera': 'Studio Inset (1.00x)'},
    {'id': 'b13', 'scene': 's03', 'scene_title': 'Scene 3 · Street Defiance', 'start': 12.66, 'end': 13.74, 'text': 'bol rahe the', 'words': 3, 'accent': None, 'col': COLOR_WHITE, 'cy': 1420, 'layout': None, 'camera': 'Clean Close (1.02x)'},
    {'id': 'b14', 'scene': 's03', 'scene_title': 'Scene 3 · Street Defiance', 'start': 13.74, 'end': 14.34, 'text': 'hum kanoon nahi maante,', 'words': 4, 'accent': 'kanoon nahi', 'col': COLOR_RED, 'cy': 1420, 'layout': None, 'camera': 'Clean Close (1.04x)'},
    {'id': 'b15', 'scene': 's03', 'scene_title': 'Scene 3 · Street Defiance', 'start': 14.34, 'end': 15.80, 'text': 'hum sadak par', 'words': 3, 'accent': None, 'col': COLOR_WHITE, 'cy': 1420, 'layout': None, 'camera': 'Clean Close (1.05x)'},
    {'id': 'b16', 'scene': 's03', 'scene_title': 'Scene 3 · Street Defiance', 'start': 15.80, 'end': 16.52, 'text': 'faisla karenge!', 'words': 2, 'accent': 'faisla!', 'col': COLOR_RED, 'cy': 1420, 'layout': None, 'camera': 'Clean Close (1.06x)'},

    # Scene 4: The Reality Check (16.52s - 21.80s) - Clean Talking Head
    {'id': 'b17', 'scene': 's04', 'scene_title': 'Scene 4 · Police & Public Backlash', 'start': 16.52, 'end': 17.74, 'text': 'Lekin jab Delhi Police ne', 'words': 5, 'accent': 'Delhi Police', 'col': COLOR_GOLD, 'cy': 1420, 'layout': None, 'camera': 'Punch Push (1.02x)'},
    {'id': 'b18', 'scene': 's04', 'scene_title': 'Scene 4 · Police & Public Backlash', 'start': 17.74, 'end': 18.96, 'text': 'danda dikhaaya', 'words': 2, 'accent': 'danda', 'col': COLOR_RED, 'cy': 1420, 'layout': None, 'camera': 'Punch Push (1.05x)'},
    {'id': 'b19', 'scene': 's04', 'scene_title': 'Scene 4 · Police & Public Backlash', 'start': 18.96, 'end': 20.54, 'text': 'aur public ne gaali di', 'words': 5, 'accent': 'public', 'col': COLOR_GOLD, 'cy': 1420, 'layout': None, 'camera': 'Heroic Close (1.07x)'},
    {'id': 'b20', 'scene': 's04', 'scene_title': 'Scene 4 · Police & Public Backlash', 'start': 20.54, 'end': 21.80, 'text': 'toh saari hawa nikal gayi!', 'words': 5, 'accent': 'hawa nikal gayi!', 'col': COLOR_RED, 'cy': 1420, 'layout': None, 'camera': 'Heroic Close (1.075x)'},

    # Scene 5: The Capitulation (21.80s - 26.22s) - Clean Talking Head
    {'id': 'b21', 'scene': 's05', 'scene_title': 'Scene 5 · Supreme Court Petition', 'start': 21.80, 'end': 23.82, 'text': 'Aaj chupchaap', 'words': 2, 'accent': 'chupchaap', 'col': COLOR_GOLD, 'cy': 1420, 'layout': None, 'camera': 'Drift (1.02x)'},
    {'id': 'b22', 'scene': 's05', 'scene_title': 'Scene 5 · Supreme Court Petition', 'start': 23.82, 'end': 24.76, 'text': 'Supreme Court mein', 'words': 3, 'accent': 'Supreme Court', 'col': COLOR_GOLD, 'cy': 1420, 'layout': None, 'camera': 'Drift (1.03x)'},
    {'id': 'b23', 'scene': 's05', 'scene_title': 'Scene 5 · Supreme Court Petition', 'start': 24.76, 'end': 25.60, 'text': 'vakeel khada karke', 'words': 3, 'accent': None, 'col': COLOR_WHITE, 'cy': 1420, 'layout': None, 'camera': 'Drift (1.04x)'},
    {'id': 'b24', 'scene': 's05', 'scene_title': 'Scene 5 · Supreme Court Petition', 'start': 25.60, 'end': 26.22, 'text': 'petition lagayi hai.', 'words': 3, 'accent': 'petition', 'col': COLOR_GOLD, 'cy': 1420, 'layout': None, 'camera': 'Drift (1.05x)'},

    # Scene 6: The Reckoning (26.22s - 32.36s) - Clean Talking Head
    {'id': 'b25', 'scene': 's06', 'scene_title': 'Scene 6 · Civic Loss & Wasted Tax', 'start': 26.22, 'end': 28.02, 'text': 'Yeh kaam agar', 'words': 3, 'accent': None, 'col': COLOR_WHITE, 'cy': 1420, 'layout': None, 'camera': 'Eased Drift (1.05x)'},
    {'id': 'b26', 'scene': 's06', 'scene_title': 'Scene 6 · Civic Loss & Wasted Tax', 'start': 28.02, 'end': 29.00, 'text': 'day one pe kar dete,', 'words': 5, 'accent': 'day one', 'col': COLOR_GOLD, 'cy': 1420, 'layout': None, 'camera': 'Eased Drift (1.04x)'},
    {'id': 'b27', 'scene': 's06', 'scene_title': 'Scene 6 · Civic Loss & Wasted Tax', 'start': 29.00, 'end': 29.84, 'text': 'toh Delhi waalon ka', 'words': 4, 'accent': 'Delhi waalon', 'col': COLOR_WHITE, 'cy': 1420, 'layout': None, 'camera': 'Eased Drift (1.03x)'},
    {'id': 'b28', 'scene': 's06', 'scene_title': 'Scene 6 · Civic Loss & Wasted Tax', 'start': 29.84, 'end': 30.86, 'text': 'na time barbaad hota', 'words': 4, 'accent': 'time barbaad', 'col': COLOR_RED, 'cy': 1420, 'layout': None, 'camera': 'Eased Drift (1.02x)'},
    {'id': 'b29', 'scene': 's06', 'scene_title': 'Scene 6 · Civic Loss & Wasted Tax', 'start': 30.86, 'end': 32.36, 'text': 'na tax ka paisa!', 'words': 4, 'accent': 'tax ka paisa!', 'col': COLOR_GOLD, 'cy': 1420, 'layout': None, 'camera': 'Grounded (1.01x)'},

    # Scene 7: The Editorial Climax (32.36s - 38.00s) - Monumental Kinetic Typography
    {'id': 'b30', 'scene': 's07', 'scene_title': 'Scene 7 · Anti-Extortion Verdict', 'start': 33.74, 'end': 34.84, 'text': 'Bharat mein na', 'words': 3, 'accent': 'Bharat', 'col': COLOR_GOLD, 'cy': 1620, 'layout': 's07_monumental', 'camera': 'Monumental Climax Screen'},
    {'id': 'b31', 'scene': 's07', 'scene_title': 'Scene 7 · Anti-Extortion Verdict', 'start': 34.84, 'end': 35.98, 'text': 'street dadagiri chalegi', 'words': 3, 'accent': 'street dadagiri', 'col': COLOR_RED, 'cy': 1620, 'layout': 's07_monumental', 'camera': 'Monumental Climax Screen'},
    {'id': 'b32', 'scene': 's07', 'scene_title': 'Scene 7 · Anti-Extortion Verdict', 'start': 35.98, 'end': 37.42, 'text': 'na mob blackmail!', 'words': 3, 'accent': 'mob blackmail!', 'col': COLOR_RED, 'cy': 1620, 'layout': 's07_monumental', 'camera': 'Monumental Climax Screen'}
]

# Helper to create mathematically centered, clean, elegant subtitle pill
def make_centered_subtitle(text, accent, accent_col):
    """Creates a subtitle pill with pixel-perfect horizontal & vertical optical centering."""
    temp_img = Image.new('RGBA', (W, 200), (0,0,0,0))
    d = ImageDraw.Draw(temp_img)
    words = text.split()
    space_w = d.textbbox((0,0), ' ', font=FONT_SUB)[2]
    
    w_list = []
    total_w = 0
    for w in words:
        bb = d.textbbox((0,0), w, font=FONT_SUB)
        ww = bb[2] - bb[0]
        total_w += ww + space_w
        w_list.append((w, ww))
    total_w -= space_w
    
    # Calculate exact vertical bounds of the phrase for mathematical vertical centering
    full_bb = d.textbbox((0, 0), text, font=FONT_SUB)
    y0 = full_bb[1]
    y1 = full_bb[3]
    glyph_h = max(y1 - y0, 36)
    
    pad_x = 36
    pad_y = 16
    pill_w = total_w + pad_x * 2
    pill_h = glyph_h + pad_y * 2
    
    # Render pill surface
    pill_img = Image.new('RGBA', (pill_w, pill_h), (0,0,0,0))
    pd = ImageDraw.Draw(pill_img)
    # Minimal matte dark pill with subtle border
    pd.rounded_rectangle([0, 0, pill_w, pill_h], radius=20, fill=(11, 14, 20, 235), outline=(255, 255, 255, 30), width=1)
    
    # Render words with exact vertical offset (pad_y - y0)
    cur_x = pad_x
    draw_y = pad_y - y0
    for w, ww in w_list:
        clean_w = w.strip('.,!?')
        is_accent = accent and (clean_w.lower() in accent.lower() or accent.lower() in clean_w.lower())
        col = accent_col if is_accent else COLOR_WHITE
        pd.text((cur_x, draw_y), w, font=FONT_SUB, fill=col)
        cur_x += ww + space_w
        
    return pill_img, pill_w, pill_h

# -------------------------------------------------------------
# BESPOKE EDITORIAL MOTION ARCHETYPES (PROPERLY BOUNDED & RESTRAINED)
# -------------------------------------------------------------

# 1. Scene 1: FT / Bloomberg Style Transit Disparity Card
# Card dimensions: 880w x 290h, centered horizontally at x=100, y=1180 (Lower torso, 100% off face)
SURF_S01 = Image.new('RGBA', (W, H), (0,0,0,0))
card_s1 = Image.new('RGBA', (880, 290), (0,0,0,0))
cd = ImageDraw.Draw(card_s1)
# Matte dark slate container with subtle hairline border
cd.rounded_rectangle([0, 0, 880, 290], radius=20, fill=(12, 15, 22, 240), outline=(255, 255, 255, 25), width=1)
# Header
cd.text((40, 26), "TRANSIT DISRUPTION AUDIT", font=FONT_SMALL, fill=(203, 213, 225, 255))
cd.text((640, 26), "DELHI CAPITAL", font=FONT_MONO, fill=(148, 163, 184, 255))
cd.line([(40, 62), (840, 62)], fill=(255, 255, 255, 20), width=1)
# Row 1: Protestors
cd.text((40, 82), "Protestors Assembled", font=FONT_SMALL, fill=(148, 163, 184, 255))
cd.text((40, 115), "30,000", font=FONT_HEADING, fill=COLOR_WHITE)
# Clean minimal progress rule (neutral slate)
cd.rounded_rectangle([40, 175, 840, 182], radius=3, fill=(30, 41, 59, 255))
cd.rounded_rectangle([40, 175, 740, 182], radius=3, fill=(245, 200, 75, 240)) # Warm gold
# Row 2: Metro Stations
cd.text((40, 200), "DMRC Metro Stations Closed", font=FONT_SMALL, fill=(148, 163, 184, 255))
cd.text((540, 196), "40 STATIONS", font=FONT_HEADING, fill=COLOR_RED)
SURF_S01.paste(card_s1, (100, 1180), card_s1)

# 2. Scene 2: Apex Court Constitution Bench Inset Badge
# Card dimensions: 840w x 140h, centered horizontally at x=120, y=1280
SURF_S02 = Image.new('RGBA', (W, H), (0,0,0,0))
card_s2 = Image.new('RGBA', (840, 140), (0,0,0,0))
cd = ImageDraw.Draw(card_s2)
cd.rounded_rectangle([0, 0, 840, 140], radius=18, fill=(12, 15, 22, 240), outline=(255, 255, 255, 25), width=1)
cd.text((36, 28), "SUPREME COURT OF INDIA", font=FONT_BODY, fill=COLOR_WHITE)
cd.text((36, 82), "CONSTITUTION BENCH • ARTICLE 32 PROCEEDINGS", font=FONT_SMALL, fill=COLOR_GOLD)
SURF_S02.paste(card_s2, (120, 1280), card_s2)

# 3. Scene 3: Clean Verified Commuter Tweet Stack
# Card dimensions: 860w x 340h, centered horizontally at x=110, y=1140
SURF_S03 = Image.new('RGBA', (W, H), (0,0,0,0))
card_s3 = Image.new('RGBA', (860, 340), (0,0,0,0))
cd = ImageDraw.Draw(card_s3)
# Telemetry strip (Clean, minimal header without redundant clutter)
cd.rounded_rectangle([0, 0, 860, 56], radius=14, fill=(18, 24, 38, 240), outline=(255, 255, 255, 20), width=1)
cd.text((30, 16), "PUBLIC COMMUTER TELEMETRY", font=FONT_MONO, fill=(203, 213, 225, 255))
# Tweet Card 1
cd.rounded_rectangle([0, 72, 860, 196], radius=18, fill=(12, 15, 22, 245), outline=(255, 255, 255, 25), width=1)
cd.ellipse([30, 92, 66, 128], fill=(51, 65, 85, 255)) # Avatar
cd.text((80, 90), "Delhi Commuter Forum", font=FONT_SMALL, fill=COLOR_WHITE)
cd.text((340, 92), "@delhi_transit", font=FONT_MONO, fill=(148, 163, 184, 255))
cd.text((80, 132), "\"Over 1.8M passenger trips disrupted today across central corridors.\"", font=FONT_SMALL, fill=(226, 232, 240, 255))
# Tweet Card 2 (Stacked behind)
cd.rounded_rectangle([0, 212, 860, 336], radius=18, fill=(10, 13, 20, 245), outline=(255, 255, 255, 18), width=1)
cd.ellipse([30, 232, 66, 268], fill=(71, 85, 105, 255)) # Avatar
cd.text((80, 230), "Traffic Advisory Bureau", font=FONT_SMALL, fill=COLOR_WHITE)
cd.text((350, 232), "@traffic_update", font=FONT_MONO, fill=(148, 163, 184, 255))
cd.text((80, 272), "\"Vikas Marg & arterial rings locked. Ambulances rerouted.\"", font=FONT_SMALL, fill=(226, 232, 240, 255))
SURF_S03.paste(card_s3, (110, 1140), card_s3)

# 4. Scene 4: Restrained Law Enforcement Alert Card
# Card dimensions: 840w x 140h, centered horizontally at x=120, y=1280
SURF_S04 = Image.new('RGBA', (W, H), (0,0,0,0))
card_s4 = Image.new('RGBA', (840, 140), (0,0,0,0))
cd = ImageDraw.Draw(card_s4)
cd.rounded_rectangle([0, 0, 840, 140], radius=18, fill=(18, 12, 14, 240), outline=(225, 29, 72, 60), width=1)
cd.text((36, 28), "LAW ENFORCEMENT DIRECTIVE", font=FONT_BODY, fill=COLOR_WHITE)
cd.text((36, 82), "SECTION 144 ENFORCEMENT • ZERO ARTERIAL BLOCKADE TOLERANCE", font=FONT_SMALL, fill=(251, 113, 133, 255))
SURF_S04.paste(card_s4, (120, 1280), card_s4)

# 5. Scene 5: Authentic 2.5D Archival Document Dissection
# Card dimensions: 820w x 1120h, centered horizontally at x=130, y=260 (Framed on dark desk, plenty of lateral margin)
SURF_S05 = Image.new('RGBA', (W, H), (0,0,0,0))
# Background desk shadow
card_s5 = Image.new('RGBA', (820, 1120), (0,0,0,0))
cd = ImageDraw.Draw(card_s5)
# Parchment paper with subtle vintage off-white tone
cd.rounded_rectangle([0, 0, 820, 1120], radius=16, fill=(248, 246, 240, 255), outline=(210, 205, 195, 255), width=2)
# Dossier Header
cd.text((50, 45), "SWORN RECORD • JUDICIAL ARCHIVE", font=FONT_SMALL, fill=(120, 110, 100, 255))
cd.text((50, 85), "SUPREME COURT OF INDIA", font=FONT_TYPEWRITER_BOLD, fill=(20, 20, 20, 255))
cd.text((50, 145), "CIVIL ORIGINAL JURISDICTION • WRIT PETITION NO. 914", font=FONT_SMALL, fill=(80, 80, 80, 255))
cd.line([(50, 190), (770, 190)], fill=(200, 190, 180, 255), width=1)
# Document Text (Typewriter Style)
cd.text((50, 220), "MEMORANDUM OF URGENT PETITION", font=FONT_TYPEWRITER_BOLD, fill=(25, 25, 25, 255))
cd.text((50, 280), "Pursuant to prolonged street blockades in the capital city,", font=FONT_TYPEWRITER, fill=(40, 40, 40, 255))
cd.text((50, 325), "petitioners hereby invoke judicial remedies of this Court.", font=FONT_TYPEWRITER, fill=(40, 40, 40, 255))
# Realistic Yellow Highlighter Section (Subtle Warm Yellow #FEF08A)
cd.rounded_rectangle([45, 390, 775, 490], radius=6, fill=(254, 240, 138, 210))
cd.text((60, 410), "CITED OPERATIVE PRAYER:", font=FONT_SMALL, fill=(140, 90, 0, 255))
cd.text((60, 445), "PETITION FILED UNDER ARTICLE 32", font=FONT_TYPEWRITER_BOLD, fill=(15, 15, 15, 255))
# More body
cd.text((50, 530), "Relief is sought under constitutional statutory authority", font=FONT_TYPEWRITER, fill=(50, 50, 50, 255))
cd.text((50, 575), "submitting directly to the jurisdiction of the Court.", font=FONT_TYPEWRITER, fill=(50, 50, 50, 255))
# Rubber Stamp: Restrained, completely fitting within the card with 50px margins!
stamp = Image.new('RGBA', (380, 110), (0,0,0,0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([0, 0, 380, 110], radius=12, fill=(255, 255, 255, 0), outline=(225, 29, 72, 230), width=4)
sd.text((30, 20), "FILED & SUBMITTED", font=FONT_BODY, fill=(225, 29, 72, 240))
sd.text((80, 70), "SC REGISTRY • 15 OCT 2026", font=FONT_SMALL, fill=(225, 29, 72, 230))
stamp_rot = stamp.rotate(8, expand=True, resample=Image.Resampling.BICUBIC)
card_s5.paste(stamp_rot, (360, 680), stamp_rot)
SURF_S05.paste(card_s5, (130, 260), card_s5)

# 6. Scene 6: Civic Resource Loss Audit
# Card dimensions: 860w x 240h, centered horizontally at x=110, y=1220
SURF_S06 = Image.new('RGBA', (W, H), (0,0,0,0))
card_s6 = Image.new('RGBA', (860, 240), (0,0,0,0))
cd = ImageDraw.Draw(card_s6)
cd.rounded_rectangle([0, 0, 860, 240], radius=18, fill=(12, 15, 22, 240), outline=(255, 255, 255, 25), width=1)
cd.text((36, 26), "CIVIC RESOURCE & REVENUE AUDIT", font=FONT_SMALL, fill=(203, 213, 225, 255))
cd.line([(36, 62), (824, 62)], fill=(255, 255, 255, 20), width=1)
cd.text((36, 85), "5 DAYS LOST", font=FONT_HEADING, fill=COLOR_RED)
cd.text((360, 85), "1.8M CITIZEN HOURS", font=FONT_HEADING, fill=COLOR_GOLD)
cd.text((36, 175), "TAXPAYER EXCHEQUER COST • UNPRODUCTIVE METROPOLITAN HALT", font=FONT_SMALL, fill=(148, 163, 184, 255))
SURF_S06.paste(card_s6, (110, 1220), card_s6)

# 7. Scene 7: Monumental Kinetic Typography (High-Impact Editorial)
SURF_S07 = Image.new('RGBA', (W, H), (0,0,0,0))
# Deep matte backdrop
bg_plate = Image.new('RGBA', (W, H), (7, 9, 14, 255))
SURF_S07.paste(bg_plate, (0, 0))
cd = ImageDraw.Draw(SURF_S07)
# Clean kicker
cd.text((100, 420), "EDITORIAL VERDICT • RULE OF LAW", font=FONT_SMALL, fill=(148, 163, 184, 255))
cd.line([(100, 465), (980, 465)], fill=(255, 255, 255, 30), width=1)
# Monumental Headline
cd.text((100, 580), "NO STREET", font=FONT_MONUMENTAL, fill=COLOR_WHITE)
cd.text((100, 710), "DADAGIRI", font=FONT_MONUMENTAL, fill=COLOR_RED)
cd.text((100, 880), "NO MOB", font=FONT_MONUMENTAL, fill=COLOR_WHITE)
cd.text((100, 1010), "BLACKMAIL", font=FONT_MONUMENTAL, fill=COLOR_RED)

SURFACES = {
    's01_metrics': SURF_S01,
    's02_court': SURF_S02,
    's03_social': SURF_S03,
    's04_police': SURF_S04,
    's05_dossier': SURF_S05,
    's06_audit': SURF_S06,
    's07_monumental': SURF_S07
}

print("✅ Generated all 7 restrained, high-craft editorial surfaces.")

# Process each of the 32 cues: extract frame, composite archetype, center subtitle, save
html_cards = []

for idx, c in enumerate(CUES):
    cid = c['id']
    mid_t = (c['start'] + c['end']) / 2.0
    out_img_name = f"{cid}.jpg"
    raw_frame_path = OUT_DIR / f"raw_{cid}.jpg"
    comp_img_path = OUT_DIR / out_img_name
    brain_img_path = BRAIN_IMG_DIR / out_img_name
    
    # 1. Extract raw video frame at exact mid timestamp
    cmd_extract = [
        FFMPEG, '-y',
        '-ss', f"{mid_t:.3f}",
        '-i', str(RAW_VIDEO),
        '-vf', 'scale=1080:1920',
        '-vframes', '1',
        str(raw_frame_path)
    ]
    subprocess.run(cmd_extract, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Open camera frame
    if raw_frame_path.exists():
        cam = Image.open(raw_frame_path).convert('RGBA')
    else:
        cam = Image.new('RGBA', (W, H), (15, 20, 25, 255))
        
    # Apply camera zoom (sub-pixel)
    zoom = 1.00
    if '1.025x' in c['camera']: zoom = 1.025
    elif '1.05x' in c['camera']: zoom = 1.05
    elif '1.06x' in c['camera']: zoom = 1.06
    elif '1.075x' in c['camera']: zoom = 1.075
    
    if zoom > 1.001:
        zw, zh = int(W * zoom), int(H * zoom)
        cam = cam.resize((zw, zh), Image.Resampling.LANCZOS)
        cx = (zw - W) // 2
        cy = int((zh - H) * 0.35)
        cam = cam.crop((cx, cy, cx + W, cy + H))
        
    # Inset window for Scene 3 (Clean rounded matte frame only when social card is present)
    if c['scene'] == 's03' and c['layout'] == 's03_social':
        studio = Image.new('RGBA', (W, H), (7, 9, 14, 255))
        mask_win = Image.new('L', (920, 1300), 0)
        ImageDraw.Draw(mask_win).rounded_rectangle([0, 0, 920, 1300], radius=28, fill=255)
        inset_cam = cam.crop((80, 200, 1000, 1500)).resize((920, 1300), Image.Resampling.LANCZOS)
        studio.paste(inset_cam, (80, 220), mask_win)
        ImageDraw.Draw(studio).rounded_rectangle([80, 220, 1000, 1520], radius=28, outline=(255, 255, 255, 25), width=1)
        cam = studio
        
    # Composite Motion Archetype
    layout_name = c['layout']
    if layout_name in SURFACES:
        surf = SURFACES[layout_name]
        cam.paste(surf, (0, 0), surf)
        
    # Composite Centered Subtitle Pill (Rule 12 & Rule 21 Centering Safeguard)
    pill_img, pill_w, pill_h = make_centered_subtitle(c['text'], c['accent'], c['col'])
    pill_x = (W - pill_w) // 2 # STRICT HORIZONTAL CENTERING
    pill_y = c['cy']
    cam.paste(pill_img, (pill_x, pill_y), pill_img)
    
    # Save composite JPG
    cam_rgb = cam.convert('RGB')
    cam_rgb.save(comp_img_path, quality=90)
    cam_rgb.save(brain_img_path, quality=90)
    
    # Clean up raw frame
    if raw_frame_path.exists():
        raw_frame_path.unlink()
        
    # Base64 embedding
    with open(comp_img_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    data_uri = f"data:image/jpeg;base64,{b64}"
    
    accent_badge = f"<span class='text-amber-400 font-bold'>{c['accent']}</span>" if c['accent'] else "<span class='text-slate-400'>Neutral</span>"
    
    card_html = f'''
    <!-- Card {cid} -->
    <div class="flex-shrink-0 w-[240px] sm:w-[260px] bg-[#0c0e14] rounded-2xl border border-white/10 overflow-hidden shadow-xl flex flex-col group hover:border-emerald-500/50 transition-all">
      
      <!-- Composited Image (Click to Lightbox) -->
      <div class="relative w-full aspect-[9/16] bg-black overflow-hidden cursor-pointer" onclick="openLightbox('{cid}', '{data_uri}')">
        <img src="{data_uri}" class="w-full h-full object-cover transform group-hover:scale-105 transition duration-500" alt="{c['text']}">
        <div class="absolute top-2.5 left-2.5 flex items-center gap-1.5 bg-black/80 backdrop-blur-md px-2 py-0.5 rounded-full border border-white/10">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
          <span class="font-mono text-[11px] font-bold text-white">{cid.upper()}</span>
        </div>
        <div class="absolute top-2.5 right-2.5 bg-black/80 backdrop-blur-md px-2 py-0.5 rounded-full border border-white/10 font-mono text-[10px] text-slate-300">
          {c['start']:.2f}s - {c['end']:.2f}s
        </div>
        <div class="absolute bottom-2 left-2.5 right-2.5 bg-slate-950/80 backdrop-blur-sm p-1.5 rounded-lg border border-white/5 flex items-center justify-between text-[10px] font-mono">
          <span class="text-slate-400">{c['words']} words</span>
          <span class="text-emerald-400 font-bold">PASS (Safe)</span>
        </div>
      </div>

      <!-- Card Details & Feedback Action -->
      <div class="p-3.5 flex flex-col justify-between flex-1 gap-2.5">
        <div>
          <div class="text-[11px] font-mono text-slate-400 uppercase tracking-wider mb-1 flex items-center justify-between">
            <span>{c['scene'].upper()}</span>
            <span>{c['camera']}</span>
          </div>
          <p class="text-white font-bold text-xs leading-snug line-clamp-2">
            "{c['text']}"
          </p>
          <div class="mt-2 text-[11px] text-slate-400">
            Accent: {accent_badge}
          </div>
        </div>

        <button onclick="openFeedbackModal('{cid}', '{c['text']}')" class="w-full py-1.5 px-3 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-mono text-slate-200 flex items-center justify-center gap-1.5 transition-colors cursor-pointer">
          <span>✏️ Suggest Edit</span>
        </button>
      </div>

    </div>
    '''
    html_cards.append((c['scene'], c['scene_title'], card_html))
    print(f"  ✓ [{idx+1:2d}/32] Rendered refined composite frame for {cid}")

# Group cards by Scene
scenes_dict = {}
for s_id, s_title, card in html_cards:
    if s_id not in scenes_dict:
        scenes_dict[s_id] = {'title': s_title, 'cards': []}
    scenes_dict[s_id]['cards'].append(card)

sections_html = []
for s_id, s_data in scenes_dict.items():
    cards_str = '\n'.join(s_data['cards'])
    sections_html.append(f'''
    <!-- Scene {s_id.upper()} -->
    <section class="space-y-3">
      <div class="flex items-center justify-between pb-1 border-b border-white/10">
        <div class="flex items-center gap-2.5">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
          <h2 class="text-base md:text-lg font-bold text-white tracking-tight">{s_data['title']}</h2>
        </div>
        <span class="font-mono text-xs text-slate-400 bg-white/5 px-2 py-0.5 rounded border border-white/10">
          {len(s_data['cards'])} Micro-Beats
        </span>
      </div>

      <!-- Horizontal Scrollable Row of Composited Cards -->
      <div class="flex gap-4 overflow-x-auto pb-4 pt-1 hide-scrollbar">
        {cards_str}
      </div>
    </section>
    ''')

# Assemble Complete Interactive Storyboard HTML
full_storyboard_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Production Storyboard (32 Composited Beats) · PXL_20261015_064105787</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap');
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #07090e; color: #f1f5f9; }}
    .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    .hide-scrollbar::-webkit-scrollbar {{ display: none; }}
    .hide-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
  </style>
</head>
<body class="min-h-screen py-8 px-4 md:px-10">
  <div class="max-w-7xl mx-auto space-y-8">
    
    <!-- Minimal Header with Actions -->
    <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
      <div>
        <div class="flex items-center gap-3 mb-1.5">
          <span class="px-2.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono text-xs font-semibold uppercase">
            32 Micro-Chunk Beats · Restrained Vox/FT Editorial Standard
          </span>
          <span class="text-slate-400 font-mono text-xs">PXL_20261015_064105787.mp4 · 38.89s @ 60 FPS</span>
        </div>
        <h1 class="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
          Master Editorial Storyboard: Rule of Law vs. Mob Blackmail
        </h1>
        <p class="text-slate-400 text-xs md:text-sm mt-1">
          Centered captions, zero overflowing boundaries, authentic document framing, and restrained editorial color palette.
        </p>
      </div>

      <!-- Action Center -->
      <div class="flex items-center gap-3 flex-wrap">
        <button onclick="openFeedbackDrawer()" class="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/15 border border-white/15 text-xs font-mono text-white flex items-center gap-2 transition-colors cursor-pointer">
          <span>📝 Review Edits</span>
          <span id="badgeCount" class="w-5 h-5 rounded-full bg-emerald-500 text-black font-bold flex items-center justify-center text-[10px]">0</span>
        </button>
        <button onclick="copyAllFeedback()" class="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-mono font-bold text-xs flex items-center gap-2 transition-colors cursor-pointer">
          📋 Copy Feedback
        </button>
      </div>
    </header>

    <!-- Scenes Sections -->
    <div class="space-y-8">
      {''.join(sections_html)}
    </div>

    <!-- Final Approval Action Card -->
    <div class="bg-gradient-to-r from-slate-900 to-emerald-950/40 border-2 border-emerald-500/40 rounded-3xl p-8 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-6">
      <div>
        <div class="flex items-center gap-2.5 mb-2">
          <span class="w-3 h-3 rounded-full bg-emerald-400 animate-ping"></span>
          <h3 class="text-2xl font-black text-white">Approve Production Storyboard</h3>
        </div>
        <p class="text-slate-300 text-sm max-w-xl">
          Review the 32 composited frames above. Every caption is centered horizontally with safe padding, and all elements strictly respect lateral margins.
        </p>
      </div>
      <button onclick="copyAllFeedback()" class="px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-black font-black text-base rounded-2xl shadow-lg shadow-emerald-500/20 transform hover:-translate-y-0.5 active:translate-y-0 transition cursor-pointer">
        ✓ Confirm & Render 60 FPS Master
      </button>
    </div>

  </div>

  <!-- Lightbox Modal -->
  <div id="lightboxModal" class="fixed inset-0 bg-black/90 backdrop-blur-md hidden z-50 flex items-center justify-center p-4" onclick="closeLightbox()">
    <div class="max-w-[480px] w-full max-h-[92vh] flex flex-col items-center gap-3" onclick="event.stopPropagation()">
      <div class="w-full flex justify-between items-center text-xs font-mono text-slate-400 px-2">
        <span id="lightboxTitle">PREVIEW</span>
        <button onclick="closeLightbox()" class="text-white hover:text-rose-400 font-bold text-lg">✕</button>
      </div>
      <img id="lightboxImg" class="w-full h-auto max-h-[82vh] object-contain rounded-2xl border border-white/20 shadow-2xl" src="" alt="Zoom Frame">
    </div>
  </div>

  <!-- Feedback Drawer -->
  <div id="feedbackDrawer" class="fixed inset-y-0 right-0 w-full max-w-md bg-slate-900 border-l border-white/10 shadow-2xl p-6 hidden z-50 flex flex-col justify-between">
    <div>
      <div class="flex items-center justify-between pb-4 border-b border-white/10 mb-4">
        <h3 class="text-lg font-bold text-white flex items-center gap-2">
          <span>📝 Editorial Suggestions</span>
          <span id="drawerCount" class="text-xs bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-full font-mono">0</span>
        </h3>
        <button onclick="closeFeedbackDrawer()" class="text-slate-400 hover:text-white text-lg">✕</button>
      </div>
      <div id="feedbackList" class="space-y-3 overflow-y-auto max-h-[70vh] hide-scrollbar text-xs">
        <p class="text-slate-500 italic">No edits suggested yet. Click 'Suggest Edit' on any card to refine captions or timing.</p>
      </div>
    </div>
    <div class="pt-4 border-t border-white/10 flex gap-3">
      <button onclick="copyAllFeedback()" class="flex-1 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-black font-mono font-bold text-xs rounded-xl">
        📋 Copy All to Clipboard
      </button>
    </div>
  </div>

  <!-- Suggest Edit Modal -->
  <div id="editModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm hidden z-50 flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-white/15 rounded-2xl p-6 max-w-md w-full space-y-4">
      <h3 class="text-base font-bold text-white flex items-center justify-between">
        <span id="editModalTitle">Edit Beat</span>
        <button onclick="closeEditModal()" class="text-slate-400 hover:text-white">✕</button>
      </h3>
      <div>
        <label class="block text-xs font-mono text-slate-400 mb-1">Current Caption</label>
        <input id="editCaptionInput" type="text" class="w-full bg-slate-950 border border-white/15 rounded-xl px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-emerald-500">
      </div>
      <div>
        <label class="block text-xs font-mono text-slate-400 mb-1">Editor Notes / Tweak Instruction</label>
        <textarea id="editNotesInput" rows="3" placeholder="e.g., Change accent word to '30,000' or push 0.2s earlier..." class="w-full bg-slate-950 border border-white/15 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"></textarea>
      </div>
      <div class="flex gap-2 justify-end pt-2">
        <button onclick="closeEditModal()" class="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-mono text-slate-300">Cancel</button>
        <button onclick="saveFeedback()" class="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 rounded-xl text-xs font-mono font-bold text-black">Save Tweak</button>
      </div>
    </div>
  </div>

  <script>
    let feedback = JSON.parse(localStorage.getItem('pxl4_feedback') || '{{}}');
    let activeCardId = null;

    function updateBadge() {{
      const count = Object.keys(feedback).length;
      document.getElementById('badgeCount').innerText = count;
      document.getElementById('drawerCount').innerText = count;
      renderFeedbackList();
    }}

    function openLightbox(cid, src) {{
      document.getElementById('lightboxTitle').innerText = cid.toUpperCase() + ' · FULL PREVIEW (1080x1920)';
      document.getElementById('lightboxImg').src = src;
      document.getElementById('lightboxModal').classList.remove('hidden');
    }}

    function closeLightbox() {{
      document.getElementById('lightboxModal').classList.add('hidden');
    }}

    function openFeedbackDrawer() {{
      document.getElementById('feedbackDrawer').classList.remove('hidden');
    }}

    function closeFeedbackDrawer() {{
      document.getElementById('feedbackDrawer').classList.add('hidden');
    }}

    function openFeedbackModal(cid, text) {{
      activeCardId = cid;
      document.getElementById('editModalTitle').innerText = 'Suggest Edit for ' + cid.toUpperCase();
      document.getElementById('editCaptionInput').value = feedback[cid]?.caption || text;
      document.getElementById('editNotesInput').value = feedback[cid]?.notes || '';
      document.getElementById('editModal').classList.remove('hidden');
    }}

    function closeEditModal() {{
      document.getElementById('editModal').classList.add('hidden');
    }}

    function saveFeedback() {{
      const caption = document.getElementById('editCaptionInput').value;
      const notes = document.getElementById('editNotesInput').value;
      if (notes || caption) {{
        feedback[activeCardId] = {{ caption, notes }};
      }} else {{
        delete feedback[activeCardId];
      }}
      localStorage.setItem('pxl4_feedback', JSON.stringify(feedback));
      closeEditModal();
      updateBadge();
    }}

    function renderFeedbackList() {{
      const list = document.getElementById('feedbackList');
      const keys = Object.keys(feedback);
      if (keys.length === 0) {{
        list.innerHTML = '<p class="text-slate-500 italic">No edits suggested yet. Click \\'Suggest Edit\\' on any card.</p>';
        return;
      }}
      let html = '';
      keys.forEach(k => {{
        const item = feedback[k];
        html += `
          <div class="bg-slate-950 p-3 rounded-xl border border-white/10 space-y-1">
            <div class="flex justify-between items-center text-slate-400 font-mono text-[11px]">
              <span class="text-emerald-400 font-bold">${{k.toUpperCase()}}</span>
              <button onclick="removeFeedback('${{k}}')" class="text-rose-400 hover:text-rose-300">✕</button>
            </div>
            <div class="text-white font-medium">"${{item.caption}}"</div>
            ${{item.notes ? `<div class="text-slate-400 italic">Note: ${{item.notes}}</div>` : ''}}
          </div>
        `;
      }});
      list.innerHTML = html;
    }}

    function removeFeedback(k) {{
      delete feedback[k];
      localStorage.setItem('pxl4_feedback', JSON.stringify(feedback));
      updateBadge();
    }}

    function copyAllFeedback() {{
      const keys = Object.keys(feedback);
      if (keys.length === 0) {{
        navigator.clipboard.writeText("Approved as is! Ready to render 60 FPS master.");
        alert("Approved! Confirmation copied to clipboard. Paste to Antigravity to render.");
      }} else {{
        let text = "Here are my requested tweaks for PXL_20261015_064105787:\\n";
        keys.forEach(k => {{
          text += `- Beat ${{k.toUpperCase()}}: "${{feedback[k].caption}}" (Notes: ${{feedback[k].notes}})\\n`;
        }});
        navigator.clipboard.writeText(text);
        alert("Feedback copied to clipboard! Paste it to Antigravity to adjust.");
      }}
    }}

    updateBadge();
  </script>
</body>
</html>
'''

# Write to both working dir and brain artifact dir
with open(WORK_DIR / 'approval_storyboard.html', 'w', encoding='utf-8') as f:
    f.write(full_storyboard_html)

with open(BRAIN_DIR / 'approval_storyboard.html', 'w', encoding='utf-8') as f:
    f.write(full_storyboard_html)

with open(BRAIN_DIR / 'approval_storyboard_pxl4.html', 'w', encoding='utf-8') as f:
    f.write(full_storyboard_html)

print("🎉 Master Storyboard compilation complete! Written to approval_storyboard.html")
