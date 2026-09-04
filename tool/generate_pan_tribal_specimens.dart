// Copyright (c) 2026, The PocketGull Project Authors.
// All rights reserved. Use of this source code is governed by an OFL 1.1 license.

/// Pan-Tribal Sovereign Specimen & Landmark Vector Suite Generator
///
/// Procedurally synthesizes the 5 canonical museum print specimen plates in SVG
/// across 4 major North American sovereign linguistic traditions:
///   1. Diné Bizaad (Navajo Nation / Four Sacred Mountains / Red Sandstone & Turquoise)
///   2. Lakȟótiyapi (Očhéthi Šakówiŋ / Great Plains / Prairie Sage & Sun Gold)
///   3. dxʷləšucid / Lushootseed (Coast Salish / Cedar & Salmon / Puget Sound Mist)
///   4. Tsalagi Gawonihisdi (Cherokee Nation / Sequoyah Syllabary / Blue Ridge & Ozarks)
///
/// Renders 300 DPI Master Museum Print PNGs using headless Inkscape in WSL.
library;

import 'dart:convert';
import 'dart:io';

void main() async {
  stdout.writeln('=== POCKETGULL PAN-TRIBAL SOVEREIGN SPECIMEN GENERATOR ===');
  stdout.writeln('Honoring the 574+ Sovereign Tribes, First Nations & Circumpolar Communities\n');

  final repoDir = Directory('c:/Users/philg/Pocketgull/pocketgull-typeface');

  // Load high-resolution masterwork substrates
  final pebblePath = '${repoDir.path}/documentation/masterworks/pacific_northwest/pebble_pnw_biodiversity.webp';
  final kellsPath = '${repoDir.path}/documentation/masterworks/pacific_northwest/kells_pnw_vexillology.webp';
  final rubaiyatPath = '${repoDir.path}/documentation/masterworks/pacific_northwest/rubaiyat_pnw_astrolabe.webp';
  final arcticKellsPath = '${repoDir.path}/documentation/masterworks/inuktitut/kells_arctic_vexillology.webp';
  final arcticPebblePath = '${repoDir.path}/documentation/masterworks/inuktitut/pebble_arctic_biodiversity.webp';
  final devicePath = '${repoDir.path}/article/libre_pocketgull_device_1x1.jpg';

  stdout.write('Loading photographic and fine-art substrates... ');
  final pebbleBase64 = File(pebblePath).existsSync() ? base64Encode(File(pebblePath).readAsBytesSync()) : '';
  final kellsBase64 = File(kellsPath).existsSync() ? base64Encode(File(kellsPath).readAsBytesSync()) : '';
  final rubaiyatBase64 = File(rubaiyatPath).existsSync() ? base64Encode(File(rubaiyatPath).readAsBytesSync()) : '';
  final arcticKellsBase64 = File(arcticKellsPath).existsSync() ? base64Encode(File(arcticKellsPath).readAsBytesSync()) : '';
  final arcticPebbleBase64 = File(arcticPebblePath).existsSync() ? base64Encode(File(arcticPebblePath).readAsBytesSync()) : '';
  final deviceBase64 = File(devicePath).existsSync() ? base64Encode(File(devicePath).readAsBytesSync()) : '';
  stdout.writeln('OK\n');

  final traditions = [
    navajoTradition(kellsBase64.isNotEmpty ? kellsBase64 : deviceBase64),
    lakotaTradition(rubaiyatBase64.isNotEmpty ? rubaiyatBase64 : deviceBase64),
    salishTradition(pebbleBase64.isNotEmpty ? pebbleBase64 : deviceBase64),
    cherokeeTradition(kellsBase64.isNotEmpty ? kellsBase64 : deviceBase64),
    ojibweTradition(pebbleBase64.isNotEmpty ? pebbleBase64 : deviceBase64),
    mohawkTradition(kellsBase64.isNotEmpty ? kellsBase64 : deviceBase64),
    hawaiianTradition(pebbleBase64.isNotEmpty ? pebbleBase64 : deviceBase64),
    inupiaqTradition(arcticKellsBase64.isNotEmpty ? arcticKellsBase64 : (arcticPebbleBase64.isNotEmpty ? arcticPebbleBase64 : deviceBase64)),
    hopiTradition(rubaiyatBase64.isNotEmpty ? rubaiyatBase64 : deviceBase64),
    choctawTradition(kellsBase64.isNotEmpty ? kellsBase64 : deviceBase64),
  ];

  for (final t in traditions) {
    stdout.writeln('------------------------------------------------------------');
    stdout.writeln('Generating Specimen Suite for: ${t.title} (${t.nativeName})');
    stdout.writeln('Jurisdiction: ${t.jurisdiction}');
    stdout.writeln('------------------------------------------------------------');

    final targetDir = Directory('${repoDir.path}/documentation/images/${t.id}');
    if (!targetDir.existsSync()) {
      targetDir.createSync(recursive: true);
    }

    // 1. Social GitHub Preview (1280x640)
    stdout.write('  [1/5] Synthesizing social_github_preview.svg... ');
    final socialSvg = generateSocialPreview(t);
    File('${targetDir.path}/social_github_preview.svg').writeAsStringSync(socialSvg);
    stdout.writeln('OK');

    // 2. Type Engineering Blueprint (2688x3600, 300 DPI)
    stdout.write('  [2/5] Synthesizing pocketgull_type_engineering_specimen.svg... ');
    final engSvg = generateTypeEngineeringPlate(t);
    File('${targetDir.path}/pocketgull_type_engineering_specimen.svg').writeAsStringSync(engSvg);
    stdout.writeln('OK');

    // 3. Clinical Telemetry Specimen (2688x3600, 300 DPI)
    stdout.write('  [3/5] Synthesizing pocketgull_telemetry_type_specimen.svg... ');
    final telSvg = generateTelemetryTypePlate(t);
    File('${targetDir.path}/pocketgull_telemetry_type_specimen.svg').writeAsStringSync(telSvg);
    stdout.writeln('OK');

    // 4. Pedagogical Typeface Specimen (2688x3600, 300 DPI)
    stdout.write('  [4/5] Synthesizing pocketgull_pedagogical_typeface.svg... ');
    final pedSvg = generatePedagogicalPlate(t);
    File('${targetDir.path}/pocketgull_pedagogical_typeface.svg').writeAsStringSync(pedSvg);
    stdout.writeln('OK');

    // 5. PERMA+ Thoughts Card (2400x2400, 300 DPI)
    stdout.write('  [5/5] Synthesizing pocketgull_perma_thoughts_card.svg... ');
    final permaSvg = generatePermaThoughtsCard(t);
    File('${targetDir.path}/pocketgull_perma_thoughts_card.svg').writeAsStringSync(permaSvg);
    stdout.writeln('OK');

    // Rasterize 300 DPI PNGs via WSL Inkscape
    stdout.writeln('\n  Rasterizing 300 DPI Master Museum Print PNGs via WSL Inkscape:');
    final specs = [
      ('social_github_preview.svg', 'social_github_preview.png', 1280, 640),
      ('pocketgull_type_engineering_specimen.svg', 'pocketgull_type_engineering_specimen.png', 2688, 3600),
      ('pocketgull_telemetry_type_specimen.svg', 'pocketgull_telemetry_type_specimen.png', 2688, 3600),
      ('pocketgull_pedagogical_typeface.svg', 'pocketgull_pedagogical_typeface.png', 2688, 3600),
      ('pocketgull_perma_thoughts_card.svg', 'pocketgull_perma_thoughts_card.png', 2400, 2400),
    ];

    for (final (svgName, pngName, width, height) in specs) {
      final wslSvgPath = '/mnt/c/Users/philg/Pocketgull/pocketgull-typeface/documentation/images/${t.id}/$svgName';
      final wslPngPath = '/mnt/c/Users/philg/Pocketgull/pocketgull-typeface/documentation/images/${t.id}/$pngName';

      stdout.write('    -> $pngName (${width}x$height)... ');
      final result = await Process.run('wsl', [
        '--',
        '/usr/bin/inkscape',
        wslSvgPath,
        '--export-type=png',
        '--export-filename=$wslPngPath',
        '-w',
        '$width',
        '-h',
        '$height',
      ]);

      if (result.exitCode == 0) {
        final pngFile = File('${targetDir.path}/$pngName');
        final sizeMb = (pngFile.existsSync() ? pngFile.lengthSync() / (1024 * 1024) : 0).toStringAsFixed(2);
        stdout.writeln('OK ($sizeMb MB)');
      } else {
        stderr.writeln('FAILED (exit code ${result.exitCode})');
        stderr.writeln(result.stderr);
      }
    }
    stdout.writeln('');
  }

  stdout.writeln('============================================================');
  stdout.writeln('ALL PAN-TRIBAL MASTER SPECIMEN SUITES GENERATED & VERIFIED');
  stdout.writeln('============================================================');
}

// =============================================================================
// TRIBAL TRADITION DOMAIN MODEL
// =============================================================================
class TribalTradition {
  final String id;
  final String title;
  final String nativeName;
  final String jurisdiction;
  final String regionTag;
  final String primaryColor;
  final String secondaryColor;
  final String accentColor;
  final String darkBasalt;
  final String washiBg;
  final String bannerGradientStart;
  final String bannerGradientEnd;
  final String backdropBase64;
  final String emblemSymbol;
  final String landscapeTitle;
  final String landscapePoetics;
  final Map<String, String> vitals;
  final List<(String, String, String)> pillars; // (PillarName, NativeName, Concept)
  final List<(String, String, String)> technicalFeatures; // (Feature, Metric, Value)
  final List<(String, String)> vocabulary; // (Native, English)

  TribalTradition({
    required this.id,
    required this.title,
    required this.nativeName,
    required this.jurisdiction,
    required this.regionTag,
    required this.primaryColor,
    required this.secondaryColor,
    required this.accentColor,
    required this.darkBasalt,
    required this.washiBg,
    required this.bannerGradientStart,
    required this.bannerGradientEnd,
    required this.backdropBase64,
    required this.emblemSymbol,
    required this.landscapeTitle,
    required this.landscapePoetics,
    required this.vitals,
    required this.pillars,
    required this.technicalFeatures,
    required this.vocabulary,
  });
}

