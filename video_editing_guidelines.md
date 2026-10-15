---
name: talking-head-edit
description: Edit face-cam / talking-head videos into minimalist, premium-looking vertical (9:16) Reels/Shorts using 60 FPS procedural motion graphics, FFmpeg, Playwright, and Python - silence removal, sub-pixel floating-point camera zoom, Hinglish word-level micro-chunk captions with active karaoke pop, live video frosted glassmorphism, lower-torso procedural cards, tactile micro-SFX, SIMD hardware film grain, mandatory HTML approval storyboard gate, and EBU R128 loudness-normalized audio. Use this skill whenever the user mentions editing a face cam video, talking head video, reel, short, captions, subtitles, motion graphics, or burning text onto a raw recording.
---

# Talking-Head Edit (60 FPS Procedural Motion Graphics & Editorial Standard)

Goal: Raw face-cam in, clean, high-craft 60 FPS vertical motion graphics out. **Restraint is the style.** 
Derived directly from real-world high-craft creator references and editorial documentary style (Vox, Johnny Harris, Bloomberg Originals).

---

## The 18 Iron Rules

### 1. The Sacred Face Rule (100% Off-Face Guarantee)
- **Face is Sacred:** The speaker's eyes, glasses, nose, mouth, beard, and facial expressions ($y \le 980	ext{px}$ on 1080p, or $y \le 340	ext{px}$ on mobile canvas) must **NEVER** have any text, boxes, or graphic elements rendered over them.
- **Lower-Torso Anchoring:** All motion graphic cards, badges, and citations must be strictly anchored to the **mid/lower torso on the shirt** ($y \ge 1200	ext{px}$ on 1080p), providing $\ge 220	ext{px}$ of clear breathing room below the chin.
- **No Hairline Boxes:** Never place floating pill boxes or text headers at the top of the frame ($y \le 250	ext{px}$). They collide with hair, look like accidental watermarks, and get covered by Instagram's native top header.

### 2. Unified Sentence Continuity & Audio-Locked Transitions (Zero Pre-Mature Cuts)
- **Zero Pre-Mature Cuts:** A scene change or screen cut must **NEVER** occur mid-sentence or before the spoken clause has finished playing. Transitions must be locked strictly to acoustic pauses between sentences (`pause >= 0.25s`).
- **Zero Orphaned / Pre-Loaded Subtitles:** The text displayed on screen must strictly match the phrase being spoken. Never display clauses belonging to the next scene.
- Never slice a spoken sentence across a graphic card. Spoken subtitles must always remain a coherent, continuous phrase in the caption zone.

### 3. Shirt Luminance Contrast & Anti-Yellow Rule
- **Anti-Yellow Washout on Light Shirts:** When the speaker wears an off-white, light cream, beige, or light-colored shirt, **NEVER use pale or medium yellow (`#FFD84D`, `#F8D25F`)** for text or highlights. Yellow merges into the shirt's luminance and becomes illegible.
- **High-Contrast Color System over Light Shirts:**
  - **Crisp Pure White (`#FFFFFF`)**: With a frosted dark backing card (`bg-black/85 backdrop-blur-md px-5 py-2.5 rounded-2xl border border-white/10`) or dual Gaussian drop shadow ($\sigma=14$ tight, $\sigma=4$ sharp).
  - **Power Word Accents**: Use high-chroma **Restrained Crimson (`#FF4B4B`)**, **Vibrant Emerald (`#34D399`)**, or **Electric Cyan (`#00E5FF`)**, ensuring $\ge 7:1$ contrast against light apparel.
- **Auto-Margin Safe Enforcement:** Any line exceeding $82\%$ of screen width must be automatically wrapped into 2 lines or dynamically downscaled, guaranteeing $\ge 120	ext{px}$ safe margins on left and right edges.

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
- **Safe Vertical Slot:** When a scene features 2-line subtitles (starting at $y pprox 1360	ext{px}$ / $2720	ext{px}$ 4K), graphic cards must use a compact horizontal profile ($	ext{height} \le 90	ext{px}$ at 1080p / $\le 180	ext{px}$ at 4K) positioned at $y pprox 1160-1180	ext{px}$ ($2320-2360	ext{px}$ 4K), guaranteeing $> 120	ext{px}$ of clear space above subtitles.

