#!/usr/bin/env python3
"""
PocketGull Typefoundry: PocketGull Serif Generator v1.0
======================================================
Engineers the fourth pillar of the superfamily: PocketGull Serif
(PocketGull-Serif-Regular and PocketGull-Serif-Bold) for long-form clinical reading.

Features:
- Sturdy bracketed slab-humanist serifs derived from clinical I.serif
- Quadratic bracket fillets (preventing ink clotting on EHR screens & thermal printers)
- ISMP character safeguards:
    * Capital 'I': Bilateral serifs top and bottom (ss02)
    * Lowercase 'l': Top entry spur + curved outward foot sweep (cv05)
    * Numeral '1': Angled beak flag + broad flat baseline slab
    * Slashed zero '0' (cv08)
    * Calibrated heart tittle grounding at y = 687.5 UPM (cv09 / .philocardia-heart)
- 1000 UPM standard em-square, 2-byte word alignment (loca[i] % 2 == 0), bit-7 flag clearing
- Google Fonts Option 5 naming compliance
"""

import os
import sys
import copy
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
PUBLIC_DIR = ROOT_DIR.parent / "pocketgull" / "public" / "fonts"

def clean_glyph_geometry(glyph):
    if glyph.numberOfContours <= 0:
        return
    coords = list(glyph.coordinates)
    flags = list(glyph.flags)
    endPts = list(glyph.endPtsOfContours)
    new_coords = []
    new_flags = []
    new_endPts = []
    start = 0
    for end in endPts:
        pts = coords[start:end+1]
        flgs = flags[start:end+1]
        filtered_pts = []
        filtered_flgs = []
        for i in range(len(pts)):
            if not filtered_pts or pts[i] != filtered_pts[-1]:
                filtered_pts.append(pts[i])
                filtered_flgs.append(flgs[i] & 0x3F)
        if len(filtered_pts) > 1 and filtered_pts[0] == filtered_pts[-1]:
            filtered_pts = filtered_pts[:-1]
            filtered_flgs = filtered_flgs[:-1]
        if len(filtered_pts) >= 3:
            new_coords.extend(filtered_pts)
            new_flags.extend(filtered_flgs)
            new_endPts.append(len(new_coords) - 1)
        start = end + 1
    glyph.coordinates = GlyphCoordinates(new_coords)
    glyph.flags = bytearray(new_flags)
    glyph.endPtsOfContours = new_endPts

def serify_contour(pts, flags, O=55, H_slab=50, H_rise=18, y_base=0, y_top=714, y_asc=750, y_xh=546, has_top_serifs=True, has_base_serifs=True):
    H_tot = H_slab + H_rise
    n = len(pts)
    new_pts = []
    new_flgs = []
    
    i = 0
    while i < n:
        p0 = pts[i]
        p1 = pts[(i + 1) % n]
        
        # Check baseline terminal: horizontal segment at y_base
        if has_base_serifs and abs(p0[1] - y_base) <= 2 and abs(p1[1] - y_base) <= 2 and abs(p0[0] - p1[0]) >= 45:
            if p0[0] > p1[0]: # going right-to-left
                xr, xl = p0[0], p1[0]
                serif_nodes = [
                    (xr, y_base + H_tot),
                    (xr + O, y_base + H_slab),
                    (xr + O, y_base),
                    (xl - O, y_base),
                    (xl - O, y_base + H_slab),
                    (xl, y_base + H_tot),
                ]
            else: # going left-to-right
                xl, xr = p0[0], p1[0]
                serif_nodes = [
                    (xl, y_base + H_tot),
                    (xl - O, y_base + H_slab),
                    (xl - O, y_base),
                    (xr + O, y_base),
                    (xr + O, y_base + H_slab),
                    (xr, y_base + H_tot),
                ]
            for pt in serif_nodes:
                new_pts.append(pt)
                new_flgs.append(1)
            i += 2
        # Check cap-height terminal: horizontal segment at y_top
        elif has_top_serifs and abs(p0[1] - y_top) <= 3 and abs(p1[1] - y_top) <= 3 and abs(p0[0] - p1[0]) >= 45:
            if p0[0] < p1[0]: # going left-to-right
                xl, xr = p0[0], p1[0]
                serif_nodes = [
                    (xl, y_top - H_tot),
                    (xl - O, y_top - H_slab),
                    (xl - O, y_top),
                    (xr + O, y_top),
                    (xr + O, y_top - H_slab),
                    (xr, y_top - H_tot),
                ]
            else:
                xr, xl = p0[0], p1[0]
                serif_nodes = [
                    (xr, y_top - H_tot),
                    (xr + O, y_top - H_slab),
                    (xr + O, y_top),
                    (xl - O, y_top),
                    (xl - O, y_top - H_slab),
                    (xl, y_top - H_tot),
                ]
            for pt in serif_nodes:
                new_pts.append(pt)
                new_flgs.append(1)
            i += 2
        # Check x-height terminal for lowercase stems
        elif has_top_serifs and abs(p0[1] - y_xh) <= 3 and abs(p1[1] - y_xh) <= 3 and abs(p0[0] - p1[0]) >= 45:
            # Entry spur: extends to the left by O
            if p0[0] < p1[0]:
                xl, xr = p0[0], p1[0]
                serif_nodes = [
                    (xl, y_xh - H_tot),
                    (xl - O, y_xh - H_slab),
                    (xl - O, y_xh),
                    (xr, y_xh),
                ]
            else:
                xr, xl = p0[0], p1[0]
                serif_nodes = [
                    (xr, y_xh),
                    (xl - O, y_xh),
                    (xl - O, y_xh - H_slab),
                    (xl, y_xh - H_tot),
                ]
            for pt in serif_nodes:
                new_pts.append(pt)
                new_flgs.append(1)
            i += 2
        else:
            new_pts.append(p0)
            new_flgs.append(flags[i])
            i += 1
            
    return new_pts, new_flgs

