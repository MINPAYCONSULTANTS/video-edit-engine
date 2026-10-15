#!/usr/bin/env python3
import os, json, base64

ART_DIR = '/Users/sanskarsaraf/.gemini/antigravity/brain/c3d97250-5f63-4415-8e05-a6900d445973'
COMP_DIR = f'{ART_DIR}'
OUT_HTML = f'{ART_DIR}/approval_storyboard.html'

scenes = [
    {
        'id': 's01',
        'title': 'The Terror Precedent (26/11 Hook)',
        'start': 0.57, 'end': 3.20,
        'frame_file': 'storyboard_pxl3_s01.jpg',
        'transcript': 'Jis desh ne Mumbai pe 26/11 karwaya tha...',
        'highlight_text': '26/11 karwaya tha...',
        'camera': 'Wide (1.00x) Grounded & Direct',
        'mg_type': 'Security Intelligence Record (26/11 Precedent)',
        'mg_desc': 'Dark crimson intelligence alert card positioned on lower torso. Highlights cross-border terror sponsorship.',
        'sfx': 'Deep Cinematic Sub-Bass Rumble',
        'safe_status': 'PASS (100% Off Face • Lower Third)'
    },
    {
        'id': 's02',
        'title': 'The Agitation Pivot',
        'start': 3.50, 'end': 5.80,
        'frame_file': 'storyboard_pxl3_s02.jpg',
        'transcript': 'agar woh tumhare protest ke liye taaliyan baja raha hai,',
        'highlight_text': 'protest ke liye taaliyan',
        'camera': 'Smooth Push Ease-In (1.00x → 1.07x)',
        'mg_type': 'Kinetic Dialogue Subtitle',
        'mg_desc': 'Clean conversational framing without visual clutter to let the gravity of the rhetorical question land.',
        'sfx': 'Clean Dialogue Studio Master',
        'safe_status': 'PASS (100% Off Face)'
    },
    {
        'id': 's03',
        'title': 'The Psychological Warfare Verdict',
        'start': 5.80, 'end': 8.36,
        'frame_file': 'storyboard_pxl3_s03.jpg',
        'transcript': 'toh tum krantikari nahi, UNKE PUPPET HO!',
        'highlight_text': 'UNKE PUPPET HO!',
        'camera': 'Medium Held (1.07x)',
        'mg_type': 'Psychological Warfare Status Card',
        'mg_desc': 'Amber tactical banner: "STATUS: COMPROMISED". Subtitle: "UNKE PUPPET HO!" in bold red all-caps.',
        'sfx': '🔊 Tactile Mechanical Snap (-22 dB)',
        'safe_status': 'PASS (Lower Torso Anchor)'
    },
    {
        'id': 's04',
        'title': 'Geopolitical Reality',
        'start': 9.14, 'end': 11.82,
        'frame_file': 'storyboard_pxl3_s04.jpg',
        'transcript': 'Dushman desh kabhi tumhari democracy ke liye dua nahi maangta.',
        'highlight_text': 'democracy ke liye dua nahi maangta.',
        'camera': 'Smooth Eased Zoom-Out (1.07x → 1.00x)',
        'mg_type': 'Geopolitical Intelligence Badge',
        'mg_desc': 'Sleek frosted glass pill: "GEOPOLITICAL REALITY • ZERO ALLIANCE".',
        'sfx': 'Subtle Air Whoosh',
        'safe_status': 'PASS (100% Off Face)'
    },
    {
        'id': 's05',
        'title': 'Military Border Deterrence',
        'start': 12.18, 'end': 14.50,
        'frame_file': 'storyboard_pxl3_s05.jpg',
        'transcript': 'Border pe woh humari army se jeet nahi sakte,',
        'highlight_text': 'army se jeet nahi sakte,',
        'camera': 'Smooth Push Ease-In (1.00x → 1.07x)',
        'mg_type': 'Indian Armed Forces Defense Shield',
        'mg_desc': 'Emerald tactical border card: "🛡️ INDIAN ARMED FORCES • UNCONQUERABLE BORDER".',
        'sfx': 'Military Radio Chirp / Metallic Clink',
        'safe_status': 'PASS (100% Off Face)'
    },
    {
        'id': 's06',
        'title': 'Economic Velocity Disparity',
        'start': 14.50, 'end': 16.91,
        'frame_file': 'storyboard_pxl3_s06.jpg',
        'transcript': 'economic growth mein woh humse muqabla nahi kar sakte,',
        'highlight_text': 'humse muqabla nahi kar sakte,',
        'camera': 'Medium Held (1.07x)',
        'mg_type': 'Economic Growth Disparity Card',
        'mg_desc': 'Electric cyan card: "📈 ECONOMIC VELOCITY • 5TH LARGEST ECONOMY".',
        'sfx': 'Upward Metric Swell',
        'safe_status': 'PASS (100% Off Face)'
    },
    {
        'id': 's07',
        'title': 'Domestic Friction Point',
        'start': 17.39, 'end': 19.80,
        'frame_file': 'storyboard_pxl3_s07.jpg',
        'transcript': 'isliye jaise hi Delhi mein sadkein band hoti hain,',
        'highlight_text': 'sadkein band hoti hain,',
        'camera': 'Smooth Eased Zoom-Out (1.07x → 1.00x)',
        'mg_type': 'Transit Disruption Callout',
        'mg_desc': 'Clean subtitle emphasis on capital road blocks.',
        'sfx': 'Low Tension Drone',
        'safe_status': 'PASS (100% Off Face)'
    },
    {
        'id': 's08',
        'title': 'Coordinated Foreign Bot Farms',
        'start': 19.80, 'end': 22.45,
        'frame_file': 'storyboard_pxl3_s08.jpg',
        'transcript': 'unke bot farms tumhare hashtags trend karwane lagte hain!',
        'highlight_text': 'hashtags trend karwane lagte hain!',
        'camera': 'Smooth Push Ease-In (1.00x → 1.08x)',
        'mg_type': '3.5D Coordinated Bot Farms HUD',
        'mg_desc': 'Glassmorphic card: "#ChokeCapital • 240,000+ Automated Proxy Accounts • BOT DETECTION: 89.4%".',
        'sfx': 'Cyber Typing & Mechanical Notification Ping',
        'safe_status': 'PASS (100% Off Face • Lower Torso)'
    },
    {
        'id': 's09',
        'title': 'Constitutional Right to Dissent',
        'start': 22.80, 'end': 25.73,
        'frame_file': 'storyboard_pxl3_s09.jpg',
        'transcript': 'Critique any government you want, that is your right.',
        'highlight_text': 'THAT IS YOUR RIGHT.',
        'camera': 'Medium Held (1.08x)',
        'mg_type': 'Article 19(1)(a) Constitutional Badge',
        'mg_desc': 'Emerald constitutional emblem: "ARTICLE 19(1)(a) • RIGHT TO PEACEFUL DISSENT: PROTECTED".',
        'sfx': 'Subtle Page Turn',
        'safe_status': 'PASS (100% Off Face)'
    },
    {
        'id': 's10',
        'title': 'Weaponized Dissent Dossier',
        'start': 26.00, 'end': 28.42,
        'frame_file': 'storyboard_pxl3_s10.jpg',
        'transcript': 'Lekin jis din tumhara protest dushman desh ka weapon ban jaye,',
        'highlight_text': 'dushman desh ka weapon ban jaye,',
        'camera': 'Smooth Eased Zoom-Out (1.08x → 1.00x)',
        'mg_type': 'Declassified Threat Audit Dossier (Vox Style)',
        'mg_desc': 'Aged newsprint file folder with red diagonal stamp: [WEAPONIZED DISSENT] and yellow highlighter wipe.',
        'sfx': '🔊 Heavy Paper Dossier Slam (-20 dB)',
        'safe_status': 'PASS (100% Off Face • Lower Third)'
    },
    {
        'id': 's11',
        'title': 'The Climax Buildup',
        'start': 28.88, 'end': 31.40,
        'frame_file': 'storyboard_pxl3_s11.jpg',
        'transcript': 'uss din tum deshbhakt nahi,',
        'highlight_text': 'deshbhakt nahi,',
        'camera': 'Smooth Push Ease-In (1.00x → 1.08x Climax Punch)',
        'mg_type': 'Pre-Climax Tension Hold',
        'mg_desc': 'Camera pushes toward speaker eyes at 35% height. Deep pause before the final verdict.',
        'sfx': 'Sub-Bass Tension Rise',
        'safe_status': 'PASS (100% Off Face)'
    },
    {
        'id': 's12',
        'title': 'The Final Verdict (Climax Impact)',
        'start': 31.40, 'end': 35.20,
        'frame_file': 'storyboard_pxl3_s12.jpg',
        'transcript': 'tum NATIONAL LIABILITY BAN JAATE HO!',
        'highlight_text': 'NATIONAL LIABILITY BAN JAATE HO!',
        'camera': 'Extreme Close Heroic Hold (1.08x)',
        'mg_type': 'High-Impact Editorial Climax Typography',
        'mg_desc': 'Huge all-caps punch: "NATIONAL LIABILITY" in crimson red with multi-layer drop shadows.',
        'sfx': '💥 Heavy Cinematic Sub-Boom Impact (-18 dB)',
        'safe_status': 'PASS (Anchored 250px from Bottom)'
    }
]

