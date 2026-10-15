import numpy as np
import wave, struct

SFX_DIR = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit/sfx'

# 1. Cinematic Sub-Boom (50Hz decaying sine wave with subtle 80Hz punch)
sr = 44100
dur = 1.8
t = np.linspace(0, dur, int(sr * dur), False)
# Pitch envelope: 75Hz falling to 42Hz
freq = 75.0 * np.exp(-3.0 * t) + 42.0
phase = 2 * np.pi * np.cumsum(freq) / sr
envelope = np.exp(-3.2 * t)
sub_boom = np.sin(phase) * envelope * 0.75

# Add subtle filtered click transient at start
click = np.sin(2 * np.pi * 120 * t[:800]) * np.exp(-0.02 * np.arange(800)) * 0.3
sub_boom[:800] += click
sub_boom = np.clip(sub_boom, -0.95, 0.95)

with wave.open(f'{SFX_DIR}/sub_boom.wav', 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(struct.pack(f'<{len(sub_boom)}h', *(int(s * 32767) for s in sub_boom)))
print("✓ Created sub_boom.wav")

# 2. Subtle Digital Click / Typing Transient
dur_click = 0.05
t_c = np.linspace(0, dur_click, int(sr * dur_click), False)
click_snd = np.sin(2 * np.pi * 1800 * t_c) * np.exp(-120 * t_c) * 0.25
with wave.open(f'{SFX_DIR}/digital_click.wav', 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(struct.pack(f'<{len(click_snd)}h', *(int(s * 32767) for s in click_snd)))
print("✓ Created digital_click.wav")
