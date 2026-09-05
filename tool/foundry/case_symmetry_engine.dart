import 'models.dart';
import 'glyph_inspector.dart';

/// Pure Dart 3.11 Case Symmetry Engine for Google Fonts Upstream Compliance.
///
/// Synthesizes missing Unicode uppercase counterparts required for 100% FontSpector
/// casing compliance and Shaperglot language support:
/// - U+A7D2 (uniA7D2): LATIN CAPITAL LETTER DOUBLE THORN (uppercase of U+A7D3)
/// - U+A7D4 (uniA7D4): LATIN CAPITAL LETTER DOUBLE WYNN (uppercase of U+A7D5)
/// - U+A7DC (uniA7DC): LATIN CAPITAL LETTER LAMBDA WITH STROKE (uppercase of U+019B / U+A7DD)
/// - U+A7CB (uniA7CB): LATIN CAPITAL LETTER RAMS HORN (uppercase of U+0264, required for Dan & Goo)
/// - U+24B6 / U+24D0: CIRCLED LATIN CAPITAL / SMALL LETTER A (Koalib orthography)
class CaseSymmetryEngine {
  /// Synthesizes U+A7D2 Capital Double Thorn from existing Thorn glyph.
  static GlyphRecord synthesizeCapitalDoubleThorn({
    required int gid,
    required GlyphInspector inspector,
    bool isMono = false,
  }) {
    // Locate 'Thorn' (U+00DE) in the font
    final thornGid = inspector.unicodeToGid[0x00DE];
    final gData = thornGid != null ? inspector.getGlyphData(thornGid) : null;

    final contours = <GlyphContour>[];
    int adv = isMono ? 600 : 850;
    int lsb = 60;

    if (gData != null && gData['empty'] == false && gData['composite'] == false) {
      final endPts = gData['endPts'] as List<int>;
      final flags = gData['flags'] as List<int>;
      final xs = gData['xs'] as List<int>;
      final ys = gData['ys'] as List<int>;
      final origAdv = gData['adv'] as int;
      lsb = gData['lsb'] as int;
      adv = isMono ? 600 : (origAdv * 1.35).round();

      final scale = isMono ? 0.55 : 0.85;
      final offsetX = isMono ? 200 : 350;

      // Duplicate each contour for the twin thorn stem
      int startIdx = 0;
      for (final endIdx in endPts) {
        if (startIdx > endIdx) continue;
        final cLen = endIdx - startIdx + 1;

        // First Thorn contour (left)
        final c1 = GlyphContour();
        for (int i = 0; i < cLen; i++) {
          final idx = startIdx + i;
          final x = (xs[idx] * scale).round();
          final y = ys[idx];
          final onCurve = (flags[idx] & 0x01) != 0;
          c1.add(x, y, onCurve: onCurve);
        }
        contours.add(c1);

        // Second Thorn contour (right)
        final c2 = GlyphContour();
        for (int i = 0; i < cLen; i++) {
          final idx = startIdx + i;
          final x = (xs[idx] * scale + offsetX).round();
          final y = ys[idx];
          final onCurve = (flags[idx] & 0x01) != 0;
          c2.add(x, y, onCurve: onCurve);
        }
        contours.add(c2);

        startIdx = endIdx + 1;
      }
    } else {
      // Fallback procedural geometry
      final stemWidth = isMono ? 70 : 90;
      final c1 = GlyphContour()
        ..add(80, 780)
        ..add(80 + stemWidth, 780)
        ..add(80 + stemWidth, 0)
        ..add(80, 0);
      final c2 = GlyphContour()
        ..add(380, 780)
        ..add(380 + stemWidth, 780)
        ..add(380 + stemWidth, 0)
        ..add(380, 0);
      contours.addAll([c1, c2]);
    }

    return GlyphRecord(
      glyphId: gid,
      codePoint: 0xA7D2,
      name: 'uniA7D2',
      advanceWidth: adv,
      lsb: lsb,
      contours: contours,
    );
  }

