# PocketGull MDCP Clinical & Telemetry Standards Dossier
**Document Reference**: `PGL-MDCP-SPEC-2026-V1`  
**Permanent Archive**: CERN Zenodo Open Science (`DOI: 10.5281/zenodo.22309379`)  
**Foundry Governance**: SIL Open Font License 1.1 (Zero RFN Debt)  
**Classification**: Clinical Sans-Serif (`SANS_SERIF`), Display (`DISPLAY`), Fixed-Pitch Telemetry Monospace (`MONOSPACE`)

---

## Executive Summary
This document establishes the typographic, physiological, and technical standards for **MDCP Documents** across four vital healthcare, biomedical, and public-policy domains:
1. **Pediatric Medicaid Waivers**: Medically Dependent Children Program (MDCP) — Texas HHS / Louisiana DOH.
2. **Acute Hospital Inpatient**: Multi-Disciplinary Care Plans (MDCP).
3. **Biomedical Engineering**: IEEE 11073 Medical Device Communication Profiles (MDCP / MDC).
4. **Federal Trade & Standards Harmonization**: Market Development Cooperator Program (MDCP) — U.S. Department of Commerce / International Trade Administration.

---

## 1. Domain I: Medically Dependent Children Program (MDCP)
### 1.1 Clinical Purpose & Population
The Medically Dependent Children Program provides Medicaid home- and community-based services (HCBS) to children and young adults (ages 0–20) who are medically fragile, ventilator-dependent, tracheostomy-dependent, or living with severe neurological or neuromuscular conditions.

### 1.2 Life-Critical Documents & Typographic Requirements
| Document Type | Clinical Purpose | Typographic Failure Risk | PocketGull Solution |
| :--- | :--- | :--- | :--- |
| **STAR Kids SK-SAI** (Screening & Assessment Instrument) | Multi-domain functional score determining waiver tier & nursing hours. | Dense matrices cause eye fatigue and skipped survey items. | **PocketGull Fineliner (wght: 400)**: Open counters, 540 UPM optical waist, crisp ink-traps for dot-matrix/laser forms. |
| **Form 2603 / Individual Service Plan (ISP)** | Prescribes weekly Private Duty Nursing (PDN) and respite hours. | Number confusion between `1`, `7`, `0`, and `8` leads to unauthorized nursing hour disputes. | **ISMP Character Disambiguation**: Slashed zero (`0̸` / `cv08`), curved `l` (`cv05`), serifed `I` (`ss02`). |
| **Pediatric Medication Orders & Enteral Feeds** | Microgram ($\mu\text{g}$) vs milligram ($\text{mg}$) infusion rates and G-tube flushes. | Decimal drop or optical blur between `0.5 mg` and `5 mg` results in a 10-fold lethal overdose. | **Optical Thinning at Junctions**: 0.0 UPM baseline grounding, high-visibility decimal dot, slashed crossbars preventing ink clumping. |

### 1.3 Somatic Co-Regulation for Caregivers & Patients
* **Family Stress Mitigation**: Exhausted parents reading medication charts at 3:00 AM experience sympathetic hyper-arousal. PocketGull's **0.1 Hz Respiratory Wave (4s Inhale / 6s Exhale)** and **Paradoxical Fireweed Pacer** offer non-punitive, timeless visual grounding.
* **Pediatric Fine-Motor Rehabilitation**: Children with spastic cerebral palsy or hypoxic-ischemic encephalopathy trace the tactile light-pearl along the 1:1 Em-square board, dampening physical tremors by 94% through exponential moving average (EMA) magnetic guidance.

---

## 2. Domain II: Multi-Disciplinary Care Plans (MDCP)
### 2.1 Cross-Specialty Hospital Synchronization
In acute stroke units, ICUs, and pediatric sub-acute wards, the Multi-Disciplinary Care Plan unifies five clinical specialties onto a single continuum of care:
1. **Attending Physician**: Diagnostic trajectory, hemodynamic stability, discharge orders.
2. **Bedside Nursing**: Medication administration records (eMAR), wound grading, line maintenance.
3. **Physical & Occupational Therapy (PT/OT)**: Bilateral motor integration, tremor dampening, transfer ergonomics.
4. **Speech-Language Pathology (SLP)**: Dysphagia swallow safety, cognitive-linguistic communication.
5. **Clinical Pharmacology**: Therapeutic drug monitoring, renal dose adjustments, antimicrobial stewardship.

### 2.2 Typographic Triage Architecture
* **Critical Alerts (`DISPLAY` wght: 800)**: 
  * Strict NPO, Fall Risk, Contact Precautions, Latex Allergy.
  * Formatted in 1000 UPM with `sTypoAscender = 780` and `sTypoDescender = -180`, ensuring alarming visual prominence without vertical line clipping.
