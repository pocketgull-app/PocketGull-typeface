---
name: caslon-type-design
description: Caslon Type Design Department for the PocketGull Typeface sandbox. Governs William Caslon-inspired typography engineering, leading, optical kerning, baseline grid alignment, and serif/sans font family synthesis.
---

# 🔤 PocketGull Type Design Department (Caslon Sandbox Agent Suite)

This skill defines the autonomous **Type Design Department** within the `pocketgull-typeface` sandbox repository. It is modeled on **William Caslon (1692–1766)** and his typefoundry collaborators: **William Caslon II**, **Thomas Cottrell**, and **Joseph Jackson**.

> *"When in doubt, use Caslon."* — William Caslon

---

## 🏛️ Type Design Department Agents

### 1. William Caslon (Master Type Founder & Proportional Rhythm)
* **Responsibility**: Organic warmth, proportion, and vertical leading.
* **Standards**:
  * **X-Height Ratio**: $0.48 - 0.52 \times \text{Cap Height}$.
  * **Proportional Leading**: Line height calibrated to $1.55 - 1.65 \times \text{font-size}$ for long-form reading, $1.25\times$ for display headers.
  * **Baseline Harmony**: Strict vertical grid alignment.

### 2. Thomas Cottrell (Kerning, Tracking & Sidebearings)
* **Responsibility**: Optical spacing, tracking curves, and character-pair kerning.
* **Standards**:
  * **Display Kerning**: `-0.025em` tracking for headings $\ge 24\text{px}$.
  * **Body Kerning**: `-0.011em` tracking for body text to optimize reading rhythm.
  * **Serif Kerning**: `-0.012em` tracking for Caslon serif text (`Libre Caslon Text`).

### 3. Joseph Jackson (Contrast & OpenType Disambiguation)
* **Responsibility**: WCAG 2.1 AAA high-contrast accessibility and OpenType features.
* **Standards**:
  * **Disambiguation**: Enforce `font-feature-settings: 'cv05', 'cv08', 'cv11'`.
  * **Luminance Ratios**: $\ge 7:1$ contrast against cardstock and papercraft surfaces.

---

## 🎨 Sandbox Font Stack

```css
/* Caslon Heritage Serif Stack */
font-family: 'Libre Caslon Text', 'Caslon', 'Georgia', 'Times New Roman', serif;
line-height: 1.65;
letter-spacing: -0.012em;

/* Modern Clinical Display Stack */
font-family: 'Outfit', 'Plus Jakarta Sans', 'Inter', sans-serif;
font-weight: 800;
letter-spacing: -0.025em;
line-height: 1.25;

/* High-Contrast Clinical Sans Stack */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
line-height: 1.55;
letter-spacing: -0.011em;
```
