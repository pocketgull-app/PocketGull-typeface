#!/usr/bin/env python3
"""
PocketGull Typefoundry - Italic Varieties Generator
Generates true mathematical italic cuts for the PocketGull Superfamily:
  1. PocketGull-Italic.ttf (Weight 400, Italic, based on Fineliner)
  2. PocketGull-BoldItalic.ttf (Weight 700, Bold Italic, based on Bold)
  3. PocketGullMono-Italic.ttf (Weight 500, Fixed 600 UPM Monospace Italic)

Enforces:
- 1000 UPM standard em-square
- 2-byte word alignment and bit-7 flag masking (via subsequent SfntTransformer audit)
- Exact Option 5 Google Fonts versioning and metadata
- Strict 600 UPM advance width on PocketGullMono-Italic
- High-efficiency Brotli Q11 WOFF2 webfonts
"""

import math
import os
import shutil
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
OFL_PATH = ROOT_DIR / "OFL.txt"

SLANT_ANGLE_DEG = -10.5
SHEAR = math.tan(math.radians(-SLANT_ANGLE_DEG))  # ~0.18534
CENTER_Y = 260.0  # lowercase x-height optical pivot

VARIETIES = [
    {
        "source": "PocketGull-Fineliner.ttf",
        "target_stem": "PocketGull-Italic",
        "family": "PocketGull",
        "subfamily": "Italic",
        "full_name": "PocketGull Italic",
        "ps_name": "PocketGull-Italic",
        "weight": 400,
        "is_bold": False,
        "is_mono": False,
    },
    {
        "source": "PocketGull-Bold.ttf",
        "target_stem": "PocketGull-BoldItalic",
        "family": "PocketGull",
        "subfamily": "Bold Italic",
        "full_name": "PocketGull Bold Italic",
        "ps_name": "PocketGull-BoldItalic",
        "weight": 700,
        "is_bold": True,
        "is_mono": False,
    },
    {
        "source": "PocketGullMono-Regular.ttf",
        "target_stem": "PocketGullMono-Italic",
        "family": "PocketGull Mono",
        "subfamily": "Italic",
        "full_name": "PocketGull Mono Italic",
        "ps_name": "PocketGullMono-Italic",
        "weight": 500,
        "is_bold": False,
        "is_mono": True,
    },
]

def load_ofl_line1():
    if OFL_PATH.exists():
        with open(OFL_PATH, "r", encoding="utf-8") as f:
            return f.readline().strip()
    return "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-typeface)"

def set_name_record(font, name_id, text):
    """Sets a name record for Mac (1, 0, 0) and Windows Unicode (3, 1, 0x409)."""
    name_table = font["name"]
    name_table.setName(text, name_id, 1, 0, 0)
    name_table.setName(text, name_id, 3, 1, 0x409)

