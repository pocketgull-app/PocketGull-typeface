#!/usr/bin/env python3
"""
Inspect the exact Unicode character mapping (cmap) table of PocketGull font binaries.
"""

import os
import unicodedata
from fontTools.ttLib import TTFont

def audit_cmap():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    font_path = os.path.join(typeface_root, 'PocketGull-Bold.ttf')

    font = TTFont(font_path)
    cmap = font.getBestCmap()
    
    print("=" * 60)
    print("POCKETGULL FONT UNICODE CMAP AUDIT")
    print("=" * 60)
    print(f"Font Binary: {font_path}")
    print(f"Total Active Unicode Code Points in Binary: {len(cmap)}\n")

    blocks = {}
    sample_glyphs_by_block = {}

    for cp in sorted(cmap.keys()):
        char = chr(cp)
        try:
            name = unicodedata.name(char)
        except Exception:
            name = 'UNKNOWN'

        if cp < 0x0080:
            b = 'Basic Latin (ASCII)'
        elif cp < 0x0100:
            b = 'Latin-1 Supplement (Accents & Symbols)'
        elif cp < 0x0180:
            b = 'Latin Extended-A'
        elif cp < 0x0250:
            b = 'Latin Extended-B'
        elif cp < 0x0370:
            b = 'IPA / Spacing Modifiers'
        elif cp < 0x0400:
            b = 'Greek & Coptic (α, β, Ω, etc.)'
        elif cp < 0x0500:
            b = 'Cyrillic (Pan-Slavic)'
        elif cp < 0x0600:
            b = 'Hebrew'
        elif cp < 0x0700:
            b = 'Arabic'
        elif cp < 0x0A00:
            b = 'Devanagari (Indic)'
        elif cp < 0x2100:
            b = 'General Punctuation & Currency'
        elif cp < 0x2200:
            b = 'Letterlike / Apothecary Symbols'
        elif cp < 0x2300:
            b = 'Mathematical Operators'
        else:
            b = 'Miscellaneous Symbols & Private Use'

        blocks[b] = blocks.get(b, 0) + 1
        if b not in sample_glyphs_by_block:
            sample_glyphs_by_block[b] = []
        if len(sample_glyphs_by_block[b]) < 8:
            sample_glyphs_by_block[b].append(f"'{char}' (U+{cp:04X})")

    for b, count in sorted(blocks.items()):
        print(f"  • {b}: {count} characters")
        print(f"    Samples: {', '.join(sample_glyphs_by_block[b])}")

    print("\n" + "=" * 60)

if __name__ == '__main__':
    audit_cmap()
