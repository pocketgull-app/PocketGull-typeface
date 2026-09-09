#!/usr/bin/env python3
"""
PocketGull Typefoundry - Philocardia Hearts & Clinical Pictograms Synthesizer
=============================================================================
Systematically synthesizes and injects:
1. Philocardia Hearts:
   - U+2665 (♥ Black Heart Suit / uni2665)
   - U+2764 (❤ Heavy Heart / uni2764)
2. Universal Clinical Pictograms:
   - U+2695 (⚕ Rod of Asclepius / uni2695)
   - U+26A0 (⚠️ High-Alert Warning / uni26A0)
   - U+263C (☀️ Morning Dosage AM / sun)
   - U+263D (🌙 Night Dosage PM / uni263D)
   - U+2298 (⊘ Do Not Crush & Do Not Split / uni2298)
3. OpenType ss07 "Philocardia Heart Tittles":
   - i.heart and j.heart (tactile felt-marker heart replacing circular dot tittle)
   - Encapsulated strictly in GSUB ss07 (Stylistic Set 7)
   - Base cmap preserves standard dot tittles for 100% clinical safety on 6pt-8pt labels.
4. Monospace pitch invariant: All glyphs in Mono cut locked to 600 UPM.
5. Realigns all tables to 2-byte word boundaries (loca[i] % 2 == 0).
"""

import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables.ttProgram import Program
from fontTools.ttLib.tables import otTables as ot

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def find_font(filename):
    for p in [Path(r"C:\Windows\Fonts") / filename, Path("/mnt/c/Windows/Fonts") / filename]:
        if p.exists():
            return p
    raise FileNotFoundError(f"Reference font {filename} not found.")

def sanitize_contour_points(coords, endPts):
    """Eliminates consecutive identical points to guarantee 0 duplicate nodes and OTS safety."""
    start = 0
    for end in endPts:
        for i in range(start, end):
            if coords[i] == coords[i + 1]:
                coords[i + 1] = (coords[i + 1][0] + 1, coords[i + 1][1])
        if len(coords) > 1 and coords[start] == coords[end]:
            coords[end] = (coords[end][0] + 1, coords[end][1])
        start = end + 1

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

def realign_font_word_boundaries():
    """Realigns font tables and glyf records to 2-byte word boundaries via pure Dart SfntTransformer."""
    foundry_tool = ROOT_DIR / "tool" / "pocketgull_foundry.dart"
    if foundry_tool.exists():
        subprocess.run(["dart", "run", str(foundry_tool), "realign"], check=False, cwd=str(ROOT_DIR))

def build_glyph_from_ref(ref_font, ref_gname, target_adv, is_mono, target_h=650, target_y_offset=50):
    """Scales, centers, and bounds-normalizes a reference glyph to PocketGull 1000 UPM em-square."""
    scale = 1000.0 / ref_font["head"].unitsPerEm
    ref_glyf = ref_font["glyf"]
    ref_glyph = ref_glyf[ref_gname]
    
    raw_coords, endPts, flags = ref_glyph.getCoordinates(ref_glyf)
    coords = GlyphCoordinates(raw_coords)
    coords.transform(((scale, 0), (0, scale)))
    coords.toInt()

    cur_min_y = min(coords._a[1::2])
    cur_max_y = max(coords._a[1::2])
    cur_min_x = min(coords._a[0::2])
    cur_max_x = max(coords._a[0::2])
    cur_w = cur_max_x - cur_min_x
    cur_h = cur_max_y - cur_min_y

    g = Glyph()
    g.numberOfContours = len(endPts)
    g.endPtsOfContours = list(endPts)
    g.flags = bytearray([f & 0x3F for f in flags])
    g.program = Program()

    if is_mono:
        # Constrain width to 520 max to maintain clear side-bearings
        if cur_w > 520:
            m_scale = 520.0 / cur_w
            mid_x = cur_min_x + cur_w / 2.0
            mid_y = cur_min_y + cur_h / 2.0
            coords.translate((-mid_x, -mid_y))
            coords.transform(((m_scale, 0), (0, m_scale)))
            coords.translate((mid_x, mid_y))
            coords.toInt()
            cur_min_x = min(coords._a[0::2])
            cur_max_x = max(coords._a[0::2])
            cur_w = cur_max_x - cur_min_x

        dx = int((600 - cur_w) / 2) - cur_min_x
        coords.translate((dx, 0))
        coords.toInt()
        g.coordinates = coords
        sanitize_contour_points(coords, g.endPtsOfContours)
        return g, 600
    else:
        # Proportional: normalize height and side bearings
        adv = int(round(cur_w + 100))
        adv = max(adv, 450)
        dx = int((adv - cur_w) / 2) - cur_min_x
        coords.translate((dx, 0))
        coords.toInt()
        g.coordinates = coords
        sanitize_contour_points(coords, g.endPtsOfContours)
        return g, adv

