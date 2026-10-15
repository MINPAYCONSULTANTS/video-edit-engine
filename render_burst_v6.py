"""
render_burst_v6.py
──────────────────
Continuous Phrase-Level (Word-to-Word Cadence) Video Engine
• 100% video coverage: Every spoken phrase has dynamic subtitles
• NO background boxes/cards: Pure typography floating directly on video
• 3px black stroke contour + Gaussian drop shadow for crystal-clear readability
• Varied typographic hierarchy:
    - Small/medium muted setup words (Avenir Next Demi, 38-46px)
    - Big hero keywords (Avenir Next Heavy, 58-76px)
    - Gold / Amber accents on core punch words
    - Elastic micro-pop (scale 1.05 -> 1.0) on entrance
    - Special moments: Red strikethrough (Twitter Threads) & Rafale circular photo badge
• Anchor safe zone: cy ≈ 1340 (clears chin, chest gestures, and frame borders)
"""

import os, sys, subprocess, time, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORK      = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit'
RAW       = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960.mp4'
FFMPEG    = '/Users/sanskarsaraf/.gemini/antigravity/scratch/social.minpay.in/video_generator/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg'
RAFALE    = f'{WORK}/ref_assets/rafale_jet.png'
OVERLAY   = f'{WORK}/overlay_v6.mov'
TEMP_OUT  = f'{WORK}/craft_v6_temp.mp4'
FINAL_OUT = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960_EDITED.mp4'

W, H = 1080, 1920
FPS  = 30

def Fh(sz): return ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=8) # Heavy
def Fd(sz): return ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=2) # Demi Bold

WHITE = (255, 255, 255, 255)
GOLD  = (255, 210, 50,  255)
AMBER = (255, 148, 22,  255)
MUTED = (205, 215, 225, 255)

def _m(d, text, font, stroke=3):
    b = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
    return b[2]-b[0], b[3]-b[1]

def draw_text(surf, cx, cy, text, font, fill, stroke_w=3, shadow_blur=8, shadow_offset=4):
    d = ImageDraw.Draw(surf)
    w, h = _m(d, text, font, stroke_w)
    tx = cx - w // 2
    ty = cy - h // 2

    # Shadow layer
    sh_surf = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_d = ImageDraw.Draw(sh_surf)
    sh_d.text((tx, ty + shadow_offset), text, font=font,
              fill=(0, 0, 0, 220), stroke_width=stroke_w, stroke_fill=(0, 0, 0, 220))
    surf.alpha_composite(sh_surf.filter(ImageFilter.GaussianBlur(shadow_blur)))

    # Sharp text with dark contour
    d2 = ImageDraw.Draw(surf)
    d2.text((tx, ty), text, font=font, fill=fill,
            stroke_width=stroke_w, stroke_fill=(0, 0, 0, 255))
    return tx, ty, w, h

def draw_strikethrough(surf, cx, cy, text, font):
    d = ImageDraw.Draw(surf)
    w, h = _m(d, text, font, 2)
    tx = cx - w // 2
    ty = cy - h // 2

    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    ImageDraw.Draw(sh).text((tx, ty+4), text, font=font,
                            fill=(0,0,0,160), stroke_width=2, stroke_fill=(0,0,0,160))
    surf.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))

    ImageDraw.Draw(surf).text((tx, ty), text, font=font, fill=MUTED,
                              stroke_width=2, stroke_fill=(0,0,0,220))
    mid_y = ty + h // 2
    ImageDraw.Draw(surf).line([tx-6, mid_y, tx+w+6, mid_y], fill=(235, 50, 50, 255), width=5)

def draw_underline(surf, cx, text_w, y_base, color=GOLD):
    x0 = cx - text_w // 2 - 4
    x1 = cx + text_w // 2 + 4
    d = ImageDraw.Draw(surf)
    d.line([x0, y_base, x1, y_base], fill=(0,0,0,255), width=5)
    d.line([x0, y_base, x1, y_base], fill=color,       width=3)

def draw_circular_badge(surf, cx, cy, img, diameter=120):
    mask = Image.new('L', (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, diameter, diameter], fill=255)
    ri = img.resize((diameter, diameter), Image.Resampling.LANCZOS)
    ix, iy = cx - diameter//2, cy - diameter//2

    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    ImageDraw.Draw(sh).ellipse([ix, iy+5, ix+diameter, iy+diameter+5], fill=(0,0,0,180))
    surf.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))

    surf.paste(ri, (ix, iy), mask)
    ImageDraw.Draw(surf).ellipse([ix, iy, ix+diameter, iy+diameter], outline=(0,0,0,255), width=4)
    ImageDraw.Draw(surf).ellipse([ix, iy, ix+diameter, iy+diameter], outline=GOLD, width=2)

