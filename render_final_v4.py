"""
render_final_v4.py
─────────────────
Every scene has a distinct typographic personality:
  - Size hierarchy varies (hero → compact)
  - Layouts vary (stacked / inline / hero-word / strike)
  - Font weight varies (Heavy vs Demi)
  - Color accent varies (gold / amber / muted+gold)
  - Occasional underline accent on key words
No category labels.
"""

import os, sys, subprocess, time, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORK   = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit'
RAW    = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960.mp4'
FFMPEG = '/Users/sanskarsaraf/.gemini/antigravity/scratch/social.minpay.in/video_generator/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg'
RAFALE = f'{WORK}/ref_assets/rafale_jet.png'
OVERLAY   = f'{WORK}/overlay_v4.mov'
TEMP_OUT  = f'{WORK}/craft_v4_temp.mp4'
FINAL_OUT = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960_EDITED.mp4'

# ── Fonts ───────────────────────────────────────────────────────────────────
def Fh(sz): return ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=8)
def Fd(sz): return ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=2)

# ── Palette ─────────────────────────────────────────────────────────────────
WHITE  = (255, 255, 255, 255)
GOLD   = (255, 210, 50,  255)
AMBER  = (255, 148, 22,  255)
MUTED  = (160, 175, 195, 255)
CARD   = (10,  14,  20,  225)
BORDER = (255, 210, 50,  110)

W, H = 1080, 1920

def _m(d, text, font):
    b = d.textbbox((0, 0), text, font=font)
    return b[2]-b[0], b[3]-b[1]

