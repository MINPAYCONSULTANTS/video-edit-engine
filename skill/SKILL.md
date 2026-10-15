---
name: talking-head-edit
description: Edit face-cam / talking-head videos into minimalist, premium-looking vertical (9:16) Reels/Shorts using FFmpeg and Python - silence removal, smooth easing camera zoom, Hinglish word-level captions in natural lowercase with highlighted champagne-gold keywords, lower-torso motion graphics cards (X/Twitter trending cards, newspaper clippings, KPI stat pills), tactile micro-SFX, light color grade, mandatory HTML approval storyboard gate, and loudness-normalised audio. Use this skill whenever the user mentions editing a face cam video, talking head video, reel, short, captions, subtitles, motion graphics, or burning text onto a raw recording.
---

# Talking-Head Edit (Minimalist, Reference-Aligned & Storyboard-Gated)

Goal: Raw face-cam in, clean, premium vertical video out. **Restraint is the style.** 
Derived directly from real-world high-craft creator references and editorial documentary style (Vox, Johnny Harris).

---

## The 4 Iron Rules

### 1. The Sacred Face Rule (100% Off-Face Guarantee)
- **Face is Sacred:** The speaker's eyes, glasses, nose, mouth, beard, and facial expressions ($y \le 980\text{px}$ on 1080p, or $y \le 340\text{px}$ on mobile canvas) must **NEVER** have any text, boxes, or graphic elements rendered over them.
- **Lower-Torso Anchoring:** All motion graphic cards, badges, and citations must be strictly anchored to the **mid/lower torso on the shirt** ($y \ge 1200\text{px}$ on 1080p), providing $\ge 220\text{px}$ of clear breathing room below the chin.
- **No Hairline Boxes:** Never place floating pill boxes or text headers at the top of the frame ($y \le 250\text{px}$). They collide with hair, look like accidental watermarks, and get covered by Instagram's native top header.

### 2. Unified Sentence Continuity & Audio-Locked Transitions (Zero Pre-Mature Cuts)
- **Zero Pre-Mature Cuts:** A scene change or screen cut must **NEVER** occur mid-sentence or before the spoken clause has finished playing. Transitions must be locked strictly to acoustic pauses between sentences (`pause >= 0.25s`).
- **Zero Orphaned / Pre-Loaded Subtitles:** The text displayed on screen must strictly match the phrase being spoken. Never display clauses belonging to the next scene (e.g. displaying *"uss din tum deshbhakt nahi"* while the speaker is still finishing *"dushman desh ka weapon ban jaye"*).
- Never slice a spoken sentence across a graphic card (e.g. `Line 1: "har 2 mahine mein"` $\rightarrow$ `[CARD: 50 METRO STATIONS]` $\rightarrow$ `Line 2: "station band karwaoge"`). Spoken subtitles must always remain a coherent, continuous phrase in the caption zone.

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
- **Programmatic Enforcement:** Every render script MUST compute `max_card_bottom = caption_top - clearance` and clamp/reposition cards dynamically.

### 6. Vector Brand Icons & Glyph Sanitization (Anti-Tofu Rule)
- **Zero Raw Mathematical Unicode:** Never pass mathematical alphanumeric Unicode glyphs (e.g., `𝕏` `U+1D54F`), non-BMP symbols, or unsupported emoji into standard system fonts (`Avenir Next`, `Helvetica`, `Georgia`). They render as broken square boxes `[?]` ("tofu").
- **Vector Brand Marks:** Draw brand icons (like the X logo, checkmarks, warning triangles) using geometric vector lines (`ImageDraw.line` / vector polygons) or clean ASCII text.
- **Mandatory Unicode Sanitizer:** Always sanitize input strings through a text cleaner (replacing curly quotes, em-dashes, and special symbols with clean standard ASCII) before PIL rendering.

### 7. Dynamic Layout Archetypes (Never 100% Locked Full-Bleed)
- A high-production reel must **NEVER** remain locked in a static full-bleed talking head from second 0 to the end.
- Every video must dynamically leverage multiple layout archetypes across key narrative beats:
  1. **Full-Bleed Push-In (Default)**: Continuous smoothstep cubic camera push-in centered on eyes (35% height) with lower-third kinetic text.
  2. **Framed Inset ("The Studio Gallery" - Ref 2 Style)**: The speaker camera smoothly pulls back into an elegant rounded window card (e.g. $880 \times 1220\text{px}$, $36\text{px}$ radius) on a clean studio canvas, with bold glowing title typography floating in the upper margin.
  3. **Pure Graphic Cutaway ("Zero-Camera Screen" - Ref 1 & Ref 3 Style)**: Camera cuts away completely for $1.5\text{--}3.5\text{s}$ to a full-screen graphic (Retro Pixel OS, Minimalist Hero Icon, Data Velocity Dashboard) while voiceover continues seamlessly.
  4. **Split-Screen Contrast**: Vertical or dual split comparing two opposing realities.