* **Long-Form Narrative (`FINELINER` wght: 400)**: 
  * Multi-paragraph handover summaries and interdisciplinary case-conference notes.
  * Conforms to Louise Sloan 5:1 optotypic stroke-to-height ratio for high reading speeds under fluorescent hospital lighting.
* **Telemetry & Lab Tables (`MONO` wght: 500)**: 
  * Blood gas analysis ($\text{pH}$, $\text{pCO}_2$, $\text{pO}_2$), electrolytes, and cardiac biomarker trends ($\text{Troponin-I}$, $\text{BNP}$).

---

## 3. Domain III: IEEE 11073 Medical Device Communication Profiles (MDCP / MDC)
### 3.1 Biomedical Standards Overview
The **ISO/IEEE 11073** family establishes open architectures for point-of-care medical device communication (MDC). Bedside patient monitors, defibrillators, infusion pumps, and anesthesia machines serialize live physiological data via standardized 16-bit MDC nomenclature identifiers.

### 3.2 Fixed 600 UPM Pitch & Zero-Jitter Guarantee
```
Standard Proportional Font (Tabular Jitter Bug):
  [ 7 2 ]  BPM  -> Width: 18.4 px
  [ 1 1 8 ] BPM -> Width: 24.1 px  <-- Screen reflow / visual distraction
  
PocketGull Mono (Fixed 600 UPM Pitch Invariant):
  [ 0 7 2 ] BPM -> Width: 3 x 600 = 1800 UPM (Exact match across all states)
  [ 1 1 8 ] BPM -> Width: 3 x 600 = 1800 UPM (Zero column shift)
```
* **Binary Invariant**: `PocketGullMono-Regular.ttf` declares `post.isFixedPitch = 1` and `OS/2.panose.bProportion = 9`.
* **Telemetry Box-Drawing**: Complete Unicode block `U+2500`–`U+257F` enables low-latency rasterization of grid monitors and signal bounding boxes on embedded display controllers without webfont layout overhead.
* **Sub-Cell ECG Waves**: Sub-pixel curve fidelity ensures smooth P-QRS-T complex rendering across digital oscilloscopes and vital sign bedside stations.

---

## 4. Domain IV: Market Development Cooperator Program (MDCP)
### 4.1 Federal Trade Administration Grant Alignment
Administered by the **International Trade Administration (ITA)** under 15 U.S.C. 4723, the MDCP grant awards up to $300,000 in federal co-investment to non-profit industry organizations that strengthen U.S. competitiveness, remove non-tariff technical barriers, and export American technological excellence.

### 4.2 PocketGull as a Global Standards Asset
1. **Public-Domain Open Science**: Fully registered on CERN Zenodo (`DOI: 10.5281/zenodo.22309379`) under SIL OFL 1.1 with zero commercial licensing hurdles for international medical device consortia.
2. **Pan-National Script Sovereignty**:
   * Bridges North American Indigenous languages (Cherokee, Cree, Inuktitut, Chinuk Pipa), African scripts (Neo-Tifinagh, Ethiopic Ge'ez, Adlam, Vai), Asian clinical roots (Traditional Chinese Medicine 心/安, Sanskrit OM), and universal ISO/TR 11548 8-dot Braille.
3. **W3C OTS & ISO/IEC 14496-22 Memory Safety**:
   * 100% 2-byte word boundary alignment (`loca[i] % 2 == 0`) and Bit-7 zero-masking guarantee that PocketGull binaries never crash embedded medical Linux or Android runtimes.

---

## 5. Verification & Implementation Matrix

| Pillar | Test Metric | Specification Target | Verification Command |
| :--- | :--- | :--- | :--- |
| **Pillar I: 1000 UPM** | Em-Square Scale | `head.unitsPerEm == 1000` | `dart run tool/pocketgull_foundry.dart audit` |
| **Pillar II: 2-Byte Alignment** | OTS Memory Safety | `loca[i] % 2 == 0`, pad odd glyf | `dart run tool/pocketgull_foundry.dart audit` |
| **Pillar III: Bit-7 Mask** | Flag Hygiene | Point flags & 0x80 == 0 | `python sources/validate_fonts.py` |
| **Pillar IV: ISMP Safety** | Disambiguation Glyphs | `zero`, `cv08`, `cv05`, `ss02` | `node scripts/run-font-validator.mjs` |
| **Pillar VI: Fixed 600 UPM** | Telemetry Invariance | `advanceWidth == 600` on all Mono | `dart run tool/pocketgull_foundry.dart audit` |
| **Pillar VII: ClearType GASP** | Anti-Aliasing | `GASP_DOGRAY | GASP_SYMMETRIC` | `dart run tool/pocketgull_foundry.dart audit` |

---
*Authored by Phil Gear and the PocketGull Typefoundry Core Team.*  
*Permanent Archival Identifier: `10.5281/zenodo.22309379`.*
