# PocketGull Typographic Quality & Governance Standards

## 1. Quality Policy

Every font binary (`.ttf`, `.woff2`, `.vf`) committed to the **PocketGull** repository must satisfy 100% of the automated quality gates defined in `scripts/test_font_quality.py`. No commit or pull request may merge if any typographic invariant fails.

---

## 2. The Six Invariant Quality Pillars

### 1. OpenType Table Conformance
- All font binaries must provide valid `head`, `hhea`, `maxp`, `OS/2`, `name`, `cmap`, `post`, `glyf`, `loca`, and `gasp` tables.
- Em-square is locked to **1024 UPM**.
- Standardized vertical metrics: `sTypoAscender = 1136`, `sTypoDescender = -325`, `sTypoLineGap = 100` to prevent diacritic clipping across multilingual rendering.

### 2. Thomas Phinney Screen Antialiasing (`gasp`)
- All TrueType binaries must inject a version 1 `gasp` table mapping `0xFFFF` (all point sizes up to 65,535 pt) to:
  - `GASP_DOGRAY` ($0x02$)
  - `GASP_SYMMETRIC_SMOOTHING` ($0x04$) / `GASP_SYMMETRIC_GRIDFIT` ($0x08$)
- This ensures subpixel ClearType / DirectWrite antialiasing on Windows, macOS CoreText, and Linux FreeType without harsh staircase pixelation.

### 3. Continuous Filleted Contour Geometry ($G^2$ Continuity)
- All stem terminations, crossbar ends, diagonal tips, and spurs must feature smooth filleted radii ($r = 14\text{–}18\text{ UPM}$) approximated via standard cubic Bézier curves ($k = 0.55228475$).
- Hard $90^\circ$ box chops are prohibited on outer glyph contours.

### 4. Monospace Mathematical Pitch Invariants
- `PocketGullMono-Regular` must declare `isFixedPitch = 1` in the `post` table and `panose.bProportion = 9` (Monospaced).
- **Every glyph** in `PocketGullMono` must have an advance width of exactly **600 UPM**, centered horizontally within the advance cell.

### 5. Unicode Latin & Universal Clinical Telemetry (PUA)
- Complete coverage of Basic Latin (U+0020 – U+007E).
- Dedicated Private Use Area (PUA) glyphs for emergency clinical telemetry:
  - `\uE001`: Cardiac Rhythm / ECG Pulse (`icon_heart_ecg`)
  - `\uE002`: Blood Oxygen Saturation Teardrop (`icon_spo2`)
  - `\uE003`: Blood Glucose Level Drop (`icon_glucose`)
  - `\uE004`: AED Defibrillator Shock Ready (`icon_aed_shock`)
  - `\uE005`: GPS Emergency Beacon Crosshair (`icon_beacon_gps`)
  - `\uE006`: CPR Compression Coach / Oxygen Flow (`icon_cpr_coach`)

### 6. WOFF2 Compression & Web Readiness
- Every TrueType binary has a companion `.woff2` file compressed with Brotli and verified with the `wOF2` magic byte header.

---

## 3. Automated CI/CD Execution

The continuous integration pipeline (`.github/workflows/font-quality.yml`) runs on every push and pull request:
```bash
# 1. Compile Superfamily
python scripts/compile_precision_superfamily.py

# 2. Run Quality Gates (51 Assertions)
pytest scripts/test_font_quality.py -v

# 3. Generate Visual Proof Artifacts
python scripts/render_actual_font_proof.py
```
