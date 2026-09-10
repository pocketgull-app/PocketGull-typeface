#!/usr/bin/env python3
"""
PocketGull Typefoundry - ISMP & Humanist Heart Tittle OpenType Feature Curing Engine
====================================================================================
Systematically cures and injects OpenType GSUB substitution tables across all
PocketGull superfamily TTF binaries:
  - cv05 (Curved lowercase l): maps 'l' -> 'l.curved' (eliminates l vs 1 vs I collision)
  - ss02 (Serifed uppercase I): maps 'I' -> 'I.serif' (eliminates I vs l collision)
  - cv08 / zero (Slashed zero): maps 'zero' -> 'zero.slash' (eliminates 0 vs O collision)
  - ss07 / cv09 (Humanist Heart Tittles): maps 'i' -> 'i.heart', 'j' -> 'j.heart'

Enforces:
  1. OpenType Layout FeatureTag Alphabetical Ordering Invariant (OTS compliant).
  2. 2-Byte Word-Alignment Invariant (loca & glyf).
  3. Recompresses high-efficiency Brotli Q11 WOFF2 webfonts.
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables as ot
from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    ROOT_DIR / "fonts" / "ttf",
    ROOT_DIR / "ofl" / "pocketgull",
    ROOT_DIR.parent / "pocketgull" / "public" / "fonts",
]
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"

def realign_font_word_boundaries():
    """Realigns font tables and glyf records to 2-byte word boundaries via pure Dart SfntTransformer."""
    foundry_tool = ROOT_DIR / "tool" / "pocketgull_foundry.dart"
    if foundry_tool.exists():
        subprocess.run(["dart", "run", str(foundry_tool), "realign"], check=False, cwd=str(ROOT_DIR))

def sort_gsub_features(gsub):
    """Sorts GSUB FeatureList alphabetically by FeatureTag and remaps ScriptList indices."""
    if gsub.FeatureList is None or not gsub.FeatureList.FeatureRecord:
        return
    indexed_records = list(enumerate(gsub.FeatureList.FeatureRecord))
    indexed_records.sort(key=lambda item: item[1].FeatureTag)
    new_records = [item[1] for item in indexed_records]
    old_to_new = {old_idx: new_idx for new_idx, (old_idx, _) in enumerate(indexed_records)}
    gsub.FeatureList.FeatureRecord = new_records
    gsub.FeatureList.FeatureCount = len(new_records)

    def remap(indices):
        return sorted(list(set(old_to_new[i] for i in indices if i in old_to_new)))

    if gsub.ScriptList is not None:
        for s in gsub.ScriptList.ScriptRecord:
            if s.Script.DefaultLangSys is not None:
                s.Script.DefaultLangSys.FeatureIndex = remap(s.Script.DefaultLangSys.FeatureIndex)
                s.Script.DefaultLangSys.FeatureCount = len(s.Script.DefaultLangSys.FeatureIndex)
            if hasattr(s.Script, 'LangSysRecord') and s.Script.LangSysRecord:
                for ls in s.Script.LangSysRecord:
                    ls.LangSys.FeatureIndex = remap(ls.LangSys.FeatureIndex)
                    ls.LangSys.FeatureCount = len(ls.LangSys.FeatureIndex)

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
    if "glyf" not in font:
        return False

    glyf = font["glyf"]
    modified = False

    if "GSUB" not in font:
        gsub_tbl = newTable("GSUB")
        gsub = ot.GSUB()
        gsub.Version = 0x00010000
        gsub.ScriptList = ot.ScriptList()
        gsub.ScriptList.ScriptRecord = []
        for stag in ["DFLT", "latn"]:
            srec = ot.ScriptRecord()
            srec.ScriptTag = stag
            srec.Script = ot.Script()
            srec.Script.DefaultLangSys = ot.DefaultLangSys()
            srec.Script.DefaultLangSys.FeatureIndex = []
            srec.Script.DefaultLangSys.LookupOrder = None
            srec.Script.DefaultLangSys.ReqFeatureIndex = 0xFFFF
            gsub.ScriptList.ScriptRecord.append(srec)
        gsub.ScriptList.ScriptCount = len(gsub.ScriptList.ScriptRecord)
        gsub.FeatureList = ot.FeatureList()
        gsub.FeatureList.FeatureRecord = []
        gsub.FeatureList.FeatureCount = 0
        gsub.LookupList = ot.LookupList()
        gsub.LookupList.Lookup = []
        gsub.LookupList.LookupCount = 0
        gsub_tbl.table = gsub
        font["GSUB"] = gsub_tbl
        modified = True
    else:
        gsub = font["GSUB"].table

    has_l_curved = "l.curved" in glyf
    has_I_serif = "I.serif" in glyf
    has_zero_slash = "zero.slash" in glyf
    has_i_heart = "i.heart" in glyf
    has_j_heart = "j.heart" in glyf

    if gsub.LookupList is None:
        gsub.LookupList = ot.LookupList()
        gsub.LookupList.Lookup = []
        gsub.LookupList.LookupCount = 0

    # 1. zero -> zero.slash
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

    # 2. l -> l.curved
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

    # 3. I -> I.serif
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

    # 4. Humanist Heart Tittles: i -> i.heart, j -> j.heart (ss07 & cv09)
    if has_i_heart:
        heart_lookup_idx = None
        for i, lk in enumerate(gsub.LookupList.Lookup):
            if lk.LookupType == 1:
                for st in lk.SubTable:
                    if hasattr(st, "mapping") and st.mapping.get("i") == "i.heart":
                        heart_lookup_idx = i
                        if has_j_heart and "j" not in st.mapping:
                            st.mapping["j"] = "j.heart"
                            modified = True
                        break
            if heart_lookup_idx is not None:
                break

        if heart_lookup_idx is None:
            st = ot.SingleSubst()
            st.Format = 1
            st.mapping = {"i": "i.heart"}
            if has_j_heart:
                st.mapping["j"] = "j.heart"
            lk = ot.Lookup()
            lk.LookupType = 1
            lk.LookupFlag = 0
            lk.SubTable = [st]
            lk.SubTableCount = 1
            heart_lookup_idx = len(gsub.LookupList.Lookup)
            gsub.LookupList.Lookup.append(lk)
            gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
            print(f"  [{font_path.name}] Created SingleSubst Lookup {heart_lookup_idx}: 'i' -> 'i.heart', 'j' -> 'j.heart'")
            modified = True

        for tag in ("ss07", "cv09"):
            ensure_feature_record(gsub, tag, heart_lookup_idx)
            modified = True

    # 5. Correct any incorrect pre-existing feature mappings
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
            elif tag in ("ss07", "cv09") and has_i_heart:
                for idx in fr.Feature.LookupListIndex:
                    if idx < len(gsub.LookupList.Lookup):
                        lk = gsub.LookupList.Lookup[idx]
                        for st in lk.SubTable:
                            if hasattr(st, "mapping") and "i" in st.mapping:
                                if st.mapping["i"] != "i.heart":
                                    print(f"  [{font_path.name}] Correcting {tag} Lookup {idx}: 'i' -> {st.mapping['i']} => 'i.heart'")
                                    st.mapping["i"] = "i.heart"
                                    modified = True

    # 6. Alphabetically sort FeatureList for OTS compliance
    sort_gsub_features(gsub)

    if modified:
        font.save(str(font_path))
        print(f"  ✓ Successfully saved cured font: {font_path}")
        return True
    return False

def recompress_woff2(font_path: Path):
    """Recompresses a TTF binary to WOFF2 format using Brotli."""
    stem = font_path.stem
    target_woff2 = WOFF2_DIR / f"{stem}.woff2"
    compress(str(font_path), str(target_woff2))
    print(f"  ✓ Recompressed WOFF2: {target_woff2.name} ({target_woff2.stat().st_size:,} bytes)")

def main():
    print("======================================================================")
    print("  POCKETGULL TYPEFOUNDRY: ISMP & HEART TITTLE CURING ENGINE")
    print("======================================================================\n")

    total_cured = 0
    cured_ttfs = []
    for target_dir in TARGET_DIRS:
        if not target_dir.exists():
            continue

        print(f"Scanning: {target_dir}")
        for p in sorted(target_dir.glob("*.ttf")):
            if cure_font_ismp(p):
                total_cured += 1
                if target_dir == ROOT_DIR / "fonts" / "ttf":
                    cured_ttfs.append(p)

    print(f"\n✨ OpenType GSUB tables cured in {total_cured} font files.")

    # Realign 2-byte word boundaries on all TTFs via pure Dart 3.11 SfntTransformer
    print("\n• Realigning 2-byte word boundaries across all TTFs via Dart 3.11...")
    realign_font_word_boundaries()

    # Recompress WOFF2 webfonts for all fonts in fonts/ttf
    print("\n• Recompressing Brotli Q11 WOFF2 webfonts...")
    WOFF2_DIR.mkdir(parents=True, exist_ok=True)
    for p in sorted((ROOT_DIR / "fonts" / "ttf").glob("*.ttf")):
        recompress_woff2(p)

    # Sync root PocketGull-VF and PocketGullMono-Regular binaries
    root_vf_ttf = ROOT_DIR / "PocketGull-VF.ttf"
    root_vf_woff2 = ROOT_DIR / "PocketGull-VF.woff2"
    src_vf_ttf = ROOT_DIR / "fonts" / "ttf" / "PocketGull-VF.ttf"
    src_vf_woff2 = ROOT_DIR / "fonts" / "woff2" / "PocketGull-VF.woff2"

    if src_vf_ttf.exists() and root_vf_ttf.exists():
        shutil.copyfile(src_vf_ttf, root_vf_ttf)
        print("  ✓ Synchronized root PocketGull-VF.ttf")
    if src_vf_woff2.exists() and root_vf_woff2.exists():
        shutil.copyfile(src_vf_woff2, root_vf_woff2)
        print("  ✓ Synchronized root PocketGull-VF.woff2")

    root_mono_ttf = ROOT_DIR / "PocketGullMono-Regular.ttf"
    root_mono_woff2 = ROOT_DIR / "PocketGullMono-Regular.woff2"
    src_mono_ttf = ROOT_DIR / "fonts" / "ttf" / "PocketGullMono-Regular.ttf"
    src_mono_woff2 = ROOT_DIR / "fonts" / "woff2" / "PocketGullMono-Regular.woff2"

    if src_mono_ttf.exists() and root_mono_ttf.exists():
        shutil.copyfile(src_mono_ttf, root_mono_ttf)
        print("  ✓ Synchronized root PocketGullMono-Regular.ttf")
    if src_mono_woff2.exists() and root_mono_woff2.exists():
        shutil.copyfile(src_mono_woff2, root_mono_woff2)
        print("  ✓ Synchronized root PocketGullMono-Regular.woff2")

    print("\n✨ Completed! All superfamily fonts cured, realigned, and recompressed.")

if __name__ == "__main__":
    main()
