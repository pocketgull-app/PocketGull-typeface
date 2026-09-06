import copy
import json
import os
import shutil
import sys
import time
from pathlib import Path
from fontTools.ttLib import TTCollection, TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

ROOT_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
REF_TTC_PATH = Path(r"C:\Windows\Fonts\Nirmala.ttc")
TELEMETRY_PATH = ROOT_DIR / "fonts" / "tier3_indic_telemetry.json"

TARGET_FONTS = [
    {"filename": "PocketGull-Fineliner.ttf", "weight": 400, "is_mono": False, "src_idx": 0},
    {"filename": "PocketGull-Bold.ttf", "weight": 700, "is_mono": False, "src_idx": 1},
    {"filename": "PocketGull-Chiseltip.ttf", "weight": 900, "is_mono": False, "src_idx": 1},
    {"filename": "PocketGullMono-Regular.ttf", "weight": 400, "is_mono": True, "src_idx": 0},
]

# Complete Indic Core Range: All 10 major scripts of the Indian Subcontinent
INDIC_RANGES = [
    ("Devanagari", 0x0900, 0x097F),
    ("Bengali",    0x0980, 0x09FF),
    ("Gurmukhi",   0x0A00, 0x0A7F),
    ("Gujarati",   0x0A80, 0x0AFF),
    ("Oriya",      0x0B00, 0x0B7F),
    ("Tamil",      0x0B80, 0x0BFF),
    ("Telugu",     0x0C00, 0x0C7F),
    ("Kannada",    0x0C80, 0x0CFF),
    ("Malayalam",  0x0D00, 0x0D7F),
    ("Sinhala",    0x0D80, 0x0DFF),
    ("Vedic Extensions", 0x1CD0, 0x1CFF),
]

def decompose_glyph(src_glyph_name, ref_glyph_set):
    rec_pen = DecomposingRecordingPen(ref_glyph_set)
    ref_glyph_set[src_glyph_name].draw(rec_pen)
    tt_pen = TTGlyphPen(ref_glyph_set)
    rec_pen.replay(tt_pen)
    return tt_pen.glyph()

def compile_tier3_indic():
    print("=" * 70)
    print("  POCKETGULL TYPEFOUNDRY: FULL TIER 3 INDIC CORE COMPILER")
    print("  Scripts: Devanagari, Bengali, Gurmukhi, Gujarati, Oriya,")
    print("           Tamil, Telugu, Kannada, Malayalam, Sinhala, Vedic")
    print("=" * 70)

    if not REF_TTC_PATH.exists():
        print(f"[ERROR] Reference font not found at {REF_TTC_PATH}")
        sys.exit(1)

    overall_start = time.perf_counter()
    ttc = TTCollection(str(REF_TTC_PATH))

    ref_font_sample = ttc.fonts[0]
    ref_cmap_sample = ref_font_sample.getBestCmap()

    target_cps = []
    for script_name, start_cp, end_cp in INDIC_RANGES:
        cps = [cp for cp in range(start_cp, end_cp + 1) if cp in ref_cmap_sample]
        target_cps.extend(cps)
        print(f"  • {script_name} (U+{start_cp:04X}–U+{end_cp:04X}): {len(cps)} codepoints discovered")

    target_cps = sorted(list(set(target_cps)))
    print(f"\n  Total Indic Core codepoints to compile: {len(target_cps)}")
    print(f"  Total Superfamily Glyphs: {len(target_cps) * len(TARGET_FONTS):,}")

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
        ref_cmap = ref_font.getBestCmap()
        ref_glyph_set = ref_font.getGlyphSet()
        ref_hmtx = ref_font["hmtx"]

        dest_font = TTFont(str(ttf_path))
        dest_glyf = dest_font["glyf"]
        dest_hmtx = dest_font["hmtx"]

        new_glyphs_added = 0

        for cp in target_cps:
            src_gname = ref_cmap[cp]
            src_adv, src_lsb = ref_hmtx[src_gname]
            dest_gname = f"u{cp:04X}"

            glyph = decompose_glyph(src_gname, ref_glyph_set)

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

            for table in dest_font["cmap"].tables:
                if table.format in (4, 12):
                    table.cmap[cp] = dest_gname

        dest_font.setGlyphOrder(dest_glyf.glyphOrder)

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
        "script": "Tier 3: Indic Full Subcontinent Suite (10 Scripts + Vedic)",
        "unicode_ranges": [f"U+{s[1]:04X}-U+{s[2]:04X}" for s in INDIC_RANGES],
        "codepoints_synthesized": len(target_cps),
        "fonts_updated": telemetry_fonts,
        "total_glyphs_compiled": total_glyphs_compiled,
        "runtime_ms": round(overall_elapsed_ms, 2),
        "manual_hours_benchmark": manual_hours,
        "acceleration_factor": accel_factor
    }

    with open(TELEMETRY_PATH, "w", encoding="utf-8") as f:
        json.dump(telemetry_data, f, indent=2)

    print(f"\n[SUCCESS] Compiled {total_glyphs_compiled:,} Indic Core glyphs in {overall_elapsed_ms:.2f} ms ({accel_factor:,}x acceleration)")

if __name__ == "__main__":
    compile_tier3_indic()
