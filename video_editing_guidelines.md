---
name: talking-head-edit
description: Edit face-cam / talking-head videos into minimalist, premium-looking vertical (9:16) Reels/Shorts using 60 FPS procedural motion graphics, FFmpeg, Playwright, and Python - silence removal, sub-pixel floating-point camera zoom, acoustic-locked word-level micro-chunk captions with active karaoke pop, live video frosted glassmorphism, 2.5D tactile archival documents, macro financial velocity charts, 3D social avalanches, tactile micro-SFX, SIMD hardware film grain, mandatory HTML approval storyboard gate, and EBU R128 loudness-normalized audio. Use this skill whenever the user mentions editing a face cam video, talking head video, reel, short, captions, subtitles, motion graphics, or burning text onto a raw recording.
---

# Talking-Head Edit (60 FPS Procedural Motion Graphics & Editorial Standard)

Goal: Raw face-cam in, clean, high-craft 60 FPS vertical motion graphics out. **Restraint is the style.** 
Derived directly from real-world high-craft creator references and editorial documentary style (Vox, Johnny Harris, Bloomberg Originals).

---

## The 20 Iron Rules

### 1. The Sacred Face Rule (100% Off-Face Guarantee)
- **Face is Sacred:** The speaker's eyes, glasses, nose, mouth, beard, and facial expressions ($y \le 980\text{px}$ on 1080p, or $y \le 340\text{px}$ on mobile canvas) must **NEVER** have any text, boxes, or graphic elements rendered over them.
- **Lower-Torso Anchoring:** All motion graphic cards, badges, and citations must be strictly anchored to the **mid/lower torso on the shirt** ($y \ge 1200\text{px}$ on 1080p), providing $\ge 220\text{px}$ of clear breathing room below the chin.
- **No Hairline Boxes:** Never place floating pill boxes or text headers at the top of the frame ($y \le 250\text{px}$). They collide with hair, look like accidental watermarks, and get covered by Instagram's native top header.

### 2. Unified Sentence Continuity & Audio-Locked Transitions (Zero Pre-Mature Cuts)
- **Zero Pre-Mature Cuts:** A scene change or screen cut must **NEVER** occur mid-sentence or before the spoken clause has finished playing. Transitions must be locked strictly to acoustic pauses between sentences (`pause >= 0.25s`).
- **Zero Orphaned / Pre-Loaded Subtitles:** The text displayed on screen must strictly match the phrase being spoken. Never display clauses belonging to the next scene.
- Never slice a spoken sentence across a graphic card. Spoken subtitles must always remain a coherent, continuous phrase in the caption zone.

### 3. Shirt Luminance Contrast & Anti-Yellow Rule
- **Anti-Yellow Washout on Light Shirts:** When the speaker wears an off-white, light cream, beige, or light-colored shirt, **NEVER use pale or medium yellow (`#FFD84D`, `#F8D25F`)** for text or highlights. Yellow merges into the shirt's luminance and becomes illegible.
- **High-Contrast Color System over Light Shirts:**
  - **Crisp Pure White (`#FFFFFF`)**: With a frosted dark backing card (`bg-black/85 backdrop-blur-md px-5 py-2.5 rounded-2xl border border-white/10`) or dual Gaussian drop shadow ($\sigma=14$ tight, $\sigma=4$ sharp).
  - **Power Word Accents**: Use high-chroma **Restrained Crimson (`#FF4B4B`)**, **Vibrant Emerald (`#34D399`)**, or **Electric Cyan (`#00E5FF`)**, ensuring $\ge 7:1$ contrast against light apparel.
- **Auto-Margin Safe Enforcement:** Any line exceeding $82\%$ of screen width must be automatically wrapped into 2 lines or dynamically downscaled, guaranteeing $\ge 120\text{px}$ safe margins on left and right edges.

### 4. Mandatory HTML Storyboard Approval Gate (Two-Stage Workflow)
- **NEVER jump straight to a multi-minute master video render.**
- **Stage 1 — Interactive HTML Storyboard:**
  - Extract footage keyframes for every cut.
  - Generate a self-contained, interactive HTML approval artifact (`approval_storyboard.html`).
  - Feature: 9:16 phone simulator, Instagram Reels UI safe zones toggle, face protection verification boundary, scene-by-scene inspector, and audio transcript review.
- **Stage 2 — User Approval Gate:**
  - Present the storyboard to the user.
  - **Render the final master video ONLY after the user reviews and gives explicit approval.**

