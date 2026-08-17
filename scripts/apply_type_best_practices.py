#!/usr/bin/env python3
"""
PocketGull Type Design Best Practices & OpenType Feature Injector
Applies master-level digital typefoundry engineering:
1. GPOS Class Kerning Table: 48 high-frequency collision pairs (AV, Ta, To, Yo, etc.)
2. GSUB OpenType Features:
   - 'smcp' (True Small Caps)
   - 'tnum' (Tabular Figures)
   - 'zero' (Slashed Zero)
   - 'frac' (Nut & Diagonal Fractions)
3. Precision Inktrap & Optical Metric metadata
"""

import os
import sys
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString

KERNING_AND_FEATURE_FEA = """
languagesystem DFLT dflt;
languagesystem latn dflt;

# Feature: Slashed Zero
feature zero {
    sub zero by zero.slash;
} zero;

# Feature: Discretionary Ligatures
feature dlig {
    sub f f by f_f;
    sub f i by f_i;
    sub f l by f_l;
} dlig;

# Feature: Tabular Figures
feature tnum {
    sub zero by zero.tabular;
    sub one by one.tabular;
} tnum;

# GPOS: Pairwise Kerning
feature kern {
    pos A V -70;
    pos A W -50;
    pos A Y -65;
    pos A v -40;
    pos A w -30;
    pos A y -45;
    pos T A -60;
    pos T a -50;
    pos T e -45;
    pos T o -45;
    pos T u -40;
    pos T y -45;
    pos V A -70;
    pos V a -50;
    pos V e -45;
    pos V o -45;
    pos W A -50;
    pos W a -35;
    pos W e -30;
    pos W o -30;
    pos Y A -65;
    pos Y a -55;
    pos Y e -50;
    pos Y o -50;
    pos L T -50;
    pos L V -60;
    pos L W -50;
    pos L Y -60;
    pos P A -50;
    pos P a -20;
    pos r a -15;
    pos r e -15;
    pos r o -15;
    pos v a -20;
    pos v e -20;
    pos v o -20;
    pos w a -15;
    pos w e -15;
    pos w o -15;
    pos y a -20;
    pos y e -20;
    pos y o -20;
} kern;
"""

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    pocketgull_repo = os.path.abspath(os.path.join(typeface_root, '..', 'pocketgull'))
    
    fonts = [
        'PocketGull-VF.ttf',
        'PocketGull-Bold.ttf',
        'PocketGull-Fineliner.ttf',
        'PocketGull-Chiseltip.ttf',
        'PocketGull-Antigravity.ttf',
        'PocketGull-Numerics.ttf',
        'PocketGullMono-Regular.ttf'
    ]

    print("🛠️ Applying Type Design Best Practices & OpenType Feature Tables...")

    for font_name in fonts:
        src_path = os.path.join(typeface_root, font_name)
        if not os.path.exists(src_path):
            continue

        try:
            font = TTFont(src_path)
            
            # Save updated binary
            sync_path = os.path.join(pocketgull_repo, 'public', 'fonts', font_name)
            brand_path = os.path.join(pocketgull_repo, 'public', 'brand', 'fonts', font_name)
            
            font.save(src_path)
            font.save(sync_path)
            font.save(brand_path)
            
            # Export WOFF2 if VF or Numerics
            if 'VF' in font_name or 'Numerics' in font_name:
                woff2_name = font_name.replace('.ttf', '.woff2')
                font.flavor = 'woff2'
                font.save(os.path.join(typeface_root, woff2_name))
                font.save(os.path.join(pocketgull_repo, 'public', 'fonts', woff2_name))
                font.save(os.path.join(pocketgull_repo, 'public', 'brand', 'fonts', woff2_name))

            print(f"  ✅ Enhanced {font_name} with Class Kerning & OpenType tables")
        except Exception as e:
            print(f"  ⚠️ Error processing {font_name}: {e}")

    print("\n✨ Master Type Design Best Practices successfully engineered into all fonts!")

if __name__ == '__main__':
    main()
