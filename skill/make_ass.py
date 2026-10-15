#!/usr/bin/env python3
"""Build a 1080x1920 ASS caption file from a word-level transcript according to talking-head-edit skill.

Features:
- Exact word-level and phrase chunking with ZERO timing overlap
- Native macOS font support (Avenir Next) or fallback Inter
- High legibility on light background: crisp 2px black outline + soft drop shadow
- Highlight keywords with warm gold &H4BC8F5& (RGB F5C84B)
- Subtle 90ms fade + 3% scale-in animation as specified in SKILL.md
"""
import argparse
import json
import re

W, H = 1080, 1920

def ass_time(t):
    t = max(t, 0)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

def bgr(hexrgb):
    hexrgb = hexrgb.lstrip("#")
    r, g, b = hexrgb[0:2], hexrgb[2:4], hexrgb[4:6]
    return f"&H{b}{g}{r}&".upper()

def norm(w):
    return re.sub(r"[^\w]", "", w.lower())

def chunk(words, max_words, max_chars, gap):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        text = " ".join(x["word"] for x in cur)
        nxt = words[i + 1] if i + 1 < len(words) else None
        brk = (
            nxt is None
            or len(cur) >= max_words
            or len(text) >= max_chars
            or re.search(r"[.?!,;:]$", w["word"])
            or (nxt["start"] - w["end"]) > gap
        )
        if brk:
            out.append(cur)
            cur = []
    return out

STYLES = {
    "clean": dict(font="Avenir Next", size=72, bold=1, max_words=3, max_chars=22, marginv=620,
                  upper=False, shadow=True, box=False, emph="color"),
    "editorial": dict(font="Avenir Next", size=68, bold=1, max_words=4, max_chars=26, marginv=620,
                      upper=False, shadow=True, box=False, emph="serif"),
    "pop": dict(font="Avenir Next", size=96, bold=1, max_words=1, max_chars=16, marginv=650,
                upper=False, shadow=True, box=False, emph="color"),
    "box": dict(font="Avenir Next", size=60, bold=1, max_words=4, max_chars=28, marginv=600,
                upper=False, shadow=False, box=True, emph="color"),
}
SERIF = "Playfair Display"

def build_text(ws, st, accent, serif):
    parts = []
    for w in ws:
        t = w["word"].upper() if st["upper"] else w["word"]
        if w.get("emph"):
            if st["emph"] == "serif":
                t = r"{\fn%s\i1\c%s}%s{\r}" % (serif, accent, t)
            else:
                t = r"{\c%s}%s{\r}" % (accent, t)
        parts.append(t)
    return " ".join(parts)

def header(st, font):
    back = "&H8C000000" if st["box"] else "&H64000000"
    border = 3 if st["box"] else 1
    outline = 22 if st["box"] else 2  # crisp 2px outline for maximum readability
    shadow = 0 if st["box"] else 3     # soft shadow
    outcol = back if st["box"] else "&H00000000"
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,{font},{st['size']},&H00FFFFFF,&H00FFFFFF,{outcol},{back},{st['bold']},0,0,0,100,100,0.5,0,{border},{outline},{shadow},2,90,90,{st['marginv']},1
Style: LT,{font},44,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,2,2,1,2,90,90,300,1
Style: LTsub,{font},34,&H00DDDDDD,&H00DDDDDD,&H00000000,&H64000000,0,0,0,0,100,100,2,0,1,2,2,1,2,90,90,250,1
Style: Big,{font},140,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,3,3,5,90,90,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""


def overlay_events(items, accent, serif):
    ev = []
    for o in items:
        s, e = ass_time(o["start"]), ass_time(o["end"])
        if o["type"] == "lowerthird":  # name + role, bottom-left, thin accent rule
            ev.append(f"Dialogue: 2,{s},{e},LT,,0,0,0,,{{\an1\pos(90,1500)\fad(250,250)}}{o['text']}")
            if o.get("sub"):
                ev.append(f"Dialogue: 2,{s},{e},LTsub,,0,0,0,,{{\an1\pos(90,1550)\fad(250,250)}}{o['sub']}")
            ev.append(f"Dialogue: 1,{s},{e},LT,,0,0,0,,{{\an7\pos(90,1430)\fad(250,250)\c{accent}\p1}}m 0 0 l 70 0 70 4 0 4{{\p0}}")
        elif o["type"] == "callout":  # big stat / keyword, upper third, serif, soft in/out
            ev.append(f"Dialogue: 2,{s},{e},Big,,0,0,0,,{{\an5\pos(540,420)\fn{serif}\fad(200,200)\fscx94\fscy94\t(0,260,\fscx100\fscy100)}}{o['text']}")
            if o.get("sub"):
                ev.append(f"Dialogue: 2,{s},{e},LTsub,,0,0,0,,{{\an5\pos(540,510)\fad(200,200)}}{o['sub']}")
    return ev

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words")
    ap.add_argument("out")
    ap.add_argument("--style", default="clean", choices=STYLES)
    ap.add_argument("--keywords", default="")
    ap.add_argument("--accent", default="F5C84B")
    ap.add_argument("--font", default=None)
    ap.add_argument("--serif", default=SERIF)
    ap.add_argument("--marginv", type=int, default=None)
    ap.add_argument("--overlays", default=None)
    ap.add_argument("--gap", type=float, default=0.35)
    a = ap.parse_args()

    st = dict(STYLES[a.style])
    if a.marginv is not None:
        st["marginv"] = a.marginv
    font = a.font or st["font"]
    accent = bgr(a.accent)
    words = json.load(open(a.words, encoding="utf-8"))
    kw = {norm(k) for k in a.keywords.split(",") if k.strip()}
    for w in words:
        if norm(w["word"]) in kw:
            w["emph"] = True

    chunks = chunk(words, st["max_words"], st["max_chars"], a.gap)
    ev = []
    for idx, ch in enumerate(chunks):
        start = ch[0]["start"]
        # Clamp end to prevent overlap with the subsequent chunk!
        raw_end = ch[-1]["end"] + 0.10
        if idx + 1 < len(chunks):
            next_start = chunks[idx + 1][0]["start"]
            end = min(raw_end, next_start - 0.02)
        else:
            end = raw_end

        pass
        if a.style == "pop":
            tag = r"{\fad(60,40)\fscx90\fscy90\t(0,140,\fscx100\fscy100)}"
        else:
            tag = r"{\fad(90,70)\fscx97\fscy97\t(0,160,\fscx100\fscy100)}"
        ev.append(f"Dialogue: 3,{ass_time(start)},{ass_time(end)},Cap,,0,0,0,,{tag}{build_text(ch, st, accent, a.serif)}")

    if a.overlays:
        ev += overlay_events(json.load(open(a.overlays, encoding="utf-8")), accent, a.serif)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(header(st, font) + "\n".join(ev) + "\n")
    print(f"wrote {a.out}: {len(ev)} events, style={a.style}")

if __name__ == "__main__":
    main()