### 5. Programmatic Clearance Guard (Zero Caption Collision Guarantee)
- **Graphic Cards & Captions Must Never Collide:** A graphic card or badge must never intersect, overlap, or press against the subtitle lines below it.
- **Mathematical Bound:** Enforce `card_bottom <= caption_top - 60px` (at 1080p, or `- 120px` at 4K).
- **Safe Vertical Slot:** When a scene features 2-line subtitles (starting at $y \approx 1360\text{px}$ / $2720\text{px}$ 4K), graphic cards must use a compact horizontal profile ($\text{height} \le 90\text{px}$ at 1080p / $\le 180\text{px}$ at 4K) positioned at $y \approx 1160-1180\text{px}$ ($2320-2360\text{px}$ 4K), guaranteeing $> 120\text{px}$ of clear space above subtitles.

### 6. Vector Brand Icons & Glyph Sanitization (Anti-Tofu Rule)
- **Zero Raw Mathematical Unicode:** Never pass mathematical alphanumeric Unicode glyphs (e.g., `𝕏` `U+1D54F`), non-BMP symbols, or unsupported emoji into standard system fonts (`Avenir Next`, `Helvetica`, `Georgia`). They render as broken square boxes `[?]` ("tofu").
- **Vector Brand Marks:** Draw brand icons (like the X logo, checkmarks, warning triangles) using geometric vector lines (`ImageDraw.line` / vector polygons) or clean SVG/ASCII.
- **Mandatory Unicode Sanitizer:** Always sanitize input strings through a text cleaner (replacing curly quotes, em-dashes, and special symbols with clean standard ASCII) before PIL rendering.

### 7. Dynamic Layout Archetypes (Never 100% Locked Full-Bleed)
- A high-production reel must **NEVER** remain locked in a static full-bleed talking head from second 0 to the end.
- Every video must dynamically leverage multiple layout archetypes across key narrative beats:
  1. **Full-Bleed Push-In (Default)**: Continuous smoothstep cubic camera push-in centered on eyes (35% height) with lower-third kinetic text.
  2. **Framed Inset ("The Studio Gallery")**: The speaker camera smoothly pulls back into an elegant rounded window card ($920 \times 1300\text{px}$, $36\text{px}$ radius) on a clean studio canvas, with bold glowing title typography floating in the upper margin.
  3. **2.5D Tactile Archival Document**: Realistic 3D tilted document with paper texture, live yellow highlighter stroke, and red rubber stamp slam.
  4. **Macro Financial Velocity Graph**: Deep obsidian data canvas with animated glowing SVG trajectory lines and rolling counters.
  5. **3D Kinetic Social Avalanche**: Multi-layered 3D card swarm with verified badges and live rolling engagement tickers.
  6. **Monumental Typographic Slam**: High-contrast serif/sans editorial lockup with chromatic aberration impact.

### 8. Editorial Authenticity & Anti-Buzzword Standard
- **Article 19(1)(a)** is strictly **"Freedom of Speech and Expression"**. NEVER add cheap, fake tags like *"Constitutional Privilege"* or *"Protected"*.
- **Ban Fake Chapter Markers & Artificial Course Metadata**: NEVER add cheap tags like `"Chapter 01: The Agitation Paradox"`, `"Part 1"`, or artificial YouTube course numbers. If a title is needed above a Framed Inset window, use only the genuine core editorial question or factual topic (e.g. `Krantikari or Puppet?`), or genuine constitutional title (`Article 19(1)(a)`).
- **Ban Cheap Sloganeering & Sensationalist Tags**: NEVER slap tacky badges like *"Weaponized Dissent"*, *"Security Intelligence Record"*, *"Status: Compromised"*, or *"FINAL VERDICT"*. Let the script, facts, and delivery carry the power.

### 9. Framed Inset Density & Balanced Canvas Polish (Anti-Blank Canvas Rule)
- A Framed Inset window must **NEVER** look like an empty black void or a lonely box.
- **Embedded Speaker Footage**: The speaker camera footage MUST be dynamically scaled and framed inside the rounded inset window ($920 \times 1300\text{px}$, $36\text{px}$ radius) with subtle edge vignette and the subtitle card docked at the bottom of the window.
- The outer studio canvas must feature subtle, architectural dressing:
  - **Natural Studio Atmosphere**: Deep matte slate canvas (`#08090d`) with subtle contrast; zero blurry neon halos.
  - **Discreet Technical Framing**: Subtle corner registration marks (`+`), technical frame metadata (`[ 4K UHD • 24 FPS ]`). ZERO artificial chapter watermarks.
  - **Balanced Proportions**: Window should occupy 68–72% of screen height ($920 \times 1300\text{px}$ with $36\text{px}$ radius).

