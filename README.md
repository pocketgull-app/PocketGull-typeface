<div align="center">

# 🕊️ PocketGull Typeface Superfamily

[![OFL 1.1 License](https://img.shields.io/badge/License-SIL_OFL_1.1-orange.svg)](OFL.txt)
[![SemVer 2.0.0](https://img.shields.io/badge/SemVer-2.0.0-blue.svg)](CHANGELOG.md)
[![W3C OTS Validated](https://img.shields.io/badge/W3C_OTS-100%25_Valid-emerald.svg)](https://github.com/googlefonts/ots)
[![Fontbakery QA](https://img.shields.io/badge/Fontbakery-711%2F711_Passed-brightgreen.svg)](https://github.com/googlefonts/fontbakery)

<br/>

### 🌐 [Live Interactive Specimen](https://typeface.pocketgull.app) &nbsp;•&nbsp; 📦 [UFO Sources](sources/) &nbsp;•&nbsp; 📄 [SIL OFL 1.1 License](OFL.txt)

</div>

<div align="center">

<img src="documentation/images/pocketgull_device_hero.jpg" alt="PocketGull Telemetry Device & Optotypic Interface" width="100%" />

<br/><br/>

<table>
  <tr>
    <td width="50%" align="center">
      <img src="documentation/images/pocketgull_synaptic_specimen_light.png" alt="PocketGull Synaptic Codex - Light Mode" width="100%" />
    </td>
    <td width="50%" align="center">
      <img src="documentation/images/pocketgull_synaptic_specimen_dark.png" alt="PocketGull Synaptic Codex - Dark Mode" width="100%" />
    </td>
  </tr>
</table>

</div>

**PocketGull** is an open-source clinical sans-serif, display, and telemetry monospace typeface superfamily designed by Phil Gear. Engineered to bridge tactile humanist warmth with zero-error clinical precision, PocketGull solves a life-critical challenge in medical software: eliminating medication administration errors while providing an organic, fatigue-resistant texture that soothes the reader's eyes during 12-hour hospital shifts.

Originating from spontaneous felt marker lettering created on physical cardstock, PocketGull synthesizes organic stroke dynamism with the Institute for Safe Medication Practices (ISMP) character disambiguation rules and Louise Sloan 5:1 optotypic legibility standards.

---

## 🗂️ Superfamily Styles & Weights

PocketGull is engineered on a standardized 1000 UPM grid across 4 coordinated styles:

| Style | PostScript Name | Weight | Advance Metric | Primary Use Case |
| :--- | :--- | :---: | :---: | :--- |
| **PocketGull Bold** | `PocketGull-Bold` | 700 / 800 | Proportional | Prescription markers, Bionic reading anchors, alarms |
| **PocketGull Fineliner** | `PocketGull-Fineliner` | 400 | Proportional | Long-form clinical notes, EHR charts, patient leaflets |
| **PocketGull Chiseltip** | `PocketGull-Chiseltip` | 900 | Proportional | Expressive signage, trauma alerts, high-contrast placards |
| **PocketGull Mono** | `PocketGullMono-Regular` | 400 / 500 | Fixed 600 UPM | ICU telemetry, tabular vitals, gapless box drawing |

---

## 🔬 Core Innovations

* **🫀 ISMP & FDA Disambiguation**: Native slashed zero (`cv08`), curved lowercase `l` (`cv05`), serifed uppercase `I` (`ss02`), and tabular numbers (`tnum`).
* **⠃ 256 Unicode Braille Block (`U+2800`–`U+28FF`)**: Full ISO/TR 11548 tactile matrix for blister packs and pharmaceutical accessibility.
* **👁️ Sloan 5:1 Optotypes & Bouma Spacing**: Calibrated for LogMAR 0.0 acuity and peripheral anti-crowding at 50–70 cm reading distance.
* **💻 ICU Medical Terminal & Oh My Posh**: Gapless box drawing (`U+2500`–`U+257F`) and sub-cell ECG waveforms with native prompt theme (`pocketgull-ophthalmic.omp.json`).

---

## 🚀 Quickstart

Link via CSS:
```html
<link rel="stylesheet" href="https://typeface.pocketgull.app/fonts.css">
```

Enable clinical dosage disambiguation:
```css
.clinical-dosage-safe {
  font-family: 'PocketGull', sans-serif;
  font-feature-settings: "zero" 1, "cv08" 1, "cv05" 1, "ss02" 1, "tnum" 1;
}
```

---

## 📚 Documentation & Specifications

* 📖 **[Design Specification](documentation/DESIGN_SPECIFICATION.md)** — Architectural guidelines and design history
* 🔬 **[Scientific Bibliography](documentation/BIBLIOGRAPHY.md)** — Peer-reviewed ophthalmology & vision science literature
* 🏥 **[Workstation Authorization Memo](documentation/WORKSTATION_AUTHORIZATION_LETTER.md)** — Institutional deployment request for CMIOs and IT
* 🛠️ **[Building from UFO Sources](sources/)** — Compiler setup with `fontmake` and `gftools-builder`
* 🛡️ **[Security Policy](SECURITY.md)** — OpenSSF vulnerability disclosure and W3C OTS verification
* 📝 **[Changelog](CHANGELOG.md)** — Semantic Versioning history (SemVer 2.0.0)

---

## 📜 License & Copyright

PocketGull is distributed under the **[SIL Open Font License, Version 1.1](OFL.txt)**.  
Free for personal, academic, and commercial use.

**Copyright (c) 2026 The PocketGull Project Authors** ([GitHub Repository](https://github.com/pocketgull-app/pocketgull-typeface)).  
*Rooted in empirical science. Engineered for life. 🕊️*
