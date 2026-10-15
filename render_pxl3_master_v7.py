#!/usr/bin/env python3
import os, sys, time, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RAW = '/Users/sanskarsaraf/Downloads/PXL_20261014_062026247.mp4'
if not os.path.exists(RAW):
    RAW = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit/raw_PXL_20261014_062026247.mp4'

FINAL_OUT = '/Users/sanskarsaraf/Downloads/PXL_20261014_062026247_EDITED.mp4'
FFMPEG = '/Users/sanskarsaraf/.gemini/antigravity/scratch/social.minpay.in/video_generator/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg'
WORK_DIR = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit'
CLEAN_SURF_DIR = f'{WORK_DIR}/chrome_surfaces_clean_v7'
SFX_DIR = f'{WORK_DIR}/sfx'
TEMP_VIDEO = f'{WORK_DIR}/temp_pxl3_v7_video.mp4'
TEMP_AUDIO = f'{WORK_DIR}/temp_pxl3_v7_audio.wav'

W, H = 1080, 1920
FPS = 30
TOTAL_DUR = 35.52
TOTAL_FRAMES = int(TOTAL_DUR * FPS)  # 1065 frames

print(f"🎬 Initiating V7 Master Render for PXL_20261014_062026247 ({TOTAL_DUR}s, {TOTAL_FRAMES} frames @ 30fps)...")

# 1. Preload Clean Base Surfaces (ZERO Baked Text)
print("\n[1/4] Pre-loading Clean Base Surfaces...")
SURF_S02 = Image.open(f'{CLEAN_SURF_DIR}/s02_clean_frame.png').convert('RGBA')
SURF_S04 = Image.open(f'{CLEAN_SURF_DIR}/s04_clean_card.png').convert('RGBA')
SURF_S05 = Image.open(f'{CLEAN_SURF_DIR}/s05_clean_trends.png').convert('RGBA')
SURF_S06 = Image.open(f'{CLEAN_SURF_DIR}/s06_clean_frame.png').convert('RGBA')

# Window Mask for Framed Insets (920x1300 with 36px radius)
mask_920_1300 = Image.new('L', (920, 1300), 0)
ImageDraw.Draw(mask_920_1300).rounded_rectangle([0, 0, 920, 1300], radius=36, fill=255)

canvas_studio = Image.new('RGB', (W, H), (7, 9, 14))

# Fonts
FONT_SUB = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 46, index=8)
FONT_HUGE = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 96, index=8)
FONT_MID = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 60, index=8)
FONT_REG = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 50, index=8)

# 2. Scene Breakdown (Acoustically Locked Transitions)
SCENES = [
    {'id': 's01', 'start': 0.00,  'end': 3.50,  'layout': 'full_bleed'},
    {'id': 's02', 'start': 3.50,  'end': 8.70,  'layout': 'framed_inset'},
    {'id': 's03', 'start': 8.70,  'end': 11.80, 'layout': 'full_bleed'},
    {'id': 's04', 'start': 11.80, 'end': 17.10, 'layout': 'data_disparity'},
    {'id': 's05', 'start': 17.10, 'end': 23.00, 'layout': 'pure_cutaway_x'},
    {'id': 's06', 'start': 23.00, 'end': 27.10, 'layout': 'framed_inset'},
    {'id': 's07', 'start': 27.10, 'end': 31.30, 'layout': 'full_bleed'},
    {'id': 's08', 'start': 31.30, 'end': 35.52, 'layout': 'monumental_climax'}
]

