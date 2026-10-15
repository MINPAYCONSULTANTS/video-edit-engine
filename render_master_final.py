import os, sys, time, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RAW = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960.mp4'
FINAL_OUT = '/Users/sanskarsaraf/Downloads/PXL_20261012_102411960_EDITED.mp4'
FFMPEG = '/Users/sanskarsaraf/.gemini/antigravity/scratch/social.minpay.in/video_generator/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg'
WORK_DIR = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit'

W, H = 1080, 1920
FPS = 30
TOTAL_DUR = 36.52
TOTAL_FRAMES = int(TOTAL_DUR * FPS) + 1

# Fonts
F_SANS_BOLD = lambda sz: ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=0)
F_SANS_DEMI = lambda sz: ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=2)
F_SERIF_ITALIC = lambda sz: ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf', sz)

C_WHITE = (255, 255, 255, 255)
C_GOLD = (248, 210, 95, 255)
C_MUTED = (220, 225, 235, 255)
C_RED = (255, 65, 65, 255)

PHRASES = [
    # 0: Hook
    {
        'id': 'b01',
        'start': 0.00, 'end': 2.50,
        'lines': [[('evm', False), ('hack', True), ('ho gayi?', False)]],
        'top_anchor': None
    },
    {
        'id': 'b02',
        'start': 2.50, 'end': 3.94,
        'lines': [[('vote', False), ('chori', True), ('ho gaya?', False)]],
        'top_anchor': None
    },
    {
        'id': 'b03',
        'start': 3.94, 'end': 4.90,
        'lines': [[('sab sun liya...', False)]],
        'top_anchor': None
    },
    # 1: The Question
    {
        'id': 'b04',
        'start': 4.90, 'end': 6.38,
        'lines': [[('bas ek', False), ('simple sawaal!', True)]],
        'top_anchor': None
    },
    {
        'id': 'b05',
        'start': 6.38, 'end': 7.78,
        'lines': [[('supreme court', True), ('kyun nahi ja rahe ho?', False)]],
        'top_anchor': None
    },
    # 2: Constitutional Power (with Top Editorial Serif Anchor)
    {
        'id': 'b06',
        'start': 7.78, 'end': 10.60,
        'lines': [
            [('supreme court ke paas', False)],
            [('poori', False), ('constitutional power', True), ('hai ki', False)]
        ],
        'top_anchor': {
            'title': 'Constitutional Power',
            'sub': 'ARTICLE 32 & 142 • APEX JURISDICTION'
        }
    },
    {
        'id': 'b07',
        'start': 10.60, 'end': 12.44,
        'lines': [[('election', False), ('cancel', True), ('karwane ki,', False)]],
        'top_anchor': {
            'title': 'Constitutional Power',
            'sub': 'ARTICLE 32 & 142 • APEX JURISDICTION'
        }
    },
    # 3: Precedents
    {
        'id': 'b08',
        'start': 12.44, 'end': 13.94,
        'lines': [[('Bihar', True), ('mein karwaya tha,', False)]],
        'top_anchor': None
    },
    {
        'id': 'b09',
        'start': 13.94, 'end': 16.50,
        'lines': [
            [('abhi Punjab mein', False)],
            [('50 wards', True), ('mein karwaya hai.', False)]
        ],
        'top_anchor': None
    },
    # 4: Transition
    {
        'id': 'b10',
        'start': 16.50, 'end': 18.40,
        'lines': [[('court isliye nahi jaate kyunki', False)]],
        'top_anchor': None
    },
    {
        'id': 'b11',
        'start': 18.40, 'end': 20.30,
        'lines': [[('waha pe', False), ('affidavits', True), ('lagte hain.', False)]],
        'top_anchor': None
    },
    # 5: Evidence Contrast (with centered strikethrough)
    {
        'id': 'b12',
        'start': 20.30, 'end': 22.40,
        'type': 'strike',
        'strike_phrase': 'twitter threads',
        'strike_line': 'twitter threads nahi',
        'follow_line': 'sworn affidavits lagte hain',
        'top_anchor': None
    },
    # 6: Rafale Precedent
    {
        'id': 'b13',
        'start': 22.40, 'end': 24.30,
        'lines': [
            [('waha jhooth bola toh', False)],
            [('Rafale', True), ('case ki tarah', False)]
        ],
        'top_anchor': None
    },
    {
        'id': 'b14',
        'start': 24.30, 'end': 26.50,
        'lines': [[('phir se', False), ('maafi maangni', True), ('padegi.', False)]],
        'top_anchor': None
    },
    # 7: Street tamasha
    {
        'id': 'b15',
        'start': 26.50, 'end': 29.98,
        'lines': [
            [('isliye sadak par', False)],
            [('tamasha', True), ('de rahe ho.', False)]
        ],
        'top_anchor': None
    },
    # 8: Climax / Verdict
    {
        'id': 'b16',
        'start': 29.98, 'end': 32.96,
        'lines': [
            [('agar', False), ('proof', True), ('hai toh', False)],
            [('judge ke paas', True), ('jao na.', False)]
        ],
        'top_anchor': None
    },
    {
        'id': 'b17',
        'start': 32.96, 'end': 35.50,
        'lines': [
            [('Delhi ko', False), ('blackmail', True), ('kyun', False)],
            [('kar rahe ho?', False)]
        ],
        'top_anchor': None
    }
]