### 10. Authentic Editorial Hashtags (Anti-"AI JUNK" Social Standard)
- When depicting bot farms, troll networks, or trending hashtag hysteria:
- **BAN AI JUNK & CHEAP FAKE BADGES**: Absolutely NEVER add fake telemetry tags like `"BOT BURST"`, `"100/hr"`, `"VIRAL CLUSTER"`, `"PROXY ORIGIN"`, or robot emojis `🤖`.
- **BAN RAINBOW CANDY PILLS**: Never create a carnival of multi-colored rounded boxes (cyan + amber + fuchsia + emerald + rose).
- **Authentic Platform Vernacular**: Use the genuine visual vernacular of X (Twitter):
  - Stark, crisp, variable-scale typography (`#DelhiProtest`, `#VoteChori`, `#ChokeCapital`, `#DelhiShutdown`, `#EVMHack`).
  - Authentic platform metadata in muted cool slate (`#71767B`): e.g. `Trending in India • 248.4K posts`.
  - 3D multi-card cascade with real avatar badges and live rolling repost counters.

### 11. The Anti-"AI JUNK" & Editorial Craft Directive
- **No Text Glow Halos**: Never use diffuse neon text shadows (`drop-shadow-[0_0_35px_rgba(...)]`). High-end editorial style relies on typographic hierarchy, clean whitespace, and crisp kerning.
- **Financial Journalism Data Styling**: When showing economic or statistical comparisons, use the visual language of the Financial Times / Bloomberg / Vox (stark numbers, authentic source citations like `Source: IMF / World Bank`, clean hairline comparison bars, animated SVG velocity curves), rather than generic web app UI widgets.
- **Monochrome & Single Accent Restraint**: Limit the color palette to stark white (`#FFFFFF`), off-white (`#EDEDED`), slate-muted (`#71767B` / `#8A8F98`), and at most ONE intentional accent color (e.g. warm gold `#D4AF37`, vibrant emerald `#10B981`, or restrained crimson `#E02424`).

### 12. Micro-Chunk Caption Cadence (Max 4–5 Words Per Screen)
- **Hard Word Count Ceiling**: Captions on screen must **NEVER exceed 4 to 5 words** at any single moment. Never dump whole 8–12 word sentences or multi-line paragraphs onto the screen.
- **Target Cadence (2–4 Words Ideal)**: Display text in punchy, high-retention micro-bursts of **2 to 4 words** (maximum 5 words) that update in lockstep with the speaker's vocal tempo ($0.8\text{s} \text{ to } 1.4\text{s}$ per beat).
- **Why (Visual Velocity & Retention)**: In vertical Reels/Shorts, viewers scan fast. Long sentence blocks create cognitive fatigue, cover too much of the speaker's torso, and look static. Rapid micro-chunks maintain high visual energy and effortless readability.
- **Clean Single-Line Alignment**: With 2–4 words, captions naturally fit cleanly onto a **single horizontal line**, guaranteeing generous margins ($\ge 120\text{px}$ on sides) and zero collision with upper graphic cards (`Rule 5`).

### 13. Zero Text Redundancy & Anti-Duplicate Standard
- **Never Duplicate On-Screen Text**: A video frame must **NEVER display the exact same words twice** on screen (e.g. having a monumental header saying `"NATIONAL LIABILITY"` and simultaneously rendering a subtitle pill below it also saying `"NATIONAL LIABILITY"`).
- **Monumental Typography IS the Caption**: In pure typographic cutaways or climax screens, the bold editorial typography on screen *is* the spoken dialogue. Do not render a redundant secondary subtitle pill underneath it.
- **Strict Separation of Base Graphics & Subtitles**: Base graphic surfaces must **NEVER have dialogue subtitles pre-baked into their PNG images**. Subtitles must be rendered exclusively by the dynamic subtitle stream.

### 14. Minimalist & High-Signal HTML Storyboard Standard
- **Minimal, Distraction-Free Presentation**: Storyboards must follow clean, high-signal editorial design (Apple / Linear aesthetic). Remove all intrusive red dashed bounding boxes, warning borders, or fake phone notches that obscure the speaker's face.
- **100% Complete Screen Coverage**: Storyboards must display **every single scene and micro-chunk beat sequentially** with zero missing screens.
- **Clean Responsive Cards**: Each beat is presented as an unadorned 9:16 vertical preview card with its exact timestamp, word count badge ($\le 4\text{--}5\text{ words}$), and clean spoken phrase.