### 8. Editorial Authenticity & Anti-Buzzword Standard
- **Article 19(1)(a)** is strictly **"Freedom of Speech and Expression"**. NEVER add cheap, fake tags like *"Constitutional Privilege"* or *"Protected"*.
- **Ban Fake Chapter Markers & Artificial Course Metadata**: NEVER add cheap tags like `"Chapter 01: The Agitation Paradox"`, `"Part 1"`, or artificial YouTube course numbers. In punchy vertical Reels/Shorts, these look pretentious, fake, and cheap. If a title is needed above a Framed Inset window, use only the genuine core editorial question or factual topic (e.g. `Krantikari or Puppet?`), or genuine constitutional title (`Article 19(1)(a)`).
- **Ban Cheap Sloganeering & Sensationalist Tags**: NEVER slap tacky badges like *"Weaponized Dissent"*, *"Security Intelligence Record"*, *"Status: Compromised"*, or *"FINAL VERDICT"*. They look like cheap AI slop. Let the script, facts, and delivery carry the power.

### 9. Framed Inset Density & Balanced Canvas Polish (Anti-Blank Canvas Rule)
- A Framed Inset window must **NEVER** look like an empty black void or a lonely box.
- **Embedded Speaker Footage**: The speaker camera footage MUST be dynamically scaled and framed inside the rounded inset window ($920 \times 1300\text{px}$, $36\text{px}$ radius) with subtle edge vignette and the subtitle card docked at the bottom of the window, so the speaker remains fully visible and active throughout the scene.
- The outer studio canvas must feature subtle, architectural dressing:
  - **Natural Studio Atmosphere**: Deep matte slate canvas (`#08090d`) with subtle contrast; zero blurry neon halos.
  - **Discreet Technical Framing**: Subtle corner registration marks (`+`), technical frame metadata (`[ 4K UHD • 24 FPS ]`). ZERO artificial chapter watermarks.
  - **Balanced Proportions**: Window should occupy 68–72% of screen height ($920 \times 1300\text{px}$ with $36\text{px}$ radius), leaving generous but intentional margins for the crisp top title and clean base framing.
  - **Legal / Documentary Anchors**: For legal or constitutional references (e.g. Article 19), include formal documentary header hierarchy: `CONSTITUTION OF INDIA • PART III` $\rightarrow$ `ARTICLE 19(1)(a)` $\rightarrow$ `Freedom of Speech and Expression`. Absolutely zero cheap tags like "Constitutional Privilege".

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
- **Target Cadence (2–4 Words Ideal)**: Display text in punchy, high-retention micro-bursts of **2 to 4 words** (maximum 5 words) that update in lockstep with the speaker's vocal tempo ($0.8\text{s} \text{ to } 1.4\text{s}$ per beat).
- **Why (Visual Velocity & Retention)**: In vertical Reels/Shorts, viewers scan fast. Long sentence blocks create cognitive fatigue, cover too much of the speaker's torso, and look static. Rapid micro-chunks maintain high visual energy and effortless readability.
- **Natural Syntactic Chunking**: Divide sentences at natural acoustic pauses and grammatical boundaries:
  - *Example*:
    - Beat 1: `"Jis desh ne Mumbai pe"` (4 words)
    - Beat 2: `"26/11 karwaya tha..."` (3 words)
    - Beat 3: `"agar woh tumhare"` (3 words)
    - Beat 4: `"protest ke liye"` (3 words)
    - Beat 5: `"taaliyan baja raha hai,"` (4 words)
    - Beat 6: `"toh tum krantikari nahi,"` (4 words)
    - Beat 7: `"unke puppet ho!"` (3 words)
- **Clean Single-Line Alignment**: With 3–5 words, captions naturally fit cleanly onto a **single horizontal line**, guaranteeing generous margins ($\ge 120\text{px}$ on sides) and zero collision with upper graphic cards (`Rule 5`).
- **Styling & Contrast Discipline**: Micro-chunk bursts must still strictly follow **Rule 3** (crisp white `#FFFFFF` on dark frosted backing card, zero yellow over light shirts, and at most one highlighted accent keyword per burst).

