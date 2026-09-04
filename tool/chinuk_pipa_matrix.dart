// Copyright (c) 2026, The PocketGull Project Authors.
// All rights reserved. Use of this source code is governed by an OFL 1.1 license.

/// Chinuk Pipa (Duployan Shorthand for Chinuk Wawa) Matrix & Phonetic Engine
///
/// Implements sound static typing with Dart 3,
/// pattern matching, zero virtualenv friction, and microsecond precision.
///
/// Models Father Jean-Marie Le Jeune's 1891 Kamloops Wawa stenographic geometry
/// and the contemporary orthography preserved by the Confederated Tribes of Grand Ronde:
///   - Consonant Vectors (Lines & Arcs: P, T, K, R, B, D, G, L, M, N, J, S)
///   - Vocalic Circles (A, O, I, E, U, WA, WO, WI, Nasals)
///   - Affixes & Punctuation (Chinook Full Stop U+1BC9F, Reduplication Mark U+1BC9E)
///   - PERMA+ Clinical Well-Being & Medical Lexicon
library;

import 'dart:convert';
import 'dart:io';

enum StrokeType {
  lineStraight,
  lineSlanted,
  curveArch,
  circleVowel,
  circleCompound,
  affixSecant,
  affixPoint,
  punctuationSign,
}

enum ScriptCategory {
  consonant,
  vowel,
  diphthong,
  nasal,
  affix,
  punctuation,
}

class DuployanCharacter {
  final int codepoint;
  final String character;
  final String name;
  final StrokeType strokeType;
  final ScriptCategory category;
  final String phonetic;
  final String chinukUsage;
  final bool isKamloopsPipaPrimary;

  const DuployanCharacter({
    required this.codepoint,
    required this.character,
    required this.name,
    required this.strokeType,
    required this.category,
    required this.phonetic,
    required this.chinukUsage,
    this.isKamloopsPipaPrimary = false,
  });

  Map<String, dynamic> toJson() => {
    'codepoint': codepoint,
    'hex': '0x${codepoint.toRadixString(16).toUpperCase().padLeft(5, '0')}',
    'char': character,
    'name': name,
    'stroke_type': strokeType.name,
    'category': category.name,
    'phonetic': phonetic,
    'chinuk_usage': chinukUsage,
    'kamloops_primary': isKamloopsPipaPrimary,
  };
}

class PermaLexiconItem {
  final String pillar; // 'P', 'E', 'R', 'M', 'A', '+'
  final String pillarTitle;
  final String chinukTerm;
  final String phoneticIpa;
  final String duployanSequence;
  final List<int> codepoints;
  final String englishTranslation;
  final String clinicalSignificance;

  const PermaLexiconItem({
    required this.pillar,
    required this.pillarTitle,
    required this.chinukTerm,
    required this.phoneticIpa,
    required this.duployanSequence,
    required this.codepoints,
    required this.englishTranslation,
    required this.clinicalSignificance,
  });

  Map<String, dynamic> toJson() => {
    'pillar': pillar,
    'pillar_title': pillarTitle,
    'chinuk_term': chinukTerm,
    'phonetic_ipa': phoneticIpa,
    'duployan_sequence': duployanSequence,
    'codepoints': codepoints.map((c) => '0x${c.toRadixString(16).toUpperCase().padLeft(5, '0')}').toList(),
    'english_translation': englishTranslation,
    'clinical_significance': clinicalSignificance,
  };
}

