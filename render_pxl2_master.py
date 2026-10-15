#!/usr/bin/env python3
import os, sys, time, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RAW = '/Users/sanskarsaraf/Downloads/PXL_20261013_060947291~2.mp4'
FINAL_OUT = '/Users/sanskarsaraf/Downloads/PXL_20261013_060947291~2_EDITED.mp4'
FFMPEG = '/Users/sanskarsaraf/.gemini/antigravity/scratch/social.minpay.in/video_generator/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg'
WORK_DIR = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit'
SFX_DIR = f'{WORK_DIR}/sfx'

W, H = 1080, 1920
W2, H2 = 2160, 3840  # 4K UHD 2x supersampling canvas
FPS = 30
TOTAL_DUR = 32.93
TOTAL_FRAMES = int(TOTAL_DUR * FPS) + 1

# Fonts at 2x supersampling scale
F_SANS_BOLD = lambda sz: ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz * 2, index=0)
F_SANS_DEMI = lambda sz: ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz * 2, index=2)
F_SERIF_ITALIC = lambda sz: ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf', sz * 2)

C_WHITE = (255, 255, 255, 255)
C_GOLD = (255, 216, 77, 255)
C_MUTED = (200, 210, 225, 255)
C_RED = (255, 75, 75, 255)
C_STROKE = (6, 6, 9, 255)

# Narrative Phrases with word-level accuracy & zero collisions
PHRASES = [
    # 0: Hook (0.00 - 2.66s)
    {
        'id': 'b01',
        'start': 0.00, 'end': 1.44,
        'lines': [[('July mein', True), ('public', False)]]
    },
    {
        'id': 'b02',
        'start': 1.44, 'end': 2.66,
        'lines': [[('inke saath', False), ('thi...', True)]]
    },
    # 1: The Turn (2.66 - 4.30s)
    {
        'id': 'b03',
        'start': 2.66, 'end': 4.30,
        'lines': [
            [('lekin October mein jab', False)],
            [('police ne', True), ('uthaya,', False)]
        ]
    },
    # 2: Viral Trending Hashtag (4.30 - 7.50s) - Clean X Card on Lower Torso
    {
        'id': 'b04',
        'start': 4.30, 'end': 7.50,
        'lines': [
            [('toh Delhi ne', False), ('trend karwaya', True)]
        ],
        'motion_graphic': {
            'type': 'x_trending',
            'tag': '#ThankYouDelhiPolice',
            'sub': '152.4K Posts • Citizen Law & Order'
        }
    },
    # 3: Daily Commute Reality (7.70 - 12.08s) - Clean Caption Focus (Remarks Removed)
    {
        'id': 'b05',
        'start': 7.70, 'end': 9.14,
        'lines': [[('kyun', False), ('pata hai?', True)]]
    },
    {
        'id': 'b06',
        'start': 9.14, 'end': 10.50,
        'lines': [[('kyunki aam', False), ('Delhi walon ko', True)]]
    },
    {
        'id': 'b07',
        'start': 10.50, 'end': 12.08,
        # Wrapped into 2 balanced lines to eliminate left-edge cutoff
        'lines': [
            [('subah kaam pe', False)],
            [('nikalna hota hai.', True)]
        ]
    },
    # 4: Traffic & Metro Gridlock (12.08 - 17.50s) - Editorial Newspaper Clipping Popout
    {
        'id': 'b08',
        'start': 12.08, 'end': 14.56,
        'lines': [
            [('har 2 mahine mein', False)],
            [('50 metro station', 'red'), ('band karwaoge,', False)]
        ],
        'motion_graphic': {
            'type': 'newspaper_clipping',
            'headline': '"50 Metro Stations Shut Down Across Capital"',
            'sub': 'Commuters left stranded amid widespread transit gridlock.'
        }
    },
    {
        'id': 'b09',
        'start': 14.56, 'end': 15.92,
        'lines': [[('traffic choke', 'red'), ('karoge toh', False)]]
    },
    {
        'id': 'b10',
        'start': 15.92, 'end': 17.80,
        'lines': [[('log taaliyan', False), ('thodi bajayenge!', True)]]
    },
    # 5: Flight Contrast (18.10 - 20.64s)
    {
        'id': 'b11',
        'start': 18.10, 'end': 20.64,
        'lines': [
            [('flight se utha rahe the toh', False)],
            [('co-passengers', True), ('hass rahe the.', False)]
        ]
    },
    # 6: Emergency Reels vs Chennai Chill (21.20 - 28.50s) - Clean Dialogue Focus (Remarks Removed)
    {
        'id': 'b12',
        'start': 21.20, 'end': 24.50,
        'lines': [
            [('aur jab bus mein bitha ke', False)],
            [('emergency reels', 'red'), ('bana rahe the,', False)]
        ]
    },
    {
        'id': 'b13',
        'start': 24.50, 'end': 28.50,
        'lines': [
            [('tab Rahul Gandhi', True), ('Chennai mein', False)],
            [('Vijay ke saath', False), ('chill kar raha tha.', True)]
        ]
    },
    # 7: The Verdict / Climax (28.70 - 32.80s) - ALL CAPS & Enlarged Climax Punch
    {
        'id': 'b14',
        'start': 28.70, 'end': 30.50,
        'lines': [[('aam janta', True), ('tumhare', False)]]
    },
    {
        'id': 'b15',
        'start': 30.50, 'end': 32.80,
        'climax_boost': True,
        'lines': [
            [('tamashon se', True)],
            [('PAK CHUKI HAI!', True)]
        ]
    }
]

