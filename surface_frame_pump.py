#!/usr/bin/env python3
"""
surface_frame_pump.py — Frame-Accurate Playwright Animation Renderer
Renders animated HTML/DOM templates at 60 FPS via deterministic window.seekTo(t) hooks.
"""
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import io

CACHE_DIR = Path(__file__).parent / "sequence_cache"

class SurfacePump:
    def __init__(self, width=1080, height=1920):
        self.width = width
        self.height = height

    def render_sequence(self, html_path: str, duration: float, fps: int = 60, scene_id: str = None, force_rebuild: bool = False):
        """
        Renders an animated HTML file at specified FPS into an on-disk PNG sequence cache.
        Returns the path to the cached directory.
        """
        html_file = Path(html_path).resolve()
        if not html_file.exists():
            raise FileNotFoundError(f"HTML template not found: {html_file}")

        if scene_id is None:
            scene_id = html_file.stem

        out_dir = CACHE_DIR / scene_id
        out_dir.mkdir(parents=True, exist_ok=True)

        total_frames = int(round(duration * fps))
        
        # Check if already cached
        if not force_rebuild:
            existing_frames = list(out_dir.glob("frame_*.png"))
            if len(existing_frames) >= total_frames:
                print(f"⚡ [Cache Hit] {scene_id}: {len(existing_frames)} frames already present at {out_dir}")
                return out_dir

        print(f"🎬 [Playwright Pump] Rendering {scene_id} ({duration:.2f}s, {total_frames} frames @ {fps}fps)...")
        start_time = time.time()

        file_url = f"file://{html_file}"

        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--disable-web-security", "--allow-file-access-from-files"])
            page = browser.new_page(
                viewport={"width": self.width, "height": self.height},
                device_scale_factor=1
            )
            page.goto(file_url, wait_until="networkidle")

            # Verify window.seekTo is defined
            has_seek = page.evaluate("typeof window.seekTo === 'function'")
            if not has_seek:
                print(f"⚠️ Warning: window.seekTo(t) not found in {html_file.name}. Animations may not scrub.")

            for i in range(total_frames):
                t = i / float(fps)
                if has_seek:
                    page.evaluate(f"window.seekTo({t})")

                frame_path = out_dir / f"frame_{i:04d}.png"
                # omit_background=True preserves CSS alpha transparency
                page.screenshot(path=str(frame_path), omit_background=True, type="png")

                if (i + 1) % 30 == 0 or (i + 1) == total_frames:
                    pct = int(((i + 1) / total_frames) * 100)
                    elapsed = time.time() - start_time
                    fps_render = (i + 1) / max(0.1, elapsed)
                    print(f"  [{pct}%] Frame {i+1}/{total_frames} ({fps_render:.1f} fps rendering)...", end="\r")

            browser.close()

        total_elapsed = time.time() - start_time
        print(f"\n✅ Completed {scene_id} render in {total_elapsed:.1f}s ({total_frames / total_elapsed:.1f} fps)")
        return out_dir

if __name__ == "__main__":
    pump = SurfacePump()
    base_dir = Path(__file__).parent / "chrome_surfaces_clean_v7"
    
    # Render IMF card
    pump.render_sequence(str(base_dir / "s04_clean_card.html"), duration=4.14, fps=60, scene_id="s04_motion")
    
    # Render X Trends
    pump.render_sequence(str(base_dir / "s05_clean_trends.html"), duration=3.65, fps=60, scene_id="s05_motion")
    
    # Render Monumental Climax
    pump.render_sequence(str(base_dir / "s08_clean_monumental.html"), duration=2.40, fps=60, scene_id="s08_motion")
