# Caption styles (minimalist, premium)

All presets live in `scripts/make_ass.py`. Frame is 1080x1920. Sizes below are in px at that resolution.

## Contents
1. The four presets
2. Highlight rules
3. Palettes
4. Placement and safe zones
5. Timing
6. Hinglish notes
7. Choosing a style

## 1. The four presets

| Style | Look | Words on screen | Best for |
|---|---|---|---|
| `clean` (default) | Inter Bold 72, white, soft shadow; highlighted word turns accent colour | 2-3 (max 4-5) | Almost everything: explainers, advice, authority content |
| `editorial` | Inter Bold 68 white; highlighted word switches to *italic serif* (Playfair) in accent colour | 3-4 (max 5) | Thoughtful, premium, opinion or storytelling content; most "designed" look |
| `pop` | One word at a time, Inter Bold 110, 140ms scale-in 90%->100% | 1 | Punchy hooks, first 5-8 seconds, fast speakers. Use sparingly |
| `box` | Inter Bold 60 on a translucent dark box | 3-4 (max 5) | Busy or bright backgrounds where contrast is a problem |

> **Hard Limit Across All Presets:** A caption cue must **NEVER have more than 4–5 words on screen**. Chunks should be 2–4 words per beat, synchronized with spoken audio timestamps ($0.8\text{s} - 1.4\text{s}$ duration). Whole sentences or long clauses must never be dumped as a single subtitle cue.

Mixing: it is fine to use `pop` for the first hook line and `clean` for the rest only if you render two ASS files and trim, but default to one style per video.

## 2. Highlight rules

- 1 highlighted word per caption line at most; roughly 10-15% of all words.
- Highlight: numbers, amounts, the key noun ("notice", "recovery"), the contrast word ("nahi", "kabhi") when it flips the meaning.
- Do not highlight: filler ("matlab", "basically"), pronouns, whole phrases, consecutive words.
- `editorial` carries emphasis through typeface change as well as colour, so it needs even fewer highlights.

## 3. Palettes (pass with `--accent HEX`)

| Name | HEX | Mood |
|---|---|---|
| Warm gold (default) | `F5C84B` | Premium, trustworthy |
| Soft ivory | `F2E9D8` | Quiet luxury; use with `editorial` |
| Mint | `7FD6B2` | Fresh, fintech |
| Coral | `FF7A66` | Warm, energetic; use only on dark footage |
| Ice blue | `8EC5FF` | Calm, corporate |

Body text stays white `FFFFFF`. Never use more than one accent colour.

## 4. Placement and safe zones (9:16)

- Reels/Shorts overlays cover roughly the bottom 20% (caption/username/buttons) and the top 12%.
- Default `marginv` is 620 (px up from the bottom): captions land at ~68% of the height, below the chin and above the platform UI. Override: `--marginv 700` (higher), `--marginv 520` (lower).
- Keep 90px side margins. Never place text over the mouth/eyes; if the speaker is framed high, move captions down; if framed low, move up.
- Lower-third: bottom-left at x=90, y~1500. Callout: upper third at y~520.

## 5. Timing

- A caption appears at the first word's start and leaves 0.12s after the last word.
- Break lines on punctuation or pauses over 0.35s (`--gap`). Do not break between an article/pronoun and its noun.
- Entry: 90ms fade + 3% scale-in. Exit: 70ms fade. No slides, bounces or typewriter effects.

## 6. Hinglish notes

- Roman script only, lowercase except proper nouns, acronyms (DRT, SARFAESI, EMI) and sentence starts. Skip punctuation clutter: keep commas/full stops only where they help breaking lines.
- Choose one spelling per word for the whole video: "nahi" (not nahin/nahi), "hai", "toh", "kyunki", "aapko". Fix mis-heard Hindi words in `words.json` before rendering.
- English terms inside Hindi sentences keep their English spelling ("notice", "interest", "settlement").
- Devanagari captions need a Devanagari-capable font (Noto Sans Devanagari / Hind) via `--font`; not needed for the default Roman output.

## 7. Choosing a style

1. Is the footage bright/busy? -> `box`.
2. Is it a hook-heavy, fast, high-energy clip? -> `pop` for the hook only.
3. Is it an opinion/explainer where credibility matters? -> `editorial`.
4. Anything else -> `clean`.
When unsure, render `clean` and offer `editorial` as the alternate.

## Examples (word-level input -> on-screen result)

Input words (highlighted word marked with *):
`Agar aapko *DRT* ka notice aaya hai, toh ghabrane ki zaroorat nahi.`

- `clean`: line 1 "Agar aapko **DRT**" (DRT in gold) -> "ka notice aaya hai," -> "toh ghabrane ki" -> "zaroorat nahi."
- `editorial`: "Agar aapko *DRT*" with DRT in gold italic serif, rest in white Inter.
- `pop`: Agar / aapko / **DRT** / ka / notice ... each word alone, centred, 140ms scale-in.
- `box`: same breaks as `clean`, text sits on a translucent dark rectangular box.

Callout example: `{"type":"callout","text":"60 days","sub":"to respond"}` -> large serif "60 days" in the upper third with a small grey line beneath; fades in 200ms, no motion beyond a 6% scale settle.
