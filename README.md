# Video Edit Engine (High-Craft Editorial & Vertical Video System)

A Python and FFmpeg-based vertical (9:16) video editing engine designed for talking-head reels, explainers, and political/documentary shorts. Inspired by the editorial craft of Vox and Johnny Harris, this engine prioritizes restraint, typographic hierarchy, and acoustic audio synchronization.

---

## Key Features

1. **Rule 12: Micro-Chunk Subtitle Cadence (Max 4–5 Words / Screen)**
   - Dialogue advances across rapid, high-retention 2–4 word bursts (maximum 5 words) synchronized with Whisper word timestamps ($0.8\text{s} - 1.4\text{s}$ duration).
   - Crisp white typography (`#FFFFFF`) on dark frosted backing cards (`bg-black/85 backdrop-blur-xl border border-white/10`) with zero low-contrast yellow over light clothing.

2. **Rule 13: Zero Text Redundancy & Anti-Duplicate Architecture**
   - Clean separation of base graphics and dialogue subtitles.
   - On monumental climax screens, large editorial typography *is* the spoken dialogue; no redundant secondary subtitle pills.
   - Base surfaces (Framed Inset canvases, comparison cards, social feeds) have zero hardcoded subtitle text, eliminating double-rendering.

3. **Dynamic Layout Archetypes (Never 100% Full-Bleed)**
   - **Full-Bleed Push-In**: Smooth cubic Hermite camera push-in centered on speaker's eyes.
   - **Framed Inset ("Studio Gallery")**: Speaker camera pulls back into an architectural rounded window card ($920 \times 1300\text{px}$, $36\text{px}$ radius) with editorial title typography floating above.
   - **Financial Journalism Data Styling**: Stark metric comparison bars (Bloomberg / Financial Times style) with authentic source citations.
   - **Authentic Social Feeds**: High-fidelity dark mode X (Twitter) trending stream with verified metrics, zero rainbow candy boxes, and zero fake telemetry tags.
   - **Monumental Climax**: Typographic impact on deep matte black with cinematic sub-boom.

4. **Tactile Micro-SFX & EBU R128 Audio Mastering**
   - Precision acoustic audio cuts aligned to natural pauses ($p \ge 0.25\text{s}$).
   - Micro-SFX suite: tactile mechanical clicks ($-22\text{ dB}$), subtle air whooshes ($-24\text{ dB}$), and cinematic sub-boom impacts ($-20\text{ dB}$).
   - Final audio loudness normalized to the social video standard of $-14\text{ LUFS}$ ($-1.5\text{ dBTP}$).

5. **Rule 14: Interactive HTML Approval Storyboard with "Suggest Edit"**
   - Distraction-free, minimal review gallery covering 100% of narrative beats.
   - Built-in **"Suggest Edit"** modal on every card allowing subtitle corrections, highlight word adjustments, and visual feedback notes.
   - One-click **"Copy All Feedback"** button to export feedback directly into markdown.

---

## Directory Structure

```
├── skill/
│   ├── SKILL.md                 # Master editorial specification & 14 Iron Rules
│   ├── caption-styles.md        # Typography palettes & placement rules
│   └── captions_*.ass           # Reference ASS subtitle presets
├── chrome_surfaces_clean_v7/    # Clean base graphic overlays (HTML & 1080x1920 PNGs)
│   ├── s02_clean_frame.html/.png
│   ├── s04_clean_card.html/.png
│   ├── s05_clean_trends.html/.png
│   ├── s06_clean_frame.html/.png
│   └── s08_clean_monumental.html/.png
├── sfx/                         # Tactile micro-SFX suite
│   ├── digital_click.wav
│   ├── micro_whoosh.wav
│   ├── sub_boom.wav
│   └── subtle_pop.wav
├── storyboard_clean_32/         # 32 keyframe verification frames (1080x1920)
├── approval_storyboard.html     # Interactive approval storyboard with Suggest Edit
├── render_pxl3_master_v7.py     # Master FFmpeg composite render pipeline
└── README.md                    # Engine documentation
```

---

## Quickstart

### Prerequisites
- Python 3.9+
- FFmpeg (with `libx264` and `loudnorm` filter)
- Google Chrome (for headless surface rendering)
- Pillow & NumPy

```bash
pip install pillow numpy
```

### 1. Generate Base Surfaces
```bash
python3 -c "from generate_surfaces import generate_all; generate_all()"
```

### 2. Launch Interactive Storyboard
Open `approval_storyboard.html` in any modern web browser to inspect frames and suggest edits.

### 3. Render Master Deliverable
```bash
python3 render_pxl3_master_v7.py
```
Outputs master deliverable at $1080 \times 1920$, 30 fps, CRF 15 with EBU R128 audio.

---

## License
Proprietary & Confidential · Minpay Media Systems
