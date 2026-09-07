import 'dart:io';
import 'dart:async';
import 'phinney_auditor.dart';
import 'glyph_inspector.dart';

/// ANSI Color & Style codes
class Ansi {
  static const reset = '\x1B[0m';
  static const bold = '\x1B[1m';
  static const dim = '\x1B[2m';
  static const italic = '\x1B[3m';
  static const underline = '\x1B[4m';

  // Truecolor RGB foreground & background
  static String fgRgb(int r, int g, int b) => '\x1B[38;2;${r};${g};${b}m';
  static String bgRgb(int r, int g, int b) => '\x1B[48;2;${r};${g};${b}m';

  // Palette constants matching PocketGull design system
  static final sage = fgRgb(16, 185, 129); // #10b981
  static final sageBg = bgRgb(16, 185, 129);
  static final gold = fgRgb(245, 158, 11); // #f59e0b
  static final goldBg = bgRgb(245, 158, 11);
  static final red = fgRgb(239, 68, 68); // #ef4444
  static final blue = fgRgb(59, 130, 246); // #3b82f6
  static final cyan = fgRgb(6, 182, 212); // #06b6d4
  static final muted = fgRgb(148, 163, 184); // #94a3b8
  static final white = fgRgb(248, 250, 252); // #f8fafc

  static void clear() {
    stdout.write('\x1B[2J\x1B[H');
  }
}

/// Pure Dart Interactive Sanctuary Terminal Workstation
class SanctuaryTui {
  final Directory projectRoot;
  bool _running = true;

  SanctuaryTui({required this.projectRoot});

  Future<void> run() async {
    while (_running) {
      Ansi.clear();
      _renderHeader();
      _renderMenu();

      stdout.write('\n${Ansi.gold}${Ansi.bold}  Select Sanctuary Option [1-6, Q]: ${Ansi.reset}');
      final input = stdin.readLineSync()?.trim().toLowerCase();

      switch (input) {
        case '1':
          await _runBreathingSanctuary();
          break;
        case '2':
          await _runWorldMandorlaOrbit();
          break;
        case '3':
          await _runTwoKnightsConsoleTour();
          break;
        case '4':
          await _runIsmpClinicalDisambiguationTester();
          break;
        case '5':
          await _runForensicFoundryDashboard();
          break;
        case '6':
          await _runPureDartGlyphInspector();
          break;
        case 'q':
        case 'quit':
        case 'exit':
          _running = false;
          print('\n${Ansi.sage}  May calm vision and wholeness accompany your journey. Farewell! 🌿${Ansi.reset}\n');
          break;
        default:
          break;
      }
    }
  }

  void _renderHeader() {
    print('${Ansi.sage}${Ansi.bold}');
    print('  ╔═══════════════════════════════════════════════════════════════════════════╗');
    print('  ║   🕊️  POCKETGULL SANCTUARY WORKSTATION (PURE DART 3.11 TUI)              ║');
    print('  ║   Optotypic Clinical Typography • Relational Ludology • Restorative Pacing ║');
    print('  ╚═══════════════════════════════════════════════════════════════════════════╝${Ansi.reset}');
    print('  ${Ansi.muted}Foundry Root: ${projectRoot.path}${Ansi.reset}');
    print('  ${Ansi.muted}W3C OTS Memory Safety • Zero RFN • Louise Sloan 5:1 Optotypes${Ansi.reset}\n');
  }

  void _renderMenu() {
    print('  ${Ansi.white}${Ansi.bold}Available Sanctuary Chambers:${Ansi.reset}\n');
    print('  ${Ansi.gold}[1]${Ansi.reset} 🫁  ${Ansi.bold}Circadian & Bio-Clock Pacing${Ansi.reset}  - 4-7-8 Parasympathetic & Sinus Breathing');
    print('  ${Ansi.gold}[2]${Ansi.reset} 🪐  ${Ansi.bold}The World Card (Tarot XXI)${Ansi.reset}   - Cosmic Mandorla, 4 Elemental Guardians & Lemniscates');
    print('  ${Ansi.gold}[3]${Ansi.reset} 🐴  ${Ansi.bold}Two Knights\' Midline Tour${Ansi.reset}   - Bilateral Saccadic Neuro-Rehabilitation');
    print('  ${Ansi.gold}[4]${Ansi.reset} 💊  ${Ansi.bold}ISMP Clinical Disambiguation${Ansi.reset} - Slashed Zero, Curved l, Serifed I, Slashed Z');
    print('  ${Ansi.gold}[5]${Ansi.reset} 🏛️  ${Ansi.bold}Foundry Forensic Health Grid${Ansi.reset} - 48 Font Binaries, Word Alignment & OTS Audit');
    print('  ${Ansi.gold}[6]${Ansi.reset} 🔍  ${Ansi.bold}Pure Dart SFNT Glyph Inspector${Ansi.reset}- Parse TrueType tables, bounds & contours');
    print('  ${Ansi.muted}[Q]  Exit Sanctuary Workstation${Ansi.reset}');
  }

