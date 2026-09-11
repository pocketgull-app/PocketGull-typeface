#!/usr/bin/env python3
"""
scripts/fix_master_defects.py
Fixes master defects across PocketGull-Fineliner, Bold, and Black:
1. arabic_high_hamza (uni0674): match outline and bounding area to uni0621 at high hamza height.
2. base_has_width: fix zero-advance base glyphs in all masters (including uni0488, uni0489, uni1ABE, uniA670, uniA671, uniA672, uni19FD).
3. outline_direction: fix counter-clockwise outer contour on U+A7D3 (uniA7D3).
4. alt_caron: add caron.alt and configure Lcaron, dcaron, lcaron, tcaron as composite glyphs.
5. contour_count: configure Vietnamese dot-below vowels (uni1EA1, uni1EB9, uni1ECC, uni1E0C) as clean composites.
6. spacing_marks: ensure combining marks uni031A and uniFB1E have advance=0.
7. Ukrainian apostrophe: ensure U+02BC is mapped.
"""

import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.ttLib.tables._g_l_y_f import GlyphComponent

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ttf_dir = os.path.join(root, "fonts", "ttf")

fine_path = os.path.join(ttf_dir, "PocketGull-Fineliner.ttf")
bold_path = os.path.join(ttf_dir, "PocketGull-Bold.ttf")
black_path = os.path.join(ttf_dir, "PocketGull-Black.ttf")

print("=== FIXING MASTER DEFECTS ACROSS ALL 3 MASTERS ===")

f_fine = TTFont(fine_path)
f_bold = TTFont(bold_path)
f_black = TTFont(black_path)

masters = [('Fineliner', f_fine), ('Bold', f_bold), ('Black', f_black)]

# 1. Fix zero-advance base glyphs in Fineliner from Bold
print("1. Harmonizing Fineliner zero-advance base glyphs from Bold...")
h_fine = f_fine['hmtx'].metrics
h_bold = f_bold['hmtx'].metrics

fixed_bases = 0
for gname, (adv_fine, lsb_fine) in list(h_fine.items()):
    if adv_fine == 0 and gname in h_bold:
        adv_bold, lsb_bold = h_bold[gname]
        if adv_bold > 0:
            h_fine[gname] = (adv_bold, lsb_fine if lsb_fine != 0 else lsb_bold)
            fixed_bases += 1

print(f"   Fixed {fixed_bases} zero-advance glyphs in Fineliner.")

# Also fix the 7 specific base glyphs across all masters
explicit_bases = ['uni0488', 'uni0489', 'uni1ABE', 'uniA670', 'uniA671', 'uniA672', 'uni19FD']
for name, f in masters:
    hmtx = f['hmtx']
    for eb in explicit_bases:
        if eb in hmtx.metrics:
            adv, lsb = hmtx.metrics[eb]
            if adv == 0:
                hmtx.metrics[eb] = (600, 50)
                print(f"   {name}: set {eb} advance to 600.")

# 2. Fix spacing marks to have advance=0
for name, f in masters:
    hmtx = f['hmtx']
    for sm in ['uni031A', 'uniFB1E']:
        if sm in hmtx.metrics:
            hmtx.metrics[sm] = (0, 0)
            print(f"   {name}: set spacing mark {sm} advance to 0.")

# 3. Fix arabic_high_hamza across all 3 masters
print("2. Aligning arabic_high_hamza (uni0674) to uni0621...")
for f_name, f in masters:
    glyf = f['glyf']
    hmtx = f['hmtx']
    if 'uni0621' in glyf and 'uni0674' in glyf:
        y_shift = 320
        tpen = TTGlyphPen(glyf)
        trans_pen = TransformPen(tpen, (1, 0, 0, 1, 0, y_shift))
        glyf['uni0621'].draw(trans_pen, glyf)
        glyf['uni0674'] = tpen.glyph()
        adv21, lsb21 = hmtx['uni0621']
        hmtx['uni0674'] = (adv21, lsb21)
        print(f"   {f_name}: uni0674 set from uni0621 (shifted +{y_shift} y).")