def render_surface_for_phrase(p):
    """Renders the transparent RGBA surface for a phrase"""
    surf = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    f_sans = F_SANS_BOLD(54)
    
    # 1. Top Section Anchor if present
    if p.get('top_anchor'):
        ta = p['top_anchor']
        f_serif = F_SERIF_ITALIC(50)
        f_sub = F_SANS_DEMI(22)
        
        # Shadow pass
        sh_top = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(sh_top)
        
        bbox_t = s_draw.textbbox((0, 0), ta['title'], font=f_serif)
        tw_t = bbox_t[2] - bbox_t[0]
        s_draw.text(((W - tw_t) // 2, 170 + 4), ta['title'], font=f_serif, fill=(0, 0, 0, 220))
        
        bbox_s = s_draw.textbbox((0, 0), ta['sub'], font=f_sub)
        tw_s = bbox_s[2] - bbox_s[0]
        s_draw.text(((W - tw_s) // 2, 225 + 3), ta['sub'], font=f_sub, fill=(0, 0, 0, 220))
        
        surf.alpha_composite(sh_top.filter(ImageFilter.GaussianBlur(7)))
        
        # Text pass
        draw = ImageDraw.Draw(surf)
        draw.text(((W - tw_t) // 2, 170), ta['title'], font=f_serif, fill=C_GOLD, stroke_width=1, stroke_fill=(10, 10, 12, 230))
        draw.text(((W - tw_s) // 2, 225), ta['sub'], font=f_sub, fill=C_MUTED, stroke_width=1, stroke_fill=(10, 10, 12, 230))

    # 2. Evidence Contrast Strikethrough Scene
    if p.get('type') == 'strike':
        full_text = p['strike_line']
        target_text = p['strike_phrase']
        follow_text = p['follow_line']
        
        cx, cy1, cy2 = 540, 1340, 1420
        
        # Line 1: twitter threads nahi
        draw = ImageDraw.Draw(surf)
        bbox1 = draw.textbbox((0, 0), full_text, font=f_sans)
        tw1, th1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
        tx1 = cx - tw1 // 2
        ty1 = cy1 - th1 // 2
        
        w_target = draw.textlength(target_text, font=f_sans)
        bbox_target = draw.textbbox((0, 0), target_text, font=f_sans)
        opt_y = ty1 + (bbox_target[1] + bbox_target[3]) // 2
        
        # Shadow for line 1
        sh1 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sdraw1 = ImageDraw.Draw(sh1)
        sdraw1.text((tx1, ty1 + 4), full_text, font=f_sans, fill=(0, 0, 0, 220))
        sdraw1.text((tx1, ty1 + 2), full_text, font=f_sans, fill=(0, 0, 0, 250))
        surf.alpha_composite(sh1.filter(ImageFilter.GaussianBlur(7)))
        
        # Draw line 1 text
        draw = ImageDraw.Draw(surf)
        draw.text((tx1, ty1), full_text, font=f_sans, fill=C_WHITE, stroke_width=2, stroke_fill=(10, 10, 12, 230))
        
        # Draw red hairline strike right across "twitter threads"
        draw.line([tx1 - 6, opt_y + 2, tx1 + int(w_target) + 6, opt_y + 2], fill=(0, 0, 0, 180), width=5)
        draw.line([tx1 - 6, opt_y, tx1 + int(w_target) + 6, opt_y], fill=C_RED, width=3)
        
        # Line 2: sworn affidavits lagte hain (in rich gold)
        sh2 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sdraw2 = ImageDraw.Draw(sh2)
        bbox2 = sdraw2.textbbox((0, 0), follow_text, font=f_sans)
        tw2, th2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
        tx2 = cx - tw2 // 2
        ty2 = cy2 - th2 // 2
        sdraw2.text((tx2, ty2 + 4), follow_text, font=f_sans, fill=(0, 0, 0, 220))
        surf.alpha_composite(sh2.filter(ImageFilter.GaussianBlur(7)))
        
        draw = ImageDraw.Draw(surf)
        draw.text((tx2, ty2), follow_text, font=f_sans, fill=C_GOLD, stroke_width=2, stroke_fill=(10, 10, 12, 230))
        return surf

    # 3. Standard Body Captions (1 or 2 lines)
    lines = p.get('lines', [])
    cx = 540
    base_cy = 1370 if len(lines) == 1 else 1340
    line_spacing = 70
    
    for l_idx, line in enumerate(lines):
        curr_cy = base_cy + l_idx * line_spacing
        
        # Measure line
        draw = ImageDraw.Draw(surf)
        space_w = draw.textlength(' ', font=f_sans)
        total_w = sum(draw.textlength(w, font=f_sans) for w, is_emph in line) + space_w * (len(line) - 1)
        curr_x = cx - total_w // 2
        
        # Shadow pass
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(sh)
        temp_x = curr_x
        for w, is_emph in line:
            sdraw.text((temp_x, curr_cy + 4), w, font=f_sans, fill=(0, 0, 0, 220))
            sdraw.text((temp_x, curr_cy + 2), w, font=f_sans, fill=(0, 0, 0, 250))
            temp_x += draw.textlength(w, font=f_sans) + space_w
        surf.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
        
        # Text pass
        draw = ImageDraw.Draw(surf)
        for w, is_emph in line:
            color = C_GOLD if is_emph else C_WHITE
            draw.text((curr_x, curr_cy), w, font=f_sans, fill=color, stroke_width=2, stroke_fill=(10, 10, 12, 230))
            curr_x += draw.textlength(w, font=f_sans) + space_w
            
    return surf

print("Pre-rendering all 18 phrase graphic surfaces...")
SURFACES = {}
for p in PHRASES:
    SURFACES[p['id']] = render_surface_for_phrase(p)
print(f"Pre-rendered {len(SURFACES)} graphic surfaces successfully!")

# Build overlay video stream with smooth animation physics
OVERLAY_MOV = f'{WORK_DIR}/overlay_animated_reference.mov'
print(f"Streaming animated overlay to {OVERLAY_MOV}...")

proc = subprocess.Popen([
    FFMPEG, '-y',
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-s', f'{W}x{H}',
    '-pix_fmt', 'rgba',
    '-r', str(FPS),
    '-i', '-',
    '-c:v', 'qtrle',
    OVERLAY_MOV
], stdin=subprocess.PIPE)

empty_frame = Image.new('RGBA', (W, H), (0, 0, 0, 0))
empty_bytes = empty_frame.tobytes()

t_fade_in = 0.08   # 80ms smooth fade & pop
t_fade_out = 0.06  # 60ms smooth dissolution

for f_idx in range(TOTAL_FRAMES):
    t = f_idx / FPS
    
    # Find active phrase
    active_p = None
    for p in PHRASES:
        if p['start'] <= t < p['end']:
            active_p = p
            break
            
    if active_p is None:
        proc.stdin.write(empty_bytes)
        continue
        
    surf = SURFACES[active_p['id']]
    s_time = active_p['start']
    e_time = active_p['end']
    
    # Calculate smooth entrance / exit physics
    alpha = 1.0
    scale = 1.0
    dy = 0
    
    if t - s_time < t_fade_in:
        progress = max(0.0, min(1.0, (t - s_time) / t_fade_in))
        ease = 1.0 - (1.0 - progress)**2
        alpha = ease
        scale = 0.95 + 0.05 * ease
        dy = int((1.0 - ease) * 6)
    elif e_time - t < t_fade_out:
        progress = max(0.0, min(1.0, (e_time - t) / t_fade_out))
        alpha = progress
        scale = 1.0
        dy = 0
        
    if alpha < 0.01:
        proc.stdin.write(empty_bytes)
        continue
        
    # Apply alpha + micro scale/drift
    frame_img = surf
    if scale != 1.0 or dy != 0 or alpha < 0.99:
        arr = np.array(surf, dtype=np.float32)
        if alpha < 0.99:
            arr[:, :, 3] = arr[:, :, 3] * alpha
        frame_img = Image.fromarray(arr.astype(np.uint8), 'RGBA')
        
        if scale != 1.0 or dy != 0:
            nw = int(W * scale)
            nh = int(H * scale)
            res = frame_img.resize((nw, nh), Image.Resampling.BILINEAR)
            
            canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            paste_x = (W - nw) // 2
            paste_y = (H - nh) // 2 - dy
            canvas.paste(res, (paste_x, paste_y))
            frame_img = canvas
            
    proc.stdin.write(frame_img.tobytes())

proc.stdin.close()
proc.wait()
print(f"Overlay video generated successfully in {OVERLAY_MOV}!")

# Composite with Dynamic Camera Punch-In Cuts & Tone-Matched Color Grade
print("Building Final Composite with Camera Punch-Ins and Tone-Matched Color Grade...")

# 8 Zoom Cut Segments (1.00x vs 1.06x)
ZOOM_CUTS = [
    (0.00,  4.20,  1.00),   # Wide: Hook
    (4.20,  7.80,  1.06),   # Punch-in: Pivot / Question
    (7.80, 12.80,  1.00),   # Wide: Constitutional Power
    (12.80, 16.50, 1.06),   # Punch-in: Precedents
    (16.50, 20.30, 1.00),   # Wide: Transition
    (20.30, 25.50, 1.06),   # Punch-in: Evidence Contrast & Rafale
    (25.50, 30.00, 1.00),   # Wide: Street Tamasha
    (30.00, 36.52, 1.07),   # Punch-in: Climax / Verdict
]

vf_parts = []
concat_inputs = []

for idx, (s, e, z) in enumerate(ZOOM_CUTS):
    v_tag = f'v{idx}'
    concat_inputs.append(f'[{v_tag}]')
    if z > 1.00:
        # Scale and crop centered on upper-chest/face (y = 0.35)
        sw = int(1080 * z)
        # Ensure even numbers
        if sw % 2 != 0: sw += 1
        sh = int(1920 * z)
        if sh % 2 != 0: sh += 1
        crop_x = int((sw - 1080) * 0.5)
        crop_y = int((sh - 1920) * 0.35)
        vf_parts.append(f'[0:v]trim={s:.2f}:{e:.2f},setpts=PTS-STARTPTS,scale={sw}:{sh},crop=1080:1920:{crop_x}:{crop_y},setsar=1,format=yuv420p[{v_tag}]')
    else:
        vf_parts.append(f'[0:v]trim={s:.2f}:{e:.2f},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[{v_tag}]')

concat_str = ''.join(concat_inputs) + f'concat=n={len(ZOOM_CUTS)}:v=1:a=0'
color_grade = 'eq=contrast=1.05:brightness=-0.01:saturation=1.05:gamma=0.98,unsharp=5:5:0.4:5:5:0.0'
audio_master = 'highpass=f=80,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=9'

filtergraph = (
    ';'.join(vf_parts) + ';' +
    f'{concat_str},{color_grade}[v_base];' +
    '[v_base][1:v]overlay=0:0[v_final];' +
    f'[0:a]{audio_master}[a_final]'
)

cmd = [
    FFMPEG, '-y',
    '-i', RAW,
    '-i', OVERLAY_MOV,
    '-filter_complex', filtergraph,
    '-map', '[v_final]',
    '-map', '[a_final]',
    '-c:v', 'libx264',
    '-crf', '18',
    '-preset', 'fast',
    '-pix_fmt', 'yuv420p',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-movflags', '+faststart',
    FINAL_OUT
]

print("Executing final FFmpeg render...")
t0 = time.time()
res = subprocess.run(cmd, capture_output=True, text=True)
t1 = time.time()

if res.returncode != 0:
    print("FFmpeg Error:", res.stderr[-800:])
    sys.exit(1)
    
print(f"Master Video successfully rendered in {t1 - t0:.1f}s!")
print(f"Saved to: {FINAL_OUT}")
