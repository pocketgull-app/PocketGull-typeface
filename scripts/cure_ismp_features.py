#!/usr/bin/env python3
"""
PocketGull Typefoundry - ISMP & FDA OpenType Feature Curing Engine
==================================================================
Systematically cures the OpenType GSUB substitution tables across all
PocketGull superfamily TTF binaries:
  - cv05 (Curved lowercase l): maps 'l' -> 'l.curved' (eliminates l vs 1 vs I collision)
  - ss02 (Serifed uppercase I): maps 'I' -> 'I.serif' (eliminates I vs l collision)
  - cv08 / zero (Slashed zero): maps 'zero' -> 'zero.slash' (eliminates 0 vs O collision)

Corrects the 1-glyph offset bug where 'l' was incorrectly mapped to 'uni2800'
(a blank 0-contour Braille cell) and 'I' was mapped to 'l.curved'.
"""

import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from fontTools.ttLib import TTFont

ROOT_DIR = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    ROOT_DIR / "fonts" / "ttf",
    ROOT_DIR.parent / "pocketgull" / "public" / "fonts",
]

def cure_font_ismp(font_path: Path) -> bool:
    if not font_path.is_file() or not font_path.name.endswith(".ttf"):
        return False

    font = TTFont(str(font_path))
    if "GSUB" not in font or "glyf" not in font:
        return False

    glyf = font["glyf"]
    gsub = font["GSUB"].table
    modified = False

    has_l_curved = "l.curved" in glyf
    has_I_serif = "I.serif" in glyf
    has_zero_slash = "zero.slash" in glyf

    for fr in gsub.FeatureList.FeatureRecord:
        tag = fr.FeatureTag

        if tag == "cv05" and has_l_curved:
            for idx in fr.Feature.LookupListIndex:
                lk = gsub.LookupList.Lookup[idx]
                for st in lk.SubTable:
                    if hasattr(st, "mapping"):
                        old_val = st.mapping.get("l")
                        if old_val != "l.curved":
                            print(f"  [{font_path.name}] Curing cv05 Lookup {idx}: 'l' -> {old_val} => 'l.curved'")
                            st.mapping["l"] = "l.curved"
                            modified = True

        elif tag == "ss02" and has_I_serif:
            for idx in fr.Feature.LookupListIndex:
                lk = gsub.LookupList.Lookup[idx]
                for st in lk.SubTable:
                    if hasattr(st, "mapping"):
                        old_val = st.mapping.get("I")
                        if old_val != "I.serif":
                            print(f"  [{font_path.name}] Curing ss02 Lookup {idx}: 'I' -> {old_val} => 'I.serif'")
                            st.mapping["I"] = "I.serif"
                            modified = True

        elif tag in ("cv08", "zero") and has_zero_slash:
            for idx in fr.Feature.LookupListIndex:
                lk = gsub.LookupList.Lookup[idx]
                for st in lk.SubTable:
                    if hasattr(st, "mapping"):
                        old_val = st.mapping.get("zero")
                        if old_val != "zero.slash":
                            print(f"  [{font_path.name}] Curing {tag} Lookup {idx}: 'zero' -> {old_val} => 'zero.slash'")
                            st.mapping["zero"] = "zero.slash"
                            modified = True

    if modified:
        font.save(str(font_path))
        print(f"  ✓ Successfully saved cured font: {font_path}")
        return True
    return False

def main():
    print("======================================================================")
    print("  POCKETGULL TYPEFOUNDRY: ISMP OPENTYPE FEATURE CURING ENGINE")
    print("======================================================================\n")

    total_cured = 0
    for target_dir in TARGET_DIRS:
        if not target_dir.exists():
            print(f"Skipping non-existent directory: {target_dir}")
            continue

        print(f"Scanning: {target_dir}")
        for p in sorted(target_dir.glob("*.ttf")):
            if cure_font_ismp(p):
                total_cured += 1

    print(f"\n✨ Completed! Successfully cured {total_cured} font binaries.")

if __name__ == "__main__":
    main()
