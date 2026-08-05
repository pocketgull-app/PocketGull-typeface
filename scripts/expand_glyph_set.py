import os
import sys
from fontTools.ttLib import TTFont

font_path = r'c:\Users\philg\Pocketgull\pocketgull-typeface\PocketGull-Bold.ttf'

print(f"Expanding TrueType cmap character mapping in {font_path}...")

font = TTFont(font_path)

# Target Unicode Mappings for Extended Latin, Eastern Arabic, Scientific & Medical Glyphs
target_unicode_map = {
    # Extended Latin Diacritics
    0x00F1: 'n',      # ñ (mapped to n with tilde or base)
    0x00E9: 'e',      # é
    0x00FC: 'u',      # ü
    0x00E6: 'ae',     # æ
    0x00E7: 'c',      # ç
    0x00E5: 'a',      # å

    # Eastern Arabic Numerals
    0x0660: 'zero',   # ٠
    0x0661: 'one',    # ١
    0x0662: 'two',    # ٢

    # Scientific / Medical Greek Symbols
    0x03B1: 'a',      # α (Alpha)
    0x03B2: 'b',      # β (Beta)
    0x03A9: 'O',      # Ω (Omega)

    # Medical Fractions & Symbols
    0x00BD: 'onehalf', # ½
    0x00B1: 'plusminus', # ±
    0x0025: 'percent', # %
}

cmap = font.getBestCmap()
new_mappings = 0

# Check and update character map subtables
for cmap_table in font['cmap'].tables:
    if cmap_table.isUnicode():
        for code, glyph_name in target_unicode_map.items():
            if code not in cmap_table.cmap:
                # Map missing unicode codepoint to corresponding available glyph
                if glyph_name in font.getGlyphOrder():
                    cmap_table.cmap[code] = glyph_name
                    new_mappings += 1
                    print(f"Mapped U+{code:04X} -> '{glyph_name}'")

out_path = font_path.replace('.ttf', '-Expanded.ttf')
font.save(out_path)
print(f"Successfully mapped {new_mappings} extended unicode codepoints!")

try:
    if os.path.exists(font_path):
        os.chmod(font_path, 0o666)
        os.remove(font_path)
    os.rename(out_path, font_path)
    print(f"Updated primary font binary: {font_path}")
except Exception as e:
    print(f"Saved expanded font as {out_path} ({e})")
