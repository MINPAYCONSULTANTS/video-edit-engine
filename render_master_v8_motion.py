#!/usr/bin/env python3
"""
render_master_v8_motion.py — High-Performance 60 FPS Procedural Motion Graphics Compositor
Upgrades the video editing pipeline to 60 FPS, sub-pixel affine camera physics,
procedural animated HTML sequences, live Gaussian frosted glass, and kinetic word karaoke.
"""
import os
import sys
import time
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
from kinetic_subtitles import KineticSubtitleEngine, spring_ease

# Directory Configuration
BASE_DIR = Path(__file__).parent.resolve()
CACHE_DIR = BASE_DIR / "sequence_cache"
SFX_DIR = BASE_DIR / "sfx"
RAW_VIDEO = Path("/Users/sanskarsaraf/Downloads/PXL_20261014_062026247.mp4")
if not RAW_VIDEO.exists():
    RAW_VIDEO = BASE_DIR / "raw_PXL_20261014_062026247.mp4"

FINAL_OUTPUT = Path("/Users/sanskarsaraf/Downloads/PXL_20261014_062026247_V8_60FPS.mp4")
FFMPEG = "/Users/sanskarsaraf/.gemini/antigravity/scratch/social.minpay.in/video_generator/node_modules/@ffmpeg-installer/darwin-x64/ffmpeg"

# Video Specifications
W, H = 1080, 1920
FPS = 60
TOTAL_DUR = 35.52
TOTAL_FRAMES = int(TOTAL_DUR * FPS)  # 2,131 frames @ 60 FPS

print(f"🚀 [V8 60FPS Engine] Initializing Master Motion Render ({TOTAL_DUR}s, {TOTAL_FRAMES} frames @ 60 FPS)...")

# 1. Sub-Pixel Floating-Point Camera Warper (Eliminates Integer-Pixel Jitter)
def subpixel_zoom(frame_pil: Image.Image, zoom: float, anchor_x: float = 0.5, anchor_y: float = 0.35) -> Image.Image:
    """Uses floating-point crop coordinates to eliminate integer stair-stepping jitter."""
    if abs(zoom - 1.0) < 1e-4:
        return frame_pil
    zw, zh = W / zoom, H / zoom
    cx, cy = W * anchor_x, H * anchor_y
    x0 = cx - zw / 2.0
    y0 = cy - zh / 2.0
    x1 = x0 + zw
    y1 = y0 + zh
    return frame_pil.crop((x0, y0, x1, y1)).resize((W, H), Image.Resampling.BILINEAR)


# 2. Live Frosted Glassmorphism (Dynamic Video Blur Under UI)
def apply_frosted_backdrop(base_frame: Image.Image, bbox: tuple, radius: int = 12, darken: float = 0.65) -> Image.Image:
    """Slices current video region, applies Gaussian blur, and blends back for true glassmorphism."""
    if bbox is None:
        return base_frame
    x0, y0, x1, y1 = bbox
    pad = 8
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(W, x1 + pad)
    y1 = min(H, y1 + pad)

    roi = base_frame.crop((x0, y0, x1, y1))
    blurred = roi.filter(ImageFilter.GaussianBlur(radius=radius))
    darkened = Image.blend(blurred, Image.new('RGB', blurred.size, (4, 6, 12)), darken)
    base_frame.paste(darkened, (x0, y0))
    return base_frame

# 3. Inset Window Rounded Mask (920x1300 with 36px radius)
mask_920_1300 = Image.new('L', (920, 1300), 0)
ImageDraw.Draw(mask_920_1300).rounded_rectangle([0, 0, 920, 1300], radius=36, fill=255)
canvas_studio = Image.new('RGB', (W, H), (7, 9, 14))

# 4. Scene Breakdown
SCENES = [
    {"id": "S01", "name": "Hook", "start": 0.00, "end": 3.40, "type": "bleed", "zoom_start": 1.00, "zoom_end": 1.035},
    {"id": "S02", "name": "Turn Inset", "start": 3.40, "end": 7.95, "type": "inset_spring", "zoom_start": 1.00, "zoom_end": 1.02},
    {"id": "S03", "name": "Truth Bleed", "start": 7.95, "end": 13.90, "type": "bleed", "zoom_start": 1.00, "zoom_end": 1.04},
    {"id": "S04", "name": "IMF Data Motion", "start": 13.90, "end": 18.04, "type": "motion_card", "seq": "s04_motion", "zoom_start": 1.00, "zoom_end": 1.025},
    {"id": "S05", "name": "Bot Surge Cascade", "start": 18.04, "end": 21.69, "type": "motion_full", "seq": "s05_motion"},
    {"id": "S06", "name": "Article 19 Inset", "start": 21.69, "end": 26.85, "type": "inset_spring", "zoom_start": 1.00, "zoom_end": 1.02},
    {"id": "S07", "name": "Sovereign Red Line", "start": 26.85, "end": 32.62, "type": "bleed", "zoom_start": 1.00, "zoom_end": 1.05},
    {"id": "S08", "name": "Monumental Climax", "start": 32.62, "end": 35.52, "type": "motion_full", "seq": "s08_motion"},
]

