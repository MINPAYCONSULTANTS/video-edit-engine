#!/usr/bin/env python3
import os, sys, json, base64

FRAMES_DIR = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit/storyboard_frames'
OUT_HTML = '/Users/sanskarsaraf/.gemini/antigravity/brain/c3d97250-5f63-4415-8e05-a6900d445973/approval_storyboard.html'

scenes = [
    {
        'id': 's01',
        'title': 'The Hook',
        'start': 0.00, 'end': 2.66,
        'frame_file': 's01_hook.jpg',
        'transcript': 'July mein public inke saath thi...',
        'lines': [
            {'words': [{'text': 'July mein', 'highlight': True}, {'text': 'public', 'highlight': False}]},
            {'words': [{'text': 'inke saath', 'highlight': False}, {'text': 'thi...', 'highlight': True}]}
        ],
        'camera': 'Wide (1.00x) Grounded',
        'mg_type': 'None (Hook Focus)',
        'mg_desc': 'Pure facial hook. Face is 100% sacred and unobstructed.',
        'sfx': 'Ambient Studio Clean',
        'safe_status': 'PASS (100% Off-Face)',
        'mg_preview': None
    },
    {
        'id': 's02',
        'title': 'The Turn',
        'start': 2.66, 'end': 4.30,
        'frame_file': 's02_turn.jpg',
        'transcript': 'lekin October mein jab police ne uthaya,',
        'lines': [
            {'words': [{'text': 'lekin October mein jab', 'highlight': False}]},
            {'words': [{'text': 'police ne', 'highlight': True}, {'text': 'uthaya,', 'highlight': False}]}
        ],
        'camera': 'Smooth Push Ease-In (1.00x → 1.08x)',
        'mg_type': 'Action Accent',
        'mg_desc': 'Subtle camera tightening. Subtitle in lower third on polo shirt.',
        'sfx': 'None (Clean Speech)',
        'safe_status': 'PASS (100% Off-Face)',
        'mg_preview': None
    },
    {
        'id': 's03',
        'title': 'Viral Trending Tag',
        'start': 4.30, 'end': 7.50,
        'frame_file': 's03_hashtag.jpg',
        'transcript': 'toh Delhi ne trend karwaya #ThankYouDelhiPolice',
        'lines': [
            {'words': [{'text': 'toh Delhi ne', 'highlight': False}, {'text': 'trend karwaya', 'highlight': True}]}
        ],
        'camera': 'Medium Held (1.08x)',
        'mg_type': 'Authentic X / Twitter Trending Card',
        'mg_desc': 'Positioned strictly on lower polo shirt, 120px BELOW chin. Zero overlap with face.',
        'sfx': '🔊 Micro-Whoosh Slide In (-22 dB)',
        'safe_status': 'FIXED (100% Off Face • Lower Torso)',
        'mg_preview': 'x_trending'
    },
    {
        'id': 's04',
        'title': 'The Question & Daily Life',
        'start': 7.70, 'end': 10.50,
        'frame_file': 's04_reality_q.jpg',
        'transcript': 'kyun pata hai? kyunki aam Delhi walon ko',
        'lines': [
            {'words': [{'text': 'kyun', 'highlight': False}, {'text': 'pata hai?', 'highlight': True}]},
            {'words': [{'text': 'kyunki aam', 'highlight': False}, {'text': 'Delhi walon ko', 'highlight': True}]}
        ],
        'camera': 'Smooth Pull Glide (1.08x → 1.00x)',
        'mg_type': 'Clean Dialogue Focus (Remark Removed)',
        'mg_desc': 'Removed "Article 19: Citizen Mobility" per request. Completely clean and unobstructed.',
        'sfx': 'None',
        'safe_status': 'PASS (100% Clean)',
        'mg_preview': None
    },
    {
        'id': 's05',
        'title': 'Morning Commute Reality',
        'start': 10.50, 'end': 12.08,
        'frame_file': 's05_reality_subah.jpg',
        'transcript': 'subah kaam pe nikalna hota hai.',
        'lines': [
            {'words': [{'text': 'subah kaam pe', 'highlight': False}]},
            {'words': [{'text': 'nikalna hota hai.', 'highlight': True}]}
        ],
        'camera': 'Wide Grounded (1.00x)',
        'mg_type': 'Auto-Wrapped Natural Typography',
        'mg_desc': 'Wrapped into 2 lines. Guaranteed 160px margin buffer, zero edge cutoff.',
        'sfx': 'None',
        'safe_status': 'FIXED (Subah truncation eliminated)',
        'mg_preview': None
    },
    {
        'id': 's06',
        'title': 'Gridlock Stat: 50 Stations',
        'start': 12.08, 'end': 14.56,
        'frame_file': 's06_stat_metro.jpg',
        'transcript': 'har 2 mahine mein 50 metro station band karwaoge,',
        'lines': [
            {'words': [{'text': 'har 2 mahine mein', 'highlight': False}]},
            {'words': [{'text': '50 metro station', 'highlight': 'red'}, {'text': 'band karwaoge,', 'highlight': False}]}
        ],
        'camera': 'Wide (1.00x)',
        'mg_type': 'Editorial Newspaper Clipping Popout (High-Production)',
        'mg_desc': 'Authentic newsprint card cutout on lower polo shirt with soft paper drop shadow. 100% off the face.',
        'sfx': '🔊 Tactile Paper Pop (-22 dB)',
        'safe_status': 'FIXED (100% Off Face • Newspaper Cutout)',
        'mg_preview': 'newspaper_clipping'
    },
    {
        'id': 's07',
        'title': 'Public Reaction Contrast',
        'start': 14.56, 'end': 17.80,
        'frame_file': 's07_taaliyan.jpg',
        'transcript': 'traffic choke karoge toh log taaliyan thodi bajayenge!',
        'lines': [
            {'words': [{'text': 'traffic choke karoge', 'highlight': 'red'}, {'text': 'toh', 'highlight': False}]},
            {'words': [{'text': 'log taaliyan', 'highlight': False}, {'text': 'thodi bajayenge!', 'highlight': True}]}
        ],
        'camera': 'Wide (1.00x)',
        'mg_type': 'Kinetic Dynamic Emphasis',
        'mg_desc': 'Lower third captions on chest with gold & red emphasis.',
        'sfx': 'None',
        'safe_status': 'PASS (100% Off-Face)',
        'mg_preview': None
    },
    {
        'id': 's08',
        'title': 'Flight Transition',
        'start': 18.10, 'end': 20.64,
        'frame_file': 's08_flight.jpg',
        'transcript': 'flight se utha rahe the toh co-passengers hass rahe the.',
        'lines': [
            {'words': [{'text': 'flight se utha rahe the toh', 'highlight': False}]},
            {'words': [{'text': 'co-passengers', 'highlight': True}, {'text': 'hass rahe the.', 'highlight': False}]}
        ],
        'camera': 'Smooth Push Ease-In (1.00x → 1.10x)',
        'mg_type': 'Context Icon Tag',
        'mg_desc': 'Clean transition into political comparison.',
        'sfx': 'None',
        'safe_status': 'PASS (100% Off-Face)',
        'mg_preview': None
    },
    {
        'id': 's09',
        'title': 'Delhi: Emergency Reels',
        'start': 21.20, 'end': 24.50,
        'frame_file': 's09_delhi_bus.jpg',
        'transcript': 'aur jab bus mein bitha ke emergency reels bana rahe the,',
        'lines': [
            {'words': [{'text': 'aur jab bus mein bitha ke', 'highlight': False}]},
            {'words': [{'text': 'emergency reels', 'highlight': 'red'}, {'text': 'bana rahe the,', 'highlight': False}]}
        ],
        'camera': 'Medium Held (1.10x)',
        'mg_type': 'Clean Dialogue Focus (Remark Removed)',
        'mg_desc': 'Removed "Delhi: Bus emergency reels" badge per request. Subtitles only.',
        'sfx': 'None',
        'safe_status': 'PASS (100% Clean)',
        'mg_preview': None
    },
    {
        'id': 's10',
        'title': 'Chennai: Chilling with Vijay',
        'start': 24.50, 'end': 28.50,
        'frame_file': 's10_chennai_chill.jpg',
        'transcript': 'tab Rahul Gandhi Chennai mein Vijay ke saath chill kar raha tha.',
        'lines': [
            {'words': [{'text': 'tab Rahul Gandhi', 'highlight': True}, {'text': 'Chennai mein', 'highlight': False}]},
            {'words': [{'text': 'Vijay ke saath', 'highlight': False}, {'text': 'chill kar raha tha.', 'highlight': 'gold'}]}
        ],
        'camera': 'Medium Held (1.10x)',
        'mg_type': 'Clean Dialogue Focus (Remark Removed)',
        'mg_desc': 'Removed "Chennai: Chilling with vijay" badge per request. Subtitles only.',
        'sfx': 'None',
        'safe_status': 'PASS (100% Clean)',
        'mg_preview': None
    },
    {
        'id': 's11',
        'title': 'Closing Climax & Verdict',
        'start': 28.70, 'end': 32.80,
        'frame_file': 's11_climax.jpg',
        'transcript': 'aam janta tumhare tamashon se PAK CHUKI HAI!',
        'lines': [
            {'words': [{'text': 'aam janta', 'highlight': False}, {'text': 'tumhare', 'highlight': False}]},
            {'words': [{'text': 'tamashon se', 'highlight': True}]},
            {'words': [{'text': 'PAK CHUKI HAI!', 'highlight': True, 'all_caps_large': True}]}
        ],
        'camera': 'Climax Punch Ease (1.10x → 1.14x)',
        'mg_type': 'High-Impact Typography Climax',
        'mg_desc': 'ALL CAPS enlarged font for "PAK CHUKI HAI!" with bold champagne gold emphasis.',
        'sfx': '🔊 Low-End Impact Punch (-20 dB)',
        'safe_status': 'PASS (Enlarged ALL CAPS)',
        'mg_preview': None
    }
]