### 13. Zero Text Redundancy & Anti-Duplicate Standard
- **Never Duplicate On-Screen Text**: A video frame must **NEVER display the exact same words twice** on screen (e.g. having a monumental header saying `"NATIONAL LIABILITY"` and simultaneously rendering a subtitle pill below it also saying `"NATIONAL LIABILITY"`).
- **Monumental Typography IS the Caption**: In pure typographic cutaways or climax screens, the bold editorial typography on screen *is* the spoken dialogue. Do not render a redundant secondary subtitle pill underneath it.
- **Strict Separation of Base Graphics & Subtitles**: Base graphic surfaces (Framed Inset canvases, comparison cards, social feeds) must **NEVER have dialogue subtitles pre-baked into their PNG images**. Subtitles must be rendered exclusively by the dynamic subtitle stream to prevent double-rendered or overlapping ghost text.

### 14. Minimalist & High-Signal HTML Storyboard Standard
- **Minimal, Distraction-Free Presentation**: Storyboards must follow clean, high-signal editorial design (Apple / Linear aesthetic). Remove all intrusive red dashed bounding boxes, warning borders, or fake phone notches that obscure the speaker's face.
- **100% Complete Screen Coverage**: Storyboards must display **every single scene and micro-chunk beat sequentially** with zero missing screens.
- **Clean Responsive Cards**: Each beat is presented as an unadorned 9:16 vertical preview card with its exact timestamp, word count badge ($\le 4\text{--}5\text{ words}$), and clean spoken phrase.

---

## High-Production Motion Graphic Elements

1. **Framed Inset Studio Window (Ref 2):**
   - Speaker camera nested in rounded container ($900 \times 1280$) with soft shadow; floating glowing title, atmospheric studio gradient, and corner registration marks.
2. **Dynamic Hashtag Swarm Cloud (Bot Farms & Online Hysteria):**
   - Multi-layered floating tags (`#DelhiProtest`, `#VoteChori`) appearing and drifting across full canvas with bot telemetry badges.
3. **Pure Animation Cutaways (Ref 1 & 3):**
   - Retro OS & Pixel Simulator: Vintage 8-bit folder, bouncing pixel arrow, mechanical clicking mouse cursor, pixel typography.
   - Minimalist Luxury Hero: Pure canvas, 3.5D squircle app icon, subtle levitation float.
4. **Data Velocity & Metric Dashboards:**
   - Obsidian black canvas with live rolling counters, macro GDP comparison bars, and animated SVG sparklines.
5. **Authentic X / Twitter Trending Card:**
   - Dark frosted glass (`fill=(14, 18, 26, 240)`), verified badge, `#1 TRENDING IN INDIA`, and post count. Anchored on lower chest, $> 220\text{px}$ below chin.
6. **Authentic Newspaper / Headline Clipping:**
   - Editorial news popout for cited facts with newsprint border, subtle $1.5^\circ$ angle, and hand-drawn yellow marker highlight.
7. **Tactile Micro-SFX (Whisper Audio Polish):**
   - Synthesize or mix clean subtle micro-whooshes, mechanical mouse clicks, and gentle pop triggers at $-24\text{ dB}$ on graphic card entrances.

---

## Complete Pipeline Workflow

1. **Inspect Footage:** Check resolution, FPS, HDR/color transfer curve (`ffprobe`).
2. **Audio Transcript & Word Timing:** Transcribe speech with word-level timestamps in clean Hinglish Roman script.
3. **Camera Motion Curve:** Generate continuous cubic Hermite / smoothstep camera push/pull curve ($S(u) = 3u^2 - 2u^3$) with head tracking centered at $35\%$ height.
4. **Generate Interactive Approval Storyboard:**
   - Extract half-resolution JPEG keyframes for each cut.
   - Compile `approval_storyboard.html` with Tailwind CSS, Instagram UI overlay simulator, and off-face safe zones.
   - Open and present to the user.
5. **Obtain User Approval:** Review feedback, adjust timing or typography if requested.
6. **Master Composite Render:**
   - Pre-render 4K supersampled graphic surfaces with Lanczos filtering.
   - Stream animated transparent overlay (`qtrle`).
   - Composite using FFmpeg with `-deblock -1:-1`, CRF 15, and loudness-normalized `-14 LUFS` EBU R128 audio with tactile micro-SFX.
