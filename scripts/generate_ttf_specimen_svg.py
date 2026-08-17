#!/usr/bin/env python3
"""
Generate a complete, multi-style, high-resolution SVG specimen
directly from the compiled PocketGull TTF font binaries.
"""

import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

def render_line(glyph_set, hmtx, text, start_x, y, scale=0.35, color="#0F172A"):
    elements = []
    x = start_x
    for char in text:
        if char == ' ':
            x += 280 * scale
            continue
        if char in glyph_set:
            glyph = glyph_set[char]
            pen = SVGPathPen(glyph_set)
            glyph.draw(pen)
            path_d = pen.getCommands()
            aw, lsb = hmtx[char]
            if path_d:
                elements.append(
                    f'<g transform="translate({x}, {y}) scale({scale}, -{scale})">'
                    f'<path d="{path_d}" fill="{color}" />'
                    f'</g>'
                )
            x += aw * scale + 4
        else:
            x += 350 * scale
    return elements, x

def generate_full_specimen():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    bold_path = os.path.join(typeface_root, 'PocketGull-Bold.ttf')
    fineliner_path = os.path.join(typeface_root, 'PocketGull-Fineliner.ttf')
    
    font_bold = TTFont(bold_path)
    gs_bold = font_bold.getGlyphSet()
    hmtx_bold = font_bold['hmtx']

    font_fine = TTFont(fineliner_path)
    gs_fine = font_fine.getGlyphSet()
    hmtx_fine = font_fine['hmtx']

    W = 1200
    H = 1500
    
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="#FAF8F5" />',
        '<!-- Header -->',
        '<text x="60" y="70" font-family="sans-serif" font-size="14" font-weight="bold" fill="#EA580C" letter-spacing="3">ACTUAL TTF FONT FILE RENDER • ZERO IMAGE FILTERS</text>',
        '<text x="60" y="100" font-family="sans-serif" font-size="28" font-weight="900" fill="#0F172A">PocketGull TrueType Font Suite</text>',
        '<line x1="60" y1="120" x2="1140" y2="120" stroke="#E2E8F0" stroke-width="2" />',
    ]

    # 1. Master Wordmark (Large Bold)
    svg_parts.append('<text x="60" y="170" font-family="sans-serif" font-size="12" font-weight="bold" fill="#64748B">1. POCKETGULL MASTER DISPLAY (700 BOLD)</text>')
    el, _ = render_line(gs_bold, hmtx_bold, "PocketGull", 60, 270, scale=0.14, color="#0F172A")
    svg_parts.extend(el)

    # 2. Uppercase Alphabet A-Z
    svg_parts.append('<text x="60" y="340" font-family="sans-serif" font-size="12" font-weight="bold" fill="#64748B">2. UPPERCASE ALPHABET (A - Z)</text>')
    el, _ = render_line(gs_bold, hmtx_bold, "ABCDEFGHIJKLM", 60, 410, scale=0.065, color="#0F172A")
    svg_parts.extend(el)
    el, _ = render_line(gs_bold, hmtx_bold, "NOPQRSTUVWXYZ", 60, 480, scale=0.065, color="#0F172A")
    svg_parts.extend(el)

    # 3. Lowercase Alphabet a-z
    svg_parts.append('<text x="60" y="550" font-family="sans-serif" font-size="12" font-weight="bold" fill="#64748B">3. LOWERCASE ALPHABET (a - z)</text>')
    el, _ = render_line(gs_bold, hmtx_bold, "abcdefghijklm", 60, 610, scale=0.065, color="#0F172A")
    svg_parts.extend(el)
    el, _ = render_line(gs_bold, hmtx_bold, "nopqrstuvwxyz", 60, 670, scale=0.065, color="#0F172A")
    svg_parts.extend(el)

    # 4. Numerals & Disambiguation (0-9)
    svg_parts.append('<text x="60" y="740" font-family="sans-serif" font-size="12" font-weight="bold" fill="#64748B">4. NUMERALS & DISAMBIGUATED SLASHED ZERO (0 - 9)</text>')
    el, _ = render_line(gs_bold, hmtx_bold, "0 1 2 3 4 5 6 7 8 9", 60, 810, scale=0.075, color="#EA580C")
    svg_parts.extend(el)

    # 5. Fineliner Weight Comparison (400 Regular)
    svg_parts.append('<text x="60" y="880" font-family="sans-serif" font-size="12" font-weight="bold" fill="#64748B">5. FINELINER WEIGHT (PocketGull-Fineliner.ttf)</text>')
    el, _ = render_line(gs_fine, hmtx_fine, "Pack my box with five dozen liquor jugs.", 60, 930, scale=0.045, color="#334155")
    svg_parts.extend(el)
    el, _ = render_line(gs_fine, hmtx_fine, "Sphinx of black quartz, judge my vow.", 60, 980, scale=0.045, color="#334155")
    svg_parts.extend(el)

    # 6. Bold Weight Running Text (700 Bold)
    svg_parts.append('<text x="60" y="1050" font-family="sans-serif" font-size="12" font-weight="bold" fill="#64748B">6. BOLD DISPLAY WEIGHT (PocketGull-Bold.ttf)</text>')
    el, _ = render_line(gs_bold, hmtx_bold, "The quick brown fox jumps over the lazy dog.", 60, 1110, scale=0.048, color="#0F172A")
    svg_parts.extend(el)
    el, _ = render_line(gs_bold, hmtx_bold, "CLINICAL TELEMETRY: 98.6 BPM - 120/80 MMHG", 60, 1170, scale=0.048, color="#0F172A")
    svg_parts.extend(el)

    # Footer
    svg_parts.append('<line x1="60" y1="1240" x2="1140" y2="1240" stroke="#E2E8F0" stroke-width="2" />')
    svg_parts.append('<text x="60" y="1280" font-family="sans-serif" font-size="13" font-weight="bold" fill="#0F172A">PocketGull Open Source Typography • SIL Open Font License 1.1</text>')
    svg_parts.append('<text x="60" y="1305" font-family="sans-serif" font-size="11" fill="#64748B">Rendered directly from /public/brand/fonts/PocketGull-Bold.ttf and PocketGull-Fineliner.ttf</text>')
    svg_parts.append('</svg>')

    out_svg = os.path.join(typeface_root, 'live_rendered_font_proof.svg')
    with open(out_svg, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_parts))
    
    brand_svg = os.path.abspath(os.path.join(typeface_root, '..', 'pocketgull', 'public', 'brand', 'live_rendered_font_proof.svg'))
    with open(brand_svg, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_parts))

    print(f"✅ Generated Full Vector Specimen direct from TTF binaries: {brand_svg}")

if __name__ == '__main__':
    generate_full_specimen()
