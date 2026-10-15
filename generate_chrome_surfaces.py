#!/usr/bin/env python3
import os, subprocess, time
from PIL import Image

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
WORK_DIR = '/Users/sanskarsaraf/.gemini/antigravity/scratch/minpay/video_edit'
SURF_DIR = f'{WORK_DIR}/chrome_surfaces'
os.makedirs(SURF_DIR, exist_ok=True)

PHRASES = [
    {
        'id': 'b01',
        'lines': [
            [{'text': 'July mein', 'hl': 'gold'}, {'text': 'public', 'hl': 'white'}]
        ]
    },
    {
        'id': 'b02',
        'lines': [
            [{'text': 'inke saath', 'hl': 'white'}, {'text': 'thi...', 'hl': 'gold'}]
        ]
    },
    {
        'id': 'b03',
        'lines': [
            [{'text': 'lekin October mein jab', 'hl': 'white'}],
            [{'text': 'police ne', 'hl': 'gold'}, {'text': 'uthaya,', 'hl': 'white'}]
        ]
    },
    {
        'id': 'b04',
        'mg': 'x_trending',
        'lines': [
            [{'text': 'toh Delhi ne', 'hl': 'white'}, {'text': 'trend karwaya', 'hl': 'gold'}]
        ]
    },
    {
        'id': 'b05',
        'lines': [
            [{'text': 'kyun', 'hl': 'white'}, {'text': 'pata hai?', 'hl': 'gold'}]
        ]
    },
    {
        'id': 'b06',
        'lines': [
            [{'text': 'kyunki aam', 'hl': 'white'}, {'text': 'Delhi walon ko', 'hl': 'gold'}]
        ]
    },
    {
        'id': 'b07',
        'lines': [
            [{'text': 'subah kaam pe', 'hl': 'white'}],
            [{'text': 'nikalna hota hai.', 'hl': 'gold'}]
        ]
    },
    {
        'id': 'b08',
        'mg': 'newspaper_clipping',
        'lines': [
            [{'text': 'har 2 mahine mein', 'hl': 'white'}],
            [{'text': '50 metro station', 'hl': 'red'}, {'text': 'band karwaoge,', 'hl': 'white'}]
        ]
    },
    {
        'id': 'b09',
        'lines': [
            [{'text': 'traffic choke', 'hl': 'red'}, {'text': 'karoge toh', 'hl': 'white'}]
        ]
    },
    {
        'id': 'b10',
        'lines': [
            [{'text': 'log taaliyan', 'hl': 'white'}, {'text': 'thodi bajayenge!', 'hl': 'gold'}]
        ]
    },
    {
        'id': 'b11',
        'lines': [
            [{'text': 'flight se utha rahe the toh', 'hl': 'white'}],
            [{'text': 'co-passengers', 'hl': 'gold'}, {'text': 'hass rahe the.', 'hl': 'white'}]
        ]
    },
    {
        'id': 'b12',
        'lines': [
            [{'text': 'aur jab bus mein bitha ke', 'hl': 'white'}],
            [{'text': 'emergency reels', 'hl': 'red'}, {'text': 'bana rahe the,', 'hl': 'white'}]
        ]
    },
    {
        'id': 'b13',
        'lines': [
            [{'text': 'tab Rahul Gandhi', 'hl': 'gold'}, {'text': 'Chennai mein', 'hl': 'white'}],
            [{'text': 'Vijay ke saath', 'hl': 'white'}, {'text': 'chill kar raha tha.', 'hl': 'gold'}]
        ]
    },
    {
        'id': 'b14',
        'lines': [
            [{'text': 'aam janta', 'hl': 'gold'}, {'text': 'tumhare', 'hl': 'white'}]
        ]
    },
    {
        'id': 'b15',
        'climax': True,
        'lines': [
            [{'text': 'tamashon se', 'hl': 'gold'}],
            [{'text': 'PAK CHUKI HAI!', 'hl': 'gold', 'large': True}]
        ]
    }
]

