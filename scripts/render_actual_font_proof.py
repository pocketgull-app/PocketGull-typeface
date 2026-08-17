#!/usr/bin/env python3
"""
Inspect actual TTF font binaries and generate pure vector SVG glyph proofs
directly from the compiled font table.
"""

import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

def audit_actual_font():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    font_path = os.path.join(typeface_root, 'PocketGull-Bold.ttf')
    
    font = TTFont(font_path)
    glyf = font['glyf']
    hmtx = font['hmtx']
    glyph_set = font.getGlyphSet()
    
    print("=" * 60)
    print("ACTUAL COMPILED TTF FONT BINARY AUDIT")
    print("=" * 60)
    print(f"Font File: {font_path}")
    print(f"Total TrueType Glyphs in Binary: {len(glyf.keys())}")
    print(f"UPM: {font['head'].unitsPerEm}")
    print(f"Revision: {font['head'].fontRevision}\n")

    # Generate a pure SVG proof directly from the TTF font table
    svg_glyphs = []
    sample_chars = ['P', 'o', 'c', 'k', 'e', 't', 'G', 'u', 'l', 'A', 'B', '0', '1', '2']
    
    x_cursor = 40
    y_baseline = 750
    scale = 0.5
    
    svg_elements = []
    
    for char in sample_chars:
        if char in glyph_set:
            glyph = glyph_set[char]
            pen = SVGPathPen(glyph_set)
            glyph.draw(pen)
            path_d = pen.getCommands()
            aw, lsb = hmtx[char]
            
            # Add to audit output
            print(f"  Glyph '{char}': Contours={glyf[char].numberOfContours}, Points={len(glyf[char].coordinates)}, Advance={aw}")
            
            if path_d:
                # TrueType uses Y-up, SVG uses Y-down, flip Y
                svg_elements.append(
                    f'<g transform="translate({x_cursor * scale}, {y_baseline * scale}) scale({scale}, -{scale})">'
                    f'<path d="{path_d}" fill="#0F172A" />'
                    f'</g>'
                )
            x_cursor += aw + 20

    total_width = int(x_cursor * scale) + 60
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} 500" width="{total_width}" height="500">
  <rect width="100%" height="100%" fill="#FAF8F5" />
  <line x1="20" y1="{y_baseline * scale}" x2="{total_width - 20}" y2="{y_baseline * scale}" stroke="#EA580C" stroke-width="1.5" stroke-dasharray="4,4" />
  <text x="30" y="40" font-family="sans-serif" font-size="14" fill="#64748B" font-weight="bold">DIRECT RENDER FROM PocketGull-Bold.ttf BINARY (Zero Filter / True Vector Outlines)</text>
  {''.join(svg_elements)}
</svg>'''

    svg_out_path = os.path.join(typeface_root, 'actual_font_binary_proof.svg')
    with open(svg_out_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"\n✅ Generated 100% authentic vector SVG proof directly from TTF font tables: {svg_out_path}")

if __name__ == '__main__':
    audit_actual_font()