  /// 1. Real-Time Breathing Pacer (4-7-8)
  Future<void> _runBreathingSanctuary() async {
    Ansi.clear();
    print('\n${Ansi.sage}${Ansi.bold}  🫁 CIRCADIAN BIO-CLOCK & PARASYMPATHETIC PACER (4-7-8)${Ansi.reset}');
    print('  ${Ansi.muted}Inhale: 4s  •  Hold: 7s  •  Exhale: 8s. 1 demonstration cycle.${Ansi.reset}\n');

    final phases = [
      {'name': 'INHALE (Expand Diaphragm)', 'duration': 4, 'color': Ansi.cyan},
      {'name': 'HOLD (Gentle Stillness)  ', 'duration': 7, 'color': Ansi.gold},
      {'name': 'EXHALE (Vagal Nerve Release)', 'duration': 8, 'color': Ansi.sage},
    ];

    for (final p in phases) {
      final name = p['name'] as String;
      final dur = p['duration'] as int;
      final color = p['color'] as String;

      for (int sec = 1; sec <= dur; sec++) {
        final bar = '█' * (sec * 4);
        stdout.write('\r  $color$name: [$sec/${dur}s] $bar${Ansi.reset}   ');
        await Future.delayed(const Duration(milliseconds: 700));
      }
      print('');
    }

    print('\n  ${Ansi.sage}Deep parasympathetic breath complete.${Ansi.reset}');
    stdout.write('  ${Ansi.muted}Press Enter to return to menu...${Ansi.reset}');
    stdin.readLineSync();
  }

  /// 2. The World Card (Tarot XXI) Mandorla Orbit
  Future<void> _runWorldMandorlaOrbit() async {
    Ansi.clear();
    print('\n${Ansi.gold}${Ansi.bold}  🪐 THE WORLD (MAJOR ARCANA XXI) - THE COSMIC MANDORLA${Ansi.reset}');
    print('  ${Ansi.muted}Archetypal Completion • Four Tetramorph Guardians • Infinite Renewal${Ansi.reset}\n');

    const mandorlaArt = '''
                 (∞) Red Lemniscate - Zenith Renewal
                    ╭──────────────────────╮
  🌬️  AIR / ANGEL   │     .---.   .---.    │   🌊 WATER / EAGLE
  Intellect & Mind  │    /     \\ /     \\   │   Intuition & Depth
  432 Hz Airy Chime │   |   ♥   |   ♥   |  │   528 Hz Harmonic
                    │    \\     / \\     /   │
                    │     `---'   `---'    │
  🔥  FIRE / LION   │   [Dancing Anima: 7] │   🌍 EARTH / BULL
  Will & Vitality   │    Dual Spiral Wands │   Somatic Grounding
  660 Hz Warm Pulse │                      │   330 Hz Deep Root
                    ╰──────────────────────╯
                 (∞) Red Lemniscate - Nadir Grounding
    ''';

    print('${Ansi.sage}$mandorlaArt${Ansi.reset}');

    print('  ${Ansi.bold}Elemental Guardians Alignment Matrix:${Ansi.reset}');
    print('  • ${Ansi.cyan}🌬️ Air / Angel (Top-Left):${Ansi.reset}     Clarity of Perception & Pure Breath');
    print('  • ${Ansi.blue}🌊 Water / Eagle (Top-Right):${Ansi.reset}   Heart-Led Fluidity & Saccadic Flow');
    print('  • ${Ansi.gold}🔥 Fire / Lion (Bottom-Left):${Ansi.reset}   Radiant Focus & Kinetic Precision');
    print('  • ${Ansi.sage}🌍 Earth / Bull (Bottom-Right):${Ansi.reset} Somatic Baseline Grounding at y = 0');
    print('  • ${Ansi.red}♥ Center / Dancing Anima:${Ansi.reset}       7 Cosmic Orbit Steps to Wholeness\n');

    stdout.write('  ${Ansi.muted}Press Enter to return to menu...${Ansi.reset}');
    stdin.readLineSync();
  }

