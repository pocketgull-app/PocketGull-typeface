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

from fontTools.ttLib.tables import otTables as ot

def ensure_feature_record(gsub, tag, lookup_index):
    """Ensures a FeatureRecord with tag and lookup_index exists in GSUB and is registered in all scripts."""
    if gsub.FeatureList is None:
        gsub.FeatureList = ot.FeatureList()
        gsub.FeatureList.FeatureRecord = []
        gsub.FeatureList.FeatureCount = 0

    feature_idx = None
    for i, fr in enumerate(gsub.FeatureList.FeatureRecord):
        if fr.FeatureTag == tag:
            feature_idx = i
            if lookup_index not in fr.Feature.LookupListIndex:
                fr.Feature.LookupListIndex.append(lookup_index)
                fr.Feature.LookupCount = len(fr.Feature.LookupListIndex)
            break

    if feature_idx is None:
        fr = ot.FeatureRecord()
        fr.FeatureTag = tag
        fr.Feature = ot.Feature()
        fr.Feature.LookupListIndex = [lookup_index]
        fr.Feature.LookupCount = 1
        fr.Feature.FeatureParams = None
        feature_idx = len(gsub.FeatureList.FeatureRecord)
        gsub.FeatureList.FeatureRecord.append(fr)
        gsub.FeatureList.FeatureCount = len(gsub.FeatureList.FeatureRecord)

    # Register in all Script records
    if gsub.ScriptList is not None:
        for s in gsub.ScriptList.ScriptRecord:
            if s.Script.DefaultLangSys is None:
                s.Script.DefaultLangSys = ot.DefaultLangSys()
                s.Script.DefaultLangSys.FeatureIndex = []
                s.Script.DefaultLangSys.LookupOrder = None
                s.Script.DefaultLangSys.ReqFeatureIndex = 0xFFFF
            if feature_idx not in s.Script.DefaultLangSys.FeatureIndex:
                s.Script.DefaultLangSys.FeatureIndex.append(feature_idx)
                s.Script.DefaultLangSys.FeatureCount = len(s.Script.DefaultLangSys.FeatureIndex)
            if hasattr(s.Script, 'LangSysRecord') and s.Script.LangSysRecord:
                for ls in s.Script.LangSysRecord:
                    if feature_idx not in ls.LangSys.FeatureIndex:
                        ls.LangSys.FeatureIndex.append(feature_idx)
                        ls.LangSys.FeatureCount = len(ls.LangSys.FeatureIndex)

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

    if gsub.LookupList is None:
        gsub.LookupList = ot.LookupList()
        gsub.LookupList.Lookup = []
        gsub.LookupList.LookupCount = 0

    # 1. Check or create single-substitution lookups for ISMP disambiguation
    # zero -> zero.slash
    if has_zero_slash:
        zero_lookup_idx = None
        for i, lk in enumerate(gsub.LookupList.Lookup):
            if lk.LookupType == 1:
                for st in lk.SubTable:
                    if hasattr(st, "mapping") and st.mapping.get("zero") == "zero.slash":
                        zero_lookup_idx = i
                        break
            if zero_lookup_idx is not None:
                break

        if zero_lookup_idx is None:
            st = ot.SingleSubst()
            st.Format = 1
            st.mapping = {"zero": "zero.slash"}
            lk = ot.Lookup()
            lk.LookupType = 1
            lk.LookupFlag = 0
            lk.SubTable = [st]
            lk.SubTableCount = 1
            zero_lookup_idx = len(gsub.LookupList.Lookup)
            gsub.LookupList.Lookup.append(lk)
            gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
            print(f"  [{font_path.name}] Created SingleSubst Lookup {zero_lookup_idx}: 'zero' -> 'zero.slash'")
            modified = True

        for tag in ("zero", "cv08"):
            ensure_feature_record(gsub, tag, zero_lookup_idx)
            modified = True

    # l -> l.curved
    if has_l_curved:
        l_lookup_idx = None
        for i, lk in enumerate(gsub.LookupList.Lookup):
            if lk.LookupType == 1:
                for st in lk.SubTable:
                    if hasattr(st, "mapping") and st.mapping.get("l") == "l.curved":
                        l_lookup_idx = i
                        break
            if l_lookup_idx is not None:
                break

        if l_lookup_idx is None:
            st = ot.SingleSubst()
            st.Format = 1
            st.mapping = {"l": "l.curved"}
            lk = ot.Lookup()
            lk.LookupType = 1
            lk.LookupFlag = 0
            lk.SubTable = [st]
            lk.SubTableCount = 1
            l_lookup_idx = len(gsub.LookupList.Lookup)
            gsub.LookupList.Lookup.append(lk)
            gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
            print(f"  [{font_path.name}] Created SingleSubst Lookup {l_lookup_idx}: 'l' -> 'l.curved'")
            modified = True

        ensure_feature_record(gsub, "cv05", l_lookup_idx)
        modified = True

    # I -> I.serif
    if has_I_serif:
        I_lookup_idx = None
        for i, lk in enumerate(gsub.LookupList.Lookup):
            if lk.LookupType == 1:
                for st in lk.SubTable:
                    if hasattr(st, "mapping") and st.mapping.get("I") == "I.serif":
                        I_lookup_idx = i
                        break
            if I_lookup_idx is not None:
                break

        if I_lookup_idx is None:
            st = ot.SingleSubst()
            st.Format = 1
            st.mapping = {"I": "I.serif"}
            lk = ot.Lookup()
            lk.LookupType = 1
            lk.LookupFlag = 0
            lk.SubTable = [st]
            lk.SubTableCount = 1
            I_lookup_idx = len(gsub.LookupList.Lookup)
            gsub.LookupList.Lookup.append(lk)
            gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
            print(f"  [{font_path.name}] Created SingleSubst Lookup {I_lookup_idx}: 'I' -> 'I.serif'")
            modified = True

        ensure_feature_record(gsub, "ss02", I_lookup_idx)
        modified = True

    # Also perform mapping verification for any pre-existing features
    if gsub.FeatureList is not None:
        for fr in gsub.FeatureList.FeatureRecord:
            tag = fr.FeatureTag
            if tag == "cv05" and has_l_curved:
                for idx in fr.Feature.LookupListIndex:
                    if idx < len(gsub.LookupList.Lookup):
                        lk = gsub.LookupList.Lookup[idx]
                        for st in lk.SubTable:
                            if hasattr(st, "mapping") and "l" in st.mapping:
                                if st.mapping["l"] != "l.curved":
                                    print(f"  [{font_path.name}] Correcting cv05 Lookup {idx}: 'l' -> {st.mapping['l']} => 'l.curved'")
                                    st.mapping["l"] = "l.curved"
                                    modified = True
            elif tag == "ss02" and has_I_serif:
                for idx in fr.Feature.LookupListIndex:
                    if idx < len(gsub.LookupList.Lookup):
                        lk = gsub.LookupList.Lookup[idx]
                        for st in lk.SubTable:
                            if hasattr(st, "mapping") and "I" in st.mapping:
                                if st.mapping["I"] != "I.serif":
                                    print(f"  [{font_path.name}] Correcting ss02 Lookup {idx}: 'I' -> {st.mapping['I']} => 'I.serif'")
                                    st.mapping["I"] = "I.serif"
                                    modified = True
            elif tag in ("cv08", "zero") and has_zero_slash:
                for idx in fr.Feature.LookupListIndex:
                    if idx < len(gsub.LookupList.Lookup):
                        lk = gsub.LookupList.Lookup[idx]
                        for st in lk.SubTable:
                            if hasattr(st, "mapping") and "zero" in st.mapping:
                                if st.mapping["zero"] != "zero.slash":
                                    print(f"  [{font_path.name}] Correcting {tag} Lookup {idx}: 'zero' -> {st.mapping['zero']} => 'zero.slash'")
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
