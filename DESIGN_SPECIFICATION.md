# PocketGull Typeface Design Specification

## 1. Design Vision

**PocketGull** is an open-source handcrafted marker typeface derived from the original hand-drawn vector trace of the GearArts PocketGull brand mark. The 10 master vector glyph paths (`P`, `o`, `c`, `k`, `e`, `t`, `G`/`g`, `u`, `l`, `l`) define the foundational stroke vocabulary from which all other glyphs are extrapolated.

### Current Status (v2.000)

| Metric | Value |
|--------|-------|
| Master glyphs compiled from SVG | 9 (`P`, `o`, `c`, `k`, `e`, `t`, `g`/`G`, `u`, `l`) |
| Total glyphs in font | 235 (9 original + 226 base) |
| UPM grid | 1024 |
| Scale factor | 10.1266 (800 / 79.0) |
| Font variants | 5 (Bold, Antigravity, Chiseltip, Fineliner, Mono) |
| GSUB features | None yet |
| Kerning pairs | 1884 (inherited from base) |
| License | SIL Open Font License 1.1 |

> **Note**: 226 glyphs are currently inherited from the base font template and will be progressively replaced with original PocketGull drawings to achieve full visual consistency.

---

## 2. Vector Geometry & UPM Scaling

Raw SVG coordinates from the master wordmark (`viewBox="0 0 262.7243 79.1607"`) are scaled and transformed to the **1024 UPM** TrueType grid.

### Coordinate Transform

```
Scale     = 800 / 79.0 = 10.1266
X-origin  = -svg_xMin * Scale + LSB(40)
Y-flip    = -Scale * svg_y + (79.0 * Scale)
Advance   = svg_width * Scale + LSB(40) + RSB(40)
```

### Compiled Glyph Metrics

| Glyph | SVG Width | Font Width | Advance | BBox | Contours | Points |
|-------|-----------|-----------|---------|------|----------|--------|
| P | 39.09 | 397 | 475 | (40,2)-(437,780) | 2 | 34 |
| o | 28.89 | 292 | 372 | (40,-5)-(333,454) | 2 | 41 |
| c | 27.21 | 275 | 355 | (39,-5)-(319,463) | 1 | 39 |
| k | 31.81 | 322 | 402 | (40,13)-(362,746) | 1 | 19 |
| e | 26.97 | 273 | 353 | (39,11)-(314,477) | 2 | 39 |
| t | 23.44 | 237 | 317 | (40,5)-(277,648) | 1 | 27 |
| G/g | 36.13 | 365 | 445 | (39,2)-(406,781) | 1 | 54 |
| u | 27.49 | 278 | 358 | (40,5)-(318,466) | 1 | 33 |
| l | 10.75 | 108 | 188 | (40,9)-(149,762) | 1 | 10 |

### Vertical Metrics

| Zone | SVG Y Range | Font Y |
|------|-------------|--------|
| Ascender (top of P, k, l, G) | 0 - 5 | ~780 - 800 |
| Cap height (P top) | 2.17 | 780 |
| x-height (o, c, e, u top) | 33 - 35 | 450 - 465 |
| Baseline | 78 - 79 | 0 |

---

## 3. Stroke Anatomy

- **Vertical stems**: Thick felt-tip marker weight, organic variable width
- **Horizontal bars**: Tapered calligraphic nib stroke
- **Terminal caps**: Rounded organic corners simulating wet felt marker ink-bleed
- **Counters**: Maximized internal space in `e`, `o`, `c` for clinical readability at small sizes
- **Nib angle**: Approximately -4 degrees calligraphic chisel-tip tilt

---

## 4. Font Variants

| Variant | Subfamily | Weight | File |
|---------|-----------|--------|------|
| PocketGull Bold | Bold | 700 | `PocketGull-Bold.ttf` |
| PocketGull Antigravity | Bold | 700 | `PocketGull-Antigravity.ttf` |
| PocketGull Chiseltip | Black | 900 | `PocketGull-Chiseltip.ttf` |
| PocketGull Fineliner | Regular | 400 | `PocketGull-Fineliner.ttf` |
| PocketGull Mono | Regular | 400 | `PocketGullMono-Regular.ttf` |

All variants share the same 9 compiled master glyphs. Weight and style differentiation in the remaining glyphs comes from the base font template.

---

## 5. Build Pipeline

### Compilation Scripts

| Script | Purpose |
|--------|---------|
| `scripts/compile_v2.py` | Origin-normalized two-pass SVG-to-TTF compiler |
| `scripts/fix_all_variants.py` | Batch recompile + name table fix + fake alias removal |
| `scripts/analyze_wordmark.py` | SVG path bounding box analysis and letter mapping |
| `scripts/audit_fonts.py` | Diagnostic glyph inventory and metrics audit |

### Build Reproducibility

- **Timestamp freezing**: `head.created` and `head.modified` set to 0
- **Font revision**: `head.fontRevision = 2.0`
- **SVG source of truth**: `article/pocketgull-wordmark.svg`
- **Python runtime**: `C:\Users\philg\anaconda3\python.exe` with `fontTools`

---

## 6. Known Limitations

1. **G/g letterform**: The SVG wordmark contains a display-capital G form mapped to both `G` and `g` slots. In body text, the lowercase `g` renders as a capital letterform. This is intentional for the wordmark display use case.

2. **Base font glyphs**: 226 glyphs (A-Z except P, a-z except o/c/k/e/t/g/u/l, 0-9, punctuation, diacritics) are inherited from a base font template and have a different visual personality than the 9 master glyphs. Full visual consistency requires drawing these from scratch.

3. **No GSUB features**: Contextual alternates (`calt`), discretionary ligatures (`dlig`), and clinical icon mappings described in earlier specs do not yet exist in the compiled binaries.

4. **No GPOS kerning**: The font inherits 1884 kerning pairs from the base template, but no PocketGull-specific kerning has been authored for the master glyphs.

---

## 7. License

Released under the **SIL Open Font License 1.1 (OFL)**.
Reserved Font Name: `PocketGull`
Copyright 2026 The PocketGull Project Authors (https://github.com/philgear/pocketgull-typeface)