### 15. 60 FPS Procedural Motion Graphics Architecture (Never Static Flat PNGs)
- **Death to Static PNG Pasting**: Never take a single headless browser screenshot (`--screenshot`) of an HTML template and paste a static image onto video frames.
- **Deterministic Time Scrubbing API (`window.seekTo(t)`)**: Every HTML surface template must expose an exact, zero-latency JavaScript method: `window.seekTo(rel_t)` where `rel_t` is the scene elapsed time in seconds.
- **Physical Spring Dynamics & Easing Curves**:
  - **Critically Damped Springs**: Elements enter using physical spring math ($S(t) = 1 - e^{-\zeta \omega t}(\cos(\omega_d t) + \frac{\zeta}{\sqrt{1-\zeta^2}}\sin(\omega_d t))$) with $\zeta \approx 0.70\text{--}0.85$ and settling duration $\le 0.45\text{s}$.
  - **Rolling Numeric Counters**: Numbers must animate from 0 to target (e.g. `$0.00` to `$4.11T`) synchronized with the camera push ($0.2\text{s} - 1.25\text{s}$) with easing (`easeOutExpo` or cubic smoothstep).
  - **Dynamic Progress Bars & Gauges**: Bars must grow smoothly ($0\% \rightarrow 92\%$) alongside numbers.
  - **Staggered Spring Cascades**: Multi-element lists (like X trends #1 through #5) must stagger entry by $0.06\text{--}0.08\text{s}$ per row with physical elastic overshoot (`scale(1.04) \rightarrow scale(1.00)`).
  - **Kinetic Scale Slam**: Climax / monumental typography must slam into place (`1.15 \rightarrow 1.00`) with zero rebound for maximum impact.
- **Headless Frame Pump (`surface_frame_pump.py`)**: Use headless Playwright to seek and extract PNG frames at **60.0 FPS** directly into `sequence_cache/` for instant, frame-perfect streaming during final master composite.

### 16. 60 FPS Sub-Pixel Camera Mechanics & Anti-Jitter Standard
- **60.0 FPS Master Delivery Standard**: All master video deliveries must render and mux at **60.0 FPS** (never 30 FPS).
- **Sub-Pixel Floating-Point Cropping**: During slow camera pushes/zooms, integer pixel cropping (`int(x0), int(y0)`) causes visible stair-stepping and micro-jitter.
- All camera pans and zooms **MUST utilize floating-point sub-pixel coordinates** with bilinear or bicubic resampling:
  ```python
  def subpixel_zoom(frame_pil: Image.Image, zoom: float, anchor_x: float = 0.5, anchor_y: float = 0.35) -> Image.Image:
      if abs(zoom - 1.0) < 1e-4:
          return frame_pil
      zw, zh = W / zoom, H / zoom
      cx, cy = W * anchor_x, H * anchor_y
      x0 = cx - zw / 2.0
      y0 = cy - zh / 2.0
      return frame_pil.crop((x0, y0, x0 + zw, y0 + zh)).resize((W, H), Image.Resampling.BILINEAR)
  ```
- Guarantees completely buttery, analog camera motion identical to high-end NLEs (After Effects / DaVinci Resolve).

### 17. Live ROI Frosted Glassmorphism & Atmospheric Film Grain
- **True Video Frosted Glassmorphism**: Cards and subtitle pills must never be flat opaque grey boxes.
  - Dynamically crop the live video region under the element's bounding box:
  - Apply Gaussian blur ($\sigma = 10\text{--}12$).
  - Blend with deep obsidian slate (`#04060c` at $65\text{--}72\%$ opacity).
  - Composite the UI element on top.
- **Atmospheric Film Grain**: Use FFmpeg hardware SIMD video filter (`-vf noise=c0s=3:allf=t` at $2.5\text{--}3\%$) on the final composite pipe. This binds the 60 FPS camera, live video, and HTML graphic surfaces into a cohesive, non-digital documentary film texture without dropping CPU render performance.

### 18. Dynamic Spring-Morphing Subtitle Pills & Active Word Karaoke Pop
- **Spring-Morphing Container**: Subtitle pills must dynamically adjust their container dimensions based on active text length with spring smoothing.
- **Word-Level Active Karaoke Highlighting**:
  - The currently spoken active word pops up (`translateY(-2px)`) in high-contrast crisp pure white (`#FFFFFF`) or accent gold/crimson.
  - Inactive words in the active micro-chunk rest at $65\text{--}70\%$ soft slate opacity (`rgba(255, 255, 255, 0.68)`).
- **Automated Anti-Redundancy Muting**: The subtitle engine must automatically mute subtitle pills whenever a full-screen typographic cutaway (Monumental Climax) or dense social feed (Trending stack) is active (`Rule 13`).

### 19. Strict Acoustic-Locked Vocal Synchrony (Zero Caption Lag / Drift)
- **Zero Manual Timestamp Guessing**: Subtitle cues and word-level highlighting must **NEVER** be estimated or hardcoded to manual scene timings.
- **Direct Whisper Timestamp Derivation**: Subtitle engines must extract exact word start/end millisecond timestamps directly from Whisper/Groq transcription JSON (`words[i].start` and `words[i].end`).
- **Acoustic Breath Chunking**: Micro-chunks ($\le 4\text{--}5\text{ words}$) must be assembled by segmenting words at punctuation marks and natural breath pauses ($gap \ge 0.15\text{s}$).
- **Frame-Accurate Word Highlighting**: Active karaoke highlighting must evaluate `word.start <= t <= word.end` at every video frame ($60\text{ FPS} = 16.6\text{ms}$ resolution), guaranteeing zero latency between speaker lip movement, speech audio, and highlighted words.

### 20. 4 High-Craft Editorial Motion Archetypes (Beyond Flat Web UI Cards)
- **Archetype A — 2.5D Archival Document Dissection**: Aged parchment / newsprint paper, 3D perspective tilt (`rotateX`, `rotateY`), live animated yellow/gold highlighter stroke (`mix-blend-mode: multiply`) sweeping across cited evidence, and red rubber stamp slam (`CONFIDENTIAL / EXHIBIT`) with spring impact.
- **Archetype B — Macro Financial Velocity & Trajectory Graph**: FT / Bloomberg / Vox macro-economics aesthetic. Matte obsidian canvas, glowing emerald/rose SVG velocity curves, live rolling number counters (`$0.00T \rightarrow $4.11T`), dynamic progress bars, and coordinate metadata.
- **Archetype C — 3D Kinetic Social Avalanche**: Multi-layered 3D perspective card stack (`translateZ`, `rotateX`) with real X/Twitter post anatomy, verified badges, live incrementing engagement tickers, and depth of field blur.
- **Archetype D — Monumental Typographic Impact Lockup**: Dramatic editorial title sequences pairing high-contrast serifs with heavy sans-serifs, kinetic word slam ($1.25 \rightarrow 1.00$), and chromatic aberration impact.

---

## Complete 60 FPS Procedural Motion Pipeline Workflow

1. **Inspect Footage & Audio**:
   - Check resolution, native FPS, HDR/color transfer curve (`ffprobe`).
   - Extract audio and transcribe speech with word-level timestamps in clean Hinglish Roman script.
2. **Acoustic Micro-Chunk Assembly (Rule 19)**:
   - Group transcription into high-retention micro-chunks of **2 to 4 words** ($\le 5\text{ words}$ max) locked to exact Whisper millisecond timestamps.
3. **Select & Author Procedural Editorial Archetypes (Rule 20)**:
   - Choose from the 4 Editorial Motion Archetypes (2.5D Document, Financial Velocity, Social Avalanche, Monumental Typography).
   - Inject the deterministic `window.seekTo(t)` API with spring physics, rolling counters, and 3D perspective.
4. **Pre-Render Frame Sequences (Playwright Pump)**:
   - Run `surface_frame_pump.py` to pre-render dynamic surfaces at **60.0 FPS** into `sequence_cache/`.
5. **Interactive HTML Approval Storyboard**:
   - Compile `approval_storyboard.html` with minimalist design and present to the user.
   - Obtain user approval before starting final composite.
6. **Master 60 FPS Composite Render (`render_master_v8_motion.py`)**:
   - Stream raw video frames from FFmpeg reader pipe at 60 FPS.
   - Apply sub-pixel floating-point camera zoom curve.
   - Composite dynamic motion frame sequences from `sequence_cache/`.
   - Apply live ROI frosted glassmorphism and overlay spring-morphing kinetic subtitles with acoustic-locked karaoke pop.
   - Stream composite frames into FFmpeg writer pipe with hardware SIMD film grain (`noise=c0s=3:allf=t`).
7. **Audio Design & EBU R128 Loudness Normalization**:
   - Mix multi-channel Foley SFX suite (digital clicks, micro-whooshes, subtle pops, sub-boom) locked to scene transitions.
   - Synthesize to intermediate `temp_audio.wav` and normalize audio to **$-14\text{ LUFS}$** ($-1.5\text{ dBTP}$, AAC 192 kbps, 96 kHz).
8. **Clean 2-Stage Mux & Final Deliverable Verification**:
   - Mux `temp_video` + `temp_audio` directly without source HEVC container collisions.
   - Verify duration, 60.0 FPS framerate, stream integrity, and playback in QuickTime / AVFoundation.
