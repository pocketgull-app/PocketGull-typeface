# Canadian Aboriginal Syllabics (Inuktitut) Language Map
## A Pedagogical & Clinical Guide to Rotational Phonetic Geometry

**Superfamily**: PocketGull (`Fineliner`, `Bold`, `Chiseltip`, `Mono`)  
**Unicode Block**: `U+1400`–`U+167F` (Canadian Aboriginal Syllabics)  
**Standard**: Google Fonts Specification, OFL 1.1, WCAG AAA  
**Audience**: Students, Clinicians, Community Educators, Typographers  

---

## 1. The 1840 Rotational Geometry

Invented in 1840 by James Evans in collaboration with Cree knowledge keepers at Norway House, Manitoba, Canadian Aboriginal Syllabics is one of humanity’s most mathematically elegant writing systems. 

Rather than memorizing hundreds of arbitrary letterforms, the syllabary uses **geometric symmetry**:
- Each **consonant family** is represented by a distinctive geometric skeleton (chevron, crescent, crossbar, wedge, box).
- The **vowel** attached to that consonant is determined solely by the **rotational orientation** of that skeleton across four cardinal angles:

$$\theta \in \{0^\circ \text{ (I)}, 90^\circ \text{ (U)}, 180^\circ \text{ (A)}, 270^\circ \text{ (E)}\}$$

```
                ▲ 0° (Orientation I: /i/)
                │
  270° (E: /e/) ◄───┼───► 90° (Orientation U: /u/)
                │
                ▼ 180° (Orientation A: /a/)
```

---

## 2. The Complete 13-Series Inuktitut Matrix

Every cell below represents an official Inuktitut syllabic codepoint. Inuktitut in Nunavut and Nunavik primarily uses the three vowel orientations **I**, **U**, and **A**, while Eastern/Cree dialects also utilize **E**.

| Series | Consonant | Base Primitive | Orientation I (/i/) | Orientation U (/u/) | Orientation A (/a/) | Orientation E (/e/) | Coda Final (Superscript) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **01. Vowels** | (None) | Equilateral Triangle | **ᐃ** (`U+1403`) | **ᐅ** (`U+1405`) | **ᐊ** (`U+140A`) | **ᐁ** (`U+1401`) | — |
| **02. P-Series** | /p/ | Open Chevron | **ᐱ** (`U+1431`) | **ᐳ** (`U+1433`) | **ᐸ** (`U+1438`) | **ᐯ** (`U+142F`) | **ᑉ** (`U+1449`) |
| **03. T-Series** | /t/ | Crossbar Stem | **ᑎ** (`U+144E`) | **ᑐ** (`U+1450`) | **ᑕ** (`U+1455`) | **ᑌ** (`U+144C`) | **ᑦ** (`U+1466`) |
| **04. K-Series** | /k/ | Wedge Angle | **ᑭ** (`U+146D`) | **ᑯ** (`U+146F`) | **ᑲ** (`U+1472`) | **ᑫ** (`U+146B`) | **ᒃ** (`U+1483`) |
| **05. G-Series** | /g/ | Curved Crescent | **ᒋ** (`U+148B`) | **ᒍ** (`U+148D`) | **ᒐ** (`U+1490`) | **ᒉ** (`U+1489`) | **ᒡ** (`U+14A1`) |
| **06. M-Series** | /m/ | Open Square Box | **ᒥ** (`U+14A5`) | **ᒧ** (`U+14A7`) | **ᒪ** (`U+14AA`) | **ᒣ** (`U+14A3`) | **ᒻ** (`U+14BB`) |
| **07. N-Series** | /n/ | Bent Chevron | **ᓂ** (`U+14C2`) | **ᓄ** (`U+14C4`) | **ᓇ** (`U+14C7`) | **ᓀ** (`U+14C0`) | **ᓐ** (`U+14D0`) |
| **08. S-Series** | /s/ | Double Arch Loop | **ᓯ** (`U+14EF`) | **ᓱ** (`U+14F1`) | **ᓴ** (`U+14F4`) | **ᓭ** (`U+14ED`) | **ᔅ** (`U+1505`) |
| **09. L-Series** | /l/ | Stem with Loop | **ᓕ** (`U+14D5`) | **ᓗ** (`U+14D7`) | **ᓚ** (`U+14DA`) | **ᓓ** (`U+14D3`) | **ᓪ** (`U+14EA`) |
| **10. J-Series** | /j/ (y) | Dot Hook | **ᔨ** (`U+1528`) | **ᔪ** (`U+152A`) | **ᔭ** (`U+152D`) | **ᔦ** (`U+1526`) | **ᔾ** (`U+153E`) |
| **11. R-Series** | /r/ (q) | Double Arch Hook | **ᕆ** (`U+1546`) | **ᕈ** (`U+1548`) | **ᕋ** (`U+154B`) | **ᕂ** (`U+1542`) | **ᕐ** (`U+1550`) |
| **12. Q-Series** | /q/ (uvular) | Hooked Angle Cross | **ᕿ** (`U+157F`) | **ᖁ** (`U+1581`) | **ᖃ** (`U+1583`) | **ᕴ** (`U+1574`) | **ᖅ** (`U+1585`) |
| **13. NG-Series** | /ŋ/ | Composite Angle | **ᖏ** (`U+1590`) | **ᖑ** (`U+1591`) | **ᖓ** (`U+1593`) | **ᖐ** (`U+158E`) | **ᖕ** (`U+1595`) |

---

## 3. Long Vowels (Diacritic Superdots)

In Inuktitut, vowel length is phonemically distinctive (*minimal pairs* depend on vowel duration). A single raised dot above the syllabic character doubles the vowel duration:

