"""
Task D: Inventory all non-master glyphs and categorize by replacement priority.
Outputs a structured report of which glyphs need original drawings.
"""
from fontTools.ttLib import TTFont

FONT_PATH = r'c:\Users\philg\Pocketgull\pocketgull-typeface\PocketGull-Bold.ttf'
MASTER_GLYPHS = {'P', 'o', 'c', 'k', 'e', 't', 'g', 'u', 'l', 'G'}

# Priority tiers for clinical typeface usage
TIER_1_CRITICAL = {
    'digits': list('0123456789'),
    'basic_punct': ['.', ',', ':', ';', '!', '?', '-', '(', ')', '/', "'"],
    'medical_units': ['%', '+', '=', '<', '>', '#', '@'],
}

TIER_2_BODY_TEXT = {
    'remaining_lowercase': [c for c in 'abcdfhijmnpqrsvwxyz'],
    'remaining_uppercase': [c for c in 'ABCDEFHIJKLMNOPQRSTUVWXYZ'],
}

TIER_3_EXTENDED = {
    'brackets': ['[', ']', '{', '}', '\\', '|', '~', '^', '_', '`'],
    'quotes': ['"'],
    'currency': ['$'],
    'math': ['*'],
}

font = TTFont(FONT_PATH)
glyph_order = [g for g in font.getGlyphOrder() if isinstance(g, str)]
cmap = font.getBestCmap()
metrics = font['hmtx'].metrics
glyf = font['glyf']

# Reverse cmap: glyph name -> unicode codepoints
name_to_cp = {}
if cmap:
    for cp, name in cmap.items():
        name_to_cp.setdefault(name, []).append(cp)

print("=" * 70)
print("POCKETGULL GLYPH REPLACEMENT ROADMAP")
print("=" * 70)
print(f"Total glyphs: {len(glyph_order)}")
print(f"Master (original SVG): {len(MASTER_GLYPHS)}")
print(f"Base (needs replacement): {len(glyph_order) - len(MASTER_GLYPHS)}")
print()

def print_tier(tier_name, groups):
    print(f"\n--- {tier_name} ---")
    total = 0
    for group_name, chars in groups.items():
        present = []
        missing = []
        for ch in chars:
            cp = ord(ch)
            if cp in cmap:
                gname = cmap[cp]
                if gname in MASTER_GLYPHS:
                    continue  # skip master glyphs
                aw = metrics[gname][0] if gname in metrics else '?'
                g = glyf[gname]
                nc = g.numberOfContours if hasattr(g, 'numberOfContours') else 0
                present.append(f"  '{ch}' (U+{cp:04X}) -> {gname:15s}  aw={str(aw):>5s}  contours={nc}")
            else:
                missing.append(f"  '{ch}' (U+{cp:04X}) -> NOT IN CMAP")
        
        if present or missing:
            print(f"\n  [{group_name}] ({len(present)} present, {len(missing)} missing)")
            for line in present:
                print(line)
            for line in missing:
                print(line)
            total += len(present) + len(missing)
    return total

t1 = print_tier("TIER 1: CRITICAL (clinical readouts, vitals, dosages)", TIER_1_CRITICAL)
t2 = print_tier("TIER 2: BODY TEXT (remaining alphabet)", TIER_2_BODY_TEXT)
t3 = print_tier("TIER 3: EXTENDED (brackets, currency, math)", TIER_3_EXTENDED)

# Diacritics
print(f"\n--- TIER 4: DIACRITICS (composite glyphs) ---")
diacritics = []
for gname in glyph_order:
    if gname in MASTER_GLYPHS or gname in ('.notdef', 'space', 'NULL', 'CR'):
        continue
    g = glyf[gname]
    if hasattr(g, 'numberOfContours') and g.numberOfContours == -1:
        if hasattr(g, 'components'):
            comp_names = [c.glyphName for c in g.components]
            cps = name_to_cp.get(gname, [])
            cp_str = ', '.join(f'U+{c:04X}' for c in cps) if cps else 'no cmap'
            diacritics.append(f"  {gname:20s}  ({cp_str})  components: {', '.join(comp_names)}")

print(f"  {len(diacritics)} composite diacritics (inherit from base glyphs)")
for line in diacritics[:15]:
    print(line)
if len(diacritics) > 15:
    print(f"  ... and {len(diacritics) - 15} more")

print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")
print(f"  Tier 1 (Critical):  {t1} glyphs  <- DO FIRST")
print(f"  Tier 2 (Body Text): {t2} glyphs  <- visual consistency")
print(f"  Tier 3 (Extended):  {t3} glyphs")
print(f"  Tier 4 (Diacritics): {len(diacritics)} composite glyphs (auto-update when base glyphs change)")
print(f"\n  Total needing original drawings: ~{t1 + t2 + t3}")
print(f"  Diacritics auto-inherit: {len(diacritics)}")

font.close()