def build_scene_surface(spec):
    s = Image.new('RGBA', (W, H), (0,0,0,0))
    cy      = spec.get('cy', 1340)
    rows    = spec.get('rows', [])
    strike  = spec.get('strike', None)
    ul_row  = spec.get('underline', None)
    top_img = spec.get('top_img', None)

    td = ImageDraw.Draw(s)
    row_measures = []
    for row in rows:
        segs = []
        for txt, fnt, col in row:
            w, h = _m(td, txt, fnt)
            segs.append((txt, fnt, col, w, h))
        total_w = sum(seg[3] for seg in segs) + 14 * (len(segs) - 1)
        max_h   = max(seg[4] for seg in segs)
        row_measures.append((segs, total_w, max_h))

    ROW_GAP = 12
    img_d   = 120
    block_h = 0
    if top_img: block_h += img_d + 16
    if strike:
        _, sh_ = _m(td, strike[0], strike[1], 2)
        block_h += sh_ + 14
    for _, _, mh in row_measures:
        block_h += mh + ROW_GAP
    block_h -= ROW_GAP

    cur = cy - block_h // 2

    if top_img:
        draw_circular_badge(s, W//2, cur + img_d//2, top_img, img_d)
        cur += img_d + 16

    if strike:
        _, sh_ = _m(td, strike[0], strike[1], 2)
        draw_strikethrough(s, W//2, cur + sh_//2, strike[0], strike[1])
        cur += sh_ + 14

    for ri, (segs, total_w, max_h) in enumerate(row_measures):
        sx = W//2 - total_w//2
        for txt, fnt, col, sw_, sh_ in segs:
            draw_text(s, sx + sw_//2, cur + max_h//2, txt, fnt, col)
            sx += sw_ + 14

        if ul_row == ri:
            draw_underline(s, W//2, total_w, cur + max_h + 7)

        cur += max_h + ROW_GAP

    return s

rafale_img = Image.open(RAFALE).convert('RGBA') if os.path.exists(RAFALE) else None

# ── Complete Continuous Phrase-Burst Timeline ─────────────────────────────────
BURSTS = [
    # 0.0 - 2.5: EVM HACK? HO GAYI!
    {
        'id': 'p01', 'start': 0.0, 'end': 2.45, 'cy': 1345,
        'rows': [
            [('EVM HACK?', Fh(70), GOLD)],
            [('HO GAYI!',  Fh(48), WHITE)],
        ]
    },
    # 2.45 - 3.9: VOTE CHORI HO GAYA?
    {
        'id': 'p02', 'start': 2.45, 'end': 3.90, 'cy': 1340,
        'rows': [
            [('VOTE CHORI', Fh(56), GOLD), ('HO GAYA?', Fh(56), WHITE)],
        ]
    },
    # 3.9 - 4.9: SAB SUN LIYA...
    {
        'id': 'p03', 'start': 3.90, 'end': 4.90, 'cy': 1335,
        'rows': [
            [('SAB SUN LIYA...', Fd(48), MUTED)],
        ]
    },
    # 4.9 - 6.35: BAS EK SIMPLE SAWAAL!
    {
        'id': 'p04', 'start': 4.90, 'end': 6.35, 'cy': 1340,
        'rows': [
            [('BAS EK',         Fd(40), MUTED)],
            [('SIMPLE SAWAAL!', Fh(64), GOLD)],
        ]
    },
    # 6.35 - 7.75: SUPREME COURT KYUN NAHI JA RAHE?
    {
        'id': 'p05', 'start': 6.35, 'end': 7.75, 'cy': 1350,
        'underline': 0,
        'rows': [
            [('SUPREME COURT',      Fh(56), GOLD)],
            [('KYUN NAHI JA RAHE?', Fh(42), WHITE)],
        ]
    },
    # 7.75 - 10.45: POORI CONSTITUTIONAL POWER HAI
    {
        'id': 'p06', 'start': 7.75, 'end': 10.45, 'cy': 1340,
        'rows': [
            [('SUPREME COURT KE PAAS', Fd(38), MUTED)],
            [('CONSTITUTIONAL POWER HAI!', Fh(54), GOLD)],
        ]
    },
    # 10.45 - 12.4: ELECTION CANCEL KARWANE KI!
    {
        'id': 'p07', 'start': 10.45, 'end': 12.40, 'cy': 1345,
        'rows': [
            [('ELECTION CANCEL', Fh(52), WHITE)],
            [('KARWANE KI!',     Fh(64), AMBER)],
        ]
    },
    # 12.4 - 13.5: BIHAR MEIN KARWAYA THA!
    {
        'id': 'p08', 'start': 12.40, 'end': 13.50, 'cy': 1335,
        'rows': [
            [('BIHAR MEIN —', Fd(38), MUTED), ('ELECTION NULLIFIED', Fh(52), WHITE)],
        ]
    },
    # 13.5 - 15.5: PUNJAB MEIN 50 WARDS RE-POLL!
    {
        'id': 'p09', 'start': 13.50, 'end': 15.80, 'cy': 1335,
        'rows': [
            [('PUNJAB MEIN —', Fd(38), MUTED), ('50 WARDS', Fh(56), GOLD), ('RE-POLL', Fh(56), WHITE)],
        ]
    },
    # 15.8 - 18.0: COURT ISLIYE NAHI JAATE...
    {
        'id': 'p10', 'start': 15.80, 'end': 18.00, 'cy': 1340,
        'rows': [
            [('COURT ISLIYE NAHI JAATE...', Fd(48), MUTED)],
        ]
    },
    # 18.0 - 19.95: KYUNKI WAHA PE AFFIDAVITS LAGTE HAIN!
    {
        'id': 'p11', 'start': 18.00, 'end': 19.95, 'cy': 1345,
        'rows': [
            [('KYUNKI WAHA PE',    Fd(40), MUTED)],
            [('SWORN AFFIDAVITS!', Fh(60), GOLD)],
        ]
    },
    # 19.95 - 21.8: TWITTER THREADS NAHI! (Strikethrough)
    {
        'id': 'p12', 'start': 19.95, 'end': 21.80, 'cy': 1345,
        'strike': ('TWITTER THREADS', Fd(48)),
        'rows': [
            [('TWITTER THREADS NAHI!', Fh(52), WHITE)],
        ]
    },
    # 21.8 - 25.35: WAHA JHOOTH BOLA TOH RAFALE JAISI MAAFI! (With Rafale badge)
    {
        'id': 'p13', 'start': 21.80, 'end': 25.40, 'cy': 1420,
        'top_img': rafale_img,
        'rows': [
            [('WAHA JHOOTH BOLA TOH', Fd(38), MUTED)],
            [('RAFALE JAISI MAAFI!',  Fh(54), GOLD)],
        ]
    },
    # 25.4 - 28.5: ISLIYE SADAK PAR TAMASHA... KYUN?
    {
        'id': 'p14', 'start': 25.40, 'end': 28.50, 'cy': 1350,
        'rows': [
            [('SADAK PAR TAMASHA', Fh(46), WHITE)],
            [('KYUN?',             Fh(82), AMBER)],
        ]
    },
    # 28.5 - 31.95: AGAR PROOF HAI TOH JUDGE KE PAAS JAO!
    {
        'id': 'p15', 'start': 28.50, 'end': 31.95, 'cy': 1345,
        'rows': [
            [('AGAR PROOF HAI', Fd(38), MUTED)],
            [('JAO JUDGE', Fh(60), WHITE), ('KE PAAS!', Fh(60), GOLD)],
        ]
    },
    # 31.95 - 35.5: STOP BLACKMAILING DELHI!
    {
        'id': 'p16', 'start': 31.95, 'end': 35.50, 'cy': 1360,
        'rows': [
            [('STOP BLACKMAILING', Fh(50), WHITE)],
            [('DELHI!',            Fh(84), AMBER)],
        ]
    },
]

print("1. Pre-rendering burst surfaces...")
surfaces_dict = {}
for b in BURSTS:
    surfaces_dict[b['id']] = build_scene_surface(b)
print(f"  {len(surfaces_dict)} phrase burst surfaces rendered.")

# ── Animation & Video Generation ──────────────────────────────────────────────
TOTAL_FRAMES = int(36.52 * FPS)
EMPTY = b'\x00' * (W * H * 4)

print("2. Generating continuous overlay stream with micro-physics...")
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
    active_b = None
    for b in BURSTS:
        if b['start'] <= t < b['end']:
            active_b = b
            break

    if active_b is None:
        proc.stdin.write(EMPTY)
        continue

    bid = active_b['id']
    s_t = active_b['start']
    e_t = active_b['end']
    dur_f = max(int((e_t - s_t) * FPS), 1)
    cur_f = int((t - s_t) * FPS)

    # Elastic entrance physics (frames 0..4)
    # Scale slightly from 1.05 down to 1.0, alpha fade 0 -> 1
    if cur_f < 4:
        alpha = (cur_f + 1) / 4.0
        # Subtle scale pop
        scale = 1.04 - 0.04 * (cur_f / 3.0)
    elif cur_f > dur_f - 3:
        alpha = max(0.0, (dur_f - cur_f) / 3.0)
        scale = 1.0
    else:
        alpha = 1.0
        scale = 1.0

    base_pil = surfaces_dict[bid]
    if scale != 1.0:
        # Resize from center
        nw, nh = int(W * scale), int(H * scale)
        scaled_img = base_pil.resize((nw, nh), Image.Resampling.BILINEAR)
        # Crop or paste back to (W, H)
        ox, oy = (nw - W) // 2, (nh - H) // 2
        frame_pil = scaled_img.crop((ox, oy, ox + W, oy + H))
    else:
        frame_pil = base_pil.copy()

    arr = np.array(frame_pil, dtype=np.uint8)

    # Apply alpha
    if alpha < 0.99:
        arr[..., 3] = (arr[..., 3].astype(np.float32) * alpha).astype(np.uint8)

    # Gentle 2px upward kinetic drift
    drift = int(-2 * cur_f / max(dur_f, 1))
    if drift != 0:
        shifted = np.zeros_like(arr)
        shifted[:drift, :] = arr[-drift:, :]
        arr = shifted

    proc.stdin.write(arr.tobytes())

proc.stdin.close()
proc.wait()
print(f"  Overlay stream encoded in {time.time()-t0:.1f}s")

print("3. Final Composite & Dialogue Equalization...")
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
print(f"\n✓ Complete Video Ready: {mb:.1f} MB in {time.time()-t1:.1f}s")
print(f"   {FINAL_OUT}")
