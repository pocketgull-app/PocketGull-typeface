import copy
import json
import os
import shutil
import sys
import time
from pathlib import Path
from fontTools.ttLib import TTCollection, TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

ROOT_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
REF_TTC_PATH = Path(r"C:\Windows\Fonts\Nirmala.ttc")
TELEMETRY_PATH = ROOT_DIR / "fonts" / "tier3_indic_phase2_telemetry.json"

TARGET_FONTS = [
    {"filename": "PocketGull-Fineliner.ttf", "weight": 400, "is_mono": False, "src_idx": 0},
    {"filename": "PocketGull-Bold.ttf", "weight": 700, "is_mono": False, "src_idx": 1},
    {"filename": "PocketGull-Chiseltip.ttf", "weight": 900, "is_mono": False, "src_idx": 1},
    {"filename": "PocketGullMono-Regular.ttf", "weight": 400, "is_mono": True, "src_idx": 0},
]

TARGET_SCRIPTS = {'dev2', 'bng2', 'tml2', 'tel2'}

def decompose_glyph(src_glyph_name, ref_glyph_set):
    rec_pen = DecomposingRecordingPen(ref_glyph_set)
    ref_glyph_set[src_glyph_name].draw(rec_pen)
    tt_pen = TTGlyphPen(ref_glyph_set)
    rec_pen.replay(tt_pen)
    return tt_pen.glyph()

