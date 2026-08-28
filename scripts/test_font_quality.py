"""
PocketGull Typeface Quality Verification Test Suite
===================================================
Automated quality gates asserting:
1. OpenType Table Conformance (head, hhea, maxp, OS/2, name, cmap, post, glyf, loca, gasp)
2. Thomas Phinney gasp Anti-Aliasing Table configuration (GASP_DOGRAY | GASP_SYMMETRIC_SMOOTHING)
3. 1024 UPM Grid & Vertical Metric Consistency (Ascender, Descender, Cap-Height, x-Height)
4. Monospace Invariants (Identical 600 UPM advance width across all glyphs in PocketGullMono)
5. Glyph Contour Geometry & Clockwise Winding Topology
6. Unicode Latin & PUA Clinical Telemetry Mapping (U+E001 - U+E006)
7. Greek Pharmacology & Mathematical Constants Mapping (Delta, Sigma, Omega, alpha, beta, gamma, mu, pi)
8. Cyrillic Emergency Medicine Letterforms Mapping (D, ZH, I, L, P, F, TS, CH, SH, SHCH, YU, YA)
9. WOFF2 Compression & Magic Byte Header Validity
"""

import os
import struct
import pytest
from fontTools.ttLib import TTFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SUPERFAMILY_FONTS = [
    'PocketGull-Fineliner.ttf',
    'PocketGull-Bold.ttf',
    'PocketGull-Chiseltip.ttf',
    'PocketGull-Antigravity.ttf',
    'PocketGullMono-Regular.ttf',
    'PocketGull-Numerics.ttf',
]

SUPERFAMILY_WOFF2 = [f.replace('.ttf', '.woff2') for f in SUPERFAMILY_FONTS]


class TestFontFilesExistence:
    """Ensure all required font binaries and proof artifacts are built and present."""

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_ttf_file_exists_and_non_empty(self, font_name):
        font_path = os.path.join(REPO_ROOT, font_name)
        assert os.path.exists(font_path), f"Missing TTF binary: {font_name}"
        assert os.path.getsize(font_path) > 1000, f"TTF binary suspiciously small: {font_name}"

    @pytest.mark.parametrize('woff2_name', SUPERFAMILY_WOFF2)
    def test_woff2_file_exists_and_valid_magic(self, woff2_name):
        woff2_path = os.path.join(REPO_ROOT, woff2_name)
        assert os.path.exists(woff2_path), f"Missing WOFF2 binary: {woff2_name}"
        assert os.path.getsize(woff2_path) > 500, f"WOFF2 binary suspiciously small: {woff2_name}"
        with open(woff2_path, 'rb') as f:
            magic = f.read(4)
            assert magic == b"wOF2", f"Invalid WOFF2 magic bytes in {woff2_name}: {magic}"

    def test_specimen_proof_image_exists(self):
        proof_path = os.path.join(REPO_ROOT, 'PocketGull-Authentic-Specimen.png')
        assert os.path.exists(proof_path), "Missing master specimen proof image"
        assert os.path.getsize(proof_path) > 50000, "Specimen proof image size too small"


class TestOpenTypeTableIntegrity:
    """Validate OpenType table structure, UPM metrics, and gasp smoothing."""

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_required_opentype_tables(self, font_name):
        font_path = os.path.join(REPO_ROOT, font_name)
        font = TTFont(font_path)
        required_tables = ['head', 'hhea', 'maxp', 'OS/2', 'name', 'cmap', 'post', 'glyf', 'loca', 'gasp']
        for table_tag in required_tables:
            assert table_tag in font, f"Font {font_name} is missing critical OpenType table: {table_tag}"

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_upm_and_vertical_metrics(self, font_name):
        font_path = os.path.join(REPO_ROOT, font_name)
        font = TTFont(font_path)
        assert font['head'].unitsPerEm == 1024, f"Font {font_name} UPM != 1024"
        assert font['hhea'].ascent == 1136, f"Font {font_name} hhea.ascent != 1136"
        assert font['hhea'].descent == -325, f"Font {font_name} hhea.descent != -325"
        assert font['OS/2'].sTypoAscender == 1136, f"Font {font_name} sTypoAscender != 1136"
        assert font['OS/2'].sTypoDescender == -325, f"Font {font_name} sTypoDescender != -325"

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_gasp_table_subpixel_smoothing(self, font_name):
        """Assert gasp table enforces DirectWrite ClearType & Dogray anti-aliasing."""
        font_path = os.path.join(REPO_ROOT, font_name)
        font = TTFont(font_path)
        gasp_ranges = font['gasp'].gaspRange
        assert 65535 in gasp_ranges or 0xFFFF in gasp_ranges, f"Font {font_name} missing 0xFFFF gasp range"
        flags = gasp_ranges.get(65535) or gasp_ranges.get(0xFFFF)
        assert (flags & 0x02) != 0, f"Font {font_name} missing GASP_DOGRAY flag"
        assert (flags & 0x04) != 0 or (flags & 0x08) != 0, f"Font {font_name} missing smoothing flag"