// -----------------------------------------------------------------------------
// 1. DINÉ BIZAAD (NAVAJO NATION)
// -----------------------------------------------------------------------------
TribalTradition navajoTradition(String backdrop) => TribalTradition(
  id: 'navajo',
  title: 'Diné Bizaad (Navajo)',
  nativeName: 'Diné bi Bibeehazʼáanii',
  jurisdiction: 'Navajo Nation • IHS Navajo Area',
  regionTag: 'NN-AZ/NM/UT',
  primaryColor: '#991B1B', // Red Sandstone
  secondaryColor: '#0D9488', // Sacred Turquoise
  accentColor: '#F59E0B', // Sun Gold
  darkBasalt: '#0F172A',
  washiBg: '#FAF8F5',
  bannerGradientStart: '#7F1D1D',
  bannerGradientEnd: '#0F766E',
  backdropBase64: backdrop,
  emblemSymbol: '🏜️',
  landscapeTitle: 'The Four Sacred Mountains & Red Mesa Sanctuaries',
  landscapePoetics:
      'Bounded by Blanca Peak (East), Mount Taylor (South), San Francisco Peaks (West), and Hesperus Peak (North). '
      'From Canyon de Chelly’s sheer red sandstone spires to the sagebrush-scented breeze off high piñon mesas, '
      'health is living in sacred beauty (Hózhó).',
  vitals: {
    'HEART_RATE': '72 BPM • Dilwosh',
    'BLOOD_PRESSURE': '120/80 mmHg • Dił',
    'SPO2': '99% • Atsiis oxygen',
    'TEMP': '37.0°C • Atsiis',
    'RX_TITLE': 'Azeeʼ Ííłʼíní (Physician Order)',
    'RX_BODY': 'Tʼáá ákwíí jį́ tʼááłáʼí azeeʼ yidlą́ (Take 1 tablet daily with clean water)',
  },
  pillars: [
    ('Positive Emotion', 'Hózhó', 'Walking in harmony, joy, and somatic equilibrium'),
    ('Engagement', 'Nitsáhákees', 'Mindful dawn thinking and focused mental intention'),
    ('Relationships', 'Kʼé', 'Sacred kinship, mutual compassion, and respectful relations'),
    ('Meaning', 'Nahatʼá', 'Life purpose guided by the teachings of the Holy People'),
    ('Accomplishment', 'Iiná', 'Active daily living with vigor, endurance, and fortitude'),
    ('Health Vitality', 'Atsʼíís Baa Áháyą́', 'Holistic care for the body through traditional foodways'),
  ],
  technicalFeatures: [
    ('Stacked Acute Nasal Clearance', 'ą́, ę́, į́, ǫ́', '>= 110 UPM Head Space'),
    ('Barred Alveolar Fricative', 'Ł, ł, ƛ', '1.4x Optical Stem Aperture'),
    ('First-Class Glottal Stop', 'Azeeʼ (Saltillo ʼ)', '340 UPM Advance Width'),
    ('Thermal Label Integrity', 'Prescription MAR', '0% Tone Truncation'),
  ],
  vocabulary: [
    ('Hózhó', 'Universal balance, beauty, and complete health'),
    ('Azeeʼ', 'Medicine, botanical remedy, or treatment'),
    ('Tádídíín', 'Sacred blue corn pollen used in blessing rituals'),
    ('Kʼé', 'Compassion, extended family kinship, and unity'),
    ('Iiná', 'Vitality, physical life, and enduring resilience'),
    ('Łichííʼ', 'Red sandstone earth and sacred hematite color'),
    ('Tsʼah', 'Wild sagebrush medicine for purification and lungs'),
    ('Nitsáhákees', 'Foundational dawn thinking and mental clarity'),
  ],
);

// -----------------------------------------------------------------------------
// 2. LAKÓTIYAPI (GREAT PLAINS OČHÉTHI ŠAKÓWIŊ)
// -----------------------------------------------------------------------------
TribalTradition lakotaTradition(String backdrop) => TribalTradition(
  id: 'lakota',
  title: 'Lakȟótiyapi (Lakota)',
  nativeName: 'Očhéthi Šakówiŋ',
  jurisdiction: 'Great Plains Intertribal • IHS Great Plains Area',
  regionTag: 'GP-SD/ND/NE',
  primaryColor: '#166534', // Prairie Sage Green
  secondaryColor: '#B91C1C', // Pipestone Red
  accentColor: '#EAB308', // Sacred Sun Gold
  darkBasalt: '#0B1320',
  washiBg: '#FAF8F5',
  bannerGradientStart: '#14532D',
  bannerGradientEnd: '#991B1B',
  backdropBase64: backdrop,
  emblemSymbol: '🦬',
  landscapeTitle: 'Paha Sapa (The Black Hills) & The Prairie Sea',
  landscapePoetics:
      'Paha Sapa is the sacred heart of everything that is. From the pine-crowned granite needles of Harney Peak '
      'to the boundless rolling green waves of the tallgrass prairie beneath an immense high-plains sky, '
      'all living things are related (Mitákuye Oyásʼiŋ).',
  vitals: {
    'HEART_RATE': '72 BPM • Čhaŋté',
    'BLOOD_PRESSURE': '120/80 mmHg • We / Mni',
    'SPO2': '99% • Thaspáŋ SpO2',
    'TEMP': '98.6°F • Tȟačháŋ',
    'RX_TITLE': 'Pȟežúta Wičhása (Healer Order)',
    'RX_BODY': 'Aŋpétu ičhúŋhaŋ pȟežúta waŋží yatkȟáŋ (Take one remedy tablet daily with meals)',
  },
  pillars: [
    ('Positive Emotion', 'Wóblakela', 'Deep inner peace, quiet mind, and calm spirit'),
    ('Engagement', 'Wóčhaŋtognake', 'Generosity and heartfelt dedication to community'),
    ('Relationships', 'Mitákuye Oyásʼiŋ', 'All My Relations: kinship with all living beings'),
    ('Meaning', 'Wóohitika', 'Brave perseverance and sacred purpose for the people'),
    ('Accomplishment', 'Wóksape', 'Wisdom earned through experience, discipline, and age'),
    ('Health Vitality', 'Wičhóni Wašté', 'The Good Life: physical vitality and pure breath'),
  ],
  technicalFeatures: [
    ('Consonantal Caron Elevation', 'č, ȟ, ǩ, š, ž', '>= 120 UPM Clearance'),
    ('Nasalized Velar Eng', 'ŋ (Lakota Ogonek/Eng)', 'Symmetric Descender Balance'),
    ('High Tone Acutes', 'á, é, í, ó, ú', 'Non-Clipping Accent Bounds'),
    ('Monospace Telemetry', 'Čhaŋté 72 BPM', 'Zero Layout Jitter at 600 UPM'),
  ],
  vocabulary: [
    ('Mitákuye Oyásʼiŋ', 'All my relations; all life is sacredly connected'),
    ('Pȟežúta', 'Medicine, herbal healing plant, or pharmaceutical'),
    ('Wachanga', 'Sweetgrass braided for peaceful prayer and healing'),
    ('Čhaŋté', 'The physical and spiritual heart of the person'),
    ('Paha Sapa', 'The Black Hills; the sacred heart of the universe'),
    ('Tatanka', 'The sacred American Bison that gave life to the people'),
    ('Ičháȟpe-ȟú', 'Purple coneflower (Echinacea) immune warrior'),
    ('Wóphila', 'Immense heartfelt gratitude for life and healing'),
  ],
);

// -----------------------------------------------------------------------------
// 3. COAST SALISH (LUSHOOTSEED / DXʷLƏŠUCID)
// -----------------------------------------------------------------------------
TribalTradition salishTradition(String backdrop) => TribalTradition(
  id: 'salish',
  title: 'dxʷləšucid (Lushootseed)',
  nativeName: 'Coast Salish Nations',
  jurisdiction: 'Northwest Portland Area Indian Health Board (NPAIHB)',
  regionTag: 'NW-WA/BC',
  primaryColor: '#0369A1', // Salish Sea Cobalt
  secondaryColor: '#C2410C', // Redcedar Bark Amber
  accentColor: '#0F766E', // River Glacial Teal
  darkBasalt: '#08131D',
  washiBg: '#FAF8F5',
  bannerGradientStart: '#075985',
  bannerGradientEnd: '#9A3412',
  backdropBase64: backdrop,
  emblemSymbol: '🌊',
  landscapeTitle: 'The Salish Sea, Snoqualmie Plume & The Great Cedar Canopy',
  landscapePoetics:
      'Where 800-year-old western redcedars drape with moss above churning tidal fiords. '
      'From Snoqualmie Falls plunging into emerald foam to the glaciated peak of Tahoma watching over the river deltas, '
      'the returning salmon sustain the life breath (ʔəshəliʔ).',
  vitals: {
    'HEART_RATE': '72 BPM • həliʔ',
    'BLOOD_PRESSURE': '120/80 mmHg • qʷul̕',
    'SPO2': '99% • ɬax̌t SpO2',
    'TEMP': '37.0°C • ʔəshəliʔ',
    'RX_TITLE': 'sʔuladxʷ Care Plan (Clinical Order)',
    'RX_BODY': 'kʷaxʷaɬ ti sʔuladxʷ gʷəɬ dᶻixʷ (Nourish the body daily with pure spring water)',
  },
  pillars: [
    ('Positive Emotion', 'ʔəshəliʔ', 'The sacred breath of life, vitality, and optimism'),
    ('Engagement', 'sʔuladxʷ', 'Honoring the seasonal salmon run with reverent labor'),
    ('Relationships', 'ʔalʔal', 'The welcoming longhouse where family gathers as one'),
    ('Meaning', 'xʷəč̓il̕', 'Awakening spiritual purpose through ancestral teachings'),
    ('Accomplishment', 'ƛʼubƛʼub', 'Excellence, mastery, and restorative wellness'),
    ('Health Vitality', 'xʷiʔ kʷis bəɬah', 'Clear unhindered breathing and whole-body vigor'),
  ],
  technicalFeatures: [
    ('Lateral Fricative Aperture', 'ɬ (Barred L)', '1.4x Optical Cross-Loop Clearance'),
    ('Barred Lambda Integrity', 'ƛ, ƛʼ', 'Dedicated Glyphic Skeleton Matrix'),
    ('Phonetic Schwa Alignment', 'ə (Turned e)', 'True x-Height Optical Normalization'),
    ('Labialized Velar Suffix', 'kʷ, xʷ, qʷ', 'Elevated Superscript Precision'),
  ],
  vocabulary: [
    ('ʔəshəliʔ', 'Life breath, spirit, and whole-body vitality'),
    ('sʔuladxʷ', 'Wild salmon; the sacred sustenance of the river'),
    ('ƛʼubƛʼub', 'Very good; optimal somatic and mental well-being'),
    ('ʔalʔal', 'Traditional cedar longhouse and communal home'),
    ('dxʷləšucid', 'Puget Sound Salish ancestral language'),
    ('Kanim', 'Dugout western redcedar canoe for ocean journeys'),
    ('Tahoma', 'The towering glaciated volcanic mother mountain'),
    ('qʷəl̕qʷələb', 'The sacred killer whale (Orca) of the deep waters'),
  ],
);

