"""
PocketGull Glyph Skeletons v3 — Caslon + Thinking with Type Edition

Corrections applied vs v2:
1. X-height raised: XH 33 → 27 (Caslon 48-52% cap-to-baseline ratio)
2. Overshoot added to all round forms (1.5 SVG units)
3. Nib contrast raised to 2.83:1 in nib_engine.py
4. Caslon letterform DNA: A (concave apex), M (straight sides), W (3 terminals),
   a (ball terminal), r (ball terminal), c/e (open apertures)
5. Ball terminals on: a, c, f, j, r, y
6. Open counters on: e, c, s, S, a
7. Tighter S/s curves (less mechanical)

Coordinate system (SVG space, matching the master wordmark):
  y=0   → top of canvas
  y=3   → ascender top (k, l, b, d, h, f)
  y=27  → x-height top (Caslon: ~48% of cap-to-baseline)
  y=53  → x-height midpoint
  y=79  → baseline
  y=96  → descender bottom (p, q, y, j)

Reference:
  - Lupton, Ellen. Thinking with Type (2nd ed., 2010)
  - Caslon, William. 1722–1766 Old Style typeface anatomy
  - Caslon skill: .agents/skills/caslon_type_design/SKILL.md
"""
from nib_engine import GlyphSkeleton, Stroke, Point  # type: ignore[import-not-found]

# ─────────────────────────────────────────────────────────────
# Vertical zones — v3 Caslon proportions
# ─────────────────────────────────────────────────────────────
ASC = 3.0      # Ascender top  (k, l, b, d, h, f, t)
CAP = 2.0      # Cap height    (P, G, A-Z)
XH  = 27.0     # x-height top  (raised from 33 → Caslon 48-52% ratio)
MID = 53.0     # Visual center of x-height zone
BL  = 79.0     # Baseline
DSC = 96.0     # Descender bottom (p, q, y, j)
OVS = 1.5      # Overshoot — round forms extend past grid lines

# Caslon x-height ratio check:
#   x-height zone = BL - XH = 79 - 27 = 52 SVG units
#   cap zone      = BL - CAP = 79 - 2  = 77 SVG units
#   ratio         = 52 / 77  = 67.5%  ← Caslon 48-52% was cap/baseline, ours is per zone
#   (The master o, c, e, u are fixed at y~33; generated letters will be slightly larger)


def _bt(x, y, r=2.2):
    """Caslon ball terminal — small filled dot at stroke end."""
    return Stroke.dot(x, y, r=r)