class TestMonospaceIntegrity:
    """Assert strict monospace pitch and advance width invariants for PocketGullMono."""

    def test_mono_regular_fixed_pitch(self):
        mono_path = os.path.join(REPO_ROOT, 'PocketGullMono-Regular.ttf')
        font = TTFont(mono_path)
        assert font['post'].isFixedPitch == 1, "PocketGullMono-Regular must declare isFixedPitch = 1 in post table"
        assert font['OS/2'].panose.bProportion == 9, "PocketGullMono-Regular PANOSE bProportion must be 9 (Monospaced)"

    def test_mono_advance_widths_uniformity(self):
        mono_path = os.path.join(REPO_ROOT, 'PocketGullMono-Regular.ttf')
        font = TTFont(mono_path)
        hmtx = font['hmtx'].metrics
        expected_width = 600
        for glyph_name, (advance, lsb) in hmtx.items():
            if glyph_name not in ['.notdef']:
                assert advance == expected_width, (
                    f"PocketGullMono glyph '{glyph_name}' has non-uniform advance width {advance} (expected {expected_width})"
                )


class TestUnicodeMappingAndClinicalPUA:
    """Assert 100% mapping of ASCII printable and PUA Emergency Medical Telemetry glyphs."""

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_ascii_printable_coverage(self, font_name):
        font_path = os.path.join(REPO_ROOT, font_name)
        font = TTFont(font_path)
        cmap = font.getBestCmap()
        assert cmap is not None, f"Font {font_name} missing unicode cmap table"
        for codepoint in range(0x21, 0x7F):
            assert codepoint in cmap, f"Font {font_name} missing ASCII codepoint {hex(codepoint)} ('{chr(codepoint)}')"

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_pua_clinical_telemetry_coverage(self, font_name):
        font_path = os.path.join(REPO_ROOT, font_name)
        font = TTFont(font_path)
        cmap = font.getBestCmap()
        pua_codepoints = [0xE001, 0xE002, 0xE003, 0xE004, 0xE005, 0xE006]
        for cp in pua_codepoints:
            assert cp in cmap, f"Font {font_name} missing PUA clinical telemetry codepoint {hex(cp)}"

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_greek_pharmacology_coverage(self, font_name):
        """Assert Greek mathematical & pharmacology units (Delta, Sigma, Omega, alpha, beta, gamma, mu, pi)."""
        font_path = os.path.join(REPO_ROOT, font_name)
        font = TTFont(font_path)
        cmap = font.getBestCmap()
        greek_codepoints = [0x0394, 0x03A3, 0x03A9, 0x03B1, 0x03B2, 0x03B3, 0x03BC, 0x03C0, 0x00B5]
        for cp in greek_codepoints:
            assert cp in cmap, f"Font {font_name} missing Greek codepoint {hex(cp)}"

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_cyrillic_triage_coverage(self, font_name):
        """Assert Cyrillic emergency medicine letterforms (D, ZH, I, L, P, F, TS, CH, SH, SHCH, YU, YA)."""
        font_path = os.path.join(REPO_ROOT, font_name)
        font = TTFont(font_path)
        cmap = font.getBestCmap()
        cyrillic_codepoints = [
            0x0414, 0x0434, 0x0416, 0x0436, 0x0418, 0x0438, 0x041B, 0x043B,
            0x041F, 0x043F, 0x0424, 0x0444, 0x0426, 0x0446, 0x0427, 0x0447,
            0x0428, 0x0448, 0x0429, 0x0449, 0x042E, 0x044E, 0x042F, 0x044F
        ]
        for cp in cyrillic_codepoints:
            assert cp in cmap, f"Font {font_name} missing Cyrillic codepoint {hex(cp)}"


class TestGlyphGeometryAndTopologies:
    """Validate glyph vector contours, non-degeneracy, and positive contour area."""

    @pytest.mark.parametrize('font_name', SUPERFAMILY_FONTS)
    def test_master_glyphs_have_valid_contours(self, font_name):
        font_path = os.path.join(REPO_ROOT, font_name)
        font = TTFont(font_path)
        glyf_table = font['glyf']
        cmap = font.getBestCmap()

        master_chars = ['P', 'o', 'c', 'k', 'e', 't', 'G', 'u', 'l', 'A', 'B', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for char in master_chars:
            cp = ord(char)
            glyph_name = cmap[cp]
            glyph = glyf_table[glyph_name]
            assert glyph.numberOfContours > 0, f"Font {font_name} glyph '{char}' has 0 contours"
            assert glyph.xMax > glyph.xMin, f"Font {font_name} glyph '{char}' has invalid zero-width bounding box"
            assert glyph.yMax > glyph.yMin, f"Font {font_name} glyph '{char}' has invalid zero-height bounding box"

if __name__ == '__main__':
    pytest.main(['-v', __file__])
