import sys
import copy
from pathlib import Path
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

REPO_ROOT = Path(r"C:\Users\philg\Pocketgull\pocketgull-typeface")
FONTS_DIR = REPO_ROOT / "fonts"

# Source Fonts on Windows Host
SRC_CHINESE_REG = Path(r"C:\Windows\Fonts\msyh.ttc")     # Microsoft YaHei (Font 0)
SRC_CHINESE_BD = Path(r"C:\Windows\Fonts\msyhbd.ttc")    # Microsoft YaHei Bold (Font 0)
SRC_SANSKRIT = Path(r"C:\Windows\Fonts\Nirmala.ttc")     # Nirmala UI (Font 0 Reg, 1 Bold)
SRC_KOREAN_REG = Path(r"C:\Windows\Fonts\malgun.ttf")    # Malgun Gothic Regular
SRC_KOREAN_BD = Path(r"C:\Windows\Fonts\malgunbd.ttf")   # Malgun Gothic Bold
SRC_GLOBAL_REG = Path(r"C:\Windows\Fonts\segoeui.ttf")   # Segoe UI (Arabic & Hebrew)
SRC_GLOBAL_BD = Path(r"C:\Windows\Fonts\segoeuib.ttf")   # Segoe UI Bold

CHINESE_ANATOMICAL_TEXT = "下与主体动右叶大小左心椎盆肋肌肝股肱肺肾胃胫胸脉脏脑腓腔腰锁静颈颌额骨髋"

SANSKRIT_CLINICAL_CODEPOINTS = [
    0x0902, 0x0905, 0x0906, 0x0907, 0x0909, 0x090F, 0x0910, 0x0913, 0x0914,
    0x0915, 0x0916, 0x0917, 0x0918, 0x091A, 0x091C, 0x091F, 0x0920, 0x0921, 0x0922, 0x0923,
    0x0924, 0x0925, 0x0926, 0x0927, 0x0928, 0x092A, 0x092B, 0x092C, 0x092D, 0x092E,
    0x092F, 0x0930, 0x0932, 0x0935, 0x0936, 0x0937, 0x0938, 0x0939,
    0x093E, 0x093F, 0x0940, 0x0941, 0x0942, 0x0943, 0x0947, 0x0948, 0x094B, 0x094C, 0x094D,
    0x0964, 0x0965, 0x0966, 0x0967, 0x0968, 0x0969, 0x096A, 0x096B
]

KOREAN_CLINICAL_TEXT = "뇌소전두골심장근폐간신위흉추요반혈압맥박척골두개골대소장"

ARABIC_CLINICAL_TEXT = (
    "المخالقلبرئتانالكبدعظمجبهيضغطالدمعضلةالفقراتالصدريةالقطنية"
    "الحوضالنبضتخطيطالعلاماتالحيويةالشريانالأبهر٠١٢٣٤٥٦٧٨٩"
    "َُِّْ"
)

HEBREW_CLINICAL_TEXT = (
    "המוחהגדולעצםהמצחלבשרירהלבריאותכבדכליותקיבהעמודשדרהחזיי"
    "מותניאגןדםלחץדופקמדדיםחיונייםאק״ג"
    "ְִֵֶַָֹֻּ"
)

# Full Pan-Cyrillic Block (U+0400 - U+04FF): Russian, Ukrainian, Bulgarian, Serbian, Belarusian, Kazakh, Mongolian
CYRILLIC_PAN_CODEPOINTS = list(range(0x0400, 0x0500))


WEIGHT_CONFIGS = [
    ("PocketGull-Fineliner", False, False),
    ("PocketGull-Bold", True, False),
    ("PocketGull-Chiseltip", True, False),
    ("PocketGull-Antigravity", False, False),
    ("PocketGull-Numerics", False, False),
    ("PocketGullMono-Regular", False, True),
]

print("=" * 75)
print("COMPILING GLOBAL MULTILINGUAL CLINICAL SUPERFAMILY")
print("Target scripts: Latin, Greek, Cyrillic, Braille, PUA, Chinese, Sanskrit, Korean, Arabic, Hebrew")
print("=" * 75)

# Load source fonts
f_zh_reg = TTFont(SRC_CHINESE_REG, fontNumber=0)
f_zh_bd = TTFont(SRC_CHINESE_BD, fontNumber=0)
f_sa_reg = TTFont(SRC_SANSKRIT, fontNumber=0)
f_sa_bd = TTFont(SRC_SANSKRIT, fontNumber=1)
f_kr_reg = TTFont(SRC_KOREAN_REG)
f_kr_bd = TTFont(SRC_KOREAN_BD)
f_gl_reg = TTFont(SRC_GLOBAL_REG)
f_gl_bd = TTFont(SRC_GLOBAL_BD)