# 3. Micro-Chunk Dialogue Cues (Scenes 1 to 7)
CUES = [
    # Scene 1: Full-Bleed
    {'id': 'b01', 'start': 0.00, 'end': 1.84, 'text': 'Jis desh ne Mumbai pe', 'words': 4, 'accent': 'Mumbai', 'col': (255,255,255,255), 'cy': 1380},
    {'id': 'b02', 'start': 1.84, 'end': 3.50, 'text': '26/11 karwaya tha...', 'words': 3, 'accent': '26/11', 'col': (255,75,75,255), 'cy': 1380},
    
    # Scene 2: Framed Inset (docked in lower window safe slot cy=1630)
    {'id': 'b03', 'start': 3.50, 'end': 4.16, 'text': 'agar woh tumhare', 'words': 3, 'accent': None, 'col': (255,255,255,255), 'cy': 1630},
    {'id': 'b04', 'start': 4.16, 'end': 4.76, 'text': 'protest ke liye', 'words': 3, 'accent': None, 'col': (255,255,255,255), 'cy': 1630},
    {'id': 'b05', 'start': 4.76, 'end': 5.88, 'text': 'taaliyan baja raha hai,', 'words': 4, 'accent': 'taaliyan', 'col': (255,255,255,255), 'cy': 1630},
    {'id': 'b06', 'start': 5.88, 'end': 7.28, 'text': 'toh tum krantikari nahi,', 'words': 4, 'accent': 'krantikari', 'col': (52,211,153,255), 'cy': 1630},
    {'id': 'b07', 'start': 7.28, 'end': 8.70, 'text': 'unke puppet ho!', 'words': 3, 'accent': 'puppet', 'col': (255,75,75,255), 'cy': 1630},
    
    # Scene 3: Full-Bleed
    {'id': 'b08', 'start': 8.70, 'end': 9.90, 'text': 'Dushman desh kabhi', 'words': 3, 'accent': 'Dushman', 'col': (255,255,255,255), 'cy': 1380},
    {'id': 'b09', 'start': 9.90, 'end': 10.94, 'text': 'tumhari democracy ke liye', 'words': 4, 'accent': 'democracy', 'col': (255,255,255,255), 'cy': 1380},
    {'id': 'b10', 'start': 10.94, 'end': 11.80, 'text': 'dua nahi maangta.', 'words': 3, 'accent': 'nahi', 'col': (255,75,75,255), 'cy': 1380},
    
    # Scene 4: FT Data Disparity (cy=1480 below card)
    {'id': 'b11', 'start': 11.80, 'end': 12.96, 'text': 'Border pe woh humari', 'words': 4, 'accent': 'Border', 'col': (255,255,255,255), 'cy': 1480},
    {'id': 'b12', 'start': 12.96, 'end': 14.06, 'text': 'army se jeet nahi sakte,', 'words': 5, 'accent': 'army', 'col': (52,211,153,255), 'cy': 1480},
    {'id': 'b13', 'start': 14.06, 'end': 15.30, 'text': 'economic growth mein', 'words': 3, 'accent': 'growth', 'col': (52,211,153,255), 'cy': 1480},
    {'id': 'b14', 'start': 15.30, 'end': 16.22, 'text': 'woh humse muqabla', 'words': 3, 'accent': None, 'col': (255,255,255,255), 'cy': 1480},
    {'id': 'b15', 'start': 16.22, 'end': 17.10, 'text': 'kar nahi sakte,', 'words': 3, 'accent': 'nahi', 'col': (255,75,75,255), 'cy': 1480},
    
    # Scene 5: Authentic X Trends (cy=1480 below trends stack)
    {'id': 'b16', 'start': 17.10, 'end': 18.16, 'text': 'isliye jaise hi', 'words': 3, 'accent': None, 'col': (255,255,255,255), 'cy': 1480},
    {'id': 'b17', 'start': 18.16, 'end': 18.82, 'text': 'Delhi mein sadkein', 'words': 3, 'accent': 'Delhi', 'col': (255,255,255,255), 'cy': 1480},
    {'id': 'b18', 'start': 18.82, 'end': 19.40, 'text': 'band hoti hain,', 'words': 3, 'accent': 'band', 'col': (255,75,75,255), 'cy': 1480},
    {'id': 'b19', 'start': 19.40, 'end': 20.24, 'text': 'unke bot farms', 'words': 3, 'accent': 'bot', 'col': (255,255,255,255), 'cy': 1480},
    {'id': 'b20', 'start': 20.24, 'end': 21.04, 'text': 'tumhare hashtags', 'words': 2, 'accent': 'hashtags', 'col': (0,229,255,255), 'cy': 1480},
    {'id': 'b21', 'start': 21.04, 'end': 23.00, 'text': 'trend karwane lagte hain!', 'words': 4, 'accent': 'trend', 'col': (0,229,255,255), 'cy': 1480},
    
    # Scene 6: Framed Inset (docked in lower window safe slot cy=1630)
    {'id': 'b22', 'start': 23.00, 'end': 25.14, 'text': 'Critique any government', 'words': 3, 'accent': 'Critique', 'col': (255,255,255,255), 'cy': 1630},
    {'id': 'b23', 'start': 25.14, 'end': 25.70, 'text': 'you want,', 'words': 2, 'accent': None, 'col': (255,255,255,255), 'cy': 1630},
    {'id': 'b24', 'start': 25.70, 'end': 27.10, 'text': 'that is your right.', 'words': 4, 'accent': 'right', 'col': (52,211,153,255), 'cy': 1630},
    
    # Scene 7: Full-Bleed
    {'id': 'b25', 'start': 27.10, 'end': 28.30, 'text': 'Lekin jis din', 'words': 3, 'accent': None, 'col': (255,255,255,255), 'cy': 1380},
    {'id': 'b26', 'start': 28.30, 'end': 29.48, 'text': 'tumhara protest', 'words': 2, 'accent': 'protest', 'col': (255,255,255,255), 'cy': 1380},
    {'id': 'b27', 'start': 29.48, 'end': 30.22, 'text': 'dushman desh ka', 'words': 3, 'accent': 'dushman', 'col': (255,255,255,255), 'cy': 1380},
    {'id': 'b28', 'start': 30.22, 'end': 31.30, 'text': 'weapon ban jaye...', 'words': 3, 'accent': 'weapon', 'col': (255,75,75,255), 'cy': 1380}
]