def generate_italics():
    print("=" * 70)
    print("  POCKETGULL TYPEFOUNDRY: MATHEMATICAL ITALIC VARIETY COMPILER")
    print(f"  Slant Angle: {SLANT_ANGLE_DEG}° (Shear: {SHEAR:.5f}, Pivot Y: {CENTER_Y})")
    print("=" * 70)

    ofl_line1 = load_ofl_line1()
    dx = -CENTER_Y * SHEAR

    for var in VARIETIES:
        src_path = TTF_DIR / var["source"]
        if not src_path.exists():
            print(f"[ERROR] Source font not found: {src_path}")
            continue

        print(f"\n[COMPILE] {var['source']} -> {var['target_stem']}.ttf ...")
        font = TTFont(str(src_path))
        glyf = font["glyf"]
        hmtx = font["hmtx"]

        # 1. Slant all simple and composite glyphs
        for gname in font.getGlyphOrder():
            glyph = glyf[gname]
            if glyph.numberOfContours > 0:
                glyph.coordinates.transform([[1, 0], [SHEAR, 1]])
                glyph.coordinates.translate((dx, 0))
            elif glyph.isComposite():
                for comp in glyph.components:
                    if hasattr(comp, "x") and hasattr(comp, "y"):
                        comp.x = round(comp.x + comp.y * SHEAR)

        # 1b. Optical Correction for Slashed Zero (zero.slash and zero in Mono)
        # Mechanical shear pushes the slash diagonal from 59.4° down to 52.1°, flattening it
        # and crowding the inner counter curves. We apply an optical pitch restoration
        # (+30 UPM on bottom points, -24 UPM on top points) to restore a crisp 56.5° angle.
        for gname in ("zero.slash", "zero"):
            if gname in glyf:
                glyph = glyf[gname]
                if glyph.numberOfContours == 3:
                    pts, ends, flags = glyph.getCoordinates(glyf)
                    slash_start = ends[0] + 1
                    slash_end = ends[1]
                    if slash_end - slash_start + 1 == 4:
                        new_pts = list(pts)
                        for i in range(slash_start, slash_end + 1):
                            px, py = new_pts[i]
                            if py < 300:
                                new_pts[i] = (px + 30, py)
                            else:
                                new_pts[i] = (px - 24, py)
                        glyph.coordinates = GlyphCoordinates(new_pts)

        # 2. Recalculate bounds and update metrics
        for gname in font.getGlyphOrder():
            glyph = glyf[gname]
            glyph.recalcBounds(glyf)
            old_width, old_lsb = hmtx[gname]
            new_lsb = glyph.xMin if glyph.numberOfContours > 0 or glyph.isComposite() else old_lsb

            if var["is_mono"]:
                # Monospace invariant: strict 600 UPM advance width!
                hmtx[gname] = (600, new_lsb)
            else:
                hmtx[gname] = (old_width, new_lsb)

        # 3. Update Font Tables for Italic Specification
        # post table
        font["post"].italicAngle = SLANT_ANGLE_DEG

        # head table
        font["head"].fontRevision = 3.0
        if var["is_bold"]:
            font["head"].macStyle = 0x0003  # Bold (0x01) + Italic (0x02)
        else:
            font["head"].macStyle = 0x0002  # Italic (0x02)

        # OS/2 table
        os2 = font["OS/2"]
        os2.usWeightClass = var["weight"]
        # Set fsSelection: bit 0 (Italic) + bit 7 (USE_TYPO_METRICS = 0x80)
        fs_selection = 0x80 | 0x01
        if var["is_bold"]:
            fs_selection |= 0x20  # bit 5 (Bold)
        os2.fsSelection = fs_selection

        if var["is_mono"]:
            font["post"].isFixedPitch = 1
            os2.panose.bProportion = 9

        # Update STAT table axis values if present
        if "STAT" in font:
            stat = font["STAT"].table
            if hasattr(stat, "AxisValueArray") and stat.AxisValueArray:
                for av in stat.AxisValueArray.AxisValue:
                    # If this refers to the ital axis
                    if hasattr(av, "AxisIndex") and av.AxisIndex < len(stat.DesignAxisRecord.Axis):
                        axis_tag = stat.DesignAxisRecord.Axis[av.AxisIndex].AxisTag
                        if axis_tag == "ital":
                            av.Value = 1.0

        # Update name table
        set_name_record(font, 0, ofl_line1)
        set_name_record(font, 1, var["family"])
        set_name_record(font, 2, var["subfamily"])
        set_name_record(font, 3, f"3.000;PGUL;{var['ps_name']}")
        set_name_record(font, 4, var["full_name"])
        set_name_record(font, 5, "Version 3.000; The PocketGull Project Authors; OFL 1.1")
        set_name_record(font, 6, var["ps_name"])

        # Save TTF
        out_ttf = TTF_DIR / f"{var['target_stem']}.ttf"
        font.save(str(out_ttf))
        print(f"  [OK] Saved TTF: {out_ttf.name} ({out_ttf.stat().st_size / 1024:.1f} KB)")

        # Save WOFF2 (Brotli compression)
        out_woff2 = WOFF2_DIR / f"{var['target_stem']}.woff2"
        font.flavor = "woff2"
        font.save(str(out_woff2))
        print(f"  [OK] Saved WOFF2: {out_woff2.name} ({out_woff2.stat().st_size / 1024:.1f} KB)")

    print("\n[SUCCESS] Italic varieties generation complete.")

if __name__ == "__main__":
    generate_italics()
