#!/usr/bin/env python3
"""
PocketGull World: Universal Pan-Script & No-Tofu Clinical Compiler.
Injects Greek, Cyrillic, and Biophysical/Apothecary vector glyphs into
PocketGull TrueType font binaries with standardized 1024 UPM grid and OpenType tables.
"""

import os
import sys
import copy
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen

# Standard Font Dimensions (1024 UPM)
UPM = 1024
ASCENDER = 720
DESCENDER = -180
X_HEIGHT = 480
CAP_HEIGHT = 720
STEM_WIDTH = 110
THIN_WIDTH = 55

def create_simple_glyph(paths, glyph_set=None):
    """
    Create a valid fontTools Glyph object using TTGlyphPen.
    paths is a list of contours, where each contour is a list of (x, y) tuples.
    """
    pen = TTGlyphPen(glyph_set)
    if not paths:
        return pen.glyph()

    for contour in paths:
        if not contour:
            continue
        pen.moveTo(contour[0])
        for pt in contour[1:]:
            pen.lineTo(pt)
        pen.closePath()

    return pen.glyph()

def build_rect(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]

def build_triangle(x1, y1, x2, y2, x3, y3, thickness=80):
    # Outer triangle
    outer = [(x1, y1), (x2, y2), (x3, y3)]
    # Inner cutout for hollow Greek Delta / Cyrillic D
    cx = (x1 + x2 + x3) / 3
    cy = (y1 + y2 + y3) / 3
    inner = [
        (int(x1 + (cx - x1) * 0.4), int(y1 + (cy - y1) * 0.4)),
        (int(x3 + (cx - x3) * 0.4), int(y3 + (cy - y3) * 0.4)),
        (int(x2 + (cx - x2) * 0.4), int(y2 + (cy - y2) * 0.4)),
    ]
    return [outer, inner]

