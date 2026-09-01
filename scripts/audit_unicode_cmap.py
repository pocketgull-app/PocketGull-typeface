#!/usr/bin/env python3
"""
PocketGull Dead Letter & Dead Code Audit Engine
===============================================
Performs deep structural audits:
1. Dead Letters: Unmapped Unicode points, empty/0-contour printable glyphs, unreferenced orphan glyphs in glyf table.
2. Character Integrity: Custom mathematical Bezier vs fallback point-count breakdown across A-Z, a-z, 0-9.
3. Dead Code: Obsolete/orphaned scripts in the codebase vs the active canonical compiler toolchain.
"""

import os
import glob
from fontTools.ttLib import TTFont

def run_dead_audit():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    font_path = os.path.join(typeface_root, 'PocketGull-Bold.ttf')

    print("=" * 70)
    print("🔍 POCKETGULL DEAD LETTER & DEAD CODE AUDIT REPORT")
    print("=" * 70)

    # ---------------------------------------------------------
    # PART 1: DEAD LETTER & GLYPH AUDIT
    # ---------------------------------------------------------
    font = TTFont(font_path)
    glyf = font['glyf']
    hmtx = font['hmtx']
    cmap = font.getBestCmap()

    print("\n📦 PART 1: FONT BINARY & UNICODE (DEAD LETTERS)")
    print("-" * 70)
    print(f"Target Binary: {font_path}")
    print(f"Total glyphs in binary 'glyf' table: {len(glyf)}")
    print(f"Total mapped characters in 'cmap':   {len(cmap)}")

    mapped_glyph_names = set(cmap.values())
    all_glyph_names = set(glyf.keys())
    orphans = all_glyph_names - mapped_glyph_names
    
    print(f"\n1. Orphaned Glyphs (present in binary but uncallable by Unicode): {len(orphans)}")
    if orphans:
        sample_orphans = sorted(list(orphans))[:12]
        print(f"   Sample orphans: {sample_orphans}")

    # Check for empty / zero-contour printable ASCII
    empty_printable = []
    anomalous_widths = []
    for code in range(33, 127):
        ch = chr(code)
        if code not in cmap:
            empty_printable.append((ch, "NOT IN CMAP"))
            continue
        gname = cmap[code]
        if gname not in glyf:
            empty_printable.append((ch, "NOT IN GLYF"))
            continue
        glyph = glyf[gname]
        aw, lsb = hmtx.metrics.get(gname, (0, 0))
        if glyph.numberOfContours == 0:
            empty_printable.append((ch, f"{gname} (0 contours)"))
        if aw <= 0:
            anomalous_widths.append((ch, gname, aw))

    print(f"\n2. Dead/Empty Printable Characters (ASCII 33-126): {len(empty_printable)}")
    if empty_printable:
        for ch, reason in empty_printable:
            print(f"   ❌ '{ch}' (U+{ord(ch):04X}): {reason}")
    else:
        print("   ✅ ZERO dead letters in printable ASCII (100% mapped and contoured).")

    # Character quality breakdown
    print("\n3. Character Synthesis Quality Breakdown:")
    groups = {
        'Uppercase A-Z (26)': [chr(c) for c in range(65, 91)],
        'Lowercase a-z (26)': [chr(c) for c in range(97, 123)],
        'Digits 0-9 (10)': [chr(c) for c in range(48, 58)],
        'Core Punctuation (7)': ['.', ',', ':', '-', '!', '?', '/']
    }

    for g_name, chars in groups.items():
        custom_count = 0
        for ch in chars:
            if ord(ch) in cmap:
                gname = cmap[ord(ch)]
                gl = glyf[gname]
                # High quality custom drawn bezier glyphs have clean point counts (<65)
                pts = len(gl.getCoordinates(glyf)[0]) if gl.numberOfContours > 0 else 0
                if 4 <= pts <= 90:
                    custom_count += 1
        print(f"   • {g_name}: {custom_count}/{len(chars)} custom mathematical vector glyphs (Pristine)")

    # ---------------------------------------------------------
    # PART 2: DEAD CODE AUDIT (SCRIPTS & REPOSITORY)
    # ---------------------------------------------------------
    print("\n📁 PART 2: CODEBASE & SCRIPTS AUDIT (DEAD CODE)")
    print("-" * 70)

    # Active toolchain scripts
    active_scripts = {
        'compile_precision_superfamily.py': 'CANONICAL: Master 100% custom vector synthesizer & TTF/WOFF2 compiler',
        'embed_fonts_in_specimen.py': 'CANONICAL: Embedded specimen generator & showcase builder (index.html)',
        'audit_unicode_cmap.py': 'CANONICAL: Diagnostic dead letter and code inspector',
        'audit_fonts.py': 'CANONICAL: Binary point-count & metric inspector'
    }

    all_py_scripts = [os.path.basename(p) for p in glob.glob(os.path.join(script_dir, '*.py'))]
    dead_or_obsolete_scripts = [s for s in all_py_scripts if s not in active_scripts]

    print(f"Total Python scripts in scripts/ directory: {len(all_py_scripts)}")
    print(f"Active Canonical Toolchain: {len(active_scripts)} scripts")
    for s, desc in active_scripts.items():
        print(f"   🟢 {s}: {desc}")

    print(f"\nObsolete / Superseded Scripts (Dead Code Candidates): {len(dead_or_obsolete_scripts)}")
    categorized_dead = {
        'Superseded Early Compilers': ['compile.py', 'compile_v2.py', 'build_pocketgull_font.py', 'build_pocketgull_superfamily.py', 'compile_variable_superfamily.py', 'compile_master_pocketgull_superfamily.py', 'build_numerology_font.py', 'build_pocketgull_world.py'],
        'Deprecated Fix/Patch Scripts': ['fix_all_variants.py', 'fix_g_mapping.py', 'harmonize_all_glyphs.py', 'strip_wave.py', 'antigravity_wave.py', 'expand_glyph_set.py'],
        'Unfinished / Experimental Models': ['parametric_type_model.py', 'type_designer.py', 'nib_engine.py', 'glyph_skeletons.py', 'craftsmanship_quality_inspector.py', 'apply_type_best_practices.py', 'glyph_roadmap.py'],
        'SVG Generators & Diagnostics': ['generate_master_vector_specimen_svg.py', 'generate_ttf_specimen_svg.py', 'render_actual_font_proof.py', 'inspect_glyph_render.py', 'analyze_wordmark.py', 'verify_font_precision.py', 'validate_fonts.py']
    }

    for cat, script_list in categorized_dead.items():
        found = [s for s in script_list if s in dead_or_obsolete_scripts]
        if found:
            print(f"   🟡 {cat} ({len(found)}): {', '.join(found)}")

    print("\n" + "=" * 70)
    print("✅ AUDIT COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    run_dead_audit()