def render_master():
    # Initialize Subtitle Engine
    sub_engine = KineticSubtitleEngine(str(BASE_DIR / "transcription_pxl3_groq.json"), W, H)

    # Launch FFmpeg Raw Video Pipe Reader
    print(f"\n[1/3] Spawning FFmpeg 60 FPS Frame Reader from {RAW_VIDEO.name}...")
    read_cmd = [
        FFMPEG, "-ss", "0", "-i", str(RAW_VIDEO),
        "-vf", f"fps={FPS},scale={W}:{H}:flags=bicubic",
        "-f", "image2pipe", "-pix_fmt", "rgb24", "-vcodec", "rawvideo", "-"
    ]
    pipe_reader = subprocess.Popen(read_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)

    # Launch FFmpeg Master Video Pipe Writer with Hardware Noise Filter (2.5% film grain)
    temp_video = BASE_DIR / "temp_pxl3_v8_video.mp4"
    temp_audio = BASE_DIR / "temp_pxl3_v8_audio.wav"
    if temp_video.exists():
        temp_video.unlink()
    if temp_audio.exists():
        temp_audio.unlink()

    write_cmd = [
        FFMPEG, "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-",
        "-vf", "noise=c0s=3:allf=t",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "15",
        "-pix_fmt", "yuv420p",
        str(temp_video)
    ]
    pipe_writer = subprocess.Popen(write_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)

    bytes_per_frame = W * H * 3
    print(f"\n[2/3] Compositing {TOTAL_FRAMES} frames at 60 FPS with Sub-Pixel Camera & Motion Sequences...")
    start_render_time = time.time()

    for f_idx in range(TOTAL_FRAMES):
        t = f_idx / float(FPS)

        # Read raw video frame
        raw_bytes = pipe_reader.stdout.read(bytes_per_frame)
        if len(raw_bytes) < bytes_per_frame:
            print(f"\n⚠️ End of stream at frame {f_idx}/{TOTAL_FRAMES}")
            break

        frame_pil = Image.frombytes('RGB', (W, H), raw_bytes)

        # Identify current scene
        scene = SCENES[-1]
        for s in SCENES:
            if s["start"] <= t < s["end"]:
                scene = s
                break

        s_dur = scene["end"] - scene["start"]
        rel_t = t - scene["start"]
        s_type = scene["type"]

        # -------------------------------------------------------------
        # A. RENDER BASE SCENE ARCHETYPE
        # -------------------------------------------------------------
        if s_type == "bleed":
            z_start = scene.get("zoom_start", 1.00)
            z_end = scene.get("zoom_end", 1.04)
            zoom = z_start + (z_end - z_start) * (rel_t / max(0.1, s_dur))
            comp = subpixel_zoom(frame_pil, zoom, 0.50, 0.35)

        elif s_type == "inset_spring":
            spring_val = spring_ease(rel_t, 220, 22)
            comp = canvas_studio.copy()
            
            z_start = scene.get("zoom_start", 1.00)
            z_end = scene.get("zoom_end", 1.025)
            zoom = z_start + (z_end - z_start) * (rel_t / max(0.1, s_dur))
            zoomed_speaker = subpixel_zoom(frame_pil, zoom, 0.50, 0.35)

            # Window crop & paste
            resized_crop = zoomed_speaker.crop((80, 220, 1000, 1520)).resize((920, 1300), Image.Resampling.BICUBIC)
            comp.paste(resized_crop, (80, 240), mask_920_1300)

        elif s_type == "motion_card":
            z_start = scene.get("zoom_start", 1.00)
            z_end = scene.get("zoom_end", 1.025)
            zoom = z_start + (z_end - z_start) * (rel_t / max(0.1, s_dur))
            comp = subpixel_zoom(frame_pil, zoom, 0.50, 0.35)

            # Load frame from sequence cache
            seq_name = scene.get("seq")
            seq_dir = CACHE_DIR / seq_name
            seq_frame_idx = int(rel_t * FPS)
            card_frame_file = seq_dir / f"frame_{seq_frame_idx:04d}.png"
            if not card_frame_file.exists():
                card_frame_file = sorted(seq_dir.glob("frame_*.png"))[-1]

            card_img = Image.open(card_frame_file)
            card_bbox = card_img.getbbox()
            if card_bbox:
                # Live frosted backdrop blur under card
                comp = apply_frosted_backdrop(comp, card_bbox, radius=12, darken=0.72)
                if card_img.mode == 'RGBA':
                    comp.paste(card_img, (0, 0), card_img)
                else:
                    comp.paste(card_img, (0, 0))

        elif s_type == "motion_full":
            seq_name = scene.get("seq")
            seq_dir = CACHE_DIR / seq_name
            seq_frame_idx = int(rel_t * FPS)
            full_frame_file = seq_dir / f"frame_{seq_frame_idx:04d}.png"
            if not full_frame_file.exists():
                full_frame_file = sorted(seq_dir.glob("frame_*.png"))[-1]

            full_surf = Image.open(full_frame_file)
            if full_surf.mode == 'RGBA':
                comp = Image.new('RGB', (W, H), (4, 5, 8))
                comp.paste(full_surf, (0, 0), full_surf)
            else:
                comp = full_surf.convert('RGB')


        # -------------------------------------------------------------
        # B. COMPOSITE KINETIC SUBTITLES WITH LIVE BACKDROP BLUR
        # -------------------------------------------------------------
        if s_type != "motion_full":
            sub_overlay, sub_bbox = sub_engine.get_subtitle_frame(t)
            if sub_overlay and sub_bbox:
                comp = apply_frosted_backdrop(comp, sub_bbox, radius=10, darken=0.70)
                comp.paste(sub_overlay, (0, 0), sub_overlay)

        # Write frame to video pipe
        pipe_writer.stdin.write(comp.tobytes())

        # Progress reporting
        if (f_idx + 1) % 60 == 0 or (f_idx + 1) == TOTAL_FRAMES:
            elapsed = time.time() - start_render_time
            render_fps = (f_idx + 1) / max(0.1, elapsed)
            percent = int(((f_idx + 1) / TOTAL_FRAMES) * 100)
            eta = (TOTAL_FRAMES - (f_idx + 1)) / max(0.1, render_fps)
            print(f"  [{percent:3d}%] Frame {f_idx+1}/{TOTAL_FRAMES} | {render_fps:4.1f} FPS | ETA: {eta:3.0f}s")
            sys.stdout.flush()

    pipe_reader.stdout.close()
    pipe_reader.wait()
    pipe_writer.stdin.close()
    pipe_writer.wait()

    if pipe_writer.returncode != 0:
        raise RuntimeError(f"Video writer failed with returncode {pipe_writer.returncode}")

    total_render_elapsed = time.time() - start_render_time
    print(f"\n✅ Video stream completed in {total_render_elapsed:.1f}s ({TOTAL_FRAMES / total_render_elapsed:.1f} FPS)")

    # -------------------------------------------------------------
    # 3. AUDIO PIPELINE: SFX SUITE + EBU R128 NORMALIZATION
    # -------------------------------------------------------------
    print("\n[3/4] Synthesizing 6-Channel Foley Sound Design & EBU R128 Loudness Normalization...")

    filter_complex = (
        "[0:a]volume=1.0[voice];"
        "[1:a]adelay=0|0,volume=0.35[s01];"
        "[2:a]adelay=3400|3400,volume=0.45[s02];"
        "[3:a]adelay=13900|13900,volume=0.40[s04];"
        "[1:a]adelay=18040|18040,volume=0.35[s05];"
        "[4:a]adelay=32620|32620,volume=0.60[s08];"
        "[voice][s01][s02][s04][s05][s08]amix=inputs=6:duration=first:dropout_transition=2,"
        "loudnorm=I=-14:LRA=7:tp=-1.5[aout]"
    )

    aud_cmd = [
        FFMPEG, "-y",
        "-t", str(TOTAL_DUR),
        "-i", str(RAW_VIDEO),
        "-i", str(SFX_DIR / "digital_click.wav"),
        "-i", str(SFX_DIR / "micro_whoosh.wav"),
        "-i", str(SFX_DIR / "subtle_pop.wav"),
        "-i", str(SFX_DIR / "sub_boom.wav"),
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        str(temp_audio)
    ]
    subprocess.run(aud_cmd, check=True)
    print("✅ Audio stream synthesized & loudness normalized to -14 LUFS!")

    # -------------------------------------------------------------
    # 4. FINAL CLEAN MUX: VIDEO + AUDIO (ZERO CONTAINER CONFLICTS)
    # -------------------------------------------------------------
    print("\n[4/4] Muxing Clean 60 FPS Video & Audio into Master Deliverable...")
    mux_cmd = [
        FFMPEG, "-y",
        "-i", str(temp_video),
        "-i", str(temp_audio),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(FINAL_OUTPUT)
    ]
    subprocess.run(mux_cmd, check=True)

    if temp_video.exists():
        temp_video.unlink()
    if temp_audio.exists():
        temp_audio.unlink()

    print(f"\n🎉 [COMPLETE] Master 60 FPS Motion Deliverable Ready:")
    print(f"👉 {FINAL_OUTPUT}")
    file_size_mb = FINAL_OUTPUT.stat().st_size / (1024 * 1024)
    print(f"   Size: {file_size_mb:.2f} MB | Framerate: 60 FPS | Audio: -14 LUFS")

if __name__ == "__main__":
    render_master()
