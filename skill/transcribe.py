#!/usr/bin/env python3
"""Word-level transcript -> words.json (for make_ass.py).

Usage: python transcribe.py cut.mp4 words.json [--model large-v3] [--glossary "DRT,SARFAESI,CaseMate"]

Hinglish in Roman script: Whisper tends to emit Devanagari when language="hi".
We pass a Roman-Hinglish initial_prompt (plus your glossary) and language="en" so output
stays in Roman script. ALWAYS review words.json before rendering - Hinglish is the weakest case.
Requires: pip install faster-whisper
"""
import argparse
import json

from faster_whisper import WhisperModel

PROMPT = ("Yeh ek Hinglish video hai. Hum Hindi aur English mix karke bolte hain, "
          "jaise: aaj hum baat karenge ki notice aaye toh kya karna chahiye, bilkul simple tarike se.")

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("out")
ap.add_argument("--model", default="large-v3")
ap.add_argument("--language", default="en")  # "en" keeps Roman script for Hinglish
ap.add_argument("--glossary", default="")    # domain terms to spell correctly
a = ap.parse_args()

prompt = PROMPT + (" Terms: " + a.glossary.replace(",", ", ") + "." if a.glossary else "")
model = WhisperModel(a.model, compute_type="auto")
segs, _ = model.transcribe(a.video, language=a.language, word_timestamps=True,
                           initial_prompt=prompt, vad_filter=True, beam_size=5)
words = []
for s in segs:
    for w in s.words:
        words.append({"word": w.word.strip(), "start": round(w.start, 2),
                      "end": round(w.end, 2), "emph": False})
json.dump(words, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(words)} words -> {a.out}. Review spelling, then mark emph=true on key words.")