  /// Synthesizes U+A7D4 Capital Double Wynn from existing Wynn glyph.
  static GlyphRecord synthesizeCapitalDoubleWynn({
    required int gid,
    required GlyphInspector inspector,
    bool isMono = false,
  }) {
    final wynnGid = inspector.unicodeToGid[0x01F7] ?? inspector.unicodeToGid[0x00DE];
    final gData = wynnGid != null ? inspector.getGlyphData(wynnGid) : null;

    final contours = <GlyphContour>[];
    int adv = isMono ? 600 : 850;
    int lsb = 60;

    if (gData != null && gData['empty'] == false && gData['composite'] == false) {
      final endPts = gData['endPts'] as List<int>;
      final flags = gData['flags'] as List<int>;
      final xs = gData['xs'] as List<int>;
      final ys = gData['ys'] as List<int>;
      final origAdv = gData['adv'] as int;
      lsb = gData['lsb'] as int;
      adv = isMono ? 600 : (origAdv * 1.35).round();

      final scale = isMono ? 0.55 : 0.85;
      final offsetX = isMono ? 200 : 350;

      int startIdx = 0;
      for (final endIdx in endPts) {
        if (startIdx > endIdx) continue;
        final cLen = endIdx - startIdx + 1;

        final c1 = GlyphContour();
        for (int i = 0; i < cLen; i++) {
          final idx = startIdx + i;
          final x = (xs[idx] * scale).round();
          final y = ys[idx];
          final onCurve = (flags[idx] & 0x01) != 0;
          c1.add(x, y, onCurve: onCurve);
        }
        contours.add(c1);

        final c2 = GlyphContour();
        for (int i = 0; i < cLen; i++) {
          final idx = startIdx + i;
          final x = (xs[idx] * scale + offsetX).round();
          final y = ys[idx];
          final onCurve = (flags[idx] & 0x01) != 0;
          c2.add(x, y, onCurve: onCurve);
        }
        contours.add(c2);

        startIdx = endIdx + 1;
      }
    }

    return GlyphRecord(
      glyphId: gid,
      codePoint: 0xA7D4,
      name: 'uniA7D4',
      advanceWidth: adv,
      lsb: lsb,
      contours: contours,
    );
  }

  /// Synthesizes U+A7DC Capital Lambda with Stroke from existing Greek Lambda.
  static GlyphRecord synthesizeCapitalLambdaStroke({
    required int gid,
    required GlyphInspector inspector,
    bool isMono = false,
  }) {
    final lambdaGid = inspector.unicodeToGid[0x039B];
    final gData = lambdaGid != null ? inspector.getGlyphData(lambdaGid) : null;

    final contours = <GlyphContour>[];
    int adv = isMono ? 600 : 700;
    int lsb = 60;

    if (gData != null && gData['empty'] == false && gData['composite'] == false) {
      final endPts = gData['endPts'] as List<int>;
      final flags = gData['flags'] as List<int>;
      final xs = gData['xs'] as List<int>;
      final ys = gData['ys'] as List<int>;
      adv = gData['adv'] as int;
      lsb = gData['lsb'] as int;

      int startIdx = 0;
      for (final endIdx in endPts) {
        if (startIdx > endIdx) continue;
        final cLen = endIdx - startIdx + 1;
        final c = GlyphContour();
        for (int i = 0; i < cLen; i++) {
          final idx = startIdx + i;
          c.add(xs[idx], ys[idx], onCurve: (flags[idx] & 0x01) != 0);
        }
        contours.add(c);
        startIdx = endIdx + 1;
      }

      // Add horizontal crossbar stroke through waist (y: 360 to 430)
      final bounds = gData['bounds'] as List<int>;
      final minX = bounds[0];
      final maxX = bounds[2];
      final midX = (minX + maxX) / 2.0;
      final barW = ((maxX - minX) * 0.70).round();
      final x0 = (midX - barW / 2.0).round();
      final x1 = (midX + barW / 2.0).round();
      const y0 = 360;
      const y1 = 430;

      final bar = GlyphContour()
        ..add(x0, y0)
        ..add(x0, y1)
        ..add(x1, y1)
        ..add(x1, y0);
      contours.add(bar);
    }

    return GlyphRecord(
      glyphId: gid,
      codePoint: 0xA7DC,
      name: 'uniA7DC',
      advanceWidth: adv,
      lsb: lsb,
      contours: contours,
    );
  }