### 6. Vector Brand Icons & Glyph Sanitization (Anti-Tofu Rule)
- **Zero Raw Mathematical Unicode:** Never pass mathematical alphanumeric Unicode glyphs (e.g., `𝕏` `U+1D54F`), non-BMP symbols, or unsupported emoji into standard system fonts (`Avenir Next`, `Helvetica`, `Georgia`). They render as broken square boxes `[?]` ("tofu").
- **Vector Brand Marks:** Draw brand icons (like the X logo, checkmarks, warning triangles) using geometric vector lines (`ImageDraw.line` / vector polygons) or clean SVG/ASCII.
- **Mandatory Unicode Sanitizer:** Always sanitize input strings through a text cleaner (replacing curly quotes, em-dashes, and special symbols with clean standard ASCII) before PIL rendering.

### 7. Dynamic Layout Archetypes (Never 100% Locked Full-Bleed)
- A high-production reel must **NEVER** remain locked in a static full-bleed talking head from second 0 to the end.
- Every video must dynamically leverage multiple layout archetypes across key narrative beats:
  1. **Full-Bleed Push-In (Default)**: Continuous smoothstep cubic camera push-in centered on eyes (35% height) with lower-third kinetic text.
  2. **Framed Inset ("The Studio Gallery")**: The speaker camera smoothly pulls back into an elegant rounded window card ($920 	imes 1300	ext{px}$, $36	ext{px}$ radius) on a clean studio canvas, with bold glowing title typography floating in the upper margin.
  3. **Pure Graphic Cutaway ("Zero-Camera Screen")**: Camera cuts away completely for $1.5	ext{--}3.5	ext{s}$ to a full-screen graphic (Data Velocity Dashboard, Staggered Social Cascade, Monumental Climax) while voiceover continues seamlessly.
  4. **Split-Screen Contrast**: Vertical or dual split comparing two opposing realities.

### 8. Editorial Authenticity & Anti-Buzzword Standard
- **Article 19(1)(a)** is strictly **"Freedom of Speech and Expression"**. NEVER add cheap, fake tags like *"Constitutional Privilege"* or *"Protected"*.
- **Ban Fake Chapter Markers & Artificial Course Metadata**: NEVER add cheap tags like `"Chapter 01: The Agitation Paradox"`, `"Part 1"`, or artificial YouTube course numbers. In punchy vertical Reels/Shorts, these look pretentious, fake, and cheap. If a title is needed above a Framed Inset window, use only the genuine core editorial question or factual topic (e.g. `Krantikari or Puppet?`), or genuine constitutional title (`Article 19(1)(a)`).
- **Ban Cheap Sloganeering & Sensationalist Tags**: NEVER slap tacky badges like *"Weaponized Dissent"*, *"Security Intelligence Record"*, *"Status: Compromised"*, or *"FINAL VERDICT"*. They look like cheap AI slop. Let the script, facts, and delivery carry the power.

### 9. Framed Inset Density & Balanced Canvas Polish (Anti-Blank Canvas Rule)
- A Framed Inset window must **NEVER** look like an empty black void or a lonely box.
- **Embedded Speaker Footage**: The speaker camera footage MUST be dynamically scaled and framed inside the rounded inset window ($920 	imes 1300	ext{px}$, $36	ext{px}$ radius) with subtle edge vignette and the subtitle card docked at the bottom of the window, so the speaker remains fully visible and active throughout the scene.
- The outer studio canvas must feature subtle, architectural dressing:
  - **Natural Studio Atmosphere**: Deep matte slate canvas (`#08090d`) with subtle contrast; zero blurry neon halos.
  - **Discreet Technical Framing**: Subtle corner registration marks (`+`), technical frame metadata (`[ 4K UHD • 24 FPS ]`). ZERO artificial chapter watermarks.
  - **Balanced Proportions**: Window should occupy 68–72% of screen height ($920 	imes 1300	ext{px}$ with $36	ext{px}$ radius), leaving generous but intentional margins for the crisp top title and clean base framing.
  - **Legal / Documentary Anchors**: For legal or constitutional references, include formal documentary header hierarchy: `CONSTITUTION OF INDIA • PART III` $ightarrow$ `ARTICLE 19(1)(a)` $ightarrow$ `Freedom of Speech and Expression`.

### 10. Authentic Editorial Hashtags (Anti-"AI JUNK" Social Standard)
- When depicting bot farms, troll networks, or trending hashtag hysteria:
- **BAN AI JUNK & CHEAP FAKE BADGES**: Absolutely NEVER add fake telemetry tags like `"BOT BURST"`, `"100/hr"`, `"VIRAL CLUSTER"`, `"PROXY ORIGIN"`, or robot emojis `🤖`.
- **BAN RAINBOW CANDY PILLS**: Never create a carnival of multi-colored rounded boxes (cyan + amber + fuchsia + emerald + rose). This screams cheap AI template.
- **Authentic Platform Vernacular**: Use the genuine visual vernacular of X (Twitter) or high-end documentary kinetic typography:
  - Stark, crisp, variable-scale typography (`#DelhiProtest`, `#VoteChori`, `#ChokeCapital`, `#DelhiShutdown`, `#EVMHack`).
  - Authentic platform metadata in muted cool slate (`#71767B`): e.g. `Trending in India • 248.4K posts` or `Trending in Politics • 182K posts`.
  - Staggered editorial layout with clean hairline rules and pure typographic contrast.