def make_html(p):
    mg_html = ''
    if p.get('mg') == 'x_trending':
        mg_html = '''
    <div class="w-[840px] bg-gradient-to-b from-[#111827]/95 to-[#080d14]/95 backdrop-blur-2xl border border-sky-500/30 rounded-3xl p-7 shadow-[0_30px_70px_rgba(0,0,0,0.95),0_0_40px_rgba(56,189,248,0.2)] flex flex-col gap-4 text-left transform -rotate-0.5">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <span class="w-3 h-3 rounded-full bg-sky-400 animate-pulse"></span>
          <span class="text-[22px] font-mono uppercase tracking-wider text-sky-400 font-bold">Trending in India • Law & Order</span>
        </div>
        <svg class="w-7 h-7 text-white fill-current opacity-90" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-[40px] font-extrabold text-white tracking-tight">#ThankYouDelhiPolice</span>
        <svg class="w-8 h-8 text-sky-400 fill-current flex-shrink-0" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
      </div>
      <div class="text-[22px] font-mono text-slate-300 font-medium">152.4K Posts • Citizen Law & Order Monitoring</div>
      <div class="flex items-center justify-between pt-3 border-t border-slate-700/60 text-[20px] font-mono text-slate-400 font-semibold">
        <span class="flex items-center gap-2">💬 4.8K</span>
        <span class="flex items-center gap-2 text-emerald-400">🔁 19.2K</span>
        <span class="flex items-center gap-2 text-rose-400">❤️ 94.6K</span>
        <span class="flex items-center gap-2 text-sky-400">📊 1.4M</span>
      </div>
    </div>
        '''
    elif p.get('mg') == 'newspaper_clipping':
        mg_html = '''
    <div class="w-[880px] bg-[#fbf8f1] text-[#1c1917] rounded-3xl p-8 shadow-[0_30px_70px_rgba(0,0,0,0.95)] border-2 border-[#dcd4c5] transform -rotate-1 flex flex-col gap-3.5 text-left">
      <div class="border-b-2 border-[#292524]/20 pb-2.5 flex items-center justify-between text-[19px] font-mono font-bold tracking-widest text-[#78716c] uppercase">
        <span class="flex items-center gap-2">
          <span>📰 THE CAPITAL DISPATCH</span>
          <span class="text-[#a8a29e]">•</span>
          <span>VOL. XLVIII NO. 248</span>
        </span>
        <span class="bg-red-700 text-white text-[14px] px-3 py-1 rounded font-mono font-black tracking-wider">BREAKING ALERT</span>
      </div>
      <div class="relative inline-block my-1">
        <span class="absolute inset-x-[-10px] inset-y-[-2px] bg-yellow-300/80 -rotate-0.5 rounded-sm -z-0"></span>
        <span class="relative z-10 font-serif italic font-extrabold text-[38px] leading-tight text-[#1c1917]">
          "50 Metro Stations Shut Down Across Capital"
        </span>
      </div>
      <div class="text-[23px] font-mono text-[#44403c] font-semibold leading-relaxed border-l-4 border-red-700 pl-3">
        Commuters left stranded amid widespread transit gridlock.
      </div>
    </div>
        '''

    lines_html = ''
    for line in p['lines']:
        spans = []
        for w in line:
            if w.get('large'):
                spans.append(f'<span class="text-[#ffd84d] font-black text-[64px] uppercase tracking-wider drop-shadow-[0_6px_12px_rgba(0,0,0,0.95)]">{w["text"]}</span>')
            elif w['hl'] == 'gold':
                spans.append(f'<span class="text-[#ffd84d] font-extrabold text-[48px] drop-shadow-[0_4px_8px_rgba(0,0,0,0.9)]">{w["text"]}</span>')
            elif w['hl'] == 'red':
                spans.append(f'<span class="text-[#ff4b4b] font-extrabold text-[48px] drop-shadow-[0_4px_8px_rgba(0,0,0,0.9)]">{w["text"]}</span>')
            else:
                spans.append(f'<span class="text-white font-bold text-[48px] drop-shadow-[0_4px_8px_rgba(0,0,0,0.9)]">{w["text"]}</span>')
        lines_html += f'<div class="flex flex-wrap justify-center items-center gap-x-3 leading-tight">{" ".join(spans)}</div>\n'

    bottom_px = 250
    gap_class = "gap-7" if p.get('mg') else "gap-3"

    return f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&family=Playfair+Display:ital,wght@1,600;1,700;1,800&display=swap');
    body {{
      margin: 0;
      padding: 0;
      width: 1080px;
      height: 1920px;
      background: transparent;
      font-family: 'Plus Jakarta Sans', sans-serif;
      overflow: hidden;
    }}
    .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    .font-serif {{ font-family: 'Playfair Display', serif; }}
  </style>
</head>
<body class="relative w-[1080px] h-[1920px] select-none">
  <div class="absolute inset-x-8 bottom-[{bottom_px}px] flex flex-col items-center justify-end {gap_class} pointer-events-none text-center">
    {mg_html}
    <div class="flex flex-col items-center justify-center text-center gap-2.5 leading-tight">
      {lines_html}
    </div>
  </div>
</body>
</html>'''

def generate_all():
    t0 = time.time()
    print("🚀 Generating Chrome-native exact HTML surfaces at 1080x1920...")
    for p in PHRASES:
        pid = p['id']
        h_code = make_html(p)
        h_path = f'{SURF_DIR}/{pid}.html'
        png_path = f'{SURF_DIR}/{pid}.png'
        with open(h_path, 'w') as f:
            f.write(h_code)
        
        cmd = [
            CHROME,
            '--headless',
            '--disable-gpu',
            '--window-size=1080,1920',
            '--default-background-color=00000000',
            f'--screenshot={png_path}',
            f'file://{h_path}'
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  ✓ Rendered Chrome surface {pid}.png")
    print(f"🎉 All 15 Chrome surfaces generated in {time.time()-t0:.1f}s!")

if __name__ == '__main__':
    generate_all()
