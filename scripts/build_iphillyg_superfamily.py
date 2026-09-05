"""
PocketGull Typefoundry: iPhillyG & Connected Fl Ligature Compiler
==================================================================
Synthesizes:
1. 'i.phillyg': Lowercase i with the optical heart-shaped tittle.
2. 'F_l': Connected display ligature for "Flight Sanctuary".
3. 'f_l': Connected standard ligature for "fl".
4. 'uni2665': Native Unicode heart glyph mapped to U+2665 and U+2764.
5. OpenType GSUB tables:
   - 'cv12' (Feature: The iPhillyG Heart Tittle) -> i -> i.phillyg
   - 'ss03' (Stylistic Set 3: iPhillyG Alternate) -> i -> i.phillyg
   - 'dlig' (Discretionary Ligatures) -> F + l -> F_l
   - 'liga' (Standard Ligatures) -> f + l -> f_l
   - Preserves ISMP features: cv08, cv05, ss02, zero.
"""

import os
import sys
import brotli
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables import otTables as ot

def create_heart_tittle_contour(cx=150, base_y=590, width=190, height=175):
    """
    Creates a clockwise quadratic Bézier heart contour centered at (cx)
    with bottom cusp at base_y and top lobes peaking at base_y + height.
    """
    half_w = width / 2.0
    top_y = base_y + height
    cleft_y = base_y + height * 0.60
    mid_y = base_y + height * 0.50

    pts = [
        (int(cx), int(base_y)),
        (int(cx + half_w * 0.95), int(base_y + height * 0.15)),
        (int(cx + half_w), int(mid_y)),
        (int(cx + half_w), int(top_y - 10)),
        (int(cx + half_w * 0.55), int(top_y)),
        (int(cx + half_w * 0.15), int(top_y)),
        (int(cx), int(cleft_y)),
        (int(cx - half_w * 0.15), int(top_y)),
        (int(cx - half_w * 0.55), int(top_y)),
        (int(cx - half_w), int(top_y - 10)),
        (int(cx - half_w), int(mid_y)),
        (int(cx - half_w * 0.95), int(base_y + height * 0.15)),
    ]
    flags = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    return pts, flags

def create_standalone_heart_glyph(advance=700, width=540, height=520, base_y=90):
    cx = advance / 2.0
    pts, flags = create_heart_tittle_contour(cx=cx, base_y=base_y, width=width, height=height)
    g = Glyph()
    g.numberOfContours = 1
    g.endPtsOfContours = [len(pts) - 1]
    g.coordinates = GlyphCoordinates(pts)
    g.flags = bytearray(flags)
    g.program = b''
    return g

def build_iphillyg_glyph(font):
    orig_i = font['glyf']['i']
    stem_end = orig_i.endPtsOfContours[0]
    stem_pts = [orig_i.coordinates[p] for p in range(stem_end + 1)]
    stem_flags = [orig_i.flags[p] & 0x3F for p in range(stem_end + 1)]

    min_x = min(p[0] for p in stem_pts)
    max_x = max(p[0] for p in stem_pts)
    cx = (min_x + max_x) / 2.0
    stem_width = max_x - min_x

    heart_w = max(170, int(stem_width * 1.25))
    heart_h = int(heart_w * 0.92)
    base_y = 590

    heart_pts, heart_flags = create_heart_tittle_contour(cx=cx, base_y=base_y, width=heart_w, height=heart_h)

    all_pts = stem_pts + heart_pts
    all_flags = stem_flags + [f & 0x3F for f in heart_flags]

    g = Glyph()
    g.numberOfContours = 2
    g.endPtsOfContours = [stem_end, len(all_pts) - 1]
    g.coordinates = GlyphCoordinates(all_pts)
    g.flags = bytearray(all_flags)
    g.program = b''
    return g

