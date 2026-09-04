# PocketGull Typeface Superfamily (Upstream Release & Foundry Governance)

## Project Overview
PocketGull is an open-source clinical sans-serif, display, and telemetry monospace typeface superfamily engineered by Phil Gear. Originating from tactile felt marker lettering created on physical cardstock for GearArts, PocketGull synthesizes humanist stroke warmth with Louise Sloan 5:1 optotypic legibility and Institute for Safe Medication Practices (ISMP) character disambiguation standards for life-critical healthcare environments.

## The Superfamily & Classification
- **Primary Google Fonts Category**: `SANS_SERIF` (with `DISPLAY` and `MONOSPACE` members).
- **PocketGull Bold** (`PocketGull-Bold.ttf`, wght: 700 / 800): Display titling, Bionic reading anchors, trauma alarms.
- **PocketGull Fineliner** (`PocketGull-Fineliner.ttf`, wght: 400): EHR clinical charts, long-form reading, patient discharge summaries.
- **PocketGull Chiseltip** (`PocketGull-Chiseltip.ttf`, wght: 900): Black calligraphic signage, high-contrast placards.
- **PocketGull Mono** (`PocketGullMono-Regular.ttf`, wght: 400 / 500): Fixed 600 UPM pitch, ICU telemetry, box drawing (`U+2500`–`U+257F`), Powerline chevrons (`uniE0B0`–`uniE0B6`), and sub-cell ECG waveforms.
- **PocketGull VF** (`PocketGull-VF.ttf`, wght: 400–900): Dynamic variable font with continuous weight axis.

---

## 🏛️ The Seven Invariant Quality Pillars

### 1. Standard 1000 UPM Em-Square
- All styles locked to standard 1000 UPM conforming to ISO/IEC 14496-22 and Google Fonts specifications.
- `USE_TYPO_METRICS` flag enabled (`fsSelection` bit 7) across all styles.
- Vertical metrics: `sTypoAscender = 780`, `sTypoDescender = -180`, `sTypoLineGap = 100`, `usWinAscent = 960` (or 1230 for display), `usWinDescent = 240` (or 520 for display).

### 2. TrueType 2-Byte Word-Alignment Invariant (`loca` & `glyf`)
- Every glyph record in `glyf` MUST be padded with a trailing `0x00` byte if odd.
- Every offset in `loca` MUST be an even integer (`loca[i] % 2 == 0`).
- Odd offsets cause unaligned memory access in DirectWrite and Chromium OTS, triggering silent font eviction after ~1 second.

### 3. Reserved Bit-7 Flag Masking
- In the TrueType `glyf` point flags byte, Bit 7 (`0x80` / flag 128) is strictly reserved and MUST be zero (`flag & 0x3F`).
- Pass all curves through quadratic conversion (`Cu2Qu`) before emitting to `TTGlyphPen`.

### 4. ISMP Life-Critical Clinical Disambiguation
- **Slashed Zero (`zero` / `cv08`)**: Mandatory on all dosages (`500 mg`). Optical thinning at contour junctions prevents ink clotting.
- **Curved Lowercase `l` (`cv05`)**: Prominent terminal foot outward sweep eliminates `1 / l / I` collisions.
- **Serifed Capital `I` (`ss02`)**: Bilobe horizontal serifs at cap-height and baseline eliminate ambiguity in biomarkers (`IL-6`, `IgA`).
- **Slashed `Z` (`cv11`)**: Distinct crossbar stroke differentiates `Z` from `2`.

### 5. Full 256 Unicode Braille Coverage (`U+2800`–`U+28FF`)
- Full ISO/TR 11548 tactile 8-dot geometry across all styles. Zero `.notdef` across the block.

### 6. Monospace Pitch Invariant (Fixed 600 UPM)
- `PocketGullMono-Regular` strictly declares `isFixedPitch = 1` in `post` and `OS/2.panose.bProportion = 9`.
- Every single glyph maintains an advance width of exactly 600 UPM.

### 7. DirectWrite / ClearType Antialiasing (`gasp`)
- Version 1 `gasp` table mapping `0xFFFF` to `GASP_DOGRAY` (0x02) and `GASP_SYMMETRIC_SMOOTHING` (0x04).

---

## 🚀 Google Fonts Upstream Packaging & Launch Standards

Every release must conform to Google Fonts onboarding standards:
- **Category**: `SANS_SERIF` with classifications `["SANS_SERIF", "DISPLAY"]`.
- **Minimalist Versioning (`nameID 5`)**: Must strictly follow Google Fonts Option 5: `Version 3.000; The PocketGull Project Authors; OFL 1.1`. `head.fontRevision` locked to exact float `3.0`.
- **Copyright & License**: `nameID 0` matches `OFL.txt` line 1 character-for-character (`Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-typeface)`).
- **Zero Reserved Font Names (RFN)**: SIL Open Font License 1.1 with no RFN restriction.
- **Designer Profile Dossier**: `documentation/designer/philgear/` containing valid `info.pb`, `bio.html` (with the Gentle Healer limerick), and `philgear.png` (300x300).
- **Automated Upstream Sync**: `upstream.yaml` configured for `gftools packager`.
- **Brotli Compression**: WOFF2 binaries compressed at Brotli quality 11.

---

## 🛠️ Mandatory Pre-Flight Verification Chain

Before approving any commit or release:
```powershell
# 1. Forensic W3C OTS & word-alignment audit (Dart 3.11)
dart run tool/pocketgull_foundry.dart audit

# 2. Python Google Fonts pre-flight specification validator
python sources/validate_fonts.py

# 3. Synchronize verified binaries to web app mirror (if app is present)
dart run tool/pocketgull_foundry.dart sync
```
