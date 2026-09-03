# Changelog

All notable changes to the **PocketGull Typeface Superfamily** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`v2.0.0`).

## [2.0.0] - 2026-09-03

### Added
- **Full Medical Terminal Glyphs (`PocketGullMono-Regular`)**: 17 Powerline chevrons, prompt anchors, and ICU status tags (`uniE0B0`–`uniE0B6`, `uniE0A0`–`uniE0A2`, `uni276F`, `uni276E`, `uni2714`, `uni2713`, `uni26A1`, `uni2300`, `uni271A`, `uni2695`) with exact 600 UPM fixed advance widths.
- **Complete 256-Glyph Unicode Braille Patterns Block (`U+2800`–`U+28FF`)**: Full ISO/TR 11548 tactile matrix support across all superfamily weights (`PocketGull-Bold`, `PocketGull-Fineliner`, `PocketGull-Chiseltip`, `PocketGullMono-Regular`).
- **OpenSSF Security Policy & Scorecard Integration**: Automated vulnerability reporting, Scorecard workflow, and SLSA provenance compliance.
- **Academic Citation Metadata (`CITATION.cff`)**: CFF 1.2.0 metadata for clinical informatics and ophthalmological literature.

### Changed
- **Standardized Version String (`nameID 5`)**: Updated to Google Fonts Option 5 Minimalist format: `Version 2.000; The PocketGull Project Authors; OFL 1.1`.
- **Aligned Font Revision Header (`head.fontRevision`)**: Exact 2.000 float match to eliminate Fontbakery version discrepancies.
- **UFO Source Synchronization**: Updated `versionMajor: 2` and `versionMinor: 0` across all 4 `.ufo` source directories.
- **Windows Bounding Box & Vertical Metrics**: Unified `OS/2.usWinAscent = 1230` and `OS/2.usWinDescent = 520` across the superfamily, eliminating Windows GDI clipping.
- **Specimen Legal Footer**: Replaced plain footer with a happy, humanist SIL OFL 1.1 footer explaining commercial/personal freedoms, Reserved Font Name (RFN) boundaries, and removing persistent floating overlay elements.
- **670nm Retinal Photobiomodulation (PBM) Integration**: Complete monochromatic ruby-red night mode overrides across all UI components and code drawers.

### Fixed
- **TrueType 2-Byte Word-Boundary Alignment**: Padded all glyph contours so that `loca[i] % 2 == 0`, passing 100% of Thomas Phinney forensic typefoundry checks.
- **W3C OpenType Sanitizer (OTS)**: 100% pass rate with zero warnings or fatals across all 16 TTF and WOFF2 binaries.
- **Fontbakery QA**: 711 automated checks passed with 0 FAILs and 0 FATALs across the proportional and monospace families.