def sanitize_text(text):
    if not isinstance(text, str):
        return text
    replacements = {
        '𝕏': 'X',
        '—': '-',
        '–': '-',
        '…': '...',
        '\u201c': '"',
        '\u201d': '"',
        '\u2018': "'",
        '\u2019': "'",
    }
    return text

def render_supersampled_surface(p):
    """Renders 4K UHD 2x surface with spacious uncompressed cards and natural lower-third captions"""
    surf2 = Image.new('RGBA', (W2, H2), (0, 0, 0, 0))
    f_sans = F_SANS_BOLD(80 if p.get('climax_boost') else 66)
    
    lines = p.get('lines', [])
    cx = W2 // 2
    mg = p.get('motion_graphic')
    
    # Natural Lower-Third Captions (Gives mid-torso huge, un-cramped breathing room)
    if mg and mg.get('type') == 'x_trending':
        base_cy = int(1660 * 2)  # Positioned lower to give spacious X card clearance
    elif len(lines) == 1:
        base_cy = int(1580 * 2)  # Single line lower third
    else:
        base_cy = int(1520 * 2)  # Two line lower third
        
    line_spacing = int(105 * 2 if p.get('climax_boost') else 94 * 2)
    
    # Mathematical Bounding Boundary for Subtitles Top Edge
    caption_top_bound = base_cy - int(65 * 2)
    MIN_CLEARANCE_PX = int(45 * 2)
    max_card_bottom = caption_top_bound - MIN_CLEARANCE_PX
    
    # 1. Motion Graphics Layer (Spacious, Elegant, Uncompressed)
    if mg:
        mtype = mg['type']
        
        # A. Authentic Twitter/X Trending Card (Spacious, Below Gestures, Vector X)
        if mtype == 'x_trending':
            f_label = F_SANS_DEMI(22)
            f_htag = F_SANS_BOLD(46)
            f_sub = F_SANS_DEMI(22)
            
            tag_text = sanitize_text(mg['tag'])
            sub_text = sanitize_text(mg['sub'])
            
            draw = ImageDraw.Draw(surf2)
            tw_htag = draw.textlength(tag_text, font=f_htag)
            bw = int(tw_htag + 200)
            bh = int(128 * 2)  # 256px tall - generous padding, zero crampedness
            bx = (W2 - bw) // 2
            by = int(1390 * 2) # Anchored safely below gesturing hand
            
            if by + bh > max_card_bottom:
                by = max_card_bottom - bh
                
            card_sh = Image.new('RGBA', (W2, H2), (0, 0, 0, 0))
            cdraw_sh = ImageDraw.Draw(card_sh)
            cdraw_sh.rounded_rectangle([bx, by, bx + bw, by + bh], radius=34, fill=(0, 0, 0, 240))
            surf2.alpha_composite(card_sh.filter(ImageFilter.GaussianBlur(28)))
            
            cdraw = ImageDraw.Draw(surf2)
            cdraw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=34, fill=(12, 16, 24, 242), outline=(51, 65, 85, 240), width=4)
            
            # Header row
            cdraw.text((bx + 48, by + 30), "TRENDING ON X • INDIA", font=f_label, fill=(56, 189, 248, 255))
            
            # Geometric Vector X logo
            xi_cx = bx + bw - 64
            xi_cy = by + 42
            r = 18
            cdraw.line([(xi_cx - r, xi_cy - r), (xi_cx + r, xi_cy + r)], fill=(255, 255, 255, 240), width=5)
            cdraw.line([(xi_cx + r, xi_cy - r), (xi_cx - r, xi_cy + r)], fill=(255, 255, 255, 240), width=5)
            
            # Hashtag & Subtitle with luxurious breathing room
            cdraw.text((bx + 48, by + 88), tag_text, font=f_htag, fill=C_WHITE)
            cdraw.text((bx + 48, by + 184), sub_text, font=f_sub, fill=(148, 163, 184, 255))

        # B. Authentic Editorial Newspaper Transit Alert (Roomy, High-End Print Aesthetic)
        elif mtype == 'newspaper_clipping':
            f_mast = F_SANS_DEMI(18)
            f_head = ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf', 52)
            f_sub = F_SANS_DEMI(20)
            
            bw, bh = 1560, 270  # Large, roomy card (780x135 at 1x)
            bx = (W2 - bw) // 2
            by = int(1190 * 2)  # Sits below collar, leaves > 150px gap before captions
            
            if by + bh > max_card_bottom:
                by = max_card_bottom - bh
                
            card = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
            cdraw = ImageDraw.Draw(card)
            
            cdraw.rounded_rectangle([0, 0, bw, bh], radius=28, fill=(247, 244, 238, 255), outline=(214, 207, 194, 255), width=4)
            cdraw.text((44, 24), 'THE CAPITAL DISPATCH • SPECIAL TRANSIT ALERT', font=f_mast, fill=(115, 115, 115, 255))
            rep_txt = 'BREAKING REPORT'
            tw_rep = cdraw.textlength(rep_txt, font=f_mast)
            cdraw.text((bw - int(tw_rep) - 44, 24), rep_txt, font=f_mast, fill=(220, 38, 38, 255))
            cdraw.line([(36, 68), (bw - 36, 68)], fill=(180, 175, 168, 180), width=2)
            
            headline = sanitize_text(mg['headline'])
            subdeck = sanitize_text(mg['sub'])
            cdraw.text((44, 92), headline, font=f_head, fill=(28, 25, 23, 255))
            cdraw.text((44, 185), subdeck, font=f_sub, fill=(87, 83, 78, 255))
            
            card_rot = card.rotate(0.8, resample=Image.Resampling.BICUBIC, expand=True)
            rx = (W2 - card_rot.width) // 2
            ry = by
            
            sh = Image.new('RGBA', (W2, H2), (0, 0, 0, 0))
            sh.paste(Image.new('RGBA', card_rot.size, (0, 0, 0, 220)), (rx, ry + 16), card_rot)
            surf2.alpha_composite(sh.filter(ImageFilter.GaussianBlur(28)))
            surf2.paste(card_rot, (rx, ry), card_rot)

    # 2. Standard Body Captions (Natural Lower-Third Margin Zone)
    # (base_cy, line_spacing, lines, and cx already initialized above)
    
    # Auto-scale font if width exceeds 82% of screen
    draw_test = ImageDraw.Draw(surf2)
    max_line_w = 0
    space_w = draw_test.textlength(' ', font=f_sans)
    for line in lines:
        w_l = sum(draw_test.textlength(w, font=f_sans) for w, _ in line) + space_w * (len(line) - 1)
        if w_l > max_line_w:
            max_line_w = w_l
            
    if max_line_w > 0.82 * W2:
        scale_ratio = (0.82 * W2) / max_line_w
        base_sz = 80 if p.get('climax_boost') else 66
        f_sans = F_SANS_BOLD(int(base_sz * scale_ratio))
    
    for l_idx, line in enumerate(lines):
        curr_cy = base_cy + l_idx * line_spacing
        
        draw = ImageDraw.Draw(surf2)
        space_w = draw.textlength(' ', font=f_sans)
        total_w = sum(draw.textlength(w, font=f_sans) for w, _ in line) + space_w * (len(line) - 1)
        curr_x = cx - total_w // 2
        
        # Outer ambient shadow
        sh_ambient = Image.new('RGBA', (W2, H2), (0, 0, 0, 0))
        sdraw_a = ImageDraw.Draw(sh_ambient)
        temp_x = curr_x
        for w, _ in line:
            sdraw_a.text((temp_x, curr_cy + 10), w, font=f_sans, fill=(0, 0, 0, 240))
            temp_x += draw.textlength(w, font=f_sans) + space_w
        surf2.alpha_composite(sh_ambient.filter(ImageFilter.GaussianBlur(22)))
        
        # Inner tight shadow
        sh_tight = Image.new('RGBA', (W2, H2), (0, 0, 0, 0))
        sdraw_t = ImageDraw.Draw(sh_tight)
        temp_x = curr_x
        for w, _ in line:
            sdraw_t.text((temp_x, curr_cy + 4), w, font=f_sans, fill=(0, 0, 0, 255))
            temp_x += draw.textlength(w, font=f_sans) + space_w
        surf2.alpha_composite(sh_tight.filter(ImageFilter.GaussianBlur(6)))
        
        # Front text with micro-contour stroke
        draw = ImageDraw.Draw(surf2)
        temp_x = curr_x
        for w, is_emph in line:
            if is_emph is True or is_emph == 'gold':
                color = C_GOLD
            elif is_emph == 'red':
                color = C_RED
            else:
                color = C_WHITE
            draw.text((temp_x, curr_cy), w, font=f_sans, fill=color, stroke_width=5, stroke_fill=C_STROKE)
            temp_x += draw.textlength(w, font=f_sans) + space_w

    return surf2.resize((W, H), Image.Resampling.LANCZOS)

