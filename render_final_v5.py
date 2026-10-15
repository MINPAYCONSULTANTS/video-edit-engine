"""
render_final_v5.py
──────────────────
NO background cards. Zero boxes.
Clean text directly on video with:
  • Thin 3px black outline for edge definition
  • Directional drop shadow (Gaussian blur) for depth
  • Typographic variety: stacked / inline / size hierarchy
  • All at cy≈1340 (safe zone — face clear, hands clear)
"""

import os, sys, subprocess, time, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORK   = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit'
RAW    = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960.mp4'
FFMPEG = '/Users/sanskarsaraf/.gemini/antigravity/scratch/social.minpay.in/video_generator/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg'
RAFALE = f'{WORK}/ref_assets/rafale_jet.png'
OVERLAY   = f'{WORK}/overlay_v5.mov'
TEMP_OUT  = f'{WORK}/craft_v5_temp.mp4'
FINAL_OUT = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960_EDITED.mp4'

def Fh(sz): return ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=8)
def Fd(sz): return ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=2)

WHITE  = (255, 255, 255, 255)
GOLD   = (255, 210, 50,  255)
AMBER  = (255, 148, 22,  255)
MUTED  = (200, 210, 225, 255)
BLACK  = (0,   0,   0,   255)

W, H = 1080, 1920

def _m(d, text, font, stroke=3):
    b = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
    return b[2]-b[0], b[3]-b[1]

def draw_text(surf, cx, cy, text, font, fill, stroke_w=3, shadow_blur=7, shadow_offset=4):
    """Draw text with directional shadow + thin outline. No background."""
    d = ImageDraw.Draw(surf)
    w, h = _m(d, text, font, stroke_w)
    tx = cx - w // 2
    ty = cy - h // 2

    # Directional shadow layer
    sh_surf = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_d = ImageDraw.Draw(sh_surf)
    sh_d.text((tx, ty + shadow_offset), text, font=font,
              fill=(0, 0, 0, 210), stroke_width=stroke_w, stroke_fill=(0, 0, 0, 210))
    surf.alpha_composite(sh_surf.filter(ImageFilter.GaussianBlur(shadow_blur)))

    # Clean text with thin outline
    d2 = ImageDraw.Draw(surf)
    d2.text((tx, ty), text, font=font, fill=fill,
            stroke_width=stroke_w, stroke_fill=(0, 0, 0, 255))

    return tx, ty, w, h

def draw_strikethrough_text(surf, cx, cy, text, font, fill=(200,210,225,255)):
    """Draw muted text with red strike line through the middle."""
    d = ImageDraw.Draw(surf)
    w, h = _m(d, text, font, 2)
    tx = cx - w // 2
    ty = cy - h // 2

    # Shadow
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    ImageDraw.Draw(sh).text((tx, ty+4), text, font=font,
                            fill=(0,0,0,160), stroke_width=2, stroke_fill=(0,0,0,160))
    surf.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))

    ImageDraw.Draw(surf).text((tx, ty), text, font=font, fill=fill,
                              stroke_width=2, stroke_fill=(0,0,0,220))
    # Red strike
    mid_y = ty + h // 2
    ImageDraw.Draw(surf).line([tx-4, mid_y, tx+w+4, mid_y], fill=(230, 55, 55, 255), width=5)

def draw_underline(surf, cx, text_w, y_base, color=GOLD):
    x0 = cx - text_w // 2 - 4
    x1 = cx + text_w // 2 + 4
    d = ImageDraw.Draw(surf)
    d.line([x0, y_base, x1, y_base], fill=(0,0,0,255), width=5)
    d.line([x0, y_base, x1, y_base], fill=color,       width=3)

def draw_circular_image(surf, cx, cy, img, diameter=120):
    """Draw a circular photo badge with gold ring, no background card."""
    mask = Image.new('L', (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, diameter, diameter], fill=255)
    ri = img.resize((diameter, diameter), Image.Resampling.LANCZOS)
    ix, iy = cx - diameter//2, cy - diameter//2

    # Shadow under image
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    ImageDraw.Draw(sh).ellipse([ix, iy+5, ix+diameter, iy+diameter+5], fill=(0,0,0,180))
    surf.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))

    surf.paste(ri, (ix, iy), mask)
    # Gold ring
    ImageDraw.Draw(surf).ellipse([ix, iy, ix+diameter, iy+diameter],
                                 outline=(0,0,0,255), width=4)
    ImageDraw.Draw(surf).ellipse([ix, iy, ix+diameter, iy+diameter],
                                 outline=GOLD, width=2)


# ── Scene builder ────────────────────────────────────────────────────────────

