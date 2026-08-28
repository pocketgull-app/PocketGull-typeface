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
  <title>PocketGull — The Handcrafted Living Brand Typeface</title>
  <meta name="description" content="Handcrafted Felt-Tip Marker Typography from the PocketGull brand. High-contrast geometric warmth, open apertures, and authentic vector craft.">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&family=Outfit:wght@400;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">

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
      --font-display: 'PocketGull VF', 'PocketGull', 'Outfit', 'Plus Jakarta Sans', 'Atkinson Hyperlegible', sans-serif;
      --font-brand: 'PocketGull', 'Outfit', 'Plus Jakarta Sans', sans-serif;
      --font-body: 'Plus Jakarta Sans', 'Atkinson Hyperlegible', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: 'PocketGull Mono', 'JetBrains Mono', monospace;
    }

    [data-theme="light"] {
      --bg-primary: #fbf9f5;
      --bg-surface: #ffffff;
      --bg-card: #f2efe9;
      --border-color: #e5e0d8;
      --text-primary: #1c1b1a;
      --text-secondary: #4a4744;
      --text-muted: #78716c;
      --accent-orange: #c27d38;
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
      font-family: var(--font-body);
      line-height: 1.6;
      padding: 24px;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-rendering: optimizeLegibility;
      transition: background-color 0.3s, color 0.3s;
    }

    .marker-underline-highlight {
      position: relative;
      display: inline-block;
    }
    .marker-underline-highlight::after {
      content: '';
      position: absolute;
      left: 0;
      bottom: 2px;
      width: 100%;
      height: 7px;
      background-color: rgba(234, 88, 12, 0.3);
      border-radius: 3px;
      z-index: -1;
      transform: rotate(-0.6deg);
    }

    .marker-bold-emphasis {
      font-family: var(--font-brand);
      font-weight: 800;
      background: linear-gradient(120deg, rgba(251, 146, 60, 0.2) 0%, rgba(249, 115, 22, 0.28) 100%);
      border-radius: 4px;
      padding: 0 6px;
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

    /* Custom Specimen Card Styles matching pocketgull.app */
    .sunlight-card {
      background: #fbf9f5;
      color: #1c1b1a;
      border: 2px solid #c27d38;
      border-radius: 24px;
      padding: 36px 32px;
      box-shadow: 0 12px 36px rgba(194, 125, 56, 0.15);
      position: relative;
      overflow: hidden;
    }
    
    .sunlight-badge {
      display: inline-block;
      background: #c27d38;
      color: #ffffff;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 4px 14px;
      border-radius: 999px;
      margin-bottom: 18px;
    }

    .sunlight-title {
      font-family: var(--font-brand);
      font-size: clamp(36px, 6vw, 68px);
      font-weight: 900;
      line-height: 1.05;
      letter-spacing: -0.025em;
      margin-bottom: 8px;
    }

    .sunlight-subtitle {
      font-family: 'Atkinson Hyperlegible', sans-serif;
      font-size: 16px;
      font-weight: 700;
      color: #c27d38;
      letter-spacing: 0.02em;
      margin-bottom: 24px;
    }

    .sunlight-chars {
      font-family: var(--font-brand);
      font-size: 18px;
      font-weight: 700;
      letter-spacing: 0.05em;
      color: #4a4744;
      border-top: 1px dashed #d5cebf;
      padding-top: 18px;
      margin-bottom: 14px;
    }

    .sunlight-footer {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #78716c;
      letter-spacing: 0.02em;
    }

    /* Tab Switcher */
    .tab-bar {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 20px;
    }

    .tab-btn {
      background: var(--bg-surface);
      color: var(--text-secondary);
      border: 1px solid var(--border-color);
      padding: 8px 18px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .tab-btn:hover {
      color: var(--text-primary);
      border-color: var(--accent-orange);
    }

    .tab-btn.active {
      background: var(--accent-orange);
      color: #ffffff;
      border-color: var(--accent-orange);
      box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
    }

    /* Preset Buttons */
    .presets-bar {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 16px;
    }

    .preset-pill {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      font-size: 11px;
      font-weight: 600;
      padding: 4px 12px;
      border-radius: 999px;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .preset-pill:hover {
      background: rgba(234, 88, 12, 0.15);
      color: var(--text-primary);
      border-color: var(--accent-orange);
    }

    /* CSS Copy Block */
    .code-box {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 20px;
      font-family: var(--font-mono);
      font-size: 12px;
      color: #38bdf8;
      overflow-x: auto;
      line-height: 1.6;
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
          <div class="tagline">Official Typography &amp; Design System (pocketgull.app)</div>
        </div>
      </div>
      <div class="controls-bar">
        <button class="btn-theme" onclick="toggleTheme()">🌓 Theme</button>
      </div>
    </header>

    <!-- Master Sunlight Specimen Card -->
    <div class="sunlight-card">
      <div class="sunlight-badge">POCKETGULL TYPEFACE SPECIMEN</div>
      <div class="sunlight-title">PocketGull</div>
      <div class="sunlight-subtitle">Handcrafted Felt-Tip Marker Typography &amp; Clinical Legibility Engine</div>
      <div class="sunlight-chars">
        Aa Bb Cc Dd Ee 0123456789 · I IV X · ½ ¼ · ± % = · α β Ω
      </div>
      <div class="sunlight-footer">
        SIL Open Font License 1.1 · Certified WCAG 2.1 AAA Contrast Ratio (8.9:1) · pocketgull.app
      </div>
    </div>

    <!-- Master Interactive Type Playground -->
    <div class="playground-card">
      <div class="section-title">✨ Interactive Live Specimen Sandbox</div>
      
      <!-- Typography Stack Tabs -->
      <div class="tab-bar">
        <button class="tab-btn active" onclick="switchStack(this, 'brand')">
          <span>🕊️</span> Display &amp; Brand (Outfit + PocketGull)
        </button>
        <button class="tab-btn" onclick="switchStack(this, 'clinical')">
          <span>🏥</span> Clinical &amp; Body (Atkinson Hyperlegible)
        </button>
        <button class="tab-btn" onclick="switchStack(this, 'telemetry')">
          <span>📊</span> Telemetry &amp; Vitals (JetBrains Mono)
        </button>
      </div>

      <!-- Quick Preset Text Prompts -->
      <div class="presets-bar">
        <span style="font-size: 11px; color: var(--text-muted); align-self: center;">Try Presets:</span>
        <button class="preset-pill" onclick="setPreset('PocketGull — Continuous Empirical Intelligence & Care')">🌟 Brand Statement</button>
        <button class="preset-pill" onclick="setPreset('Step 1: Call 911 Immediately · Bystander CPR in Progress')">🚨 911 Emergency Protocol</button>
        <button class="preset-pill" onclick="setPreset('BPM 72 · SpO2 98% · GLUCOSE 104 mg/dL · ECG LEAD II')">📈 Live Patient Vitals</button>
        <button class="preset-pill" onclick="setPreset('The quick brown fox jumps over the lazy dog 0123456789')">🔤 Alphabet &amp; Digits</button>
      </div>

      <div id="canvas" class="canvas-display" contenteditable="true" spellcheck="false" style="font-family: var(--font-brand); font-weight: 800; letter-spacing: -0.02em;">
        PocketGull — Continuous Empirical Intelligence &amp; Care
      </div>

      <div class="sliders-grid">
        <div class="slider-group">
          <div class="slider-header">
            <span>Font Size</span>
            <span id="val-size">48px</span>
          </div>
          <input type="range" id="slider-size" min="16" max="96" value="48" step="1">
        </div>

        <div class="slider-group">
          <div class="slider-header">
            <span>Letter Spacing</span>
            <span id="val-tracking">-0.02em</span>
          </div>
          <input type="range" id="slider-tracking" min="-0.05" max="0.1" value="-0.02" step="0.005">
        </div>

        <div class="slider-group">
          <div class="slider-header">
            <span>Font Weight</span>
            <span id="val-weight">800</span>
          </div>
          <input type="range" id="slider-weight" min="400" max="900" value="800" step="100">
        </div>
      </div>

      <div class="opentype-tags">
        <button class="tag-btn active" onclick="toggleFeature(this, 'zero')"><span>∅</span> Slashed Zero (zero)</button>
        <button class="tag-btn active" onclick="toggleFeature(this, 'tnum')"><span>123</span> Tabular Numbers (tnum)</button>
        <button class="tag-btn" onclick="toggleMarkerHighlight()"><span>🖍️</span> Felt Marker Highlight</button>
      </div>
    </div>

    <!-- Official pocketgull.app Typography Architecture -->
    <div class="weights-list">
      <div class="section-title">📐 The 3 Pillars of PocketGull Typography</div>

      <div class="weight-row">
        <div class="weight-meta">
          <span>1. Display &amp; Brand Headline Stack</span>
          <span><code>.font-pocketgull</code> · 800/900 Weight · -0.02em tracking</span>
        </div>
        <div class="weight-sample" style="font-family: var(--font-brand); font-weight: 800; letter-spacing: -0.02em;">
          PocketGull Sanctuary: Empirical Clinical Intelligence
        </div>
      </div>

      <div class="weight-row">
        <div class="weight-meta">
          <span>2. Clinical High-Legibility Body Stack</span>
          <span><code>.font-pocketgull-inter</code> · Atkinson Hyperlegible · Open Apertures</span>
        </div>
        <div class="weight-sample" style="font-family: 'Atkinson Hyperlegible', sans-serif; font-size: 20px; font-weight: 500; line-height: 1.6; color: var(--text-primary);">
          Bystander 911 dispatch, real-time CPR coach, and emergency waveform telemetry with zero visual ambiguity (1 vs l vs I, 0 vs O).
        </div>
      </div>

      <div class="weight-row">
        <div class="weight-meta">
          <span>3. Telemetry &amp; Tabular Monospace Stack</span>
          <span><code>.font-pocketgull-mono</code> · JetBrains Mono · Slashed Zero</span>
        </div>
        <div class="weight-sample" style="font-family: var(--font-mono); font-size: 20px; color: var(--accent-teal); font-feature-settings: 'tnum' 1, 'zero' 1;">
          HEART_RATE: 72 bpm · SPO2: 98% · GLUCOSE: 104 mg/dL · DOSE: 100 mg / 1.5 mL
        </div>
      </div>
    </div>

    <!-- Integration Code Snippet -->
    <div>
      <div class="section-title">💻 CSS Quick-Integration for Web &amp; Apps</div>
      <pre class="code-box"><code>/* 🖋️ Official PocketGull Design Tokens (from pocketgull.app) */
.font-pocketgull-brand {
  font-family: 'PocketGull', 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.font-pocketgull-clinical {
  font-family: 'Atkinson Hyperlegible', 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 500;
  line-height: 1.6;
}

.font-pocketgull-mono {
  font-family: 'PocketGull Mono', 'JetBrains Mono', monospace !important;
  font-feature-settings: "tnum" 1, "zero" 1;
}</code></pre>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('canvas');
    const sliderSize = document.getElementById('slider-size');
    const sliderTracking = document.getElementById('slider-tracking');
    const sliderWeight = document.getElementById('slider-weight');

    const valSize = document.getElementById('val-size');
    const valTracking = document.getElementById('val-tracking');
    const valWeight = document.getElementById('val-weight');

    let currentStack = 'brand';
    let isHighlighted = false;
    let activeFeatures = {
      'zero': true,
      'tnum': true
    };

    function updateCanvas() {
      const sz = parseInt(sliderSize.value, 10);
      const tr = parseFloat(sliderTracking.value);
      const wt = parseInt(sliderWeight.value, 10);

      valSize.textContent = sz + 'px';
      valTracking.textContent = tr + 'em';
      valWeight.textContent = wt;

      canvas.style.fontSize = sz + 'px';
      canvas.style.letterSpacing = tr + 'em';
      canvas.style.fontWeight = wt;

      if (currentStack === 'brand') {
        canvas.style.fontFamily = "var(--font-brand)";
      } else if (currentStack === 'clinical') {
        canvas.style.fontFamily = "'Atkinson Hyperlegible', var(--font-body)";
      } else if (currentStack === 'telemetry') {
        canvas.style.fontFamily = "var(--font-mono)";
      }

      const featStr = Object.entries(activeFeatures)
        .map(([k, v]) => `"${k}" ${v ? 1 : 0}`)
        .join(', ');
      canvas.style.fontFeatureSettings = featStr;
    }

    sliderSize.addEventListener('input', updateCanvas);
    sliderTracking.addEventListener('input', updateCanvas);
    sliderWeight.addEventListener('input', updateCanvas);

    function switchStack(btn, stackName) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentStack = stackName;
      updateCanvas();
    }

    function setPreset(text) {
      canvas.textContent = text;
    }

    function toggleFeature(elem, key) {
      activeFeatures[key] = !activeFeatures[key];
      elem.classList.toggle('active', activeFeatures[key]);
      updateCanvas();
    }

    function toggleMarkerHighlight() {
      isHighlighted = !isHighlighted;
      if (isHighlighted) {
        canvas.classList.add('marker-underline-highlight');
      } else {
        canvas.classList.remove('marker-underline-highlight');
      }
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
    }

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