  /// Synthesizes U+A7CB Capital Rams Horn from lowercase uni0264 scaled to Cap-Height.
  static GlyphRecord synthesizeCapitalRamsHorn({
    required int gid,
    required GlyphInspector inspector,
    bool isMono = false,
  }) {
    final ramsGid = inspector.unicodeToGid[0x0264];
    final gData = ramsGid != null ? inspector.getGlyphData(ramsGid) : null;

    final contours = <GlyphContour>[];
    int adv = isMono ? 600 : 700;
    int lsb = 60;

    if (gData != null && gData['empty'] == false && gData['composite'] == false) {
      final endPts = gData['endPts'] as List<int>;
      final flags = gData['flags'] as List<int>;
      final xs = gData['xs'] as List<int>;
      final ys = gData['ys'] as List<int>;
      final origAdv = gData['adv'] as int;
      final origLsb = gData['lsb'] as int;

      // Scale from x-height (~546) to Cap-Height (~714)
      const scale = 714.0 / 546.0;
      adv = isMono ? 600 : (origAdv * scale).round();
      lsb = (origLsb * scale).round();

      int startIdx = 0;
      for (final endIdx in endPts) {
        if (startIdx > endIdx) continue;
        final cLen = endIdx - startIdx + 1;
        final c = GlyphContour();
        for (int i = 0; i < cLen; i++) {
          final idx = startIdx + i;
          final x = (xs[idx] * scale).round();
          final y = (ys[idx] * scale).round();
          c.add(x, y, onCurve: (flags[idx] & 0x01) != 0);
        }
        contours.add(c);
        startIdx = endIdx + 1;
      }
    }

    return GlyphRecord(
      glyphId: gid,
      codePoint: 0xA7CB,
      name: 'uniA7CB',
      advanceWidth: adv,
      lsb: lsb,
      contours: contours,
    );
  }

  /// Synthesizes U+24B6 Circled Capital Letter A.
  static GlyphRecord synthesizeCircledCapitalA({
    required int gid,
    required GlyphInspector inspector,
    bool isMono = false,
  }) {
    final aGid = inspector.unicodeToGid[0x0041];
    final gData = aGid != null ? inspector.getGlyphData(aGid) : null;

    final contours = <GlyphContour>[];
    final adv = isMono ? 600 : 700;
    final cx = adv ~/ 2;
    const cy = 360;
    const rOut = 380;
    const rIn = 330;

    // 1. Outer circle (CW)
    contours.add(_buildCircleContour(cx, cy, rOut, clockwise: true));
    // 2. Inner circle (CCW)
    contours.add(_buildCircleContour(cx, cy, rIn, clockwise: false));

    // 3. Scale letter A inside
    if (gData != null && gData['empty'] == false && gData['composite'] == false) {
      final endPts = gData['endPts'] as List<int>;
      final flags = gData['flags'] as List<int>;
      final xs = gData['xs'] as List<int>;
      final ys = gData['ys'] as List<int>;

      const aScale = 0.55;
      final shiftX = cx - (300 * aScale).round();
      const shiftY = 160;

      int startIdx = 0;
      for (final endIdx in endPts) {
        if (startIdx > endIdx) continue;
        final cLen = endIdx - startIdx + 1;
        final c = GlyphContour();
        for (int i = 0; i < cLen; i++) {
          final idx = startIdx + i;
          final x = (xs[idx] * aScale + shiftX).round();
          final y = (ys[idx] * aScale + shiftY).round();
          c.add(x, y, onCurve: (flags[idx] & 0x01) != 0);
        }
        contours.add(c);
        startIdx = endIdx + 1;
      }
    }

    return GlyphRecord(
      glyphId: gid,
      codePoint: 0x24B6,
      name: 'uni24B6',
      advanceWidth: adv,
      lsb: cx - rOut,
      contours: contours,
    );
  }

  static GlyphContour _buildCircleContour(int cx, int cy, int r, {bool clockwise = true}) {
    final pts = [
      (cx, cy + r),
      (cx + r, cy + r),
      (cx + r, cy),
      (cx + r, cy - r),
      (cx, cy - r),
      (cx - r, cy - r),
      (cx - r, cy),
      (cx - r, cy + r),
    ];
    final flags = [true, false, true, false, true, false, true, false];

    if (!clockwise) {
      pts.reverseRange(1, pts.length);
      flags.reverseRange(1, flags.length);
    }

    final contour = GlyphContour();
    for (int i = 0; i < pts.length; i++) {
      contour.add(pts[i].$1, pts[i].$2, onCurve: flags[i]);
    }
    return contour;
  }
}

extension on List {
  void reverseRange(int start, int end) {
    var i = start;
    var j = end - 1;
    while (i < j) {
      final tmp = this[i];
      this[i] = this[j];
      this[j] = tmp;
      i++;
      j--;
    }
  }
}