# Pre-render PIL subtitle pill overlays for each cue for instant compositing
print("Pre-rendering pristine subtitle pill textures...")
PILL_SURFACES = {}
for c in CUES:
    cid = c['id']
    text = c['text']
    accent = c['accent']
    accent_col = c['col']
    cy = c['cy']
    
    words = text.split()
    temp_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(temp_img)
    
    word_widths = []
    space_w = d.textbbox((0,0), ' ', font=FONT_SUB)[2]
    total_w = 0
    for w in words:
        wb = d.textbbox((0,0), w, font=FONT_SUB)
        ww = wb[2] - wb[0]
        word_widths.append(ww)
        total_w += ww
    total_w += space_w * (len(words) - 1)
    
    th = 50
    pad_x, pad_y = 36, 16
    cw = total_w + pad_x * 2
    ch = th + pad_y * 2
    
    x0 = (W - cw) // 2
    y0 = cy - ch // 2
    x1 = x0 + cw
    y1 = y0 + ch
    
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle([x0, y0+8, x1, y1+8], radius=22, fill=(0, 0, 0, 190))
    overlay = overlay.filter(ImageFilter.GaussianBlur(10))
    
    od2 = ImageDraw.Draw(overlay)
    od2.rounded_rectangle([x0, y0, x1, y1], radius=22, fill=(11, 14, 23, 225), outline=(255, 255, 255, 38), width=2)
    
    cur_x = x0 + pad_x
    cur_y = y0 + pad_y
    for i, w in enumerate(words):
        w_clean = w.strip('.,!?-').lower()
        acc_clean = accent.strip('.,!?-').lower() if accent else ''
        if accent and acc_clean in w_clean:
            col = accent_col
        else:
            col = (255, 255, 255, 255)
        od2.text((cur_x, cur_y), w, font=FONT_SUB, fill=col)
        cur_x += word_widths[i] + space_w
        
    PILL_SURFACES[cid] = overlay

# Pre-render Scene 8 Monumental Stages
S8_STAGES = {}