def build_zoom_expression():
    """Builds the exact mathematical per-frame smoothstep easing expression for FFmpeg zoompan"""
    kfs = [
        (0.0, 1.00),
        (3.2, 1.00),
        (3.7, 1.07),
        (7.5, 1.07),
        (8.0, 1.00),
        (11.8, 1.00),
        (12.3, 1.07),
        (17.5, 1.07),
        (18.0, 1.00),
        (21.0, 1.00),
        (21.6, 1.07),
        (28.5, 1.07),
        (29.2, 1.00),
        (29.5, 1.00),
        (30.1, 1.08),
        (TOTAL_DUR, 1.08)
    ]
    expr = str(kfs[-1][1])
    for i in range(len(kfs)-2, -1, -1):
        t1, z1 = kfs[i]
        t2, z2 = kfs[i+1]
        f1, f2 = int(t1 * FPS), int(t2 * FPS)
        dur_f = f2 - f1
        if z1 == z2:
            expr = f'if(between(on,{f1},{f2}),{z1:.3f},{expr})'
        else:
            u = f'((on-{f1})/{dur_f})'
            s = f'({u}*{u}*(3-2*{u}))'
            interp = f'({z1:.3f}+({z2-z1:.3f})*{s})'
            expr = f'if(between(on,{f1},{f2}),{interp},{expr})'
    return expr

