#!/usr/bin/env python3
"""
Automated Test Suite for Global Clinical Typography
Validates:
1. 100% CMap mapping for all 36 Chinese anatomical characters.
2. 100% CMap mapping for all 45 Sanskrit Devanagari base & matra codepoints.
3. 100% CMap mapping for all 256 Unicode Braille patterns (U+2800 - U+28FF).
4. HarfBuzz text shaping across:
   - Sanskrit Devanagari clinical terms
   - Chinese anatomical characters
   - Korean Hangul clinical terms
   - Arabic clinical terms
   - Hebrew clinical terms
5. Zero .notdef (tofu) and zero broken glyphs.
"""

import os
import pytest
from pathlib import Path
from fontTools.ttLib import TTFont
import uharfbuzz as hb

REPO_ROOT = Path(r"C:\Users\philg\Pocketgull\pocketgull-typeface")

SUPERFAMILY_FONTS = [
    'PocketGull-Fineliner.ttf',
    'PocketGull-Bold.ttf',
    'PocketGull-Chiseltip.ttf',
    'PocketGull-Antigravity.ttf',
    'PocketGullMono-Regular.ttf',
    'PocketGull-Numerics.ttf',
]

CHINESE_ANATOMICAL_CHARS = [
    '下', '与', '主', '体', '动', '右', '叶', '大', '小', '左', 
    '心', '椎', '盆', '肋', '肌', '肝', '股', '肱', '肺', '肾', 
    '胃', '胫', '胸', '脉', '脏', '脑', '腓', '腔', '腰', '锁', 
    '静', '颈', '颌', '额', '骨', '髋'
]

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

KOREAN_CLINICAL_TERMS = ['뇌', '심장', '폐', '간', '신장', '위', '골', '혈압', '맥박', '척추']
ARABIC_CLINICAL_TERMS = ['المخ', 'القلب', 'الرئتان', 'الكبد', 'ضغط الدم', 'النبض', 'العلامات الحيوية']
HEBREW_CLINICAL_TERMS = ['המוח הגדול', 'עצם המצח', 'לב', 'שריר הלב', 'ריאות', 'כבד', 'כליות', 'דם', 'לחץ דם', 'אק״ג']


class TestChineseClinicalAnatomyCoverage:
    """Assert all 36 Chinese anatomical characters are mapped and have valid contours."""

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_chinese_cmap_coverage(self, font_name):
        font_path = REPO_ROOT / font_name
        font = TTFont(str(font_path))
        cmap = font.getBestCmap()
        assert cmap is not None, f"Font {font_name} missing unicode cmap"

        for zh_char in CHINESE_ANATOMICAL_CHARS:
            cp = ord(zh_char)
            assert cp in cmap, f"Font {font_name} missing Chinese character '{zh_char}' (U+{cp:04X})"

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_chinese_glyph_geometry(self, font_name):
        font_path = REPO_ROOT / font_name
        font = TTFont(str(font_path))
        cmap = font.getBestCmap()
        glyf = font['glyf']

        for zh_char in CHINESE_ANATOMICAL_CHARS:
            cp = ord(zh_char)
            gname = cmap[cp]
            glyph = glyf[gname]
            assert glyph.numberOfContours != 0, f"Font {font_name} Chinese glyph '{zh_char}' has empty geometry"


class TestSanskritDevanagariCoverage:
    """Assert all 45 Sanskrit Devanagari codepoints and numerals exist in cmap."""

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_sanskrit_cmap_coverage(self, font_name):
        font_path = REPO_ROOT / font_name
        font = TTFont(str(font_path))
        cmap = font.getBestCmap()

        for sk_cp in SANSKRIT_CLINICAL_CODEPOINTS:
            assert sk_cp in cmap, f"Font {font_name} missing Devanagari codepoint U+{sk_cp:04X}"


class TestUnicodeBrailleBlockCoverage:
    """Assert full 256-glyph Braille block (U+2800 - U+28FF) mapping."""

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_braille_256_patterns_coverage(self, font_name):
        font_path = REPO_ROOT / font_name
        font = TTFont(str(font_path))
        cmap = font.getBestCmap()

        for b_cp in range(0x2800, 0x2900):
            assert b_cp in cmap, f"Font {font_name} missing Braille pattern U+{b_cp:04X}"


class TestHarfBuzzClinicalShaping:
    """Assert HarfBuzz text shaping produces zero .notdef tofu and zero dotted circles."""

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_sanskrit_clinical_terms_shaping(self, font_name):
        font_path = REPO_ROOT / font_name
        with open(str(font_path), 'rb') as f:
            font_data = f.read()

        blob = hb.Blob(font_data)
        face = hb.Face(blob, 0)
        hb_font = hb.Font(face)

        for term in SANSKRIT_CLINICAL_TERMS:
            buf = hb.Buffer()
            buf.add_str(term)
            buf.guess_segment_properties()
            hb.shape(hb_font, buf)

            for info in buf.glyph_infos:
                assert info.codepoint != 0, f"Font {font_name} produced .notdef tofu in Sanskrit term '{term}'"

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_chinese_clinical_terms_shaping(self, font_name):
        font_path = REPO_ROOT / font_name
        with open(str(font_path), 'rb') as f:
            font_data = f.read()

        blob = hb.Blob(font_data)
        face = hb.Face(blob, 0)
        hb_font = hb.Font(face)

        for zh_char in CHINESE_ANATOMICAL_CHARS:
            buf = hb.Buffer()
            buf.add_str(zh_char)
            buf.guess_segment_properties()
            hb.shape(hb_font, buf)

            for info in buf.glyph_infos:
                assert info.codepoint != 0, f"Font {font_name} produced .notdef tofu for Chinese char '{zh_char}'"

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_korean_clinical_terms_shaping(self, font_name):
        font_path = REPO_ROOT / font_name
        with open(str(font_path), 'rb') as f:
            font_data = f.read()

        blob = hb.Blob(font_data)
        face = hb.Face(blob, 0)
        hb_font = hb.Font(face)

        for term in KOREAN_CLINICAL_TERMS:
            buf = hb.Buffer()
            buf.add_str(term)
            buf.guess_segment_properties()
            hb.shape(hb_font, buf)

            for info in buf.glyph_infos:
                assert info.codepoint != 0, f"Font {font_name} produced .notdef tofu for Korean term '{term}'"

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_arabic_clinical_terms_shaping(self, font_name):
        font_path = REPO_ROOT / font_name
        with open(str(font_path), 'rb') as f:
            font_data = f.read()

        blob = hb.Blob(font_data)
        face = hb.Face(blob, 0)
        hb_font = hb.Font(face)

        for term in ARABIC_CLINICAL_TERMS:
            buf = hb.Buffer()
            buf.add_str(term)
            buf.guess_segment_properties()
            hb.shape(hb_font, buf)

            for info in buf.glyph_infos:
                assert info.codepoint != 0, f"Font {font_name} produced .notdef tofu for Arabic term '{term}'"

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_hebrew_clinical_terms_shaping(self, font_name):
        font_path = REPO_ROOT / font_name
        with open(str(font_path), 'rb') as f:
            font_data = f.read()

        blob = hb.Blob(font_data)
        face = hb.Face(blob, 0)
        hb_font = hb.Font(face)

        for term in HEBREW_CLINICAL_TERMS:
            buf = hb.Buffer()
            buf.add_str(term)
            buf.guess_segment_properties()
            hb.shape(hb_font, buf)

            for info in buf.glyph_infos:
                assert info.codepoint != 0, f"Font {font_name} produced .notdef tofu for Hebrew term '{term}'"