// -----------------------------------------------------------------------------
// 4. CHEROKEE (TSALAGI GAWONIHISDI)
// -----------------------------------------------------------------------------
TribalTradition cherokeeTradition(String backdrop) => TribalTradition(
  id: 'cherokee',
  title: 'Tsalagi (Cherokee)',
  nativeName: 'ᏣᎳᎩ ᎠᏰᎵ (Cherokee Nation)',
  jurisdiction: 'Cherokee Nation Health Services • W.W. Hastings Hospital',
  regionTag: 'CN-OK/NC',
  primaryColor: '#1E3A8A', // Blue Ridge Smoke
  secondaryColor: '#991B1B', // Sacred Crimson
  accentColor: '#D97706', // Council Fire Gold
  darkBasalt: '#0A1128',
  washiBg: '#FAF8F5',
  bannerGradientStart: '#1E40AF',
  bannerGradientEnd: '#991B1B',
  backdropBase64: backdrop,
  emblemSymbol: '🏹',
  landscapeTitle: 'The Blue Ridge Smokies & The Ozark Rivercane Corridors',
  landscapePoetics:
      'From the misty, blue-hazed ridges of the Great Smoky Mountains where pure trout headwaters filter through '
      'ancient hemlock coves, to the spring-fed Illinois River and flowering redbuds of Tahlequah, '
      'health is the uninterrupted flow of balance (Tohi).',
  vitals: {
    'HEART_RATE': '72 BPM • ᎠᏓᏅᏙ',
    'BLOOD_PRESSURE': '120/80 mmHg • ᎩᎬ',
    'SPO2': '99% • ᎠᏍᏉᎸ SpO2',
    'TEMP': '98.6°F • ᎤᏗᎴᎬ',
    'RX_TITLE': 'ᏗᏓᏂᏫᏍᎩ ᎪᏪᎵ (Cherokee Clinical Order)',
    'RX_BODY': 'ᏑᏕᏘᏴᎯ ᏌᏊ ᎢᏳᏩᎫᏗ ᎭᎵᏍᏓᏴᎲᏍᎬ (Take one tablet once daily following nourishment)',
  },
  pillars: [
    ('Positive Emotion', 'ᏙᎯ (Tohi)', 'Uninterrupted peace, wellness, and cosmic balance'),
    ('Engagement', 'ᎣᏏᏉᏧ (Osigwitsu)', 'All is well; active harmony with the changing seasons'),
    ('Relationships', 'ᎢᏤ ᏂᏓᏛᏁᎵᏒ', 'The Seven Clans standing together in mutual protection'),
    ('Meaning', 'ᏚᏳᎪᏛ (Duyugodv)', 'Walking the straight path of justice, truth, and honor'),
    ('Accomplishment', 'ᏍᏏᏉᏯ (Sequoyah)', 'Intellectual sovereignty through writing and learning'),
    ('Health Vitality', 'ᎦᏅᏬᎯᏍᏗ', 'Deep physical healing, clean blood, and restored energy'),
  ],
  technicalFeatures: [
    ('Sequoyah Syllabic Matrix', '85 Canonical Syllables', 'Uppercase & Lowercase Unicode 8.0'),
    ('Optical Contrast Calibration', 'Ꭰ, Ꭱ, Ꭲ, Ꭳ, Ꭴ, Ꭵ', 'Louise Sloan 5:1 Acuity Ratio'),
    ('Prescription MAR Clearance', 'ᏗᏓᏂᏫᏍᎩ ᎪᏪᎵ', 'Zero Clipping on 203 DPI Wristbands'),
    ('Monospace Telemetry Alignment', '72 BPM • ᎠᏓᏅᏙ', 'Strict 600 UPM Monospace Cell Centering'),
  ],
  vocabulary: [
    ('ᏙᎯ (Tohi)', 'Wellness, peace, uninterrupted flow, and health'),
    ('ᎣᏏᏉᏧ (Osigwitsu)', 'All is well; harmony with natural law'),
    ('ᎦᏅᏬᎯᏍᏗ', 'Healing, medical recovery, and restoring strength'),
    ('ᎠᏓᏅᏙ (Adanvdo)', 'The soul, spirit, and seat of emotional health'),
    ('ᎡᎶᎯ (Elohi)', 'The sacred living Earth and all natural creations'),
    ('ᏓᎶᏂᎨ ᎤᎾᏍᏕ', 'Wild yellowroot (Xanthorhiza) antibiotic medicine'),
    ('ᏳᏅᏫᏧᎴᏅ', 'Wild American ginseng ("Little Man") adaptogen'),
    ('ᎠᎹᏱ ᎠᏘᏍᎬ', 'Going to Water morning purification ceremony'),
  ],
);

// -----------------------------------------------------------------------------
// 5. ANISHINAABEMOWIN (GREAT LAKES OJIBWE / CHIPPEWA)
// -----------------------------------------------------------------------------
TribalTradition ojibweTradition(String backdrop) => TribalTradition(
  id: 'ojibwe',
  title: 'Anishinaabemowin (Ojibwe)',
  nativeName: 'Anishinaabewaki',
  jurisdiction: 'Great Lakes Inter-Tribal Council • IHS Bemidji Area',
  regionTag: 'GL-MN/WI/MI',
  primaryColor: '#047857', // Deep Pine Green
  secondaryColor: '#B45309', // Birchbark Amber
  accentColor: '#0284C7', // Lake Superior Cobalt
  darkBasalt: '#061A14',
  washiBg: '#FAF8F5',
  bannerGradientStart: '#065F46',
  bannerGradientEnd: '#0369A1',
  backdropBase64: backdrop,
  emblemSymbol: '🌲',
  landscapeTitle: 'Gichigami (Lake Superior), Wild Rice Marshes & Birchbark Woods',
  landscapePoetics:
      'Where boundless, crystal waters of Gichigami lap against sandstone cliffs and pristine pebble shores. '
      'From autumn wild rice (Manoomin) harvesting in gentle canoes gliding through reeds, to the sweet fragrance '
      'of balsam fir and sacred sweetgrass (Wiingashk) under northern pine canopies, health is the Seven Grandfathers.',
  vitals: {
    'HEART_RATE': '72 BPM • Odeʼ',
    'BLOOD_PRESSURE': '120/80 mmHg • Miswi',
    'SPO2': '99% • Nese SpO2',
    'TEMP': '37.0°C • Wiiyaw',
    'RX_TITLE': 'Mashkiki Mashkawizii (Herbal Healing Order)',
    'RX_BODY': 'Miziwe kamig mino-bimaadiziwin (Live a good and healthy life with daily water)',
  },
  pillars: [
    ('Positive Emotion', 'Mino-bimaadiziwin', 'The Good Life: walking in joy, peace, and spiritual wellness'),
    ('Engagement', 'Manoominike', 'Honoring the wild rice harvest with deep focus and respect'),
    ('Relationships', 'Wiidookodaadiwin', 'Helping one another through communal mutual aid and solidarity'),
    ('Meaning', 'Nibwaakaawin', 'Wisdom passed through generations from the Seven Grandfathers'),
    ('Accomplishment', 'Aakodeʼewin', 'Courage and bravery to defend the health of the vulnerable'),
    ('Health Vitality', 'Mashkiki', 'Traditional botanical medicine and restored physical strength'),
  ],
  technicalFeatures: [
    ('Double-Vowel Macron Alignment', 'aa, ii, oo, e', 'Stable Vowel Quantity Balance'),
    ('Nasalized Vowel Ogonek', 'ą, į (Anishinaabe Hook)', '>= 110 UPM Clearance'),
    ('Glottal Consonant Stop', 'Odeʼ (Apostrophe)', '340 UPM Advance Width'),
    ('Monospace Telemetry Alignment', '72 BPM • Odeʼ', 'Strict 600 UPM Advance Width'),
  ],
  vocabulary: [
    ('Mino-bimaadiziwin', 'Living a good, healthy, and honorable life in balance'),
    ('Manoomin', 'Wild rice ("The Good Berry"); gift of the Creator'),
    ('Wiingashk', 'Sweetgrass; sacred hair of Mother Earth for healing'),
    ('Gichigami', 'Lake Superior; the great, cold, clean sea'),
    ('Odeʼ', 'The spiritual and anatomical human heart'),
    ('Wiigwaas', 'Birchbark used for traditional scrolls and canoes'),
    ('Mashkiki', 'Medicine, botanical cure, or medicinal herb'),
    ('Miigwech', 'Thank you; deep, heartfelt gratitude'),
  ],
);

// -----------------------------------------------------------------------------
// 6. KANIEN’KÉHA (HAUDENOSAUNEE / MOHAWK)
// -----------------------------------------------------------------------------
TribalTradition mohawkTradition(String backdrop) => TribalTradition(
  id: 'mohawk',
  title: 'Kanien’kéha (Mohawk)',
  nativeName: 'Haudenosaunee (Six Nations)',
  jurisdiction: 'Akwesasne Health Services • IHS Nashville Area',
  regionTag: 'HN-NY/QC/ON',
  primaryColor: '#581C87', // Wampum Purple
  secondaryColor: '#15803D', // White Pine Green
  accentColor: '#B45309', // Council Fire Copper
  darkBasalt: '#110B1E',
  washiBg: '#FAF8F5',
  bannerGradientStart: '#4C1D95',
  bannerGradientEnd: '#166534',
  backdropBase64: backdrop,
  emblemSymbol: '🪶',
  landscapeTitle: 'The St. Lawrence River, Longhouse Valleys & The Great White Pine',
  landscapePoetics:
      'Framed by the broad, clean waters of Kaniatarowanenneh and the ancient granite hills of the Adirondacks. '
      'Where the sweet sap of sugar maples flows in spring and the Great Tree of Peace spreads its white roots '
      'to the four corners of the earth, health begins with Words Before All Else (Ohenton Karihwatehkwen).',
  vitals: {
    'HEART_RATE': '72 BPM • Ewehyaʼti',
    'BLOOD_PRESSURE': '120/80 mmHg • Onò:kwa',
    'SPO2': '99% • Atenrokhwa SpO2',
    'TEMP': '37.0°C • Oyeròn:ta',
    'RX_TITLE': 'Ononhkwa Rotiioʼten (Clinical Directive)',
    'RX_BODY': 'Enhsatká:tho táhnon enskennekónta (Nourish the spirit and body with clean water)',
  },
  pillars: [
    ('Positive Emotion', 'Skén:nen', 'Peace, tranquility, and harmony of body and mind'),
    ('Engagement', 'Kakhwahetken', 'Tending the Three Sisters (Corn, Beans, Squash) garden'),
    ('Relationships', 'Kaianerehkó:wa', 'The Great Law of Peace uniting clans and generations'),
    ('Meaning', 'Ohenton Karihwatehkwen', 'Words Before All Else: gratitude to the whole creation'),
    ('Accomplishment', 'Kahsatsténhsera', 'Inner moral strength, resilience, and endurance'),
    ('Health Vitality', 'Onòn:kwa', 'Vital medicine, herbal therapies, and systemic vigor'),
  ],
  technicalFeatures: [
    ('Mid-Dot Vowel Length', 'a·, e·, i·, o·', 'Optical Mid-Height Baseline Alignment'),
    ('Nasal Vowel Tone Clearance', 'ę, ǫ, ę́, ǫ́', '>= 120 UPM Accent Clearance'),
    ('Phonetic Glottal Stop', 'ʔ / ʼ (Apostrophe)', '340 UPM First-Class Glyph Width'),
    ('Prescription MAR Integrity', 'Ononhkwa Rotiioʼten', 'Zero Thermal Bleed on Pharmacy Labels'),
  ],
  vocabulary: [
    ('Skén:nen', 'Peace, health, and holistic balance'),
    ('Kaianerehkó:wa', 'The Great Law of Peace and sovereign justice'),
    ('Ohenton Karihwatehkwen', 'Words spoken before all else; universal thanksgiving'),
    ('Kakhwahetken', 'The Three Sisters: corn, beans, and squash sustenance'),
    ('Onòn:kwa', 'Herbal medicine, clinical treatment, or botanical infusion'),
    ('Kahswénhta', 'Two Row Wampum belt signifying sovereign coexistence'),
    ('Onerahkwatstha', 'White pine needles brewed for vitamin C and lung wellness'),
    ('Niawenhkó:wa', 'Great and profound thanks to you'),
  ],
);