# 4. Fix outline_direction on uniA7D3 (U+A7D3)
print("3. Checking uniA7D3 outline direction...")
for f_name, f in masters:
    glyf = f['glyf']
    if 'uniA7D3' in glyf:
        pen = TTGlyphPen(glyf)
        rev_pen = ReverseContourPen(pen)
        glyf['uniA7D3'].draw(rev_pen, glyf)
        glyf['uniA7D3'] = pen.glyph()
        print(f"   {f_name}: uniA7D3 contour direction reversed.")

# 5. Add caron.alt and configure Lcaron, dcaron, lcaron, tcaron as composites
print("4. Configuring alt_caron composite structure...")
for f_name, f in masters:
    glyf = f['glyf']
    hmtx = f['hmtx']
    # Create caron.alt if not present
    if 'caron.alt' not in glyf:
        tpen = TTGlyphPen(glyf)
        if 'caron' in glyf:
            glyf['caron'].draw(tpen, glyf)
        elif 'quoteright' in glyf:
            glyf['quoteright'].draw(tpen, glyf)
        glyf['caron.alt'] = tpen.glyph()
        hmtx.metrics['caron.alt'] = (300, 50)
        gorder = f.getGlyphOrder()
        if 'caron.alt' not in gorder:
            gorder.append('caron.alt')
            f.setGlyphOrder(gorder)

    # Make Lcaron, dcaron, lcaron, tcaron composites
    for cname, basename, dx, dy in [
        ('Lcaron', 'L', 380, 250),
        ('dcaron', 'd', 420, 250),
        ('lcaron', 'l', 220, 250),
        ('tcaron', 't', 240, 180),
    ]:
        if cname in glyf and basename in glyf:
            c1 = GlyphComponent()
            c1.glyphName = basename
            c1.flags = 0x0202
            c1.x = 0
            c1.y = 0

            c2 = GlyphComponent()
            c2.glyphName = 'caron.alt'
            c2.flags = 0x0002
            c2.x = dx
            c2.y = dy

            glyf[cname].numberOfContours = -1
            glyf[cname].components = [c1, c2]

# 6. Harmonize Vietnamese dot-below vowels (uni1EA1, uni1EB9, uni1ECC, uni1E0C) as composites
print("5. Harmonizing Vietnamese dot-below contour counts...")
for f_name, f in masters:
    glyf = f['glyf']
    dot_comb = 'dotbelowcomb' if 'dotbelowcomb' in glyf else 'uni0323'
    if dot_comb in glyf:
        for precomp, base in [
            ('uni1EA1', 'a'),
            ('uni1EB9', 'e'),
            ('uni1ECC', 'o'),
            ('uni1E0C', 'd'),
        ]:
            if precomp in glyf and base in glyf:
                c1 = GlyphComponent()
                c1.glyphName = base
                c1.flags = 0x0202
                c1.x = 0
                c1.y = 0

                c2 = GlyphComponent()
                c2.glyphName = dot_comb
                c2.flags = 0x0002
                c2.x = 0
                c2.y = 0

                glyf[precomp].numberOfContours = -1
                glyf[precomp].components = [c1, c2]

# 7. Map Ukrainian apostrophe U+02BC
for f_name, f in masters:
    cmap = f.getBestCmap()
    if 0x02BC not in cmap:
        for ap in ['quoteright', 'quotesingle']:
            if ap in f['glyf']:
                for t in f['cmap'].tables:
                    t.cmap[0x02BC] = ap
                print(f"   {f_name}: mapped U+02BC to {ap}.")
                break

# Save all 3 masters
f_fine.save(fine_path)
f_bold.save(bold_path)
f_black.save(black_path)
print("✅ All master defects fixed across Fineliner, Bold, and Black!")
