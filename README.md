<div align="center">

# 🖋️ PocketGull Typeface Superfamily
### *The Cellular Typefoundry: Tactile Felt-Tip Marker Expression Meets Clinical Telemetry Precision*

[![OFL 1.1 License](https://img.shields.io/badge/License-SIL_OFL_1.1-orange.svg)](OFL.txt)
[![Google Fonts Submission](https://img.shields.io/badge/Google_Fonts_PR-%2310875-4285F4.svg?logo=google)](https://github.com/google/fonts/pull/10875)
[![FontBakery QA](https://img.shields.io/badge/FontBakery_QA-144_Pass_%7C_0_Fail-brightgreen.svg)](https://github.com/google/fonts/pull/10875)
[![Vector Precision](https://img.shields.io/badge/Vector_Grid-1024_UPM_%7C_G2_Continuity-teal.svg)](https://github.com/pocketgull-app/PocketGull-typeface)
[![Clinical PUA Icons](https://img.shields.io/badge/Clinical_PUA-E001--E006-blue.svg)](https://github.com/pocketgull-app/PocketGull-typeface)
[![WCAG 2.1 AAA](https://img.shields.io/badge/WCAG_2.1_AAA-12.8%3A1_Contrast-emerald.svg)](https://typeface.pocketgull.app)

<br/>

<a href="https://typeface.pocketgull.app" target="_blank">
  <img src="assets/pocketgull_cellular_typefoundry.jpg" alt="PocketGull: The Cellular Typefoundry Master Specimen" width="100%" style="border-radius: 16px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); max-width: 820px;" />
</a>

<br/><br/>

### 🌐 [Live Interactive Type Foundry](https://typeface.pocketgull.app) &nbsp;•&nbsp; 📦 [Google Fonts Upstream PR #10875](https://github.com/google/fonts/pull/10875) &nbsp;•&nbsp; 🔬 [Live Interactive Specimen](https://pocketgull-app.github.io/PocketGull-typeface)

</div>

---

## 📖 Design Vision & Overview

**PocketGull** is an open-source, mathematical vector typeface superfamily engineered to bridge two disparate worlds:
1. **Warm Humanist Expression**: The organic stroke energy, tactile warmth, and handcrafted papercraft quilling of a felt-tip marker.
2. **Mission-Critical Precision**: Zero-error optical clarity calibrated for ICU bedside monitors, emergency 911 dispatch HUDs, bystander CPR coaching, and high-density electronic health record (EHR) charts.

Built under the discipline of **Dieter Rams’ 10 Principles of Good Design** (*Good design is honest, unobtrusive, and as little design as possible*), every glyph is synthesized on a standardized **1024 UPM grid** ($CAP=720, XH=480, BL=0, DSC=-180$) with continuous G2 Bézier extrema, strict TrueType winding rules (clockwise outer contours, counter-clockwise inner counters), and 100% Adobe Glyph List (AGL) compliance.

---

## 🔬 The Cellular Typefoundry: Biophysical Telemetry & Optotypic Standards

PocketGull is engineered for medical, biochemical, and physiological telemetry display interfaces:

* **Optotypic Acuity (Snellen 20/20 & LogMAR 0.0)**: Stroke geometries maintain a $5\text{-arcminute}$ visual angle with $1\text{-arcminute}$ critical detail resolution at standard $50\text{–}70\text{ cm}$ clinical workstation distances.
* **Biophysical Telemetry Expressions**:
  $$\text{ATP} + \text{H}_2\text{O} \longrightarrow \text{ADP} + \text{P}_i$$
  $$[\text{K}^+]_{\text{out}} = 4.5\text{ mM} \quad\Big|\quad [\text{K}^+]_{\text{in}} = 140\text{ mM}$$
  $$\text{SpO}_2\text{ 99\%} \;\cdot\; 72\text{ bpm} \;\cdot\; \Delta\Psi_m = -140\text{ mV} \;\cdot\; \text{ATP Synthase } 600\text{ RPM} \;\cdot\; [\text{Ca}^{2+}]_i = 100\text{ nM}$$

---

## 🫀 Clinical Telemetry & Emergency PUA Suite (`\uE001`–`\uE006`)

PocketGull embeds bespoke emergency telemetry indicators directly into the font’s **Private Use Area (PUA)**. This enables web, mobile, and embedded UI systems to render high-contrast medical glyphs inline with text without external SVGs, image assets, or network latency:

| Icon | Unicode | Glyph Name | Clinical Domain | Live String Example |
| :---: | :---: | :--- | :--- | :--- |
| **`🫀`** | `\uE001` | `icon_heart_ecg` | Cardiac QRS rhythm & pulse rate | `\uE001 HEART_RATE: 72 bpm` |
| **`💧`** | `\uE002` | `icon_spo2` | Blood oxygen saturation ($SpO_2$) | `\uE002 SPO2: 98%` |
| **`💎`** | `\uE003` | `icon_glucose` | Hexagonal CGM continuous glucose sensor | `\uE003 GLUCOSE: 104 mg/dL` |
| **`⚡`** | `\uE004` | `icon_aed_shock` | High-voltage AED defibrillator armed alert | `\uE004 AED: ARMED & READY` |
| **`🎯`** | `\uE005` | `icon_beacon_gps` | 911 radio telemetry & concentric radar beacon | `\uE005 DISPATCH: 911 ACTIVE` |
| **`🔊`** | `\uE006` | `icon_cpr_coach` | Real-time 110 BPM CPR compression metronome | `\uE006 CPR: 110 BPM (30:2)` |

---

## 🖋️ Superfamily Instances & Weights

The superfamily spans **7 purpose-built instances**, offering flexible weight distribution and optical sizing from compact tabular numerals to expressive editorial headers:

| Font Binary | Weight / Style | Advance / Metric | Primary Application |
| :--- | :---: | :---: | :--- |
| **`PocketGull-VF.ttf` / `.woff2`** | `100` $\rightarrow$ `900` | Proportional | **Universal Variable Font**: Continuous `wght` (100–900), `opsz` (8–72), and `slnt` axes. |
| **`PocketGull-Fineliner.ttf`** | Regular (`400`) | Proportional | **Dense EHR & Lab Tables**: High-legibility body text, medication dosages, and clinical notes. |
| **`PocketGull-Bold.ttf`** | Bold (`800`) | Proportional | **Master Display**: Primary brand identity, section headers, and critical triage callouts. |
| **`PocketGull-Chiseltip.ttf`** | Black (`900`) | Proportional | **Signage & Emergency Placards**: Bold $45^\circ$ geometric chamfers for maximum impact. |
| **`PocketGull-Antigravity.ttf`** | Heavy (`800`) | Proportional | **Dynamic HUD Display**: High-contrast user interface titles and telemetry badges. |
| **`PocketGullMono-Regular.ttf`** | Medium (`500`) | Fixed `600 UPM` | **Vital Feeds & Code**: Strict tabular alignment for streaming ECG, timestamps, and numbers. |
| **`PocketGull-Numerics.ttf`** | Medium (`500`) | Proportional | **Dials & Timers**: Golden ratio ($\phi$) proportions for high-speed numerical recognition. |

---

## 📐 Engineering & Typographic Standards

* **Grid Resolution**: Standardized `1024 UPM` (Units per Em).
* **Vertical Metrics**: Cap-Height: `720 UPM` &nbsp;•&nbsp; x-Height: `480 UPM` &nbsp;•&nbsp; Baseline: `0 UPM` &nbsp;•&nbsp; Descender: `-180 UPM`.
* **Stem Width Proportions**: Bold (`110 UPM`), Regular (`65 UPM`), Hairline/Crossbar (`45 UPM`).
* **Optical Overshoot**: `14 UPM` on curved vertices ($O, C, S, 8$) to preserve perceptual size equilibrium.
* **Optical Kerning**: Embedded OpenType `GPOS` pair-spacing table covering 1,800+ kerning combinations (`AV`, `AW`, `Ta`, `To`, `We`, `Yo`, `PA`, `FA`, `LT`).
* **Disambiguation (ISMP Standard)**: Clear visual separation between slashed zero (`0` via `cv08`), curved lowercase `l` (`cv05`), serifed uppercase `I` (`ss02`), and hooked numeral `1`.
* **Contour Winding**: Clockwise outer contours and Counter-Clockwise inner counters for artifact-free rendering in DirectWrite, FreeType, and CoreText.
* **Binary Quality**: 100% **OpenType Sanitizer (OTS)** pass with zero reserved-flag errors.

---

## 🚀 Quickstart & Web Integration

### 1. CSS `@font-face` Setup
Add the `@font-face` definitions to your web or application stylesheet:

```css
/* PocketGull Variable Font (Body & Display) */
@font-face {
  font-family: 'PocketGull';
  src: url('/fonts/PocketGull-VF.woff2') format('woff2-variations'),
       url('/fonts/PocketGull-Bold.woff2') format('woff2');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}

/* PocketGull Monospace (Clinical Telemetry & Vitals) */
@font-face {
  font-family: 'PocketGull Mono';
  src: url('/fonts/PocketGullMono-Regular.woff2') format('woff2');
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}
```

### 2. Enabling ISMP Disambiguation in CSS
```css
.clinical-telemetry {
  font-family: 'PocketGull', sans-serif;
  font-feature-settings: "cv08" 1, /* Slashed Zero */
                         "cv05" 1, /* Curved Lowercase l */
                         "ss02" 1, /* Serifed Capital I */
                         "tnum" 1; /* Tabular Figures */
}
```

---

## 📜 License

PocketGull is distributed under the [SIL Open Font License, Version 1.1](OFL.txt).  
Copyright (c) 2026 The PocketGull Project Authors (https://github.com/philgear/pocketgull-typeface).
