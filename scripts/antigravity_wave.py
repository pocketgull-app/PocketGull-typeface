"""
PocketGull Antigravity Wave — GSUB calt feature

Creates the signature floating-baseline effect:
  base glyph → .up alternate (+15 UPM) → .dn alternate (-15 UPM) → repeat

Implementation:
  1. Clone every glyph into {glyph}.up and {glyph}.dn variants
     with outlines Y-shifted by ±WAVE_AMP UPM
  2. Write a .fea calt feature using contextual chain substitution:
        sub @base @wave_glyphs' by @up;   # after base, next is .up
        sub @up   @wave_glyphs' by @dn;   # after .up, next is .dn
        # after .dn, next is base (no substitution needed)
  3. Compile .fea into font via feaLib

Run:
    python scripts/antigravity_wave.py

References:
  - Original PocketGull spec: "Antigravity" variant — floating baseline wave +-15 UPM
  - OpenType spec: GSUB LookupType 6 (ChainContextSubst) via calt
"""

import sys
import shutil
from pathlib import Path

try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.feaLib.parser import Parser
    from fontTools.feaLib.builder import Builder
    import io
except ImportError as e:
    sys.exit(f"fontTools not available: {e}")

# ─────────────────────────────────────────────────────────────
# Wave parameters
# ─────────────────────────────────────────────────────────────
WAVE_AMP   = 15    # UPM units — vertical shift for .up / .dn alternates
WAVE_CHARS = (
    list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") +
    list("0123456789")
)


def get_glyph_ps_name(font: TTFont, char: str) -> str | None:
    """Get PostScript glyph name for a Unicode character."""
    cmap = font.getBestCmap()
    if not cmap:
        return None
    cp = ord(char)
    return cmap.get(cp)


def clone_glyph_shifted(font: TTFont, src_name: str,
                         dst_name: str, y_shift: int) -> bool:
    """
    Clone glyph src_name into dst_name with all Y coordinates
    offset by y_shift UPM. Returns True if successful.
    """
    glyf = font['glyf']
    hmtx = font['hmtx']

    if src_name not in glyf.glyphs:
        return False

    src_glyph = glyf[src_name]

    # Draw source glyph into a pen, apply Y transform, capture in new glyph
    pen = TTGlyphPen(font.getGlyphSet())
    transform_pen = TransformPen(pen, (1, 0, 0, 1, 0, y_shift))

    try:
        glyph_set = font.getGlyphSet()
        glyph_set[src_name].draw(transform_pen)
    except Exception:
        # Glyph has no contours (e.g., space) — clone as empty
        return False

    new_glyph = pen.glyph()
    if new_glyph is None:
        return False

    # Add glyph to font
    glyf.glyphs[dst_name] = new_glyph

    # Copy advance width
    advance, lsb = hmtx.metrics.get(src_name, (500, 0))
    hmtx.metrics[dst_name] = (advance, lsb)

    return True


def add_cmap_entries(font: TTFont, char_to_alternates: dict[str, tuple[str, str]]):
    """
    Alternate glyphs don't need cmap entries (they're accessed via GSUB),
    but we must register them in the glyph order.
    """
    gorder = font.getGlyphOrder()
    new_names = []
    for char, (up_name, dn_name) in char_to_alternates.items():
        if up_name not in gorder:
            new_names.append(up_name)
        if dn_name not in gorder:
            new_names.append(dn_name)
    font.setGlyphOrder(gorder + new_names)


def build_calt_fea(char_to_alternates: dict[str, tuple[str, str]],
                   glyph_set: set[str]) -> str:
    """
    Generate OpenType Feature Code for the calt Antigravity wave.

    Pattern: base → .up → .dn → base → .up → .dn → …

    Rules:
      After seeing a base glyph, substitute the next base glyph with .up
      After seeing .up, substitute the next base glyph with .dn
      After .dn, leave next as base (natural reset)
    """
    base_glyphs = []
    up_glyphs   = []
    dn_glyphs   = []

    for char, (up_name, dn_name) in sorted(char_to_alternates.items()):
        base_name = None
        for g in glyph_set:
            # Find the base glyph name for this char
            pass

    # Build glyph lists from char_to_alternates
    all_base = []
    all_up   = []
    all_dn   = []

    for char, (up_name, dn_name) in sorted(char_to_alternates.items()):
        # We need the base glyph name — get it from the substitution pairs
        # It was stored in the mapping
        base_name = _char_base_map.get(char)
        if base_name and base_name in glyph_set:
            if up_name in glyph_set and dn_name in glyph_set:
                all_base.append(base_name)
                all_up.append(up_name)
                all_dn.append(dn_name)

    if not all_base:
        return ""

    base_list = " ".join(all_base)
    up_list   = " ".join(all_up)
    dn_list   = " ".join(all_dn)

    fea = f"""# PocketGull Antigravity Wave — calt feature
# Cycles every character through base -> +{WAVE_AMP}UPM -> -{WAVE_AMP}UPM

@PG_base = [{base_list}];
@PG_up   = [{up_list}];
@PG_dn   = [{dn_list}];

feature calt {{
    lookup calt_wave_up {{
        # After a base glyph, next base glyph becomes .up
        sub @PG_base @PG_base' by @PG_up;
    }} calt_wave_up;

    lookup calt_wave_dn {{
        # After an .up glyph, next base glyph becomes .dn
        sub @PG_up @PG_base' by @PG_dn;
    }} calt_wave_dn;
}} calt;
"""
    return fea