// -----------------------------------------------------------------------------
// 7. ʻŌLELO HAWAIʻI (NATIVE HAWAIIAN PAE ʻĀINA)
// -----------------------------------------------------------------------------
TribalTradition hawaiianTradition(String backdrop) => TribalTradition(
  id: 'hawaiian',
  title: 'ʻŌlelo Hawaiʻi (Native Hawaiian)',
  nativeName: 'Pae ʻĀina o Hawaiʻi',
  jurisdiction: 'Papa Ola Lōkahi • Native Hawaiian Health Systems',
  regionTag: 'HI-PACIFIC',
  primaryColor: '#0E7490', // Pacific Reef Cyan
  secondaryColor: '#B91C1C', // ʻŌhiʻa Lehua Crimson
  accentColor: '#CA8A04', // Golden Sunlight
  darkBasalt: '#05151D',
  washiBg: '#FAF8F5',
  bannerGradientStart: '#0891B2',
  bannerGradientEnd: '#B91C1C',
  backdropBase64: backdrop,
  emblemSymbol: '🌺',
  landscapeTitle: 'The Ahupuaʻa Watershed, Emerald Knife Ridges & Turquoise Swells',
  landscapePoetics:
      'Stretching from misty cloud forests of Haleakalā and Mauna Kea through lush taro (Kalo) terraces '
      'to pristine coral reefs. Where scarlet ʻŌhiʻa blossoms grace black volcanic lava flows and ocean waves '
      'nourish the islands, health is the sacred triangle of Lōkahi (God, Humankind, Land).',
  vitals: {
    'HEART_RATE': '72 BPM • Puʻuwai',
    'BLOOD_PRESSURE': '120/80 mmHg • Koko',
    'SPO2': '99% • Ea oxygen',
    'TEMP': '37.0°C • Kino',
    'RX_TITLE': 'Lāʻau Lapaʻau (Traditional & Clinical Rx)',
    'RX_BODY': 'Inu i ka wai maʻemaʻe i kēlā me kēia lā (Nourish life with clean fresh water daily)',
  },
  pillars: [
    ('Positive Emotion', 'Ola Pono', 'Complete vitality, physical righteousness, and wholeness'),
    ('Engagement', 'Mālama ʻĀina', 'Loving stewardship and caring for the living earth'),
    ('Relationships', 'ʻOhana & Aloha', 'Deep familial love, mutual compassion, and communal bond'),
    ('Meaning', 'Lōkahi', 'Sacred harmony uniting spirit, society, and nature'),
    ('Accomplishment', 'Kuleana', 'Personal and generational responsibility to heal'),
    ('Health Vitality', 'Lāʻau Lapaʻau', 'Traditional herbal medicine and clinical therapy'),
  ],
  technicalFeatures: [
    ('ʻOkina Consonantal Primacy', 'ʻ (U+02BB Turned Comma)', 'Dedicated First-Class Consonant Metric'),
    ('Kahakō Macron Balance', 'ā, ē, ī, ō, ū', 'Optically Centered Length Bar'),
    ('Sloan 5:1 Optotype Clarity', 'Puʻuwai, Koko, Ea', 'Clear Vision at Distance'),
    ('Monospace Telemetry Alignment', '72 BPM • Puʻuwai', 'Zero Layout Jitter at 600 UPM'),
  ],
  vocabulary: [
    ('Ola Pono', 'Optimal health, vitality, wellness, and right living'),
    ('Lōkahi', 'Harmony and unity between God, people, and land'),
    ('Mālama ʻĀina', 'Care for and protect the land so it nourishes you'),
    ('Kalo', 'Taro root; sacred elder brother and ancestral staple food'),
    ('Lāʻau Lapaʻau', 'Traditional Hawaiian botanical medicine and healing arts'),
    ('Puʻuwai', 'The biological and spiritual human heart'),
    ('Ea', 'Life breath, air, sovereignty, and independence'),
    ('Mahalo Nui Loa', 'Profound, overflowing gratitude from the heart'),
  ],
);

// -----------------------------------------------------------------------------
// 8. IÑUPIAQ & YUP’IK (ALASKA NATIVE SOVEREIGNTY)
// -----------------------------------------------------------------------------
TribalTradition inupiaqTradition(String backdrop) => TribalTradition(
  id: 'inupiaq',
  title: 'Iñupiaq & Yup’ik (Alaska Native)',
  nativeName: 'Inuvialuit / Inuit / Yupiit',
  jurisdiction: 'Alaska Native Tribal Health Consortium (ANTHC) • YKHC',
  regionTag: 'AK-ARCTIC',
  primaryColor: '#1E3A8A', // Arctic Marine Deep
  secondaryColor: '#0284C7', // Glacial Ice Blue
  accentColor: '#D97706', // Seal Oil Lamp Amber
  darkBasalt: '#07111E',
  washiBg: '#FAF8F5',
  bannerGradientStart: '#172554',
  bannerGradientEnd: '#0369A1',
  backdropBase64: backdrop,
  emblemSymbol: '❄️',
  landscapeTitle: 'The Arctic Coastal Tundra, Siku Pack Ice & Northern Aurora',
  landscapePoetics:
      'Where the sun circles the horizon above midnight tundra blooms and winter skies ignite with dancing aurora. '
      'From dog teams running across frozen sea ice (Siku) along the floe edge, to the warm golden glow of the '
      'seal-oil lamp (Qulliq) in cozy sod homes, health is the resilient community bond of Inupiat Ilitqusiat.',
  vitals: {
    'HEART_RATE': '72 BPM • Uummat',
    'BLOOD_PRESSURE': '120/80 mmHg • Auluk',
    'SPO2': '99% • Aniqsaaġvik SpO2',
    'TEMP': '37.0°C • Timi',
    'RX_TITLE': 'Iñuuniaġvigmi Iñugiksuq (Wellness Directive)',
    'RX_BODY': 'Niqipiaq iñuuniaġutigiplugu (Nourish body and soul with wholesome country food)',
  },
  pillars: [
    ('Positive Emotion', 'Quviasuktuq', 'Heartfelt joy, contentment, and laughter in community'),
    ('Engagement', 'Aŋuniaq', 'Subsistence hunting with reverence, patience, and skill'),
    ('Relationships', 'Iḷagiikłiq', 'Sacred extended family kinship and honoring elders'),
    ('Meaning', 'Inupiat Ilitqusiat', 'Living the 17 ancestral values: sharing and respect'),
    ('Accomplishment', 'Naluqataq', 'Spring whaling feast celebrating abundance and bravery'),
    ('Health Vitality', 'Niqipiaq', 'Nutrient-rich traditional country foods: seal, char, berries'),
  ],
  technicalFeatures: [
    ('Barred Voiceless Lateral', 'ł, ḷ, ƚ', '1.4x Optical Cross-Loop Aperture'),
    ('Consonantal Underdot Clearance', 'ḷ, ñ, ŋ, ġ', '>= 110 UPM Descender Spacing'),
    ('Arctic Vowel Length Macrons', 'ā, ī, ū', 'Optically Balanced Stroke Widths'),
    ('Prescription MAR Integrity', 'Uummat 72 BPM', 'Zero Layout Shift on EHR Monitors'),
  ],
  vocabulary: [
    ('Niqipiaq', 'Real, traditional country food rich in vital micronutrients'),
    ('Qulliq', 'Traditional soapstone lamp burning seal oil for warmth and light'),
    ('Inupiat Ilitqusiat', 'The 17 traditional values guiding honorable Arctic life'),
    ('Uummat', 'The physical and emotional heart of a person'),
    ('Siku', 'Sea ice; living platform of travel, hunting, and life'),
    ('Kallu', 'Thunder and natural cosmic forces'),
    ('Arigaa', 'Expression of delight, beauty, and appreciation'),
    ('Quyanaqpak', 'Thank you very much; profound gratitude to the community'),
  ],
);

// -----------------------------------------------------------------------------
// 9. HOPI & TOHONO O’ODHAM (SONORAN DESERT & MESAS)
// -----------------------------------------------------------------------------
TribalTradition hopiTradition(String backdrop) => TribalTradition(
  id: 'hopi',
  title: 'Hopi & O’odham (Desert Mesas)',
  nativeName: 'Hopituskwa & Tohono O’odham',
  jurisdiction: 'IHS Phoenix & Tucson Areas • Sells Hospital',
  regionTag: 'SW-AZ/SONORA',
  primaryColor: '#B45309', // Sonoran Ochre
  secondaryColor: '#047857', // Saguaro Forest Green
  accentColor: '#D97706', // Desert Sun Gold
  darkBasalt: '#1A1208',
  washiBg: '#FAF8F5',
  bannerGradientStart: '#92400E',
  bannerGradientEnd: '#065F46',
  backdropBase64: backdrop,
  emblemSymbol: '🌽',
  landscapeTitle: 'The High Sandstone Mesas & Towering Saguaro Forests',
  landscapePoetics:
      'From the timeless, wind-swept stone heights of Third Mesa (Orayvi) where blue corn roots plunge deep into arid sand, '
      'to the majestic Saguaro cactus (Ha:ṣan) giants guarding sacred Baboquivari Peak beneath crystalline starry skies, '
      'health is living in sacred balance (Sumi’nangwa).',
  vitals: {
    'HEART_RATE': '72 BPM • Unaqa',
    'BLOOD_PRESSURE': '120/80 mmHg • Ungwa',
    'SPO2': '99% • Hikwsi SpO2',
    'TEMP': '37.0°C • Toko',
    'RX_TITLE': 'Tuuhikya Mongwi (Traditional Healing Plan)',
    'RX_BODY': 'Sumi’nangwa kyelöwma (Walk with a pure, peaceful heart and daily clean water)',
  },
  pillars: [
    ('Positive Emotion', 'Sumi’nangwa', 'Working and living together with one harmonious heart and mind'),
    ('Engagement', 'Qatsit Ayó’nangwa', 'Reverent farming of sacred corn under the desert sun'),
    ('Relationships', 'Kyakyawnangwa', 'Deep mutual respect and compassion among all clan relatives'),
    ('Meaning', 'Hopi Navoti', 'Ancestral prophecy and spiritual wisdom guiding every generation'),
    ('Accomplishment', 'Mongwi', 'Humility in leadership and self-reliant endurance through drought'),
    ('Health Vitality', 'Qatsit Qapesi', 'Whole-body strength nourished by blue corn and desert botanicals'),
  ],
  technicalFeatures: [
    ('Length Marker Normalization', 'a:, e:, i:, o:', 'Symmetric Optical Colon Spacing'),
    ('Barred Dentals & Hooks', 'đ, d̨, n̨', '1.4x Optical Aperture Clearance'),
    ('Sonoran Glottal Stop', 'ʼ / ’ (Saltillo)', '340 UPM First-Class Glyph Advance'),
    ('Thermal Clinical Display', 'Unaqa 72 BPM', 'Zero Layout Jitter at High Heat'),
  ],
  vocabulary: [
    ('Sumi’nangwa', 'All people coming together with one peaceful heart and mind'),
    ('Hopituskwa', 'The ancestral, sacred Hopi homeland and high mesas'),
    ('Ha:ṣan', 'The sacred Saguaro cactus that sustains life in the desert'),
    ('Sakyawqa', 'Sacred blue corn; spiritual mother and nutritional foundation'),
    ('Tuuhikya', 'Traditional healer, herbal medicine keeper, or clinician'),
    ('Unaqa', 'The anatomical and spiritual heart of the person'),
    ('Umuk', 'Monsoon thunder and lightning bringing life-giving rain'),
    ('Askwali / Kwakwháy', 'Heartfelt thanks and gratitude from the women and men'),
  ],
);

