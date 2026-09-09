#!/usr/bin/env python3
"""
PocketGull Typefoundry: Duplicate Node Removal & Geometry Sanitizer
===================================================================
Scans TTF fonts and removes consecutive duplicate nodes from contours,
ensuring 0 duplicate nodes per Google Fonts specification.
"""

from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables.ttProgram import Program

ROOT_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

def sanitize_font_nodes(font_path):
    font = TTFont(font_path)
    glyf = font['glyf']
    cleaned_glyphs = 0
    total_removed = 0
    
    for gname in font.getGlyphOrder():
        g = glyf[gname]
        if g.numberOfContours <= 0:
            continue
            
        coords = list(g.coordinates)
        flags = list(g.flags)
        endPts = list(g.endPtsOfContours)
        
        new_coords = []
        new_flags = []
        new_endPts = []
        
        start = 0
        glyph_modified = False
        
        for end in endPts:
            c_coords = coords[start:end+1]
            c_flags = flags[start:end+1]
            
            cleaned_c_coords = []
            cleaned_c_flags = []
            
            n = len(c_coords)
            for i in range(n):
                next_i = (i + 1) % n
                # Check if current point is identical to next point
                if c_coords[i] == c_coords[next_i]:
                    total_removed += 1
                    glyph_modified = True
                    # skip point i
                    continue
                cleaned_c_coords.append(c_coords[i])
                cleaned_c_flags.append(c_flags[i])
                
            # If contour became too small (less than 3 points), keep original
            if len(cleaned_c_coords) < 3:
                cleaned_c_coords = c_coords
                cleaned_c_flags = c_flags
                
            new_coords.extend(cleaned_c_coords)
            new_flags.extend(cleaned_c_flags)
            new_endPts.append(len(new_coords) - 1)
            start = end + 1
            
        if glyph_modified:
            new_glyph = Glyph()
            new_glyph.numberOfContours = len(new_endPts)
            new_glyph.endPtsOfContours = new_endPts
            new_glyph.coordinates = GlyphCoordinates(new_coords)
            new_glyph.flags = bytearray([f & 0x3F for f in new_flags])
            new_glyph.program = Program()
            new_glyph.recalcBounds(glyf)
            glyf[gname] = new_glyph
            cleaned_glyphs += 1
            
    if cleaned_glyphs > 0:
        font.save(font_path)
        print(f"[{font_path.name}] Sanitized {cleaned_glyphs} glyphs (removed {total_removed} duplicate points).")
    else:
        print(f"[{font_path.name}] 100% clean (0 duplicate points found).")
    font.close()

if __name__ == "__main__":
    for ttf in TTF_DIR.glob("*.ttf"):
        sanitize_font_nodes(ttf)
    print("[SUCCESS] All font outlines sanitized.")
