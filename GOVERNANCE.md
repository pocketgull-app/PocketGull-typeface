# Project Governance & Typographic Oversight Policy

**PocketGull Typeface Superfamily**  
*Open Source Governance, Clinical & Ophthalmological Typography Review Board, and Release Protocol*

---

## 🏛️ 1. Governance Principles

PocketGull Typeface Superfamily is an open-source medical and ophthalmological typography project developed by **PocketGull LLC** in collaboration with clinical researchers, optometrists, vision scientists, and type designers.

Our governance model ensures:
1. **Ophthalmological Rigor & Evidence Grounding**: All letterform metrics, stroke contrasts, x-height ratios, and counter spaces must be grounded in peer-reviewed vision science literature (Louise Sloan 5:1 acuity, Hermann Bouma crowding coefficients, ISO/TR 11548 Braille dimensions, DIN 1450 legibility standards).
2. **Deterministic Safety Precedence**: Stylistic flourishes never compromise clinical readability or the Institute for Safe Medication Practices (ISMP) zero-error character disambiguation rules.
3. **Radical Transparency & Libre Licensing**: 100% open-source licensing under the **SIL Open Font License 1.1 (OFL-1.1)**, open vector sources (UFO3 / Glyphs), reproducible build toolchains (gftools-builder, ontmake), and public issue tracking.
4. **Binary Integrity & Memory Safety**: Zero W3C OpenType Sanitizer (OTS) violations, 2-byte word boundary alignment, and hermetic CI validation.

---

## 👥 2. Roles & Responsibilities

### 2.1 Lead Systems Architect & Benevolent Dictator for Now (BDFN)
* **Lead Architect**: **Phil Gear** ([ORCID: 0009-0008-1372-5381](https://orcid.org/0009-0008-1372-5381))
* Retains final architectural, licensing, and security decision-making authority over core repository branches, font naming, and cryptographic release seals.

### 2.2 Typographic & Clinical Review Board (TCRB)
* Composed of vision researchers, clinicians, ophthalmologists, and type engineers.
* Reviews all Pull Requests touching:
  * ISMP high-risk medication safety glyphs (cv08 slashed zero, cv05 curved l, ss02 serifed I).
  * Unicode Braille patterns (U+2800..U+28FF) and tactile embossing metrics.
  * Dyslexia-conscious baseline weighting and saccadic reading anchors.
  * Monospace 600 UPM advance metrics and ICU vitals table alignment.
  * Photobiomodulation (670nm PBM) optical contrast calibration.

### 2.3 Core Maintainers
* Review daily pull requests, maintain CI/CD pipelines, and enforce pre-flight test suites (alidate_fonts.py, ontbakery check-googlefonts).

---

## 📜 3. Decision-Making & RFC Process

Significant architectural, metric, or glyph set changes follow a lightweight **Request for Comments (RFC)** process:

1. **RFC Proposal**: Contributor opens an issue with the [TYPOGRAPHY-RFC] template or starts a GitHub Discussion.
2. **Review Period**: 7-day public review period for community feedback and clinical verification.
3. **Proof-of-Work Verification**: Implementation must provide 100% passing tests via sources/validate_fonts.py and Fontbakery (0 FAILs, 0 FATALs).
4. **Consensus & Merge**: Merged upon approval by the Lead Architect.

---

## 🛡️ 4. Emergency Patch Protocol (STAT Override)

In the event of an identified clinical safety hazard, OTS memory violation, or critical table corruption:
1. Maintainers may push an emergency fix directly to a hotfix branch on main.
2. The hotfix must satisfy the mandatory OTS sanitizer and alidate_fonts.py test suites.
3. A post-mortem incident report will be published in SECURITY.md within 48 hours.

---

<p align="center">
  <sub>© 2026 PocketGull LLC & Phil Gear. Distributed under the SIL Open Font License 1.1.</sub>
</p>