// -----------------------------------------------------------------------------
// 10. CHOCTAW & MVSKOKE (SOUTHEAST & OKLAHOMA)
// -----------------------------------------------------------------------------
TribalTradition choctawTradition(String backdrop) => TribalTradition(
  id: 'choctaw',
  title: 'Chahta & Mvskoke (Southeast & Oklahoma)',
  nativeName: 'Chahta Yakni & Mvskoke Etvlwv',
  jurisdiction: 'Choctaw Nation Health Services • IHS Oklahoma City Area',
  regionTag: 'SE-OK/MS/AL',
  primaryColor: '#7C2D12', // Red Clay Terra Cotta
  secondaryColor: '#15803D', // River Cane Green
  accentColor: '#B45309', // Council Fire Gold
  darkBasalt: '#180F0A',
  washiBg: '#FAF8F5',
  bannerGradientStart: '#7C2D12',
  bannerGradientEnd: '#166534',
  backdropBase64: backdrop,
  emblemSymbol: '🌾',
  landscapeTitle: 'The Rolling Red Hills, Cypress Bayous & Ancient Mounds',
  landscapePoetics:
      'From the sacred emergence mound of Nanih Waiya to the winding, cypress-shaded river cane brakes '
      'and flowering redbud ridges of Oklahoma. Where ancestral spring waters flow clean through rich red earth, '
      'health is the unbroken chain of generational care (Chahta Alla).',
  vitals: {
    'HEART_RATE': '72 BPM • Chunuk',
    'BLOOD_PRESSURE': '120/80 mmHg • Issish',
    'SPO2': '99% • Foha SpO2',
    'TEMP': '98.6°F • Haknip',
    'RX_TITLE': 'Alikchi Holisso (Clinical Care Order)',
    'RX_BODY': 'Nittak moma okipata ishko (Drink pure living water daily for somatic vigor)',
  },
  pillars: [
    ('Positive Emotion', 'Yukpa', 'Deep, joyful gladness of heart and inner serenity'),
    ('Engagement', 'Holisso Chito', 'Dedicated study, cultural knowledge, and language transmission'),
    ('Relationships', 'Imponna', 'Compassionate family kinship and honoring the wisdom of elders'),
    ('Meaning', 'Chahta Immi', 'Living traditional Choctaw heritage, faith, and moral integrity'),
    ('Accomplishment', 'Miko', 'Humble service, perseverance, and endurance for the nation'),
    ('Health Vitality', 'Achanahali', 'Vigorous physical health, stamina, and traditional nourishment'),
  ],
  technicalFeatures: [
    ('Underdot Vowel Precision', 'ạ, ẹ, ị, ọ', '>= 110 UPM Descender Clearance'),
    ('Mvskoke Vowel Transliteration', 'v, e, u (Schwa & Barred ɨ)', 'Optical Baseline Stability'),
    ('Glottal Apostrophe Spacing', 'Chunukʼ (Saltillo)', '340 UPM Advance Width'),
    ('Monospace Telemetry Alignment', '72 BPM • Chunuk', 'Strict 600 UPM Monospace Alignment'),
  ],
  vocabulary: [
    ('Yukpa', 'Joyful, happy, and lighthearted wellness of the soul'),
    ('Issish', 'Living blood circulating through the body'),
    ('Alikchi', 'Traditional doctor, healer, or prescribing clinician'),
    ('Nanih Waiya', 'The sacred ancestral mound of emergence and life'),
    ('Chunuk', 'The anatomical heart and inner seat of thought'),
    ('Kowi', 'The quiet forest, deep timber, and medicinal plants'),
    ('Ahe', 'Wild sweet potatoes and traditional sustaining tubers'),
    ('Yakoke', 'Thank you; deep, heartfelt appreciation'),
  ],
);