# Module-level map populated during processing
_char_base_map: dict[str, str] = {}


def process_font(path: Path, app_fonts: Path) -> tuple[int, int]:
    """
    Process one font variant:
    1. Clone glyphs into .up / .dn alternates
    2. Inject calt feature
    Returns (n_alternates_added, n_calt_rules)
    """
    font = TTFont(path)
    glyph_set_before = set(font.getGlyphOrder())

    char_to_alternates: dict[str, tuple[str, str]] = {}

    # Step 1: clone shifted glyphs
    _char_base_map.clear()
    for char in WAVE_CHARS:
        base_name = get_glyph_ps_name(font, char)
        if not base_name or base_name not in glyph_set_before:
            continue

        up_name = f"{base_name}.up"
        dn_name = f"{base_name}.dn"

        # Register glyph order first
        gorder = font.getGlyphOrder()
        if up_name not in gorder:
            gorder.append(up_name)
        if dn_name not in gorder:
            gorder.append(dn_name)
        font.setGlyphOrder(gorder)

        # Ensure hmtx has entries for new glyphs
        advance, lsb = font['hmtx'].metrics.get(base_name, (500, 0))
        font['hmtx'].metrics[up_name] = (advance, lsb)
        font['hmtx'].metrics[dn_name] = (advance, lsb)

        # Clone with Y shift
        ok_up = clone_glyph_shifted(font, base_name, up_name, +WAVE_AMP)
        ok_dn = clone_glyph_shifted(font, base_name, dn_name, -WAVE_AMP)

        if ok_up and ok_dn:
            char_to_alternates[char] = (up_name, dn_name)
            _char_base_map[char] = base_name

    n_alts = len(char_to_alternates) * 2

    # Step 2: build and inject calt feature
    glyph_set_now = set(font.getGlyphOrder())
    fea_str = build_calt_fea(char_to_alternates, glyph_set_now)

    n_rules = 0
    if fea_str:
        try:
            fea_file = io.StringIO(fea_str)
            parser = Parser(fea_file, glyphNames=list(glyph_set_now))
            tree = parser.parse()
            builder = Builder(font, tree)
            builder.build()
            n_rules = len(char_to_alternates)
        except Exception as e:
            print(f"    [!] calt build error: {e}")
            # Write .fea file alongside font for manual inspection
            fea_out = path.parent / f"{path.stem}_calt.fea"
            fea_out.write_text(fea_str, encoding='utf-8')
            print(f"    [i] .fea written to: {fea_out.name}")

    font.save(path)

    # Sync to app
    if app_fonts.exists():
        shutil.copy2(path, app_fonts / path.name)

    return n_alts, n_rules


def main():
    root      = Path(__file__).parent.parent
    fonts_dir = root
    app_fonts = root.parent / 'pocketgull' / 'public' / 'fonts'

    variants = [
        'PocketGull-Bold.ttf',
        'PocketGull-Antigravity.ttf',
        'PocketGull-Chiseltip.ttf',
        'PocketGull-Fineliner.ttf',
        'PocketGullMono-Regular.ttf',
    ]

    print("=" * 60)
    print("POCKETGULL ANTIGRAVITY WAVE ENGINE")
    print("=" * 60)
    print(f"\n  Wave amplitude : +-{WAVE_AMP} UPM")
    print(f"  Wave characters: {len(WAVE_CHARS)}")
    print(f"  Expected alts  : {len(WAVE_CHARS) * 2} per variant\n")

    for variant in variants:
        path = fonts_dir / variant
        if not path.exists():
            print(f"  SKIP {variant} -- not found")
            continue

        n_alts, n_rules = process_font(path, app_fonts)
        sync_note = "-> synced" if app_fonts.exists() else ""
        print(f"  {variant}: {n_alts} alt glyphs, {n_rules} calt rules {sync_note}")

    print(f"\n{'=' * 60}")
    print("ANTIGRAVITY WAVE COMPLETE")
    print("=" * 60)
    print()
    print("To activate in CSS:")
    print("  font-feature-settings: 'calt' 1;")
    print("  (Most browsers enable calt by default)")


if __name__ == '__main__':
    main()