def build_fl_connected_glyph(font):
    f_glyf = font['glyf']['F']
    l_glyf = font['glyf']['l']
    f_adv, f_lsb = font['hmtx']['F']
    l_adv, l_lsb = font['hmtx']['l']

    f_pts = [f_glyf.coordinates[p] for p in range(len(f_glyf.coordinates))]
    f_min_x = min(p[0] for p in f_pts)
    f_max_x = max(p[0] for p in f_pts)
    
    l_pts = [l_glyf.coordinates[p] for p in range(len(l_glyf.coordinates))]
    l_width = max(p[0] for p in l_pts) - min(p[0] for p in l_pts)
    l_top_y = max(p[1] for p in l_pts)

    l_stem_left = f_max_x - 19
    l_stem_right = l_stem_left + l_width

    arm_top_y = f_pts[2][1]
    arm_bot_y = f_pts[4][1]

    stem_left = f_pts[1][0]
    stem_right = f_pts[0][0]

    mid_top_y = f_pts[6][1]
    mid_bot_y = f_pts[8][1]
    mid_right = f_pts[7][0]

    poly = [
        (stem_left, 0),
        (stem_left, arm_top_y),
        (l_stem_left, arm_top_y),
        (l_stem_left, l_top_y),
        (l_stem_right, l_top_y),
        (l_stem_right, 0),
        (l_stem_left, 0),
        (l_stem_left, arm_bot_y),
        (stem_right, arm_bot_y),
        (stem_right, mid_top_y),
        (mid_right, mid_top_y),
        (mid_right, mid_bot_y),
        (stem_right, mid_bot_y),
        (stem_right, 0),
    ]

    flags = [1 & 0x3F] * len(poly)

    g = Glyph()
    g.numberOfContours = 1
    g.endPtsOfContours = [len(poly) - 1]
    g.coordinates = GlyphCoordinates(poly)
    g.flags = bytearray(flags)
    g.program = b''
    advance = l_stem_right + l_lsb
    return g, advance, stem_left

def build_fl_lowercase_glyph(font):
    f_glyf = font['glyf']['f']
    l_glyf = font['glyf']['l']
    f_adv, f_lsb = font['hmtx']['f']
    l_adv, l_lsb = font['hmtx']['l']

    f_pts = [f_glyf.coordinates[p] for p in range(len(f_glyf.coordinates))]
    f_flags = [f_glyf.flags[p] & 0x3F for p in range(len(f_glyf.coordinates))]

    l_pts = [l_glyf.coordinates[p] for p in range(len(l_glyf.coordinates))]
    l_flags = [l_glyf.flags[p] & 0x3F for p in range(len(l_glyf.coordinates))]

    f_max_x = max(p[0] for p in f_pts)
    shift_x = f_max_x - 30

    shifted_l_pts = [(p[0] + shift_x, p[1]) for p in l_pts]

    all_pts = f_pts + shifted_l_pts
    all_flags = f_flags + l_flags

    g = Glyph()
    g.numberOfContours = 2
    g.endPtsOfContours = [len(f_pts) - 1, len(all_pts) - 1]
    g.coordinates = GlyphCoordinates(all_pts)
    g.flags = bytearray(all_flags)
    g.program = b''
    advance = shift_x + max(p[0] for p in l_pts) + l_lsb
    return g, advance, f_lsb

