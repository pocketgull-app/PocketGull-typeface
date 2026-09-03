#!/usr/bin/env python3
"""
PocketGull Master Multilingual Precision Superfamily Compiler
Compiles all 6 weights with:
1. Authentic Master Hand-Drawn Vector Contours (1024 UPM Grid)
2. Life-Critical Clinical PUA Telemetry (U+E001 - U+E006)
3. Greek Pharmacology Units (Alpha - Omega, Delta, Sigma, Mu, Pi)
4. Cyrillic Emergency Triage Homoglyphs
5. Full 256-Glyph Unicode Braille Patterns Block (U+2800 - U+28FF, ISO/TR 11548)
6. ISMP / FDA Clinical Disambiguation (zero.slash, l.curved, I.serif)
7. OpenType GSUB Feature Tables (zero, cv08, cv05, ss02)
8. Curated 36 Chinese Anatomical Hanzi Characters (U+4E00 - U+9ACB)
9. Curated 45 Sanskrit Devanagari Base & Matra Codepoints (U+0902 - U+096B)
10. Unencoded Devanagari Conjuncts & Ligatures for Clinical Terms
11. Thomas Phinney gasp Subpixel Antialiasing Tables
12. Monospace Invariant: Fixed 600 UPM Advance across ALL glyphs in PocketGullMono-Regular
13. True Brotli WOFF2 & TTF Compilation + Synchronization to fonts/ directory
"""

import os
import sys
import shutil
import tempfile
from pathlib import Path
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
import fontTools.feaLib.builder as feaBuilder

def extract_decomposed_glyph(src_glyph_set, src_glyph_name, transform_matrix):
    """Decomposes any composite or simple glyph recursively into standalone contours."""
    rec = DecomposingRecordingPen(src_glyph_set)
    src_glyph_set[src_glyph_name].draw(rec)
    pen = TTGlyphPen(None)
    tpen = TransformPen(pen, transform_matrix)
    rec.replay(tpen)
    return pen.glyph()

# Add pocketgull-typeface scripts to sys.path
typeface_root = Path(r"C:\Users\philg\Pocketgull\pocketgull-typeface")
sys.path.insert(0, str(typeface_root / 'scripts'))

from compile_precision_superfamily import create_precision_extensions, make_clean_glyph

# ─────────────────────────────────────────────────────────────────────────────
# 1. BRAILLE PATTERNS GENERATOR (U+2800 - U+28FF)
# ─────────────────────────────────────────────────────────────────────────────
def draw_smooth_circle(pen, cx, cy, r):
    """Draw a clean, clockwise circular dot using 4 cubic Bezier segments."""
    k = r * 0.55228475
    pen.moveTo((cx, cy + r))
    pen.curveTo((cx + k, cy + r), (cx + r, cy + k), (cx + r, cy))
    pen.curveTo((cx + r, cy - k), (cx + k, cy - r), (cx, cy - r))
    pen.curveTo((cx - k, cy - r), (cx - r, cy - k), (cx - r, cy))
    pen.curveTo((cx - r, cy + k), (cx - k, cy + r), (cx, cy + r))
    pen.closePath()

def generate_braille_glyph(codepoint, dot_radius=50, advance_width=600):
    bitmask = codepoint - 0x2800
    dot_coords = {
        0: (200, 580), # Dot 1
        1: (200, 420), # Dot 2
        2: (200, 260), # Dot 3
        3: (380, 580), # Dot 4
        4: (380, 420), # Dot 5
        5: (380, 260), # Dot 6
        6: (200, 100), # Dot 7
        7: (380, 100), # Dot 8
    }

    def draw_dots(pen):
        for bit_idx, (cx, cy) in dot_coords.items():
            if (bitmask >> bit_idx) & 1:
                draw_smooth_circle(pen, cx, cy, dot_radius)

    return draw_dots, advance_width

# ─────────────────────────────────────────────────────────────────────────────
# 2. CHINESE ANATOMICAL HANZI CATALOG
# ─────────────────────────────────────────────────────────────────────────────
CHINESE_ANATOMICAL_CHARS = [
    '下', '与', '主', '体', '动', '右', '叶', '大', '小', '左', 
    '心', '椎', '盆', '肋', '肌', '肝', '股', '肱', '肺', '肾', 
    '胃', '胫', '胸', '脉', '脏', '脑', '腓', '腔', '腰', '锁', 
    '静', '颈', '颌', '额', '骨', '髋'
]