| Short Vowel | Long Vowel (Superdot) | Phonetic Value | Example Word | English Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **ᐃ** (/i/) | **ᐄ** (`U+1404`, /ii/) | High front long | **ᐄᒃ** (*iik*) | Two eyes |
| **ᐅ** (/u/) | **ᐆ** (`U+1406`, /uu/) | High back rounded long | **ᐆᒻᒪᑎ** (*uummati*) | Heart |
| **ᐊ** (/a/) | **ᐋ** (`U+140B`, /aa/) | Low central open long | **ᐋᓐᓂᐊᕕᒃ** (*aanniavik*) | Hospital |
| **ᑎ** (/ti/) | **ᑏ** (`U+144F`, /tii/) | Alveolar long | **ᑏ** (*tii*) | Tea |
| **ᑐ** (/tu/) | **ᑑ** (`U+1451`, /tuu/) | Alveolar rounded long | **ᑑᒑᖅ** (*tuugaaq*) | Narwhal tusk |
| **ᑕ** (/ta/) | **ᑖ** (`U+1456`, /taa/) | Alveolar open long | **ᑖᒃᑐᖅ** (*taaktuq*) | Dark / night |

---

## 4. Special Nunavut & Arctic Characters

1. **ᕵ** (`U+1575`) / **ᕼ** (`U+15A4`) — **Nunavut H**: Used in western dialects (Inuinnaqtun) and loanwords.
2. **ᙱ** (`U+1585`) — **Double NNG Ligature**: Combines the nasal coda with the stop for clusters like *aanniaqarnaangittuliriniq*.
3. **ᖖ** (`U+1596`) — **Raised Small NNG Coda**: Superscript nasal cluster coda.

---

## 5. The PERMA+ Clinical Well-Being Lexicon

In the PocketGull medical care plan architecture, Inuktitut typography directly serves community health across Martin Seligman's **PERMA+ Clinical Well-Being & Lifestyle Medicine Model**:

```
 ┌─────────────────────────────────────────────────────────────┐
 │                      PERMA+ VITALITY                        │
 │                                                             │
 │   [P] ᖁᕕᐊᓱᖕᓂᖅ      Positive Emotion & Mental Peace        │
 │   [E] ᐱᓕᕆᖃᑕᐅᓂᖅ      Deep Engagement & Cultural Presence    │
 │   [R] ᐃᓅᖃᑎᒌᖕᓂᖅ      Sacred Relationships & Kinship (Inuu)  │
 │   [M] ᑐᑭᖃᕐᓂᖅ        Existential Purpose & Meaning          │
 │   [A] ᐱᔭᕇᖅᓯᓂᖅ      Accomplishment & Patient Mastery       │
 │   [+] ᑎᒥᒥᒃ ᑲᒪᑦᑎᐊᕐᓂᖅ Physical Vitality & Somatic Health    │
 └─────────────────────────────────────────────────────────────┘
```

### Detailed Clinical Lexicon:

| Pillar | Inuktitut Term | Romanization | Clinical Physiology & Meaning |
| :--- | :--- | :--- | :--- |
| **Positive Emotion (P)** | **ᖁᕕᐊᓱᖕᓂᖅ** | *Quviasungniq* | Vagal tone elevation, parasympathetic stabilization, resilience. |
| **Engagement (E)** | **ᐱᓕᕆᖃᑕᐅᓂᖅ** | *Piliriqatauniq* | Flow state, cultural craft, dopamine regulation, executive focus. |
| **Relationships (R)** | **ᐃᓅᖃᑎᒌᖕᓂᖅ** | *Inuuqatigiingniq* | Social determinants of health (SDOH), communal safety, oxytocin. |
| **Meaning (M)** | **ᑐᑭᖃᕐᓂᖅ** | *Tukiqarniq* | Existential coherence, mental health grounding, suicide prevention. |
| **Accomplishment (A)** | **ᐱᔭᕇᖅᓯᓂᖅ** | *Pijariiqsiniq* | Patient Activation Measure (PAM), rehabilitation adherence. |
| **Physical Vitality (+)** | **ᑎᒥᒥᒃ ᑲᒪᑦᑎᐊᕐᓂᖅ** | *Timimik Kamattiarniq* | Metabolic health, blood pressure, restful sleep, cardiac rhythm. |
| **EHR Department Header** | **ᐋᓐᓂᐊᖃᕐᓇᙱᑦᑐᓕᕆᓂᖅ** | *Aanniaqarnaangittuliriniq* | Department of Health / Healthcare Services. |
| **Primary Physician** | **ᓘᒃᑖᖅ** | *Luuktaaq* | Licensed Medical Doctor / Attending Physician. |
| **Telehealth Nurse** | **ᐋᓐᓂᐊᓯᐅᖅᑎ** | *Aanniasiurti* | Registered Nurse / Community Health Officer. |
| **Heart / Telemetry** | **ᐆᒻᒪᑎ** | *Uummati* | Cardiac rate, rhythm, telemetry ECG tracing. |
| **Blood / Hemodynamics**| **ᐊᐅᒃ** | *Auk* | Blood pressure, hemoglobin, SpO2 perfusion. |

---

## 6. Typographic Anatomy in PocketGull

- **Unit Per Em (UPM)**: 1000 UPM grid.
- **Optotypes**: Designed according to Louise Sloan 5:1 optotype legibility standards for clear resolution at distance.
- **Nib Model**: Elliptical chisel nib ($a = 6.5, b = 2.3, \theta = -4^\circ$) creating the warm human presence of an intentional ink stroke.
- **Monospace Alignment**: In `PocketGullMono-Regular`, all 640 Syllabics are centered exactly on a **600 UPM advance width**, guaranteeing zero layout drift in serial medical terminals and EHR monitors.