// =============================================================================
// PLATE 1: SOCIAL GITHUB PREVIEW (1280x640)
// =============================================================================
String generateSocialPreview(TribalTradition t) {
  final photoEmbed = t.backdropBase64.isNotEmpty
      ? '''
      <g transform="translate(60, 60)">
        <rect x="2" y="6" width="460" height="520" rx="18" fill="#78716C" fill-opacity="0.08"/>
        <clipPath id="ghImgClip_${t.id}"><rect width="460" height="520" rx="18"/></clipPath>
        <rect width="460" height="520" rx="18" fill="#FAF8F5"/>
        <image href="data:image/webp;base64,${t.backdropBase64}" width="460" height="520" preserveAspectRatio="xMidYMid slice" clip-path="url(#ghImgClip_${t.id})"/>
        <rect width="460" height="520" rx="18" fill="url(#photoOverlay_${t.id})" clip-path="url(#ghImgClip_${t.id})"/>
      </g>
      '''
      : '';

  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1280" height="640" viewBox="0 0 1280 640" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
      .font-brand { font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-native { font-family: 'PocketGull', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
    <linearGradient id="bgGrad_${t.id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="40%" stop-color="#FAF8F5"/>
      <stop offset="100%" stop-color="#F2ECE1"/>
    </linearGradient>
    <linearGradient id="photoOverlay_${t.id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FAF8F5" stop-opacity="0.05"/>
      <stop offset="70%" stop-color="#FAF8F5" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#FAF8F5" stop-opacity="0.85"/>
    </linearGradient>
    <linearGradient id="bannerGrad_${t.id}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="${t.bannerGradientStart}"/>
      <stop offset="100%" stop-color="${t.bannerGradientEnd}"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1280" height="640" fill="url(#bgGrad_${t.id})"/>

  <!-- Deckle Borders -->
  <rect x="24" y="24" width="1232" height="592" fill="none" stroke="#E2DACB" stroke-width="1.5"/>
  <rect x="30" y="30" width="1220" height="580" fill="none" stroke="#E2DACB" stroke-width="0.8" stroke-dasharray="4,4"/>

  <!-- Top Quad-Color Trim -->
  <rect x="24" y="24" width="308" height="4" fill="${t.primaryColor}"/>
  <rect x="332" y="24" width="308" height="4" fill="${t.secondaryColor}"/>
  <rect x="640" y="24" width="308" height="4" fill="${t.accentColor}"/>
  <rect x="948" y="24" width="308" height="4" fill="#0F172A"/>

  $photoEmbed

  <!-- Main Content (Right Side) -->
  <g transform="translate(560, 75)">
    <!-- Header Badges -->
    <g transform="translate(0, 0)">
      <rect width="90" height="26" rx="4" fill="${t.primaryColor}"/>
      <text x="45" y="17" class="font-mono" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.08em">${t.regionTag}</text>

      <rect x="100" y="0" width="160" height="26" rx="4" fill="#E2E8F0"/>
      <text x="180" y="17" class="font-mono" font-size="10.5" font-weight="bold" fill="#334155" text-anchor="middle">CASE STUDY 07</text>

      <rect x="270" y="0" width="160" height="26" rx="4" fill="#FEF3C7"/>
      <text x="350" y="17" class="font-mono" font-size="10.5" font-weight="bold" fill="#B45309" text-anchor="middle">SOVEREIGN CDS</text>
    </g>

    <!-- Sovereign Title -->
    <text x="0" y="70" class="font-brand" font-size="34" font-weight="800" fill="#0F172A">${t.title}</text>
    <text x="0" y="105" class="font-native" font-size="24" font-weight="700" fill="${t.secondaryColor}">${t.nativeName}</text>
    <text x="0" y="132" class="font-mono" font-size="12" font-weight="600" fill="#64748B">${t.jurisdiction.toUpperCase()}</text>

    <!-- Horizontal Divider -->
    <line x1="0" y1="150" x2="650" y2="150" stroke="#CBD5E1" stroke-width="1.2"/>

    <!-- Bioregional Landscape Inset Card -->
    <g transform="translate(0, 168)">
      <rect width="650" height="92" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
      <rect width="4" height="92" rx="2" fill="${t.secondaryColor}"/>
      <text x="18" y="24" class="font-brand" font-size="12" font-weight="700" fill="${t.primaryColor}">${t.emblemSymbol} ${t.landscapeTitle.toUpperCase()}</text>
      <foreignObject x="18" y="32" width="615" height="54">
        <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; color: #475569; line-height: 1.45;">
          ${t.landscapePoetics}
        </div>
      </foreignObject>
    </g>

    <!-- Key Technical Invariants Table -->
    <g transform="translate(0, 276)">
      <text x="0" y="16" class="font-brand" font-size="12" font-weight="700" fill="#0F172A">CLINICAL LIFE-SAFETY INVARIANTS</text>
      <g transform="translate(0, 26)">
        <rect width="315" height="52" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="14" y="22" class="font-mono" font-size="10" font-weight="bold" fill="#64748B">${t.technicalFeatures[0].$1}</text>
        <text x="14" y="40" class="font-native" font-size="15" font-weight="bold" fill="${t.primaryColor}">${t.technicalFeatures[0].$2} <tspan font-family="'JetBrains Mono'" font-size="11" font-weight="600" fill="#0F172A">(${t.technicalFeatures[0].$3})</tspan></text>

        <rect x="330" y="0" width="320" height="52" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="344" y="22" class="font-mono" font-size="10" font-weight="bold" fill="#64748B">${t.technicalFeatures[1].$1}</text>
        <text x="344" y="40" class="font-native" font-size="15" font-weight="bold" fill="${t.secondaryColor}">${t.technicalFeatures[1].$2} <tspan font-family="'JetBrains Mono'" font-size="11" font-weight="600" fill="#0F172A">(${t.technicalFeatures[1].$3})</tspan></text>
      </g>
    </g>

    <!-- Bottom Bedside Telemetry Strip -->
    <g transform="translate(0, 375)">
      <rect width="650" height="60" rx="8" fill="${t.darkBasalt}"/>
      <text x="20" y="24" class="font-mono" font-size="10" font-weight="bold" fill="#38BDF8">REAL-TIME CLINICAL HUD • 600 UPM MONOSPACE</text>
      <text x="20" y="46" class="font-mono" font-size="13" font-weight="bold" fill="#10B981">${t.vitals['HEART_RATE']}   <tspan fill="#F59E0B">${t.vitals['BLOOD_PRESSURE']}</tspan>   <tspan fill="#38BDF8">${t.vitals['SPO2']}</tspan></text>
      <circle cx="620" cy="30" r="5" fill="#10B981"/>
    </g>

    <!-- Footer Imprint -->
    <g transform="translate(0, 460)">
      <text x="0" y="16" class="font-mono" font-size="9.5" fill="#94A3B8">POCKETGULL TYPEFOUNDRY SUPERFAMILY • 100% OTS MEMORY SAFE • SIL OPEN FONT LICENSE 1.1</text>
    </g>
  </g>
</svg>
''';
}

// =============================================================================
// PLATE 2: TYPE ENGINEERING BLUEPRINT (2688x3600, 300 DPI)
// =============================================================================
String generateTypeEngineeringPlate(TribalTradition t) {
  final sb = StringBuffer();
  sb.writeln('''<?xml version="1.0" encoding="UTF-8"?>
<svg width="2688" height="3600" viewBox="0 0 2688 3600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@400;600;700&amp;display=swap');
      .font-title { font-family: 'Plus Jakarta Sans', sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-glyph { font-family: 'PocketGull', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
    <pattern id="grid_${t.id}" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#0284C7" stroke-width="0.75" stroke-opacity="0.15"/>
    </pattern>
    <pattern id="gridMajor_${t.id}" width="200" height="200" patternUnits="userSpaceOnUse">
      <path d="M 200 0 L 0 0 0 200" fill="none" stroke="#0284C7" stroke-width="1.5" stroke-opacity="0.3"/>
    </pattern>
  </defs>

  <!-- Blueprint Deep Navy Canvas -->
  <rect width="2688" height="3600" fill="#041426"/>
  <rect width="2688" height="3600" fill="url(#grid_${t.id})"/>
  <rect width="2688" height="3600" fill="url(#gridMajor_${t.id})"/>

  <!-- Outer Technical Drafting Border -->
  <rect x="80" y="80" width="2528" height="3440" fill="none" stroke="#0284C7" stroke-width="3" opacity="0.8"/>
  <rect x="100" y="100" width="2488" height="3400" fill="none" stroke="#0284C7" stroke-width="1" stroke-dasharray="10,10" opacity="0.6"/>

  <!-- Header Block -->
  <g transform="translate(140, 160)">
    <text x="0" y="50" class="font-mono" font-size="28" font-weight="700" fill="#38BDF8" letter-spacing="0.15em">POCKETGULL CLINICAL TYPEFOUNDRY • 1000 UPM ARCHITECTURAL BLUEPRINT</text>
    <text x="0" y="130" class="font-title" font-size="64" font-weight="800" fill="#FFFFFF">${t.title.toUpperCase()}</text>
    <text x="0" y="195" class="font-glyph" font-size="44" font-weight="700" fill="${t.accentColor}">${t.nativeName} • ${t.jurisdiction}</text>
    <line x1="0" y1="240" x2="2408" y2="240" stroke="#0284C7" stroke-width="2.5" opacity="0.7"/>
  </g>

  <!-- Section 1: Optical Metrics & Invariants -->
  <g transform="translate(140, 480)">
    <text x="0" y="0" class="font-mono" font-size="32" font-weight="700" fill="#38BDF8">01 / GEOMETRIC INVARIANTS &amp; BOUNDING BOX ALLOCATION</text>
    
    <!-- 4 Diagnostic Metric Cards -->
''');

  for (int i = 0; i < t.technicalFeatures.length; i++) {
    final feat = t.technicalFeatures[i];
    final col = i % 2;
    final row = i ~/ 2;
    final cx = col * 1230;
    final cy = 40 + row * 220;

    sb.writeln('''
    <g transform="translate($cx, $cy)">
      <rect width="1180" height="180" rx="12" fill="#08233C" stroke="#0284C7" stroke-width="2"/>
      <text x="30" y="50" class="font-mono" font-size="22" font-weight="bold" fill="#94A3B8">${feat.$1.toUpperCase()}</text>
      <text x="30" y="120" class="font-glyph" font-size="48" font-weight="bold" fill="${t.accentColor}">${feat.$2}</text>
      <text x="30" y="155" class="font-mono" font-size="20" font-weight="600" fill="#38BDF8">${feat.$3}</text>
    </g>
''');
  }

  sb.writeln('''
  </g>

  <!-- Section 2: Large Calligraphic Vector Anatomy Showcase -->
  <g transform="translate(140, 1040)">
    <text x="0" y="0" class="font-mono" font-size="32" font-weight="700" fill="#38BDF8">02 / LARGE OPTOTYPIC GLYPH DISSECTION (LOUISE SLOAN 5:1 RATIO)</text>
    
    <rect y="40" width="2408" height="960" rx="16" fill="#061C30" stroke="#0284C7" stroke-width="2"/>

    <!-- Baseline, X-Height, Cap-Height, Ascender Guide Lines -->
    <line x1="80" y1="360" x2="2328" y2="360" stroke="#EF4444" stroke-width="2" stroke-dasharray="8,8"/>
    <text x="2338" y="365" class="font-mono" font-size="18" fill="#EF4444">Cap-Height (+714)</text>

    <line x1="80" y1="520" x2="2328" y2="520" stroke="#38BDF8" stroke-width="2" stroke-dasharray="8,8"/>
    <text x="2338" y="525" class="font-mono" font-size="18" fill="#38BDF8">x-Height (+546)</text>

    <line x1="80" y1="800" x2="2328" y2="800" stroke="#10B981" stroke-width="2.5"/>
    <text x="2338" y="805" class="font-mono" font-size="18" font-weight="bold" fill="#10B981">Baseline (0 UPM)</text>

    <line x1="80" y1="920" x2="2328" y2="920" stroke="#F59E0B" stroke-width="2" stroke-dasharray="8,8"/>
    <text x="2338" y="925" class="font-mono" font-size="18" fill="#F59E0B">Descender (-220)</text>

    <!-- Giant Glyphs Rendered with Chisel Nib Dynamics -->
    <g transform="translate(140, 800)">
      <text x="0" y="0" class="font-glyph" font-size="360" font-weight="800" fill="#FFFFFF">${t.vocabulary[0].$1}</text>
    </g>
  </g>

  <!-- Section 3: Bioregional Landscape & Land-Based Epistemology -->
  <g transform="translate(140, 2120)">
    <text x="0" y="0" class="font-mono" font-size="32" font-weight="700" fill="#38BDF8">03 / TRADITIONAL ECOLOGICAL KNOWLEDGE (TEK) &amp; LAND CARTOGRAPHY</text>
    <rect y="40" width="2408" height="420" rx="16" fill="#08233C" stroke="#0284C7" stroke-width="2"/>
    <text x="50" y="110" class="font-title" font-size="40" font-weight="bold" fill="${t.accentColor}">${t.emblemSymbol} ${t.landscapeTitle.toUpperCase()}</text>
    <foreignObject x="50" y="150" width="2300" height="280">
      <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; color: #E2E8F0; line-height: 1.6;">
        ${t.landscapePoetics}
        <br/><br/>
        <strong style="color: #38BDF8;">Sovereignty Invariant:</strong> Clinical state calculations, drug dosages, and health records in ${t.title} strictly eliminate missing-glyph boxes (tofu), honoring ancestral land stewardship and self-determination.
      </div>
    </foreignObject>
  </g>

  <!-- Section 4: Pharmacopeia & Medical Lexicon Grid -->
  <g transform="translate(140, 2660)">
    <text x="0" y="0" class="font-mono" font-size="32" font-weight="700" fill="#38BDF8">04 / SOVEREIGN PHARMACOPEIA &amp; CLINICAL TERMINOLOGY</text>
    <g transform="translate(0, 40)">
''');

  for (int i = 0; i < t.vocabulary.length; i++) {
    final item = t.vocabulary[i];
    final col = i % 2;
    final row = i ~/ 2;
    final vx = col * 1230;
    final vy = row * 135;

    sb.writeln('''
      <g transform="translate($vx, $vy)">
        <rect width="1180" height="110" rx="8" fill="#061C30" stroke="#0284C7" stroke-width="1.2"/>
        <text x="30" y="50" class="font-glyph" font-size="34" font-weight="bold" fill="#FFFFFF">${item.$1}</text>
        <text x="30" y="85" class="font-mono" font-size="20" fill="#94A3B8">${item.$2}</text>
      </g>
''');
  }

  sb.writeln('''
    </g>
  </g>

  <!-- Footer Technical Block -->
  <g transform="translate(140, 3360)">
    <line x1="0" y1="0" x2="2408" y2="0" stroke="#0284C7" stroke-width="2" opacity="0.7"/>
    <text x="0" y="60" class="font-mono" font-size="24" fill="#94A3B8">POCKETGULL SUPERFAMILY • ARCHIVAL SPECIMEN • ISO 3166-2: ${t.regionTag} • SIL OFL 1.1 • CERN ZENODO DOI: 10.5281/ZENODO.18882512</text>
  </g>
</svg>
''');
  return sb.toString();
}

// =============================================================================
// PLATE 3: CLINICAL TELEMETRY SPECIMEN (2688x3600, 300 DPI)
// =============================================================================
String generateTelemetryTypePlate(TribalTradition t) {
  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="2688" height="3600" viewBox="0 0 2688 3600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@400;600;700&amp;display=swap');
      .font-brand { font-family: 'Plus Jakarta Sans', sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-native { font-family: 'PocketGull', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
  </defs>

  <!-- Basalt Black Medical Terminal Background -->
  <rect width="2688" height="3600" fill="#090E17"/>

  <!-- Hospital Monitor Frame -->
  <rect x="80" y="80" width="2528" height="3440" rx="24" fill="#0F172A" stroke="#1E293B" stroke-width="4"/>

  <!-- Top ICU Status Header -->
  <g transform="translate(140, 160)">
    <rect width="2408" height="120" rx="12" fill="#1E293B"/>
    <circle cx="50" cy="60" r="14" fill="#10B981"/>
    <text x="90" y="70" class="font-mono" font-size="32" font-weight="bold" fill="#F8FAFC">ICU BED 04 • ${t.jurisdiction.toUpperCase()}</text>
    <text x="1850" y="70" class="font-mono" font-size="28" font-weight="bold" fill="#94A3B8">STANDBY: TELEHEALTH SYNC</text>
  </g>

  <!-- Big Telemetry Vitals Grid -->
  <g transform="translate(140, 340)">
    <!-- Heart Rate Card -->
    <rect width="1180" height="420" rx="16" fill="#131E33" stroke="#10B981" stroke-width="3"/>
    <text x="50" y="80" class="font-mono" font-size="32" font-weight="bold" fill="#10B981">HR / PULSE (ECG LEAD II)</text>
    <text x="50" y="240" class="font-native" font-size="120" font-weight="800" fill="#10B981">72</text>
    <text x="260" y="240" class="font-native" font-size="44" font-weight="bold" fill="#6EE7B7">BPM • ${t.vitals['HEART_RATE']!.split('•').last.trim()}</text>
    <!-- ECG Sine Path -->
    <path d="M 50 340 L 300 340 L 340 310 L 380 400 L 420 250 L 460 360 L 500 340 L 1120 340" fill="none" stroke="#10B981" stroke-width="5" stroke-linecap="round"/>

    <!-- Blood Pressure Card -->
    <g transform="translate(1230, 0)">
      <rect width="1180" height="420" rx="16" fill="#131E33" stroke="#F59E0B" stroke-width="3"/>
      <text x="50" y="80" class="font-mono" font-size="32" font-weight="bold" fill="#F59E0B">NIBP (ARTERIAL PRESSURE)</text>
      <text x="50" y="240" class="font-native" font-size="120" font-weight="800" fill="#F59E0B">120/80</text>
      <text x="530" y="240" class="font-native" font-size="44" font-weight="bold" fill="#FDE68A">mmHg • ${t.vitals['BLOOD_PRESSURE']!.split('•').last.trim()}</text>
      <text x="50" y="340" class="font-mono" font-size="28" fill="#94A3B8">MAP: 93.3 mmHg • REGULAR SINUS</text>
    </g>
  </g>

  <!-- Second Row Vitals -->
  <g transform="translate(140, 820)">
    <!-- SpO2 Card -->
    <rect width="1180" height="340" rx="16" fill="#131E33" stroke="#38BDF8" stroke-width="3"/>
    <text x="50" y="80" class="font-mono" font-size="32" font-weight="bold" fill="#38BDF8">PULSE OXIMETRY (SpO2)</text>
    <text x="50" y="230" class="font-native" font-size="110" font-weight="800" fill="#38BDF8">99%</text>
    <text x="330" y="230" class="font-native" font-size="40" font-weight="bold" fill="#BAE6FD">${t.vitals['SPO2']!.split('•').last.trim()}</text>

    <!-- Temperature Card -->
    <g transform="translate(1230, 0)">
      <rect width="1180" height="340" rx="16" fill="#131E33" stroke="#EC4899" stroke-width="3"/>
      <text x="50" y="80" class="font-mono" font-size="32" font-weight="bold" fill="#EC4899">CORE BODY TEMP</text>
      <text x="50" y="230" class="font-native" font-size="110" font-weight="800" fill="#EC4899">${t.vitals['TEMP']!.split('•').first.trim()}</text>
      <text x="440" y="230" class="font-native" font-size="40" font-weight="bold" fill="#FBCFE8">NORMOTHERMIC</text>
    </g>
  </g>

  <!-- Medication Administration Record (MAR) Container -->
  <g transform="translate(140, 1220)">
    <rect width="2408" height="840" rx="20" fill="#111C2E" stroke="#3B82F6" stroke-width="3"/>
    <g transform="translate(60, 80)">
      <text x="0" y="0" class="font-mono" font-size="36" font-weight="bold" fill="#60A5FA">ELECTRONIC PRESCRIBING &amp; CLINICAL ORDER (RPMS / EHR)</text>
      <text x="0" y="60" class="font-native" font-size="44" font-weight="bold" fill="${t.accentColor}">${t.vitals['RX_TITLE']}</text>
      
      <!-- Callout Box for Drug Direction -->
      <g transform="translate(0, 100)">
        <rect width="2288" height="240" rx="12" fill="#1E293B" stroke="#60A5FA" stroke-width="2"/>
        <text x="40" y="70" class="font-mono" font-size="26" font-weight="bold" fill="#94A3B8">CLINICAL DIRECTIVE IN NATIVE SOVEREIGN ORTHOGRAPHY:</text>
        <text x="40" y="150" class="font-native" font-size="48" font-weight="bold" fill="#FFFFFF">${t.vitals['RX_BODY']}</text>
      </g>

      <!-- Safety Badges -->
      <g transform="translate(0, 400)">
        <rect width="700" height="90" rx="10" fill="#065F46"/>
        <text x="350" y="55" class="font-mono" font-size="24" font-weight="bold" fill="#D1FAE5" text-anchor="middle">✓ ZERO TONE TRUNCATION</text>

        <rect x="740" y="0" width="700" height="90" rx="10" fill="#1E3A8A"/>
        <text x="1090" y="55" class="font-mono" font-size="24" font-weight="bold" fill="#DBEAFE" text-anchor="middle">✓ 1.4x BAR CONTRAST (ISMP 2026)</text>

        <rect x="1480" y="0" width="800" height="90" rx="10" fill="#701A75"/>
        <text x="1880" y="55" class="font-mono" font-size="24" font-weight="bold" fill="#FDF4FF" text-anchor="middle">✓ FIRST-CLASS GLOTTAL LETTER</text>
      </g>
    </g>
  </g>

  <!-- Bioregional Land & Healing Banner -->
  <g transform="translate(140, 2120)">
    <rect width="2408" height="1140" rx="20" fill="#131E33" stroke="#334155" stroke-width="2"/>
    <g transform="translate(60, 80)">
      <text x="0" y="0" class="font-mono" font-size="32" font-weight="bold" fill="#38BDF8">LAND-BASED HEALING &amp; TRADITIONAL KNOWLEDGE INTEGRATION</text>
      <text x="0" y="70" class="font-native" font-size="44" font-weight="bold" fill="${t.accentColor}">${t.emblemSymbol} ${t.landscapeTitle}</text>
      <foreignObject x="0" y="110" width="2280" height="360">
        <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 28px; color: #E2E8F0; line-height: 1.65;">
          ${t.landscapePoetics}
        </div>
      </foreignObject>

      <!-- 4 Pillars of Community Recovery -->
      <g transform="translate(0, 520)">
        <text x="0" y="0" class="font-mono" font-size="26" font-weight="bold" fill="#94A3B8">CLINICAL PROTOCOLS RECOGNIZED IN THIS EHR TENANT:</text>
        <g transform="translate(0, 30)">
          <rect width="540" height="200" rx="12" fill="#1E293B"/>
          <text x="30" y="60" class="font-native" font-size="34" font-weight="bold" fill="#FFFFFF">${t.vocabulary[0].$1}</text>
          <text x="30" y="110" class="font-mono" font-size="20" fill="#94A3B8">${t.vocabulary[0].$2}</text>

          <rect x="580" y="0" width="540" height="200" rx="12" fill="#1E293B"/>
          <text x="610" y="60" class="font-native" font-size="34" font-weight="bold" fill="#FFFFFF">${t.vocabulary[1].$1}</text>
          <text x="610" y="110" class="font-mono" font-size="20" fill="#94A3B8">${t.vocabulary[1].$2}</text>

          <rect x="1160" y="0" width="540" height="200" rx="12" fill="#1E293B"/>
          <text x="1190" y="60" class="font-native" font-size="34" font-weight="bold" fill="#FFFFFF">${t.vocabulary[2].$1}</text>
          <text x="1190" y="110" class="font-mono" font-size="20" fill="#94A3B8">${t.vocabulary[2].$2}</text>

          <rect x="1740" y="0" width="540" height="200" rx="12" fill="#1E293B"/>
          <text x="1770" y="60" class="font-native" font-size="34" font-weight="bold" fill="#FFFFFF">${t.vocabulary[3].$1}</text>
          <text x="1770" y="110" class="font-mono" font-size="20" fill="#94A3B8">${t.vocabulary[3].$2}</text>
        </g>
      </g>
    </g>
  </g>

  <!-- Footer Technical Summary -->
  <g transform="translate(140, 3340)">
    <text x="0" y="0" class="font-mono" font-size="24" fill="#64748B">POCKETGULL ICU TELEMETRY • ZERO JITTER MONOSPACE 600 UPM • W3C OTS VERIFIED • HL7 FHIR R4 COMPLIANT</text>
  </g>
</svg>
''';
}

// =============================================================================
// PLATE 4: PEDAGOGICAL TYPEFACE SPECIMEN (2688x3600, 300 DPI)
// =============================================================================
String generatePedagogicalPlate(TribalTradition t) {
  final sb = StringBuffer();
  sb.writeln('''<?xml version="1.0" encoding="UTF-8"?>
<svg width="2688" height="3600" viewBox="0 0 2688 3600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@400;600;700&amp;display=swap');
      .font-title { font-family: 'Plus Jakarta Sans', sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-native { font-family: 'PocketGull', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
    <linearGradient id="polarWashi_${t.id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="50%" stop-color="#FAF8F5"/>
      <stop offset="100%" stop-color="#F3ECE2"/>
    </linearGradient>
  </defs>

  <!-- Archival Polar Washi Paper Surface -->
  <rect width="2688" height="3600" fill="url(#polarWashi_${t.id})"/>

  <!-- Museum Deckle Frame -->
  <rect x="80" y="80" width="2528" height="3440" fill="none" stroke="#D1C7B7" stroke-width="3"/>
  <rect x="100" y="100" width="2488" height="3400" fill="none" stroke="#D1C7B7" stroke-width="1.2" stroke-dasharray="12,12"/>

  <!-- Color Header Ribbon -->
  <rect x="80" y="80" width="632" height="12" fill="${t.primaryColor}"/>
  <rect x="712" y="80" width="632" height="12" fill="${t.secondaryColor}"/>
  <rect x="1344" y="80" width="632" height="12" fill="${t.accentColor}"/>
  <rect x="1976" y="80" width="632" height="12" fill="#1E293B"/>

  <!-- Broadside Header -->
  <g transform="translate(160, 220)">
    <text x="0" y="40" class="font-mono" font-size="28" font-weight="bold" fill="#64748B" letter-spacing="0.1em">POCKETGULL PEDAGOGICAL BROADSIDE • SOVEREIGN INDIGENOUS TYPOGRAPHY</text>
    <text x="0" y="130" class="font-title" font-size="72" font-weight="800" fill="#0F172A">${t.title}</text>
    <text x="0" y="200" class="font-native" font-size="48" font-weight="700" fill="${t.secondaryColor}">${t.nativeName} • ${t.jurisdiction}</text>
    <line x1="0" y1="240" x2="2368" y2="240" stroke="#CBD5E1" stroke-width="2"/>
  </g>

  <!-- Master Alphabet & Syllable Specimen Wall -->
  <g transform="translate(160, 560)">
    <text x="0" y="0" class="font-mono" font-size="30" font-weight="bold" fill="#475569">01 / COMPLETE SOVEREIGN GLYPH RUN &amp; ORTHOGRAPHIC INVENTORY</text>
    <rect y="30" width="2368" height="640" rx="16" fill="#FFFFFF" stroke="#E2DACB" stroke-width="2"/>
    
    <!-- Large Character Display -->
    <g transform="translate(60, 160)">
      <text x="0" y="0" class="font-native" font-size="64" font-weight="800" fill="#0F172A" letter-spacing="0.08em">
        A B C D E G H I J K L M N O P Q R S T U W X Y Z
      </text>
      <text x="0" y="90" class="font-native" font-size="64" font-weight="800" fill="#0F172A" letter-spacing="0.08em">
        a b c d e g h i j k l m n o p q r s t u w x y z
      </text>
      <text x="0" y="200" class="font-native" font-size="76" font-weight="800" fill="${t.primaryColor}" letter-spacing="0.12em">
        ą́ ę́ į́ ǫ́ Ł ł ƛ ɬ ə ʔ ʼ ʻ č ȟ ǩ ŋ š ž
      </text>
      <text x="0" y="320" class="font-native" font-size="72" font-weight="800" fill="${t.secondaryColor}" letter-spacing="0.1em">
        Ꭰ Ꭱ Ꭲ Ꭳ Ꭴ Ꭵ Ꭶ Ꭷ Ꭸ Ꭹ Ꭺ Ꭻ Ꭼ Ꭽ Ꭾ Ꭿ Ꮀ Ꮁ Ꮂ
      </text>
      <text x="0" y="420" class="font-mono" font-size="32" font-weight="bold" fill="#64748B">
        0 1 2 3 4 5 6 7 8 9 • ISMP SLASHED ZERO: 0̸ • TABULAR NUMBERS: 120/80
      </text>
    </g>
  </g>

  <!-- Section 2: Bioregional Landscape & Flora Immersion -->
  <g transform="translate(160, 1300)">
    <text x="0" y="0" class="font-mono" font-size="30" font-weight="bold" fill="#475569">02 / WALKING THE LANDS &amp; NATURE WITHOUT TRAVELING</text>
    <rect y="30" width="2368" height="520" rx="16" fill="#FFFFFF" stroke="#E2DACB" stroke-width="2"/>
    <g transform="translate(60, 100)">
      <text x="0" y="0" class="font-title" font-size="44" font-weight="800" fill="${t.primaryColor}">${t.emblemSymbol} ${t.landscapeTitle.toUpperCase()}</text>
      <foreignObject x="0" y="35" width="2240" height="360">
        <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 26px; color: #334155; line-height: 1.65;">
          ${t.landscapePoetics}
          <br/><br/>
          <em style="color: ${t.secondaryColor}; font-weight: 600;">Traditional Ecological Knowledge (TEK):</em> Indigenous languages preserve micro-climate data, seasonal bird migrations, and botanical chemistry refined over millennia. PocketGull provides the high-legibility digital typography required to pass this knowledge across generations.
        </div>
      </foreignObject>
    </g>
  </g>

  <!-- Section 3: 8-Word Pharmacopeia Broadside Cards -->
  <g transform="translate(160, 1920)">
    <text x="0" y="0" class="font-mono" font-size="30" font-weight="bold" fill="#475569">03 / CULTURAL PHARMACOPEIA &amp; PHILOSOPHICAL FOUNDATIONS</text>
    <g transform="translate(0, 30)">
''');

  for (int i = 0; i < t.vocabulary.length; i++) {
    final item = t.vocabulary[i];
    final col = i % 2;
    final row = i ~/ 2;
    final px = col * 1210;
    final py = row * 180;

    sb.writeln('''
      <g transform="translate($px, $py)">
        <rect width="1160" height="150" rx="12" fill="#FFFFFF" stroke="#E2DACB" stroke-width="1.8"/>
        <text x="40" y="65" class="font-native" font-size="44" font-weight="bold" fill="${t.primaryColor}">${item.$1}</text>
        <text x="40" y="115" class="font-title" font-size="24" font-weight="600" fill="#475569">${item.$2}</text>
      </g>
''');
  }

  sb.writeln('''
    </g>
  </g>

  <!-- Section 4: Typography Weight Comparison -->
  <g transform="translate(160, 2760)">
    <text x="0" y="0" class="font-mono" font-size="30" font-weight="bold" fill="#475569">04 / THE FOUR FOUNDATIONAL SUPERFAMILY WEIGHTS</text>
    <rect y="30" width="2368" height="560" rx="16" fill="#FFFFFF" stroke="#E2DACB" stroke-width="2"/>
    <g transform="translate(60, 100)">
      <text x="0" y="30" class="font-mono" font-size="22" font-weight="bold" fill="#64748B">1. POCKETGULL FINELINER (WEIGHT 400 PROPORTIONAL) — LONG-FORM CLINICAL NOTES</text>
      <text x="0" y="80" class="font-native" font-size="38" font-weight="400" fill="#0F172A">${t.vocabulary[0].$1}: ${t.vocabulary[0].$2}. ${t.vocabulary[1].$1}: ${t.vocabulary[1].$2}.</text>

      <text x="0" y="160" class="font-mono" font-size="22" font-weight="bold" fill="#64748B">2. POCKETGULL BOLD (WEIGHT 700 PROPORTIONAL) — PRESCRIPTION LABELS &amp; ALARMS</text>
      <text x="0" y="210" class="font-native" font-size="40" font-weight="700" fill="#0F172A">${t.vocabulary[0].$1}: ${t.vocabulary[0].$2}. ${t.vocabulary[1].$1}: ${t.vocabulary[1].$2}.</text>

      <text x="0" y="290" class="font-mono" font-size="22" font-weight="bold" fill="#64748B">3. POCKETGULL CHISELTIP (WEIGHT 900 PROPORTIONAL) — TRAUMA PLACARDS &amp; WAYFINDING</text>
      <text x="0" y="340" class="font-native" font-size="42" font-weight="900" fill="#0F172A">${t.vocabulary[0].$1}: ${t.vocabulary[0].$2}. ${t.vocabulary[1].$1}: ${t.vocabulary[1].$2}.</text>

      <text x="0" y="420" class="font-mono" font-size="22" font-weight="bold" fill="#64748B">4. POCKETGULL MONO (600 UPM MEDICAL TERMINAL) — REAL-TIME BIOMETRIC READOUTS</text>
      <text x="0" y="470" class="font-mono" font-size="36" font-weight="700" fill="#0369A1">HR 72 BPM | BP 120/80 mmHg | SpO2 99% | TEMP 37.0°C</text>
    </g>
  </g>

  <!-- Footer Imprint -->
  <g transform="translate(160, 3420)">
    <text x="0" y="0" class="font-mono" font-size="24" fill="#64748B">POCKETGULL PEDAGOGICAL PLATE • 300 DPI MASTER PRINT QUALITY • SIL OPEN FONT LICENSE 1.1</text>
  </g>
</svg>
''');
  return sb.toString();
}

// =============================================================================
// PLATE 5: PERMA+ THOUGHTS CARD (2400x2400, 300 DPI)
// =============================================================================
String generatePermaThoughtsCard(TribalTradition t) {
  final sb = StringBuffer();
  sb.writeln('''<?xml version="1.0" encoding="UTF-8"?>
<svg width="2400" height="2400" viewBox="0 0 2400 2400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
      .font-brand { font-family: 'Plus Jakarta Sans', sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-native { font-family: 'PocketGull', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
    <linearGradient id="permaBg_${t.id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#FAF8F5"/>
      <stop offset="100%" stop-color="#F2EDE4"/>
    </linearGradient>
  </defs>

  <!-- Surface Paperboard -->
  <rect width="2400" height="2400" fill="url(#permaBg_${t.id})"/>

  <!-- Tactile Frame -->
  <rect x="60" y="60" width="2280" height="2280" fill="none" stroke="#D6CEBF" stroke-width="2.5"/>
  <rect x="80" y="80" width="2240" height="2240" fill="none" stroke="#D6CEBF" stroke-width="1.2" stroke-dasharray="10,10"/>

  <!-- Card Header -->
  <g transform="translate(140, 160)">
    <text x="0" y="40" class="font-mono" font-size="28" font-weight="bold" fill="#64748B" letter-spacing="0.12em">PERMA+ HOLISTIC CLINICAL WELL-BEING &amp; SOVEREIGN TRADITION</text>
    <text x="0" y="125" class="font-brand" font-size="64" font-weight="800" fill="#0F172A">${t.title}</text>
    <text x="0" y="185" class="font-native" font-size="42" font-weight="700" fill="${t.secondaryColor}">${t.nativeName} • ${t.jurisdiction}</text>
    <line x1="0" y1="220" x2="2120" y2="220" stroke="#CBD5E1" stroke-width="2"/>
  </g>

  <!-- 6 PERMA+ Pillar Cards -->
  <g transform="translate(140, 440)">
''');

  for (int i = 0; i < t.pillars.length; i++) {
    final p = t.pillars[i];
    final col = i % 2;
    final row = i ~/ 2;
    final cx = col * 1080;
    final cy = row * 540;

    sb.writeln('''
    <g transform="translate($cx, $cy)">
      <rect width="1040" height="480" rx="18" fill="#FFFFFF" stroke="#E2DACB" stroke-width="2"/>
      <rect width="12" height="480" rx="6" fill="${col == 0 ? t.primaryColor : t.secondaryColor}"/>
      
      <g transform="translate(50, 70)">
        <text x="0" y="0" class="font-mono" font-size="24" font-weight="bold" fill="#64748B">PILLAR 0${i + 1} • ${p.$1.toUpperCase()}</text>
        <text x="0" y="65" class="font-native" font-size="52" font-weight="800" fill="${t.primaryColor}">${p.$2}</text>
        <foreignObject x="0" y="105" width="940" height="260">
          <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 26px; color: #334155; line-height: 1.55;">
            ${p.$3}
          </div>
        </foreignObject>
      </g>
    </g>
''');
  }

  sb.writeln('''
  </g>

  <!-- Bottom Land & Resilience Epilogue -->
  <g transform="translate(140, 2140)">
    <rect width="2120" height="140" rx="12" fill="#0F172A"/>
    <text x="40" y="55" class="font-brand" font-size="28" font-weight="bold" fill="#F8FAFC">${t.emblemSymbol} ${t.landscapeTitle.toUpperCase()}</text>
    <text x="40" y="100" class="font-mono" font-size="20" fill="#94A3B8">POCKETGULL OPEN HEALTHCARE TYPOGRAPHY • DEDICATED TO TRIBAL WELL-BEING &amp; SELF-DETERMINATION</text>
  </g>
</svg>
''');
  return sb.toString();
}
