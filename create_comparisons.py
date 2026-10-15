import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORK_DIR = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit'
RAW_DIR = f'{WORK_DIR}/comparison_output'
OUT_DIR = f'{WORK_DIR}/comparison_output'

# Fonts
F_SANS_BOLD = lambda sz: ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=0)
F_SANS_DEMI = lambda sz: ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=2)
F_SANS_MED = lambda sz: ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', sz, index=5)
F_SERIF_BOLD = lambda sz: ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf', sz)
F_SERIF_ITALIC = lambda sz: ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf', sz)

C_WHITE = (255, 255, 255, 255)
C_GOLD = (248, 210, 95, 255)       # Rich, warm champagne gold
C_MUTED = (220, 225, 235, 255)      # Bright clean silver
C_RED = (255, 65, 65, 255)

def draw_clean_text(base, cx, cy, text, font, fill=C_WHITE, stroke_w=2):
    """Draws text with a refined soft shadow + micro-contour for guaranteed legibility"""
    draw = ImageDraw.Draw(base)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx, ty = cx - tw // 2, cy - th // 2
    
    # 1. Subtle diffuse shadow pass (wide soft bloom)
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sh)
    sdraw.text((tx, ty + 4), text, font=font, fill=(0, 0, 0, 220))
    sdraw.text((tx, ty + 2), text, font=font, fill=(0, 0, 0, 250))
    sh_blur = sh.filter(ImageFilter.GaussianBlur(7))
    base.alpha_composite(sh_blur)
    
    # 2. Main text with refined micro-stroke (1.5px black) to guarantee pop on beige shirt folds
    draw = ImageDraw.Draw(base)
    draw.text((tx, ty), text, font=font, fill=fill, stroke_width=stroke_w, stroke_fill=(10, 10, 12, 230))
    return (tx, ty, tw, th)

def draw_phrase_words(base, cx, cy, words_list, font, stroke_w=2):
    """Draws words on a single line with individual word colors and natural spacing"""
    draw = ImageDraw.Draw(base)
    space_w = draw.textlength(' ', font=font)
    
    total_w = sum(draw.textlength(w, font=font) for w, c in words_list) + space_w * (len(words_list) - 1)
    curr_x = cx - total_w // 2
    
    # Shadow pass
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sh)
    temp_x = curr_x
    for w, c in words_list:
        sdraw.text((temp_x, cy + 4), w, font=font, fill=(0, 0, 0, 220))
        temp_x += draw.textlength(w, font=font) + space_w
    sh_blur = sh.filter(ImageFilter.GaussianBlur(7))
    base.alpha_composite(sh_blur)
    
    # Text pass with clean micro-stroke
    draw = ImageDraw.Draw(base)
    for w, c in words_list:
        draw.text((curr_x, cy), w, font=font, fill=c, stroke_width=stroke_w, stroke_fill=(10, 10, 12, 230))
        curr_x += draw.textlength(w, font=font) + space_w

# --- Scene 1: Hook ("evm hack ho gayi?") ---
raw1 = Image.open(f'{RAW_DIR}/raw_hook.jpg').convert('RGBA')
old1_ov = Image.open(f'{WORK_DIR}/prev8_HOOK_evm_hack.png').convert('RGBA')
old1 = Image.alpha_composite(raw1, old1_ov)

new1 = raw1.copy()
draw_phrase_words(new1, 540, 1370, [
    ('evm', C_WHITE),
    ('hack', C_GOLD),
    ('ho gayi?', C_WHITE)
], F_SANS_BOLD(56), stroke_w=2)

# --- Scene 2: Constitutional Precedent ("supreme court / constitutional power") ---
raw2 = Image.open(f'{RAW_DIR}/raw_sc_power.jpg').convert('RGBA')
old2_ov = Image.open(f'{WORK_DIR}/prev8_ARGUMENT_const_power.png').convert('RGBA')
old2 = Image.alpha_composite(raw2, old2_ov)

