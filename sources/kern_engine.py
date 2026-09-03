"""
PocketGull Kerning Engine — GPOS via feaLib (fontTools 4.x)

Generates a .fea kern feature string and compiles it into all 5 font variants
using fontTools.feaLib.builder.addOpenTypeFeatures.

References:
  - Lupton: "The details of kerning ... are fundamental to readability."
  - Caslon (Cottrell): optical tracking, sidebearing calibration
  - Clinical priority pairs: BP, HR, SpO2, Rx, %, /, #, dosage numerals

Run:
    python scripts/kern_engine.py
"""

import shutil
import sys
from pathlib import Path

try:
    from fontTools.ttLib import TTFont
    from fontTools.feaLib.builder import addOpenTypeFeatures
    from fontTools.feaLib import ast as feaAst
except ImportError as e:
    sys.exit(f"fontTools not available: {e}")


# ─────────────────────────────────────────────────────────────
# Kern Pair Definitions
# (left_glyph_ps_name, right_glyph_ps_name, kern_upm)
# Negative = tighter, Positive = looser (1024 UPM)
# ─────────────────────────────────────────────────────────────
KERN_PAIRS: list[tuple[str, str, int]] = [
    # ── Caps + lowercase opticals ────────────────────────────
    ("T", "o",   -60), ("T", "a",   -60), ("T", "e",   -60),
    ("T", "u",   -60), ("T", "i",   -45), ("T", "r",   -55),
    ("T", "y",   -55), ("T", "comma", -70), ("T", "period", -70),
    ("T", "colon", -60),

    ("A", "V",   -75), ("A", "W",   -65), ("A", "T",   -60),
    ("A", "v",   -60), ("A", "w",   -55), ("A", "y",   -55),

    ("V", "A",   -75), ("V", "o",   -55), ("V", "a",   -60),
    ("V", "e",   -55), ("V", "u",   -50),
    ("V", "comma", -75), ("V", "period", -75),

    ("W", "A",   -65), ("W", "o",   -45), ("W", "a",   -50),
    ("W", "e",   -45),

    ("P", "A",   -80), ("P", "a",   -65),
    ("P", "comma", -75), ("P", "period", -75),

    ("F", "a",   -65), ("F", "o",   -60), ("F", "e",   -60),
    ("F", "period", -80), ("F", "comma", -80),

    ("Y", "o",   -65), ("Y", "a",   -65), ("Y", "e",   -65),
    ("Y", "u",   -60), ("Y", "comma", -80), ("Y", "period", -80),

    ("L", "T",   -55), ("L", "V",   -65), ("L", "W",   -60),
    ("L", "Y",   -65),

    # ── Lowercase optical pairs ───────────────────────────────
    ("r", "a",   -30), ("r", "o",   -30), ("r", "v",   -35),
    ("r", "y",   -35), ("r", "comma", -35), ("r", "period", -35),

    ("v", "a",   -40), ("v", "e",   -35), ("v", "o",   -35),
    ("v", "comma", -45), ("v", "period", -45),

    ("w", "a",   -35), ("w", "e",   -30), ("w", "o",   -30),
    ("w", "comma", -40), ("w", "period", -40),

    ("y", "o",   -30), ("y", "a",   -30),
    ("y", "comma", -35), ("y", "period", -35),

    # ── Digits — clinical readability ────────────────────────
    ("one", "one",   +25),
    ("one", "zero",  +15),
    ("seven", "slash",  -20),
    ("slash", "eight",  -15),
    ("slash", "zero",   -15),

    # Rx abbreviation: tighten R-x
    ("R", "x",   -25),

    # ── Clinical symbols ─────────────────────────────────────
    ("numbersign", "three",  -10),
    ("numbersign", "zero",   -10),
    ("parenleft", "T",    -15), ("parenleft", "V",    -15),
    ("parenright", "period", -20), ("parenright", "comma",  -20),
    ("quotesingle", "T",   -40), ("quotesingle", "V",   -35),
]


