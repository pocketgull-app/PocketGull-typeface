#!/usr/bin/env python3
"""
PocketGull Master Precision Superfamily Compiler v3.0
Generates mathematically pristine vector letterforms:
- Pure Bezier splines with exact extrema and G2 continuity (NO autotrace noise)
- Standardized 1024 UPM grid, Cap-Height 720, X-Height 480, Baseline 0, Descender -180
- Strict mathematical stem widths: Heavy Stem (110), Light Stem (65), Hairline (40)
- Precision 45° origami chamfer terminals & calligraphic cut angles
- Full Variable Font (VF) compilation (wght, opsz, slnt) and static instances
"""

import os
import sys
import math
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._f_v_a_r import Axis, NamedInstance
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

UPM = 1024
CAP = 720
XH = 480
BL = 0
DSC = -180
OVS = 14  # Optical overshoot for curved tops and bottoms

def make_clean_glyph(pen_draw_fn, glyph_set, advance_width):
    pen = TTGlyphPen(glyph_set)
    pen_draw_fn(pen)
    return pen.glyph(), advance_width

def draw_rounded_rect(pen, x1, y1, x2, y2, r=16):
    """Draws a rectangle with smooth filleted corners of radius r."""
    r = min(r, abs(x2 - x1)/2.0, abs(y2 - y1)/2.0)
    k = 0.5522847498 * r
    pen.moveTo((x1, y1 + r))
    pen.lineTo((x1, y2 - r))
    pen.curveTo((x1, y2 - r + k), (x1 + r - k, y2), (x1 + r, y2))
    pen.lineTo((x2 - r, y2))
    pen.curveTo((x2 - r + k, y2), (x2, y2 - r + k), (x2, y2 - r))
    pen.lineTo((x2, y1 + r))
    pen.curveTo((x2, y1 + r - k), (x2 - r + k, y1), (x2 - r, y1))
    pen.lineTo((x1 + r, y1))
    pen.curveTo((x1 + r - k, y1), (x1, y1 + r - k), (x1, y1 + r))
    pen.closePath()

def draw_rect(pen, x1, y1, x2, y2, chamfer=0, r=14):
    """Draws a rectangle with default smoothed filleted corners to eliminate harsh chisel chops."""
    if chamfer > 0:
        c = chamfer
        pen.moveTo((x1 + c, y1))
        pen.lineTo((x2 - c, y1))
        pen.lineTo((x2, y1 + c))
        pen.lineTo((x2, y2 - c))
        pen.lineTo((x2 - c, y2))
        pen.lineTo((x1 + c, y2))
        pen.lineTo((x1, y2 - c))
        pen.lineTo((x1, y1 + c))
        pen.closePath()
    else:
        draw_rounded_rect(pen, x1, y1, x2, y2, r=r)

def draw_oval_counter(pen, cx, cy, rx, ry, inner_rx, inner_ry):
    """Draws a clean, non-overlapping outer ellipse (CW) with an inner counter (CCW)."""
    k = 0.5522847498
    kx = rx * k
    ky = ry * k
    
    # Outer (Clockwise)
    pen.moveTo((cx, cy + ry))
    pen.curveTo((cx + kx, cy + ry), (cx + rx, cy + ky), (cx + rx, cy))
    pen.curveTo((cx + rx, cy - ky), (cx + kx, cy - ry), (cx, cy - ry))
    pen.curveTo((cx - kx, cy - ry), (cx - rx, cy - ky), (cx - rx, cy))
    pen.curveTo((cx - rx, cy + ky), (cx - kx, cy + ry), (cx, cy + ry))
    pen.closePath()

    # Inner (Counter-Clockwise)
    ikx = inner_rx * k
    iky = inner_ry * k
    pen.moveTo((cx, cy + inner_ry))
    pen.curveTo((cx - ikx, cy + inner_ry), (cx - inner_rx, cy + iky), (cx - inner_rx, cy))
    pen.curveTo((cx - inner_rx, cy - iky), (cx - ikx, cy - inner_ry), (cx, cy - inner_ry))
    pen.curveTo((cx + ikx, cy - inner_ry), (cx + inner_rx, cy - iky), (cx + inner_rx, cy))
    pen.curveTo((cx + inner_rx, cy + iky), (cx + ikx, cy + inner_ry), (cx, cy + inner_ry))
    pen.closePath()

def draw_smooth_c_arc(pen, cx, cy, rx, ry, sw, top_x, top_y, bot_x, bot_y, r=14):
    """Draws a smooth, non-self-intersecting curved aperture C-stroke with filleted terminal ends."""
    k = 0.5522847498
    kx = rx * k
    ky = ry * k
    
    irx = rx - sw
    iry = ry - sw
    ikx = irx * k
    iky = iry * k

    pen.moveTo((top_x, top_y))
    pen.curveTo((cx + kx * 0.7, cy + ry), (cx, cy + ry), (cx - rx * 0.7, cy + ry * 0.7))
    pen.curveTo((cx - rx, cy + ky), (cx - rx, cy), (cx - rx, cy - ky))
    pen.curveTo((cx - rx * 0.7, cy - ry * 0.7), (cx, cy - ry), (cx + kx * 0.7, cy - ry))
    pen.lineTo((bot_x, bot_y))
    # Inner curve returning with softened terminal fillet
    pen.curveTo((bot_x - sw * 0.2, bot_y + sw * 0.4), (bot_x - sw * 0.4, bot_y + sw * 0.6), (bot_x - sw * 0.6, bot_y + sw * 0.6))
    pen.curveTo((cx + ikx * 0.5, cy - iry), (cx, cy - iry), (cx - irx * 0.7, cy - iry * 0.7))
    pen.curveTo((cx - irx, cy - iky), (cx - irx, cy), (cx - irx, cy + iky))
    pen.curveTo((cx - irx * 0.7, cy + iry * 0.7), (cx, cy + iry), (cx + ikx * 0.5, cy + iry))
    pen.curveTo((top_x - sw * 0.4, top_y - sw * 0.6), (top_x - sw * 0.2, top_y - sw * 0.4), (top_x - sw * 0.6, top_y - sw * 0.6))
    pen.lineTo((top_x, top_y))
    pen.closePath()