  /// 3. Two Knights\' Console Midline Tour
  Future<void> _runTwoKnightsConsoleTour() async {
    Ansi.clear();
    print('\n${Ansi.bold}  🐴 TWO KNIGHTS\' MIDLINE TOUR (BILATERAL SACCADE REHABILITATION)${Ansi.reset}');
    print('  ${Ansi.muted}Left Hemisphere (Emerald Knight 🐴) • Right Hemisphere (Golden Knight 🦄)${Ansi.reset}\n');

    final board = List.generate(6, (r) => List.generate(6, (c) => '.'));
    final letters = ['P', 'O', 'C', 'K', 'E', 'T', 'G', 'U', 'L', 'L', '♥', '∞'];
    int letterIdx = 0;

    int leftR = 5, leftC = 0;
    int rightR = 0, rightC = 5;
    board[leftR][leftC] = 'H';
    board[rightR][rightC] = 'E';

    void printBoard() {
      print('     0   1   2   3   4   5');
      print('   ┌───┬───┬───┬───┬───┬───┐');
      for (int r = 0; r < 6; r++) {
        stdout.write(' $r │');
        for (int c = 0; c < 6; c++) {
          if (r == leftR && c == leftC) {
            stdout.write(' ${Ansi.sage}🐴${Ansi.reset}│');
          } else if (r == rightR && c == rightC) {
            stdout.write(' ${Ansi.gold}🦄${Ansi.reset}│');
          } else if (board[r][c] != '.') {
            stdout.write(' ${Ansi.cyan}${board[r][c]}${Ansi.reset} │');
          } else {
            final isAlt = (r + c) % 2 == 1;
            stdout.write(isAlt ? ' · │' : '   │');
          }
        }
        print('');
        if (r < 5) print('   ├───┼───┼───┼───┼───┼───┤');
      }
      print('   └───┴───┴───┴───┴───┴───┘\n');
    }

    printBoard();
    print('  ${Ansi.sage}Executing Bilateral Saccade Sequence:${Ansi.reset}');

    final moves = [
      {'knight': 'Left 🐴', 'dr': -2, 'dc': 1},
      {'knight': 'Right 🦄', 'dr': 2, 'dc': -1},
      {'knight': 'Left 🐴', 'dr': -1, 'dc': 2},
      {'knight': 'Right 🦄', 'dr': 1, 'dc': -2},
    ];

    for (final m in moves) {
      await Future.delayed(const Duration(milliseconds: 600));
      final k = m['knight'] as String;
      final dr = m['dr'] as int;
      final dc = m['dc'] as int;

      if (k.startsWith('Left')) {
        leftR += dr;
        leftC += dc;
        board[leftR][leftC] = letters[letterIdx++ % letters.length];
      } else {
        rightR += dr;
        rightC += dc;
        board[rightR][rightC] = letters[letterIdx++ % letters.length];
      }

      Ansi.clear();
      print('\n${Ansi.bold}  🐴 TWO KNIGHTS\' MIDLINE TOUR - Step Completed!${Ansi.reset}\n');
      printBoard();
      print('  Step: $k moved L-shape (dr: $dr, dc: $dc). Midline Crossed! ✨');
    }

    stdout.write('\n  ${Ansi.muted}Press Enter to return to menu...${Ansi.reset}');
    stdin.readLineSync();
  }