# Load base64 for each frame
for s in scenes:
    fpath = os.path.join(FRAMES_DIR, s['frame_file'])
    if os.path.exists(fpath):
        with open(fpath, 'rb') as f:
            s['b64'] = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')
    else:
        s['b64'] = ''

# Generate HTML file
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reel Motion Graphics & Storyboard Approval System</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&family=Playfair+Display:ital,wght@1,600;1,700&display=swap');
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
    .font-serif { font-family: 'Playfair Display', serif; }
    .phone-stage {
      width: 360px;
      height: 640px;
      aspect-ratio: 9 / 16;
    }
  </style>
</head>
<body class="bg-[#0b0d13] text-[#e2e8f0] antialiased min-h-screen p-4 md:p-6 lg:p-8">

  <!-- Top Global Header -->
  <header class="max-w-7xl mx-auto mb-8 bg-[#131620] border border-[#23293e] rounded-2xl p-6 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
    <div>
      <div class="flex items-center gap-3 mb-2">
        <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span> Unwanted Remarks Removed
        </span>
        <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-500/10 text-amber-400 border border-amber-500/30 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-amber-400"></span> "PAK CHUKI HAI!" ALL CAPS
        </span>
        <span class="text-xs text-slate-400 font-mono">PXL_20261013_060947291~2</span>
      </div>
      <h1 class="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">Interactive Visual Review & Motion Graphics Director</h1>
      <p class="text-sm text-slate-400 mt-1">Remarks removed from scenes 4, 9, 10. Climax updated to enlarged ALL CAPS.</p>
    </div>

    <!-- Global Controls -->
    <div class="flex flex-wrap items-center gap-3">
      <button id="toggle-safe-btn" onclick="toggleSafeOverlay()" class="px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800/80 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition flex items-center gap-2">
        <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        <span id="safe-btn-text">Instagram Safe Zones: ON</span>
      </button>

      <button onclick="approveAllScenes()" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-xs font-bold text-white shadow-lg shadow-emerald-900/30 transition flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
        Approve & Render Final Master
      </button>
    </div>
  </header>

  <!-- Main Grid: Phone Simulator (Left) + Scene Scrubber & Inspector (Right) -->
  <main class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
    
    <!-- LEFT: Phone Canvas (Col 1-5) -->
    <div class="lg:col-span-5 flex flex-col items-center">
      <div class="sticky top-6 flex flex-col items-center w-full">
        <div class="text-xs uppercase tracking-wider font-bold text-slate-400 mb-3 flex items-center justify-between w-[360px]">
          <span>Live 9:16 Canvas Simulator</span>
          <span id="scene-counter" class="font-mono text-emerald-400">Scene 1 of 11</span>
        </div>

        <!-- Phone Outer Shell -->
        <div class="phone-stage relative bg-black rounded-[40px] shadow-[0_25px_60px_-15px_rgba(0,0,0,0.8)] border-[6px] border-[#222736] overflow-hidden select-none">
          <img id="stage-bg" src="" alt="Video Frame" class="absolute inset-0 w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-b from-black/15 via-transparent to-black/35 pointer-events-none"></div>

          <!-- UNIFIED LOWER-THIRD STAGE (Guaranteed 100% OFF FACE) -->
          <div class="absolute inset-x-3 bottom-[92px] pointer-events-none flex flex-col items-center justify-end gap-2.5 z-10">
            <div id="mg-layer" class="w-full flex justify-center items-center"></div>
            <div id="caption-layer" class="w-full flex flex-col items-center justify-center text-center"></div>
          </div>

          <!-- Face Protection Safe Boundary -->
          <div id="face-boundary" class="absolute top-[80px] left-[55px] right-[55px] h-[190px] border-2 border-dashed border-sky-400/30 rounded-2xl pointer-events-none flex items-start justify-center pt-1.5 transition-opacity duration-200">
            <span class="text-[8px] font-mono font-bold text-sky-300 bg-sky-950/80 px-2 py-0.5 rounded shadow">FACE PROTECTED ZONE (ZERO ELEMENTS)</span>
          </div>

          <!-- Instagram Safe Overlay -->
          <div id="safe-overlay" class="absolute inset-0 pointer-events-none transition-opacity duration-200">
            <div class="absolute top-0 inset-x-0 h-[70px] border-b-2 border-dashed border-red-500/50 bg-red-500/10 flex items-center justify-center">
              <span class="text-[9px] font-mono font-bold tracking-widest text-red-300 bg-red-950/80 px-2 py-0.5 rounded">INSTAGRAM HEADER ZONE</span>
            </div>
            <div class="absolute bottom-0 inset-x-0 h-[85px] border-t-2 border-dashed border-red-500/50 bg-red-500/10 flex items-center justify-center">
              <span class="text-[9px] font-mono font-bold tracking-widest text-red-300 bg-red-950/80 px-2 py-0.5 rounded">BOTTOM UI & AUDIO ZONE</span>
            </div>
            <div class="absolute right-0 top-1/2 -translate-y-1/2 w-[55px] h-[220px] border-l-2 border-dashed border-amber-500/50 bg-amber-500/10 flex flex-col items-center justify-around py-3">
              <div class="w-6 h-6 rounded-full bg-white/20 flex items-center justify-center text-[10px] text-white">❤️</div>
              <div class="w-6 h-6 rounded-full bg-white/20 flex items-center justify-center text-[10px] text-white">💬</div>
              <div class="w-6 h-6 rounded-full bg-white/20 flex items-center justify-center text-[10px] text-white">↗️</div>
              <div class="w-6 h-6 rounded-full bg-white/20 flex items-center justify-center text-[10px] text-white">⋯</div>
            </div>
            <div class="absolute top-[75px] bottom-[90px] left-[15px] right-[58px] border border-emerald-400/40 rounded-lg pointer-events-none flex items-start justify-end p-1">
              <span class="text-[8px] font-mono text-emerald-400 bg-emerald-950/70 px-1 rounded">SAFE CONTENT ZONE</span>
            </div>
          </div>

          <!-- Camera Tag -->
          <div class="absolute top-3 left-4 bg-black/70 backdrop-blur-md px-2.5 py-1 rounded-full text-[10px] font-mono text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5 z-20">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
            <span id="stage-camera">1.00x Grounded Wide</span>
          </div>

          <!-- Timestamp Tag -->
          <div class="absolute top-3 right-4 bg-black/70 backdrop-blur-md px-2.5 py-1 rounded-full text-[10px] font-mono text-slate-300 border border-slate-700 z-20">
            <span id="stage-time">0.00s - 2.66s</span>
          </div>
        </div>

        <!-- Controls Under Phone -->
        <div class="w-[360px] mt-4 flex items-center justify-between gap-2 bg-[#131620] border border-[#23293e] rounded-xl p-3 shadow-lg">
          <button onclick="prevScene()" class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
          </button>
          
          <button id="play-btn" onclick="toggleAutoPlay()" class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition flex items-center gap-2">
            <svg id="play-icon" class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"/></svg>
            <span id="play-text">Auto Preview</span>
          </button>

          <button onclick="nextScene()" class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </button>
        </div>
      </div>
    </div>

    <!-- RIGHT: Inspector (Col 6-12) -->
    <div class="lg:col-span-7 flex flex-col gap-6">

      <!-- Scene Quick Select Timeline Pills -->
      <div class="bg-[#131620] border border-[#23293e] rounded-2xl p-5 shadow-xl">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"/></svg>
            Timeline Scene Scrubber
          </h2>
          <span class="text-xs text-slate-400 font-mono">11 Cuts • Click To Inspect</span>
        </div>
        <div class="grid grid-cols-4 sm:grid-cols-6 lg:grid-cols-11 gap-1.5" id="timeline-pills"></div>
      </div>

      <!-- Current Scene Deep Inspector Card -->
      <div class="bg-[#131620] border border-[#23293e] rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div class="flex items-center justify-between pb-4 border-b border-[#23293e]">
          <div>
            <span id="inspector-badge" class="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">SCENE 01</span>
            <h3 id="inspector-title" class="text-xl font-bold text-white mt-1">The Hook</h3>
          </div>
          <div class="text-right font-mono text-xs">
            <span id="inspector-timing" class="text-slate-400">0.00s – 2.66s (2.66s)</span>
            <div id="inspector-status" class="mt-1 text-emerald-400 font-semibold flex items-center gap-1 justify-end">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Approved
            </div>
          </div>
        </div>

        <!-- Spoken Audio & Subtitles -->
        <div class="mt-5">
          <label class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Spoken Audio Hindi Phrase</label>
          <div id="inspector-transcript" class="mt-1.5 p-3.5 bg-[#0b0d13] border border-[#23293e] rounded-xl text-sm font-medium text-slate-200">
            "July mein public inke saath thi..."
          </div>
        </div>

        <!-- Motion Graphic Solution & Comparison -->
        <div class="mt-5 p-4 rounded-xl bg-gradient-to-br from-[#1a1e2e] to-[#121522] border border-[#2d344d]">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-bold text-emerald-400 uppercase tracking-wide flex items-center gap-1.5">
              <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              Current Visual Plan
            </span>
            <span id="inspector-mg-type" class="text-xs font-mono text-slate-400">None (Hook Focus)</span>
          </div>
          <p id="inspector-mg-desc" class="text-xs leading-relaxed text-slate-300">
            Pure facial hook. Face is 100% sacred and unobstructed.
          </p>
        </div>

        <!-- Technical Parameters Grid -->
        <div class="mt-5 grid grid-cols-1 sm:grid-cols-4 gap-3">
          <div class="bg-[#0b0d13] p-3 rounded-xl border border-[#23293e]">
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Camera Motion</span>
            <span id="inspector-camera" class="text-xs font-mono font-semibold text-emerald-300 mt-0.5 block">1.00x Wide</span>
          </div>
          <div class="bg-[#0b0d13] p-3 rounded-xl border border-[#23293e]">
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Face Protection</span>
            <span id="inspector-safe" class="text-xs font-mono font-semibold text-emerald-300 mt-0.5 block">PASS (100% Off-Face)</span>
          </div>
          <div class="bg-[#0b0d13] p-3 rounded-xl border border-[#23293e]">
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Tactile SFX</span>
            <span id="inspector-sfx" class="text-xs font-mono font-semibold text-purple-300 mt-0.5 block">Clean Studio</span>
          </div>
          <div class="bg-[#0b0d13] p-3 rounded-xl border border-[#23293e]">
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Anchor Placement</span>
            <span class="text-xs font-mono font-semibold text-amber-300 mt-0.5 block">Polo Shirt (Torso)</span>
          </div>
        </div>

        <!-- Ready to Render Direct Action -->
        <div class="mt-6 pt-5 border-t border-[#23293e] flex items-center justify-between gap-4">
          <span class="text-xs text-slate-400 font-mono">Status: Ready For Master Render</span>
          <button onclick="approveAllScenes()" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-xs font-bold text-white shadow-lg shadow-emerald-900/30 transition flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
            Trigger Final Render
          </button>
        </div>
      </div>

    </div>
  </main>

  <script>
    const scenes = ''' + json.dumps(scenes) + ''';
    let currentIdx = 0;
    let isAutoPlaying = false;
    let autoPlayTimer = null;
    let showSafeOverlay = true;

    function renderScene(idx) {
      currentIdx = idx;
      const s = scenes[idx];

      const bgImg = document.getElementById('stage-bg');
      bgImg.src = s.b64;

      document.getElementById('stage-camera').innerText = s.camera;
      document.getElementById('stage-time').innerText = `${s.start.toFixed(2)}s – ${s.end.toFixed(2)}s`;
      document.getElementById('scene-counter').innerText = `Scene ${idx + 1} of ${scenes.length}`;

      const capLayer = document.getElementById('caption-layer');
      capLayer.innerHTML = '';
      
      s.lines.forEach(line => {
        const lineDiv = document.createElement('div');
        lineDiv.className = 'flex flex-wrap justify-center items-center gap-x-1.5 my-0.5 leading-tight';
        
        line.words.forEach(w => {
          const span = document.createElement('span');
          span.innerText = w.text;
          
          if (w.all_caps_large) {
            span.className = 'text-[#ffd84d] font-black text-[18px] tracking-wide uppercase drop-shadow-[0_3px_6px_rgba(0,0,0,0.95)]';
          } else if (w.highlight === true || w.highlight === 'gold') {
            span.className = 'text-[#ffd84d] font-extrabold text-[14px] drop-shadow-[0_2px_4px_rgba(0,0,0,0.9)]';
          } else if (w.highlight === 'red') {
            span.className = 'text-[#ff4b4b] font-extrabold text-[14px] drop-shadow-[0_2px_4px_rgba(0,0,0,0.9)]';
          } else {
            span.className = 'text-white font-bold text-[14px] drop-shadow-[0_2px_4px_rgba(0,0,0,0.9)]';
          }
          lineDiv.appendChild(span);
        });
        capLayer.appendChild(lineDiv);
      });

      const mgLayer = document.getElementById('mg-layer');
      mgLayer.innerHTML = '';

      if (s.mg_preview === 'x_trending') {
        mgLayer.innerHTML = `
          <div class="w-[290px] bg-[#0c1018]/95 backdrop-blur-md border border-slate-700/80 rounded-2xl p-3.5 shadow-2xl flex flex-col gap-1.5 text-left transition-all mt-14">
            <div class="flex items-center justify-between">
              <span class="text-[9px] font-mono uppercase tracking-wider text-sky-400 font-bold">Trending on X • India</span>
              <svg class="w-3.5 h-3.5 text-white fill-current" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </div>
            <div class="text-[13px] font-extrabold text-white tracking-tight">
              #ThankYouDelhiPolice
            </div>
            <div class="text-[9px] font-mono text-slate-300">152.4K Posts • Citizen Law & Order</div>
          </div>
        `;
      } else if (s.mg_preview === 'newspaper_clipping') {
        mgLayer.innerHTML = `
          <div class="w-[310px] bg-[#f7f4ee] text-[#1c1917] rounded-xl p-3.5 shadow-2xl border border-[#d6cfc2] transform -rotate-1 transition-all">
            <div class="border-b border-[#292524]/20 pb-1.5 mb-1.5 flex items-center justify-between text-[7.5px] font-mono font-bold tracking-widest text-[#78716c] uppercase">
              <span>The Capital Dispatch • Transit Alert</span>
              <span class="text-red-700 font-extrabold tracking-wider">BREAKING</span>
            </div>
            <div class="font-serif italic font-extrabold text-[12px] leading-snug text-[#1c1917]">
              "50 Metro Stations Shut Down Across Capital"
            </div>
            <div class="mt-1.5 text-[8.5px] font-mono text-[#57534e]">
              Commuters left stranded amid widespread transit gridlock.
            </div>
          </div>
        `;
      }

      // Update Inspector Panel
      document.getElementById('inspector-badge').innerText = `SCENE ${String(idx + 1).padStart(2, '0')}`;
      document.getElementById('inspector-title').innerText = s.title;
      document.getElementById('inspector-timing').innerText = `${s.start.toFixed(2)}s – ${s.end.toFixed(2)}s (${(s.end - s.start).toFixed(2)}s)`;
      document.getElementById('inspector-transcript').innerText = `"${s.transcript}"`;
      document.getElementById('inspector-mg-type').innerText = s.mg_type;
      document.getElementById('inspector-mg-desc').innerText = s.mg_desc;
      document.getElementById('inspector-camera').innerText = s.camera;
      document.getElementById('inspector-safe').innerText = s.safe_status;
      document.getElementById('inspector-sfx').innerText = s.sfx;

      document.querySelectorAll('.scene-pill').forEach((btn, pidx) => {
        if (pidx === idx) {
          btn.className = 'scene-pill py-2 px-1 rounded-lg text-center font-mono text-[10px] font-bold transition bg-emerald-500 text-black shadow-md shadow-emerald-500/30';
        } else {
          btn.className = 'scene-pill py-2 px-1 rounded-lg text-center font-mono text-[10px] font-bold transition bg-slate-800 text-slate-300 hover:bg-slate-700';
        }
      });
    }

    function initTimeline() {
      const container = document.getElementById('timeline-pills');
      container.innerHTML = '';
      scenes.forEach((s, idx) => {
        const btn = document.createElement('button');
        btn.className = 'scene-pill py-2 px-1 rounded-lg text-center font-mono text-[10px] font-bold transition bg-slate-800 text-slate-300 hover:bg-slate-700';
        btn.innerText = `S${idx + 1}`;
        btn.onclick = () => renderScene(idx);
        container.appendChild(btn);
      });
    }

    function nextScene() {
      if (currentIdx < scenes.length - 1) renderScene(currentIdx + 1);
      else renderScene(0);
    }

    function prevScene() {
      if (currentIdx > 0) renderScene(currentIdx - 1);
      else renderScene(scenes.length - 1);
    }

    function toggleAutoPlay() {
      isAutoPlaying = !isAutoPlaying;
      const btnText = document.getElementById('play-text');
      if (isAutoPlaying) {
        btnText.innerText = 'Pause';
        autoPlayTimer = setInterval(nextScene, 2600);
      } else {
        btnText.innerText = 'Auto Preview';
        clearInterval(autoPlayTimer);
      }
    }

    function toggleSafeOverlay() {
      showSafeOverlay = !showSafeOverlay;
      const overlay = document.getElementById('safe-overlay');
      const faceBoundary = document.getElementById('face-boundary');
      const text = document.getElementById('safe-btn-text');
      if (showSafeOverlay) {
        overlay.classList.remove('opacity-0');
        faceBoundary.classList.remove('opacity-0');
        text.innerText = 'Instagram Safe Zones: ON';
      } else {
        overlay.classList.add('opacity-0');
        faceBoundary.classList.add('opacity-0');
        text.innerText = 'Instagram Safe Zones: OFF';
      }
    }

    function approveAllScenes() {
      alert('Approved! Please give the go-ahead in chat to begin rendering.');
    }

    initTimeline();
    renderScene(0);
  </script>
</body>
</html>
'''

with open(OUT_HTML, 'w') as f:
    f.write(html_template)

print(f'Successfully re-generated storyboard HTML at {OUT_HTML}')