html_cards = []
for s in scenes:
    img_path = f'{COMP_DIR}/{s["frame_file"]}'
    with open(img_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    data_uri = f'data:image/jpeg;base64,{b64}'
    
    html_cards.append(f'''
    <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl flex flex-col md:flex-row gap-6 items-center">
      <div class="w-full md:w-[260px] flex-shrink-0 relative rounded-2xl overflow-hidden border border-slate-700 shadow-lg">
        <img src="{data_uri}" class="w-full h-auto object-cover" alt="{s['title']}">
        <span class="absolute top-3 left-3 bg-black/80 backdrop-blur-md text-white font-mono text-xs px-2.5 py-1 rounded-full font-bold">
          {s['id'].upper()} • {s['start']:.2f}s - {s['end']:.2f}s
        </span>
      </div>
      <div class="flex-1 flex flex-col justify-between h-full w-full">
        <div>
          <div class="flex items-center justify-between gap-3 mb-2">
            <h3 class="text-xl font-black text-white">{s['title']}</h3>
            <span class="text-xs font-mono font-bold px-3 py-1 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
              {s['safe_status']}
            </span>
          </div>
          <p class="text-slate-300 font-medium text-base mb-3 leading-relaxed">
            "{s['transcript']}"
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3 text-sm">
            <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700/50">
              <span class="text-slate-400 font-mono text-xs block uppercase">Camera Motion</span>
              <span class="text-white font-semibold">{s['camera']}</span>
            </div>
            <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700/50">
              <span class="text-slate-400 font-mono text-xs block uppercase">Sound Cue</span>
              <span class="text-amber-300 font-semibold">{s['sfx']}</span>
            </div>
          </div>
          <div class="bg-slate-800/40 p-3 rounded-xl border border-slate-700/40 text-xs">
            <span class="text-sky-400 font-mono font-bold block uppercase mb-1">Visual Element: {s['mg_type']}</span>
            <span class="text-slate-300">{s['mg_desc']}</span>
          </div>
        </div>
      </div>
    </div>
    ''')

full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Approval Storyboard: PXL_20261014_062026247</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen py-12 px-6">
  <div class="max-w-5xl mx-auto space-y-8">
    <!-- Header -->
    <div class="bg-gradient-to-r from-red-950/60 via-slate-900 to-slate-900 border border-red-900/40 rounded-3xl p-8 shadow-2xl">
      <div class="flex flex-wrap items-center justify-between gap-4 mb-4">
        <span class="px-3.5 py-1.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/40 font-mono text-xs font-bold uppercase tracking-wider">
          🔒 Production Approval Gate
        </span>
        <span class="text-slate-400 font-mono text-sm">Source: PXL_20261014_062026247.mp4 (35.52s)</span>
      </div>
      <h1 class="text-3xl md:text-4xl font-black text-white tracking-tight mb-3">
        Interactive Editorial Storyboard: National Security & Proxy Agitations
      </h1>
      <p class="text-slate-300 text-base leading-relaxed max-w-3xl">
        Every graphic surface is rendered directly via <strong>Google Chrome Headless at 1080x1920</strong> with spring physics (<span class="text-sky-400 font-mono">cubic-bezier(0.175, 0.885, 0.32, 1.275)</span>), ambient breathing float, and tactile micro-SFX cues. Subtitles and graphic elements are anchored safely on the lower third to guarantee zero facial obstruction.
      </p>
    </div>

    <!-- Scene Cards -->
    <div class="space-y-6">
      {''.join(html_cards)}
    </div>

    <!-- Interactive Approval Box -->
    <div class="bg-slate-900 border-2 border-emerald-500/40 rounded-3xl p-8 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-6">
      <div>
        <h3 class="text-2xl font-black text-white mb-2">Ready to Render Master Video?</h3>
        <p class="text-slate-300 text-sm max-w-xl">
          Review the 12 scene compositions above. If you want any text, color, timing, or element adjusted, specify your feedback. If you approve, confirm to trigger the full 4K-to-1080p master render.
        </p>
      </div>
      <div class="flex-shrink-0">
        <div class="px-8 py-4 rounded-2xl bg-emerald-500 text-slate-950 font-black text-lg shadow-[0_0_30px_rgba(16,185,129,0.4)] flex items-center gap-3 select-none">
          <span>✓</span> STORYBOARD READY FOR APPROVAL
        </div>
      </div>
    </div>
  </div>
</body>
</html>'''

with open(OUT_HTML, 'w') as f:
    f.write(full_html)
print(f'🎉 Interactive Storyboard successfully compiled to: {OUT_HTML}')