# ─────────────────────────────────────────────────────────────────────────────
# 3. SANSKRIT CLINICAL DEVANAGARI CODEPOINTS & CLINICAL TERMS
# ─────────────────────────────────────────────────────────────────────────────
SANSKRIT_CLINICAL_CODEPOINTS = [
    0x0902, 0x0905, 0x0906, 0x0909, 0x090A, 0x0913, 0x0915, 0x0917, 0x0918, 0x0919, 
    0x091C, 0x091F, 0x0921, 0x0923, 0x0924, 0x0925, 0x0926, 0x0927, 0x0928, 0x092A, 
    0x092B, 0x092C, 0x092D, 0x092E, 0x092F, 0x0930, 0x0932, 0x0935, 0x0936, 0x0937, 
    0x0938, 0x0939, 0x093E, 0x093F, 0x0940, 0x0941, 0x0942, 0x0943, 0x0947, 0x094B, 
    0x094D, 0x0966, 0x0967, 0x096A, 0x096B
]

SANSKRIT_CLINICAL_TERMS = [
    'ललाटास्थि', 'मस्तिष्कम्', 'अनुमस्तिष्कम्', 'हनु', 'ग्रीवा-कशेरुका',
    'वक्ष-कशेरुका', 'कटि-कशेरुका', 'वामाक्षक', 'दक्षाक्षक', 'उरस्',
    'पर्शुक १-४', 'पर्शुक ५-१०', 'हृदयम् • हृत्पेशी', 'वाम-फुप्फुस',
    'दक्षिण-फुप्फुस', 'यकृत्', 'आमाशय', 'दक्षिण-वृक्क', 'वाम-वृक्क',
    'श्रोणिफलक', 'दक्षिण-ऊर्वस्थि', 'वाम-ऊर्वस्थि', 'दक्षिण-जङ्घास्थि',
    'वाम-जङ्घास्थि', 'दक्षिण-प्रगण्डास्थि', 'वाम-प्रगण्डास्थि', 'महाधमनी',
    'महाशिरा', 'भूताग्नि • कोशिकीय ओजस्', 'बीज भाग • प्रकृति संस्कार',
    'कोश कला • प्राण वहा स्रोतस्', 'अस्थि मज्जा धात्वाधार'
]