# ── Card renderer ────────────────────────────────────────────────────────────
def build_card(spec: dict) -> np.ndarray:
    """
    spec keys:
      'layout'  : 'inline' | 'stacked' | 'hero' | 'strike'
      'cy'      : int  — vertical center of card on full 1080×1920 canvas
      'lines'   : list of lists of (text, font, color)  — each inner list = one row
      'strike'  : (text, font, color) | None  — shown above lines with red line
      'underline': row index to underline | None
      'top_img' : PIL Image | None — circular badge above content
    """
    surf = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    td   = ImageDraw.Draw(surf)

    layout    = spec.get('layout', 'inline')
    cy        = spec.get('cy', 1340)
    lines     = spec.get('lines', [])     # list of rows; each row = list of (txt, font, col)
    strike    = spec.get('strike', None)
    ul_row    = spec.get('underline', None)
    top_img   = spec.get('top_img', None)
    img_d     = 130
    PAD_X, PAD_Y = 44, 20
    ROW_GAP   = 10

    # ── measure every row ──────────────────────────────────────────────────
    row_data = []   # list of {'segs': [(txt,fnt,col,w,h)], 'total_w', 'max_h'}
    for row in lines:
        segs = []
        for txt, fnt, col in row:
            w, h = _m(td, txt, fnt)
            segs.append((txt, fnt, col, w, h))
        total_w = sum(s[3] for s in segs) + 14 * (len(segs)-1)
        max_h   = max(s[4] for s in segs)
        row_data.append({'segs': segs, 'total_w': total_w, 'max_h': max_h})

    st_w = st_h = 0
    if strike:
        st_w, st_h = _m(td, strike[0], strike[1])

    # ── card dimensions ────────────────────────────────────────────────────
    max_row_w = max((r['total_w'] for r in row_data), default=0)
    card_w    = max(max_row_w, st_w, 340) + PAD_X * 2
    card_h    = PAD_Y
    if top_img:  card_h += img_d + 16
    if strike:   card_h += st_h + 14
    for r in row_data:
        card_h += r['max_h'] + ROW_GAP
    card_h += PAD_Y - ROW_GAP

    cx = W // 2
    x0, x1 = max(30, cx - card_w//2), min(W-30, cx + card_w//2)
    y0, y1 = cy - card_h//2, cy + card_h//2

    # ── shadow ─────────────────────────────────────────────────────────────
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([x0, y0+9, x1, y1+9], radius=22, fill=(0,0,0,155))
    surf.alpha_composite(sh.filter(ImageFilter.GaussianBlur(11)))

    # ── card body ──────────────────────────────────────────────────────────
    cb = Image.new('RGBA', (W, H), (0,0,0,0))
    ImageDraw.Draw(cb).rounded_rectangle([x0, y0, x1, y1], radius=22, fill=CARD, outline=BORDER, width=2)
    surf.alpha_composite(cb)

    # ── content ────────────────────────────────────────────────────────────
    d   = ImageDraw.Draw(surf)
    cur = y0 + PAD_Y

    if top_img:
        mask = Image.new('L', (img_d, img_d), 0)
        ImageDraw.Draw(mask).ellipse([0,0,img_d,img_d], fill=255)
        ix = cx - img_d//2
        surf.paste(top_img.resize((img_d,img_d), Image.Resampling.LANCZOS), (ix, cur), mask)
        ImageDraw.Draw(surf).ellipse([ix, cur, ix+img_d, cur+img_d], outline=GOLD, width=3)
        cur += img_d + 16

    if strike:
        st_txt, st_fnt, st_col = strike
        sx = cx - st_w//2
        d.text((sx, cur), st_txt, font=st_fnt, fill=st_col)
        d.line([sx-4, cur+st_h//2, sx+st_w+4, cur+st_h//2], fill=(228, 58, 58, 255), width=5)
        cur += st_h + 14

    for ri, rd in enumerate(row_data):
        total_w = rd['total_w']
        max_h   = rd['max_h']
        sx      = cx - total_w // 2
        base_y  = cur

        for txt, fnt, col, sw, sh_ in rd['segs']:
            # vertically center segment within tallest seg in row
            ty = base_y + (max_h - sh_) // 2
            d.text((sx, ty), txt, font=fnt, fill=col)
            sx += sw + 14

        # underline accent
        if ul_row == ri:
            ul_x0 = cx - total_w//2 - 2
            ul_x1 = cx + total_w//2 + 2
            ul_y  = base_y + max_h + 5
            d.line([ul_x0, ul_y, ul_x1, ul_y], fill=(10,14,20,255), width=5)
            d.line([ul_x0, ul_y, ul_x1, ul_y], fill=GOLD,           width=3)

        cur += max_h + ROW_GAP

    return np.array(surf, dtype=np.uint8)


# ── Scene definitions ────────────────────────────────────────────────────────
#   Every scene has a distinct personality.

rafale_img = Image.open(RAFALE).convert('RGBA') if os.path.exists(RAFALE) else None

SCENE_SPECS = {

    # A1 — BIG opening hero, stacked two-line
    'A1': {
        'cy': 1350,
        'lines': [
            [('EVM HACK?',   Fh(70), GOLD)],
            [('HO GAYI!',    Fh(50), WHITE)],
        ],
    },

    # A2 — Same energy, inline, slightly smaller — voice shifts here
    'A2': {
        'cy': 1340,
        'lines': [
            [('VOTE CHORI', Fh(56), GOLD), ('HO GAYA?', Fh(56), WHITE)],
        ],
    },

    # B1 — Compact demi-heavy mix, conversational
    'B1': {
        'cy': 1330,
        'lines': [
            [('BAS EK', Fd(40), MUTED)],
            [('SIMPLE SAWAAL!', Fh(60), GOLD)],
        ],
    },

    # B2 — Punchy, stacked with gold underline on key phrase
    'B2': {
        'cy': 1350,
        'underline': 0,
        'lines': [
            [('SUPREME COURT', Fh(54), GOLD)],
            [('KYUN NAHI JA RAHE?', Fh(44), WHITE)],
        ],
    },

    # C1 — Long statement, two lines, key word larger
    'C1': {
        'cy': 1350,
        'lines': [
            [('ELECTION CANCEL', Fh(50), WHITE)],
            [('KARWANE KI POWER!', Fh(56), GOLD)],
        ],
    },

    # D1 — Small descriptor + big fact  (BIHAR big, inline)
    'D1': {
        'cy': 1335,
        'lines': [
            [('BIHAR —', Fd(38), MUTED), ('ELECTION NULLIFIED', Fh(54), WHITE)],
        ],
    },

    # D2 — Same structure, gold accent swaps
    'D2': {
        'cy': 1335,
        'lines': [
            [('PUNJAB —', Fd(38), MUTED), ('50 WARDS', Fh(58), GOLD), ('RE-POLL', Fh(58), WHITE)],
        ],
    },

    # E1 — Strikethrough contrast card
    'E1': {
        'cy': 1345,
        'strike': ('TWITTER THREADS', Fd(44), MUTED),
        'lines': [
            [('SWORN AFFIDAVITS!', Fh(58), GOLD)],
        ],
    },

    # F1 — Image badge, compact stacked (cy lower, image larger)
    'F1': {
        'cy': 1450,
        'top_img': rafale_img,
        'lines': [
            [('UNCONDITIONAL', Fh(48), WHITE)],
            [('APOLOGY IN SC', Fh(48), GOLD)],
        ],
    },

    # G1 — Rhetorical question, KYUN? big + amber pop
    'G1': {
        'cy': 1340,
        'lines': [
            [('SADAK PAR TAMASHA', Fh(44), WHITE)],
            [('KYUN?', Fh(80), AMBER)],
        ],
    },

    # H1 — Urgent command, single bold line, no descriptor
    'H1': {
        'cy': 1340,
        'lines': [
            [('JAO JUDGE', Fh(60), WHITE), ('KE PAAS!', Fh(60), GOLD)],
        ],
    },

    # H2 — Climax. DELHI! = massive amber
    'H2': {
        'cy': 1365,
        'lines': [
            [('STOP BLACKMAILING', Fh(50), WHITE)],
            [('DELHI!', Fh(82), AMBER)],
        ],
    },
}

print("Building surfaces...")
surfaces = {sid: build_card(spec) for sid, spec in SCENE_SPECS.items()}
print(f"  {len(surfaces)} surfaces ready.")

TIMELINE = [
    ('A1',  0.0,   2.5),
    ('A2',  2.5,   3.9),
    # gap 3.9–4.9 — "sab sun liya…"
    ('B1',  4.9,   6.35),
    ('B2',  6.35,  7.8),
    ('C1',  7.8,  12.4),
    ('D1', 12.4,  13.5),
    ('D2', 13.5,  16.0),
    # gap 16.0–18.0 — "court isliye nahi jaate…"
    ('E1', 18.0,  21.5),
    ('F1', 21.5,  25.5),
    ('G1', 25.5,  28.5),
    ('H1', 28.5,  31.5),
    ('H2', 31.5,  35.2),
]

FPS   = 30
TOTAL = int(36.52 * FPS)
EMPTY = b'\x00' * (W * H * 4)

print("2. Generating overlay...")
cmd_ov = [
    FFMPEG, '-y',
    '-f', 'rawvideo', '-pix_fmt', 'rgba',
    '-s', f'{W}x{H}', '-r', str(FPS),
    '-i', '-', '-c:v', 'qtrle', OVERLAY
]
proc = subprocess.Popen(cmd_ov, stdin=subprocess.PIPE,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
t0 = time.time()

for f in range(TOTAL):
    t = f / FPS
    written = False
    for sid, s, e in TIMELINE:
        if not (s <= t < e):
            continue
        arr   = surfaces[sid].copy()
        dur_f = int((e - s) * FPS)
        cur_f = int((t - s) * FPS)

        # entrance ease-out (5 frames)
        if cur_f < 5:
            alpha = 1.0 - (1.0 - cur_f/5.0)**2
        # exit linear (4 frames)
        elif cur_f > dur_f - 4:
            alpha = max(0.0, (dur_f - cur_f) / 4.0)
        else:
            alpha = 1.0

        if alpha < 0.99:
            arr[..., 3] = (arr[..., 3].astype(np.float32) * alpha).astype(np.uint8)

        # gentle 3px upward drift
        drift = int(-3 * cur_f / max(dur_f, 1))
        if drift:
            shifted = np.zeros_like(arr)
            shifted[:drift, :] = arr[-drift:, :]
            arr = shifted

        proc.stdin.write(arr.tobytes())
        written = True
        break

    if not written:
        proc.stdin.write(EMPTY)

proc.stdin.close()
proc.wait()
print(f"  Overlay in {time.time()-t0:.1f}s")

print("3. Final composite...")
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
print(f"\n✓  {mb:.1f} MB  —  {time.time()-t1:.1f}s")
print(f"   {FINAL_OUT}")
