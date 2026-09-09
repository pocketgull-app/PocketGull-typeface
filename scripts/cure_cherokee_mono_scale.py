#!/usr/bin/env python3
"""
PocketGull Typefoundry: Cherokee Mono Optical Scale Curation
============================================================
Restores Cherokee Syllabary (U+13A0–U+13FF) in PocketGullMono
from cramped 342 UPM specks to authoritative 680 UPM cap-height
conforming to Invariant Pillar 8.
"""

from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables.ttProgram import Program

ROOT_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

def cure_cherokee_in_mono(mono_name, prop_name):
    mono_path = TTF_DIR / mono_name
    prop_path = TTF_DIR / prop_name
    
    mono_font = TTFont(mono_path)
    prop_font = TTFont(prop_path)
    
    mono_glyf = mono_font['glyf']
    mono_hmtx = mono_font['hmtx']
    mono_cmap = mono_font.getBestCmap()
    
    prop_glyf = prop_font['glyf']
    prop_cmap = prop_font.getBestCmap()
    
    cherokee_codepoints = [cp for cp in range(0x13A0, 0x1400) if cp in mono_cmap and cp in prop_cmap]
    print(f"[{mono_name}] Found {len(cherokee_codepoints)} Cherokee codepoints to cure...")
    
    cured = 0
    for cp in cherokee_codepoints:
        mono_gname = mono_cmap[cp]
        prop_gname = prop_cmap[cp]
        
        src_glyph = prop_glyf[prop_gname]
        if src_glyph.numberOfContours <= 0:
            continue
            
        # Clone coordinates from proportional master
        coords = GlyphCoordinates(src_glyph.coordinates)
        flags = bytearray(src_glyph.flags)
        endPts = list(src_glyph.endPtsOfContours)
        
        # Proportional bounds
        all_x = [pt[0] for pt in coords]
        all_y = [pt[1] for pt in coords]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        cur_w = max_x - min_x
        cur_h = max_y - min_y
        
        # Scale to 680 UPM height
        target_h = 680.0
        sy = target_h / cur_h if cur_h > 0 else 1.0
        
        # Width constraint: must fit in 600 UPM cell with min 40 UPM sidebearings (max_w = 520 UPM)
        scaled_w = cur_w * sy
        if scaled_w > 520.0:
            sx = 520.0 / cur_w
        else:
            sx = sy
            
        # Apply scale
        coords.transform(((sx, 0), (0, sy)))
        coords.toInt()
        
        # Recalculate bounds after scale
        all_x = [pt[0] for pt in coords]
        min_x, max_x = min(all_x), max(all_x)
        scaled_w = max_x - min_x
        
        # Center horizontally in fixed 600 UPM cell
        target_lsb = int((600 - scaled_w) / 2)
        dx = target_lsb - min_x
        coords.translate((dx, 0))
        coords.toInt()
        
        new_glyph = Glyph()
        new_glyph.numberOfContours = len(endPts)
        new_glyph.endPtsOfContours = endPts
        new_glyph.coordinates = coords
        new_glyph.flags = bytearray([f & 0x3F for f in flags])
        new_glyph.program = Program()
        new_glyph.recalcBounds(mono_glyf)
        mono_glyf[mono_gname] = new_glyph
        
        # Monospace pitch invariant: advance width MUST be exactly 600 UPM
        mono_hmtx[mono_gname] = (600, new_glyph.xMin)
        cured += 1
        
    print(f"[{mono_name}] Cured {cured} Cherokee glyphs to 680 UPM optical height.")
    
    # Save TTF
    mono_font.save(mono_path)
    mono_font.close()
    prop_font.close()

if __name__ == "__main__":
    cure_cherokee_in_mono("PocketGullMono-Regular.ttf", "PocketGull-Regular.ttf")
    cure_cherokee_in_mono("PocketGullMono-Bold.ttf", "PocketGull-Bold.ttf")
    cure_cherokee_in_mono("PocketGullMono-Italic.ttf", "PocketGull-Italic.ttf")
    print("[SUCCESS] All Cherokee Mono glyphs optically cured to 680 UPM!")