### 11. The Anti-"AI JUNK" & Editorial Craft Directive
- **No Text Glow Halos**: Never use diffuse neon text shadows (`drop-shadow-[0_0_35px_rgba(...)]`). High-end editorial style relies on typographic hierarchy, clean whitespace, and crisp kerning.
- **Financial Journalism Data Styling**: When showing economic or statistical comparisons, use the visual language of the Financial Times / Bloomberg / Vox (stark numbers, authentic source citations like `Source: IMF / World Bank`, clean hairline comparison bars), rather than generic web app UI widgets.
- **Monochrome & Single Accent Restraint**: Limit the color palette to stark white (`#FFFFFF`), off-white (`#EDEDED`), slate-muted (`#71767B` / `#8A8F98`), and at most ONE intentional accent color (e.g. warm gold `#D4AF37` or restrained crimson `#E02424`). Zero rainbow multi-color clutter.

### 12. Micro-Chunk Caption Cadence (Max 4–5 Words Per Screen)
- **Hard Word Count Ceiling**: Captions on screen must **NEVER exceed 4 to 5 words** at any single moment. Never dump whole 8–12 word sentences or multi-line paragraphs onto the screen.
- **Target Cadence (2–4 Words Ideal)**: Display text in punchy, high-retention micro-bursts of **2 to 4 words** (maximum 5 words) that update in lockstep with the speaker's vocal tempo ($0.8	ext{s} 	ext{ to } 1.4	ext{s}$ per beat).
- **Why (Visual Velocity & Retention)**: In vertical Reels/Shorts, viewers scan fast. Long sentence blocks create cognitive fatigue, cover too much of the speaker's torso, and look static. Rapid micro-chunks maintain high visual energy and effortless readability.
- **Natural Syntactic Chunking**: Divide sentences at natural acoustic pauses and grammatical boundaries.
- **Clean Single-Line Alignment**: With 2–4 words, captions naturally fit cleanly onto a **single horizontal line**, guaranteeing generous margins ($\ge 120	ext{px}$ on sides) and zero collision with upper graphic cards (`Rule 5`).

### 13. Zero Text Redundancy & Anti-Duplicate Standard
- **Never Duplicate On-Screen Text**: A video frame must **NEVER display the exact same words twice** on screen (e.g. having a monumental header saying `"NATIONAL LIABILITY"` and simultaneously rendering a subtitle pill below it also saying `"NATIONAL LIABILITY"`).
- **Monumental Typography IS the Caption**: In pure typographic cutaways or climax screens, the bold editorial typography on screen *is* the spoken dialogue. Do not render a redundant secondary subtitle pill underneath it.
- **Strict Separation of Base Graphics & Subtitles**: Base graphic surfaces (Framed Inset canvases, comparison cards, social feeds) must **NEVER have dialogue subtitles pre-baked into their PNG images**. Subtitles must be rendered exclusively by the dynamic subtitle stream to prevent double-rendered or overlapping ghost text.

### 14. Minimalist & High-Signal HTML Storyboard Standard
- **Minimal, Distraction-Free Presentation**: Storyboards must follow clean, high-signal editorial design (Apple / Linear aesthetic). Remove all intrusive red dashed bounding boxes, warning borders, or fake phone notches that obscure the speaker's face.
- **100% Complete Screen Coverage**: Storyboards must display **every single scene and micro-chunk beat sequentially** with zero missing screens.
- **Clean Responsive Cards**: Each beat is presented as an unadorned 9:16 vertical preview card with its exact timestamp, word count badge ($\le 4	ext{--}5	ext{ words}$), and clean spoken phrase.

