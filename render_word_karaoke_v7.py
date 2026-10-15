"""
render_word_karaoke_v7.py
─────────────────────────
Word-to-Word Dynamic Transcription Engine:
• Continuous Word-by-Word Active Tracking (Karaoke Pop Style):
  - 2 to 4 words visible on screen in clean lines (no clutter)
  - As each exact word is spoken, it lights up in GOLD / AMBER and pops in size (+15-20%)
  - Words not yet spoken or just finished stay in clean muted/white
• NO background cards / boxes: Direct on video with 3px black stroke contour + drop shadow
• Varied font sizes and hero word emphasis based on vocal energy
• Smooth 30fps rendering with per-word timing precision
"""

import os, sys, subprocess, time, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORK      = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit'
RAW       = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960.mp4'
FFMPEG    = '/Users/sanskarsaraf/.gemini/antigravity/scratch/social.minpay.in/video_generator/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg'
RAFALE    = f'{WORK}/ref_assets/rafale_jet.png'
OVERLAY   = f'{WORK}/overlay_v7.mov'
TEMP_OUT  = f'{WORK}/craft_v7_temp.mp4'
FINAL_OUT = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960_EDITED.mp4'

W, H = 1080, 1920
FPS  = 30

def Fh(sz): return ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=8) # Heavy
def Fd(sz): return ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=2) # Demi Bold

WHITE = (255, 255, 255, 255)
GOLD  = (255, 215, 45,  255)
AMBER = (255, 148, 22,  255)
MUTED = (195, 205, 215, 255)
INACT = (140, 150, 165, 220)

# Full aligned 96 words with exact start/end timestamps and Roman/Hinglish text
with open(f'{WORK}/full_aligned_words.json') as f:
    raw_words = json.load(f)

HINGLISH_WORDS = [
    "EVM", "HACK?", "HO", "GAYI!",
    "VOTE", "CHORI", "HO", "GAYA?",
    "SAB", "SUN", "LIYA...",
    "BAS", "EK", "SIMPLE", "SAWAAL!",
    "SUPREME", "COURT", "KYUN", "NAHI", "JA", "RAHE", "HO?",
    "SUPREME", "COURT", "KE", "PAAS", "POORI", "CONSTITUTIONAL", "POWER", "HAI", "KI",
    "ELECTION", "CANCEL", "KARWANE", "KI!",
    "BIHAR", "MEIN", "KARWAYA", "THA!",
    "ABHI", "PUNJAB", "MEIN", "50", "WARDS", "MEIN", "KARWAYA", "HAI.",
    "COURT", "ISLIYE", "NAHI", "JAATE", "KYUNKI",
    "WAHA", "PE", "AFFIDAVITS", "LAGTE", "HAIN!",
    "TWITTER", "THREADS", "NAHI!",
    "WAHA", "JHOOTH", "BOLA", "TOH", "RAFALE", "WALE", "CASE", "KI", "TARAH", "PHIR", "SE",
    "MAAFI", "MAANGNI", "PADEGI!",
    "ISLIYE", "SADAK", "PAR", "TAMASHA", "DE", "RAHE", "HO?",
    "AGAR", "PROOF", "HAI", "TOH", "JUDGE", "KE", "PAAS", "JAO", "NA!",
    "DELHI", "KO", "BLACK-", "MAIL", "KYUN", "KAR", "RAHE", "HO?"
]

ALIGNED_DATA = []
for i in range(len(raw_words)):
    rw = raw_words[i]
    hw = HINGLISH_WORDS[i] if i < len(HINGLISH_WORDS) else rw['word']
    ALIGNED_DATA.append({
        'word': hw,
        'start': rw['start'],
        'end': rw['end']
    })

