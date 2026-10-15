#!/usr/bin/env bash
# Final render: light grade + burned-in captions/overlays + loudness-normalised audio.
# Usage: scripts/render.sh cut.mp4 captions.ass final.mp4 [fontsdir]
# Input should already be 1080x1920 (from cut_silence.py).
set -euo pipefail

IN="$1"; ASS="$2"; OUT="$3"; FONTS="${4:-$(dirname "$0")/../assets/fonts}"

# Grade: gentle contrast + saturation, tiny sharpen. Keep it natural - premium = restraint.
GRADE="eq=contrast=1.04:saturation=1.06:gamma=1.0,unsharp=5:5:0.4:5:5:0.0"

# Audio: remove rumble, light compression, social loudness (-14 LUFS, -1.5 dBTP).
AUDIO="highpass=f=80,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=9"

ffmpeg -y -hide_banner -i "$IN" \
  -vf "${GRADE},subtitles='${ASS}':fontsdir='${FONTS}'" \
  -af "$AUDIO" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k -movflags +faststart "$OUT"

echo "done -> $OUT"
