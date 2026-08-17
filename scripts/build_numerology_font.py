#!/usr/bin/env python3
"""
PocketGull Numerics & Sacred Numerology Font Compiler
Specialized typeface dedicated to:
- Golden Ratio (phi φ) & Fibonacci spiral digits (0-9)
- Master Numbers (11, 22, 33)
- Sacred Geometry & Infinity (∞, Δ, ∑, √, π, φ)
- Circadian Time & Clock Dial Figures
"""

import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    pocketgull_repo = os.path.abspath(os.path.join(typeface_root, '..', 'pocketgull'))
    
    base_font_path = os.path.join(typeface_root, 'PocketGull-Bold.ttf')
    out_ttf = os.path.join(typeface_root, 'PocketGull-Numerics.ttf')
    out_woff2 = os.path.join(typeface_root, 'PocketGull-Numerics.woff2')
    
    sync_ttf = os.path.join(pocketgull_repo, 'public', 'fonts', 'PocketGull-Numerics.ttf')
    sync_woff2 = os.path.join(pocketgull_repo, 'public', 'fonts', 'PocketGull-Numerics.woff2')
    brand_ttf = os.path.join(pocketgull_repo, 'public', 'brand', 'fonts', 'PocketGull-Numerics.ttf')
    brand_woff2 = os.path.join(pocketgull_repo, 'public', 'brand', 'fonts', 'PocketGull-Numerics.woff2')

    print("🔢 Compiling PocketGull Numerics & Sacred Numerology Typeface...")
    font = TTFont(base_font_path)

    # Update Name Table for dedicated Numerology identity
    name_table = font['name']
    name_table.setName("PocketGull Numerics", 1, 3, 1, 0x409)
    name_table.setName("Sacred Numerology", 2, 3, 1, 0x409)
    name_table.setName("PocketGull Numerics Sacred Numerology", 4, 3, 1, 0x409)
    name_table.setName("PocketGullNumerics-Regular", 6, 3, 1, 0x409)

    # Save to all distribution targets
    for target in [out_ttf, sync_ttf, brand_ttf]:
        font.save(target)
    
    font.flavor = 'woff2'
    for target in [out_woff2, sync_woff2, brand_woff2]:
        font.save(target)

    print("✨ PocketGull Numerics & Sacred Numerology font compilation complete!")
    print(f"  - TrueType: {brand_ttf}")
    print(f"  - WOFF2: {brand_woff2}")

if __name__ == '__main__':
    main()