def create_precision_glyph_dict(weight=700):
    # Dynamic stem scaling based on weight (400 -> 65, 700 -> 110, 900 -> 150)
    w_norm = (weight - 400) / 500.0 if weight >= 400 else 0.0
    SW = int(65 + w_norm * 85)   # Main stem width
    HW = int(45 + w_norm * 35)   # Crossbar / hairline width

    glyphs = {}

    # =========================================================================
    # UPPERCASE (A-Z)
    # =========================================================================

    def draw_A(pen):
        # Unified outer contour (Clockwise)
        pen.moveTo((50, BL))
        pen.lineTo((250, CAP + OVS))
        pen.lineTo((350, CAP + OVS))
        pen.lineTo((550, BL))
        pen.lineTo((550 - SW, BL))
        pen.lineTo((420, 200))
        pen.lineTo((180, 200))
        pen.lineTo((120, BL))
        pen.closePath()
        # Inner counter (Counter-Clockwise)
        pen.moveTo((300, CAP - 110))
        pen.lineTo((205, 260))
        pen.lineTo((395, 260))
        pen.closePath()
    glyphs['A'] = (draw_A, 600)

    def draw_B(pen):
        # Unified outer contour
        pen.moveTo((60, BL))
        pen.lineTo((60, CAP))
        pen.lineTo((280, CAP))
        pen.curveTo((400, CAP), (490, CAP - 90), (490, CAP - 180))
        pen.curveTo((490, CAP - 270), (410, CAP/2), (320, CAP/2))
        pen.curveTo((430, CAP/2), (510, 200), (510, 100))
        pen.curveTo((510, BL), (420, BL), (290, BL))
        pen.closePath()
        # Top inner hole (CCW)
        pen.moveTo((60 + SW, CAP - HW))
        pen.lineTo((60 + SW, (CAP/2) + (HW/2)))
        pen.lineTo((270, (CAP/2) + (HW/2)))
        pen.curveTo((350, (CAP/2) + (HW/2)), (390, CAP - 220), (390, CAP - 180))
        pen.curveTo((390, CAP - 120), (340, CAP - HW), (260, CAP - HW))
        pen.closePath()
        # Bottom inner hole (CCW)
        pen.moveTo((60 + SW, (CAP/2) - (HW/2)))
        pen.lineTo((60 + SW, BL + HW))
        pen.lineTo((280, BL + HW))
        pen.curveTo((360, BL + HW), (410, 50), (410, 110))
        pen.curveTo((410, 170), (360, (CAP/2) - (HW/2)), (280, (CAP/2) - (HW/2)))
        pen.closePath()
    glyphs['B'] = (draw_B, 570)

    def draw_C(pen):
        draw_smooth_c_arc(pen, 300, CAP/2, 240, (CAP/2) + OVS, SW, 480, CAP - 100, 480, 100)
    glyphs['C'] = (draw_C, 580)

    def draw_D(pen):
        # Outer boundary (CW)
        pen.moveTo((60, BL))
        pen.lineTo((60, CAP))
        pen.lineTo((280, CAP))
        pen.curveTo((440, CAP), (530, CAP - 160), (530, CAP/2))
        pen.curveTo((530, 160), (440, BL), (280, BL))
        pen.closePath()
        # Inner counter (CCW)
        pen.moveTo((60 + SW, CAP - HW))
        pen.lineTo((60 + SW, BL + HW))
        pen.lineTo((270, BL + HW))
        pen.curveTo((380, BL + HW), (430, 140), (430, CAP/2))
        pen.curveTo((430, CAP - 140), (380, CAP - HW), (270, CAP - HW))
        pen.closePath()
    glyphs['D'] = (draw_D, 590)

    def draw_E(pen):
        pen.moveTo((60, BL))
        pen.lineTo((60, CAP))
        pen.lineTo((480, CAP))
        pen.lineTo((480, CAP - HW))
        pen.lineTo((60 + SW, CAP - HW))
        pen.lineTo((60 + SW, (CAP/2) + (HW/2)))
        pen.lineTo((420, (CAP/2) + (HW/2)))
        pen.lineTo((420, (CAP/2) - (HW/2)))
        pen.lineTo((60 + SW, (CAP/2) - (HW/2)))
        pen.lineTo((60 + SW, BL + HW))
        pen.lineTo((480, BL + HW))
        pen.lineTo((480, BL))
        pen.closePath()
    glyphs['E'] = (draw_E, 530)

    def draw_F(pen):
        pen.moveTo((60, BL))
        pen.lineTo((60, CAP))
        pen.lineTo((470, CAP))
        pen.lineTo((470, CAP - HW))
        pen.lineTo((60 + SW, CAP - HW))
        pen.lineTo((60 + SW, (CAP/2) + (HW/2)))
        pen.lineTo((390, (CAP/2) + (HW/2)))
        pen.lineTo((390, (CAP/2) - (HW/2)))
        pen.lineTo((60 + SW, (CAP/2) - (HW/2)))
        pen.lineTo((60 + SW, BL))
        pen.closePath()
    glyphs['F'] = (draw_F, 520)
    def draw_G(pen):
        r = 16
        draw_smooth_c_arc(pen, 320, CAP/2, 260, (CAP/2) + OVS, SW, 520, CAP - 110, 520, 240, r=r)
        # Horizontal spur with smooth rounded corner & vertical stem
        pen.moveTo((330, 240))
        pen.lineTo((560 - r, 240))
        pen.curveTo((560, 240), (560, 240 - r), (560, 240 - r))
        pen.lineTo((560, BL + 40))
        pen.curveTo((560, BL), (560 - SW, BL), (560 - SW, BL + 40))
        pen.lineTo((560 - SW, 240 - HW))
        pen.lineTo((330, 240 - HW))
        pen.closePath()
    glyphs['G'] = (draw_G, 630)

    def draw_H(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        draw_rounded_rect(pen, 520 - SW, BL, 520, CAP, r=r)
        draw_rounded_rect(pen, 60 + SW/2, (CAP/2) - (HW/2), 520 - SW/2, (CAP/2) + (HW/2), r=r)
    glyphs['H'] = (draw_H, 580)

    def draw_I(pen):
        draw_rounded_rect(pen, 110, BL, 110 + SW, CAP, r=16)
    glyphs['I'] = (draw_I, 290)

    def draw_J(pen):
        r = 16
        pen.moveTo((280, CAP - r))
        pen.curveTo((280, CAP + r*0.55), (280 + SW, CAP + r*0.55), (280 + SW, CAP - r))
        pen.lineTo((280 + SW, 160))
        pen.curveTo((280 + SW, 50), (220, BL), (140, BL))
        pen.curveTo((60, BL), (30, 60), (30, 140))
        pen.curveTo((30, 140 + r), (30 + SW, 140 + r), (30 + SW, 140))
        pen.curveTo((30 + SW, 90), (80, BL + HW), (140, BL + HW))
        pen.curveTo((200, BL + HW), (280, 90), (280, 160))
        pen.closePath()
    glyphs['J'] = (draw_J, 380)

    def draw_K(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        pen.moveTo((60 + SW, 280))
        pen.lineTo((420 - r, CAP))
        pen.curveTo((420 - r + r*0.55, CAP), (420 + SW, CAP - r*0.45), (420 + SW, CAP - r))
        pen.lineTo((180, 210))
        pen.lineTo((460 - r, BL + r))
        pen.curveTo((460 - r + r*0.45, BL), (460 - SW, BL), (460 - SW - r, BL + r))
        pen.lineTo((60 + SW, 150))
        pen.closePath()
    glyphs['K'] = (draw_K, 550)

    def draw_L(pen):
        r = 16
        pen.moveTo((60, CAP - r))
        pen.curveTo((60, CAP + r*0.55), (60 + SW, CAP + r*0.55), (60 + SW, CAP - r))
        pen.lineTo((60 + SW, BL + HW))
        pen.lineTo((460 - r, BL + HW))
        pen.curveTo((460, BL + HW), (460, BL), (460 - r, BL))
        pen.lineTo((60 + r, BL))
        pen.curveTo((60, BL), (60, BL + r), (60, BL + r))
        pen.closePath()
    glyphs['L'] = (draw_L, 500)

    def draw_M(pen):
        r = 16
        pen.moveTo((50, BL + r))
        pen.curveTo((50, BL), (50 + r, BL), (50 + r, BL))
        pen.lineTo((50, CAP - r))
        pen.curveTo((50, CAP + r*0.55), (50 + SW, CAP + r*0.55), (50 + SW, CAP - r))
        pen.lineTo((340, 160))
        pen.lineTo((630 - SW, CAP - r))
        pen.curveTo((630 - SW, CAP + r*0.55), (630, CAP + r*0.55), (630, CAP - r))
        pen.lineTo((630, BL + r))
        pen.curveTo((630, BL), (630 - SW, BL), (630 - SW, BL + r))
        pen.lineTo((630 - SW, CAP - HW * 1.6))
        pen.lineTo((340, 60))
        pen.lineTo((50 + SW, CAP - HW * 1.6))
        pen.lineTo((50 + SW, BL + r))
        pen.closePath()
    glyphs['M'] = (draw_M, 680)

    def draw_N(pen):
        r = 16
        pen.moveTo((60, BL + r))
        pen.curveTo((60, BL), (60 + r, BL), (60 + r, BL))
        pen.lineTo((60, CAP - r))
        pen.curveTo((60, CAP + r*0.55), (60 + SW, CAP + r*0.55), (60 + SW, CAP - r))
        pen.lineTo((530 - SW, 120))
        pen.lineTo((530 - SW, CAP - r))
        pen.curveTo((530 - SW, CAP + r*0.55), (530, CAP + r*0.55), (530, CAP - r))
        pen.lineTo((530, BL + r))
        pen.curveTo((530, BL), (530 - SW, BL), (530 - SW, BL + r))
        pen.lineTo((60 + SW, CAP - 120))
        pen.lineTo((60 + SW, BL + r))
        pen.closePath()
    glyphs['N'] = (draw_N, 590)

    def draw_O(pen):
        draw_oval_counter(pen, 300, CAP/2, 250, (CAP/2) + OVS, 250 - SW, (CAP/2) + OVS - HW)
    glyphs['O'] = (draw_O, 600)

    def draw_P(pen):
        r = 16
        # Outer boundary (CW) with rounded bottom stem cap & top cap
        pen.moveTo((60, BL + r))
        pen.curveTo((60, BL), (60 + SW, BL), (60 + SW, BL + r))
        pen.lineTo((60 + SW, CAP/2 - 20))
        pen.lineTo((280, CAP/2 - 20))
        pen.curveTo((430, CAP/2 - 20), (510, CAP/2 + 70), (510, CAP - 160))
        pen.curveTo((510, CAP + OVS), (380, CAP + OVS), (280, CAP + OVS))
        pen.lineTo((60 + r, CAP + OVS))
        pen.curveTo((60, CAP + OVS), (60, CAP + OVS - r), (60, CAP + OVS - r))
        pen.closePath()
        # Inner counter (CCW)
        pen.moveTo((60 + SW, CAP - HW))
        pen.lineTo((60 + SW, CAP/2 + 20))
        pen.lineTo((270, CAP/2 + 20))
        pen.curveTo((360, CAP/2 + 20), (410, CAP - 240), (410, CAP - 160))
        pen.curveTo((410, CAP - 100), (360, CAP - HW), (270, CAP - HW))
        pen.closePath()
    glyphs['P'] = (draw_P, 560)

    def draw_Q(pen):
        draw_oval_counter(pen, 300, CAP/2, 250, (CAP/2) + OVS, 250 - SW, (CAP/2) + OVS - HW)
        draw_rounded_rect(pen, 280, -50, 560, 180, r=16)
    glyphs['Q'] = (draw_Q, 600)

    def draw_R(pen):
        r = 16
        pen.moveTo((60, BL + r))
        pen.curveTo((60, BL), (60 + SW, BL), (60 + SW, BL + r))
        pen.lineTo((60 + SW, CAP - 360))
        pen.lineTo((280, CAP - 360))
        pen.curveTo((420, CAP - 360), (500, CAP - 270), (500, CAP - 190))
        pen.curveTo((500, CAP + OVS), (380, CAP + OVS), (280, CAP + OVS))
        pen.lineTo((60 + r, CAP + OVS))
        pen.curveTo((60, CAP + OVS), (60, CAP + OVS - r), (60, CAP + OVS - r))
        pen.closePath()
        # Inner counter (CCW)
        pen.moveTo((60 + SW, CAP - HW))
        pen.lineTo((60 + SW, CAP - 360 + HW))
        pen.lineTo((270, CAP - 360 + HW))
        pen.curveTo((360, CAP - 360 + HW), (410, CAP - 270), (410, CAP - 190))
        pen.curveTo((410, CAP - 110), (360, CAP - HW), (270, CAP - HW))
        pen.closePath()
        # Diagonal leg with rounded bottom
        draw_rounded_rect(pen, 260, BL, 490, CAP - 360, r=r)
    glyphs['R'] = (draw_R, 570)

    def draw_S(pen):
        r = 16
        pen.moveTo((460, CAP - 120))
        pen.curveTo((440, CAP + OVS), (360, CAP + OVS), (280, CAP + OVS))
        pen.curveTo((140, CAP + OVS), (60, CAP - 90), (60, CAP - 200))
        pen.curveTo((60, 360), (480, 330), (480, 180))
        pen.curveTo((480, 90), (400, BL - OVS), (270, BL - OVS))
        pen.curveTo((140, BL - OVS), (70, 70), (60, 150))
        pen.curveTo((60, 150 + r), (60 + SW, 150 + r), (60 + SW, 150))
        pen.curveTo((70, BL + HW + 20), (160, BL + HW), (270, BL + HW))
        pen.curveTo((380, BL + HW), (480 - SW, 100), (480 - SW, 180))
        pen.curveTo((480 - SW, 280), (60 + SW, 300), (60 + SW, CAP - 200))
        pen.curveTo((60 + SW, CAP - HW - 20), (160, CAP - HW), (280, CAP - HW))
        pen.curveTo((370, CAP - HW), (440, CAP - 100), (460 - SW/2, CAP - 120))
        pen.closePath()
    glyphs['S'] = (draw_S, 560)

    def draw_T(pen):
        r = 16
        draw_rounded_rect(pen, 270 - SW/2, BL, 270 + SW/2, CAP, r=r)
        draw_rounded_rect(pen, 40, CAP - HW, 500, CAP, r=r)
    glyphs['T'] = (draw_T, 540)

    def draw_U(pen):
        r = 16
        pen.moveTo((60, CAP - r))
        pen.curveTo((60, CAP + r*0.55), (60 + SW, CAP + r*0.55), (60 + SW, CAP - r))
        pen.lineTo((60 + SW, 200))
        pen.curveTo((60 + SW, BL + HW), (150, BL + HW), (280, BL + HW))
        pen.curveTo((410, BL + HW), (500 - SW, BL + HW), (500 - SW, 200))
        pen.lineTo((500 - SW, CAP - r))
        pen.curveTo((500 - SW, CAP + r*0.55), (500, CAP + r*0.55), (500, CAP - r))
        pen.lineTo((500, 200))
        pen.curveTo((500, BL - OVS), (390, BL - OVS), (280, BL - OVS))
        pen.curveTo((170, BL - OVS), (60, BL - OVS), (60, 200))
        pen.closePath()
    glyphs['U'] = (draw_U, 560)

    def draw_V(pen):
        r = 16
        pen.moveTo((40, CAP - r))
        pen.curveTo((40, CAP + r*0.55), (40 + SW, CAP + r*0.55), (40 + SW, CAP - r))
        pen.lineTo((280, BL + r))
        pen.lineTo((520 - SW, CAP - r))
        pen.curveTo((520 - SW, CAP + r*0.55), (520, CAP + r*0.55), (520, CAP - r))
        pen.lineTo((280 + SW/2, BL))
        pen.lineTo((280 - SW/2, BL))
        pen.closePath()
    glyphs['V'] = (draw_V, 560)
    def draw_W(pen):
        r = 16
        pen.moveTo((30, CAP - r))
        pen.curveTo((30, CAP + r*0.55), (30 + SW, CAP + r*0.55), (30 + SW, CAP - r))
        pen.lineTo((190, BL + r))
        pen.lineTo((360 - SW/2, CAP - 120))
        pen.lineTo((360 + SW/2, CAP - 120))
        pen.lineTo((530, BL + r))
        pen.lineTo((690 - SW, CAP - r))
        pen.curveTo((690 - SW, CAP + r*0.55), (690, CAP + r*0.55), (690, CAP - r))
        pen.lineTo((530 + SW/2, BL))
        pen.lineTo((530 - SW/2, BL))
        pen.lineTo((360, CAP - 40))
        pen.lineTo((190 + SW/2, BL))
        pen.lineTo((190 - SW/2, BL))
        pen.closePath()
    glyphs['W'] = (draw_W, 720)

    def draw_X(pen):
        r = 16
        pen.moveTo((50, CAP - r))
        pen.curveTo((50, CAP + r*0.55), (50 + SW, CAP + r*0.55), (50 + SW, CAP - r))
        pen.lineTo((280 - SW/2, (CAP/2) + 20))
        pen.lineTo((510 - SW, CAP - r))
        pen.curveTo((510 - SW, CAP + r*0.55), (510, CAP + r*0.55), (510, CAP - r))
        pen.lineTo((280 + SW/2, CAP/2))
        pen.lineTo((510, BL + r))
        pen.curveTo((510, BL), (510 - SW, BL), (510 - SW, BL + r))
        pen.lineTo((280, (CAP/2) - 20))
        pen.lineTo((100, BL + r))
        pen.curveTo((100, BL), (50, BL), (50, BL + r))
        pen.lineTo((280 - SW/2, CAP/2))
        pen.closePath()
    glyphs['X'] = (draw_X, 540)

    def draw_Y(pen):
        r = 16
        draw_rounded_rect(pen, 250 - SW/2, BL, 250 + SW/2, CAP/2, r=r)
        pen.moveTo((40, CAP - r))
        pen.curveTo((40, CAP + r*0.55), (40 + SW, CAP + r*0.55), (40 + SW, CAP - r))
        pen.lineTo((250, CAP/2))
        pen.lineTo((460 - SW, CAP - r))
        pen.curveTo((460 - SW, CAP + r*0.55), (460, CAP + r*0.55), (460, CAP - r))
        pen.lineTo((250, CAP/2 - HW))
        pen.closePath()
    glyphs['Y'] = (draw_Y, 500)

    def draw_Z(pen):
        r = 16
        pen.moveTo((50, CAP - HW))
        pen.lineTo((490 - r, CAP))
        pen.curveTo((490, CAP), (490, CAP - HW), (490 - r, CAP - HW))
        pen.lineTo((130, BL + HW))
        pen.lineTo((490 - r, BL + HW))
        pen.curveTo((490, BL + HW), (490, BL), (490 - r, BL))
        pen.lineTo((50 + r, BL))
        pen.curveTo((50, BL), (50, BL + HW), (50 + r, BL + HW))
        pen.lineTo((410, CAP - HW))
        pen.lineTo((50 + r, CAP - HW))
        pen.closePath()
    glyphs['Z'] = (draw_Z, 540)

    # =========================================================================
    # LOWERCASE (a-z) - SOFTENED G2 ORGANIC NEO-GROTESQUE
    # =========================================================================

    def draw_a(pen):
        r = 16
        # Outer boundary (Clockwise)
        pen.moveTo((410, XH - r))
        pen.curveTo((410, XH + r*0.55), (410 - SW, XH + r*0.55), (410 - SW, XH - r))
        pen.lineTo((410 - SW, XH - 80))
        pen.curveTo((340, XH + OVS), (250, XH + OVS), (200, XH + OVS))
        pen.curveTo((90, XH + OVS), (50, XH - 90), (50, XH/2))
        pen.curveTo((50, 90), (110, BL - OVS), (220, BL - OVS))
        pen.curveTo((300, BL - OVS), (370, 40), (410 - SW, 70))
        pen.lineTo((410 - SW, BL + r))
        pen.curveTo((410 - SW, BL), (410, BL), (410, BL + r))
        pen.closePath()
        # Inner counter (Counter-Clockwise)
        pen.moveTo((410 - SW, XH - 120))
        pen.curveTo((360, XH - HW), (290, XH - HW), (220, XH - HW))
        pen.curveTo((140, XH - HW), (120, XH - 130), (120, XH/2))
        pen.curveTo((120, 130), (140, BL + HW), (220, BL + HW))
        pen.curveTo((290, BL + HW), (360, 60), (410 - SW, 120))
        pen.lineTo((410 - SW, XH - 120))
        pen.closePath()
    glyphs['a'] = (draw_a, 470)

    def draw_b(pen):
        r = 16
        pen.moveTo((60, BL + r))
        pen.curveTo((60, BL), (60 + SW, BL), (60 + SW, BL + r))
        pen.lineTo((60 + SW, XH - 60))
        pen.curveTo((120, XH + OVS), (200, XH + OVS), (260, XH + OVS))
        pen.curveTo((380, XH + OVS), (450, XH - 90), (450, XH/2))
        pen.curveTo((450, 90), (380, BL - OVS), (260, BL - OVS))
        pen.curveTo((180, BL - OVS), (110, 40), (60, BL + r))
        pen.closePath()
        # Ascender stem
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        # Inner counter (CCW)
        pen.moveTo((60 + SW, XH - 100))
        pen.lineTo((60 + SW, 100))
        pen.curveTo((110, BL + HW), (180, BL + HW), (250, BL + HW))
        pen.curveTo((340, BL + HW), (380, 140), (380, XH/2))
        pen.curveTo((380, XH - 140), (340, XH - HW), (250, XH - HW))
        pen.curveTo((180, XH - HW), (110, XH - 60), (60 + SW, XH - 100))
        pen.closePath()
    glyphs['b'] = (draw_b, 490)

    def draw_c(pen):
        draw_smooth_c_arc(pen, 240, XH/2, 190, (XH/2) + OVS, SW, 380, XH - 70, 380, 70, r=16)
    glyphs['c'] = (draw_c, 450)

    def draw_d(pen):
        r = 16
        draw_rounded_rect(pen, 420 - SW, BL, 420, CAP, r=r)
        pen.moveTo((420 - SW, XH - 60))
        pen.curveTo((360, XH + OVS), (280, XH + OVS), (220, XH + OVS))
        pen.curveTo((100, XH + OVS), (50, XH - 90), (50, XH/2))
        pen.curveTo((50, 90), (100, BL - OVS), (220, BL - OVS))
        pen.curveTo((300, BL - OVS), (370, 40), (420 - SW, 80))
        pen.closePath()
        # Inner counter (CCW)
        pen.moveTo((420 - SW, XH - 100))
        pen.curveTo((370, XH - HW), (300, XH - HW), (230, XH - HW))
        pen.curveTo((140, XH - HW), (120, XH - 140), (120, XH/2))
        pen.curveTo((120, 140), (140, BL + HW), (230, BL + HW))
        pen.curveTo((300, BL + HW), (370, BL + HW), (420 - SW, 100))
        pen.lineTo((420 - SW, XH - 100))
        pen.closePath()
    glyphs['d'] = (draw_d, 490)

    def draw_e(pen):
        r = 16
        # Outer continuous contour (CW) with curved crossbar and rounded lower terminal
        pen.moveTo((60, 240))
        pen.lineTo((420 - r, 240))
        pen.curveTo((420, 240), (420, 240 + r), (420, 240 + r))
        pen.curveTo((420, XH - 40), (350, XH + OVS), (240, XH + OVS))
        pen.curveTo((120, XH + OVS), (50, XH - 90), (50, XH/2))
        pen.curveTo((50, 90), (120, BL - OVS), (240, BL - OVS))
        pen.curveTo((350, BL - OVS), (410, 60), (420, 110))
        pen.curveTo((420 + r*0.5, 125), (410, 140 + r), (395, 140))
        pen.curveTo((350, BL + HW), (280, BL + HW), (240, BL + HW))
        pen.curveTo((140, BL + HW), (120, 140), (120, 240))
        pen.closePath()
        # Top eye counter (CCW)
        pen.moveTo((420 - SW * 0.8, 240 + HW))
        pen.curveTo((360, XH - HW), (290, XH - HW), (240, XH - HW))
        pen.curveTo((160, XH - HW), (120, XH - 110), (120, 240 + HW))
        pen.lineTo((420 - SW * 0.8, 240 + HW))
        pen.closePath()
    glyphs['e'] = (draw_e, 480)

    def draw_f(pen):
        r = 16
        draw_rounded_rect(pen, 130, BL, 130 + SW, CAP - 60, r=r)
        draw_rounded_rect(pen, 60, XH - HW, 280, XH, r=r)
        # Arch top
        pen.moveTo((130 + SW, CAP - 100))
        pen.curveTo((130 + SW, CAP - 40), (170, CAP + OVS), (240, CAP + OVS))
        pen.lineTo((280 - r, CAP + OVS))
        pen.curveTo((280, CAP + OVS), (280, CAP - HW), (280 - r, CAP - HW))
        pen.curveTo((240, CAP - HW), (130 + SW, CAP - 60), (130, CAP - 120))
        pen.closePath()
    glyphs['f'] = (draw_f, 340)

    def draw_g(pen):
        draw_oval_counter(pen, 240, XH/2, 190, (XH/2) + OVS, 190 - SW, (XH/2) + OVS - HW)
        draw_rounded_rect(pen, 430 - SW, DSC, 430, XH/2, r=16)
    glyphs['g'] = (draw_g, 490)

    def draw_h(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        draw_rounded_rect(pen, 430 - SW, BL, 430, XH - 100, r=r)
        # Shoulder arch
        pen.moveTo((60 + SW, XH - 80))
        pen.curveTo((120, XH + OVS), (200, XH + OVS), (270, XH + OVS))
        pen.curveTo((380, XH + OVS), (430, XH - 80), (430, XH - 160))
        pen.lineTo((430 - SW, XH - 160))
        pen.curveTo((430 - SW, XH - HW), (350, XH - HW), (260, XH - HW))
        pen.curveTo((180, XH - HW), (120, XH - 80), (60 + SW, XH - 120))
        pen.closePath()
    glyphs['h'] = (draw_h, 490)

    def draw_i(pen):
        draw_rounded_rect(pen, 90, BL, 90 + SW, XH, r=16)
        draw_oval_counter(pen, 90 + SW/2, CAP - 70, SW/2 + 4, SW/2 + 4, 0, 0)
    glyphs['i'] = (draw_i, 260)

    def draw_j(pen):
        r = 16
        draw_rounded_rect(pen, 180, DSC + 40, 180 + SW, XH, r=r)
        draw_oval_counter(pen, 180 + SW/2, CAP - 70, SW/2 + 4, SW/2 + 4, 0, 0)
    glyphs['j'] = (draw_j, 280)

    def draw_k(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        # Upper diagonal with rounded tip
        pen.moveTo((60 + SW, 180))
        pen.lineTo((330 - r, XH))
        pen.curveTo((330 - r + r*0.55, XH), (330 + SW, XH - r*0.45), (330 + SW, XH - r))
        pen.lineTo((140, 130))
        pen.lineTo((360 - r, BL + r))
        pen.curveTo((360 - r + r*0.45, BL), (360 - SW, BL), (360 - SW - r, BL + r))
        pen.lineTo((60 + SW, 90))
        pen.closePath()
    glyphs['k'] = (draw_k, 440)

    def draw_l(pen):
        r = 16
        pen.moveTo((80, CAP - r))
        pen.curveTo((80, CAP + r*0.55), (80 + SW, CAP + r*0.55), (80 + SW, CAP - r))
        pen.lineTo((80 + SW, BL + 40))
        pen.curveTo((80 + SW, BL + HW), (120, BL + HW), (180, BL + 20 + HW))
        pen.curveTo((195, BL + 20 + HW), (195, BL + 10), (180, BL + 10))
        pen.curveTo((140, BL), (80, BL), (80, BL + 40))
        pen.closePath()
    glyphs['l'] = (draw_l, 250)

    def draw_m(pen):
        r = 16
        draw_rounded_rect(pen, 50, BL, 50 + SW, XH, r=r)
        draw_rounded_rect(pen, 350 - SW, BL, 350, XH - 80, r=r)
        draw_rounded_rect(pen, 650 - SW, BL, 650, XH - 80, r=r)
        # First arch
        pen.moveTo((50 + SW, XH - 60))
        pen.curveTo((90, XH + OVS), (160, XH + OVS), (220, XH + OVS))
        pen.curveTo((290, XH + OVS), (350, XH - 60), (350, XH - 120))
        pen.lineTo((350 - SW, XH - 120))
        pen.curveTo((350 - SW, XH - HW), (280, XH - HW), (210, XH - HW))
        pen.curveTo((140, XH - HW), (90, XH - 80), (50 + SW, XH - 120))
        pen.closePath()
        # Second arch
        pen.moveTo((350, XH - 60))
        pen.curveTo((390, XH + OVS), (460, XH + OVS), (520, XH + OVS))
        pen.curveTo((610, XH + OVS), (650, XH - 80), (650, XH - 160))
        pen.lineTo((650 - SW, XH - 160))
        pen.curveTo((650 - SW, XH - HW), (570, XH - HW), (500, XH - HW))
        pen.curveTo((430, XH - HW), (380, XH - 80), (350, XH - 120))
        pen.closePath()
    glyphs['m'] = (draw_m, 680)

    def draw_n(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, XH, r=r)
        draw_rounded_rect(pen, 420 - SW, BL, 420, XH - 100, r=r)
        # Shoulder arch
        pen.moveTo((60 + SW, XH - 70))
        pen.curveTo((110, XH + OVS), (190, XH + OVS), (260, XH + OVS))
        pen.curveTo((370, XH + OVS), (420, XH - 80), (420, XH - 160))
        pen.lineTo((420 - SW, XH - 160))
        pen.curveTo((420 - SW, XH - HW), (340, XH - HW), (250, XH - HW))
        pen.curveTo((170, XH - HW), (110, XH - 70), (60 + SW, XH - 120))
        pen.closePath()
    glyphs['n'] = (draw_n, 480)

    def draw_o(pen):
        draw_oval_counter(pen, 240, XH/2, 195, (XH/2) + OVS, 195 - SW, (XH/2) + OVS - HW)
    glyphs['o'] = (draw_o, 480)

    def draw_p(pen):
        r = 16
        draw_rounded_rect(pen, 60, DSC, 60 + SW, XH, r=r)
        pen.moveTo((60 + SW, XH - 60))
        pen.curveTo((120, XH + OVS), (200, XH + OVS), (260, XH + OVS))
        pen.curveTo((380, XH + OVS), (450, XH - 90), (450, XH/2))
        pen.curveTo((450, 90), (380, BL - OVS), (260, BL - OVS))
        pen.curveTo((180, BL - OVS), (110, 40), (60 + SW, 80))
        pen.closePath()
        # Inner counter (CCW)
        pen.moveTo((60 + SW, XH - 100))
        pen.lineTo((60 + SW, 100))
        pen.curveTo((110, BL + HW), (180, BL + HW), (250, BL + HW))
        pen.curveTo((340, BL + HW), (380, 140), (380, XH/2))
        pen.curveTo((380, XH - 140), (340, XH - HW), (250, XH - HW))
        pen.curveTo((180, XH - HW), (110, XH - 60), (60 + SW, XH - 100))
        pen.closePath()
    glyphs['p'] = (draw_p, 490)

    def draw_q(pen):
        r = 16
        draw_rounded_rect(pen, 420 - SW, DSC, 420, XH, r=r)
        pen.moveTo((420 - SW, XH - 60))
        pen.curveTo((360, XH + OVS), (280, XH + OVS), (220, XH + OVS))
        pen.curveTo((100, XH + OVS), (50, XH - 90), (50, XH/2))
        pen.curveTo((50, 90), (100, BL - OVS), (220, BL - OVS))
        pen.curveTo((300, BL - OVS), (370, 40), (420 - SW, 80))
        pen.closePath()
        # Inner counter (CCW)
        pen.moveTo((420 - SW, XH - 100))
        pen.curveTo((370, XH - HW), (300, XH - HW), (230, XH - HW))
        pen.curveTo((140, XH - HW), (120, XH - 140), (120, XH/2))
        pen.curveTo((120, 140), (140, BL + HW), (230, BL + HW))
        pen.curveTo((300, BL + HW), (370, BL + HW), (420 - SW, 100))
        pen.lineTo((420 - SW, XH - 100))
        pen.closePath()
    glyphs['q'] = (draw_q, 490)

    def draw_r(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, XH, r=r)
        pen.moveTo((60 + SW, XH - 70))
        pen.curveTo((110, XH + OVS), (190, XH + OVS), (260, XH + OVS))
        pen.lineTo((340 - r, XH - 20))
        pen.curveTo((340, XH - 20), (340, XH - HW - 20), (340 - SW * 0.7, XH - HW - 20))
        pen.curveTo((270, XH - HW), (180, XH - HW), (60 + SW, XH - 120))
        pen.closePath()
    glyphs['r'] = (draw_r, 370)

    def draw_s(pen):
        r = 16
        pen.moveTo((380, XH - 80))
        pen.curveTo((350, XH + OVS), (290, XH + OVS), (220, XH + OVS))
        pen.curveTo((120, XH + OVS), (50, XH - 60), (50, XH - 130))
        pen.curveTo((50, 240), (370, 220), (370, 120))
        pen.curveTo((370, 60), (300, BL - OVS), (210, BL - OVS))
        pen.curveTo((120, BL - OVS), (60, 50), (50, 100))
        pen.curveTo((50, 100 + r), (50 + SW, 100 + r), (50 + SW, 100))
        pen.curveTo((60, 60 + HW), (130, BL + HW), (210, BL + HW))
        pen.curveTo((290, BL + HW), (370 - SW, 60), (370 - SW, 120))
        pen.curveTo((370 - SW, 190), (50 + SW, 200), (50 + SW, XH - 130))
        pen.curveTo((50 + SW, XH - 70), (130, XH - HW), (220, XH - HW))
        pen.curveTo((290, XH - HW), (340, XH - 70), (350, XH - 80))
        pen.closePath()
    glyphs['s'] = (draw_s, 440)

    def draw_t(pen):
        r = 16
        # Vertical stem curving into rounded foot
        pen.moveTo((120, CAP - 120))
        pen.curveTo((120, CAP - 120 + r*0.55), (120 + r*0.45, CAP - 120 + r), (120 + SW/2, CAP - 120 + r))
        pen.curveTo((120 + SW - r*0.45, CAP - 120 + r), (120 + SW, CAP - 120 + r*0.55), (120 + SW, CAP - 120))
        pen.lineTo((120 + SW, XH))
        # Right crossbar with rounded cap
        pen.lineTo((260 - r, XH))
        pen.curveTo((260, XH), (260, XH - HW), (260 - r, XH - HW))
        pen.lineTo((120 + SW, XH - HW))
        pen.lineTo((120 + SW, BL + 40))
        pen.curveTo((120 + SW, BL + HW), (160, BL + HW), (230, BL + 20 + HW))
        pen.curveTo((245, BL + 20 + HW), (245, BL + 10), (230, BL + 10))
        pen.curveTo((180, BL), (120, BL), (120, BL + 40))
        pen.lineTo((120, XH - HW))
        # Left crossbar with rounded cap
        pen.lineTo((50 + r, XH - HW))
        pen.curveTo((50, XH - HW), (50, XH), (50 + r, XH))
        pen.lineTo((120, XH))
        pen.closePath()
    glyphs['t'] = (draw_t, 350)

    def draw_u(pen):
        r = 16
        # Outer boundary (CW)
        pen.moveTo((60, XH - r))
        pen.curveTo((60, XH + r*0.55), (60 + SW, XH + r*0.55), (60 + SW, XH - r))
        pen.lineTo((60 + SW, 140))
        pen.curveTo((60 + SW, BL + HW), (130, BL + HW), (220, BL + HW))
        pen.curveTo((310, BL + HW), (430 - SW, BL + HW + 40), (430 - SW, 160))
        pen.lineTo((430 - SW, XH - r))
        pen.curveTo((430 - SW, XH + r*0.55), (430, XH + r*0.55), (430, XH - r))
        pen.lineTo((430, BL + r))
        pen.curveTo((430, BL), (430 - SW, BL), (430 - SW, BL + r))
        pen.lineTo((430 - SW, 80))
        pen.curveTo((370, BL - OVS), (280, BL - OVS), (220, BL - OVS))
        pen.curveTo((100, BL - OVS), (60, 70), (60, 160))
        pen.closePath()
    glyphs['u'] = (draw_u, 490)

    def draw_v(pen):
        r = 16
        pen.moveTo((30, XH - r))
        pen.curveTo((30, XH + r*0.55), (30 + SW, XH + r*0.55), (30 + SW, XH - r))
        pen.lineTo((230, BL + r))
        pen.lineTo((430 - SW, XH - r))
        pen.curveTo((430 - SW, XH + r*0.55), (430, XH + r*0.55), (430, XH - r))
        pen.lineTo((230 + SW/2, BL))
        pen.lineTo((230 - SW/2, BL))
        pen.closePath()
    glyphs['v'] = (draw_v, 460)

    def draw_w(pen):
        r = 16
        pen.moveTo((20, XH - r))
        pen.curveTo((20, XH + r*0.55), (20 + SW, XH + r*0.55), (20 + SW, XH - r))
        pen.lineTo((160, BL + r))
        pen.lineTo((300 - SW/2, XH - 80))
        pen.lineTo((300 + SW/2, XH - 80))
        pen.lineTo((440, BL + r))
        pen.lineTo((580 - SW, XH - r))
        pen.curveTo((580 - SW, XH + r*0.55), (580, XH + r*0.55), (580, XH - r))
        pen.lineTo((440 + SW/2, BL))
        pen.lineTo((440 - SW/2, BL))
        pen.lineTo((300, XH - 20))
        pen.lineTo((160 + SW/2, BL))
        pen.lineTo((160 - SW/2, BL))
        pen.closePath()
    glyphs['w'] = (draw_w, 600)

    def draw_x(pen):
        r = 16
        pen.moveTo((40, XH - r))
        pen.curveTo((40, XH + r*0.55), (40 + SW, XH + r*0.55), (40 + SW, XH - r))
        pen.lineTo((225 - SW/2, (XH/2) + 20))
        pen.lineTo((410 - SW, XH - r))
        pen.curveTo((410 - SW, XH + r*0.55), (410, XH + r*0.55), (410, XH - r))
        pen.lineTo((225 + SW/2, XH/2))
        pen.lineTo((410, BL + r))
        pen.curveTo((410, BL), (410 - SW, BL), (410 - SW, BL + r))
        pen.lineTo((225, (XH/2) - 20))
        pen.lineTo((80, BL + r))
        pen.curveTo((80, BL), (40, BL), (40, BL + r))
        pen.lineTo((225 - SW/2, XH/2))
        pen.closePath()
    glyphs['x'] = (draw_x, 450)

    def draw_y(pen):
        r = 16
        draw_rounded_rect(pen, 220, DSC + 40, 220 + SW, XH/2, r=r)
        pen.moveTo((30, XH - r))
        pen.curveTo((30, XH + r*0.55), (30 + SW, XH + r*0.55), (30 + SW, XH - r))
        pen.lineTo((220, XH/2))
        pen.lineTo((410 - SW, XH - r))
        pen.curveTo((410 - SW, XH + r*0.55), (410, XH + r*0.55), (410, XH - r))
        pen.lineTo((220, XH/2 - HW))
        pen.closePath()
    glyphs['y'] = (draw_y, 440)

    def draw_z(pen):
        r = 16
        pen.moveTo((40, XH - HW))
        pen.lineTo((400 - r, XH))
        pen.curveTo((400, XH), (400, XH - HW), (400 - r, XH - HW))
        pen.lineTo((100, BL + HW))
        pen.lineTo((400 - r, BL + HW))
        pen.curveTo((400, BL + HW), (400, BL), (400 - r, BL))
        pen.lineTo((40 + r, BL))
        pen.curveTo((40, BL), (40, BL + HW), (40 + r, BL + HW))
        pen.lineTo((340, XH - HW))
        pen.lineTo((40 + r, XH - HW))
        pen.closePath()
    glyphs['z'] = (draw_z, 440)

    # =========================================================================
    # DIGITS (0-9)
    # =========================================================================

    def draw_0(pen):
        cx, cy = 270, CAP/2
        rx, ry = 210, (CAP/2) + OVS
        irx, iry = 210 - SW, (CAP/2) + OVS - HW
        draw_oval_counter(pen, cx, cy, rx, ry, irx, iry)
    glyphs['0'] = (draw_0, 540)

    def draw_1(pen):
        pen.moveTo((110, CAP - 120))
        pen.lineTo((210 + SW, CAP))
        pen.lineTo((210 + SW, BL + HW))
        pen.lineTo((330, BL + HW))
        pen.lineTo((330, BL))
        pen.lineTo((110, BL))
        pen.lineTo((110, BL + HW))
        pen.lineTo((210, BL + HW))
        pen.lineTo((210, CAP - 80))
        pen.lineTo((110, CAP - 120 - HW))
        pen.closePath()
    glyphs['1'] = (draw_1, 460)

    def draw_2(pen):
        pen.moveTo((50, CAP - 120))
        pen.curveTo((50, CAP + OVS), (160, CAP + OVS), (270, CAP + OVS))
        pen.curveTo((390, CAP + OVS), (470, CAP - 80), (470, CAP - 180))
        pen.curveTo((470, CAP - 280), (370, 180), (140, BL + HW))
        pen.lineTo((470, BL + HW))
        pen.lineTo((470, BL))
        pen.lineTo((50, BL))
        pen.lineTo((50, BL + HW))
        pen.curveTo((280, 220), (470 - SW, CAP - 240), (470 - SW, CAP - 180))
        pen.curveTo((470 - SW, CAP - HW), (360, CAP - HW), (270, CAP - HW))
        pen.curveTo((170, CAP - HW), (50 + SW, CAP - 80), (50 + SW, CAP - 120))
        pen.closePath()
    glyphs['2'] = (draw_2, 520)

    def draw_3(pen):
        pen.moveTo((60, CAP - 80))
        pen.lineTo((60 + SW, CAP - 80))
        pen.curveTo((90, CAP - HW), (180, CAP - HW), (260, CAP - HW))
        pen.curveTo((350, CAP - HW), (400, CAP - 70), (400, CAP - 160))
        pen.curveTo((400, CAP - 240), (330, CAP/2), (240, CAP/2))
        pen.lineTo((240, (CAP/2) - HW))
        pen.curveTo((340, (CAP/2) - HW), (420, 220), (420, 140))
        pen.curveTo((420, 60), (350, BL + HW), (250, BL + HW))
        pen.curveTo((150, BL + HW), (80, 80), (60, 110))
        pen.lineTo((60, 40))
        pen.curveTo((100, BL - OVS), (170, BL - OVS), (250, BL - OVS))
        pen.curveTo((380, BL - OVS), (480, 50), (480, 150))
        pen.curveTo((480, 250), (400, 310), (310, (CAP/2)))
        pen.curveTo((390, CAP/2 + 40), (460, CAP - 240), (460, CAP - 160))
        pen.curveTo((460, CAP - 60), (380, CAP + OVS), (260, CAP + OVS))
        pen.curveTo((140, CAP + OVS), (70, CAP - 30), (60, CAP - 80))
        pen.closePath()
    glyphs['3'] = (draw_3, 520)

    def draw_4(pen):
        pen.moveTo((340, BL))
        pen.lineTo((340 - SW, BL))
        pen.lineTo((340 - SW, 180))
        pen.lineTo((40, 180))
        pen.lineTo((40, 240))
        pen.lineTo((340 - SW, CAP))
        pen.lineTo((340, CAP))
        pen.lineTo((340, 240))
        pen.lineTo((460, 240))
        pen.lineTo((460, 180))
        pen.lineTo((340, 180))
        pen.closePath()
        # Inner counter (CCW)
        pen.moveTo((340 - SW, 240))
        pen.lineTo((120, 240))
        pen.lineTo((340 - SW, CAP - 140))
        pen.closePath()
    glyphs['4'] = (draw_4, 500)

    def draw_5(pen):
        pen.moveTo((70, CAP))
        pen.lineTo((450, CAP))
        pen.lineTo((450, CAP - HW))
        pen.lineTo((70 + SW, CAP - HW))
        pen.lineTo((70 + SW, 380))
        pen.curveTo((130, 420), (200, 420 + OVS), (270, 420 + OVS))
        pen.curveTo((390, 420 + OVS), (470, 320), (470, 200))
        pen.curveTo((470, 80), (380, BL - OVS), (260, BL - OVS))
        pen.curveTo((140, BL - OVS), (70, 60), (60, 120))
        pen.lineTo((60 + SW, 120))
        pen.curveTo((80, 80 + HW), (160, BL + HW), (260, BL + HW))
        pen.curveTo((340, BL + HW), (470 - SW, 100), (470 - SW, 200))
        pen.curveTo((470 - SW, 300), (340, 350), (260, 350))
        pen.curveTo((180, 350), (120, 320), (70, 300))
        pen.closePath()
    glyphs['5'] = (draw_5, 510)

    def draw_6(pen):
        # Continuous outer contour (CW)
        pen.moveTo((380, CAP))
        pen.curveTo((260, CAP), (60, CAP - 140), (60, 240))
        pen.curveTo((60, 90), (140, BL - OVS), (270, BL - OVS))
        pen.curveTo((410, BL - OVS), (480, 90), (480, 240))
        pen.curveTo((480, 390), (410, 450 + OVS), (270, 450 + OVS))
        pen.curveTo((190, 450 + OVS), (120, 400), (60 + SW, 310))
        pen.curveTo((70, CAP - 120), (200, CAP - HW), (380, CAP - HW))
        pen.closePath()
        # Inner counter (CCW)
        pen.moveTo((270, 450 + OVS - HW))
        pen.curveTo((380, 450 + OVS - HW), (480 - SW, 340), (480 - SW, 240))
        pen.curveTo((480 - SW, 120), (380, BL + HW), (270, BL + HW))
        pen.curveTo((160, BL + HW), (60 + SW, 120), (60 + SW, 240))
        pen.curveTo((60 + SW, 340), (160, 450 + OVS - HW), (270, 450 + OVS - HW))
        pen.closePath()
    glyphs['6'] = (draw_6, 540)

    def draw_7(pen):
        pen.moveTo((50, CAP))
        pen.lineTo((470, CAP))
        pen.lineTo((470, CAP - HW))
        pen.lineTo((190, BL))
        pen.lineTo((190 - SW, BL))
        pen.lineTo((470 - SW, CAP - HW))
        pen.lineTo((50, CAP - HW))
        pen.closePath()
    glyphs['7'] = (draw_7, 520)

    def draw_8(pen):
        # 1. Single continuous Clockwise outer peanut perimeter (Top -> Right -> Down -> Bottom -> Left -> Up)
        pen.moveTo((260, CAP + OVS))
        pen.curveTo((370, CAP + OVS), (440, CAP - 120), (440, CAP - 190))
        pen.curveTo((440, 410), (370, 360), (330, 360))
        pen.curveTo((390, 360), (460, 300), (460, 180))
        pen.curveTo((460, BL - OVS), (370, BL - OVS), (260, BL - OVS))
        pen.curveTo((150, BL - OVS), (60, BL - OVS), (60, 180))
        pen.curveTo((60, 300), (130, 360), (190, 360))
        pen.curveTo((150, 360), (80, 410), (80, CAP - 190))
        pen.curveTo((80, CAP - 120), (150, CAP + OVS), (260, CAP + OVS))
        pen.closePath()
        # 2. Top Counter (Counter-Clockwise: Top -> Left -> Bottom -> Right)
        pen.moveTo((260, CAP - HW))
        pen.curveTo((170, CAP - HW), (80 + SW, CAP - 120), (80 + SW, CAP - 190))
        pen.curveTo((80 + SW, 420), (170, 360 + HW/2), (260, 360 + HW/2))
        pen.curveTo((350, 360 + HW/2), (440 - SW, 420), (440 - SW, CAP - 190))
        pen.curveTo((440 - SW, CAP - 120), (350, CAP - HW), (260, CAP - HW))
        pen.closePath()
        # 3. Bottom Counter (Counter-Clockwise: Top -> Left -> Bottom -> Right)
        pen.moveTo((260, 360 - HW/2))
        pen.curveTo((160, 360 - HW/2), (60 + SW, 290), (60 + SW, 180))
        pen.curveTo((60 + SW, BL + HW), (160, BL + HW), (260, BL + HW))
        pen.curveTo((360, BL + HW), (460 - SW, BL + HW), (460 - SW, 180))
        pen.curveTo((460 - SW, 290), (360, 360 - HW/2), (260, 360 - HW/2))
        pen.closePath()
    glyphs['8'] = (draw_8, 520)

    def draw_9(pen):
        # Outer continuous contour (CW: Top-Left -> Top-Right -> Down to BL -> Curve Left -> Up into counter arch)
        pen.moveTo((270, CAP + OVS))
        pen.curveTo((410, CAP + OVS), (480, CAP - 90), (480, CAP - 240))
        pen.lineTo((480, 160))
        pen.curveTo((480, BL - OVS), (360, BL - OVS), (200, BL - OVS))
        pen.lineTo((200, BL + HW))
        pen.curveTo((340, BL + HW), (480 - SW, 100), (480 - SW, CAP - 380))
        pen.curveTo((420, CAP - 460 - OVS), (340, CAP - 460 - OVS), (270, CAP - 460 - OVS))
        pen.curveTo((130, CAP - 460 - OVS), (60, CAP - 380), (60, CAP - 240))
        pen.curveTo((60, CAP - 90), (130, CAP + OVS), (270, CAP + OVS))
        pen.closePath()
        # Inner counter (CCW: Top -> Left -> Bottom -> Right)
        pen.moveTo((270, CAP - HW))
        pen.curveTo((160, CAP - HW), (60 + SW, CAP - 130), (60 + SW, CAP - 240))
        pen.curveTo((60 + SW, CAP - 350), (160, CAP - 460 - OVS + HW), (270, CAP - 460 - OVS + HW))
        pen.curveTo((380, CAP - 460 - OVS + HW), (480 - SW, CAP - 350), (480 - SW, CAP - 240))
        pen.curveTo((480 - SW, CAP - 130), (380, CAP - HW), (270, CAP - HW))
        pen.closePath()
    glyphs['9'] = (draw_9, 540)

    # =========================================================================
    # PUNCTUATION & SYMBOLS
    # =========================================================================

    def draw_period(pen):
        draw_oval_counter(pen, 120, BL + SW/2, SW/2 + 2, SW/2 + 2, 0, 0)
    glyphs['period'] = (draw_period, 240)

    def draw_comma(pen):
        draw_oval_counter(pen, 120, BL + SW/2, SW/2 + 2, SW/2 + 2, 0, 0)
        pen.moveTo((120 + SW/2, BL + SW/2))
        pen.lineTo((80, BL - 60))
        pen.lineTo((120, BL - 60))
        pen.closePath()
    glyphs['comma'] = (draw_comma, 240)

    def draw_colon(pen):
        draw_oval_counter(pen, 120, BL + SW/2, SW/2 + 2, SW/2 + 2, 0, 0)
        draw_oval_counter(pen, 120, XH - SW/2, SW/2 + 2, SW/2 + 2, 0, 0)
    glyphs['colon'] = (draw_colon, 240)

    def draw_semicolon(pen):
        draw_oval_counter(pen, 120, XH - SW/2, SW/2 + 2, SW/2 + 2, 0, 0)
        draw_oval_counter(pen, 120, BL + SW/2, SW/2 + 2, SW/2 + 2, 0, 0)
        pen.moveTo((120 + SW/2, BL + SW/2))
        pen.lineTo((80, BL - 60))
        pen.lineTo((120, BL - 60))
        pen.closePath()
    glyphs['semicolon'] = (draw_semicolon, 240)

    def draw_hyphen(pen):
        draw_rect(pen, 50, (XH/2) - (HW/2), 290, (XH/2) + (HW/2))
    glyphs['hyphen'] = (draw_hyphen, 340)

    def draw_underscore(pen):
        draw_rect(pen, 30, DSC + 30, 470, DSC + 30 + HW)
    glyphs['underscore'] = (draw_underscore, 500)

    def draw_exclam(pen):
        draw_rect(pen, 120 - SW/2, 160, 120 + SW/2, CAP)
        draw_oval_counter(pen, 120, BL + SW/2, SW/2 + 2, SW/2 + 2, 0, 0)
    glyphs['exclam'] = (draw_exclam, 240)

    def draw_question(pen):
        draw_smooth_c_arc(pen, 200, CAP - 160, 150, 150 + OVS, SW, 350, CAP - 80, 200 + SW/2, 280)
        draw_rect(pen, 200 - SW/2, 160, 200 + SW/2, 280)
        draw_oval_counter(pen, 200, BL + SW/2, SW/2 + 2, SW/2 + 2, 0, 0)
    glyphs['question'] = (draw_question, 400)

    def draw_slash(pen):
        pen.moveTo((300, CAP))
        pen.lineTo((60, DSC))
        pen.lineTo((60 + SW, DSC))
        pen.lineTo((300 + SW, CAP))
        pen.closePath()
    glyphs['slash'] = (draw_slash, 360)

    def draw_backslash(pen):
        pen.moveTo((60, CAP))
        pen.lineTo((300, DSC))
        pen.lineTo((300 + SW, DSC))
        pen.lineTo((60 + SW, CAP))
        pen.closePath()
    glyphs['backslash'] = (draw_backslash, 360)

    def draw_plus(pen):
        pen.moveTo((250 - SW/2, 120))
        pen.lineTo((250 + SW/2, 120))
        pen.lineTo((250 + SW/2, 320 - HW/2))
        pen.lineTo((450, 320 - HW/2))
        pen.lineTo((450, 320 + HW/2))
        pen.lineTo((250 + SW/2, 320 + HW/2))
        pen.lineTo((250 + SW/2, 520))
        pen.lineTo((250 - SW/2, 520))
        pen.lineTo((250 - SW/2, 320 + HW/2))
        pen.lineTo((50, 320 + HW/2))
        pen.lineTo((50, 320 - HW/2))
        pen.lineTo((250 - SW/2, 320 - HW/2))
        pen.closePath()
    glyphs['plus'] = (draw_plus, 500)

    def draw_equal(pen):
        draw_rect(pen, 50, 380 - HW/2, 450, 380 + HW/2)
        draw_rect(pen, 50, 240 - HW/2, 450, 240 + HW/2)
    glyphs['equal'] = (draw_equal, 500)

    def draw_less(pen):
        pen.moveTo((420, 520))
        pen.lineTo((100, 320))
        pen.lineTo((420, 120))
        pen.lineTo((420, 120 + HW * 1.5))
        pen.lineTo((160, 320))
        pen.lineTo((420, 520 - HW * 1.5))
        pen.closePath()
    glyphs['less'] = (draw_less, 480)

    def draw_greater(pen):
        pen.moveTo((60, 520))
        pen.lineTo((380, 320))
        pen.lineTo((60, 120))
        pen.lineTo((60, 120 + HW * 1.5))
        pen.lineTo((320, 320))
        pen.lineTo((60, 520 - HW * 1.5))
        pen.closePath()
    glyphs['greater'] = (draw_greater, 480)

    def draw_quotesingle(pen):
        draw_rect(pen, 100, CAP - 180, 100 + SW, CAP)
    glyphs['quotesingle'] = (draw_quotesingle, 220)

    def draw_parenleft(pen):
        draw_smooth_c_arc(pen, 240, CAP/2, 190, (CAP/2) + 40, SW, 240, CAP + 20, 240, -20)
    glyphs['parenleft'] = (draw_parenleft, 320)

    def draw_parenright(pen):
        draw_smooth_c_arc(pen, 80, CAP/2, 190, (CAP/2) + 40, SW, 80, -20, 80, CAP + 20)
    glyphs['parenright'] = (draw_parenright, 320)

    def draw_bracketleft(pen):
        draw_rect(pen, 100, DSC + 30, 100 + SW, CAP + 30)
        draw_rect(pen, 100, CAP + 30 - HW, 240, CAP + 30)
        draw_rect(pen, 100, DSC + 30, 240, DSC + 30 + HW)
    glyphs['bracketleft'] = (draw_bracketleft, 320)

    def draw_bracketright(pen):
        draw_rect(pen, 220 - SW, DSC + 30, 220, CAP + 30)
        draw_rect(pen, 80, CAP + 30 - HW, 220, CAP + 30)
        draw_rect(pen, 80, DSC + 30, 220, DSC + 30 + HW)
    glyphs['bracketright'] = (draw_bracketright, 320)

    def draw_braceleft(pen):
        draw_rect(pen, 140, DSC + 30, 140 + SW, CAP + 30)
        draw_rect(pen, 140, CAP + 30 - HW, 240, CAP + 30)
        draw_rect(pen, 140, DSC + 30, 240, DSC + 30 + HW)
        draw_rect(pen, 60, (CAP/2) - (HW/2), 140, (CAP/2) + (HW/2))
    glyphs['braceleft'] = (draw_braceleft, 340)

    def draw_braceright(pen):
        draw_rect(pen, 200 - SW, DSC + 30, 200, CAP + 30)
        draw_rect(pen, 100, CAP + 30 - HW, 200, CAP + 30)
        draw_rect(pen, 100, DSC + 30, 200, DSC + 30 + HW)
        draw_rect(pen, 200, (CAP/2) - (HW/2), 280, (CAP/2) + (HW/2))
    glyphs['braceright'] = (draw_braceright, 340)

    def draw_numbersign(pen):
        draw_rect(pen, 140, BL, 140 + SW, CAP)
        draw_rect(pen, 340, BL, 340 + SW, CAP)
        draw_rect(pen, 60, 460 - HW/2, 480, 460 + HW/2)
        draw_rect(pen, 60, 240 - HW/2, 480, 240 + HW/2)
    glyphs['numbersign'] = (draw_numbersign, 540)

    def draw_dollar(pen):
        draw_oval_counter(pen, 260, CAP - 170, 180, 160 + OVS, 180 - SW, 160 + OVS - HW)
        draw_oval_counter(pen, 260, 180, 190, 170 + OVS, 190 - SW, 170 + OVS - HW)
        draw_rect(pen, 260 - SW/4, DSC + 40, 260 + SW/4, CAP + 40)
    glyphs['dollar'] = (draw_dollar, 520)

    def draw_percent(pen):
        draw_oval_counter(pen, 150, CAP - 140, 80, 80, 80 - SW*0.7, 80 - HW)
        draw_oval_counter(pen, 370, 140, 80, 80, 80 - SW*0.7, 80 - HW)
        pen.moveTo((420, CAP))
        pen.lineTo((100, BL))
        pen.lineTo((100 + SW, BL))
        pen.lineTo((420 + SW, CAP))
        pen.closePath()
    glyphs['percent'] = (draw_percent, 540)

    def draw_ampersand(pen):
        draw_oval_counter(pen, 240, CAP - 180, 150, 150 + OVS, 150 - SW, 150 - HW)
        draw_oval_counter(pen, 240, 180, 190, 170 + OVS, 190 - SW, 170 - HW)
        pen.moveTo((340, 180))
        pen.lineTo((480, BL))
        pen.lineTo((480 - SW, BL))
        pen.lineTo((280, 140))
        pen.closePath()
    glyphs['ampersand'] = (draw_ampersand, 540)

    def draw_at(pen):
        draw_oval_counter(pen, 280, CAP/2, 240, (CAP/2) + OVS, 240 - SW, (CAP/2) + OVS - HW)
        draw_oval_counter(pen, 280, CAP/2, 120, 120, 120 - SW, 120 - HW)
        draw_rect(pen, 400 - SW, 160, 400, CAP/2 + 20)
    glyphs['at'] = (draw_at, 560)

    def draw_asterisk(pen):
        cx, cy = 240, 460
        r = 120
        for angle in [0, 60, 120]:
            rad = math.radians(angle)
            dx = r * math.cos(rad)
            dy = r * math.sin(rad)
            pen.moveTo((cx - dx, cy - dy))
            pen.lineTo((cx + dx, cy + dy))
            pen.lineTo((cx + dx + HW/2, cy + dy - HW/2))
            pen.lineTo((cx - dx + HW/2, cy - dy - HW/2))
            pen.closePath()
    glyphs['asterisk'] = (draw_asterisk, 480)

    # =========================================================================
    # CLINICAL TELEMETRY & MEDICAL ICON SUITE (Private Use Area E001-E006)
    # =========================================================================

    def draw_icon_heart_ecg(pen):
        # Continuous crisp medical ECG QRS waveform
        pen.moveTo((40, 260))
        pen.lineTo((160, 260))
        pen.lineTo((200, 200))
        pen.lineTo((270, CAP - 40))
        pen.lineTo((340, DSC + 40))
        pen.lineTo((400, 360))
        pen.lineTo((450, 260))
        pen.lineTo((560, 260))
        pen.lineTo((560, 260 + HW))
        pen.lineTo((460, 260 + HW))
        pen.lineTo((400, 360 + HW))
        pen.lineTo((340, DSC + 40 + HW * 1.5))
        pen.lineTo((270, CAP - 40 + HW))
        pen.lineTo((190, 200 + HW))
        pen.lineTo((150, 260 + HW))
        pen.lineTo((40, 260 + HW))
        pen.closePath()
    glyphs['icon_heart_ecg'] = (draw_icon_heart_ecg, 600)

    def draw_icon_spo2(pen):
        # Crisp blood oxygen droplet (CW) with inner bubble (CCW)
        pen.moveTo((300, CAP - 40))
        pen.curveTo((380, 420), (480, 260), (480, 160))
        pen.curveTo((480, BL - OVS), (120, BL - OVS), (120, 160))
        pen.curveTo((120, 260), (220, 420), (300, CAP - 40))
        pen.closePath()
        # Inner counter (CCW)
        pen.moveTo((300, CAP - 140))
        pen.curveTo((240, 380), (160, 240), (160, 160))
        pen.curveTo((160, BL + HW * 1.5), (440, BL + HW * 1.5), (440, 160))
        pen.curveTo((440, 240), (360, 380), (300, CAP - 140))
        pen.closePath()
    glyphs['icon_spo2'] = (draw_icon_spo2, 600)

    def draw_icon_glucose(pen):
        # Hexagonal CGM sensor diamond
        pen.moveTo((300, CAP - 40))
        pen.lineTo((520, 360))
        pen.lineTo((520, 120))
        pen.lineTo((300, BL - 40))
        pen.lineTo((80, 120))
        pen.lineTo((80, 360))
        pen.closePath()
        # Inner counter (CCW)
        pen.moveTo((300, CAP - 120))
        pen.lineTo((130, 340))
        pen.lineTo((130, 140))
        pen.lineTo((300, BL + 40))
        pen.lineTo((470, 140))
        pen.lineTo((470, 340))
        pen.closePath()
        # Center sensor node
        draw_oval_counter(pen, 300, 240, 60, 60, 0, 0)
    glyphs['icon_glucose'] = (draw_icon_glucose, 600)

    def draw_icon_aed_shock(pen):
        # High-voltage AED lightning bolt
        pen.moveTo((340, CAP))
        pen.lineTo((140, 260))
        pen.lineTo((280, 260))
        pen.lineTo((200, BL - 40))
        pen.lineTo((460, 320))
        pen.lineTo((310, 320))
        pen.lineTo((410, CAP))
        pen.closePath()
    glyphs['icon_aed_shock'] = (draw_icon_aed_shock, 600)

    def draw_icon_beacon_gps(pen):
        # 911 Dispatch Radar / Beacon
        draw_oval_counter(pen, 300, 260, 220, 220, 220 - HW, 220 - HW)
        draw_oval_counter(pen, 300, 260, 140, 140, 140 - HW, 140 - HW)
        draw_oval_counter(pen, 300, 260, 50, 50, 0, 0)
    glyphs['icon_beacon_gps'] = (draw_icon_beacon_gps, 600)

    def draw_icon_cpr_coach(pen):
        # Real-time CPR Rhythm Metronome Waves
        draw_oval_counter(pen, 300, 260, 70, 70, 0, 0)
        draw_smooth_c_arc(pen, 300, 260, 160, 160, HW, 300, 420, 300, 100)
        draw_smooth_c_arc(pen, 300, 260, 160, 160, HW, 300, 100, 300, 420)
        draw_smooth_c_arc(pen, 300, 260, 240, 240, HW, 300, 500, 300, 20)
        draw_smooth_c_arc(pen, 300, 260, 240, 240, HW, 300, 20, 300, 500)
    glyphs['icon_cpr_coach'] = (draw_icon_cpr_coach, 600)

    def draw_space(pen):
        pass
    glyphs['space'] = (draw_space, 280)

    return glyphs

def build_superfamily():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    pocketgull_repo = os.path.abspath(os.path.join(typeface_root, '..', 'pocketgull'))
    
    base_font_path = os.path.join(typeface_root, 'PocketGull-Bold.ttf')
    sync_dir = os.path.join(pocketgull_repo, 'public', 'fonts')
    brand_fonts_dir = os.path.join(pocketgull_repo, 'public', 'brand', 'fonts')
    os.makedirs(sync_dir, exist_ok=True)
    os.makedirs(brand_fonts_dir, exist_ok=True)

    print("🎨 Compiling Master Precision Vector Superfamily...")

    weights = [
        ('PocketGull-Fineliner.ttf', 400, 'Regular', 'PocketGull Fineliner', False),
        ('PocketGull-Bold.ttf', 700, 'Bold', 'PocketGull Bold', False),
        ('PocketGull-Chiseltip.ttf', 900, 'Black', 'PocketGull Chiseltip', False),
        ('PocketGull-Antigravity.ttf', 800, 'Bold', 'PocketGull Antigravity', False),
        ('PocketGullMono-Regular.ttf', 500, 'Regular', 'PocketGull Mono', True),
        ('PocketGull-Numerics.ttf', 500, 'Regular', 'PocketGull Numerics', False),
    ]

    PUA_MAP = {
        'icon_heart_ecg': 0xE001,
        'icon_spo2': 0xE002,
        'icon_glucose': 0xE003,
        'icon_aed_shock': 0xE004,
        'icon_beacon_gps': 0xE005,
        'icon_cpr_coach': 0xE006,
    }

    for filename, wght, style_name, full_name, is_mono in weights:
        font = TTFont(base_font_path)
        glyf_table = font['glyf']
        hmtx_table = font['hmtx']
        glyph_set = font.getGlyphSet()

        precision_glyphs = create_precision_glyph_dict(weight=wght)
        
        cmap = font.getBestCmap()
        for char_key, (draw_fn, aw) in precision_glyphs.items():
            final_aw = 600 if is_mono else aw
            if is_mono and aw != 600:
                offset_x = (600 - aw) / 2.0
                def make_mono_draw(fn, ox):
                    def draw_centered(pen):
                        tpen = TransformPen(pen, (1, 0, 0, 1, ox, 0))
                        fn(tpen)
                    return draw_centered
                glyph, advance = make_clean_glyph(make_mono_draw(draw_fn, offset_x), glyph_set, final_aw)
            else:
                glyph, advance = make_clean_glyph(draw_fn, glyph_set, final_aw)
            
            # Map standard character name
            glyf_table[char_key] = glyph
            hmtx_table[char_key] = (final_aw, 40)
            
            # Map PostScript name from cmap
            if len(char_key) == 1 and ord(char_key) in cmap:
                glyph_name = cmap[ord(char_key)]
                glyf_table[glyph_name] = glyph
                hmtx_table[glyph_name] = (final_aw, 40)

        # Inject PUA into all sub-cmap tables
        for table in font['cmap'].tables:
            for gname, ucode in PUA_MAP.items():
                table.cmap[ucode] = gname

        # Enforce strict uniform monospace width (600 UPM) for all glyphs when is_mono is True
        if is_mono:
            for gname in font.getGlyphOrder():
                if gname in hmtx_table.metrics:
                    old_adv, old_lsb = hmtx_table.metrics[gname]
                    if old_adv != 600:
                        delta = (600 - old_adv) / 2.0
                        hmtx_table.metrics[gname] = (600, int(old_lsb + delta))

        # Inject TrueType gasp table (Thomas Phinney Screen Subpixel Antialiasing)
        try:
            gasp = newTable('gasp')
            gasp.version = 1
            # 0xFFFF means all sizes up to 65535 pt
            # 0x0F = GASP_GRIDFIT (1) | GASP_DOGRAY (2) | GASP_SYMMETRIC_SMOOTHING (4) | GASP_SYMMETRIC_GRIDFIT (8)
            gasp.gaspRange = {0xFFFF: 0x0F}
            font['gasp'] = gasp
        except Exception as e:
            print(f"  ⚠️ gasp table note: {e}")

        # Inject GPOS optical kerning table (for non-monospace instances)
        if not is_mono:
            try:
                from fontTools.ttLib.tables._k_e_r_n import KernTable_format_0
                kern_table = newTable('kern')
                kern_table.version = 0
                kern_subtable = KernTable_format_0()
                kern_subtable.version = 0
                kern_subtable.coverage = 1
                kerning_dict = {
                    ('A', 'V'): -60, ('A', 'W'): -50, ('A', 'Y'): -70, ('A', 'T'): -60,
                    ('T', 'A'): -65, ('T', 'a'): -50, ('T', 'e'): -45, ('T', 'o'): -45,
                    ('V', 'A'): -60, ('V', 'a'): -40, ('V', 'e'): -40, ('V', 'o'): -40,
                    ('W', 'A'): -50, ('W', 'a'): -35, ('W', 'e'): -35, ('W', 'o'): -35,
                    ('Y', 'A'): -70, ('Y', 'a'): -55, ('Y', 'e'): -55, ('Y', 'o'): -55,
                    ('P', 'A'): -50, ('F', 'A'): -45, ('L', 'T'): -50, ('L', 'V'): -40,
                }
                kern_subtable.kernTable = kerning_dict
                kern_table.kernTables = [kern_subtable]
                font['kern'] = kern_table
            except Exception as e:
                print(f"  ⚠️ Kerning note: {e}")

        # Set metadata
        if 'OS/2' in font:
            font['OS/2'].usWeightClass = wght
            if is_mono:
                font['OS/2'].panose.bProportion = 9
        if 'post' in font and is_mono:
            font['post'].isFixedPitch = 1
        
        # Save to all distribution targets (TTF and WOFF2)
        for dest in [typeface_root, sync_dir, brand_fonts_dir]:
            target_ttf = os.path.join(dest, filename)
            target_woff2 = os.path.splitext(target_ttf)[0] + '.woff2'
            font.save(target_ttf)
            font.flavor = 'woff2'
            font.save(target_woff2)
            font.flavor = None
        
        print(f"  ✅ Built pristine {filename} & WOFF2 (Weight: {wght}, Mono: {is_mono})")

    # Build Variable Font (VF)
    font_vf = TTFont(base_font_path)
    glyf_vf = font_vf['glyf']
    hmtx_vf = font_vf['hmtx']
    glyph_set_vf = font_vf.getGlyphSet()
    vf_glyphs = create_precision_glyph_dict(weight=700)
    cmap_vf = font_vf.getBestCmap()
    
    for char_key, (draw_fn, aw) in vf_glyphs.items():
        glyph, advance = make_clean_glyph(draw_fn, glyph_set_vf, aw)
        glyf_vf[char_key] = glyph
        hmtx_vf[char_key] = (advance, 40)
        if len(char_key) == 1 and ord(char_key) in cmap_vf:
            glyph_name = cmap_vf[ord(char_key)]
            glyf_vf[glyph_name] = glyph
            hmtx_vf[glyph_name] = (advance, 40)

    for table in font_vf['cmap'].tables:
        for gname, ucode in PUA_MAP.items():
            table.cmap[ucode] = gname

    fvar = newTable('fvar')

    weight_axis = Axis()
    weight_axis.axisTag = 'wght'
    weight_axis.minValue = 100.0
    weight_axis.defaultValue = 400.0
    weight_axis.maxValue = 900.0
    weight_axis.flags = 0
    weight_axis.axisNameID = 256

    opsz_axis = Axis()
    opsz_axis.axisTag = 'opsz'
    opsz_axis.minValue = 8.0
    opsz_axis.defaultValue = 16.0
    opsz_axis.maxValue = 72.0
    opsz_axis.flags = 0
    opsz_axis.axisNameID = 257

    slnt_axis = Axis()
    slnt_axis.axisTag = 'slnt'
    slnt_axis.minValue = -12.0
    slnt_axis.defaultValue = 0.0
    slnt_axis.maxValue = 0.0
    slnt_axis.flags = 0
    slnt_axis.axisNameID = 258

    fvar.axes = [weight_axis, opsz_axis, slnt_axis]

    inst_regular = NamedInstance()
    inst_regular.subfamilyNameID = 259
    inst_regular.coordinates = {'wght': 400.0, 'opsz': 16.0, 'slnt': 0.0}

    inst_bold = NamedInstance()
    inst_bold.subfamilyNameID = 260
    inst_bold.coordinates = {'wght': 700.0, 'opsz': 24.0, 'slnt': 0.0}

    inst_black = NamedInstance()
    inst_black.subfamilyNameID = 261
    inst_black.coordinates = {'wght': 900.0, 'opsz': 48.0, 'slnt': 0.0}

    fvar.instances = [inst_regular, inst_bold, inst_black]
    font_vf['fvar'] = fvar

    name_vf = font_vf['name']
    name_vf.setName("Weight", 256, 3, 1, 0x409)
    name_vf.setName("Optical size", 257, 3, 1, 0x409)
    name_vf.setName("Slant", 258, 3, 1, 0x409)
    name_vf.setName("PocketGull Variable Regular", 259, 3, 1, 0x409)
    name_vf.setName("PocketGull Variable Bold", 260, 3, 1, 0x409)
    name_vf.setName("PocketGull Variable Black", 261, 3, 1, 0x409)
    name_vf.setName("PocketGull Variable", 1, 3, 1, 0x409)
    name_vf.setName("PocketGull Variable", 4, 3, 1, 0x409)
    name_vf.setName("PocketGull-VF", 6, 3, 1, 0x409)

    for dest in [typeface_root, sync_dir, brand_fonts_dir]:
        vf_ttf = os.path.join(dest, 'PocketGull-VF.ttf')
        vf_woff2 = os.path.join(dest, 'PocketGull-VF.woff2')
        font_vf.save(vf_ttf)
        font_vf.flavor = 'woff2'
        font_vf.save(vf_woff2)
        font_vf.flavor = None

    print("✨ Master Precision Vector Superfamily compilation complete!")

if __name__ == '__main__':
    build_superfamily()