new2 = raw2.copy()
# Top Editorial Header (higher up at y=175 in clean wall space)
draw_clean_text(new2, 540, 170, 'Constitutional Power', F_SERIF_ITALIC(50), fill=C_GOLD, stroke_w=1)
draw_clean_text(new2, 540, 225, 'ARTICLE 32 & 142 • APEX JURISDICTION', F_SANS_DEMI(22), fill=C_MUTED, stroke_w=1)

# Spoken caption
draw_phrase_words(new2, 540, 1350, [
    ('supreme court', C_GOLD),
    ('ke paas', C_WHITE)
], F_SANS_BOLD(52), stroke_w=2)
draw_phrase_words(new2, 540, 1420, [
    ('poori', C_WHITE),
    ('power', C_GOLD),
    ('hai...', C_WHITE)
], F_SANS_BOLD(52), stroke_w=2)

# --- Scene 3: Evidence Contrast ("twitter threads vs affidavits") ---
raw3 = Image.open(f'{RAW_DIR}/raw_contrast.jpg').convert('RGBA')
old3_ov = Image.open(f'{WORK_DIR}/prev8_SHOUT_twitter_fixed.png').convert('RGBA')
old3 = Image.alpha_composite(raw3, old3_ov)

new3 = raw3.copy()
tx, ty, tw, th = draw_clean_text(new3, 540, 1340, 'twitter threads nahi', F_SANS_BOLD(52), fill=C_WHITE, stroke_w=2)
# Hairline strikethrough in red with micro black shadow
s_draw = ImageDraw.Draw(new3)
s_draw.line([tx - 10, 1340 + 2, tx + tw + 10, 1340 + 2], fill=(0, 0, 0, 200), width=5)
s_draw.line([tx - 8, 1340, tx + tw + 8, 1340], fill=C_RED, width=3)

# Line 2: sworn affidavits in rich gold
draw_clean_text(new3, 540, 1420, 'sworn affidavits lagte hain', F_SANS_BOLD(54), fill=C_GOLD, stroke_w=2)

def make_comparison_canvas(img_old, img_new, title):
    w, h = 810, 1440
    i_old = img_old.resize((w, h), Image.Resampling.LANCZOS)
    i_new = img_new.resize((w, h), Image.Resampling.LANCZOS)
    
    pad = 40
    header_h = 140
    canvas_w = w * 2 + pad * 3
    canvas_h = h + header_h + pad * 2
    
    canvas = Image.new('RGB', (canvas_w, canvas_h), (14, 17, 23))
    draw = ImageDraw.Draw(canvas)
    
    f_title = ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf', 36)
    f_badge = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 24, index=0)
    
    draw.text((pad, 40), title, font=f_title, fill=(255, 255, 255))
    
    # Left: OLD
    draw.rounded_rectangle([pad, 95, pad + 340, 135], radius=6, fill=(40, 20, 25), outline=(220, 70, 70), width=1)
    draw.text((pad + 16, 102), 'OLD: LOUD / ALL-CAPS / BOXES', font=f_badge, fill=(240, 100, 100))
    
    # Right: NEW
    x2 = pad * 2 + w
    draw.rounded_rectangle([x2, 95, x2 + 420, 135], radius=6, fill=(20, 35, 30), outline=(60, 200, 130), width=1)
    draw.text((x2 + 16, 102), 'NEW: MINIMALIST / REFERENCE STYLE', font=f_badge, fill=(80, 220, 150))
    
    canvas.paste(i_old.convert('RGB'), (pad, header_h + pad))
    canvas.paste(i_new.convert('RGB'), (x2, header_h + pad))
    return canvas

c1 = make_comparison_canvas(old1, new1, "HOOK MOMENT (01.2s) • Natural Lowercase vs All-Caps Screaming")
c1.save(f'{OUT_DIR}/compare_01_hook.jpg', quality=95)

c2 = make_comparison_canvas(old2, new2, "LEGAL PRECEDENT (08.2s) • Clean Top Serif Title vs Floating Box")
c2.save(f'{OUT_DIR}/compare_02_precedent.jpg', quality=95)

c3 = make_comparison_canvas(old3, new3, "EVIDENCE CONTRAST (20.8s) • Clean Strikethrough vs Orange Impact")
c3.save(f'{OUT_DIR}/compare_03_contrast.jpg', quality=95)

print("Comparisons updated and polished!")
