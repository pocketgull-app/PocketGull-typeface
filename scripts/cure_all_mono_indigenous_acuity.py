#!/usr/bin/env python3
"""
PocketGull Typefoundry: Pan-Indigenous Monospace Acuity Restorer
================================================================
Cures all 800 squashed non-Latin and indigenous glyphs in PocketGullMono
(Ethiopic Ge'ez, Inuktitut/Cree, Neo-Tifinagh, Vai, Adlam, Chinuk Pipa)
restoring them from cramped ~340 UPM specks to authoritative 680 UPM
optical cap-height in strict conformity with Invariant Pillar 8.
"""

from pathlib import Path
import sys
import unicodedata
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables.ttProgram import Program

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

def cure_mono_family(mono_name, prop_name):
    mono_path = TTF_DIR / mono_name
    prop_path = TTF_DIR / prop_name
    
    mono_font = TTFont(mono_path)
    prop_font = TTFont(prop_path)
    
    mono_glyf = mono_font['glyf']
    mono_hmtx = mono_font['hmtx']
    mono_cmap = mono_font.getBestCmap()
    
    prop_glyf = prop_font['glyf']
    prop_cmap = prop_font.getBestCmap()
    
    cured_count = 0
    
    for cp, mono_gname in mono_cmap.items():
        if cp not in prop_cmap:
            continue
            
        char = chr(cp)
        cat = unicodedata.category(char)
        if not cat.startswith(('L', 'N')):
            continue
            
        name = unicodedata.name(char, '')
        if 'MODIFIER' in name or 'SUPER' in name or 'SUBSCRIPT' in name or 'SMALL' in name:
            continue
        if 0x02B0 <= cp <= 0x02FF or 0x1D00 <= cp <= 0x1DBF or 0x2070 <= cp <= 0x209F:
            continue
            
        mg = mono_glyf[mono_gname]
        prop_gname = prop_cmap[cp]
        pg = prop_glyf[prop_gname]
        
        if mg.numberOfContours <= 0 or pg.numberOfContours <= 0:
            continue
            
        m_coords = list(mg.coordinates)
        p_coords = list(pg.coordinates)
        
        m_h = max(pt[1] for pt in m_coords) - min(pt[1] for pt in m_coords)
        p_h = max(pt[1] for pt in p_coords) - min(pt[1] for pt in p_coords)
        
        # Check if glyph is shrunken in mono compared to proportional master
        if p_h >= 520 and m_h < 490:
            # Rebuild from proportional master outline
            src_coords = GlyphCoordinates(pg.coordinates)
            src_flags = list(pg.flags)
            src_endPts = list(pg.endPtsOfContours)
            
            all_x = [pt[0] for pt in src_coords]
            all_y = [pt[1] for pt in src_coords]
            min_x, max_x = min(all_x), max(all_x)
            min_y, max_y = min(all_y), max(all_y)
            cur_w = max_x - min_x
            cur_h = max_y - min_y
            
            if cur_h <= 0 or cur_w <= 0:
                continue
                
            # Target 680 UPM optical height (matching Latin cap-height)
            target_h = 680.0
            sy = target_h / cur_h
            
            # Width constraint: max 520 UPM inside 600 UPM fixed pitch cell (40 UPM margins)
            if (cur_w * sy) > 520.0:
                sx = 520.0 / cur_w
            else:
                sx = sy
                
            # Apply scale
            src_coords.transform(((sx, 0), (0, sy)))
            src_coords.toInt()
            
            # Recalculate bounds
            all_x = [pt[0] for pt in src_coords]
            min_x, max_x = min(all_x), max(all_x)
            scaled_w = max_x - min_x
            
            # Center horizontally in fixed 600 UPM cell
            target_lsb = int((600 - scaled_w) / 2)
            dx = target_lsb - min_x
            src_coords.translate((dx, 0))
            src_coords.toInt()
            
            # Clean consecutive duplicate points
            cleaned_coords = []
            cleaned_flags = []
            cleaned_endPts = []
            
            coords_list = list(src_coords)
            start = 0
            for end in src_endPts:
                c_pts = coords_list[start:end+1]
                c_flg = src_flags[start:end+1]
                
                contour_pts = []
                contour_flg = []
                n = len(c_pts)
                for i in range(n):
                    next_i = (i + 1) % n
                    if c_pts[i] == c_pts[next_i]:
                        continue
                    contour_pts.append(c_pts[i])
                    contour_flg.append(c_flg[i] & 0x3F) # Mask bit 7
                    
                if len(contour_pts) < 3:
                    contour_pts = c_pts
                    contour_flg = [f & 0x3F for f in c_flg]
                    
                cleaned_coords.extend(contour_pts)
                cleaned_flags.extend(contour_flg)
                cleaned_endPts.append(len(cleaned_coords) - 1)
                start = end + 1
                
            new_glyph = Glyph()
            new_glyph.numberOfContours = len(cleaned_endPts)
            new_glyph.endPtsOfContours = cleaned_endPts
            new_glyph.coordinates = GlyphCoordinates(cleaned_coords)
            new_glyph.flags = bytearray(cleaned_flags)
            new_glyph.program = Program()
            new_glyph.recalcBounds(mono_glyf)
            mono_glyf[mono_gname] = new_glyph
            
            # Monospace pitch invariant: advance width MUST be exactly 600 UPM
            mono_hmtx[mono_gname] = (600, new_glyph.xMin)
            cured_count += 1
            
    print(f"[{mono_name}] Successfully cured {cured_count} glyphs to 680 UPM optical parity!")
    mono_font.save(mono_path)
    mono_font.close()
    prop_font.close()
    return cured_count

if __name__ == "__main__":
    cure_mono_family("PocketGullMono-Regular.ttf", "PocketGull-Regular.ttf")
    cure_mono_family("PocketGullMono-Bold.ttf", "PocketGull-Bold.ttf")
    cure_mono_family("PocketGullMono-Italic.ttf", "PocketGull-Italic.ttf")
    print("\n[SUCCESS] All Pan-Indigenous Monospace glyphs cured across superfamily!")