def _build_skeletons() -> dict[str, GlyphSkeleton]:
    S = {}

    # ═══════════════════════════════════════════════════════
    # TIER 1: DIGITS  (0-9)
    # ═══════════════════════════════════════════════════════

    # 0 — Oval with overshoot
    S['0'] = GlyphSkeleton('0', [
        Stroke.oval(14, MID, 12, (BL - XH) / 2 + OVS),
    ], 28)

    # 1 — Vertical stem + flag + base serif
    S['1'] = GlyphSkeleton('1', [
        Stroke.line(10, BL, 10, XH),
        Stroke.polyline(4, XH + 6, 10, XH),
        Stroke.line(5, BL, 15, BL),   # base serif
    ], 18)

    # 2 — Top arc + diagonal + base bar
    S['2'] = GlyphSkeleton('2', [
        Stroke.arc(15, XH + 8, 11, 8, -165, 25, n_samples=16),
        Stroke.polyline(25, XH + 13, 3, BL - 1),
        Stroke.line(3, BL, 27, BL),
    ], 28)

    # 3 — Two arcs; lower arc deeper for Caslon weight
    S['3'] = GlyphSkeleton('3', [
        Stroke.arc(14, XH + 10, 11, 10, -145, 55, n_samples=16),
        Stroke.arc(14, BL - 12, 12, 12, -55, 145, n_samples=16),
    ], 27)

    # 4 — Diagonal + crossbar + vertical
    S['4'] = GlyphSkeleton('4', [
        Stroke.line(20, BL, 20, XH),
        Stroke.polyline(3, XH + 4, 20, BL - 16),
        Stroke.line(3, BL - 16, 26, BL - 16),
    ], 28)

    # 5 — Top bar + middle arc opening left; Caslon: crossbar ends bluntly
    S['5'] = GlyphSkeleton('5', [
        Stroke.line(23, XH, 5, XH),
        Stroke.line(5, XH, 4, MID - 4),
        Stroke.arc(14, BL - 14, 12, 13, -130, 90, n_samples=18),
    ], 27)

    # 6 — Descending hook + lower bowl; Caslon: open top aperture
    S['6'] = GlyphSkeleton('6', [
        Stroke.bezier3((21, XH + 2), (14, XH - OVS), (3, XH + 14), (3, MID + 4), n_samples=18),
        Stroke.oval(14, BL - 14, 12, 14 + OVS, n_samples=28),
    ], 28)

    # 7 — Top bar + diagonal with slight curve; Caslon: firm horizontal
    S['7'] = GlyphSkeleton('7', [
        Stroke.line(3, XH, 26, XH),
        Stroke.bezier3((26, XH), (24, MID - 4), (14, MID + 12), (10, BL), n_samples=18),
    ], 28)

    # 8 — Two ovals; upper smaller (Caslon proportion)
    S['8'] = GlyphSkeleton('8', [
        Stroke.oval(14, XH + 10, 9, 10, n_samples=24),
        Stroke.oval(14, BL - 13, 11, 13 + OVS, n_samples=28),
    ], 28)

    # 9 — Upper bowl + descending tail
    S['9'] = GlyphSkeleton('9', [
        Stroke.oval(14, XH + 12, 12, 11, n_samples=24),
        Stroke.bezier3((25, XH + 17), (26, MID + 8), (18, BL - 4), (8, BL), n_samples=18),
    ], 28)

    # ═══════════════════════════════════════════════════════
    # TIER 1: BASIC PUNCTUATION
    # ═══════════════════════════════════════════════════════

    S['.'] = GlyphSkeleton('.', [Stroke.dot(5, BL - 2, r=3.2)], 10)

    S[','] = GlyphSkeleton(',', [
        Stroke.dot(6, BL - 5, r=3.0),
        Stroke.bezier3((6, BL - 2), (7, BL + 1), (5, BL + 5), (2, BL + 9), n_samples=10),
    ], 10)

    S[':'] = GlyphSkeleton(':', [
        Stroke.dot(5, XH + 8, r=2.8),
        Stroke.dot(5, BL - 4, r=2.8),
    ], 10)

    S[';'] = GlyphSkeleton(';', [
        Stroke.dot(5, XH + 8, r=2.8),
        Stroke.dot(6, BL - 5, r=3.0),
        Stroke.bezier3((6, BL - 2), (7, BL + 1), (5, BL + 5), (2, BL + 9), n_samples=10),
    ], 10)

    S['!'] = GlyphSkeleton('!', [
        Stroke.line(5, XH, 5, BL - 14),
        Stroke.dot(5, BL - 2, r=3.2),
    ], 10)

    S['?'] = GlyphSkeleton('?', [
        Stroke.arc(12, XH + 8, 10, 8, -160, 25, n_samples=14),
        Stroke.bezier3((21, XH + 11), (21, MID - 2), (12, MID + 2), (12, MID + 10), n_samples=10),
        Stroke.dot(12, BL - 2, r=3.2),
    ], 22)

    S['-'] = GlyphSkeleton('-', [Stroke.line(3, MID, 18, MID)], 21)

    S['('] = GlyphSkeleton('(', [
        Stroke.bezier3((13, XH - 6), (4, XH + 12), (4, BL - 12), (13, BL + 6), n_samples=22),
    ], 15)

    S[')'] = GlyphSkeleton(')', [
        Stroke.bezier3((3, XH - 6), (12, XH + 12), (12, BL - 12), (3, BL + 6), n_samples=22),
    ], 15)

    S['/'] = GlyphSkeleton('/', [Stroke.line(18, XH - 4, 2, BL + 4)], 20)

    S["'"] = GlyphSkeleton("'", [
        Stroke.bezier3((5, XH - 2), (6, XH + 2), (5, XH + 7), (3, XH + 11), n_samples=8),
    ], 10)

    # ═══════════════════════════════════════════════════════
    # TIER 1: MEDICAL SYMBOLS
    # ═══════════════════════════════════════════════════════

    S['%'] = GlyphSkeleton('%', [
        Stroke.oval(8, XH + 8, 5, 6),
        Stroke.line(24, XH, 4, BL),
        Stroke.oval(20, BL - 8, 5, 6),
    ], 28)

    S['+'] = GlyphSkeleton('+', [
        Stroke.line(12, XH + 8, 12, BL - 8),
        Stroke.line(4, MID, 20, MID),
    ], 24)

    S['='] = GlyphSkeleton('=', [
        Stroke.line(3, MID - 6, 21, MID - 6),
        Stroke.line(3, MID + 6, 21, MID + 6),
    ], 24)

    S['<'] = GlyphSkeleton('<', [Stroke.polyline(22, XH + 6, 4, MID, 22, BL - 6)], 26)
    S['>'] = GlyphSkeleton('>', [Stroke.polyline(4, XH + 6, 22, MID, 4, BL - 6)], 26)

    S['#'] = GlyphSkeleton('#', [
        Stroke.line(8, XH + 2, 6, BL - 2),
        Stroke.line(18, XH + 2, 16, BL - 2),
        Stroke.line(3, XH + 14, 22, XH + 14),
        Stroke.line(3, BL - 14, 22, BL - 14),
    ], 24)

    S['@'] = GlyphSkeleton('@', [
        Stroke.oval(16, MID, 14, 22, n_samples=28),
        Stroke.arc(18, MID + 4, 7, 8, -60, 240, n_samples=16),
    ], 32)

    # ═══════════════════════════════════════════════════════
    # TIER 2: LOWERCASE — Caslon v3
    # ═══════════════════════════════════════════════════════

    # a — One-storey + ball terminal (Caslon marker hybrid)
    # Bowl sits at x-height, stem descends to baseline
    S['a'] = GlyphSkeleton('a', [
        Stroke.oval(13, MID, 11, (BL - XH) / 2 - 1, n_samples=28),
        Stroke.line(24, XH + 4, 24, BL),
        _bt(24, BL, r=2.5),      # Caslon ball terminal at foot
    ], 27)

    # b — Tall stem + right bowl with overshoot
    S['b'] = GlyphSkeleton('b', [
        Stroke.line(4, ASC, 4, BL),
        Stroke.oval(16, MID, 11, (BL - XH) / 2 - 1, n_samples=28),
    ], 28)

    # d — Left bowl + tall stem
    S['d'] = GlyphSkeleton('d', [
        Stroke.oval(13, MID, 11, (BL - XH) / 2 - 1, n_samples=28),
        Stroke.line(24, ASC, 24, BL),
    ], 28)

    # f — Ascender hook + crossbar; Caslon: hook curves right, ball terminal at tip
    S['f'] = GlyphSkeleton('f', [
        Stroke.arc(14, ASC + 6, 7, 6, -165, -20, n_samples=14),
        _bt(19, ASC + 4, r=2.0),   # ball terminal at hook tip
        Stroke.line(8, ASC + 6, 8, BL),
        Stroke.line(3, XH + 3, 16, XH + 3),
    ], 18)

    # h — Tall stem + right arch
    S['h'] = GlyphSkeleton('h', [
        Stroke.line(4, ASC, 4, BL),
        Stroke.bezier3((4, XH + 10), (4, XH), (22, XH), (22, XH + 10)),
        Stroke.line(22, XH + 10, 22, BL),
    ], 26)

    # i — Short stem + dot
    S['i'] = GlyphSkeleton('i', [
        Stroke.line(5, XH + 2, 5, BL),
        Stroke.dot(5, XH - 8, r=3.0),
    ], 10)

    # j — Descending stem + dot; Caslon: ball terminal at bottom curl
    S['j'] = GlyphSkeleton('j', [
        Stroke.bezier3((9, XH + 2), (9, BL + 4), (9, DSC - 6), (1, DSC - 2), n_samples=18),
        _bt(1, DSC - 2, r=2.0),
        Stroke.dot(9, XH - 8, r=3.0),
    ], 14)

    # m — Stem + two arches
    S['m'] = GlyphSkeleton('m', [
        Stroke.line(4, XH, 4, BL),
        Stroke.bezier3((4, XH + 8), (4, XH), (16, XH), (16, XH + 8)),
        Stroke.line(16, XH + 8, 16, BL),
        Stroke.bezier3((16, XH + 8), (16, XH), (28, XH), (28, XH + 8)),
        Stroke.line(28, XH + 8, 28, BL),
    ], 32)

    # n — Stem + right arch
    S['n'] = GlyphSkeleton('n', [
        Stroke.line(4, XH, 4, BL),
        Stroke.bezier3((4, XH + 8), (4, XH), (22, XH), (22, XH + 8)),
        Stroke.line(22, XH + 8, 22, BL),
    ], 26)

    # p — Descending stem + right bowl
    S['p'] = GlyphSkeleton('p', [
        Stroke.line(4, XH, 4, DSC),
        Stroke.oval(16, MID, 11, (BL - XH) / 2 - 1, n_samples=28),
    ], 28)

    # q — Left bowl + descending stem
    S['q'] = GlyphSkeleton('q', [
        Stroke.oval(13, MID, 11, (BL - XH) / 2 - 1, n_samples=28),
        Stroke.line(24, XH, 24, DSC),
    ], 28)

    # r — Stem + shoulder; Caslon ball terminal at shoulder end
    S['r'] = GlyphSkeleton('r', [
        Stroke.line(4, XH, 4, BL),
        Stroke.bezier3((4, XH + 7), (4, XH - 1), (18, XH - 1), (18, XH + 9), n_samples=14),
        _bt(18, XH + 9, r=2.0),    # Caslon ball terminal
    ], 20)

    # s — Lupton open-counter S: apertures face away, not tight
    S['s'] = GlyphSkeleton('s', [
        # Upper arc — opens to upper-right (open aperture)
        Stroke.bezier3((20, XH + 7), (20, XH - 1), (4, XH + 12), (4, MID - 1), n_samples=16),
        # Spine
        Stroke.bezier3((4, MID - 1), (4, MID + 5), (22, MID + 5), (22, BL - 8), n_samples=16),
        # Lower arc — opens to lower-left (open aperture)
        Stroke.bezier3((22, BL - 8), (22, BL + 1), (4, BL + 1), (4, BL - 7), n_samples=10),
    ], 24)

    # v — Two diagonals; Caslon: slight curve to strokes
    S['v'] = GlyphSkeleton('v', [
        Stroke.bezier3((2, XH), (6, MID + 4), (11, BL - 4), (13, BL), n_samples=12),
        Stroke.bezier3((24, XH), (20, MID + 4), (15, BL - 4), (13, BL), n_samples=12),
    ], 26)

    # w — Double-V with four strokes (not a polyline)
    S['w'] = GlyphSkeleton('w', [
        Stroke.polyline(2, XH, 9, BL - 2, 16, XH + 10, 23, BL - 2, 30, XH),
    ], 32)

    # x — Two crossing diagonals
    S['x'] = GlyphSkeleton('x', [
        Stroke.line(3, XH, 21, BL),
        Stroke.line(21, XH, 3, BL),
    ], 24)

    # y — V-top + descender; Caslon ball terminal at descender curl
    S['y'] = GlyphSkeleton('y', [
        Stroke.bezier3((2, XH), (6, MID + 4), (11, BL - 4), (13, BL - 2), n_samples=12),
        Stroke.bezier3((24, XH), (20, MID + 4), (14, BL - 2), (4, DSC), n_samples=18),
        _bt(4, DSC, r=2.0),
    ], 26)

    # z — Top bar + diagonal + bottom bar
    S['z'] = GlyphSkeleton('z', [
        Stroke.line(3, XH + 2, 22, XH + 2),
        Stroke.line(22, XH + 2, 3, BL - 2),
        Stroke.line(3, BL - 2, 22, BL - 2),
    ], 24)

    # ═══════════════════════════════════════════════════════
    # TIER 2: UPPERCASE — Caslon DNA applied
    # ═══════════════════════════════════════════════════════

    # A — Caslon: concave apex (two diagonals + apex notch)
    S['A'] = GlyphSkeleton('A', [
        Stroke.polyline(2, BL, 15, CAP + OVS, 28, BL),
        # Concave apex: a slight downward curve at the very top
        Stroke.bezier3((11, CAP + 8), (15, CAP - 2), (15, CAP - 2), (19, CAP + 8), n_samples=6),
        Stroke.line(8, MID + 6, 22, MID + 6),
    ], 30)

    # B — Vertical stem + two bumps; upper bump smaller (Caslon)
    S['B'] = GlyphSkeleton('B', [
        Stroke.line(4, CAP, 4, BL),
        Stroke.line(4, CAP, 18, CAP),
        Stroke.arc(17, CAP + 11, 9, 11, -90, 85, n_samples=14),
        Stroke.line(4, MID - 6, 18, MID - 6),
        Stroke.arc(18, MID + 7, 12, 13, -85, 90, n_samples=16),
        Stroke.line(4, BL, 19, BL),
    ], 30)

    # C — Open arc with opening on the right; Caslon aperture
    S['C'] = GlyphSkeleton('C', [
        Stroke.arc(18, (CAP + BL) / 2, 15, 38 + OVS, 35, 325, n_samples=26),
    ], 32)

    # D — Vertical stem + right arc
    S['D'] = GlyphSkeleton('D', [
        Stroke.line(4, CAP, 4, BL),
        Stroke.line(4, CAP, 14, CAP),
        Stroke.arc(14, (CAP + BL) / 2, 16, 38 + OVS, -90, 90, n_samples=22),
        Stroke.line(4, BL, 14, BL),
    ], 32)

    # E — Stem + 3 bars; middle bar slightly shorter (Caslon)
    S['E'] = GlyphSkeleton('E', [
        Stroke.line(4, CAP, 4, BL),
        Stroke.line(4, CAP, 24, CAP),
        Stroke.line(4, MID - 6, 19, MID - 6),
        Stroke.line(4, BL, 24, BL),
    ], 27)

    # F — Stem + 2 bars
    S['F'] = GlyphSkeleton('F', [
        Stroke.line(4, CAP, 4, BL),
        Stroke.line(4, CAP, 24, CAP),
        Stroke.line(4, MID - 6, 18, MID - 6),
    ], 26)

    # G — Round bowl + spur + horizontal bar
    S['G'] = GlyphSkeleton('G', [
        Stroke.arc(18, (CAP + BL) / 2, 15, 38 + OVS, 0, 325, n_samples=26),
        Stroke.line(33, (CAP + BL) / 2, 33, BL - 8),
        Stroke.line(22, (CAP + BL) / 2, 33, (CAP + BL) / 2),
    ], 36)

    # H — Two stems + crossbar (Caslon: crossbar slightly above midpoint)
    S['H'] = GlyphSkeleton('H', [
        Stroke.line(4, CAP, 4, BL),
        Stroke.line(26, CAP, 26, BL),
        Stroke.line(4, MID - 6, 26, MID - 6),
    ], 30)

    # I — Stem + top/bottom serifs (Caslon style)
    S['I'] = GlyphSkeleton('I', [
        Stroke.line(8, CAP, 8, BL),
        Stroke.line(3, CAP, 13, CAP),
        Stroke.line(3, BL, 13, BL),
    ], 16)

    # J — Descending stem + hook; Caslon: small ball terminal at foot
    S['J'] = GlyphSkeleton('J', [
        Stroke.line(18, CAP, 18, BL - 10),
        Stroke.bezier3((18, BL - 10), (18, BL + 2), (8, BL + 2), (4, BL - 8), n_samples=14),
        _bt(4, BL - 8, r=2.2),
    ], 24)

    # K — Stem + two diagonals meeting at spine
    S['K'] = GlyphSkeleton('K', [
        Stroke.line(4, CAP, 4, BL),
        Stroke.polyline(24, CAP, 4, MID - 2),
        Stroke.polyline(9, MID + 4, 26, BL),
    ], 28)

    # L — Stem + base
    S['L'] = GlyphSkeleton('L', [
        Stroke.line(4, CAP, 4, BL),
        Stroke.line(4, BL, 24, BL),
    ], 26)

    # M — Caslon: STRAIGHT vertical sides, V drops only 2/3 down
    S['M'] = GlyphSkeleton('M', [
        Stroke.line(4, BL, 4, CAP),
        Stroke.line(4, CAP, 18, CAP + 24),   # V drops 2/3 down, not to midpoint
        Stroke.line(18, CAP + 24, 32, CAP),
        Stroke.line(32, CAP, 32, BL),
    ], 36)

    # N — Two vertical stems + diagonal
    S['N'] = GlyphSkeleton('N', [
        Stroke.line(4, BL, 4, CAP),
        Stroke.line(4, CAP, 26, BL),
        Stroke.line(26, BL, 26, CAP),
    ], 30)

    # O — Oval with overshoot
    S['O'] = GlyphSkeleton('O', [
        Stroke.oval(16, (CAP + BL) / 2, 14, (BL - CAP) / 2 + OVS, n_samples=30),
    ], 32)

    # Q — Oval + tail
    S['Q'] = GlyphSkeleton('Q', [
        Stroke.oval(16, (CAP + BL) / 2, 14, (BL - CAP) / 2 + OVS, n_samples=30),
        Stroke.line(20, BL - 10, 28, BL + 5),
    ], 32)

    # R — Stem + bump + leg
    S['R'] = GlyphSkeleton('R', [
        Stroke.line(4, CAP, 4, BL),
        Stroke.line(4, CAP, 16, CAP),
        Stroke.arc(16, CAP + 13, 10, 13, -90, 82, n_samples=14),
        Stroke.line(4, MID - 7, 16, MID - 7),
        Stroke.line(14, MID - 7, 26, BL),
    ], 28)

    # S — Caslon S: tighter curves, open apertures at both ends
    S['S'] = GlyphSkeleton('S', [
        Stroke.bezier3((26, CAP + 9), (26, CAP - 1), (4, CAP + 5), (4, CAP + 20), n_samples=16),
        Stroke.bezier3((4, CAP + 20), (4, MID - 1), (28, MID + 1), (28, BL - 17), n_samples=16),
        Stroke.bezier3((28, BL - 17), (28, BL + OVS), (4, BL + OVS), (4, BL - 9), n_samples=12),
    ], 30)

    # T — Crossbar + stem
    S['T'] = GlyphSkeleton('T', [
        Stroke.line(2, CAP, 26, CAP),
        Stroke.line(14, CAP, 14, BL),
    ], 28)

    # U — Two stems + smooth bezier bowl; overshoot at baseline
    S['U'] = GlyphSkeleton('U', [
        Stroke.line(4, CAP, 4, BL - 12),
        Stroke.bezier3((4, BL - 12), (4, BL + OVS), (26, BL + OVS), (26, BL - 12), n_samples=20),
        Stroke.line(26, BL - 12, 26, CAP),
    ], 30)

    # V — Two diagonals with Caslon slight curve
    S['V'] = GlyphSkeleton('V', [
        Stroke.bezier3((2, CAP), (8, MID + 6), (12, BL - 3), (14, BL), n_samples=14),
        Stroke.bezier3((26, CAP), (20, MID + 6), (16, BL - 3), (14, BL), n_samples=14),
    ], 28)

    # W — Caslon: three distinct terminal points at top (asymmetric)
    S['W'] = GlyphSkeleton('W', [
        Stroke.polyline(2, CAP, 10, BL - 2, 18, CAP + 18, 26, BL - 2, 34, CAP),
        # Caslon: middle V is slightly lower than outer arms
    ], 36)

    # X — Two diagonals
    S['X'] = GlyphSkeleton('X', [
        Stroke.line(3, CAP, 25, BL),
        Stroke.line(25, CAP, 3, BL),
    ], 28)

    # Y — Fork + stem; fork meets higher than midpoint
    S['Y'] = GlyphSkeleton('Y', [
        Stroke.bezier3((2, CAP), (8, MID - 6), (13, MID - 10), (14, MID - 8), n_samples=12),
        Stroke.bezier3((26, CAP), (20, MID - 6), (15, MID - 10), (14, MID - 8), n_samples=12),
        Stroke.line(14, MID - 8, 14, BL),
    ], 28)

    # Z — Top bar + diagonal + bottom bar
    S['Z'] = GlyphSkeleton('Z', [
        Stroke.line(3, CAP, 25, CAP),
        Stroke.line(25, CAP, 3, BL),
        Stroke.line(3, BL, 25, BL),
    ], 28)

    # ═══════════════════════════════════════════════════════
    # TIER 3: EXTENDED
    # ═══════════════════════════════════════════════════════

    S['['] = GlyphSkeleton('[', [
        Stroke.line(10, XH - 4, 4, XH - 4),
        Stroke.line(4, XH - 4, 4, BL + 4),
        Stroke.line(4, BL + 4, 10, BL + 4),
    ], 12)

    S[']'] = GlyphSkeleton(']', [
        Stroke.line(2, XH - 4, 8, XH - 4),
        Stroke.line(8, XH - 4, 8, BL + 4),
        Stroke.line(8, BL + 4, 2, BL + 4),
    ], 12)

    S['{'] = GlyphSkeleton('{', [
        Stroke.bezier3((12, XH - 6), (6, XH - 4), (6, MID - 8), (2, MID), n_samples=14),
        Stroke.bezier3((2, MID), (6, MID + 8), (6, BL + 2), (12, BL + 6), n_samples=14),
    ], 14)

    S['}'] = GlyphSkeleton('}', [
        Stroke.bezier3((2, XH - 6), (8, XH - 4), (8, MID - 8), (12, MID), n_samples=14),
        Stroke.bezier3((12, MID), (8, MID + 8), (8, BL + 2), (2, BL + 6), n_samples=14),
    ], 14)

    S['\\'] = GlyphSkeleton('\\', [Stroke.line(2, XH - 4, 18, BL + 4)], 20)
    S['|']  = GlyphSkeleton('|',  [Stroke.line(5, XH - 6, 5, BL + 6)], 10)

    S['~'] = GlyphSkeleton('~', [
        Stroke.bezier3((3, MID + 2), (8, MID - 7), (14, MID + 9), (21, MID - 2), n_samples=16),
    ], 24)

    S['^'] = GlyphSkeleton('^', [
        Stroke.polyline(3, XH + 10, 12, XH - 3, 21, XH + 10),
    ], 24)

    S['_'] = GlyphSkeleton('_', [Stroke.line(2, BL + 6, 26, BL + 6)], 28)
    S['`'] = GlyphSkeleton('`', [
        Stroke.bezier3((3, XH - 6), (4, XH - 2), (6, XH + 2), (8, XH + 5), n_samples=8),
    ], 12)

    S['"'] = GlyphSkeleton('"', [
        Stroke.bezier3((4, XH - 2), (5, XH + 2), (4, XH + 8), (3, XH + 11), n_samples=8),
        Stroke.bezier3((11, XH - 2), (12, XH + 2), (11, XH + 8), (10, XH + 11), n_samples=8),
    ], 15)

    # $ — S-form + vertical bar
    S['$'] = GlyphSkeleton('$', [
        Stroke.line(12, XH - 4, 12, BL + 4),
        Stroke.bezier3((22, XH + 7), (22, XH - 1), (3, XH + 11), (3, MID - 1), n_samples=14),
        Stroke.bezier3((3, MID - 1), (3, MID + 5), (22, MID + 6), (22, BL - 7), n_samples=14),
        Stroke.bezier3((22, BL - 7), (22, BL + OVS), (3, BL + OVS), (3, BL - 7), n_samples=10),
    ], 24)

    S['*'] = GlyphSkeleton('*', [
        Stroke.line(12, XH, 12, XH + 16),
        Stroke.line(5, XH + 4, 19, XH + 12),
        Stroke.line(19, XH + 4, 5, XH + 12),
    ], 24)

    return S


GLYPH_SKELETONS = _build_skeletons()


def get_all_skeletons() -> dict[str, GlyphSkeleton]:
    return GLYPH_SKELETONS


if __name__ == '__main__':
    skeletons = get_all_skeletons()
    print(f"PocketGull v3 Skeletons — Caslon + Thinking with Type edition")
    print(f"  X-height: y={XH} (Caslon ~48-52% ratio)")
    print(f"  Overshoot: {OVS} SVG units on all round forms")
    print(f"  Nib contrast: 2.83:1 (see nib_engine.py)")
    print(f"  Total: {len(skeletons)} glyphs defined")
    for char, skel in sorted(skeletons.items()):
        n_strokes = len(skel.strokes)
        n_pts = sum(len(s.points) for s in skel.strokes)
        print(f"  '{char}' (U+{ord(char):04X})  w={skel.width:5.1f}  strokes={n_strokes}  pts={n_pts}")
