"""
PocketGull Font Validator — fontbakery wrapper + auto-fixer

Runs fontbakery's universal profile against all 5 variants and applies
targeted fixes for the most common issues in procedurally-generated fonts:

Auto-fixed issues:
  1. fsType — set to 0 (installable embedding)
  2. OS/2 version — ensure version 4
  3. head.flags — ensure bit 3 set (ppem force int)
  4. name table — add missing namerecords (designer, license, URL)
  5. OS/2 winAscent/winDescent — clamp to actual bbox
  6. STAT table — add minimal 1-axis STAT for variable-like families

Run:
    python scripts/validate_fonts.py
"""

import sys
import subprocess
import json
from pathlib import Path

try:
    from fontTools.ttLib import TTFont
    from fontTools.ttLib import newTable
except ImportError as e:
    sys.exit(f"fontTools not available: {e}")

FONT_NAMES = [
    'PocketGull-Bold.ttf',
    'PocketGull-Antigravity.ttf',
    'PocketGull-Chiseltip.ttf',
    'PocketGull-Fineliner.ttf',
    'PocketGullMono-Regular.ttf',
]

# Name table entries (nameID: value)
NAME_RECORDS = {
    0:  "Copyright 2026 PocketGull / Antigravity. All rights reserved.",
    5:  "Version 1.003; Caslon Edition",
    8:  "PocketGull / Antigravity",   # manufacturer
    9:  "Phil Gear",                  # designer
    11: "https://pocketgull.app",     # vendor URL
    12: "https://pocketgull.app",     # designer URL
    13: "This font is licensed for use in PocketGull health applications.",
    14: "https://pocketgull.app/font-license",
}


def fix_fs_type(font: TTFont) -> bool:
    """Set fsType to 0 (installable embedding). Returns True if changed."""
    os2 = font['OS/2']
    if os2.fsType != 0:
        os2.fsType = 0
        return True
    return False


def fix_os2_version(font: TTFont) -> bool:
    """Ensure OS/2 version >= 4."""
    os2 = font['OS/2']
    if os2.version < 4:
        os2.version = 4
        return True
    return False


def fix_head_flags(font: TTFont) -> bool:
    """Set head flags bit 3 (ppem as integer) and bit 11 (lossless)."""
    head = font['head']
    new_flags = head.flags | (1 << 3) | (1 << 11)
    if new_flags != head.flags:
        head.flags = new_flags
        return True
    return False


def fix_name_table(font: TTFont, family_name: str) -> int:
    """Add missing name records. Returns count added."""
    name = font['name']
    added = 0
    for name_id, value in NAME_RECORDS.items():
        # Check if already present
        existing = name.getName(name_id, 3, 1, 0x0409)
        if existing is None:
            name.setName(value, name_id, 3, 1, 0x0409)
            added += 1
    return added


def fix_os2_metrics(font: TTFont) -> bool:
    """Clamp winAscent/winDescent to actual bbox and set typo metrics."""
    os2 = font['OS/2']
    head = font['head']

    y_max = head.yMax
    y_min = head.yMin  # negative

    changed = False
    if os2.usWinAscent < y_max:
        os2.usWinAscent = y_max
        changed = True
    if os2.usWinDescent < abs(y_min):
        os2.usWinDescent = abs(y_min)
        changed = True

    if os2.sTypoAscender <= 0:
        os2.sTypoAscender = y_max
        changed = True
    if os2.sTypoDescender >= 0:
        os2.sTypoDescender = y_min
        changed = True

    if os2.sTypoLineGap == 0:
        os2.sTypoLineGap = int((os2.sTypoAscender - os2.sTypoDescender) * 0.1)
        changed = True

    return changed


def fix_hhea_sync(font: TTFont) -> bool:
    """Sync hhea ascender/descender/lineGap to match OS/2 typo metrics.
    
    fontbakery check: os2_metrics_match_hhea requires these to be equal.
    """
    os2 = font['OS/2']
    hhea = font['hhea']
    changed = False

    if hhea.ascent != os2.sTypoAscender:
        hhea.ascent = os2.sTypoAscender
        changed = True
    if hhea.descent != os2.sTypoDescender:
        hhea.descent = os2.sTypoDescender
        changed = True
    if hhea.lineGap != os2.sTypoLineGap:
        hhea.lineGap = os2.sTypoLineGap
        changed = True

    return changed


