"""
PocketGull Font Audit Script v3
Accesses hmtx.metrics dict directly to avoid __contains__ KeyError bug.
"""
import os
from fontTools.ttLib import TTFont

FONT_DIR = r'c:\Users\philg\Pocketgull\pocketgull-typeface'

def audit_font(path):
    basename = os.path.basename(path)
    size_kb = os.path.getsize(path) / 1024
    print(f"\n{'='*70}")
    print(f"FONT: {basename}  ({size_kb:.1f} KB)")
    print(f"{'='*70}")

    font = TTFont(path)

    # 1. Name table
    if 'name' in font:
        for record in font['name'].names:
            if record.nameID in (0, 1, 2, 4, 5, 6):
                try:
                    val = record.toUnicode()
                except:
                    val = str(record.string)
                labels = {0:'Copyright', 1:'Family', 2:'Subfamily', 4:'Full Name', 5:'Version', 6:'PostScript'}
                print(f"  name[{record.nameID}] {labels.get(record.nameID,'')}: {val}")

    # 2. Head table
    if 'head' in font:
        h = font['head']
        print(f"\n  head.unitsPerEm: {h.unitsPerEm}")

    # 3. Glyph inventory
    glyph_order = font.getGlyphOrder()
    print(f"  Total glyphs: {len(glyph_order)}")

    # 4. cmap
    cmap = font.getBestCmap()
    if cmap:
        print(f"  cmap entries: {len(cmap)}")

    # 5. Get hmtx metrics dict safely
    metrics = {}
    if 'hmtx' in font:
        metrics = font['hmtx'].metrics  # direct dict access

    # 6. Contour audit
    pocketgull_chars = ['P', 'o', 'c', 'k', 'e', 't', 'g', 'u', 'l']
    sample_chars = ['.notdef', 'space', 'A', 'B', 'C', 'a', 'b', 'zero', 'one',
                    'exclam', 'period', 'ntilde', 'eacute']
    show_chars = set(pocketgull_chars + sample_chars)

    if 'glyf' in font:
        glyf = font['glyf']
        empty_count = 0
        real_count = 0
        all_aws = {}

        print(f"\n  --- Master Glyphs (P-o-c-k-e-t-g-u-l) ---")
        for name in glyph_order:
            if not isinstance(name, str):
                continue
            try:
                g = glyf[name]
            except Exception:
                continue

            nc = g.numberOfContours if hasattr(g, 'numberOfContours') else 0
            aw = metrics[name][0] if name in metrics else '?'
            lsb = metrics[name][1] if name in metrics else '?'
            all_aws[name] = aw

            if nc == 0:
                empty_count += 1
                if name in pocketgull_chars:
                    print(f"    {name:20s}  aw={str(aw):>5s}  ** EMPTY (0 contours) **")
                continue

            real_count += 1

            if nc == -1:
                comp_count = len(g.components) if hasattr(g, 'components') else 0
                detail = f"COMPOSITE ({comp_count} components)"
                bbox_str = "n/a"
            else:
                npts = len(g.coordinates) if hasattr(g, 'coordinates') and g.coordinates else 0
                bbox_str = f"({g.xMin},{g.yMin})-({g.xMax},{g.yMax})" if hasattr(g, 'xMin') and g.xMin is not None else "n/a"
                detail = f"{nc} contours, {npts} pts"

            if name in pocketgull_chars:
                print(f"    {name:20s}  aw={str(aw):>5s}  lsb={str(lsb):>5s}  {bbox_str:30s}  {detail}")

        print(f"\n  --- Sample Other Glyphs ---")
        for name in glyph_order:
            if not isinstance(name, str) or name in pocketgull_chars:
                continue
            if name not in show_chars:
                continue
            try:
                g = glyf[name]
            except:
                continue
            nc = g.numberOfContours if hasattr(g, 'numberOfContours') else 0
            aw = metrics[name][0] if name in metrics else '?'
            lsb = metrics[name][1] if name in metrics else '?'
            if nc == 0:
                print(f"    {name:20s}  aw={str(aw):>5s}  EMPTY")
            elif nc == -1:
                comp_count = len(g.components) if hasattr(g, 'components') else 0
                print(f"    {name:20s}  aw={str(aw):>5s}  COMPOSITE ({comp_count} components)")
            else:
                npts = len(g.coordinates) if hasattr(g, 'coordinates') and g.coordinates else 0
                bbox_str = f"({g.xMin},{g.yMin})-({g.xMax},{g.yMax})" if hasattr(g, 'xMin') and g.xMin is not None else "n/a"
                print(f"    {name:20s}  aw={str(aw):>5s}  {nc} contours, {npts} pts  {bbox_str}")

        print(f"\n  Summary: {real_count} with contours, {empty_count} empty")

        # Advance width analysis
        int_aws = {k: v for k, v in all_aws.items() if isinstance(v, int) and v > 0}
        if int_aws:
            vals = sorted(set(int_aws.values()))
            print(f"  Advance width range: {min(vals)} - {max(vals)} ({len(vals)} unique)")
            # Show master glyph widths vs rest
            master_aws = {ch: int_aws.get(ch, '?') for ch in pocketgull_chars}
            print(f"  Master glyph widths: {master_aws}")

    # 7. Layout features
    if 'GSUB' in font:
        gsub = font['GSUB'].table
        features = set()
        if gsub.FeatureList:
            for fr in gsub.FeatureList.FeatureRecord:
                features.add(fr.FeatureTag)
        print(f"\n  GSUB features: {', '.join(sorted(features)) if features else 'NONE'}")
    else:
        print(f"\n  GSUB: NOT PRESENT (no ligatures/calt/dlig)")

    if 'kern' in font:
        pair_count = 0
        for subtable in font['kern'].kernTables:
            if hasattr(subtable, 'kernTable'):
                pair_count += len(subtable.kernTable)
        print(f"  kern: {pair_count} pairs")
    else:
        print(f"  kern: NOT PRESENT")

    font.close()


ttf_files = sorted([f for f in os.listdir(FONT_DIR) if f.endswith('.ttf')])
print(f"Found {len(ttf_files)} .ttf files in {FONT_DIR}\n")

# Only audit the two that matter most
for f in ['PocketGull-Bold.ttf', 'PocketGull-Antigravity.ttf']:
    full = os.path.join(FONT_DIR, f)
    if os.path.exists(full):
        try:
            audit_font(full)
        except Exception as e:
            import traceback
            print(f"\nERROR auditing {f}:")
            traceback.print_exc()

print(f"\n{'='*70}")
print("AUDIT COMPLETE")
print(f"{'='*70}")