def build_fea_string(pairs: list[tuple[str, str, int]],
                     glyph_set: set[str]) -> str:
    """Generate a .fea format kern feature string, filtering missing glyphs."""
    lines = ["feature kern {"]
    count = 0
    for left, right, kern_val in pairs:
        if left in glyph_set and right in glyph_set:
            lines.append(f"    pos {left} {right} {kern_val};")
            count += 1
    lines.append("} kern;")
    return "\n".join(lines), count


def inject_kern(font: TTFont, pairs: list[tuple[str, str, int]]) -> int:
    """Inject kern feature via feaLib."""
    glyph_set = set(font.getGlyphOrder())
    fea_str, count = build_fea_string(pairs, glyph_set)
    if count == 0:
        return 0

    import io
    from fontTools.feaLib.parser import Parser
    from fontTools.feaLib.builder import Builder

    fea_file = io.StringIO(fea_str)
    try:
        parser = Parser(fea_file, glyphNames=list(glyph_set))
        tree = parser.parse()
        builder = Builder(font, tree)
        builder.build()
    except Exception as e:
        print(f"    [!] feaLib error: {e}")
        # Fallback: write raw kern table via direct GPOS
        return _inject_kern_raw(font, pairs, glyph_set)

    return count


def _inject_kern_raw(font: TTFont,
                     pairs: list[tuple[str, str, int]],
                     glyph_set: set[str]) -> int:
    """
    Fallback: inject kern via raw GPOS data structure manipulation
    using fontTools.ttLib's table builder.
    """
    from collections import defaultdict
    from fontTools.ttLib import newTable

    valid = [(l, r, k) for l, r, k in pairs if l in glyph_set and r in glyph_set]
    if not valid:
        return 0

    # Use the kern table (TrueType kern, not OpenType GPOS)
    # Format 0: pairs sorted by (left << 16 | right glyph index)
    gorder = font.getGlyphOrder()
    gindex = {g: i for i, g in enumerate(gorder)}

    kern_pairs_sorted = sorted(
        [(gindex[l], gindex[r], k) for l, r, k in valid if l in gindex and r in gindex]
    )

    if 'kern' in font:
        kern_table = font['kern']
    else:
        kern_table = newTable('kern')
        kern_table.version = 0

    from fontTools.ttLib.tables._k_e_r_n import KernTable_format_0
    ktf0 = KernTable_format_0(apple=False)
    ktf0.kernTable = {}
    for li, ri, k in kern_pairs_sorted:
        left_name = gorder[li]
        right_name = gorder[ri]
        ktf0.kernTable[(left_name, right_name)] = k

    kern_table.kernTables = [ktf0]
    font['kern'] = kern_table
    return len(kern_pairs_sorted)


def main():
    root = Path(__file__).parent.parent
    fonts_dir = root  # TTFs are compiled to the typeface root
    app_fonts = root.parent / 'pocketgull' / 'public' / 'fonts'

    variants = [
        'PocketGull-Bold.ttf',
        'PocketGull-Antigravity.ttf',
        'PocketGull-Chiseltip.ttf',
        'PocketGull-Fineliner.ttf',
        'PocketGullMono-Regular.ttf',
    ]

    print("=" * 60)
    print("POCKETGULL KERNING ENGINE")
    print("=" * 60)
    print(f"\n  Kern pair definitions: {len(KERN_PAIRS)}")
    print(f"  Fonts dir: {fonts_dir}\n")

    total = 0
    for variant in variants:
        path = fonts_dir / variant
        if not path.exists():
            print(f"  SKIP {variant} — not found")
            continue

        font = TTFont(path)
        n = inject_kern(font, KERN_PAIRS)
        font.save(path)
        total += n
        print(f"  {variant}: {n} pairs injected OK")

        if app_fonts.exists():
            shutil.copy2(path, app_fonts / variant)
            print(f"    -> synced to public/fonts/")

    print(f"\n  Total pairs applied: {total}")
    print(f"\n{'=' * 60}")
    print("KERNING COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