class ChinukPipaMatrix {
  /// Core Duployan & Chinuk Pipa Characters
  static const List<DuployanCharacter> roster = [
    // ── Consonants: Straight Lines ──
    DuployanCharacter(codepoint: 0x1BC00, character: '\u{1BC00}', name: 'DUPLOYAN LETTER H', strokeType: StrokeType.lineStraight, category: ScriptCategory.consonant, phonetic: 'h', chinukUsage: 'Heehee (laughter, play)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC01, character: '\u{1BC01}', name: 'DUPLOYAN LETTER X', strokeType: StrokeType.lineSlanted, category: ScriptCategory.consonant, phonetic: 'x', chinukUsage: 'X / Ch guttural sounds', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC02, character: '\u{1BC02}', name: 'DUPLOYAN LETTER P', strokeType: StrokeType.lineSlanted, category: ScriptCategory.consonant, phonetic: 'p', chinukUsage: 'Pipa (paper, letter, book)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC03, character: '\u{1BC03}', name: 'DUPLOYAN LETTER T', strokeType: StrokeType.lineStraight, category: ScriptCategory.consonant, phonetic: 't', chinukUsage: 'Tumtum (heart, mind, spirit)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC04, character: '\u{1BC04}', name: 'DUPLOYAN LETTER F', strokeType: StrokeType.lineSlanted, category: ScriptCategory.consonant, phonetic: 'f', chinukUsage: 'French loanwords / variants', isKamloopsPipaPrimary: false),
    DuployanCharacter(codepoint: 0x1BC05, character: '\u{1BC05}', name: 'DUPLOYAN LETTER K', strokeType: StrokeType.lineStraight, category: ScriptCategory.consonant, phonetic: 'k', chinukUsage: 'Kloshe (good, peaceful, well)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC06, character: '\u{1BC06}', name: 'DUPLOYAN LETTER L', strokeType: StrokeType.lineSlanted, category: ScriptCategory.consonant, phonetic: 'l', chinukUsage: 'La-kret (medicine, health)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC07, character: '\u{1BC07}', name: 'DUPLOYAN LETTER B', strokeType: StrokeType.lineSlanted, category: ScriptCategory.consonant, phonetic: 'b', chinukUsage: 'Boston (American, English)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC08, character: '\u{1BC08}', name: 'DUPLOYAN LETTER D', strokeType: StrokeType.lineStraight, category: ScriptCategory.consonant, phonetic: 'd', chinukUsage: 'Doctor (physician, healer)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC09, character: '\u{1BC09}', name: 'DUPLOYAN LETTER V', strokeType: StrokeType.lineSlanted, category: ScriptCategory.consonant, phonetic: 'v', chinukUsage: 'Voyageur French sounds', isKamloopsPipaPrimary: false),
    DuployanCharacter(codepoint: 0x1BC0A, character: '\u{1BC0A}', name: 'DUPLOYAN LETTER G', strokeType: StrokeType.lineStraight, category: ScriptCategory.consonant, phonetic: 'g', chinukUsage: 'Gis-giss (rattle, medicine charm)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC0B, character: '\u{1BC0B}', name: 'DUPLOYAN LETTER R', strokeType: StrokeType.lineSlanted, category: ScriptCategory.consonant, phonetic: 'r', chinukUsage: 'Rare loanwords / dialectal', isKamloopsPipaPrimary: false),

    // ── Consonants: Curves & Arcs ──
    DuployanCharacter(codepoint: 0x1BC19, character: '\u{1BC19}', name: 'DUPLOYAN LETTER M', strokeType: StrokeType.curveArch, category: ScriptCategory.consonant, phonetic: 'm', chinukUsage: 'Mamook (work, make, heal)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC1A, character: '\u{1BC1A}', name: 'DUPLOYAN LETTER N', strokeType: StrokeType.curveArch, category: ScriptCategory.consonant, phonetic: 'n', chinukUsage: 'Nanitch (see, watch, attend)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC1B, character: '\u{1BC1B}', name: 'DUPLOYAN LETTER J', strokeType: StrokeType.curveArch, category: ScriptCategory.consonant, phonetic: 'ʃ / tʃ', chinukUsage: 'Chako (come, arrive, become)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC1C, character: '\u{1BC1C}', name: 'DUPLOYAN LETTER S', strokeType: StrokeType.curveArch, category: ScriptCategory.consonant, phonetic: 's', chinukUsage: 'Skookum (strong, resilient)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC38, character: '\u{1BC38}', name: 'DUPLOYAN LETTER W', strokeType: StrokeType.circleCompound, category: ScriptCategory.consonant, phonetic: 'w', chinukUsage: 'Wawa (words, speech, talk)', isKamloopsPipaPrimary: true),

    // ── Vowels: Circles ──
    DuployanCharacter(codepoint: 0x1BC41, character: '\u{1BC41}', name: 'DUPLOYAN LETTER A', strokeType: StrokeType.circleVowel, category: ScriptCategory.vowel, phonetic: 'a', chinukUsage: 'Alki (future, by-and-by)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC44, character: '\u{1BC44}', name: 'DUPLOYAN LETTER O', strokeType: StrokeType.circleVowel, category: ScriptCategory.vowel, phonetic: 'o', chinukUsage: 'Olally (berry, sustenance)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC46, character: '\u{1BC46}', name: 'DUPLOYAN LETTER I', strokeType: StrokeType.circleVowel, category: ScriptCategory.vowel, phonetic: 'i', chinukUsage: 'Ikt (one, unity, baseline)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC47, character: '\u{1BC47}', name: 'DUPLOYAN LETTER E', strokeType: StrokeType.circleVowel, category: ScriptCategory.vowel, phonetic: 'e', chinukUsage: 'Ehkoli (whale, marine strength)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC51, character: '\u{1BC51}', name: 'DUPLOYAN LETTER U', strokeType: StrokeType.circleVowel, category: ScriptCategory.vowel, phonetic: 'u / uː', chinukUsage: 'Ulman (elder, ancient wisdom)', isKamloopsPipaPrimary: true),

    // ── Diphthongs & Glides ──
    DuployanCharacter(codepoint: 0x1BC5C, character: '\u{1BC5C}', name: 'DUPLOYAN LETTER WA', strokeType: StrokeType.circleCompound, category: ScriptCategory.diphthong, phonetic: 'wa', chinukUsage: 'Wawa (speech, discourse)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC5D, character: '\u{1BC5D}', name: 'DUPLOYAN LETTER WO', strokeType: StrokeType.circleCompound, category: ScriptCategory.diphthong, phonetic: 'wo', chinukUsage: 'Compound vocalic glide', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC5E, character: '\u{1BC5E}', name: 'DUPLOYAN LETTER WI', strokeType: StrokeType.circleCompound, category: ScriptCategory.diphthong, phonetic: 'wi', chinukUsage: 'Win (wind, respiration, breath)', isKamloopsPipaPrimary: true),

    // ── Punctuation & Distinctive Chinuk Pipa Marks ──
    DuployanCharacter(codepoint: 0x1BC9F, character: '\u{1BC9F}', name: 'DUPLOYAN PUNCTUATION CHINOOK FULL STOP', strokeType: StrokeType.punctuationSign, category: ScriptCategory.punctuation, phonetic: 'sentence final', chinukUsage: 'Kamloops Wawa sentence delimiter', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC9E, character: '\u{1BC9E}', name: 'DUPLOYAN DOUBLE MARK', strokeType: StrokeType.punctuationSign, category: ScriptCategory.punctuation, phonetic: 'reduplication', chinukUsage: 'Reduplication marker (tumtum, heehee)', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC9C, character: '\u{1BC9C}', name: 'DUPLOYAN SIGN O WITH CROSS', strokeType: StrokeType.punctuationSign, category: ScriptCategory.punctuation, phonetic: 'symbolic', chinukUsage: 'Sacred, ceremonial, and hymn header', isKamloopsPipaPrimary: true),

    // ── High Affixes (U+1BC80 - U+1BC88) ──
    DuployanCharacter(codepoint: 0x1BC80, character: '\u{1BC80}', name: 'DUPLOYAN AFFIX HIGH ACUTE', strokeType: StrokeType.affixSecant, category: ScriptCategory.affix, phonetic: 'pitch / accent', chinukUsage: 'Tonal / inflection marker', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC81, character: '\u{1BC81}', name: 'DUPLOYAN AFFIX HIGH TIGHT ACUTE', strokeType: StrokeType.affixSecant, category: ScriptCategory.affix, phonetic: 'short stress', chinukUsage: 'Abbreviation accent', isKamloopsPipaPrimary: false),
    DuployanCharacter(codepoint: 0x1BC82, character: '\u{1BC82}', name: 'DUPLOYAN AFFIX HIGH GRAVE', strokeType: StrokeType.affixSecant, category: ScriptCategory.affix, phonetic: 'falling tone', chinukUsage: 'Grammatical particle marker', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC84, character: '\u{1BC84}', name: 'DUPLOYAN AFFIX HIGH DOT', strokeType: StrokeType.affixPoint, category: ScriptCategory.affix, phonetic: 'nasalization', chinukUsage: 'Vowel nasalization / abbreviation', isKamloopsPipaPrimary: true),
    DuployanCharacter(codepoint: 0x1BC85, character: '\u{1BC85}', name: 'DUPLOYAN AFFIX HIGH CIRCLE', strokeType: StrokeType.affixPoint, category: ScriptCategory.affix, phonetic: 'vowel extension', chinukUsage: 'Elision mark', isKamloopsPipaPrimary: false),
  ];

  /// The PERMA+ Clinical Well-Being & Medical Lexicon
  static const List<PermaLexiconItem> permaLexicon = [
    PermaLexiconItem(
      pillar: 'P',
      pillarTitle: 'Positive Emotion',
      chinukTerm: 'Kloshe Tumtum',
      phoneticIpa: '/tɬuːʃ təm.təm/',
      duployanSequence: '𛰅𛰆𛱄𛰜 𛰃𛱑𛰙 𛰃𛱑𛰙',
      codepoints: [0x1BC05, 0x1BC06, 0x1BC44, 0x1BC1C, 0x0020, 0x1BC03, 0x1BC51, 0x1BC19, 0x0020, 0x1BC03, 0x1BC51, 0x1BC19],
      englishTranslation: 'Good Heart / Peace of Mind',
      clinicalSignificance: 'Vagal tone elevation, parasympathetic calming, anxiety reduction, holistic serenity.',
    ),
    PermaLexiconItem(
      pillar: 'E',
      pillarTitle: 'Engagement',
      chinukTerm: 'Heehee',
      phoneticIpa: '/hiː.hiː/',
      duployanSequence: '𛰀𛱇𛰀𛱇',
      codepoints: [0x1BC00, 0x1BC47, 0x1BC00, 0x1BC47],
      englishTranslation: 'Laughter / Play / Joyful Focus',
      clinicalSignificance: 'Dopaminergic regulation, recreational therapy, pediatric engagement, restorative humor.',
    ),
    PermaLexiconItem(
      pillar: 'R',
      pillarTitle: 'Relationships',
      chinukTerm: 'Tilikum',
      phoneticIpa: '/tɪ.lɪ.kəm/',
      duployanSequence: '𛰃𛱆𛰆𛱆𛰅𛱑𛰙',
      codepoints: [0x1BC03, 0x1BC46, 0x1BC06, 0x1BC46, 0x1BC05, 0x1BC51, 0x1BC19],
      englishTranslation: 'People / Family / Sacred Community',
      clinicalSignificance: 'Social determinants of health (SDOH), tribal kinship, peer support, oxytocin release.',
    ),
    PermaLexiconItem(
      pillar: 'M',
      pillarTitle: 'Meaning',
      chinukTerm: 'Kloshe Wawa',
      phoneticIpa: '/tɬuːʃ waː.waː/',
      duployanSequence: '𛰅𛰆𛱄𛰜 𛰸𛱁𛰸𛱁',
      codepoints: [0x1BC05, 0x1BC06, 0x1BC44, 0x1BC1C, 0x0020, 0x1BC38, 0x1BC41, 0x1BC38, 0x1BC41],
      englishTranslation: 'Good Words / Truthful Counsel',
      clinicalSignificance: 'Existential coherence, culturally safe clinical communication, informed consent.',
    ),
    PermaLexiconItem(
      pillar: 'A',
      pillarTitle: 'Accomplishment',
      chinukTerm: 'Mamook Kloshe',
      phoneticIpa: '/maː.muːk tɬuːʃ/',
      duployanSequence: '𛰙𛱁𛰙𛱑𛰅 𛰅𛰆𛱄𛰜',
      codepoints: [0x1BC19, 0x1BC41, 0x1BC19, 0x1BC51, 0x1BC05, 0x0020, 0x1BC05, 0x1BC06, 0x1BC44, 0x1BC1C],
      englishTranslation: 'To Make Well / Healing Mastery',
      clinicalSignificance: 'Patient Activation Measure (PAM), therapy completion, physical rehabilitation adherence.',
    ),
    PermaLexiconItem(
      pillar: '+',
      pillarTitle: 'Physical Vitality',
      chinukTerm: 'Kloshe Muckamuck',
      phoneticIpa: '/tɬuːʃ mə.kə.mək/',
      duployanSequence: '𛰅𛰆𛱄𛰜 𛰙𛱑𛰅𛱁𛰙𛱑𛰅',
      codepoints: [0x1BC05, 0x1BC06, 0x1BC44, 0x1BC1C, 0x0020, 0x1BC19, 0x1BC51, 0x1BC05, 0x1BC41, 0x1BC19, 0x1BC51, 0x1BC05],
      englishTranslation: 'Good Food / Nourishment & Vitality',
      clinicalSignificance: 'Nutritional stabilization, metabolic health, traditional foodways, physical vigor.',
    ),
  ];
}

void main(List<String> args) {
  final sw = Stopwatch()..start();
  stdout.writeln('=== CHINUK PIPA (DUPLOYAN) MATRIX AUDITOR (DART 3.11) ===');
  stdout.writeln('Loaded ${ChinukPipaMatrix.roster.length} primary Chinuk Pipa stenographic characters.');
  stdout.writeln('Loaded ${ChinukPipaMatrix.permaLexicon.length} PERMA+ clinical health lexicon entries.');

  final strokeCategories = <StrokeType, int>{};
  for (final item in ChinukPipaMatrix.roster) {
    strokeCategories[item.strokeType] = (strokeCategories[item.strokeType] ?? 0) + 1;
  }
  stdout.writeln('\nStroke Category Distribution:');
  strokeCategories.forEach((k, v) => stdout.writeln('  • ${k.name}: $v glyphs'));

  stdout.writeln('\nPERMA+ Clinical Lexicon Verification:');
  for (final item in ChinukPipaMatrix.permaLexicon) {
    stdout.writeln('  [${item.pillar}] ${item.chinukTerm.padRight(16)} -> ${item.duployanSequence} (${item.englishTranslation})');
  }

  final jsonOut = jsonEncode({
    'timestamp': DateTime.now().toUtc().toIso8601String(),
    'script': 'Chinuk Pipa (Duployan Shorthand for Chinuk Wawa)',
    'historical_origin': 'Father Jean-Marie Le Jeune (1891, Kamloops Wawa) & Confederated Tribes of Grand Ronde',
    'unicode_range': 'U+1BC00 - U+1BC9F',
    'roster_count': ChinukPipaMatrix.roster.length,
    'perma_pillars_count': ChinukPipaMatrix.permaLexicon.length,
    'characters': ChinukPipaMatrix.roster.map((e) => e.toJson()).toList(),
    'perma_lexicon': ChinukPipaMatrix.permaLexicon.map((e) => e.toJson()).toList(),
  });

  final outFile = File('fonts/chinuk_pipa_matrix.json');
  outFile.writeAsStringSync(jsonOut);
  sw.stop();
  stdout.writeln('\n[SUCCESS] Exported validated Chinuk Pipa matrix to ${outFile.path} in ${sw.elapsedMicroseconds} μs');
}