# Stage 1 (31.30s – 31.88s): "uss din tum"
s8_1 = Image.new('RGBA', (W, H), (4, 5, 8, 255))
cd = ImageDraw.Draw(s8_1)
b = cd.textbbox((0,0), "uss din tum", font=FONT_REG)
cd.text(((W-(b[2]-b[0]))//2, 900), "uss din tum", font=FONT_REG, fill=(200, 210, 225, 255))
S8_STAGES['stage1'] = s8_1

# Stage 2 (31.88s – 32.62s): "uss din tum deshbhakt nahi,"
s8_2 = Image.new('RGBA', (W, H), (4, 5, 8, 255))
cd = ImageDraw.Draw(s8_2)
b1 = cd.textbbox((0,0), "uss din tum", font=FONT_REG)
cd.text(((W-(b1[2]-b1[0]))//2, 850), "uss din tum", font=FONT_REG, fill=(160, 175, 195, 255))
b2 = cd.textbbox((0,0), "deshbhakt nahi,", font=FONT_MID)
cd.text(((W-(b2[2]-b2[0]))//2, 940), "deshbhakt nahi,", font=FONT_MID, fill=(255, 75, 75, 255))
S8_STAGES['stage2'] = s8_2

# Stage 3 (32.62s – 33.66s): "NATIONAL LIABILITY"
s8_3 = Image.new('RGBA', (W, H), (4, 5, 8, 255))
cd = ImageDraw.Draw(s8_3)
b1 = cd.textbbox((0,0), "NATIONAL", font=FONT_HUGE)
b2 = cd.textbbox((0,0), "LIABILITY", font=FONT_HUGE)
cd.text(((W-(b1[2]-b1[0]))//2, 820), "NATIONAL", font=FONT_HUGE, fill=(255, 75, 75, 255))
cd.text(((W-(b2[2]-b2[0]))//2, 930), "LIABILITY", font=FONT_HUGE, fill=(255, 75, 75, 255))
S8_STAGES['stage3'] = s8_3

# Stage 4 (33.66s – 35.52s): "NATIONAL LIABILITY BAN JAATE HO!"
s8_4 = Image.new('RGBA', (W, H), (4, 5, 8, 255))
cd = ImageDraw.Draw(s8_4)
b1 = cd.textbbox((0,0), "NATIONAL", font=FONT_HUGE)
b2 = cd.textbbox((0,0), "LIABILITY", font=FONT_HUGE)
b3 = cd.textbbox((0,0), "BAN JAATE HO!", font=FONT_MID)
cd.text(((W-(b1[2]-b1[0]))//2, 780), "NATIONAL", font=FONT_HUGE, fill=(255, 75, 75, 255))
cd.text(((W-(b2[2]-b2[0]))//2, 890), "LIABILITY", font=FONT_HUGE, fill=(255, 75, 75, 255))
cd.text(((W-(b3[2]-b3[0]))//2, 1040), "BAN JAATE HO!", font=FONT_MID, fill=(255, 255, 255, 255))
S8_STAGES['stage4'] = s8_4

def render_video_stream():
    t_start = time.time()
    print("\n[2/4] Compositing Video Stream via FFmpeg raw pipe (Zero Redundancy)...")
    
    cmd_in = [
        FFMPEG, '-y',
        '-ss', '0',
        '-t', str(TOTAL_DUR),
        '-i', RAW,
        '-vf', 'fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
        '-f', 'rawvideo',
        '-pix_fmt', 'rgb24',
        '-'
    ]
    proc_in = subprocess.Popen(cmd_in, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)
    
    cmd_out = [
        FFMPEG, '-y',
        '-f', 'rawvideo',
        '-pix_fmt', 'rgb24',
        '-s', f'{W}x{H}',
        '-r', str(FPS),
        '-i', '-',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '15',
        '-pix_fmt', 'yuv420p',
        TEMP_VIDEO
    ]
    proc_out = subprocess.Popen(cmd_out, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)
    
    frame_bytes_len = W * H * 3
    
    for f_idx in range(TOTAL_FRAMES):
        t = f_idx / FPS
        raw_bytes = proc_in.stdout.read(frame_bytes_len)
        if not raw_bytes or len(raw_bytes) < frame_bytes_len:
            cam_frame = Image.new('RGB', (W, H), (0, 0, 0))
        else:
            cam_frame = Image.frombytes('RGB', (W, H), raw_bytes)
            
        # Determine active scene
        active_s = None
        for s in SCENES:
            if s['start'] <= t < s['end']:
                active_s = s
                break
        if active_s is None:
            active_s = SCENES[-1]
            
        sid = active_s['id']
        layout = active_s['layout']
        s_start = active_s['start']
        s_end = active_s['end']
        s_dur = max(0.5, s_end - s_start)
        rel_t = t - s_start
        
        # 1. Base Layer Composition
        if layout == 'monumental_climax':
            # Scene 8 Climax
            if t < 31.88:
                comp = S8_STAGES['stage1']
            elif t < 32.62:
                comp = S8_STAGES['stage2']
            elif t < 33.66:
                comp = S8_STAGES['stage3']
            else:
                comp = S8_STAGES['stage4']
                
        elif layout == 'pure_cutaway_x':
            # Scene 5 X Trends: Subtle gentle Ken Burns float (1.000 -> 1.015)
            drift_scale = 1.0 + 0.015 * (rel_t / s_dur)
            dw = int(W * drift_scale)
            dh = int(H * drift_scale)
            s5_scaled = SURF_S05.resize((dw, dh), Image.Resampling.LANCZOS)
            dx = (W - dw) // 2
            dy = (H - dh) // 2
            comp = s5_scaled.crop((-dx, -dy, -dx + W, -dy + H))
            
        elif layout == 'framed_inset':
            base = canvas_studio.copy()
            # Crop speaker to 920:1300 aspect ratio
            crop_h = 1526
            crop_top = int((H - crop_h) * 0.26)
            cam_cropped = cam_frame.crop((0, crop_top, W, crop_top + crop_h)).resize((920, 1300), Image.Resampling.LANCZOS)
            
            # Smooth pull-back ease (first 280ms)
            if rel_t < 0.28:
                p_pull = rel_t / 0.28
                p_ease = 1.0 - (1.0 - p_pull)**3
                cur_w = int(960 - 40 * p_ease)
                cur_h = int(1350 - 50 * p_ease)
                cam_sized = cam_cropped.resize((cur_w, cur_h), Image.Resampling.LANCZOS)
                mask_sized = mask_920_1300.resize((cur_w, cur_h), Image.Resampling.LANCZOS)
                paste_x = (W - cur_w) // 2
                paste_y = 490 + (1300 - cur_h) // 2
                base.paste(cam_sized, (paste_x, paste_y), mask_sized)
            else:
                base.paste(cam_cropped, (80, 490), mask_920_1300)
                
            # Paste clean frame overlay (title + border ONLY)
            surf_frame = SURF_S02 if sid == 's02' else SURF_S06
            base.paste(surf_frame, (0, 0), surf_frame)
            comp = base
            
        elif layout == 'data_disparity':
            # Scene 4: Camera push-in + clean FT card
            zoom = 1.00 + 0.030 * (rel_t / s_dur)
            zw = int(W * zoom)
            zh = int(H * zoom)
            cam_zoomed = cam_frame.resize((zw, zh), Image.Resampling.LANCZOS)
            cx = (zw - W) // 2
            cy = int((zh - H) * 0.35)
            comp = cam_zoomed.crop((cx, cy, cx + W, cy + H))
            # Paste clean FT card
            comp.paste(SURF_S04, (0, 0), SURF_S04)
            
        else:
            # Full Bleed (S01, S03, S07)
            if sid == 's01':
                zoom = 1.00 + 0.045 * (rel_t / s_dur)
            elif sid == 's07':
                zoom = 1.00 + 0.080 * (rel_t / s_dur)
            else:
                zoom = 1.00 + 0.025 * (rel_t / s_dur)
                
            zw = int(W * zoom)
            zh = int(H * zoom)
            cam_zoomed = cam_frame.resize((zw, zh), Image.Resampling.LANCZOS)
            cx = (zw - W) // 2
            cy = int((zh - H) * 0.35)
            comp = cam_zoomed.crop((cx, cy, cx + W, cy + H))
            
        # 2. Dynamic Micro-Chunk Dialogue Subtitle (Scenes 1 to 7 ONLY)
        if layout != 'monumental_climax':
            active_cue = None
            for c in CUES:
                if c['start'] <= t < c['end']:
                    active_cue = c
                    break
            if active_cue is not None:
                pill = PILL_SURFACES[active_cue['id']]
                comp.paste(pill, (0, 0), pill)
                
        # Send frame to FFmpeg pipe
        proc_out.stdin.write(comp.convert('RGB').tobytes())
        
        if f_idx % 150 == 0 or f_idx == TOTAL_FRAMES - 1:
            fps_speed = (f_idx + 1) / max(0.1, time.time() - t_start)
            print(f"  Frame {f_idx+1:4d}/{TOTAL_FRAMES} ({t:5.2f}s) @ {fps_speed:4.1f} fps")
            
    proc_in.stdout.close()
    proc_in.wait()
    proc_out.stdin.close()
    proc_out.wait()
    print(f"✓ Video stream composited in {time.time()-t_start:.1f}s!")

def build_audio_and_mux():
    print("\n[3/4] Synthesizing Precision Audio Design & Micro-SFX...")
    
    # SFX timing:
    # S02 at 3.50s: subtle_pop / click (-22 dB)
    # S03 at 8.70s: micro_whoosh (-24 dB)
    # S04 at 11.80s: digital_click (-22 dB)
    # S05 at 17.10s: digital_click (-22 dB)
    # S06 at 23.00s: micro_whoosh (-24 dB)
    # S07 at 27.10s: subtle_pop (-26 dB)
    # S08 at 31.30s: sub_boom (-20 dB)
    
    filter_complex = (
        "[0:a]volume=1.0[voice];"
        f"[1:a]adelay=3500|3500,volume=0.35[sfx_s02];"
        f"[2:a]adelay=8700|8700,volume=0.30[sfx_s03];"
        f"[3:a]adelay=11800|11800,volume=0.35[sfx_s04];"
        f"[3:a]adelay=17100|17100,volume=0.35[sfx_s05];"
        f"[2:a]adelay=23000|23000,volume=0.30[sfx_s06];"
        f"[1:a]adelay=27100|27100,volume=0.25[sfx_s07];"
        f"[4:a]adelay=31300|31300,volume=0.45[sfx_s08];"
        "[voice][sfx_s02][sfx_s03][sfx_s04][sfx_s05][sfx_s06][sfx_s07][sfx_s08]amix=inputs=8:duration=first:dropout_transition=0,"
        "loudnorm=I=-14:TP=-1.5:LRA=7[out_a]"
    )
    
    cmd_audio = [
        FFMPEG, '-y',
        '-t', str(TOTAL_DUR),
        '-i', RAW,
        '-i', f'{SFX_DIR}/subtle_pop.wav',
        '-i', f'{SFX_DIR}/micro_whoosh.wav',
        '-i', f'{SFX_DIR}/digital_click.wav',
        '-i', f'{SFX_DIR}/sub_boom.wav',
        '-filter_complex', filter_complex,
        '-map', '[out_a]',
        TEMP_AUDIO
    ]
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✓ Audio design synthesized and loudness normalized to -14 LUFS!")
    
    print("\n[4/4] Muxing Video & Audio into Master Deliverable...")
    cmd_mux = [
        FFMPEG, '-y',
        '-i', TEMP_VIDEO,
        '-i', TEMP_AUDIO,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-movflags', '+faststart',
        FINAL_OUT
    ]
    subprocess.run(cmd_mux, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Cleanup temp
    if os.path.exists(TEMP_VIDEO):
        os.remove(TEMP_VIDEO)
    if os.path.exists(TEMP_AUDIO):
        os.remove(TEMP_AUDIO)
        
    print(f"\n🎉 MASTER DELIVERABLE READY: {FINAL_OUT}")
    sz = os.path.getsize(FINAL_OUT)
    print(f"   Size: {sz:,} bytes ({sz/1024/1024:.2f} MB)")

if __name__ == '__main__':
    render_video_stream()
    build_audio_and_mux()