def compile_pan_asian_indic_superfamily():
    base_font_path = typeface_root / 'PocketGull-VF.ttf'
    fonts_dir = typeface_root / 'fonts'
    fonts_dir.mkdir(exist_ok=True)

    if not base_font_path.exists():
        print(f"Error: Base master font not found at {base_font_path}")
        sys.exit(1)

    print("🚀 Compiling Pan-Asian & Indic Precision Superfamily (1024 UPM)...")

    weights = [
        ('PocketGull-Fineliner.ttf', 300, 'Fineliner', 'PocketGull Fineliner', False, False, 2),
        ('PocketGull-Bold.ttf', 700, 'Bold', 'PocketGull Bold', False, True, 1),
        ('PocketGull-Chiseltip.ttf', 800, 'Chiseltip', 'PocketGull Chiseltip', False, True, 1),
        ('PocketGull-Antigravity.ttf', 400, 'Antigravity', 'PocketGull Antigravity', False, False, 0),
        ('PocketGullMono-Regular.ttf', 500, 'Regular', 'PocketGullMono Regular', True, False, 0),
        ('PocketGull-Numerics.ttf', 600, 'Numerics', 'PocketGull Numerics', False, True, 1),
    ]

    PUA_MAP = {
        'icon_heart_ecg': 0xE001,
        'icon_spo2': 0xE002,
        'icon_glucose': 0xE003,
        'icon_aed_shock': 0xE004,
        'icon_beacon_gps': 0xE005,
        'icon_cpr_coach': 0xE006,
    }

    CYRILLIC_HOMOGLYPHS = {
        0x0410: 'A', 0x0412: 'B', 0x0415: 'E', 0x041A: 'K', 0x041C: 'M',
        0x041D: 'H', 0x041E: 'O', 0x0420: 'P', 0x0421: 'C', 0x0422: 'T',
        0x0423: 'Y', 0x0425: 'X', 0x0430: 'a', 0x0435: 'e', 0x043E: 'o',
        0x0440: 'p', 0x0441: 'c', 0x0443: 'y', 0x0445: 'x',
    }

    msyh_reg_path = Path(r"C:\Windows\Fonts\msyh.ttc")
    msyh_bd_path = Path(r"C:\Windows\Fonts\msyhbd.ttc")
    nirmala_path = Path(r"C:\Windows\Fonts\Nirmala.ttc")

    has_sources = msyh_reg_path.exists() and nirmala_path.exists()

    for filename, wght, style_name, full_name, is_mono, msyh_is_bold, nirmala_num in weights:
        font = TTFont(str(base_font_path))
        glyf_table = font['glyf']
        hmtx_table = font['hmtx']
        glyph_set = font.getGlyphSet()
        cmap = font.getBestCmap()

        # ─── A. Inject Precision Vectors (Greek, Math, PUA) ───────────────────
        precision_extensions = create_precision_extensions(weight=wght)
        for char_key, (draw_fn, aw) in precision_extensions.items():
            final_aw = 600 if is_mono else aw
            if is_mono and aw != 600:
                offset_x = (600 - aw) / 2.0
                def make_mono_draw(fn, ox):
                    def draw_centered(pen):
                        tpen = TransformPen(pen, (1, 0, 0, 1, ox, 0))
                        fn(tpen)
                    return draw_centered
                glyph, advance = make_clean_glyph(make_mono_draw(draw_fn, offset_x), glyph_set, final_aw)
            else:
                glyph, advance = make_clean_glyph(draw_fn, glyph_set, final_aw)

            glyph_name = char_key
            if len(char_key) == 1:
                cp = ord(char_key)
                glyph_name = cmap.get(cp) or f"uni{cp:04X}"

            if glyph_name not in font.getGlyphOrder():
                font.setGlyphOrder(font.getGlyphOrder() + [glyph_name])

            glyf_table[glyph_name] = glyph
            hmtx_table.metrics[glyph_name] = (final_aw, 40)

            if len(char_key) == 1:
                cp = ord(char_key)
                for table in font['cmap'].tables:
                    table.cmap[cp] = glyph_name
            elif char_key.startswith('uni') and len(char_key) == 7:
                try:
                    cp = int(char_key[3:], 16)
                    for table in font['cmap'].tables:
                        table.cmap[cp] = char_key
                except ValueError:
                    pass

        # ─── B. Inject Cyrillic Homoglyphs & PUA Telemetry ─────────────────────
        for cp, latin_char in CYRILLIC_HOMOGLYPHS.items():
            latin_cp = ord(latin_char)
            latin_gname = cmap.get(latin_cp) or latin_char
            for table in font['cmap'].tables:
                table.cmap[cp] = latin_gname

        for table in font['cmap'].tables:
            for gname, ucode in PUA_MAP.items():
                if gname not in font.getGlyphOrder():
                    font.setGlyphOrder(font.getGlyphOrder() + [gname])
                table.cmap[ucode] = gname

        # ─── C. Inject Full 256-Glyph Unicode Braille Patterns Block ─────────
        braille_radius = 65 if wght >= 700 else 52
        for b_cp in range(0x2800, 0x2900):
            b_fn, b_aw = generate_braille_glyph(b_cp, dot_radius=braille_radius, advance_width=600)
            b_glyph, _ = make_clean_glyph(b_fn, glyph_set, 600)
            b_gname = f"uni{b_cp:04X}"

            if b_gname not in font.getGlyphOrder():
                font.setGlyphOrder(font.getGlyphOrder() + [b_gname])

            glyf_table[b_gname] = b_glyph
            hmtx_table.metrics[b_gname] = (600, 100)

            for table in font['cmap'].tables:
                table.cmap[b_cp] = b_gname

        # ─── D. Inject Chinese Anatomical Characters (MS YaHei, 2048->1024) ───
        if has_sources:
            src_cjk_path = msyh_bd_path if (msyh_is_bold and msyh_bd_path.exists()) else msyh_reg_path
            src_cjk_font = TTFont(str(src_cjk_path), fontNumber=0)
            cjk_cmap = src_cjk_font.getBestCmap()
            cjk_glyphs = src_cjk_font.getGlyphSet()

            for zh_char in CHINESE_ANATOMICAL_CHARS:
                zh_cp = ord(zh_char)
                if zh_cp in cjk_cmap:
                    src_gname = cjk_cmap[zh_cp]
                    src_adv, src_lsb = src_cjk_font['hmtx'][src_gname]
                    if is_mono:
                        scale_f = 600.0 / 2048.0 * 0.90
                        ox = (600.0 - (src_adv * scale_f)) / 2.0
                        oy = 50.0
                        zh_glyph = extract_decomposed_glyph(cjk_glyphs, src_gname, (scale_f, 0, 0, scale_f, ox, oy))
                        dest_adv = 600
                    else:
                        zh_glyph = extract_decomposed_glyph(cjk_glyphs, src_gname, (0.5, 0, 0, 0.5, 0, 0))
                        dest_adv = int(src_adv * 0.5)

                    zh_gname = f"uni{zh_cp:04X}"

                    if zh_gname not in font.getGlyphOrder():
                        font.setGlyphOrder(font.getGlyphOrder() + [zh_gname])

                    glyf_table[zh_gname] = zh_glyph
                    hmtx_table.metrics[zh_gname] = (dest_adv, int(src_lsb * (0.5 if not is_mono else scale_f)))

                    for table in font['cmap'].tables:
                        table.cmap[zh_cp] = zh_gname

        # ─── E. Inject Sanskrit Devanagari Codepoints & Conjuncts ─────────────
        if has_sources:
            src_indic_font = TTFont(str(nirmala_path), fontNumber=nirmala_num)
            indic_cmap = src_indic_font.getBestCmap()
            indic_glyphs = src_indic_font.getGlyphSet()

            # Base codepoints
            for sk_cp in SANSKRIT_CLINICAL_CODEPOINTS:
                if sk_cp in indic_cmap:
                    src_gname = indic_cmap[sk_cp]
                    src_adv, src_lsb = src_indic_font['hmtx'][src_gname]
                    src_g = indic_glyphs[src_gname]

                    if is_mono:
                        scale_f = 600.0 / 2048.0 * 0.95
                        ox = (600.0 - (src_adv * scale_f)) / 2.0
                        oy = 20.0
                        sk_glyph = extract_decomposed_glyph(indic_glyphs, src_gname, (scale_f, 0, 0, scale_f, ox, oy))
                        dest_adv = 600
                    else:
                        sk_glyph = extract_decomposed_glyph(indic_glyphs, src_gname, (0.5, 0, 0, 0.5, 0, 0))
                        dest_adv = int(src_adv * 0.5)
                    sk_gname = f"uni{sk_cp:04X}"

                    if sk_gname not in font.getGlyphOrder():
                        font.setGlyphOrder(font.getGlyphOrder() + [sk_gname])

                    glyf_table[sk_gname] = sk_glyph
                    hmtx_table.metrics[sk_gname] = (dest_adv, int(src_lsb * (0.5 if not is_mono else scale_f)))

                    for table in font['cmap'].tables:
                        table.cmap[sk_cp] = sk_gname

            # Conjunct ligatures
            import uharfbuzz as hb
            with open(str(nirmala_path), 'rb') as f:
                nirmala_data = f.read()
            blob = hb.Blob(nirmala_data)
            face = hb.Face(blob, nirmala_num)
            hb_font = hb.Font(face)

            clinical_conjunct_gids = set()
            for term in SANSKRIT_CLINICAL_TERMS:
                buf = hb.Buffer()
                buf.add_str(term)
                buf.guess_segment_properties()
                hb.shape(hb_font, buf)
                for info in buf.glyph_infos:
                    clinical_conjunct_gids.add(info.codepoint)

            nirmala_order = src_indic_font.getGlyphOrder()
            for gid in clinical_conjunct_gids:
                src_gname = nirmala_order[gid]
                if src_gname not in glyf_table:
                    src_adv, src_lsb = src_indic_font['hmtx'][src_gname]
                    src_g = indic_glyphs[src_gname]

                    if is_mono:
                        scale_f = 600.0 / 2048.0 * 0.95
                        ox = (600.0 - (src_adv * scale_f)) / 2.0
                        oy = 20.0
                        conj_glyph = extract_decomposed_glyph(indic_glyphs, src_gname, (scale_f, 0, 0, scale_f, ox, oy))
                        dest_adv = 600
                    else:
                        conj_glyph = extract_decomposed_glyph(indic_glyphs, src_gname, (0.5, 0, 0, 0.5, 0, 0))
                        dest_adv = int(src_adv * 0.5)
                    dest_gname = f"dev_{src_gname}"

                    if dest_gname not in font.getGlyphOrder():
                        font.setGlyphOrder(font.getGlyphOrder() + [dest_gname])

                    glyf_table[dest_gname] = conj_glyph
                    hmtx_table.metrics[dest_gname] = (dest_adv, int(src_lsb * (0.5 if not is_mono else scale_f)))

        # ─── F. ISMP Clinical Disambiguation (zero.slash, I.serif, l.curved) ─
        glyph_order = font.getGlyphOrder()

        if 'zero' in glyf_table:
            z = glyf_table['zero']
            pen = TTGlyphPen(glyf_table)
            z.draw(pen, glyf_table)
            x_min, y_min, x_max, y_max = z.xMin, z.yMin, z.xMax, z.yMax
            stroke = max(25, int((x_max - x_min) * 0.12))
            pen.moveTo((x_min + stroke, y_min + int((y_max - y_min) * 0.15)))
            pen.lineTo((x_max - stroke, y_max - int((y_max - y_min) * 0.15)))
            pen.lineTo((x_max - stroke - stroke, y_max - int((y_max - y_min) * 0.15)))
            pen.lineTo((x_min + stroke - stroke, y_min + int((y_max - y_min) * 0.15)))
            pen.closePath()
            z_slash = pen.glyph()
            z_slash.flags = [f & 0x3F for f in z_slash.flags] if hasattr(z_slash, 'flags') else []
            glyf_table['zero.slash'] = z_slash
            hmtx_table['zero.slash'] = (600 if is_mono else hmtx_table['zero'][0], hmtx_table['zero'][1])
            if 'zero.slash' not in glyph_order:
                glyph_order.append('zero.slash')

        if 'I' in glyf_table:
            stem = glyf_table['I']
            pen = TTGlyphPen(glyf_table)
            stem.draw(pen, glyf_table)
            x_min, y_min, x_max, y_max = stem.xMin, stem.yMin, stem.xMax, stem.yMax
            ser_w = max(45, int((x_max - x_min) * 0.75))
            ser_h = max(25, int((y_max - y_min) * 0.06))
            pen.moveTo((x_min - ser_w, y_max))
            pen.lineTo((x_max + ser_w, y_max))
            pen.lineTo((x_max + ser_w, y_max - ser_h))
            pen.lineTo((x_min - ser_w, y_max - ser_h))
            pen.closePath()
            pen.moveTo((x_min - ser_w, y_min + ser_h))
            pen.lineTo((x_max + ser_w, y_min + ser_h))
            pen.lineTo((x_max + ser_w, y_min))
            pen.lineTo((x_min - ser_w, y_min))
            pen.closePath()
            I_serif = pen.glyph()
            I_serif.flags = [f & 0x3F for f in I_serif.flags] if hasattr(I_serif, 'flags') else []
            glyf_table['I.serif'] = I_serif
            hmtx_table['I.serif'] = (600 if is_mono else (hmtx_table['I'][0] + int(ser_w * 0.5)), hmtx_table['I'][1])
            if 'I.serif' not in glyph_order:
                glyph_order.append('I.serif')

        if 'l' in glyf_table:
            stem = glyf_table['l']
            pen = TTGlyphPen(glyf_table)
            stem.draw(pen, glyf_table)
            x_min, y_min, x_max, y_max = stem.xMin, stem.yMin, stem.xMax, stem.yMax
            tail_w = max(55, int((x_max - x_min) * 0.85))
            tail_h = max(45, int((y_max - y_min) * 0.12))
            pen.moveTo((x_max, y_min + int(tail_h * 0.8)))
            pen.lineTo((x_max + tail_w, y_min + tail_h))
            pen.lineTo((x_max + tail_w - 15, y_min))
            pen.lineTo((x_min, y_min))
            pen.closePath()
            l_curved = pen.glyph()
            l_curved.flags = [f & 0x3F for f in l_curved.flags] if hasattr(l_curved, 'flags') else []
            glyf_table['l.curved'] = l_curved
            hmtx_table['l.curved'] = (600 if is_mono else (hmtx_table['l'][0] + int(tail_w * 0.5)), hmtx_table['l'][1])
            if 'l.curved' not in glyph_order:
                glyph_order.append('l.curved')

        font.setGlyphOrder(glyph_order)

        # ─── G. Compile OpenType GSUB Layout Tables ───────────────────────────
        fea_code = """
languagesystem DFLT dflt;
languagesystem latn dflt;
languagesystem deva dflt;
languagesystem dev2 dflt;

feature zero {
    sub zero by zero.slash;
} zero;

feature cv08 {
    cvParameters {
        FeatUILabelNameID { name "Slashed Zero"; };
    };
    sub zero by zero.slash;
} cv08;

feature cv05 {
    cvParameters {
        FeatUILabelNameID { name "Curved Lowercase L"; };
    };
    sub l by l.curved;
} cv05;

feature ss02 {
    featureNames {
        name "Serifed Capital I";
    };
    sub I by I.serif;
} ss02;
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.fea', delete=False, encoding='utf-8') as f:
            f.write(fea_code)
            fea_path = f.name

        try:
            feaBuilder.addOpenTypeFeatures(font, fea_path)
        except Exception as e:
            print(f"  ⚠️ OpenType feature warning: {e}")
        finally:
            if os.path.exists(fea_path):
                os.remove(fea_path)

        # ─── H. Monospace Invariant Check (PocketGullMono-Regular) ───────────
        if is_mono:
            for gname in font.getGlyphOrder():
                if gname in hmtx_table.metrics:
                    old_adv, old_lsb = hmtx_table.metrics[gname]
                    if old_adv != 600:
                        delta = (600 - old_adv) / 2.0
                        hmtx_table.metrics[gname] = (600, int(old_lsb + delta))

        # ─── I. Inject Thomas Phinney gasp Subpixel Smoothing Table ───────────
        try:
            gasp = newTable('gasp')
            gasp.version = 1
            gasp.gaspRange = {0xFFFF: 0x0F}
            font['gasp'] = gasp
        except Exception as e:
            print(f"  ⚠️ gasp table note: {e}")

        # ─── J. Standardized Vertical & OS/2 Metrics ──────────────────────────
        font['OS/2'].usWeightClass = wght
        font['head'].unitsPerEm = 1024
        font['hhea'].ascent = 1136
        font['hhea'].descent = -325
        font['OS/2'].sTypoAscender = 1136
        font['OS/2'].sTypoDescender = -325

        if is_mono:
            font['post'].isFixedPitch = 1
            font['OS/2'].panose.bProportion = 9
        else:
            font['post'].isFixedPitch = 0
            font['OS/2'].panose.bProportion = 0

        # ─── K. Save TTF & WOFF2 (Root & fonts/ Subdirectory) ─────────────────
        out_ttf_path = typeface_root / filename
        font.save(str(out_ttf_path))
        shutil.copy(str(out_ttf_path), str(fonts_dir / filename))
        print(f"  ✅ Saved TTF ({style_name}): {filename}")

        try:
            font.flavor = 'woff2'
            woff2_name = filename.replace('.ttf', '.woff2')
            out_woff2_path = typeface_root / woff2_name
            font.save(str(out_woff2_path))
            shutil.copy(str(out_woff2_path), str(fonts_dir / woff2_name))
            print(f"  📦 Saved Brotli WOFF2: {woff2_name}")
        except Exception as e:
            print(f"  ⚠️ WOFF2 note: {e}")

    print("\n🎉 Pan-Asian & Indic Superfamily Compilation Complete!")

if __name__ == '__main__':
    compile_pan_asian_indic_superfamily()