# Define Phrased Sentences with Word Groups
# Each group has: id, start, end, lines of word indices, special effects (underline, badge, strike)
GROUPS = [
    {
        'id': 'g01', 'start': 0.0, 'end': 2.45, 'cy': 1345,
        'lines': [
            [(0, 68, True), (1, 68, True)],        # EVM HACK?
            [(2, 50, False), (3, 50, False)],      # HO GAYI!
        ]
    },
    {
        'id': 'g02', 'start': 2.45, 'end': 3.90, 'cy': 1340,
        'lines': [
            [(4, 56, True), (5, 56, True)],        # VOTE CHORI
            [(6, 52, False), (7, 52, False)],      # HO GAYA?
        ]
    },
    {
        'id': 'g03', 'start': 3.90, 'end': 4.90, 'cy': 1335,
        'lines': [
            [(8, 48, False), (9, 48, False), (10, 48, False)], # SAB SUN LIYA...
        ]
    },
    {
        'id': 'g04', 'start': 4.90, 'end': 6.35, 'cy': 1340,
        'lines': [
            [(11, 42, False), (12, 42, False)],    # BAS EK
            [(13, 64, True), (14, 64, True)],      # SIMPLE SAWAAL!
        ]
    },
    {
        'id': 'g05', 'start': 6.35, 'end': 7.75, 'cy': 1345,
        'lines': [
            [(15, 58, True), (16, 58, True)],      # SUPREME COURT
            [(17, 44, False), (18, 44, False), (19, 44, False), (20, 44, False), (21, 44, False)], # KYUN NAHI JA RAHE HO?
        ]
    },
    {
        'id': 'g06', 'start': 7.75, 'end': 10.45, 'cy': 1340,
        'lines': [
            [(22, 44, False), (23, 44, False), (24, 40, False), (25, 40, False), (26, 42, False)], # SUPREME COURT KE PAAS POORI
            [(27, 56, True), (28, 56, True), (29, 44, False), (30, 40, False)], # CONSTITUTIONAL POWER HAI KI
        ]
    },
    {
        'id': 'g07', 'start': 10.45, 'end': 12.40, 'cy': 1345,
        'lines': [
            [(31, 52, False), (32, 52, False)],    # ELECTION CANCEL
            [(33, 62, True), (34, 62, True)],      # KARWANE KI!
        ]
    },
    {
        'id': 'g08', 'start': 12.40, 'end': 13.50, 'cy': 1335,
        'lines': [
            [(35, 48, True), (36, 44, False), (37, 52, False), (38, 52, False)], # BIHAR MEIN KARWAYA THA!
        ]
    },
    {
        'id': 'g09', 'start': 13.50, 'end': 15.80, 'cy': 1335,
        'lines': [
            [(39, 44, False), (40, 52, True), (41, 44, False)], # ABHI PUNJAB MEIN
            [(42, 60, True), (43, 60, True), (44, 42, False), (45, 50, False), (46, 44, False)], # 50 WARDS MEIN KARWAYA HAI.
        ]
    },
    {
        'id': 'g10', 'start': 15.80, 'end': 18.00, 'cy': 1340,
        'lines': [
            [(46, 48, False), (47, 48, False), (48, 48, False), (49, 48, False), (50, 48, False)], # COURT ISLIYE NAHI JAATE KYUNKI
        ]
    },
    {
        'id': 'g11', 'start': 18.00, 'end': 19.95, 'cy': 1345,
        'lines': [
            [(51, 44, False), (52, 44, False)],    # WAHA PE
            [(53, 62, True), (54, 52, False), (55, 52, False)], # AFFIDAVITS LAGTE HAIN!
        ]
    },
    {
        'id': 'g12', 'start': 19.95, 'end': 21.80, 'cy': 1345,
        'strike': True,
        'lines': [
            [(56, 52, False), (57, 52, False), (58, 52, False)], # TWITTER THREADS NAHI!
        ]
    },
    {
        'id': 'g13', 'start': 21.80, 'end': 25.40, 'cy': 1420,
        'top_badge': True,
        'lines': [
            [(59, 40, False), (60, 44, True), (61, 42, False), (62, 40, False)], # WAHA JHOOTH BOLA TOH
            [(63, 56, True), (64, 44, False), (65, 46, False), (66, 40, False), (67, 40, False), (68, 40, False), (69, 40, False)], # RAFALE WALE CASE...
            [(70, 56, True), (71, 52, False), (72, 52, False)], # MAAFI MAANGNI PADEGI!
        ]
    },
    {
        'id': 'g14', 'start': 25.40, 'end': 28.50, 'cy': 1350,
        'lines': [
            [(73, 44, False), (74, 48, True), (75, 44, False), (76, 52, True)], # ISLIYE SADAK PAR TAMASHA
            [(77, 44, False), (78, 44, False), (78, 80, True)], # DE RAHE HO? / KYUN?
        ]
    },
    {
        'id': 'g15', 'start': 28.50, 'end': 31.95, 'cy': 1345,
        'lines': [
            [(79, 40, False), (80, 48, True), (81, 40, False), (82, 40, False)], # AGAR PROOF HAI TOH
            [(83, 60, False), (84, 46, False), (85, 46, False), (86, 60, True), (87, 50, False)], # JUDGE KE PAAS JAO NA!
        ]
    },
    {
        'id': 'g16', 'start': 31.95, 'end': 35.50, 'cy': 1360,
        'lines': [
            [(88, 52, False), (89, 44, False), (90, 52, True), (91, 52, True)], # DELHI KO BLACK-MAIL
            [(92, 48, False), (93, 44, False), (94, 44, False), (95, 82, True)], # KYUN KAR RAHE HO?
        ]
    }
]

