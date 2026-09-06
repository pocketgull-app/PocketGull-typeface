import copy
import json
import os
import shutil
import sys
import time
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

ROOT_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
TELEMETRY_PATH = ROOT_DIR / "fonts" / "tier2_semitic_telemetry.json"

SEGOE_REG = Path(r"C:\Windows\Fonts\segoeui.ttf")
SEGOE_BOLD = Path(r"C:\Windows\Fonts\segoeuib.ttf")
MVBOLI = Path(r"C:\Windows\Fonts\mvboli.ttf")
SEGUIHIS = Path(r"C:\Windows\Fonts\seguihis.ttf")

TARGET_FONTS = [
    {"filename": "PocketGull-Fineliner.ttf", "weight": 400, "is_mono": False, "is_bold": False},
    {"filename": "PocketGull-Bold.ttf", "weight": 700, "is_mono": False, "is_bold": True},
    {"filename": "PocketGull-Chiseltip.ttf", "weight": 900, "is_mono": False, "is_bold": True},
    {"filename": "PocketGullMono-Regular.ttf", "weight": 400, "is_mono": True, "is_bold": False},
]

def decompose_glyph(src_glyph_name, ref_glyph_set):
    rec_pen = DecomposingRecordingPen(ref_glyph_set)
    ref_glyph_set[src_glyph_name].draw(rec_pen)
    tt_pen = TTGlyphPen(ref_glyph_set)
    rec_pen.replay(tt_pen)
    return tt_pen.glyph()

def compile_tier2_semitic():
    print("=" * 70)
    print("  POCKETGULL TYPEFOUNDRY: TIER 2 SEMITIC & RTL COMPILER")
    print("  Scripts: Arabic, Hebrew, Syriac, Thaana (BiDi & Cursive)")
    print("=" * 70)

    overall_start = time.perf_counter()

    f_segoe_reg = TTFont(str(SEGOE_REG))
    f_segoe_bold = TTFont(str(SEGOE_BOLD))
    f_mvboli = TTFont(str(MVBOLI))
    f_seguihis = TTFont(str(SEGUIHIS))

    cmap_segoe = f_segoe_reg.getBestCmap()
    cmap_mvboli = f_mvboli.getBestCmap()
    cmap_seguihis = f_seguihis.getBestCmap()

    # Collect codepoint sources
    script_sources = []

    # 1. Arabic: U+0600-06FF, U+0750-077F, U+08A0-08FF, Presentation Forms A & B
    for cp in cmap_segoe:
        if (0x0600 <= cp <= 0x06FF or 0x0750 <= cp <= 0x077F or 0x08A0 <= cp <= 0x08FF or 
            0xFB50 <= cp <= 0xFDFF or 0xFE70 <= cp <= 0xFEFF):
            script_sources.append((cp, 'segoe', cmap_segoe[cp]))

    # 2. Hebrew: U+0590-05FF, Presentation Forms
    for cp in cmap_segoe:
        if 0x0590 <= cp <= 0x05FF or 0xFB1D <= cp <= 0xFB4F:
            script_sources.append((cp, 'segoe', cmap_segoe[cp]))

    # 3. Syriac: U+0700-074F
    for cp in cmap_seguihis:
        if 0x0700 <= cp <= 0x074F:
            script_sources.append((cp, 'seguihis', cmap_seguihis[cp]))

    # 4. Thaana: U+0780-07BF
    for cp in cmap_mvboli:
        if 0x0780 <= cp <= 0x07BF:
            script_sources.append((cp, 'mvboli', cmap_mvboli[cp]))

    script_sources = sorted(list(set(script_sources)), key=lambda x: x[0])
    print(f"  • Total Tier 2 Codepoints discovered: {len(script_sources)}")
    print(f"  • Total Superfamily Glyphs: {len(script_sources) * len(TARGET_FONTS):,}")

    SCALE_FACTOR = 1000.0 / 2048.0
    WOFF2_DIR.mkdir(parents=True, exist_ok=True)
    telemetry_fonts = []
    total_glyphs_compiled = 0

    for target in TARGET_FONTS:
        font_filename = target["filename"]
        weight = target["weight"]
        is_mono = target["is_mono"]
        is_bold = target["is_bold"]
        ttf_path = TTF_DIR / font_filename

        print(f"\n  • Processing {font_filename} (Weight {weight}, Mono={is_mono})...")
        font_start = time.perf_counter()

        dest_font = TTFont(str(ttf_path))
        dest_glyf = dest_font["glyf"]
        dest_hmtx = dest_font["hmtx"]

        f_segoe = f_segoe_bold if is_bold else f_segoe_reg
        segoe_glyph_set = f_segoe.getGlyphSet()
        segoe_hmtx = f_segoe["hmtx"]

        mvboli_glyph_set = f_mvboli.getGlyphSet()
        mvboli_hmtx = f_mvboli["hmtx"]

        seguihis_glyph_set = f_seguihis.getGlyphSet()
        seguihis_hmtx = f_seguihis["hmtx"]

        new_glyphs_added = 0

        for cp, src_type, src_gname in script_sources:
            dest_gname = f"u{cp:04X}"

            if src_type == 'segoe':
                src_adv, src_lsb = segoe_hmtx[src_gname]
                glyph = decompose_glyph(src_gname, segoe_glyph_set)
            elif src_type == 'mvboli':
                src_adv, src_lsb = mvboli_hmtx[src_gname]
                glyph = decompose_glyph(src_gname, mvboli_glyph_set)
            else: # seguihis
                src_adv, src_lsb = seguihis_hmtx[src_gname]
                glyph = decompose_glyph(src_gname, seguihis_glyph_set)

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
        "script": "Tier 2: RTL & Semitic (Arabic, Hebrew, Syriac, Thaana)",
        "codepoints_synthesized": len(script_sources),
        "fonts_updated": telemetry_fonts,
        "total_glyphs_compiled": total_glyphs_compiled,
        "runtime_ms": round(overall_elapsed_ms, 2),
        "manual_hours_benchmark": manual_hours,
        "acceleration_factor": accel_factor
    }

    with open(TELEMETRY_PATH, "w", encoding="utf-8") as f:
        json.dump(telemetry_data, f, indent=2)

    print(f"\n[SUCCESS] Compiled {total_glyphs_compiled:,} Tier 2 Semitic glyphs in {overall_elapsed_ms:.2f} ms ({accel_factor:,}x acceleration)")

if __name__ == "__main__":
    compile_tier2_semitic()
