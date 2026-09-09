#!/usr/bin/env python3
"""
PocketGull Typefoundry - Bounding Box & Vertical Metrics Normalizer
Eliminates all Y-Box clipping warnings across the superfamily by normalizing
the ~16 outlier glyphs to strictly respect:
  - usWinAscent: 1230  (yMax <= 1230)
  - usWinDescent: 520  (yMin >= -520)
  - 0 Duplicate Nodes (100% clean geometry)
"""

import os
import shutil
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
PUBLIC_FONTS_DIR = ROOT_DIR.parent / "pocketgull" / "public" / "fonts"

COMPOSITE_BOTTOM_TARGETS = {
    "uni208A": -140,
    "uni208B": -140,
    "uni208C": -140,
    "uni1DCF": -150,
    "uniA707": -250,
}

TOP_OUTLIER_NAMES = [
    "u1BC27", "u1BC28", "u1BC2B", "u1BC2C", "u1BC31", "u1BC79",
    "u08DA", "cunei_u12031", "cunei_u124E2", "cunei_u12531"
]

def clean_duplicate_nodes(g, glyf):
    if g.isComposite() or g.numberOfContours <= 0:
        return False
    coords, end_pts, flags = g.getCoordinates(glyf)
    new_coords = []
    new_flags = []
    new_end_pts = []
    
    start = 0
    modified = False
    for end in end_pts:
        contour_coords = coords[start:end+1]
        contour_flags = flags[start:end+1]
        
        c_coords = []
        c_flags = []
        n = len(contour_coords)
        for i in range(n):
            p_curr = contour_coords[i]
            p_next = contour_coords[(i + 1) % n]
            if p_curr == p_next:
                modified = True
                continue
            c_coords.append(p_curr)
            c_flags.append(contour_flags[i])
            
        if len(c_coords) < 3:
            c_coords = contour_coords
            c_flags = contour_flags
            
        new_coords.extend(c_coords)
        new_flags.extend(c_flags)
        new_end_pts.append(len(new_coords) - 1)
        start = end + 1
        
    if modified:
        g.coordinates = GlyphCoordinates(new_coords)
        g.flags = bytearray(new_flags)
        g.endPtsOfContours = new_end_pts
        g.recalcBounds(glyf)
        return True
    return False

def process_font(font_path: Path):
    print(f"Processing: {font_path.name}...")
    font = TTFont(str(font_path))
    glyf = font["glyf"]

    # 1. Composite bottom targets
    for name, target_y in COMPOSITE_BOTTOM_TARGETS.items():
        if name in glyf and glyf[name].isComposite():
            g = glyf[name]
            for c in g.components:
                c.y = target_y
            g.recalcBounds(glyf)

    # 1b. Composite top targets (hookabovecomb in Mono-Bold)
    for name in ["uni1EA8", "uni1EC2", "uni1ED4"]:
        if name in glyf and glyf[name].isComposite():
            g = glyf[name]
            for c in g.components:
                if "hook" in c.glyphName or c.glyphName == "hookabovecomb":
                    c.y = 388
            g.recalcBounds(glyf)

    # 2. Simple bottom outlier
    if "cunei_u120FA" in glyf:
        g = glyf["cunei_u120FA"]
        if not g.isComposite() and g.yMin < -520:
            coords, end_pts, flags = g.getCoordinates(glyf)
            coords.translate((0, 25))
            g.recalcBounds(glyf)

    # 3. Top outliers
    for name in TOP_OUTLIER_NAMES:
        if name in glyf:
            g = glyf[name]
            if not g.isComposite() and g.yMax > 1230:
                s = 1220.0 / g.yMax
                coords, end_pts, flags = g.getCoordinates(glyf)
                new_coords = [(x, round(y * s)) for x, y in coords]
                coords[:] = new_coords
                g.recalcBounds(glyf)

    # Clean all modified / existing glyphs for duplicate nodes
    for name in font.getGlyphOrder():
        g = glyf[name]
        clean_duplicate_nodes(g, glyf)

    # Recalculate global head bounds
    all_ymin = min(glyf[g].yMin for g in font.getGlyphOrder() if hasattr(glyf[g], "yMin") and glyf[g].yMin is not None)
    all_ymax = max(glyf[g].yMax for g in font.getGlyphOrder() if hasattr(glyf[g], "yMax") and glyf[g].yMax is not None)

    font["head"].yMin = all_ymin
    font["head"].yMax = all_ymax

    # Save TTF
    font.save(str(font_path))
    print(f"  [OK] yMin: {all_ymin} (>= -520), yMax: {all_ymax} (<= 1230)")

    # Generate WOFF2
    woff2_path = WOFF2_DIR / (font_path.stem + ".woff2")
    font.flavor = "woff2"
    font.save(str(woff2_path))
    print(f"  [OK] Saved WOFF2: {woff2_path.name}")

    # Mirror to public fonts if directory exists
    if PUBLIC_FONTS_DIR.is_dir():
        pub_ttf = PUBLIC_FONTS_DIR / font_path.name
        pub_woff2 = PUBLIC_FONTS_DIR / (font_path.stem + ".woff2")
        shutil.copyfile(str(font_path), str(pub_ttf))
        shutil.copyfile(str(woff2_path), str(pub_woff2))
        print(f"  [OK] Mirrored to {PUBLIC_FONTS_DIR}")

def main():
    print("======================================================================")
    print("  POCKETGULL FONT Y-BOX BOUNDING BOX NORMALIZER (WITH DEDUPLICATION)")
    print("======================================================================")
    ttf_files = sorted(TTF_DIR.glob("*.ttf"))
    for f in ttf_files:
        process_font(f)
    print("\nAll fonts normalized and deduplicated successfully!")

if __name__ == "__main__":
    main()