  /// 4. ISMP Clinical Disambiguation
  Future<void> _runIsmpClinicalDisambiguationTester() async {
    Ansi.clear();
    print('\n${Ansi.cyan}${Ansi.bold}  💊 INSTITUTE FOR SAFE MEDICATION PRACTICES (ISMP) DISAMBIGUATION${Ansi.reset}');
    print('  ${Ansi.muted}Eliminating Life-Critical Fatal Confusions in EHR Dosages & Telemetry${Ansi.reset}\n');

    final checks = [
      {
        'rule': 'ISMP Slashed Zero (cv08)',
        'ambiguity': '0 (Zero) vs O (Capital Letter O)',
        'solution': 'Internal optical slash prevents reading 500 mg as 50 Omg',
        'sample': '500 mg vs 5O0 mg',
      },
      {
        'rule': 'ISMP Curved Lowercase l (cv05)',
        'ambiguity': '1 (One) vs l (Lower L) vs I (Capital I)',
        'solution': 'Dynamic outward terminal curved foot eliminates 1/l/I collision',
        'sample': '10 mg vs 1O mg vs l0 mg',
      },
      {
        'rule': 'ISMP Serifed Capital I (ss02)',
        'ambiguity': 'I (Capital I) vs l (Lowercase L) in Biomarkers',
        'solution': 'Bilobe horizontal serifs at cap-height & baseline (IL-6, IgA)',
        'sample': 'IL-6 Interleukin vs lL-6',
      },
      {
        'rule': 'ISMP Slashed Capital Z (cv11)',
        'ambiguity': 'Z (Letter Z) vs 2 (Numeral Two)',
        'solution': 'Center horizontal crossbar stroke clearly distinguishes Z from 2',
        'sample': '2 mg Diazepam vs Z mg',
      },
    ];

    for (final c in checks) {
      print('  ${Ansi.bold}• ${c['rule']}:${Ansi.reset}');
      print('    ${Ansi.red}Hazard:${Ansi.reset}    ${c['ambiguity']}');
      print('    ${Ansi.sage}Solution:${Ansi.reset}  ${c['solution']}');
      print('    ${Ansi.gold}Dosage:${Ansi.reset}    ${c['sample']}\n');
    }

    stdout.write('  ${Ansi.muted}Press Enter to return to menu...${Ansi.reset}');
    stdin.readLineSync();
  }

  /// 5. Forensic Foundry Health Grid
  Future<void> _runForensicFoundryDashboard() async {
    Ansi.clear();
    print('\n${Ansi.bold}  🏛️  THOMAS PHINNEY FORENSIC AUDIT & HEALTH GRID${Ansi.reset}\n');

    final rootDir = projectRoot;
    final ttfDir = Directory('${rootDir.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}ttf');
    if (ttfDir.existsSync()) {
      print('  Scanning TrueType binaries in \${ttfDir.path}...\n');
      final files = ttfDir.listSync().whereType<File>().where((f) => f.path.endsWith('.ttf')).toList();
      int passed = 0;
      for (final f in files) {
        final name = f.path.split(Platform.pathSeparator).last;
        final res = ThomasPhinneyAuditor.audit(f);
        if (res.passed) {
          passed++;
          print('  ${Ansi.sage}✔ [PASS]${Ansi.reset} $name (glyphs: ${res.totalGlyphs}, loca: even, bit7: clear)');
        } else {
          print('  ${Ansi.red}✖ [FAIL]${Ansi.reset} $name - ${res.message}');
        }
      }
      print('\n  ${Ansi.gold}Foundry Status: $passed / ${files.length} Passed W3C OTS Validation.${Ansi.reset}');
    }

    stdout.write('\n  ${Ansi.muted}Press Enter to return to menu...${Ansi.reset}');
    stdin.readLineSync();
  }

  /// 6. Pure Dart Glyph Inspector
  Future<void> _runPureDartGlyphInspector() async {
    Ansi.clear();
    print('\n${Ansi.bold}  🔍 PURE DART TRUE-TYPE GLYPH INSPECTOR${Ansi.reset}\n');
    final fontFile = File('${projectRoot.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}ttf${Platform.pathSeparator}PocketGull-Bold.ttf');
    
    if (fontFile.existsSync()) {
      final inspector = GlyphInspector.fromFile(fontFile);
      print('  Font: ${fontFile.path}');
      print('  Total glyphs: ${inspector.numGlyphs}\n');

      final sample = ['0', '1', 'I', 'l', 'Z', '2', '♥'];
      for (final ch in sample) {
        final code = ch.codeUnitAt(0);
        final gid = inspector.unicodeToGid[code];
        if (gid != null) {
          final g = inspector.getGlyphData(gid);
          final bounds = g['bounds'] as List<int>? ?? [0,0,0,0];
          print('  Glyph [$ch] (U+${code.toRadixString(16).padLeft(4, "0").toUpperCase()} / GID $gid): bounds=(${bounds.join(", ")}), adv=${g['adv']}');
        }
      }
    } else {
      print('  [WARN] Font file not found at ${fontFile.path}');
    }

    stdout.write('\n  ${Ansi.muted}Press Enter to return to menu...${Ansi.reset}');
    stdin.readLineSync();
  }
}
