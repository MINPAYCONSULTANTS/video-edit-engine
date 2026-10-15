#!/usr/bin/env python3
"""Remove dead air and add subtle alternating punch-in zooms, FFmpeg only.

Output is 1080x1920 (9:16), 30fps. Run this BEFORE transcribing so captions match the cut video.

Usage: python cut_silence.py in.mp4 cut.mp4 [--noise -32dB] [--min-silence 0.45]
                             [--pad 0.08] [--punch 1.06] [--crop-x 0.5]
--crop-x : horizontal face position for 16:9 sources, 0=left 1=right (0.5 = centre).
--punch  : zoom on every other segment (1.0 disables). Keep 1.04-1.08 for a premium feel.
"""
import argparse
import os
import re
import subprocess
import tempfile

ap = argparse.ArgumentParser()
ap.add_argument("inp")
ap.add_argument("out")
ap.add_argument("--noise", default="-32dB")
ap.add_argument("--min-silence", type=float, default=0.45)
ap.add_argument("--pad", type=float, default=0.08)
ap.add_argument("--punch", type=float, default=1.06)
ap.add_argument("--crop-x", type=float, default=0.5)
ap.add_argument("--fps", type=int, default=30)
a = ap.parse_args()

dur = float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.inp]).decode())
log = subprocess.run(
    ["ffmpeg", "-hide_banner", "-i", a.inp, "-af", f"silencedetect=n={a.noise}:d={a.min_silence}",
     "-f", "null", "-"], capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]

keep, cur = [], 0.0
for i, s in enumerate(starts):
    if s - cur > 0.15:
        keep.append((max(cur - a.pad, 0), min(s + a.pad, dur)))
    cur = ends[i] if i < len(ends) else dur
if dur - cur > 0.15:
    keep.append((max(cur - a.pad, 0), dur))
if not keep:
    keep = [(0, dur)]

vf, parts = [], []
for i, (s, e) in enumerate(keep):
    z = a.punch if (i % 2 == 1 and a.punch > 1) else 1.0
    base = "scale=1080:1920:force_original_aspect_ratio=increase"
    zoom = f",scale=iw*{z}:ih*{z}" if z > 1 else ""
    # crop AFTER scaling so the zoom stays centred on the chosen face position
    crop = f"crop=1080:1920:x='(iw-1080)*{a.crop_x}':y='(ih-1920)/2'"
    vf.append(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS,{base}{zoom},{crop},setsar=1,fps={a.fps},format=yuv420p[v{i}]")
    vf.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={max(e-s-0.02,0):.3f}:d=0.02[a{i}]")
    parts.append(f"[v{i}][a{i}]")
graph = ";".join(vf) + ";" + "".join(parts) + f"concat=n={len(keep)}:v=1:a=1[v][a]"

with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
    f.write(graph)
    script = f.name
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-i", a.inp, "-filter_complex_script", script,
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", a.out], check=True)
os.unlink(script)
kept = sum(e - s for s, e in keep)
print(f"{len(keep)} segments, {dur:.1f}s -> {kept:.1f}s")