### 15. 60 FPS Procedural Motion Graphics Architecture (Never Static Flat PNGs)
- **Death to Static PNG Pasting**: Never take a single headless browser screenshot (`--screenshot`) of an HTML template and paste a static image onto video frames. That turns rich CSS/DOM layouts into dead, flat stills.
- **Deterministic Time Scrubbing API (`window.seekTo(t)`)**: Every HTML surface template must expose an exact, zero-latency JavaScript method: `window.seekTo(rel_t)` where `rel_t` is the scene elapsed time in seconds.
- **Physical Spring Dynamics & Easing Curves**:
  - **Critically Damped Springs**: Elements enter using physical spring math ($S(t) = 1 - e^{-\zeta \omega t}(\cos(\omega_d t) + rac{\zeta}{\sqrt{1-\zeta^2}}\sin(\omega_d t))$) with $\zeta pprox 0.70	ext{--}0.85$ and settling duration $\le 0.45	ext{s}$.
  - **Rolling Numeric Counters**: Numbers must animate from 0 to target (e.g. `$0.00` to `$4.11T`) synchronized with the camera push ($0.2	ext{s} - 1.25	ext{s}$) with easing (`easeOutExpo` or cubic smoothstep).
  - **Dynamic Progress Bars & Gauges**: Bars must grow smoothly ($0\% ightarrow 92\%$) alongside numbers.
  - **Staggered Spring Cascades**: Multi-element lists (like X trends #1 through #5) must stagger entry by $0.06	ext{--}0.08	ext{s}$ per row with physical elastic overshoot (`scale(1.04) ightarrow scale(1.00)`).
  - **Kinetic Scale Slam**: Climax / monumental typography must slam into place (`1.15 ightarrow 1.00`) with zero rebound for maximum impact.
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
  - Apply Gaussian blur ($\sigma = 10	ext{--}12$).
  - Blend with deep obsidian slate (`#04060c` at $65	ext{--}72\%$ opacity).
  - Composite the UI element on top.
- **Atmospheric Film Grain**: Use FFmpeg hardware SIMD video filter (`-vf noise=c0s=3:allf=t` at $2.5	ext{--}3\%$) on the final composite pipe. This binds the 60 FPS camera, live video, and HTML graphic surfaces into a cohesive, non-digital documentary film texture without dropping CPU render performance.

### 18. Dynamic Spring-Morphing Subtitle Pills & Active Word Karaoke Pop
- **Spring-Morphing Container**: Subtitle pills must dynamically adjust their container dimensions based on active text length with spring smoothing.
- **Word-Level Active Karaoke Highlighting**:
  - The currently spoken active word pops up (`translateY(-2px)`) in high-contrast crisp pure white (`#FFFFFF`) or accent gold/crimson.
  - Inactive words in the active micro-chunk rest at $65	ext{--}70\%$ soft slate opacity (`rgba(255, 255, 255, 0.68)`).
- **Automated Anti-Redundancy Muting**: The subtitle engine must automatically mute subtitle pills whenever a full-screen typographic cutaway (Monumental Climax) or dense social feed (Trending stack) is active (`Rule 13`).

---

## Complete 60 FPS Procedural Motion Pipeline Workflow

1. **Inspect Footage & Audio**:
   - Check resolution, native FPS, HDR/color transfer curve (`ffprobe`).
   - Extract audio and transcribe speech with word-level timestamps in clean Hinglish Roman script.
2. **Micro-Chunk Partitioning**:
   - Group transcription into high-retention micro-chunks of **2 to 4 words** ($\le 5	ext{ words}$ max).
3. **Procedural HTML Surface Authoring**:
   - Build HTML/CSS surfaces with Tailwind CSS and inject the deterministic `window.seekTo(t)` API with spring physics, rolling counters, and staggered cascades.
4. **Pre-Render Frame Sequences (Playwright Pump)**:
   - Run `surface_frame_pump.py` to pre-render dynamic surfaces at **60.0 FPS** into `sequence_cache/`.
5. **Interactive HTML Approval Storyboard**:
   - Compile `approval_storyboard.html` with minimalist design and present to the user.
   - Obtain user approval before starting final composite.
6. **Master 60 FPS Composite Render (`render_master_v8_motion.py`)**:
   - Stream raw video frames from FFmpeg reader pipe at 60 FPS.
   - Apply sub-pixel floating-point camera zoom curve.
   - Composite dynamic motion frame sequences from `sequence_cache/`.
   - Apply live ROI frosted glassmorphism and overlay spring-morphing kinetic subtitles with word karaoke pop.
   - Stream composite frames into FFmpeg writer pipe with hardware SIMD film grain (`noise=c0s=3:allf=t`).
7. **Audio Design & EBU R128 Loudness Normalization**:
   - Mix multi-channel Foley SFX suite (digital clicks, micro-whooshes, subtle pops, sub-boom) locked to scene transitions.
   - Normalize audio to **$-14	ext{ LUFS}$** ($-1.5	ext{ dBTP}$, AAC 192 kbps, 96 kHz) using FFmpeg `loudnorm`.
8. **Final Deliverable Verification**:
   - Verify duration, 60.0 FPS framerate, stream integrity, and playback in QuickTime / AVFoundation.
