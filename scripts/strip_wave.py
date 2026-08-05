"""
Strip Antigravity Wave — remove calt GSUB feature and .up/.dn alternate glyphs
from all PocketGull font variants.

This is a reversible operation; re-run antigravity_wave.py to restore.
"""

import shutil
import sys
from pathlib import Path

try:
    from fontTools.ttLib import TTFont  # type: ignore[import-not-found]
except ImportError as e:
    sys.exit(f"fontTools not available: {e}")

FONT_NAMES = [
    'PocketGull-Bold.ttf',
    'PocketGull-Antigravity.ttf',
    'PocketGull-Chiseltip.ttf',
    'PocketGull-Fineliner.ttf',
    'PocketGullMono-Regular.ttf',
]


def strip_wave(path: Path) -> tuple[int, bool]:
    """
    Remove .up and .dn alternate glyphs and the calt GSUB feature.
    Returns (n_glyphs_removed, calt_removed).
    """
    font = TTFont(path)

    # 1. Collect alternate glyph names
    gorder = font.getGlyphOrder()
    wave_glyphs = set(g for g in gorder if g.endswith('.up') or g.endswith('.dn'))

    # 2. Remove from glyf table BEFORE updating glyph order
    #    Use 'is not None' — truthiness check triggers glyf.__len__ assertion
    glyf = font.get('glyf')
    if glyf is not None:
        for name in wave_glyphs:
            if name in glyf.glyphs:
                del glyf.glyphs[name]

    # 3. Remove from hmtx
    hmtx = font.get('hmtx')
    if hmtx is not None:
        for name in wave_glyphs:
            hmtx.metrics.pop(name, None)

    # 4. Update glyph order (must happen after glyf cleanup)
    new_order = [g for g in gorder if g not in wave_glyphs]
    font.setGlyphOrder(new_order)

    # 5. Remove calt from GSUB
    calt_removed = False
    if 'GSUB' in font:
        gsub = font['GSUB'].table
        if gsub.FeatureList:
            kept = [f for f in gsub.FeatureList.FeatureRecord
                    if f.FeatureTag != 'calt']
            if len(kept) < len(gsub.FeatureList.FeatureRecord):
                calt_removed = True
            gsub.FeatureList.FeatureRecord = kept
            gsub.FeatureList.FeatureCount = len(kept)

    font.save(path)
    return len(wave_glyphs), calt_removed


def main():
    root      = Path(__file__).parent.parent
    app_fonts = root.parent / 'pocketgull' / 'public' / 'fonts'

    print("=" * 60)
    print("STRIP ANTIGRAVITY WAVE")
    print("=" * 60)
    print()

    total_glyphs = 0
    for variant in FONT_NAMES:
        path = root / variant
        if not path.exists():
            print(f"  SKIP {variant}")
            continue

        n_glyphs, calt_removed = strip_wave(path)
        total_glyphs += n_glyphs
        calt_note = "calt removed" if calt_removed else "no calt found"
        print(f"  {variant}: {n_glyphs} alt glyphs removed, {calt_note}")

        if app_fonts.exists():
            shutil.copy2(path, app_fonts / variant)
            print(f"    -> synced to public/fonts/")

    print(f"\n  Total alternate glyphs removed: {total_glyphs}")
    print(f"\n{'=' * 60}")
    print("WAVE STRIPPED")
    print("=" * 60)


if __name__ == '__main__':
    main()