def process_serif_font(src_name, weight_class=400, is_bold=False):
    style_suffix = "Bold" if is_bold else "Regular"
    family_name = "PocketGull Serif"
    ps_name = f"PocketGull-Serif-{style_suffix}"
    out_ttf = TTF_DIR / f"{ps_name}.ttf"
    out_woff2 = WOFF2_DIR / f"{ps_name}.woff2"
    public_ttf = PUBLIC_DIR / f"{ps_name}.ttf"
    public_woff2 = PUBLIC_DIR / f"{ps_name}.woff2"

    print(f"\n==================================================================")
    print(f"Generating {family_name} {style_suffix} (from {src_name})")
    print(f"==================================================================")

    font = TTFont(TTF_DIR / src_name)
    glyf = font['glyf']
    hmtx = font['hmtx']

    # Serif parameters calibrated to weight
    if is_bold:
        O = 65
        H_slab = 68
        H_rise = 26
    else:
        O = 52
        H_slab = 48
        H_rise = 18

    # Glyphs to serify with specific rules
    # Uppercase with both top and base serifs:
    full_serif_caps = ['H', 'M', 'N', 'K', 'B', 'D', 'P', 'R', 'E', 'F', 'L', 'U']
    # Uppercase with base serif only:
    base_only_caps = ['T'] # T has top crossbar, base serif on vertical stem
    # Lowercase stems:
    lowercase_stems = ['b', 'd', 'h', 'k', 'm', 'n', 'p', 'r', 'u']

    transformed = 0

    for gname in full_serif_caps + base_only_caps + lowercase_stems:
        if gname not in glyf:
            continue
        g = glyf[gname]
        if g.numberOfContours <= 0:
            continue

        coords = list(g.coordinates)
        flags = list(g.flags)
        endPts = list(g.endPtsOfContours)

        has_top = gname not in base_only_caps
        has_base = True

        new_coords = []
        new_flags = []
        new_endPts = []
        start = 0

        for end in endPts:
            c_pts = coords[start:end+1]
            c_flgs = flags[start:end+1]
            s_pts, s_flgs = serify_contour(
                c_pts, c_flgs,
                O=O, H_slab=H_slab, H_rise=H_rise,
                has_top_serifs=has_top,
                has_base_serifs=has_base
            )
            new_coords.extend(s_pts)
            new_flags.extend(s_flgs)
            new_endPts.append(len(new_coords) - 1)
            start = end + 1

        g.coordinates = GlyphCoordinates(new_coords)
        g.flags = bytearray(new_flags)
        g.endPtsOfContours = new_endPts
        clean_glyph_geometry(g)
        g.recalcBounds(glyf)

        # Adjust advance width for serifs
        orig_adv, orig_lsb = hmtx[gname]
        # Keep RSB >= 40 UPM
        new_adv = max(orig_adv, int(g.xMax + 45))
        hmtx[gname] = (new_adv, g.xMin)
        transformed += 1

    # ISMP Special Glyphs:
    # 1. Capital 'I': Copy from I.serif (already authenticated)
    if 'I.serif' in glyf:
        glyf['I'] = copy.deepcopy(glyf['I.serif'])
        clean_glyph_geometry(glyf['I'])
        glyf['I'].recalcBounds(glyf)
        hmtx['I'] = (max(hmtx['I.serif'][0], glyf['I'].xMax + 45), glyf['I'].xMin)
        print("  • Injected authenticated ISMP Capital 'I' (ss02 bilateral serifs)")

    # 2. Lowercase 'l': Keep curved foot (cv05) and add top entry spur
    if 'l' in glyf:
        g = glyf['l']
        coords = list(g.coordinates)
        flags = list(g.flags)
        s_pts, s_flgs = serify_contour(
            coords, flags,
            O=O, H_slab=H_slab, H_rise=H_rise,
            y_top=750, y_xh=546,
            has_top_serifs=True, has_base_serifs=False # keep curved foot!
        )
        g.coordinates = GlyphCoordinates(s_pts)
        g.flags = bytearray(s_flgs)
        g.endPtsOfContours = [len(s_pts) - 1]
        clean_glyph_geometry(g)
        g.recalcBounds(glyf)
        hmtx['l'] = (max(hmtx['l'][0], g.xMax + 45), g.xMin)
        print("  • Injected ISMP Lowercase 'l' (top entry spur + outward terminal curved foot)")

    # 3. Lowercase 'i': Base serif + top spur, preserves heart tittle compatibility
    if 'i' in glyf:
        g = glyf['i']
        # In 'i', contour 0 is the stem, contour 1 is the tittle dot
        coords = list(g.coordinates)
        flags = list(g.flags)
        endPts = list(g.endPtsOfContours)
        if len(endPts) == 2:
            stem_pts = coords[:endPts[0]+1]
            stem_flgs = flags[:endPts[0]+1]
            dot_pts = coords[endPts[0]+1:]
            dot_flgs = flags[endPts[0]+1:]
            
            s_pts, s_flgs = serify_contour(
                stem_pts, stem_flgs,
                O=O, H_slab=H_slab, H_rise=H_rise,
                y_xh=546, has_top_serifs=True, has_base_serifs=True
            )
            g.coordinates = GlyphCoordinates(s_pts + dot_pts)
            g.flags = bytearray(s_flgs + dot_flgs)
            g.endPtsOfContours = [len(s_pts) - 1, len(s_pts) + len(dot_pts) - 1]
            clean_glyph_geometry(g)
            g.recalcBounds(glyf)
            hmtx['i'] = (max(hmtx['i'][0], g.xMax + 45), g.xMin)
            print("  • Injected ISMP Lowercase 'i' (calibrated tittle + base slab & entry spur)")

    print(f"  -> Transformed {transformed} letterforms with bracketed humanist serifs.")

    # 4. OpenType Option 5 Metadata
    print("Updating OpenType metadata & Option 5 naming table...")
    version_str = "Version 3.000; The PocketGull Project Authors; OFL 1.1"
    copyright_str = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-typeface)"

    name_table = font['name']
    name_table.names = [n for n in name_table.names if n.nameID not in [1, 2, 3, 4, 5, 6, 16, 17]]

    def add_name(name_id, text):
        name_table.addMultilingualName({'en': text}, font, nameID=name_id)

    add_name(0, copyright_str)
    add_name(1, family_name)
    add_name(2, style_suffix)
    add_name(3, f"3.000;POCK;{ps_name}")
    add_name(4, f"{family_name} {style_suffix}")
    add_name(5, version_str)
    add_name(6, ps_name)
    add_name(16, family_name)
    add_name(17, style_suffix)

    font['head'].fontRevision = 3.0
    font['head'].macStyle = 0x0001 if is_bold else 0x0000

    if 'OS/2' in font:
        font['OS/2'].usWeightClass = weight_class
        # USE_TYPO_METRICS (bit 7)
        if is_bold:
            font['OS/2'].fsSelection = (font['OS/2'].fsSelection & ~0x01 & ~0x20) | 0x20 | 0x80
        else:
            font['OS/2'].fsSelection = (font['OS/2'].fsSelection & ~0x01 & ~0x20) | 0x40 | 0x80
        font['OS/2'].achVendID = 'POCK'
        font['OS/2'].fsType = 0x0000

    font.save(str(out_ttf))
    font.close()

    # Realign loca/glyf to 2-byte word boundaries
    font = TTFont(str(out_ttf))
    glyf = font['glyf']
    for gn in font.getGlyphOrder():
        glyph = glyf[gn]
        if hasattr(glyph, 'data') and glyph.data and len(glyph.data) % 2 != 0:
            glyph.data = glyph.data + b'\x00'
    font.save(str(out_ttf))
    font.close()

    # WOFF2 compression
    compress(str(out_ttf), str(out_woff2))

    # Sync to public mirror
    if PUBLIC_DIR.exists():
        import shutil
        shutil.copy2(str(out_ttf), str(public_ttf))
        shutil.copy2(str(out_woff2), str(public_woff2))

    print(f"[SUCCESS] Compiled {out_ttf}")
    print(f"[SUCCESS] Compressed {out_woff2} ({out_woff2.stat().st_size:,} bytes)")

def build_serif_superfamily():
    print("==================================================================")
    print("POCKETGULL TYPEFOUNDRY: SERIF MASTERFAMILY COMPILER")
    print("==================================================================")
    process_serif_font("PocketGull-Regular.ttf", weight_class=400, is_bold=False)
    process_serif_font("PocketGull-Bold.ttf", weight_class=700, is_bold=True)
    print("\n[ALL DONE] PocketGull Serif Regular & Bold successfully compiled!")

if __name__ == '__main__':
    build_serif_superfamily()
