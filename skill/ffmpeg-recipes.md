# FFmpeg recipes (minimalist extras)

## Contents
1. Fast draft render
2. 16:9 source with blurred background (no crop)
3. Thin progress bar
4. Simple end card
5. Background music under voice
6. Speed ramp on a filler section
7. B-roll / image cutaway
8. Thumbnail frame
9. Troubleshooting

## 1. Fast draft render (check timing/style in seconds)
```bash
ffmpeg -y -i cut.mp4 -vf "scale=540:960,subtitles=captions.ass:fontsdir=assets/fonts:original_size=1080x1920" \
  -c:v libx264 -crf 28 -preset ultrafast -c:a aac -b:a 96k draft.mp4
```

## 2. 16:9 source, keep full frame over a blurred background
```bash
ffmpeg -y -i in.mp4 -filter_complex \
"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:5,eq=brightness=-0.08[bg];\
 [0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:a copy wide.mp4
```
Use only when the speaker cannot be cropped to 9:16 without cutting off the frame.

## 3. Thin progress bar (3px, bottom, accent colour)
```bash
-vf "...,drawbox=x=0:y=ih-8:w='iw*t/DURATION':h=3:color=0xF5C84B@0.9:t=fill"
```
Replace DURATION with the video length in seconds. Keep it above the platform UI (move to `y=ih-330` if the platform bar collides).

## 4. Simple end card (2s, dark, centred text)
```bash
ffmpeg -y -f lavfi -i "color=c=0x0e0e12:s=1080x1920:d=2:r=30" -f lavfi -i "anullsrc=r=44100:cl=stereo" \
 -vf "drawtext=fontfile=assets/fonts/Inter-SemiBold.ttf:text='Follow for more':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2:alpha='if(lt(t,0.3),t/0.3,1)'" \
 -t 2 -c:v libx264 -pix_fmt yuv420p -c:a aac end.mp4
ffmpeg -y -i final.mp4 -i end.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" final_end.mp4
```
Only add an end card if the user asked; many reels look cleaner without one.

## 5. Background music under voice (only if asked)
```bash
ffmpeg -y -i final.mp4 -stream_loop -1 -i music.mp3 -filter_complex \
"[1:a]volume=0.18[m];[m][0:a]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck];\
 [0:a][duck]amix=inputs=2:duration=first:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac out.mp4
```
Use royalty-free or user-owned music only.

## 6. Speed ramp on a filler section (1.15x, subtle)
Keep speed changes <= 1.15x so the voice stays natural.
```bash
ffmpeg -y -i in.mp4 -filter_complex "[0:v]setpts=PTS/1.12[v];[0:a]atempo=1.12[a]" -map "[v]" -map "[a]" fast.mp4
```

## 7. B-roll / image cutaway (2s, with fade)
```bash
ffmpeg -y -i main.mp4 -loop 1 -t 2 -i broll.png -filter_complex \
"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuva420p,fade=t=in:st=0:d=0.2:alpha=1,fade=t=out:st=1.8:d=0.2:alpha=1,setpts=PTS+5/TB[b];\
 [0:v][b]overlay=enable='between(t,5,7)'[v]" -map "[v]" -map 0:a -c:a copy out.mp4
```
Here the cutaway appears from 5s to 7s. Keep the voice track running underneath.

## 8. Thumbnail frame
```bash
ffmpeg -ss 3.2 -i final.mp4 -frames:v 1 -q:v 2 thumb.jpg
```

## 9. Troubleshooting
- **Captions in wrong font**: font family name does not match; run `fc-scan assets/fonts/*.ttf | grep family` and pass `--font`.
- **Captions missing**: path with spaces/colons in the `subtitles=` filter; copy files to a simple path or escape it.
- **Audio/video drift after cut**: you transcribed the original, not `cut.mp4`. Re-run transcription on the cut file.
- **Concat error "Failed to configure output pad"**: segments differ in SAR/format; `cut_silence.py` already sets `setsar=1,format=yuv420p`.
- **Jump cuts feel choppy**: raise `--pad` to 0.12 and `--min-silence` to 0.6, or lower `--punch` to 1.04.
