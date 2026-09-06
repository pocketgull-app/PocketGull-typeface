#!/usr/bin/env python3
"""
PocketGull Typefoundry - Deduplication & Metadata Normalizer
1. Deduplicates consecutive identical nodes in glyph contours.
2. Removes redundant closing points (start == end).
3. Normalizes nameID 0, nameID 5, and head.fontRevision to SemVer 3.0.0.
"""

import os
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
OFL_DIR = ROOT_DIR / "ofl"
OFL_TXT = ROOT_DIR / "OFL.txt"

with open(OFL_TXT, "r", encoding="utf-8") as f:
    OFL_LINE_1 = f.readline().strip()

EXPECTED_VERSION = "Version 3.000; The PocketGull Project Authors; OFL 1.1"

def deduplicate_glyph(glyph):
    if glyph.numberOfContours <= 0:
        return 0
    coords = list(glyph.coordinates)
    flags = list(glyph.flags)
    end_pts = glyph.endPtsOfContours

    new_all_pts = []
    new_all_flags = []
    new_end_pts = []
    removed_count = 0

    start = 0
    for end in end_pts:
        contour_pts = coords[start : end + 1]
        contour_flags = flags[start : end + 1]
        start = end + 1

        if not contour_pts:
            continue

        c_pts = [contour_pts[0]]
        c_flags = [contour_flags[0]]
        for i in range(1, len(contour_pts)):
            if contour_pts[i] != c_pts[-1]:
                c_pts.append(contour_pts[i])
                c_flags.append(contour_flags[i])
            else:
                removed_count += 1

        # Check closing point (if last point explicitly matches first point)
        if len(c_pts) > 1 and c_pts[0] == c_pts[-1]:
            c_pts.pop()
            c_flags.pop()
            removed_count += 1

        if len(c_pts) < 3:
            # Degenerate contour (less than 3 points cannot define an area)
            continue

        new_all_pts.extend(c_pts)
        new_all_flags.extend(c_flags)
        new_end_pts.append(len(new_all_pts) - 1)

    if new_end_pts:
        glyph.coordinates = GlyphCoordinates(new_all_pts)
        glyph.flags = bytearray(new_all_flags)
        glyph.endPtsOfContours = new_end_pts
        glyph.numberOfContours = len(new_end_pts)
    else:
        glyph.numberOfContours = 0
        glyph.coordinates = GlyphCoordinates([])
        glyph.flags = bytearray([])
        glyph.endPtsOfContours = []

    return removed_count

def process_font(font_path: Path):
    print(f"Processing: {font_path.name} ...")
    font = TTFont(str(font_path))
    modified = False

    # 1. Deduplicate glyf contours
    if "glyf" in font:
        glyf = font["glyf"]
        total_dups_removed = 0
        for gname in font.getGlyphOrder():
            glyph = glyf[gname]
            total_dups_removed += deduplicate_glyph(glyph)
        if total_dups_removed > 0:
            print(f"  • Deduplicated {total_dups_removed} contour points")
            modified = True

    # 2. Normalize head.fontRevision
    rev = round(font["head"].fontRevision, 4)
    if rev != 3.0:
        font["head"].fontRevision = 3.0
        print(f"  • Fixed head.fontRevision: {rev} -> 3.0")
        modified = True

    # 3. Normalize name table (nameID 0 and nameID 5)
    name_table = font["name"]
    for record in name_table.names:
        if record.nameID == 0:
            val = record.toUnicode()
            if val != OFL_LINE_1:
                record.string = OFL_LINE_1.encode(record.getEncoding())
                print(f"  • Normalized nameID 0 to match OFL.txt line 1")
                modified = True
        elif record.nameID == 5:
            val = record.toUnicode()
            if val != EXPECTED_VERSION:
                record.string = EXPECTED_VERSION.encode(record.getEncoding())
                print(f"  • Normalized nameID 5 to Option 5 format")
                modified = True

    if modified:
        font.save(str(font_path))
        print(f"  [SAVED] {font_path.name}")
    else:
        print(f"  [CLEAN] No changes needed")

def main():
    # Remove test font if present
    test_font = TTF_DIR / "PocketGull-VF-test.ttf"
    if test_font.exists():
        test_font.unlink()
        print(f"Removed test artifact: {test_font.name}")
    test_woff2 = ROOT_DIR / "fonts" / "woff2" / "PocketGull-VF-test.woff2"
    if test_woff2.exists():
        test_woff2.unlink()
        print(f"Removed test artifact: {test_woff2.name}")

    # Process all TTFs in fonts/ttf
    for ttf in sorted(TTF_DIR.glob("*.ttf")):
        process_font(ttf)

    # Process all TTFs in ofl/
    for ttf in sorted(OFL_DIR.glob("**/*.ttf")):
        process_font(ttf)

if __name__ == "__main__":
    main()