def build(spec):
    s = Image.new('RGBA', (W, H), (0,0,0,0))
    layout = spec.get('layout', 'stacked')
    cy     = spec.get('cy', 1340)
    rows   = spec.get('rows', [])       # list of rows; each row = list of (text,font,color)
    strike = spec.get('strike', None)   # (text, font) shown above rows, crossed out
    ul_row = spec.get('underline', None)
    top_img = spec.get('top_img', None)

    # ── measure all rows ───────────────────────────────────────────────────
    td = ImageDraw.Draw(s)
    row_measures = []
    for row in rows:
        segs = []
        for txt, fnt, col in row:
            w, h = _m(td, txt, fnt)
            segs.append((txt, fnt, col, w, h))
        total_w = sum(seg[3] for seg in segs) + 14*(len(segs)-1)
        max_h   = max(seg[4] for seg in segs)
        row_measures.append((segs, total_w, max_h))

    # ── total block height ─────────────────────────────────────────────────
    ROW_GAP = 12
    img_d   = 120

    block_h = 0
    if top_img:   block_h += img_d + 18
    if strike:
        sw, sh_ = _m(td, strike[0], strike[1], 2)
        block_h += sh_ + 16
    for _, _, mh in row_measures:
        block_h += mh + ROW_GAP
    block_h -= ROW_GAP

    # ── draw from top ──────────────────────────────────────────────────────
    cur = cy - block_h // 2

    if top_img:
        draw_circular_image(s, W//2, cur + img_d//2, top_img, img_d)
        cur += img_d + 18

    if strike:
        sw, sh_ = _m(td, strike[0], strike[1], 2)
        draw_strikethrough_text(s, W//2, cur + sh_//2, strike[0], strike[1])
        cur += sh_ + 16

    for ri, (segs, total_w, max_h) in enumerate(row_measures):
        sx = W//2 - total_w//2
        for txt, fnt, col, sw_, sh_ in segs:
            tx_off = sw_//2
            draw_text(s, sx + tx_off, cur + max_h//2, txt, fnt, col)
            sx += sw_ + 14

        if ul_row == ri:
            _, _, total_w2, _ = _m(td, segs[0][0], segs[0][1]), 0, 0, 0
            # underline the full row width
            draw_underline(s, W//2, total_w, cur + max_h + 7)

        cur += max_h + ROW_GAP

    return np.array(s, dtype=np.uint8)


# ── Scene specs ──────────────────────────────────────────────────────────────
rafale_img = Image.open(RAFALE).convert('RGBA') if os.path.exists(RAFALE) else None

SPECS = {
    # A1 — Hero stacked opener
    'A1': {'cy': 1350, 'rows': [
        [('EVM HACK?',  Fh(72), GOLD)],
        [('HO GAYI!',   Fh(50), WHITE)],
    ]},

    # A2 — Inline, slightly calmer
    'A2': {'cy': 1340, 'rows': [
        [('VOTE CHORI', Fh(56), GOLD), ('HO GAYA?', Fh(56), WHITE)],
    ]},

    # B1 — Small setup + big punchline
    'B1': {'cy': 1340, 'rows': [
        [('BAS EK',          Fd(40), MUTED)],
        [('SIMPLE SAWAAL!',  Fh(62), GOLD)],
    ]},

    # B2 — Supreme court with underline on first row
    'B2': {'cy': 1355, 'underline': 0, 'rows': [
        [('SUPREME COURT',     Fh(56), GOLD)],
        [('KYUN NAHI JA RAHE?', Fh(44), WHITE)],
    ]},

    # C1 — Constitutional power, two-line stacked
    'C1': {'cy': 1355, 'rows': [
        [('ELECTION CANCEL',   Fh(50), WHITE)],
        [('KARWANE KI POWER!', Fh(56), GOLD)],
    ]},

    # D1 — Muted descriptor + fact inline
    'D1': {'cy': 1335, 'rows': [
        [('BIHAR —', Fd(38), MUTED), ('ELECTION NULLIFIED', Fh(54), WHITE)],
    ]},

    # D2 — Three segment inline, gold stat
    'D2': {'cy': 1335, 'rows': [
        [('PUNJAB —', Fd(38), MUTED), ('50 WARDS', Fh(56), GOLD), ('RE-POLL', Fh(56), WHITE)],
    ]},

    # E1 — Strikethrough contrast
    'E1': {'cy': 1345, 'strike': ('TWITTER THREADS', Fd(44)), 'rows': [
        [('SWORN AFFIDAVITS!', Fh(60), GOLD)],
    ]},

    # F1 — Circular Rafale badge + text, no card
    'F1': {'cy': 1420, 'top_img': rafale_img, 'rows': [
        [('UNCONDITIONAL', Fh(48), WHITE)],
        [('APOLOGY IN SC', Fh(48), GOLD)],
    ]},

    # G1 — Rhetorical stacked, KYUN? massive
    'G1': {'cy': 1345, 'rows': [
        [('SADAK PAR TAMASHA', Fh(44), WHITE)],
        [('KYUN?',             Fh(82), AMBER)],
    ]},

    # H1 — Clean inline command
    'H1': {'cy': 1340, 'rows': [
        [('JAO JUDGE', Fh(60), WHITE), ('KE PAAS!', Fh(60), GOLD)],
    ]},

    # H2 — Climax, DELHI! enormous
    'H2': {'cy': 1365, 'rows': [
        [('STOP BLACKMAILING', Fh(50), WHITE)],
        [('DELHI!',            Fh(84), AMBER)],
    ]},
}

print("Building surfaces...")
surfaces = {sid: build(spec) for sid, spec in SPECS.items()}
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

        if cur_f < 5:
            alpha = 1.0 - (1.0 - cur_f/5.0)**2
        elif cur_f > dur_f - 4:
            alpha = max(0.0, (dur_f - cur_f) / 4.0)
        else:
            alpha = 1.0

        if alpha < 0.99:
            arr[..., 3] = (arr[..., 3].astype(np.float32) * alpha).astype(np.uint8)

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
print(f"\n✓  {mb:.1f} MB  in  {time.time()-t1:.1f}s")
print(f"   {FINAL_OUT}")
