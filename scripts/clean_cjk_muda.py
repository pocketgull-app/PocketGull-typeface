#!/usr/bin/env python3
"""
scripts/clean_cjk_muda.py
=========================
Applies the Toyota Production System (TPS) Muda Elimination principle:
Removes accidental East Asian CJK, Hangul, Kana, and Kangxi codepoints
from PocketGull proportional TTF fonts.

Preserves 100% of:
- Latin (Extended, IPA, Archaic)
- Louise Sloan 5:1 Optotypes
- ISMP Clinical Disambiguation (slashed zero, curved l, serifed I, slashed Z)
- Greek & Cyrillic
- Canadian Aboriginal Syllabics (U+1400..U+167F)
- Duployan / Chinuk Pipa (U+1BC00..U+1BC9F)
- 256 Unicode Braille Patterns (U+2800..U+28FF)
- Box Drawing & ICU Telemetry (U+2500..U+257F)
- Arabic & Hebrew
- Cherokee, Ethiopic, Vai, Adlam, Tifinagh
- Math & General Punctuation

Also fixes:
- nameID 9 (Designer: Phil Gear)
- .notdef contour geometry (non-blank)
- OS/2 xAvgCharWidth
"""

import os
import sys
import glob
import unicodedata

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import _g_l_y_f
from fontTools.subset import Subsetter, Options

def is_cjk_muda(cp):
    # Hangul Jamo, Hangul Compatibility Jamo, Hangul Jamo Extended-A & B, Hangul Syllables
    if (0x1100 <= cp <= 0x11FF) or (0x3130 <= cp <= 0x318F) or (0xA960 <= cp <= 0xA97F) or (0xAC00 <= cp <= 0xD7AF) or (0xD7B0 <= cp <= 0xD7FF):
        return True
    # CJK Radicals, Kangxi, Ideographic Description, CJK Symbols & Punctuation, Hiragana, Katakana, Bopomofo, Kanbun, CJK Strokes, Katakana Phonetic, Enclosed CJK, CJK Compatibility, CJK Unified Ideographs, etc.
    if (0x2E80 <= cp <= 0x312F) or (0x3190 <= cp <= 0x9FFF) or (0xF900 <= cp <= 0xFAFF) or (0xFE30 <= cp <= 0xFE4F) or (0xFF65 <= cp <= 0xFF9F) or (0x1B000 <= cp <= 0x1B2FF) or (0x20000 <= cp <= 0x2FA1F):
        return True
    try:
        name = unicodedata.name(chr(cp), '')
        for keyword in ['CJK', 'HANGUL', 'HIRAGANA', 'KATAKANA', 'BOPOMOFO', 'IDEOGRAPHIC', 'KANGXI']:
            if keyword in name:
                return True
    except Exception:
        pass
    return False

def ensure_notdef_drawing(font):
    """Ensure .notdef has a simple rectangular outline so it's not blank."""
    if 'glyf' not in font:
        return
    glyf = font['glyf']
    if '.notdef' in glyf:
        notdef = glyf['.notdef']
        if notdef.numberOfContours == 0 or len(notdef.getCoordinates(glyf)[0]) == 0:
            # Draw standard rectangular box
            c1 = [(50, 0), (50, 700), (450, 700), (450, 0)]
            c2 = [(100, 50), (400, 50), (400, 650), (100, 650)]
            coords = _g_l_y_f.GlyphCoordinates(c1 + c2)
            notdef.numberOfContours = 2
            notdef.endPtsOfContours = [3, 7]
            notdef.flags = bytearray([1] * 8)
            notdef.coordinates = coords
            notdef.xMin = 50
            notdef.yMin = 0
            notdef.xMax = 450
            notdef.yMax = 700
            notdef.program = _g_l_y_f.ttProgram.Program()
            if 'hmtx' in font:
                font['hmtx']['.notdef'] = (500, 50)

def clean_font(ttf_path):
    print(f"Processing: {ttf_path}")
    font = TTFont(ttf_path)
    cmap = font.getBestCmap()
    if not cmap:
        print("  [SKIP] No cmap table found.")
        return

    # Check how many CJK codepoints
    cjk_cps = [cp for cp in cmap.keys() if is_cjk_muda(cp)]
    if not cjk_cps:
        print(f"  [OK] No CJK bloat detected ({len(cmap)} codepoints).")
        # Ensure nameID 9 and notdef anyway
        changed = False
        if 'name' in font:
            names = font['name']
            if not any(n.nameID == 9 for n in names.names):
                names.addMultilingualName({'en': 'Phil Gear'}, font, nameID=9)
                changed = True
        ensure_notdef_drawing(font)
        if changed:
            font.save(ttf_path)
        return

    print(f"  • Found {len(cjk_cps)} CJK/Hangul/Kana codepoints out of {len(cmap)} total.")
    keep_unicodes = [cp for cp in cmap.keys() if not is_cjk_muda(cp)]

    # Subset the font
    options = Options()
    options.set(passthrough_tables=True)
    subsetter = Subsetter(options=options)
    subsetter.populate(unicodes=keep_unicodes)
    subsetter.subset(font)

    # Ensure Designer nameID 9
    if 'name' in font:
        names = font['name']
        if not any(n.nameID == 9 for n in names.names):
            names.addMultilingualName({'en': 'Phil Gear'}, font, nameID=9)

    # Ensure .notdef drawing
    ensure_notdef_drawing(font)

    # Recalculate xAvgCharWidth
    if 'OS/2' in font and 'hmtx' in font:
        hmtx = font['hmtx']
        advances = [adv for adv, _ in hmtx.metrics.values() if adv > 0]
        if advances:
            font['OS/2'].xAvgCharWidth = int(round(sum(advances) / len(advances)))

    font.save(ttf_path)
    sz = os.path.getsize(ttf_path)
    print(f"  ✅ Saved cleaned font! Glyphs: {len(font.getGlyphOrder())}, Size: {sz:,} bytes")

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ttf_dir = os.path.join(root, 'fonts', 'ttf')
    
    # Fonts to clean (proportional cuts; Mono has 0 CJK)
    ttf_files = sorted(glob.glob(os.path.join(ttf_dir, 'PocketGull-*.ttf')))
    
    print(f"=== TPS MUDA ELIMINATION: Stripping CJK Bloat from {len(ttf_files)} fonts ===")
    for path in ttf_files:
        # Don't touch VF yet, it will be recompiled from masters
        if 'PocketGull-VF' in path:
            continue
        clean_font(path)
    print("=== MUDA ELIMINATION COMPLETE ===")

if __name__ == '__main__':
    main()