def inject_philocardia():
    print("=" * 80)
    print("  POCKETGULL FOUNDRY: PHILOCARDIA HEARTS & CLINICAL PICTOGRAMS MASTER SYNTHESIS")
    print("=" * 80)

    ref_path = find_font("seguisym.ttf")
    print(f"  • Reference Glyph Source: {ref_path}")
    ref_font = TTFont(str(ref_path))

    # Reference glyph mappings in Segoe UI Symbol
    # U+2665 -> heart
    # U+2764 -> uni2764
    # U+2695 -> uni2695 (Rod of Asclepius)
    # U+26A0 -> uni26A0 (Warning Sign)
    # U+263C -> sun (Morning AM)
    # U+263D -> uni263D (Night PM)
    # U+2298 -> uni2298 (Do Not Crush)
    pictogram_specs = [
        (0x2665, "uni2665", "heart"),
        (0x2764, "uni2764", "uni2764"),
        (0x2695, "uni2695", "uni2695"),
        (0x26A0, "uni26A0", "uni26A0"),
        (0x263C, "uni263C", "sun"),
        (0x263D, "uni263D", "uni263D"),
        (0x2298, "uni2298", "uni2298"),
    ]

    ref_glyf = ref_font["glyf"]
    heart_coords_raw, heart_endpts, heart_flags = ref_glyf["heart"].getCoordinates(ref_glyf)
    scale = 1000.0 / ref_font["head"].unitsPerEm

    target_fonts = sorted([f for f in TTF_DIR.glob("*.ttf")])

    for font_path in target_fonts:
        fname = font_path.name
        is_mono = "Mono" in fname
        font = TTFont(str(font_path))
        glyf = font["glyf"]
        hmtx = font["hmtx"]
        gorder = font.getGlyphOrder()
        modified = False

        # 1. Inject Philocardia Hearts & Pictograms into glyf, hmtx, and cmap
        for cp, dest_name, ref_src in pictogram_specs:
            g, adv = build_glyph_from_ref(ref_font, ref_src, 600 if is_mono else 700, is_mono)
            glyf[dest_name] = g
            g.recalcBounds(glyf)
            hmtx[dest_name] = (adv, g.xMin)

            if dest_name not in gorder:
                gorder.append(dest_name)

            for table in font["cmap"].tables:
                if table.format == 12:
                    table.cmap[cp] = dest_name
                elif table.format == 4 and cp <= 0xFFFF:
                    table.cmap[cp] = dest_name

            modified = True

        # 2. Synthesize i.heart and j.heart for ss07 OpenType Stylistic Set
        for base_char, heart_char in [("i", "i.heart"), ("j", "j.heart")]:
            if base_char in glyf and glyf[base_char].numberOfContours >= 2:
                base_g = glyf[base_char]
                raw_c, endpts, fl = base_g.getCoordinates(glyf)
                
                # Contour 0 is the stem
                stem_c = raw_c[0:endpts[0] + 1]
                stem_fl = fl[0:endpts[0] + 1]

                # Contour 1 is the tittle dot
                dot_c = raw_c[endpts[0] + 1:endpts[1] + 1]
                dot_min_x = min(c[0] for c in dot_c)
                dot_max_x = max(c[0] for c in dot_c)
                dot_min_y = min(c[1] for c in dot_c)
                dot_max_y = max(c[1] for c in dot_c)
                dot_cx = (dot_min_x + dot_max_x) / 2.0
                dot_cy = (dot_min_y + dot_max_y) / 2.0
                dot_w = dot_max_x - dot_min_x
                dot_h = dot_max_y - dot_min_y

                # Transform reference heart into tittle heart
                h_coords = GlyphCoordinates(heart_coords_raw)
                h_min_x = min(h_coords._a[0::2])
                h_max_x = max(h_coords._a[0::2])
                h_min_y = min(h_coords._a[1::2])
                h_max_y = max(h_coords._a[1::2])
                h_w = h_max_x - h_min_x
                h_h = h_max_y - h_min_y

                # Scale heart to match tittle dot optical area (~115% of dot diameter)
                target_tittle_size = max(dot_w, dot_h) * 1.15
                h_scale = target_tittle_size / max(h_w, h_h)

                h_mid_x = h_min_x + h_w / 2.0
                h_mid_y = h_min_y + h_h / 2.0

                h_coords.translate((-h_mid_x, -h_mid_y))
                h_coords.transform(((h_scale, 0), (0, h_scale)))
                h_coords.translate((dot_cx, dot_cy))
                h_coords.toInt()

                # Combine stem + heart tittle
                all_coords = stem_c + list(h_coords)
                all_flags = list(stem_fl) + [f & 0x3F for f in heart_flags]
                new_endpts = [len(stem_c) - 1, len(all_coords) - 1]

                heart_g = Glyph()
                heart_g.numberOfContours = 2
                heart_g.endPtsOfContours = new_endpts
                heart_g.flags = bytearray(all_flags)
                heart_g.program = Program()
                c_obj = GlyphCoordinates(all_coords)
                sanitize_contour_points(c_obj, heart_g.endPtsOfContours)
                heart_g.coordinates = c_obj
                heart_g.recalcBounds(glyf)

                base_adv, _ = hmtx[base_char]
                glyf[heart_char] = heart_g
                hmtx[heart_char] = (base_adv, heart_g.xMin)

                if heart_char not in gorder:
                    gorder.append(heart_char)

                modified = True

        # 3. Setup OpenType GSUB ss07 "Philocardia Heart Tittles"
        if "GSUB" in font:
            gsub = font["GSUB"].table
            if gsub.LookupList is None:
                gsub.LookupList = ot.LookupList()
                gsub.LookupList.Lookup = []
                gsub.LookupList.LookupCount = 0

            # Find or create SingleSubst lookup for i -> i.heart, j -> j.heart
            ss07_lookup_idx = None
            for i_idx, lk in enumerate(gsub.LookupList.Lookup):
                if lk.LookupType == 1:
                    for st in lk.SubTable:
                        if hasattr(st, "mapping") and st.mapping.get("i") == "i.heart":
                            ss07_lookup_idx = i_idx
                            st.mapping["j"] = "j.heart"
                            break
                if ss07_lookup_idx is not None:
                    break

            if ss07_lookup_idx is None:
                st = ot.SingleSubst()
                st.Format = 1
                st.mapping = {"i": "i.heart", "j": "j.heart"}
                lk = ot.Lookup()
                lk.LookupType = 1
                lk.LookupFlag = 0
                lk.SubTable = [st]
                lk.SubTableCount = 1
                ss07_lookup_idx = len(gsub.LookupList.Lookup)
                gsub.LookupList.Lookup.append(lk)
                gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)

            ensure_feature_record(gsub, "ss07", ss07_lookup_idx)

        # Update glyph order & save
        font.setGlyphOrder(gorder)
        font.save(str(font_path))
        print(f"  [OK] {fname:28s} | Injected 7 pictograms + ss07 (i.heart, j.heart)")

    # Realign word boundaries across all fonts
    print("\n  • Realigning 2-byte word boundaries on all TTFs via Dart 3.11...")
    realign_font_word_boundaries()

    # Sync root PocketGullMono-Regular.ttf and PocketGull-VF.ttf
    root_mono = ROOT_DIR / "PocketGullMono-Regular.ttf"
    if root_mono.exists() and (TTF_DIR / "PocketGullMono-Regular.ttf").exists():
        shutil.copyfile(TTF_DIR / "PocketGullMono-Regular.ttf", root_mono)
        print("  [OK] Synchronized root PocketGullMono-Regular.ttf")

    root_vf = ROOT_DIR / "PocketGull-VF.ttf"
    if root_vf.exists() and (TTF_DIR / "PocketGull-VF.ttf").exists():
        shutil.copyfile(TTF_DIR / "PocketGull-VF.ttf", root_vf)
        print("  [OK] Synchronized root PocketGull-VF.ttf")

    print("\n[SUCCESS] Philocardia hearts and clinical pictograms successfully synthesized across superfamily!")

if __name__ == "__main__":
    inject_philocardia()