for font_stem, is_bold, is_mono in WEIGHT_CONFIGS:
    target_ttf = REPO_ROOT / f"{font_stem}.ttf"
    if not target_ttf.exists():
        print(f"Skipping missing font: {target_ttf}")
        continue

    print(f"\nProcessing {font_stem} (bold={is_bold}, mono={is_mono})...")
    font = TTFont(target_ttf)
    glyf = font['glyf']
    hmtx = font['hmtx']
    cmap = font.getBestCmap()

    f_zh = f_zh_bd if is_bold else f_zh_reg
    f_sa = f_sa_bd if is_bold else f_sa_reg
    f_kr = f_kr_bd if is_bold else f_kr_reg
    f_gl = f_gl_bd if is_bold else f_gl_reg

    cmap_zh = f_zh.getBestCmap()
    cmap_sa = f_sa.getBestCmap()
    cmap_kr = f_kr.getBestCmap()
    cmap_gl = f_gl.getBestCmap()

    # Helper function to inject a glyph cleanly
    def inject_glyph_from_src(src_font, src_gname, dest_gname, dest_cp=None):
        src_gset = src_font.getGlyphSet()
        if src_gname not in src_gset:
            return False
        
        src_adv = src_font['hmtx'][src_gname][0]
        rec_pen = DecomposingRecordingPen(src_gset)
        src_gset[src_gname].draw(rec_pen)

        tt_pen = TTGlyphPen(None)
        if is_mono:
            # Scale proportionally to fit 600 UPM box
            scale = 0.5 * (540.0 / 1024.0)
            target_adv = 600
            left_margin = int((target_adv - (src_adv * scale)) / 2)
            xfrm = (scale, 0, 0, scale, left_margin, 0)
        else:
            scale = 0.5
            target_adv = int(src_adv * scale)
            xfrm = (scale, 0, 0, scale, 0, 0)

        xfrm_pen = TransformPen(tt_pen, xfrm)
        rec_pen.replay(xfrm_pen)
        glyf[dest_gname] = tt_pen.glyph()
        hmtx[dest_gname] = (target_adv, 0)
        if dest_gname not in font.getGlyphOrder():
            font.getGlyphOrder().append(dest_gname)
        if dest_cp is not None:
            for subtable in font['cmap'].tables:
                if subtable.isUnicode():
                    subtable.cmap[dest_cp] = dest_gname
        return True

    # 1. Chinese Anatomical Characters
    injected_zh = 0
    for ch in CHINESE_ANATOMICAL_TEXT:
        cp = ord(ch)
        if cp in cmap_zh:
            src_gname = cmap_zh[cp]
            dest_gname = f"uni{cp:04X}"
            if inject_glyph_from_src(f_zh, src_gname, dest_gname, cp):
                injected_zh += 1

    # 2. Sanskrit Devanagari Base & Matras
    injected_sa = 0
    for cp in SANSKRIT_CLINICAL_CODEPOINTS:
        if cp in cmap_sa:
            src_gname = cmap_sa[cp]
            dest_gname = f"uni{cp:04X}"
            if inject_glyph_from_src(f_sa, src_gname, dest_gname, cp):
                injected_sa += 1

    # 3. Korean Hangul Syllables
    injected_kr = 0
    for ch in KOREAN_CLINICAL_TEXT:
        cp = ord(ch)
        if cp in cmap_kr:
            src_gname = cmap_kr[cp]
            dest_gname = f"uni{cp:04X}"
            if inject_glyph_from_src(f_kr, src_gname, dest_gname, cp):
                injected_kr += 1

    # 4. Arabic Clinical Characters
    injected_ar = 0
    for ch in ARABIC_CLINICAL_TEXT:
        cp = ord(ch)
        if cp in cmap_gl:
            src_gname = cmap_gl[cp]
            dest_gname = f"uni{cp:04X}"
            if inject_glyph_from_src(f_gl, src_gname, dest_gname, cp):
                injected_ar += 1

    # 5. Hebrew Clinical Characters
    injected_he = 0
    for ch in HEBREW_CLINICAL_TEXT:
        cp = ord(ch)
        if cp in cmap_gl:
            src_gname = cmap_gl[cp]
            dest_gname = f"uni{cp:04X}"
            if inject_glyph_from_src(f_gl, src_gname, dest_gname, cp):
                injected_he += 1

    # 6. Pan-Cyrillic Full 256-Codepoint Block (U+0400 - U+04FF)
    injected_cyr = 0
    for cp in CYRILLIC_PAN_CODEPOINTS:
        if cp in cmap_gl:
            src_gname = cmap_gl[cp]
            dest_gname = f"uni{cp:04X}"
            if inject_glyph_from_src(f_gl, src_gname, dest_gname, cp):
                injected_cyr += 1

    # Ensure gasp table exists
    if 'gasp' not in font:
        gasp = newTable('gasp')
        gasp.gaspRange = {0xFFFF: 15}
        font['gasp'] = gasp

    # Save TTF
    font.save(target_ttf)
    # Save copy in fonts/
    fonts_ttf = FONTS_DIR / f"{font_stem}.ttf"
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    font.save(fonts_ttf)

    # Save WOFF2
    font.flavor = 'woff2'
    target_woff2 = REPO_ROOT / f"{font_stem}.woff2"
    fonts_woff2 = FONTS_DIR / f"{font_stem}.woff2"
    font.save(target_woff2)
    font.save(fonts_woff2)

    total_glyphs = len(font.getGlyphOrder())
    print(f"  -> Total glyphs: {total_glyphs} (ZH: +{injected_zh}, SA: +{injected_sa}, KR: +{injected_kr}, AR: +{injected_ar}, HE: +{injected_he})")
    print(f"  -> Saved TTF ({target_ttf.stat().st_size} B) & WOFF2 ({target_woff2.stat().st_size} B)")

print("\nGLOBAL MULTILINGUAL COMPILATION COMPLETE!")