def inject_glyphs_and_features(font_path):
    print(f"\n--- Processing: {font_path} ---")
    font = TTFont(font_path)
    glyf = font['glyf']
    hmtx = font['hmtx']

    # 1. Build and inject 'i.phillyg'
    g_iphillyg = build_iphillyg_glyph(font)
    glyf['i.phillyg'] = g_iphillyg
    i_adv, i_lsb = hmtx['i']
    hmtx['i.phillyg'] = (i_adv, i_lsb)
    print("  + Injected 'i.phillyg' (i with heart tittle)")

    # 2. Build and inject 'F_l' connected ligature
    g_fl_cap, fl_cap_adv, fl_cap_lsb = build_fl_connected_glyph(font)
    glyf['F_l'] = g_fl_cap
    hmtx['F_l'] = (fl_cap_adv, fl_cap_lsb)
    print(f"  + Injected 'F_l' connected ligature (adv={fl_cap_adv})")

    # 3. Build and inject 'f_l' lowercase ligature
    g_fl_low, fl_low_adv, fl_low_lsb = build_fl_lowercase_glyph(font)
    glyf['f_l'] = g_fl_low
    hmtx['f_l'] = (fl_low_adv, fl_low_lsb)
    print(f"  + Injected 'f_l' standard ligature (adv={fl_low_adv})")

    # 4. Build and inject 'uni2665' (Unicode Heart)
    g_heart = create_standalone_heart_glyph(advance=700)
    glyf['uni2665'] = g_heart
    hmtx['uni2665'] = (700, 80)
    
    for table in font['cmap'].tables:
        if table.isUnicode():
            table.cmap[0x2665] = 'uni2665'
            table.cmap[0x2764] = 'uni2665'
    print("  + Injected 'uni2665' and mapped to U+2665 & U+2764 in cmap")

    # 5. Wire GSUB tables (cv12, ss03, dlig, liga)
    if 'GSUB' not in font:
        print("  ! GSUB not found, skipping feature injection")
    else:
        gsub = font['GSUB'].table

        # Single Substitution: i -> i.phillyg
        sub_iphillyg = ot.SingleSubst()
        sub_iphillyg.mapping = {'i': 'i.phillyg'}

        lookup_iphillyg = ot.Lookup()
        lookup_iphillyg.LookupType = 1
        lookup_iphillyg.LookupFlag = 0
        lookup_iphillyg.SubTable = [sub_iphillyg]
        lookup_iphillyg_idx = len(gsub.LookupList.Lookup)
        gsub.LookupList.Lookup.append(lookup_iphillyg)

        # Ligature Substitution: F + l -> F_l (dlig)
        lig_Fl = ot.Ligature()
        lig_Fl.LigGlyph = 'F_l'
        lig_Fl.Component = ['l']

        lig_sub_dlig = ot.LigatureSubst()
        lig_sub_dlig.ligatures = {'F': [lig_Fl]}

        lookup_dlig = ot.Lookup()
        lookup_dlig.LookupType = 4
        lookup_dlig.LookupFlag = 0
        lookup_dlig.SubTable = [lig_sub_dlig]
        lookup_dlig_idx = len(gsub.LookupList.Lookup)
        gsub.LookupList.Lookup.append(lookup_dlig)

        # Ligature Substitution: f + l -> f_l (liga)
        lig_fl = ot.Ligature()
        lig_fl.LigGlyph = 'f_l'
        lig_fl.Component = ['l']

        lig_sub_liga = ot.LigatureSubst()
        lig_sub_liga.ligatures = {'f': [lig_fl]}

        lookup_liga = ot.Lookup()
        lookup_liga.LookupType = 4
        lookup_liga.LookupFlag = 0
        lookup_liga.SubTable = [lig_sub_liga]
        lookup_liga_idx = len(gsub.LookupList.Lookup)
        gsub.LookupList.Lookup.append(lookup_liga)

        features_to_add = [
            ('cv12', [lookup_iphillyg_idx]),
            ('ss03', [lookup_iphillyg_idx]),
            ('dlig', [lookup_dlig_idx]),
            ('liga', [lookup_liga_idx]),
        ]

        for tag, lookup_indices in features_to_add:
            feat_rec = ot.FeatureRecord()
            feat_rec.FeatureTag = tag
            feat_rec.Feature = ot.Feature()
            feat_rec.Feature.LookupListIndex = lookup_indices
            feat_rec.Feature.LookupCount = len(lookup_indices)
            gsub.FeatureList.FeatureRecord.append(feat_rec)
            f_idx = len(gsub.FeatureList.FeatureRecord) - 1

            for script_rec in gsub.ScriptList.ScriptRecord:
                s = script_rec.Script
                if s.DefaultLangSys:
                    if f_idx not in s.DefaultLangSys.FeatureIndex:
                        s.DefaultLangSys.FeatureIndex.append(f_idx)
                for lang_rec in s.LangSysRecord:
                    if f_idx not in lang_rec.LangSys.FeatureIndex:
                        lang_rec.LangSys.FeatureIndex.append(f_idx)
            print(f"  + Registered GSUB feature '{tag}' with lookup {lookup_indices}")

    font.save(font_path)
    print(f"  [SAVED] {font_path}")

    woff2_path = font_path.replace('/ttf/', '/woff2/').replace('\\ttf\\', '\\woff2\\').replace('.ttf', '.woff2')
    with open(font_path, 'rb') as f:
        ttf_bytes = f.read()
    compressed = brotli.compress(ttf_bytes, quality=11)
    with open(woff2_path, 'wb') as f:
        f.write(compressed)
    print(f"  [WOFF2] Wrote {woff2_path} ({len(compressed)} bytes, Brotli Q11)")

def main():
    target_fonts = [
        'fonts/ttf/PocketGull-Bold.ttf',
        'fonts/ttf/PocketGull-Fineliner.ttf',
        'fonts/ttf/PocketGull-Chiseltip.ttf',
    ]
    for font_path in target_fonts:
        if os.path.exists(font_path):
            inject_glyphs_and_features(font_path)

if __name__ == '__main__':
    main()