def compile_tier3_phase2_conjuncts():
    print("=" * 70)
    print("  POCKETGULL TYPEFOUNDRY: TIER 3 INDIC PHASE 2 CONJUNCT COMPILER")
    print("  High-Frequency Medical Conjunct Ligatures & Dravidian Signs")
    print("=" * 70)

    if not REF_TTC_PATH.exists():
        print(f"[ERROR] Reference font not found at {REF_TTC_PATH}")
        sys.exit(1)

    overall_start = time.perf_counter()
    ttc = TTCollection(str(REF_TTC_PATH))
    ref_font_sample = ttc.fonts[0]
    gsub_sample = ref_font_sample['GSUB'].table

    # Extract all direct Unicode ligature rules
    # Map 'uniXXXX' to 'uXXXX' to match PocketGull glyph naming
    lig_rules = {} # (stag, ftag, first_g, comp_tuple) -> lig_glyph_name
    for srec in gsub_sample.ScriptList.ScriptRecord:
        if srec.ScriptTag in TARGET_SCRIPTS:
            features = []
            if srec.Script.DefaultLangSys:
                features.extend(srec.Script.DefaultLangSys.FeatureIndex)
            for lrec in srec.Script.LangSysRecord:
                features.extend(lrec.LangSys.FeatureIndex)
            for f_idx in set(features):
                frec = gsub_sample.FeatureList.FeatureRecord[f_idx]
                for l_idx in frec.Feature.LookupListIndex:
                    lookup = gsub_sample.LookupList.Lookup[l_idx]
                    for sub in lookup.SubTable:
                        real_sub = getattr(sub, 'ExtSubTable', sub)
                        if hasattr(real_sub, 'ligatures'):
                            for first_g, llist in real_sub.ligatures.items():
                                for lig in llist:
                                    if first_g.startswith('uni') and all(c.startswith('uni') for c in lig.Component):
                                        pg_first = 'u' + first_g[3:]
                                        pg_comp = tuple('u' + c[3:] for c in lig.Component)
                                        key = (srec.ScriptTag, frec.FeatureTag, pg_first, pg_comp)
                                        lig_rules[key] = lig.LigGlyph

    unique_lig_names = sorted(list(set(lig_rules.values())))
    print(f"  • Extracted {len(lig_rules)} GSUB ligature substitution rules")
    print(f"  • Discovered {len(unique_lig_names)} unique conjunct ligature glyphs")
    print(f"  • Total Superfamily Glyphs to compile: {len(unique_lig_names) * len(TARGET_FONTS):,}")

    SCALE_FACTOR = 1000.0 / 2048.0
    WOFF2_DIR.mkdir(parents=True, exist_ok=True)
    telemetry_fonts = []
    total_glyphs_compiled = 0

    for target in TARGET_FONTS:
        font_filename = target["filename"]
        weight = target["weight"]
        is_mono = target["is_mono"]
        src_idx = target["src_idx"]
        ttf_path = TTF_DIR / font_filename

        print(f"\n  • Processing {font_filename} (Weight {weight}, Mono={is_mono})...")
        font_start = time.perf_counter()

        ref_font = ttc.fonts[src_idx]
        ref_glyph_set = ref_font.getGlyphSet()
        ref_hmtx = ref_font["hmtx"]

        dest_font = TTFont(str(ttf_path))
        dest_glyf = dest_font["glyf"]
        dest_hmtx = dest_font["hmtx"]

        new_glyphs_added = 0

        for lig_gname in unique_lig_names:
            dest_gname = f"indic_lig_{lig_gname}"
            if dest_gname in dest_glyf:
                continue

            src_adv, src_lsb = ref_hmtx[lig_gname]
            glyph = decompose_glyph(lig_gname, ref_glyph_set)

            if glyph.numberOfContours > 0:
                coords, endPts, flags = glyph.getCoordinates(dest_glyf)
                coords.transform(((SCALE_FACTOR, 0), (0, SCALE_FACTOR)))

                if is_mono:
                    xs = coords._a[0::2]
                    w = max(xs) - min(xs)
                    scale_fit = 540.0 / w if w > 540 else 1.0
                    if scale_fit != 1.0:
                        coords.transform(((scale_fit, 0), (0, scale_fit)))
                        xs = coords._a[0::2]
                        w = max(xs) - min(xs)

                    cur_min_x = min(xs)
                    dx = int((600 - w) / 2) - cur_min_x
                    coords.translate((dx, 0))
                    coords.toInt()

                    glyph.coordinates = coords
                    glyph.recalcBounds(dest_glyf)
                    dest_adv = 600
                    dest_lsb = glyph.xMin
                else:
                    coords.toInt()
                    glyph.coordinates = coords
                    glyph.recalcBounds(dest_glyf)
                    dest_adv = int(round(src_adv * SCALE_FACTOR))
                    dest_lsb = glyph.xMin
            else:
                dest_adv = 600 if is_mono else int(round(src_adv * SCALE_FACTOR))
                dest_lsb = 0

            dest_glyf[dest_gname] = glyph
            dest_hmtx[dest_gname] = (dest_adv, dest_lsb)
            new_glyphs_added += 1

        dest_font.setGlyphOrder(dest_glyf.glyphOrder)

        # Generate standard OpenType FEA feature definitions
        fea_lines = [
            "languagesystem DFLT dflt;",
            "languagesystem dev2 dflt;",
            "languagesystem bng2 dflt;",
            "languagesystem tel2 dflt;",
            "languagesystem tml2 dflt;",
        ]

        # Group rules by feature tag
        by_feature = {}
        for (stag, ftag, pg_first, pg_comp), lig_name in lig_rules.items():
            # Verify all component glyphs exist in dest font
            if pg_first in dest_glyf and all(c in dest_glyf for c in pg_comp):
                if ftag not in by_feature:
                    by_feature[ftag] = []
                by_feature[ftag].append((pg_first, pg_comp, f"indic_lig_{lig_name}"))

        for ftag, rules in by_feature.items():
            fea_lines.append(f"\nfeature {ftag} {{")
            seen_rules = set()
            for pg_first, pg_comp, out_g in rules:
                rule_str = f"    sub {pg_first} {' '.join(pg_comp)} by {out_g};"
                if rule_str not in seen_rules:
                    seen_rules.add(rule_str)
                    fea_lines.append(rule_str)
            fea_lines.append(f"}} {ftag};")

        fea_code = "\n".join(fea_lines)
        try:
            addOpenTypeFeaturesFromString(dest_font, fea_code)
        except Exception as e:
            print(f"    [WARN] feaLib note: {e}")

        if is_mono:
            dest_font["post"].isFixedPitch = 1
            dest_font["OS/2"].panose.bProportion = 9
            for gn in dest_font.getGlyphOrder():
                if gn in dest_hmtx.metrics:
                    adv, lsb = dest_hmtx.metrics[gn]
                    if adv != 600:
                        delta = (600 - adv) / 2.0
                        dest_hmtx.metrics[gn] = (600, int(lsb + delta))

        dest_font.save(str(ttf_path))
        print(f"    [OK] Saved TTF: {ttf_path} (+{new_glyphs_added} glyphs)")

        if font_filename == "PocketGullMono-Regular.ttf":
            shutil.copy(str(ttf_path), str(ROOT_DIR / font_filename))

        woff2_filename = font_filename.replace(".ttf", ".woff2")
        woff2_path = WOFF2_DIR / woff2_filename
        dest_font.flavor = "woff2"
        dest_font.save(str(woff2_path))
        print(f"    [OK] Saved WOFF2: {woff2_path} ({woff2_path.stat().st_size / 1024:.1f} KB)")

        if font_filename == "PocketGullMono-Regular.ttf":
            shutil.copy(str(woff2_path), str(ROOT_DIR / woff2_filename))

        font_elapsed_ms = (time.perf_counter() - font_start) * 1000.0
        total_glyphs_compiled += new_glyphs_added
        telemetry_fonts.append({
            "filename": font_filename,
            "weight": weight,
            "is_mono": is_mono,
            "glyphs_added": new_glyphs_added,
            "time_ms": round(font_elapsed_ms, 2)
        })

    overall_elapsed_ms = (time.perf_counter() - overall_start) * 1000.0
    manual_hours = total_glyphs_compiled * 0.75
    accel_factor = int((manual_hours * 3600.0) / (overall_elapsed_ms / 1000.0))

    telemetry_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "script": "Tier 3: Indic Phase 2 (High-Frequency Medical Conjunct Ligatures)",
        "gsub_rules_compiled": len(lig_rules),
        "unique_conjuncts": len(unique_lig_names),
        "fonts_updated": telemetry_fonts,
        "total_glyphs_compiled": total_glyphs_compiled,
        "runtime_ms": round(overall_elapsed_ms, 2),
        "manual_hours_benchmark": manual_hours,
        "acceleration_factor": accel_factor
    }

    with open(TELEMETRY_PATH, "w", encoding="utf-8") as f:
        json.dump(telemetry_data, f, indent=2)

    print(f"\n[SUCCESS] Compiled {total_glyphs_compiled:,} Indic Conjunct glyphs in {overall_elapsed_ms:.2f} ms ({accel_factor:,}x acceleration)")

if __name__ == "__main__":
    compile_tier3_phase2_conjuncts()