# Helper to draw single styled word
def draw_word(draw, surf, x, y, text, font, is_active, is_hero, is_spoken):
    if is_active:
        col = AMBER if is_hero else GOLD
        stroke_w = 4
        scale_boost = 1.12
    elif is_spoken:
        col = WHITE
        stroke_w = 3
        scale_boost = 1.0
    else:
        col = INACT
        stroke_w = 2
        scale_boost = 1.0

    # Bounding box
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_w)
    bw, bh = b[2]-b[0], b[3]-b[1]

    # Draw shadow
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    sh_d = ImageDraw.Draw(sh)
    sh_d.text((x, y + 4), text, font=font, fill=(0,0,0,210), stroke_width=stroke_w, stroke_fill=(0,0,0,210))
    surf.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6 if is_active else 4)))

    # Draw text
    draw.text((x, y), text, font=font, fill=col, stroke_width=stroke_w, stroke_fill=(0,0,0,255))
    return bw, bh

rafale_img = Image.open(RAFALE).convert('RGBA') if os.path.exists(RAFALE) else None

def render_frame_for_time(t):
    surf = Image.new('RGBA', (W, H), (0,0,0,0))
    d = ImageDraw.Draw(surf)

    # Find active group
    grp = None
    for g in GROUPS:
        if g['start'] <= t < g['end']:
            grp = g
            break
    if grp is None:
        return np.array(surf, dtype=np.uint8)

    cy = grp.get('cy', 1340)
    lines_spec = grp.get('lines', [])

    # Measure all lines
    measured_lines = []
    for l in lines_spec:
        line_words = []
        line_w = 0
        line_h = 0
        for wid, base_sz, is_hero in l:
            wdata = ALIGNED_DATA[wid]
            txt = wdata['word']
            is_active = (wdata['start'] <= t <= wdata['end'])
            is_spoken = (t >= wdata['end'])

            cur_sz = int(base_sz * (1.15 if is_active else 1.0))
            fnt = Fh(cur_sz) if (is_hero or is_active) else Fd(cur_sz)

            b = d.textbbox((0, 0), txt, font=fnt, stroke_width=3)
            ww, wh = b[2]-b[0], b[3]-b[1]
            line_words.append((wid, txt, fnt, ww, wh, is_active, is_hero, is_spoken))
            line_w += ww + 14
            line_h = max(line_h, wh)
        line_w -= 14
        measured_lines.append((line_words, line_w, line_h))

    ROW_GAP = 12
    badge_d = 110
    total_h = sum(mh for _, _, mh in measured_lines) + ROW_GAP * (len(measured_lines) - 1)
    if grp.get('top_badge') and rafale_img:
        total_h += badge_d + 16

    cur_y = cy - total_h // 2

    if grp.get('top_badge') and rafale_img:
        # Draw circular rafale badge
        mask = Image.new('L', (badge_d, badge_d), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, badge_d, badge_d], fill=255)
        ri = rafale_img.resize((badge_d, badge_d), Image.Resampling.LANCZOS)
        bx, by = W//2 - badge_d//2, cur_y
        surf.paste(ri, (bx, by), mask)
        d.ellipse([bx, by, bx+badge_d, by+badge_d], outline=(0,0,0,255), width=4)
        d.ellipse([bx, by, bx+badge_d, by+badge_d], outline=GOLD, width=2)
        cur_y += badge_d + 16

    for line_words, lw, lh in measured_lines:
        cur_x = W//2 - lw // 2
        for wid, txt, fnt, ww, wh, is_active, is_hero, is_spoken in line_words:
            wy = cur_y + (lh - wh) // 2
            draw_word(d, surf, cur_x, wy, txt, fnt, is_active, is_hero, is_spoken)
            cur_x += ww + 14

        if grp.get('strike'):
            # Draw red line through the strike group
            mid_y = cur_y + lh // 2
            d.line([W//2 - lw//2 - 6, mid_y, W//2 + lw//2 + 6, mid_y], fill=(235, 50, 50, 255), width=5)

        cur_y += lh + ROW_GAP

    return np.array(surf, dtype=np.uint8)

print("1. Initializing word-karaoke video rendering...")
TOTAL_FRAMES = int(36.52 * FPS)
EMPTY = b'\x00' * (W * H * 4)

cmd_ov = [
    FFMPEG, '-y',
    '-f', 'rawvideo', '-pix_fmt', 'rgba',
    '-s', f'{W}x{H}', '-r', str(FPS),
    '-i', '-', '-c:v', 'qtrle', OVERLAY
]
proc = subprocess.Popen(cmd_ov, stdin=subprocess.PIPE,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
t0 = time.time()

for f in range(TOTAL_FRAMES):
    t = f / FPS
    arr = render_frame_for_time(t)
    proc.stdin.write(arr.tobytes())

proc.stdin.close()
proc.wait()
print(f"✓ Word-by-word overlay rendered in {time.time()-t0:.1f}s")

print("2. Final Composite & Dialogue Normalization...")
fc = (
    "[0:v]eq=contrast=1.01:brightness=0.0:saturation=1.02[vb];"
    "[vb][1:v]overlay=0:0[vout]"
)
af = "highpass=f=80,lowpass=f=12000,loudnorm=I=-16:TP=-1.5:LRA=10"
cmd_r = [
    FFMPEG, '-y',
    '-i', RAW, '-i', OVERLAY,
    '-filter_complex', fc,
    '-map', '[vout]', '-map', '0:a',
    '-af', af,
    '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
    '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '192k',
    TEMP_OUT
]
t1 = time.time()
res = subprocess.run(cmd_r, capture_output=True, text=True)
if res.returncode != 0:
    print("FFmpeg error:\n", res.stderr[-2000:])
    sys.exit(1)

if os.path.exists(FINAL_OUT):
    os.remove(FINAL_OUT)
os.rename(TEMP_OUT, FINAL_OUT)

mb = os.path.getsize(FINAL_OUT) / 1024 / 1024
print(f"\n✓ True Word-to-Word Transcription Video Complete: {mb:.1f} MB in {time.time()-t1:.1f}s")
print(f"   {FINAL_OUT}")