def main():
    print("=" * 65)
    print("🎬 EDITORIAL REEL MASTER RENDER: PXL_20261013_060947291~2 (V5 FINAL)")
    print("=" * 65)
    t_start = time.time()
    
    # Step 1: Load Chrome-native exact HTML surfaces
    print("\n[1/3] Loading Chrome-native exact HTML graphic surfaces...")
    SURFACES = {}
    for p in PHRASES:
        png_path = f'{WORK_DIR}/chrome_surfaces/{p["id"]}.png'
        SURFACES[p['id']] = Image.open(png_path).convert('RGBA')
        print(f"  ✓ Loaded Chrome surface {p['id']}")
    print("All graphic surfaces loaded from exact HTML storyboard engine!")

    # Step 2: Stream animated overlay
    OVERLAY_MOV = f'{WORK_DIR}/pxl2_overlay_animated.mov'
    if os.path.exists(OVERLAY_MOV) and os.path.getsize(OVERLAY_MOV) > 100_000_000 and '--force-overlay' not in sys.argv:
        print(f"\n[2/3] Found existing valid overlay: {OVERLAY_MOV} ({os.path.getsize(OVERLAY_MOV)/(1024*1024):.1f} MB). Skipping re-stream!")
    else:
        print(f"\n[2/3] Streaming animated overlay to {OVERLAY_MOV}...")
        
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

        t_spring_in = 0.28   # 280ms spring overshoot entry (~8.4 frames)
        t_glide_out = 0.12   # 120ms smooth glide & fade exit (~3.6 frames)

        for f_idx in range(TOTAL_FRAMES):
            t = f_idx / FPS
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
            dur = max(0.4, e_time - s_time)
            
            alpha = 1.0
            scale = 1.0
            y_offset = 0.0
            
            # 1. Entry Phase: Spring Pop-Up with Elastic Overshoot
            if t < s_time + t_spring_in:
                p_in = max(0.0, min(1.0, (t - s_time) / t_spring_in))
                # Alpha: cubic ease-out over first 160ms
                p_alpha = min(1.0, (t - s_time) / 0.16)
                alpha = 1.0 - (1.0 - p_alpha) ** 3
                # Scale: 0.92 -> 1.025 peak -> 1.000 settled
                base_s = 0.92 + 0.08 * (1.0 - (1.0 - p_in) ** 2)
                overshoot = np.sin(p_in * np.pi) * 0.032
                scale = base_s + overshoot
                # Vertical translation: +45px (below) -> -4px (overshoot) -> 0px
                y_offset = 45.0 * ((1.0 - p_in) ** 2) - np.sin(p_in * np.pi) * 6.0
                
            # 2. Exit Phase: Eased Downward Glide & Dissolution
            elif t > e_time - t_glide_out:
                p_out = max(0.0, min(1.0, (e_time - t) / t_glide_out))
                alpha = p_out ** 1.8
                scale = 1.0
                y_offset = 24.0 * (1.0 - p_out)
                
            # 3. Idle Phase: Ambient Breathing Float & Subtle Micro-Drift
            else:
                elapsed = t - (s_time + t_spring_in)
                # Gentle vertical float (+/- 3.5px)
                y_offset = np.sin(elapsed * 2.2) * 3.5
                # Slow micro-scale breathing drift (1.000 -> 1.018)
                scale = 1.0 + 0.018 * min(1.0, elapsed / dur)
                alpha = 1.0
                
            if alpha < 0.01:
                proc.stdin.write(empty_bytes)
                continue
                
            frame_surf = surf
            if scale != 1.0 or abs(y_offset) > 0.5:
                scale_w = int(W * scale)
                scale_h = int(H * scale)
                scaled = surf.resize((scale_w, scale_h), Image.Resampling.LANCZOS)
                frame_surf = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                paste_x = (W - scale_w) // 2
                paste_y = (H - scale_h) // 2 + int(y_offset)
                frame_surf.paste(scaled, (paste_x, paste_y), scaled)
                
            if alpha < 0.99:
                r, g, b, a = frame_surf.split()
                a = a.point(lambda p: int(p * alpha))
                frame_surf = Image.merge('RGBA', (r, g, b, a))
                
            proc.stdin.write(frame_surf.tobytes())

        proc.stdin.close()
        proc.wait()
        print("✓ Animated overlay stream generated successfully!")

    # Step 3: Final Composite with Smooth Easing Zoom, Tone Grade, Micro-SFX & -14 LUFS Audio
    print("\n[3/3] Executing Final Master Render with Tactile Micro-SFX & Tone Grade...")
    zoom_expr = build_zoom_expression()
    
    sfx_whoosh = f'{SFX_DIR}/micro_whoosh.wav'
    sfx_pop = f'{SFX_DIR}/subtle_pop.wav'
    
    vf_chain = (
        f"zoompan=z='{zoom_expr}':x='iw/2-(iw/zoom/2)':y='ih*0.35-(ih/zoom*0.35)':d=1:s=1080x1920:fps=30,"
        f"eq=contrast=1.08:brightness=0.01:saturation=1.12,"
        f"unsharp=3:3:0.4:3:3:0.0[base];"
        f"[base][1:v]overlay=0:0[v]"
    )
    
    # 3 clean cues: X card at 4.30s, Newspaper clipping at 12.08s, and Climax impact at 30.50s
    af_chain = (
        f"[2:a]adelay=4300|4300,volume=0.22[s1];"
        f"[3:a]adelay=12080|12080,volume=0.22[s2];"
        f"[3:a]adelay=30500|30500,volume=0.25[s3];"
        f"[0:a][s1][s2][s3]amix=inputs=4:duration=first:dropout_transition=0,"
        f"loudnorm=I=-14:LRA=7:TP=-1.5[aout]"
    )
    
    cmd_final = [
        FFMPEG, '-y',
        '-i', RAW,
        '-i', OVERLAY_MOV,
        '-i', sfx_whoosh,
        '-i', sfx_pop,
        '-filter_complex', f'{vf_chain};{af_chain}',
        '-map', '[v]',
        '-map', '[aout]',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '15',
        '-deblock', '-1:-1',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        FINAL_OUT
    ]
    
    subprocess.run(cmd_final, check=True)
    dt = time.time() - t_start
    print(f"\n🎉 Master Video successfully rendered in {dt:.1f}s!")
    print(f"📁 Saved to: {FINAL_OUT}")

if __name__ == '__main__':
    main()
