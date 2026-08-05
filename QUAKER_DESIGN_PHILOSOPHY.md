# 🌾 Quaker Type Design Philosophy & Plainness Standard

> *"Let your Yea be Yea, and your Nay be Nay; for whatsoever is more than these cometh of evil."* — Matthew 5:37  
> *"Truth is plain, simple, and unadorned."* — Quaker Testimony of Simplicity (Plainness)

---

## 🕯️ The 5 Quaker Design Testimonies in Type Engineering

### 1. Testimony of Simplicity (Plainness / *Simplicitas*)
* **Elimination of Superfluity**: Strips away artificial drop-shadows, 3D text strokes, fake gold gradients, and ostentatious flourishes.
* **Honesty of Form**: Every curve and stroke stems directly from the functional vector path of the original hand-drawn felt-tip mark (`P-o-c-k-e-t-g-u-l-l`).

### 2. Testimony of Peace & Stillness (*Tranquillitas*)
* **Generous Leading & Breathing Room**: Line height set to $1.7\times$ font size to create calm, unhurried visual rhythm.
* **Quiet Contrast & Warm Color Palette**: Natural linen (`#F5F3EF`), deep charcoal ink (`#1C1B1A`), and warm ochre (`#C27D38`) replace harsh synthetic colors.

### 3. Testimony of Integrity & Truth (*Veritas*)
* **Zero Disguise**: No fake font-mashing or artificial skewing (`skewX`). A single, honest, fully-formed typeface serves every purpose.
* **Clear Disambiguation**: Zero ambiguity between `1`, `l`, `I` and `0`, `O` for patient safety and medical truth.

### 4. Testimony of Equality (*Aequabilitas*)
* **WCAG 2.1 AAA Accessibility**: Universal legibility across high-contrast daylight, papercraft cardstock, and dark mode displays. Equal ease of reading for all eyes.

### 5. Testimony of Community & Stewardship (*Communitas*)
* **SIL Open Font License 1.1**: Open-source, freely shared, and built for the common good.

---

## 🎨 Quaker Plainness Design Tokens

```css
/* Quaker Plainness Theme System */
:root {
  --quaker-paper: #fbf9f5;      /* Unbleached Natural Paper */
  --quaker-linen: #f2efe9;      /* Raw Handwoven Linen */
  --quaker-ink: #1c1b1a;        /* Deep Iron-Gall Ink */
  --quaker-slate: #4a4744;      /* Quiet Slate Stone */
  --quaker-ochre: #c27d38;      /* Warm Earth Ochre Accent */
  
  --quaker-leading-body: 1.7;   /* Peaceful, spacious line-height */
  --quaker-leading-heading: 1.3;/* Calm, unforced title rhythm */
  --quaker-tracking-body: -0.01em;
  --quaker-tracking-heading: -0.02em;
}
```