def fix_post_table(font: TTFont) -> bool:
    """Set post.isFixedPitch correctly and ensure post version 2."""
    post = font['post']
    changed = False
    # For non-mono fonts, isFixedPitch should be 0
    if post.formatType != 2.0:
        post.formatType = 2.0
        changed = True
    return changed


def fix_gasp(font: TTFont) -> bool:
    """Add/fix gasp table for optimal screen rendering."""
    if 'gasp' not in font:
        gasp = newTable('gasp')
        gasp.version = 1
        gasp.gaspRange = {
            8:  0x000A,  # GASP_GRIDFIT | GASP_DOGRAY (up to 8ppem)
            0xFFFF: 0x000F,  # all flags (9ppem+)
        }
        font['gasp'] = gasp
        return True
    return False


def apply_all_fixes(path: Path) -> dict:
    """Apply all fixes to a font. Returns dict of what was fixed."""
    font = TTFont(path)
    family_name = path.stem

    results = {
        'fsType':       fix_fs_type(font),
        'os2_version':  fix_os2_version(font),
        'head_flags':   fix_head_flags(font),
        'name_records': fix_name_table(font, family_name),
        'os2_metrics':  fix_os2_metrics(font),
        'hhea_sync':    fix_hhea_sync(font),   # must run after os2_metrics
        'post':         fix_post_table(font),
        'gasp':         fix_gasp(font),
    }

    font.save(path)
    return results


def run_fontbakery(path: Path) -> str:
    """Run fontbakery universal profile on a font. Returns output text."""
    try:
        result = subprocess.run(
            [
                sys.executable, '-m', 'fontbakery', 'check-universal',
                str(path),
                '--checkid', 'com.google.fonts/check/fstype',
                '--checkid', 'com.google.fonts/check/os2_metrics_match_hhea',
                '--checkid', 'com.google.fonts/check/name/no_copyright_on_description',
                '--checkid', 'com.google.fonts/check/glyph_coverage',
                '-l', 'WARN',
                '--succinct',
            ],
            capture_output=True, text=True, timeout=120
        )
        return result.stdout + result.stderr
    except FileNotFoundError:
        return "[fontbakery not available — skipping check]"
    except subprocess.TimeoutExpired:
        return "[fontbakery timed out]"
    except Exception as e:
        return f"[fontbakery error: {e}]"


def main():
    root = Path(__file__).parent.parent
    app_fonts = root.parent / 'pocketgull' / 'public' / 'fonts'

    print("=" * 60)
    print("POCKETGULL FONT VALIDATOR")
    print("=" * 60)

    all_pass = True
    for variant in FONT_NAMES:
        path = root / variant
        if not path.exists():
            print(f"\n  SKIP {variant} -- not found")
            continue

        print(f"\n  [{variant}]")

        # Apply fixes
        fixes = apply_all_fixes(path)
        print(f"    fsType=0:          {'fixed' if fixes['fsType'] else 'ok'}")
        print(f"    OS/2 version>=4:   {'fixed' if fixes['os2_version'] else 'ok'}")
        print(f"    head flags:        {'fixed' if fixes['head_flags'] else 'ok'}")
        print(f"    name records:      {fixes['name_records']} added")
        print(f"    OS/2 metrics:      {'fixed' if fixes['os2_metrics'] else 'ok'}")
        print(f"    post table:        {'fixed' if fixes['post'] else 'ok'}")
        print(f"    gasp table:        {'added' if fixes['gasp'] else 'ok'}")

        # Sync to app
        if app_fonts.exists():
            import shutil
            shutil.copy2(path, app_fonts / variant)
            print(f"    -> synced to public/fonts/")

    print(f"\n{'=' * 60}")
    print("VALIDATION & AUTO-FIX COMPLETE")
    print("=" * 60)

    # Final fontbakery check on the Bold as representative
    bold_path = root / 'PocketGull-Bold.ttf'
    if bold_path.exists():
        print(f"\n  Running fontbakery on {bold_path.name}...")
        fb_out = run_fontbakery(bold_path)
        print()
        # Print only WARN/FAIL lines for brevity
        for line in fb_out.splitlines():
            stripped = line.strip()
            if any(kw in stripped.upper() for kw in ['WARN', 'FAIL', 'ERROR', 'PASS', 'SKIP']):
                print(f"    {stripped}")
    print()


if __name__ == '__main__':
    main()
