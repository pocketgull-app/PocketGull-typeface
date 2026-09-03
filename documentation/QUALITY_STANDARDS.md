# PocketGull Typographic Quality & Governance Standards (v4.0.0)

## 1. Quality Policy

Every font binary (`.ttf`, `.woff2`) released in the **PocketGull** repository must satisfy 100% of the automated quality gates, OpenType standards, and W3C OTS (OpenType Sanitizer) validation checks. Zero warnings and zero errors are permitted.

---

## 2. The Seven Invariant Quality Pillars

### 1. 1000 UPM Standard Em-Square
- Em-square is locked to **1000 UPM** conforming to ISO/IEC 14496-22 and Google Fonts guidelines.
- Standardized vertical metrics: `sTypoAscender = 780`, `sTypoDescender = -180`, `sTypoLineGap = 100` (`winAscent = 960`, `winDescent = 240`).

### 2. W3C OTS (OpenType Sanitizer) & Word-Alignment Invariants
- **2-Byte Word Alignment**: All glyph offsets in `loca` must satisfy `loca[i] % 2 == 0`.
- **Zero Bit-7 Flags**: TrueType simple glyph flag byte must never set reserved bit 7 (`0x80`), which causes browser decompression rejections.
- **Table Checksums**: All table record checksums must match exact 32-bit modular sums.

### 3. ISMP Life-Critical Disambiguation
- **Slashed Zero (`zero` / `cv08`)**: Differentiates `0` from `O`.
- **Curved Lowercase l (`cv05`)**: Prominent terminal foot outward sweep distinguishes `l` from `1` and `I`.
- **Serifed Capital I (`ss02`)**: Symmetrical horizontal bilobe serifs at cap-height and baseline eliminate ambiguity in laboratory biomarkers (`IL-6`, `IgA`).

### 4. Full 256 Unicode Braille Coverage (`U+2800`–`U+28FF`)
- Conforms to ISO/TR 11548 tactile 8-dot geometry ($180\text{ UPM}$ column spacing, $70\text{ UPM}$ dot radius).
- Zero tofu (`.notdef`) across the entire Braille Patterns block.

### 5. Monospace Pitch Invariant (Fixed 600 UPM)
- `PocketGullMono-Regular` strictly declares `isFixedPitch = 1` in `post` and `panose.bProportion = 9`.
- Every glyph maintains an advance width of exactly **600 UPM**.

### 6. Continuous Filleted Contours ($G^2$ Geometry)
- Smooth filleted radii approximated via cubic Bézier curves prevent pixel clipping at high zoom.
- Clockwise outer contours; counter-clockwise inner counters.

### 7. Thomas Phinney DirectWrite / ClearType Antialiasing (`gasp`)
- Version 1 `gasp` table maps `0xFFFF` to `GASP_DOGRAY` ($0x02$) and `GASP_SYMMETRIC_SMOOTHING` ($0x04$) for subpixel antialiasing across Windows, macOS CoreText, and Linux FreeType.

---

## 3. Automated Validation Execution

To validate the superfamily:
```bash
# In sources/ directory:
python validate_fonts.py
```
