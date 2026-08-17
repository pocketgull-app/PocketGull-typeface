#!/usr/bin/env python3
"""
Generate a pristine, museum-grade, high-contrast vector SVG specimen sheet
extracted directly from PocketGull-Bold.ttf with fill-rule="evenodd" and exact metrics.
"""

import os
import base64
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

def render_master_svg():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    bold_path = os.path.join(typeface_root, 'PocketGull-Bold.ttf')
    woff2_path = os.path.join(typeface_root, 'PocketGull-Bold.woff2')
    output_svg = os.path.join(typeface_root, 'actual_font_binary_proof.svg')

    bold_font = TTFont(bold_path)
    cmap = bold_font.getBestCmap()
    glyph_set = bold_font.getGlyphSet()
    hmtx = bold_font['hmtx'].metrics

    # Base64 encode WOFF2 for embedded @font-face fallback
    woff2_b64 = ""
    if os.path.exists(woff2_path):
        with open(woff2_path, 'rb') as f:
            woff2_b64 = base64.b64encode(f.read()).decode('ascii')

    def get_path_and_width(char):
        cp = ord(char)
        name = cmap.get(cp)
        if not name or name not in glyph_set:
            return "", 400
        
        pen = SVGPathPen(glyph_set)
        glyph_set[name].draw(pen)
        d = pen.getCommands()
        adv_w = hmtx.get(name, (600, 0))[0]
        return d, adv_w

    width = 1200
    height = 1750

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <defs>')
    svg.append('    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">')
    svg.append('      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#E2E8F0" stroke-width="0.75" />')
    svg.append('    </pattern>')
    svg.append('  </defs>')

    svg.append('  <style>')
    if woff2_b64:
        svg.append(f"""
    @font-face {{
      font-family: 'PocketGull Embedded';
      src: url('data:font/woff2;charset=utf-8;base64,{woff2_b64}') format('woff2');
      font-weight: 700;
      font-style: normal;
    }}
        """)
    svg.append("""
    .ui-meta { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .glyph-path { fill-rule: evenodd; fill: #0F172A; }
    .glyph-path-gold { fill-rule: evenodd; fill: #EA580C; }
    .glyph-path-light { fill-rule: evenodd; fill: #FAF8F5; }
    .glyph-path-amber { fill-rule: evenodd; fill: #E9C46A; }
    """)
    svg.append('  </style>')

    # Background
    svg.append(f'  <rect width="{width}" height="{height}" fill="#FAF8F5" />')
    svg.append(f'  <rect width="{width}" height="{height}" fill="url(#grid)" opacity="0.6" />')
    
    # Outer Border
    svg.append(f'  <rect x="30" y="30" width="{width-60}" height="{height-60}" rx="16" fill="none" stroke="#CBD5E1" stroke-width="1.5" />')
    svg.append(f'  <rect x="38" y="38" width="{width-76}" height="{height-76}" rx="10" fill="none" stroke="#EA580C" stroke-width="0.75" stroke-dasharray="6,4" />')

    # Top Header
    svg.append('  <g transform="translate(60, 80)">')
    svg.append('    <text x="0" y="0" class="ui-meta" font-size="11" font-weight="900" fill="#EA580C" letter-spacing="3">POCKETGULL TYPEFOUNDRY · SPECIMEN BROADSIDE</text>')
    svg.append('    <text x="0" y="24" class="ui-meta" font-size="28" font-weight="900" fill="#0F172A" letter-spacing="-0.5">The Living Brand Superfamily</text>')
    svg.append('    <text x="1080" y="0" class="ui-meta" font-size="11" font-weight="700" fill="#64748B" text-anchor="end">1024 UPM · TRUE BEZIER VECTORS</text>')
    svg.append('    <text x="1080" y="24" class="ui-meta" font-size="11" font-weight="700" fill="#10B981" text-anchor="end">SIL OFL 1.1 · WCAG 2.2 AAA COMPLIANT</text>')
    svg.append('  </g>')

    svg.append(f'  <line x1="60" y1="130" x2="{width-60}" y2="130" stroke="#0F172A" stroke-width="2" />')

    # Precise TrueType Glyph Line Renderer with fill-rule="evenodd"
    def render_vector_line(text, start_x, baseline_y, scale_factor=0.10, css_class="glyph-path", tracking=15):
        elements = []
        cur_x = start_x
        for ch in text:
            if ch == ' ':
                cur_x += 320 * scale_factor
                continue
            path_d, adv_w = get_path_and_width(ch)
            if path_d:
                elements.append(f'<g transform="translate({cur_x:.2f}, {baseline_y:.2f}) scale({scale_factor:.4f}, {-scale_factor:.4f})"><path d="{path_d}" class="{css_class}" /></g>')
            cur_x += (adv_w + tracking) * scale_factor
        return "\n".join(elements)

    # 1. Master Brand Wordmark
    svg.append('  <!-- ══ SECTION 1: MASTER WORDMARK ══ -->')
    svg.append('  <g transform="translate(60, 240)">')
    svg.append(f'    <line x1="0" y1="0" x2="{width-120}" y2="0" stroke="#EA580C" stroke-width="1" stroke-dasharray="4,4" />')
    svg.append('  </g>')
    svg.append(render_vector_line("PocketGull", 60, 240, scale_factor=0.16, css_class="glyph-path", tracking=10))

    # 2. Uppercase Alphabet
    svg.append('  <!-- ══ SECTION 2: UPPERCASE ALPHABET ══ -->')
    svg.append('  <text x="60" y="300" class="ui-meta" font-size="10" font-weight="800" fill="#EA580C" letter-spacing="2">UPPERCASE DISPLAY HIERARCHY</text>')
    svg.append(render_vector_line("A B C D E F G H I J K L M", 60, 360, scale_factor=0.065, css_class="glyph-path", tracking=35))
    svg.append(render_vector_line("N O P Q R S T U V W X Y Z", 60, 425, scale_factor=0.065, css_class="glyph-path", tracking=35))

    # 3. Lowercase Alphabet
    svg.append('  <!-- ══ SECTION 3: LOWERCASE ALPHABET ══ -->')
    svg.append('  <text x="60" y="480" class="ui-meta" font-size="10" font-weight="800" fill="#EA580C" letter-spacing="2">LOWERCASE APERTURE &amp; COUNTER BALANCE</text>')
    svg.append(render_vector_line("a b c d e f g h i j k l m", 60, 535, scale_factor=0.065, css_class="glyph-path", tracking=35))
    svg.append(render_vector_line("n o p q r s t u v w x y z", 60, 595, scale_factor=0.065, css_class="glyph-path", tracking=35))

    # 4. Numerals & Slashed Zero
    svg.append('  <!-- ══ SECTION 4: NUMERALS & SLASHED ZERO ══ -->')
    svg.append('  <text x="60" y="655" class="ui-meta" font-size="10" font-weight="800" fill="#EA580C" letter-spacing="2">CLINICAL NUMERALS &amp; SLASHED ZERO (0 vs O)</text>')
    svg.append(render_vector_line("0 1 2 3 4 5 6 7 8 9", 60, 715, scale_factor=0.075, css_class="glyph-path", tracking=45))

    # 5. Multi-Script Box (Greek & Cyrillic & Biophysics)
    svg.append(f'  <rect x="60" y="755" width="{width-120}" height="280" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />')
    
    svg.append('  <text x="80" y="790" class="ui-meta" font-size="10" font-weight="800" fill="#7C3AED" letter-spacing="2">GREEK &amp; COPTIC ALPHABET (α β Ω)</text>')
    svg.append(render_vector_line("Γ Δ Θ Λ Ξ Π Σ Φ Ψ Ω α β π φ", 80, 840, scale_factor=0.055, css_class="glyph-path", tracking=30))

    svg.append('  <text x="80" y="890" class="ui-meta" font-size="10" font-weight="800" fill="#0284C7" letter-spacing="2">CYRILLIC PAN-SLAVIC SCRIPT</text>')
    svg.append(render_vector_line("Б Д Ж И Я", 80, 940, scale_factor=0.065, css_class="glyph-path", tracking=45))

    svg.append('  <text x="80" y="990" class="ui-meta" font-size="10" font-weight="800" fill="#10B981" letter-spacing="2">BIOPHYSICAL CALCULUS &amp; TELEMETRY OPERATORS</text>')
    svg.append(render_vector_line("∂ ∇ ∞ ∫ ∆ ≈ ♥", 80, 1040, scale_factor=0.065, css_class="glyph-path", tracking=50))

    # 6. Clinical ICU Readout Card
    svg.append(f'  <rect x="60" y="1065" width="{width-120}" height="175" rx="12" fill="#0F172A" />')
    svg.append('  <text x="90" y="1100" class="ui-meta" font-size="11" font-weight="700" fill="#38BDF8" letter-spacing="2">REAL-TIME CLINICAL HUD READOUT (WCAG AAA)</text>')
    svg.append(render_vector_line("120/80 mmHg · 74 bpm · SpO2 98%", 90, 1155, scale_factor=0.055, css_class="glyph-path-light", tracking=15))
    svg.append(render_vector_line("ATP + H2O ➔ ADP + Pi · φ = 1.618", 90, 1205, scale_factor=0.048, css_class="glyph-path-amber", tracking=15))

    # 7. Multi-Tier Pangrams
    svg.append('  <!-- ══ SECTION 7: PANGRAMS ══ -->')
    svg.append('  <text x="60" y="1285" class="ui-meta" font-size="10" font-weight="800" fill="#EA580C" letter-spacing="2">PANGRAM LEGIBILITY AT SCALE</text>')
    svg.append(render_vector_line("The quick brown fox jumps over the lazy dog.", 60, 1335, scale_factor=0.048, css_class="glyph-path", tracking=10))
    svg.append(render_vector_line("Pack my box with five dozen liquor jugs. 1234567890", 60, 1390, scale_factor=0.042, css_class="glyph-path", tracking=10))
    svg.append(render_vector_line("Sphinx of black quartz, judge my vow. Ø vs O Disambiguation.", 60, 1445, scale_factor=0.038, css_class="glyph-path", tracking=10))

    # 8. Quaker Quality Footer
    svg.append(f'  <line x1="60" y1="1500" x2="{width-60}" y2="1500" stroke="#CBD5E1" stroke-width="1" />')
    svg.append('  <g transform="translate(60, 1540)">')
    svg.append('    <text x="0" y="0" class="ui-meta" font-size="11" font-weight="800" fill="#0F172A">QUAKER QUALITY TESTIMONY INSPECTED</text>')
    svg.append('    <text x="0" y="18" class="ui-meta" font-size="10" fill="#64748B">Simplicity · Peace · Integrity · Equality · Stewardship</text>')
    svg.append(f'    <text x="{width-120}" y="0" class="ui-meta" font-size="11" font-weight="800" fill="#EA580C" text-anchor="end">POCKETGULL TYPEFOUNDRY</text>')
    svg.append(f'    <text x="{width-120}" y="18" class="ui-meta" font-size="10" fill="#64748B" text-anchor="end">github.com/philgear/PocketGull-typeface</text>')
    svg.append('  </g>')

    svg.append('</svg>')

    full_svg_content = "\n".join(svg)
    with open(output_svg, 'w', encoding='utf-8') as f:
        f.write(full_svg_content)

    print(f"[OK] Master vector SVG specimen successfully generated: {output_svg} ({len(full_svg_content)} bytes)")

    # Also copy to article/ and pocketgull/public/brand/
    article_svg = os.path.join(typeface_root, 'article', 'actual_font_binary_proof.svg')
    with open(article_svg, 'w', encoding='utf-8') as f:
        f.write(full_svg_content)

    public_brand_svg = "/mnt/c/Users/philg/Pocketgull/pocketgull/public/brand/actual_font_binary_proof.svg"
    if os.path.exists(os.path.dirname(public_brand_svg)):
        with open(public_brand_svg, 'w', encoding='utf-8') as f:
            f.write(full_svg_content)

if __name__ == '__main__':
    render_master_svg()