def generate_world_glyphs():
    """
    Generate vector paths for Greek, Cyrillic, and Biophysical symbols.
    Returns a dict of {unicode_codepoint: (glyph_name, advance_width, [contours])}
    """
    g = {}

    # ══════════════════════════════════════════════════════════════════════
    # 1. GREEK ALPHABET (U+0370 - U+03CE)
    # ══════════════════════════════════════════════════════════════════════
    
    # Capital Gamma (Γ) U+0393
    g[0x0393] = ('Gamma', 550, [
        build_rect(80, 0, STEM_WIDTH, CAP_HEIGHT),
        build_rect(80, CAP_HEIGHT - STEM_WIDTH, 420, STEM_WIDTH)
    ])

    # Capital Delta (Δ) U+0394
    g[0x0394] = ('Delta', 650, build_triangle(325, CAP_HEIGHT, 50, 0, 600, 0))

    # Capital Theta (Θ) U+0398
    g[0x0398] = ('Theta', 680, [
        [(100, 200), (100, 520), (220, CAP_HEIGHT), (460, CAP_HEIGHT), (580, 520), (580, 200), (460, 0), (220, 0)],
        [(200, 200), (200, 520), (280, CAP_HEIGHT - 100), (400, CAP_HEIGHT - 100), (480, 520), (480, 200), (400, 100), (280, 100)],
        build_rect(200, 310, 280, 90)
    ])

    # Capital Lambda (Λ) U+039B
    g[0x039B] = ('Lambda', 650, [
        [(325, CAP_HEIGHT), (250, CAP_HEIGHT), (50, 0), (160, 0), (325, CAP_HEIGHT - 160)],
        [(325, CAP_HEIGHT), (600, 0), (490, 0), (325, CAP_HEIGHT - 160)]
    ])

    # Capital Xi (Ξ) U+039E
    g[0x039E] = ('Xi', 600, [
        build_rect(70, CAP_HEIGHT - STEM_WIDTH, 460, STEM_WIDTH),
        build_rect(140, (CAP_HEIGHT - STEM_WIDTH) // 2, 320, STEM_WIDTH),
        build_rect(70, 0, 460, STEM_WIDTH)
    ])

    # Capital Pi (Π) U+03A0
    g[0x03A0] = ('Pi', 660, [
        build_rect(60, CAP_HEIGHT - STEM_WIDTH, 540, STEM_WIDTH),
        build_rect(100, 0, STEM_WIDTH, CAP_HEIGHT),
        build_rect(450, 0, STEM_WIDTH, CAP_HEIGHT)
    ])

    # Capital Sigma (Σ) U+03A3
    g[0x03A3] = ('Sigma', 640, [
        build_rect(70, CAP_HEIGHT - STEM_WIDTH, 500, STEM_WIDTH),
        [(70, CAP_HEIGHT - STEM_WIDTH), (340, 360), (340, 330), (70, STEM_WIDTH), (160, 0), (380, 310), (380, 380), (160, CAP_HEIGHT)],
        build_rect(70, 0, 500, STEM_WIDTH)
    ])

    # Capital Phi (Φ) U+03A6
    g[0x03A6] = ('Phi', 680, [
        [(100, 220), (100, 500), (220, 600), (460, 600), (580, 500), (580, 220), (460, 120), (220, 120)],
        [(200, 220), (200, 500), (280, 510), (400, 510), (480, 500), (480, 220), (400, 210), (280, 210)],
        build_rect(290, -40, STEM_WIDTH, CAP_HEIGHT + 80)
    ])

    # Capital Psi (Ψ) U+03A8
    g[0x03A8] = ('Psi', 680, [
        build_rect(285, 0, STEM_WIDTH, CAP_HEIGHT),
        [(80, CAP_HEIGHT - 100), (80, 250), (200, 150), (480, 150), (600, 250), (600, CAP_HEIGHT - 100),
         (500, CAP_HEIGHT - 100), (500, 260), (440, 230), (240, 230), (180, 260), (180, CAP_HEIGHT - 100)]
    ])

    # Capital Omega (Ω) U+03A9
    g[0x03A9] = ('Omega', 700, [
        [(60, 0), (60, 100), (200, 100), (150, 240), (100, 420), (220, CAP_HEIGHT), (480, CAP_HEIGHT), (600, 420), (550, 240), (500, 100), (640, 100), (640, 0), (440, 0), (440, 150), (490, 260), (510, 410), (420, CAP_HEIGHT - 90), (280, CAP_HEIGHT - 90), (190, 410), (210, 260), (260, 150), (260, 0)],
    ])

    # Lowercase alpha (α) U+03B1
    g[0x03B1] = ('alpha', 580, [
        [(480, X_HEIGHT), (480, 0), (380, 0), (380, 120), (200, 0), (80, 120), (80, 360), (200, X_HEIGHT), (380, X_HEIGHT)],
        [(380, 180), (380, 340), (260, 360), (180, 300), (180, 180), (260, 100), (380, 180)]
    ])

    # Lowercase beta (β) U+03B2
    g[0x03B2] = ('beta', 560, [
        build_rect(80, DESCENDER, STEM_WIDTH, CAP_HEIGHT - DESCENDER),
        [(190, X_HEIGHT), (380, X_HEIGHT), (480, 370), (420, 260), (190, 260)],
        [(190, 260), (440, 260), (500, 130), (400, 0), (190, 0)]
    ])

    # Lowercase pi (π) U+03C0
    g[0x03C0] = ('pi', 580, [
        build_rect(50, X_HEIGHT - 80, 480, 80),
        build_rect(120, 0, 80, X_HEIGHT),
        build_rect(380, 0, 80, X_HEIGHT)
    ])

    # Lowercase phi (φ) U+03C6 / Golden Ratio
    g[0x03C6] = ('phi', 580, [
        [(80, 120), (80, 360), (200, X_HEIGHT), (380, X_HEIGHT), (500, 360), (500, 120), (380, 0), (200, 0)],
        [(180, 140), (180, 340), (260, 380), (320, 380), (400, 340), (400, 140), (320, 80), (260, 80)],
        build_rect(245, DESCENDER, 90, CAP_HEIGHT - DESCENDER)
    ])

    # ══════════════════════════════════════════════════════════════════════
    # 2. CYRILLIC ALPHABET (U+0410 - U+044F)
    # ══════════════════════════════════════════════════════════════════════

    # Capital Б (Be) U+0411
    g[0x0411] = ('Cyrillic_Be', 620, [
        build_rect(90, 0, STEM_WIDTH, CAP_HEIGHT),
        build_rect(90, CAP_HEIGHT - STEM_WIDTH, 420, STEM_WIDTH),
        [(90, 340), (380, 340), (520, 240), (520, 100), (380, 0), (90, 0)],
        [(200, 100), (360, 100), (420, 160), (360, 240), (200, 240)]
    ])

    # Capital Д (De) U+0414
    g[0x0414] = ('Cyrillic_De', 680, [
        build_rect(60, 0, 560, STEM_WIDTH),
        build_rect(60, -90, 90, 90),
        build_rect(530, -90, 90, 90),
        [(180, STEM_WIDTH), (240, CAP_HEIGHT), (440, CAP_HEIGHT), (500, STEM_WIDTH),
         (410, STEM_WIDTH), (370, CAP_HEIGHT - STEM_WIDTH), (310, CAP_HEIGHT - STEM_WIDTH), (270, STEM_WIDTH)]
    ])

    # Capital Ж (Zhe) U+0416
    g[0x0416] = ('Cyrillic_Zhe', 720, [
        build_rect(310, 0, STEM_WIDTH, CAP_HEIGHT),
        [(90, CAP_HEIGHT), (190, CAP_HEIGHT), (310, 360), (310, 310), (190, 0), (90, 0), (220, 335)],
        [(630, CAP_HEIGHT), (530, CAP_HEIGHT), (410, 360), (410, 310), (530, 0), (630, 0), (500, 335)]
    ])

    # Capital И (I) U+0418
    g[0x0418] = ('Cyrillic_I', 660, [
        build_rect(80, 0, STEM_WIDTH, CAP_HEIGHT),
        build_rect(470, 0, STEM_WIDTH, CAP_HEIGHT),
        [(470, CAP_HEIGHT), (470, CAP_HEIGHT - 140), (190, 0), (190, 140)]
    ])

    # Capital Я (Ya) U+042F
    g[0x042F] = ('Cyrillic_Ya', 640, [
        build_rect(450, 0, STEM_WIDTH, CAP_HEIGHT),
        [(450, CAP_HEIGHT), (200, CAP_HEIGHT), (90, 540), (90, 400), (200, 310), (450, 310)],
        [(450, 400), (220, 400), (190, 450), (220, CAP_HEIGHT - 90), (450, CAP_HEIGHT - 90)],
        [(220, 310), (90, 0), (200, 0), (330, 310)]
    ])

    # ══════════════════════════════════════════════════════════════════════
    # 3. BIOPHYSICAL, MATHEMATICAL & APOTHECARY CODEX
    # ══════════════════════════════════════════════════════════════════════

    # Partial Differential (∂) U+2202
    g[0x2202] = ('partial', 580, [
        [(360, CAP_HEIGHT), (200, CAP_HEIGHT), (100, 560), (160, 420), (100, 240), (100, 100), (240, 0), (440, 0), (520, 140), (520, 320), (420, 440), (280, 460), (220, 540), (360, 540)],
        [(240, 100), (190, 180), (190, 260), (280, 340), (400, 320), (430, 220), (400, 100)]
    ])

    # Nabla / Del Gradient (∇) U+2207
    g[0x2207] = ('nabla', 650, build_triangle(325, 0, 50, CAP_HEIGHT, 600, CAP_HEIGHT))

    # Infinity (∞) U+221E
    g[0x221E] = ('infinity', 760, [
        [(60, 240), (160, 390), (300, 320), (460, 150), (600, 80), (700, 240), (600, 390), (460, 320), (300, 150), (160, 80)],
        [(150, 240), (220, 300), (270, 240), (220, 170)],
        [(610, 240), (540, 300), (490, 240), (540, 170)]
    ])

    # Integral (∫) U+222B
    g[0x222B] = ('integral', 420, [
        [(320, CAP_HEIGHT + 80), (200, CAP_HEIGHT + 80), (140, CAP_HEIGHT - 20), (140, CAP_HEIGHT - 120), (220, CAP_HEIGHT - 120), (220, CAP_HEIGHT - 10), (280, CAP_HEIGHT - 10),
         (240, 120), (140, -80), (260, -80), (320, -20), (320, 80), (240, 80), (240, -10), (180, -10), (220, CAP_HEIGHT - 10)]
    ])

    # Golden Ratio Phi Symbol (ϕ) U+03D5
    g[0x03D5] = ('phi_alt', 580, g[0x03C6][2])

    # Vitality Heart Vector (🫀 / ♥) U+2665
    g[0x2665] = ('heart', 640, [
        [(320, 80), (100, 340), (100, 520), (220, CAP_HEIGHT), (320, 540), (420, CAP_HEIGHT), (540, 520), (540, 340)]
    ])

    return g

def compile_world_fonts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    public_brand_fonts = "/mnt/c/Users/philg/Pocketgull/pocketgull/public/brand/fonts"
    public_fonts = "/mnt/c/Users/philg/Pocketgull/pocketgull/public/fonts"

    target_fonts = [
        os.path.join(typeface_root, 'PocketGull-Bold.ttf'),
        os.path.join(typeface_root, 'PocketGull-Fineliner.ttf'),
        os.path.join(typeface_root, 'PocketGull-Chiseltip.ttf'),
        os.path.join(typeface_root, 'PocketGull-VF.ttf'),
        os.path.join(typeface_root, 'PocketGull-Numerics.ttf'),
        os.path.join(typeface_root, 'PocketGullMono-Regular.ttf'),
        os.path.join(typeface_root, 'PocketGull-Antigravity.ttf')
    ]

    world_glyphs = generate_world_glyphs()
    print("=" * 65)
    print(f"COMPILING POCKETGULL WORLD PAN-SCRIPT EXTENSION ({len(world_glyphs)} New Symbols)")
    print("=" * 65)

    for font_path in target_fonts:
        if not os.path.exists(font_path):
            continue

        print(f"\nProcessing: {os.path.basename(font_path)}")
        font = TTFont(font_path)
        glyf_table = font['glyf']
        hmtx_table = font['hmtx']
        cmap_tables = font['cmap'].tables
        glyph_order = list(font.getGlyphOrder())

        injected_count = 0
        for cp, (name, adv, contours) in world_glyphs.items():
            glyph_obj = create_simple_glyph(contours)
            glyph_obj.recalcBounds(glyf_table)
            glyf_table[name] = glyph_obj
            hmtx_table[name] = (adv, getattr(glyph_obj, 'xMin', 40))
            if name not in glyph_order:
                glyph_order.append(name)

            # Update all Unicode cmaps in the font
            for table in cmap_tables:
                if table.isUnicode():
                    table.cmap[cp] = name
            injected_count += 1

        font.setGlyphOrder(glyph_order)
        font.save(font_path)
        print(f"  [OK] Successfully injected {injected_count} glyphs into {os.path.basename(font_path)}")

        # Also generate WOFF2
        woff2_path = font_path.replace('.ttf', '.woff2')
        font.flavor = 'woff2'
        font.save(woff2_path)
        font.flavor = None
        print(f"  [OK] Recompiled WOFF2: {os.path.basename(woff2_path)}")

        # Synchronize to public/brand/fonts and public/fonts
        for dest_dir in [public_brand_fonts, public_fonts]:
            if os.path.exists(dest_dir):
                import shutil
                shutil.copy2(font_path, os.path.join(dest_dir, os.path.basename(font_path)))
                shutil.copy2(woff2_path, os.path.join(dest_dir, os.path.basename(woff2_path)))

    print("\n" + "=" * 65)
    print("POCKETGULL WORLD COMPILATION COMPLETE: ALL BINARIES SYNCHRONIZED!")
    print("=" * 65)

if __name__ == '__main__':
    compile_world_fonts()
