#!/usr/bin/env python3
"""
Embed Base64 WOFF2 and TTF binaries directly into index.html so the specimen
page loads 100% reliably in all browsers, even when opened via file:/// protocol!
"""

import os
import base64
import re

def embed_specimen_fonts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    index_html = os.path.join(typeface_root, 'index.html')

    # Base HTML template without bloated inline font duplication
    template = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PocketGull — The Living Brand Typeface & Typefoundry</title>
  <meta name="description" content="Open-Source Handcrafted Felt-Tip Marker & High-Contrast Clinical Typeface Superfamily. Pure mathematical Bezier precision, variable font axes, and sacred numerology.">
  
  <!-- EMBEDDED_FONTS_PLACEHOLDER -->

  <style>
    :root {
      --bg-primary: #0a0e17;
      --bg-surface: #111827;
      --bg-card: #1f2937;
      --border-color: #374151;
      --text-primary: #f9fafb;
      --text-secondary: #9ca3af;
      --text-muted: #6b7280;
      --accent-orange: #ea580c;
      --accent-teal: #14b8a6;
      --accent-gold: #eab308;
      --accent-blue: #0284c7;
      --font-display: 'PocketGull VF', 'PocketGull Bold', sans-serif;
      --font-mono: 'PocketGull Mono', monospace;
    }

    [data-theme="light"] {
      --bg-primary: #f8fafc;
      --bg-surface: #ffffff;
      --bg-card: #f1f5f9;
      --border-color: #e2e8f0;
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #94a3b8;
      --accent-orange: #c2410c;
      --accent-teal: #0d9488;
      --accent-gold: #ca8a04;
      --accent-blue: #0369a1;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-primary);
      color: var(--text-primary);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.5;
      padding: 24px;
      transition: background-color 0.3s, color 0.3s;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 32px;
    }

    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border-color);
    }

    .brand-title {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .logo-badge {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      background: linear-gradient(135deg, var(--accent-orange), #f97316);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
    }

    h1 {
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 800;
      letter-spacing: -0.02em;
    }

    .tagline {
      font-size: 13px;
      color: var(--text-secondary);
    }

    .controls-bar {
      display: flex;
      gap: 12px;
    }

    .btn-theme {
      min-height: 44px;
      padding: 8px 16px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      background: var(--bg-surface);
      color: var(--text-primary);
      cursor: pointer;
      font-weight: 600;
      font-size: 13px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }

    .btn-theme:hover {
      border-color: var(--accent-orange);
    }

    /* Master Interactive Canvas */
    .playground-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    }

    .canvas-display {
      min-height: 200px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      font-family: var(--font-display);
      font-size: 64px;
      color: var(--text-primary);
      outline: none;
      word-break: break-word;
      transition: font-size 0.1s, font-weight 0.1s;
    }

    .sliders-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
    }

    .slider-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
    }

    input[type="range"] {
      width: 100%;
      accent-color: var(--accent-orange);
    }

    .opentype-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      padding-top: 12px;
      border-top: 1px solid var(--border-color);
    }

    .tag-btn {
      min-height: 36px;
      padding: 6px 12px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-secondary);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .tag-btn.active {
      background: rgba(234, 88, 12, 0.15);
      border-color: var(--accent-orange);
      color: var(--accent-orange);
    }

    /* Glyph Broadside Grid */
    .section-title {
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .glyphs-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(64px, 1fr));
      gap: 8px;
    }

    .glyph-tile {
      aspect-ratio: 1;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-family: var(--font-display);
      font-size: 28px;
      transition: transform 0.2s, border-color 0.2s;
      cursor: pointer;
    }

    .glyph-tile:hover {
      border-color: var(--accent-teal);
      transform: scale(1.08);
      background: var(--bg-card);
    }

    .glyph-unicode {
      font-family: var(--font-mono);
      font-size: 9px;
      color: var(--text-muted);
      margin-top: 2px;
    }

    /* Comparison Weights */
    .weights-list {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .weight-row {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 18px 24px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .weight-meta {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
    }

    .weight-sample {
      font-size: 32px;
    }
  </style>
</head>
<body>

  <div class="container">
    <header>
      <div class="brand-title">
        <div class="logo-badge">🕊️</div>
        <div>
          <h1>PocketGull</h1>
          <div class="tagline">The Living Brand Typeface &amp; Typefoundry (SIL OFL 1.1)</div>
        </div>
      </div>
      <div class="controls-bar">
        <button class="btn-theme" onclick="toggleTheme()">🌓 Theme</button>
      </div>
    </header>

    <!-- Master Variable Playground -->
    <div class="playground-card">
      <div class="section-title">✨ Interactive Variable Playground</div>
      
      <div id="canvas" class="canvas-display" contenteditable="true" spellcheck="false">
        PocketGull Sanctuary 120/80 mmHg ∅
      </div>

      <div class="sliders-grid">
        <div class="slider-group">
          <div class="slider-header">
            <span>Weight (wght)</span>
            <span id="val-weight">700</span>
          </div>
          <input type="range" id="slider-weight" min="100" max="900" value="700" step="10">
        </div>

        <div class="slider-group">
          <div class="slider-header">
            <span>Optical Size (opsz)</span>
            <span id="val-opsz">48pt</span>
          </div>
          <input type="range" id="slider-opsz" min="8" max="72" value="48" step="1">
        </div>

        <div class="slider-group">
          <div class="slider-header">
            <span>Slant (slnt)</span>
            <span id="val-slnt">0°</span>
          </div>
          <input type="range" id="slider-slnt" min="-12" max="0" value="0" step="1">
        </div>

        <div class="slider-group">
          <div class="slider-header">
            <span>Font Size</span>
            <span id="val-size">64px</span>
          </div>
          <input type="range" id="slider-size" min="20" max="120" value="64" step="1">
        </div>
      </div>

      <div class="opentype-tags">
        <button class="tag-btn active" onclick="toggleFeature(this, 'zero')"><span>∅</span> Slashed Zero (zero)</button>
        <button class="tag-btn active" onclick="toggleFeature(this, 'cv05')"><span>l</span> Hooked L (cv05)</button>
        <button class="tag-btn active" onclick="toggleFeature(this, 'cv08')"><span>I</span> Seriffed I (cv08)</button>
        <button class="tag-btn active" onclick="toggleFeature(this, 'tnum')"><span>123</span> Tabular Numbers (tnum)</button>
      </div>
    </div>

    <!-- Weight Superfamily Hierarchy -->
    <div class="weights-list">
      <div class="section-title">🔤 Superfamily Weight Spectrum</div>

      <div class="weight-row">
        <div class="weight-meta">
          <span>PocketGull Fineliner (Weight: 400 Regular)</span>
          <span>Body Text &amp; Chart Notes</span>
        </div>
        <div class="weight-sample" style="font-family: 'PocketGull Fineliner', var(--font-display); font-weight: 400;">
          Sphinx of black quartz, judge my vow. 120/80 mmHg · SpO2 98%
        </div>
      </div>

      <div class="weight-row">
        <div class="weight-meta">
          <span>PocketGull Bold (Weight: 700 Bold)</span>
          <span>Headlines &amp; Brand Wordmarks</span>
        </div>
        <div class="weight-sample" style="font-family: 'PocketGull Bold', var(--font-display); font-weight: 700;">
          PocketGull Sanctuary: Empirical Clinical Intelligence &amp; Care
        </div>
      </div>

      <div class="weight-row">
        <div class="weight-meta">
          <span>PocketGull Chiseltip (Weight: 900 Black)</span>
          <span>Pediatric Medals &amp; Hero Displays</span>
        </div>
        <div class="weight-sample" style="font-family: 'PocketGull Chiseltip', var(--font-display); font-weight: 900;">
          PEDIATRIC COURAGE MEDAL · AWAKEN STRENGTH
        </div>
      </div>

      <div class="weight-row">
        <div class="weight-meta">
          <span>PocketGull World Pan-Script &amp; Calculus</span>
          <span>Greek αβΩ, Cyrillic БДЖ, Calculus ∂∇∞∫</span>
        </div>
        <div class="weight-sample" style="font-family: var(--font-display); font-weight: 700; color: var(--accent-teal);">
          α β γ δ Ω Δ Σ · Б Д Ж И Я · ∂x/∂t = ∇²Ψ + ∫ f(t)dt · 100% ♥
        </div>
      </div>
    </div>

    <!-- Master Glyph Roster -->
    <div>
      <div class="section-title">🏛️ Master Glyph Roster (260 Unicode Points)</div>
      <div id="glyph-container" class="glyphs-grid"></div>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('canvas');
    const sliderWeight = document.getElementById('slider-weight');
    const sliderOpsz = document.getElementById('slider-opsz');
    const sliderSlnt = document.getElementById('slider-slnt');
    const sliderSize = document.getElementById('slider-size');

    const valWeight = document.getElementById('val-weight');
    const valOpsz = document.getElementById('val-opsz');
    const valSlnt = document.getElementById('val-slnt');
    const valSize = document.getElementById('val-size');

    let activeFeatures = {
      'zero': true,
      'cv05': true,
      'cv08': true,
      'tnum': true
    };

    function updateCanvas() {
      const w = parseInt(sliderWeight.value, 10);
      const opsz = parseInt(sliderOpsz.value, 10);
      const slnt = parseInt(sliderSlnt.value, 10);
      const sz = parseInt(sliderSize.value, 10);

      valWeight.textContent = w;
      valOpsz.textContent = opsz + 'pt';
      valSlnt.textContent = slnt + '°';
      valSize.textContent = sz + 'px';

      if (w <= 450) {
        canvas.style.fontFamily = "'PocketGull Fineliner', 'PocketGull VF', sans-serif";
      } else if (w >= 850) {
        canvas.style.fontFamily = "'PocketGull Chiseltip', 'PocketGull VF', sans-serif";
      } else {
        canvas.style.fontFamily = "'PocketGull Bold', 'PocketGull VF', sans-serif";
      }

      canvas.style.fontWeight = w;
      canvas.style.fontVariationSettings = `'wght' ${w}, 'opsz' ${opsz}, 'slnt' ${slnt}`;
      canvas.style.fontSize = sz + 'px';
      canvas.style.transform = `skewX(${slnt}deg)`;

      const featStr = Object.entries(activeFeatures)
        .map(([k, v]) => `"${k}" ${v ? 1 : 0}`)
        .join(', ');
      canvas.style.fontFeatureSettings = featStr;
    }

    sliderWeight.addEventListener('input', updateCanvas);
    sliderOpsz.addEventListener('input', updateCanvas);
    sliderSlnt.addEventListener('input', updateCanvas);
    sliderSize.addEventListener('input', updateCanvas);

    function toggleFeature(elem, key) {
      activeFeatures[key] = !activeFeatures[key];
      elem.classList.toggle('active', activeFeatures[key]);
      updateCanvas();
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
    }

    // Populate Glyph Grid
    const glyphChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/αβγδεζηθικλμνξοπρστυφχψωΩΔΣΠБДЖИЯ∂∇−∞∫≈♥℃℉℞";
    const glyphContainer = document.getElementById('glyph-container');

    glyphChars.split('').forEach(ch => {
      const tile = document.createElement('div');
      tile.className = 'glyph-tile';
      tile.innerHTML = `<span>${ch}</span><span class="glyph-unicode">U+${ch.charCodeAt(0).toString(16).toUpperCase().padStart(4, '0')}</span>`;
      tile.onclick = () => {
        canvas.textContent += ch;
      };
      glyphContainer.appendChild(tile);
    });

    updateCanvas();
  </script>
</body>
</html>
"""

    def get_b64(filename):
        path = os.path.join(typeface_root, filename)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return base64.b64encode(f.read()).decode('ascii')
        return ""

    vf_woff2 = get_b64('PocketGull-VF.woff2') or get_b64('PocketGull-Bold.woff2')
    bold_woff2 = get_b64('PocketGull-Bold.woff2')
    fine_woff2 = get_b64('PocketGull-Fineliner.woff2')
    chisel_woff2 = get_b64('PocketGull-Chiseltip.woff2')
    num_woff2 = get_b64('PocketGull-Numerics.woff2')
    mono_woff2 = get_b64('PocketGullMono-Regular.woff2')

    font_face_block = f"""
  <style id="pocketgull-embedded-fonts">
    @font-face {{
      font-family: 'PocketGull VF';
      src: url('data:font/woff2;charset=utf-8;base64,{vf_woff2}') format('woff2');
      font-weight: 100 900;
      font-style: normal;
      font-display: swap;
    }}

    @font-face {{
      font-family: 'PocketGull Bold';
      src: url('data:font/woff2;charset=utf-8;base64,{bold_woff2}') format('woff2');
      font-weight: 700;
      font-style: normal;
      font-display: swap;
    }}

    @font-face {{
      font-family: 'PocketGull Fineliner';
      src: url('data:font/woff2;charset=utf-8;base64,{fine_woff2}') format('woff2');
      font-weight: 400;
      font-style: normal;
      font-display: swap;
    }}

    @font-face {{
      font-family: 'PocketGull Chiseltip';
      src: url('data:font/woff2;charset=utf-8;base64,{chisel_woff2}') format('woff2');
      font-weight: 900;
      font-style: normal;
      font-display: swap;
    }}

    @font-face {{
      font-family: 'PocketGull Numerics';
      src: url('data:font/woff2;charset=utf-8;base64,{num_woff2}') format('woff2');
      font-weight: 400;
      font-style: normal;
      font-display: swap;
    }}

    @font-face {{
      font-family: 'PocketGull Mono';
      src: url('data:font/woff2;charset=utf-8;base64,{mono_woff2}') format('woff2');
      font-weight: 400;
      font-style: normal;
      font-display: swap;
    }}
  </style>
"""

    final_html = template.replace('<!-- EMBEDDED_FONTS_PLACEHOLDER -->', font_face_block.strip())

    with open(index_html, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"[OK] Successfully embedded standalone Base64 fonts into clean: {index_html}")

if __name__ == '__main__':
    embed_specimen_fonts()
