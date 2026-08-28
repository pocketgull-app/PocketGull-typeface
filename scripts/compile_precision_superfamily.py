#!/usr/bin/env python3
"""
PocketGull Master Precision Superfamily Compiler v4.0
=====================================================
Compiles the complete PocketGull Superfamily preserving the high-quality,
authentic master vectors while injecting:
1. Clinical Telemetry Icons (PUA U+E001 - U+E006)
2. Greek Pharmacology & Mathematical Constants (Delta, Sigma, Omega, alpha, beta, gamma, mu, pi)
3. Cyrillic Slavic Emergency Medicine Letterforms (D, ZH, I, L, P, F, TS, CH, SH, SHCH, YU, YA, B, G, soft sign)
4. Monospace Mathematical Invariants (600 UPM advance width for PocketGullMono)
5. Thomas Phinney gasp Anti-Aliasing Table (GASP_DOGRAY | GASP_SYMMETRIC_SMOOTHING)
6. WOFF2 Brotli compression with wOF2 magic bytes
"""

import os
import sys
import math
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

UPM = 1024
CAP = 720
XH = 480
BL = 0
DSC = -180
OVS = 14

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
    if inner_rx > 0 and inner_ry > 0:
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
    
    irx = max(10, rx - sw)
    iry = max(10, ry - sw)
    ikx = irx * k
    iky = iry * k

    pen.moveTo((top_x, top_y))
    pen.curveTo((cx + kx * 0.7, cy + ry), (cx, cy + ry), (cx - rx * 0.7, cy + ry * 0.7))
    pen.curveTo((cx - rx, cy + ky), (cx - rx, cy), (cx - rx, cy - ky))
    pen.curveTo((cx - rx * 0.7, cy - ry * 0.7), (cx, cy - ry), (cx + kx * 0.7, cy - ry))
    pen.lineTo((bot_x, bot_y))
    pen.curveTo((cx + ikx * 0.5, cy - iry), (cx, cy - iry), (cx - irx * 0.7, cy - iry * 0.7))
    pen.curveTo((cx - irx, cy - iky), (cx - irx, cy), (cx - irx, cy + iky))
    pen.curveTo((cx - irx * 0.7, cy + iry * 0.7), (cx, cy + iry), (cx + ikx * 0.5, cy + iry))
    pen.lineTo((top_x, top_y))
    pen.closePath()

def create_precision_extensions(weight=700):
    w_norm = (weight - 400) / 500.0 if weight >= 400 else 0.0
    SW = int(65 + w_norm * 85)   # Main stem width
    HW = int(45 + w_norm * 35)   # Crossbar / hairline width

    glyphs = {}

    # =========================================================================
    # GREEK SCRIPT & CLINICAL PHARMACOLOGY / MATHEMATICS
    # =========================================================================

    def draw_alpha(pen):
        draw_oval_counter(pen, 240, XH/2, 190, (XH/2) + OVS, 190 - SW, (XH/2) + OVS - HW)
        draw_rounded_rect(pen, 380, BL, 450, XH/2, r=16)
    glyphs['alpha'] = (draw_alpha, 490)
    glyphs['\u03B1'] = (draw_alpha, 490)

    def draw_beta(pen):
        draw_rounded_rect(pen, 60, DSC, 60 + SW, CAP, r=16)
        pen.moveTo((60 + SW, CAP - 40))
        pen.curveTo((240, CAP + OVS), (360, CAP - 80), (360, CAP/2 + 40))
        pen.curveTo((360, CAP/2 - 20), (280, CAP/2 - 20), (60 + SW, CAP/2 - 20))
        pen.closePath()
        pen.moveTo((60 + SW, CAP/2 - 20))
        pen.curveTo((260, CAP/2 - 20), (380, 120), (380, BL + 40))
        pen.curveTo((380, BL - OVS), (200, BL - OVS), (60 + SW, BL + 20))
        pen.closePath()
    glyphs['beta'] = (draw_beta, 490)
    glyphs['\u03B2'] = (draw_beta, 490)

    def draw_gamma(pen):
        draw_rounded_rect(pen, 50, XH/2, 50 + SW, XH, r=16)
        pen.moveTo((50, XH))
        pen.lineTo((230, DSC))
        pen.lineTo((410, XH))
        pen.lineTo((410 - SW, XH))
        pen.lineTo((230, DSC + HW))
        pen.lineTo((50 + SW, XH))
        pen.closePath()
    glyphs['gamma'] = (draw_gamma, 460)
    glyphs['\u03B3'] = (draw_gamma, 460)

    def draw_delta_cap(pen):
        r = 16
        pen.moveTo((270, CAP))
        pen.lineTo((500 - r, BL + r))
        pen.curveTo((500, BL), (500 - SW, BL), (500 - SW - r, BL))
        pen.lineTo((40 + SW + r, BL))
        pen.curveTo((40 + SW, BL), (40, BL), (40, BL + r))
        pen.lineTo((270 - SW/2, CAP))
        pen.closePath()
        pen.moveTo((270, CAP - HW * 2))
        pen.lineTo((120, BL + HW))
        pen.lineTo((420, BL + HW))
        pen.closePath()
    glyphs['Delta'] = (draw_delta_cap, 540)
    glyphs['\u0394'] = (draw_delta_cap, 540)

    def draw_mu(pen):
        r = 16
        draw_rounded_rect(pen, 60, DSC, 60 + SW, XH, r=r)
        draw_rounded_rect(pen, 420 - SW, BL, 420, XH, r=r)
        pen.moveTo((60 + SW, 140))
        pen.curveTo((60 + SW, BL + HW), (130, BL + HW), (220, BL + HW))
        pen.curveTo((310, BL + HW), (420 - SW, BL + HW + 40), (420 - SW, 160))
        pen.lineTo((420, 160))
        pen.curveTo((420, BL - OVS), (280, BL - OVS), (220, BL - OVS))
        pen.curveTo((100, BL - OVS), (60 + SW, 70), (60 + SW, 140))
        pen.closePath()
    glyphs['mu'] = (draw_mu, 480)
    glyphs['\u03BC'] = (draw_mu, 480)
    glyphs['\u00B5'] = (draw_mu, 480)

    def draw_omega_cap(pen):
        r = 16
        draw_smooth_c_arc(pen, 280, CAP/2 + 40, 220, (CAP/2) + OVS - 40, SW, 440, 140, 120, 140, r=r)
        draw_rounded_rect(pen, 40, BL, 160, BL + HW, r=r)
        draw_rounded_rect(pen, 400, BL, 520, BL + HW, r=r)
        draw_rounded_rect(pen, 120, BL, 120 + SW, 140, r=r)
        draw_rounded_rect(pen, 440 - SW, BL, 440, 140, r=r)
    glyphs['Omega'] = (draw_omega_cap, 560)
    glyphs['\u03A9'] = (draw_omega_cap, 560)

    def draw_pi(pen):
        r = 16
        draw_rounded_rect(pen, 40, XH - HW, 440, XH, r=r)
        draw_rounded_rect(pen, 110, BL, 110 + SW, XH, r=r)
        draw_rounded_rect(pen, 370 - SW, BL, 370, XH, r=r)
    glyphs['pi'] = (draw_pi, 480)
    glyphs['\u03C0'] = (draw_pi, 480)

    def draw_sigma_cap(pen):
        r = 16
        draw_rounded_rect(pen, 50, CAP - HW, 490, CAP, r=r)
        draw_rounded_rect(pen, 50, BL, 490, BL + HW, r=r)
        pen.moveTo((50, CAP - HW))
        pen.lineTo((280, CAP/2))
        pen.lineTo((50, BL + HW))
        pen.lineTo((50 + SW, BL + HW))
        pen.lineTo((280 + SW, CAP/2))
        pen.lineTo((50 + SW, CAP - HW))
        pen.closePath()
    glyphs['Sigma'] = (draw_sigma_cap, 540)
    glyphs['\u03A3'] = (draw_sigma_cap, 540)

    # =========================================================================
    # CYRILLIC SCRIPT (EMERGENCY MEDICINE & INTERNATIONAL TRIAGE)
    # =========================================================================

    def draw_cyrillic_D(pen):
        r = 16
        pen.moveTo((120, BL + HW))
        pen.lineTo((180, CAP - r))
        pen.curveTo((180, CAP), (180 + SW, CAP), (180 + SW, CAP - r))
        pen.lineTo((380 - SW, CAP - r))
        pen.curveTo((380 - SW, CAP), (380, CAP), (380, CAP - r))
        pen.lineTo((440, BL + HW))
        pen.closePath()
        draw_rounded_rect(pen, 60, BL, 500, BL + HW, r=r)
        draw_rounded_rect(pen, 60, -80, 60 + SW, BL + HW, r=r)
        draw_rounded_rect(pen, 500 - SW, -80, 500, BL + HW, r=r)
    glyphs['uni0414'] = (draw_cyrillic_D, 560)
    glyphs['uni0434'] = (draw_cyrillic_D, 560)
    glyphs['\u0414'] = (draw_cyrillic_D, 560)
    glyphs['\u0434'] = (draw_cyrillic_D, 560)

    def draw_cyrillic_ZH(pen):
        r = 16
        draw_rounded_rect(pen, 280 - SW/2, BL, 280 + SW/2, CAP, r=r)
        draw_smooth_c_arc(pen, 180, CAP/2, 140, CAP/2, SW, 260, CAP - 80, 260, 80, r=r)
        pen.moveTo((300, CAP - 80))
        pen.curveTo((420, CAP/2 + 100), (420, CAP/2 - 100), (300, 80))
        pen.lineTo((300 + SW, 80))
        pen.curveTo((420 + SW, CAP/2 - 80), (420 + SW, CAP/2 + 80), (300 + SW, CAP - 80))
        pen.closePath()
    glyphs['uni0416'] = (draw_cyrillic_ZH, 580)
    glyphs['uni0436'] = (draw_cyrillic_ZH, 580)
    glyphs['\u0416'] = (draw_cyrillic_ZH, 580)
    glyphs['\u0436'] = (draw_cyrillic_ZH, 580)

    def draw_cyrillic_I(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        draw_rounded_rect(pen, 520 - SW, BL, 520, CAP, r=r)
        pen.moveTo((60 + SW, BL + r))
        pen.lineTo((520 - SW, CAP - r))
        pen.curveTo((520 - SW, CAP), (520, CAP), (520, CAP - r))
        pen.lineTo((60 + SW, BL + HW))
        pen.closePath()
    glyphs['uni0418'] = (draw_cyrillic_I, 580)
    glyphs['uni0438'] = (draw_cyrillic_I, 580)
    glyphs['\u0418'] = (draw_cyrillic_I, 580)
    glyphs['\u0438'] = (draw_cyrillic_I, 580)

    def draw_cyrillic_L(pen):
        r = 16
        draw_rounded_rect(pen, 460 - SW, BL, 460, CAP, r=r)
        pen.moveTo((60, BL + r))
        pen.curveTo((60, BL), (60 + SW, BL), (60 + SW, BL + r))
        pen.lineTo((60 + SW, CAP - 120))
        pen.curveTo((60 + SW, CAP + OVS), (240, CAP + OVS), (460 - SW, CAP))
        pen.lineTo((460 - SW, CAP - HW))
        pen.curveTo((240, CAP - HW), (60 + SW, CAP - 160), (60 + SW, BL + r))
        pen.closePath()
    glyphs['uni041B'] = (draw_cyrillic_L, 520)
    glyphs['uni043B'] = (draw_cyrillic_L, 520)
    glyphs['\u041B'] = (draw_cyrillic_L, 520)
    glyphs['\u043B'] = (draw_cyrillic_L, 520)

    def draw_cyrillic_P(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        draw_rounded_rect(pen, 520 - SW, BL, 520, CAP, r=r)
        draw_rounded_rect(pen, 60, CAP - HW, 520, CAP, r=r)
    glyphs['uni041F'] = (draw_cyrillic_P, 580)
    glyphs['uni043F'] = (draw_cyrillic_P, 580)
    glyphs['\u041F'] = (draw_cyrillic_P, 580)
    glyphs['\u043F'] = (draw_cyrillic_P, 580)

    def draw_cyrillic_F(pen):
        r = 16
        draw_rounded_rect(pen, 280 - SW/2, BL - 60, 280 + SW/2, CAP + 60, r=r)
        draw_oval_counter(pen, 170, CAP/2, 120, 180, 120 - SW, 180 - HW)
        draw_oval_counter(pen, 390, CAP/2, 120, 180, 120 - SW, 180 - HW)
    glyphs['uni0424'] = (draw_cyrillic_F, 560)
    glyphs['uni0444'] = (draw_cyrillic_F, 560)
    glyphs['\u0424'] = (draw_cyrillic_F, 560)
    glyphs['\u0444'] = (draw_cyrillic_F, 560)

    def draw_cyrillic_TS(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        draw_rounded_rect(pen, 460 - SW, BL, 460, CAP, r=r)
        draw_rounded_rect(pen, 60, BL, 460, BL + HW, r=r)
        draw_rounded_rect(pen, 460 - SW, -80, 460 + SW/2, BL + HW, r=r)
    glyphs['uni0426'] = (draw_cyrillic_TS, 540)
    glyphs['uni0446'] = (draw_cyrillic_TS, 540)
    glyphs['\u0426'] = (draw_cyrillic_TS, 540)
    glyphs['\u0446'] = (draw_cyrillic_TS, 540)

    def draw_cyrillic_CH(pen):
        r = 16
        draw_rounded_rect(pen, 440 - SW, BL, 440, CAP, r=r)
        draw_rounded_rect(pen, 60, CAP/2, 60 + SW, CAP, r=r)
        draw_rounded_rect(pen, 60, CAP/2 - HW/2, 440, CAP/2 + HW/2, r=r)
    glyphs['uni0427'] = (draw_cyrillic_CH, 500)
    glyphs['uni0447'] = (draw_cyrillic_CH, 500)
    glyphs['\u0427'] = (draw_cyrillic_CH, 500)
    glyphs['\u0447'] = (draw_cyrillic_CH, 500)

    def draw_cyrillic_SH(pen):
        r = 16
        draw_rounded_rect(pen, 50, BL, 50 + SW, CAP, r=r)
        draw_rounded_rect(pen, 320 - SW/2, BL, 320 + SW/2, CAP, r=r)
        draw_rounded_rect(pen, 590 - SW, BL, 590, CAP, r=r)
        draw_rounded_rect(pen, 50, BL, 590, BL + HW, r=r)
    glyphs['uni0428'] = (draw_cyrillic_SH, 640)
    glyphs['uni0448'] = (draw_cyrillic_SH, 640)
    glyphs['\u0428'] = (draw_cyrillic_SH, 640)
    glyphs['\u0448'] = (draw_cyrillic_SH, 640)

    def draw_cyrillic_SHCH(pen):
        r = 16
        draw_rounded_rect(pen, 50, BL, 50 + SW, CAP, r=r)
        draw_rounded_rect(pen, 320 - SW/2, BL, 320 + SW/2, CAP, r=r)
        draw_rounded_rect(pen, 590 - SW, BL, 590, CAP, r=r)
        draw_rounded_rect(pen, 50, BL, 590, BL + HW, r=r)
        draw_rounded_rect(pen, 590 - SW, -80, 590 + SW/2, BL + HW, r=r)
    glyphs['uni0429'] = (draw_cyrillic_SHCH, 660)
    glyphs['uni0449'] = (draw_cyrillic_SHCH, 660)
    glyphs['\u0429'] = (draw_cyrillic_SHCH, 660)
    glyphs['\u0449'] = (draw_cyrillic_SHCH, 660)

    def draw_cyrillic_YU(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        draw_rounded_rect(pen, 60 + SW, (CAP/2) - (HW/2), 340, (CAP/2) + (HW/2), r=r)
        draw_oval_counter(pen, 430, CAP/2, 160, (CAP/2) + OVS, 160 - SW, (CAP/2) + OVS - HW)
    glyphs['uni042E'] = (draw_cyrillic_YU, 620)
    glyphs['uni044E'] = (draw_cyrillic_YU, 620)
    glyphs['\u042E'] = (draw_cyrillic_YU, 620)
    glyphs['\u044E'] = (draw_cyrillic_YU, 620)

    def draw_cyrillic_YA(pen):
        r = 16
        draw_rounded_rect(pen, 500 - SW, BL, 500, CAP, r=r)
        pen.moveTo((500 - SW, CAP))
        pen.lineTo((280, CAP))
        pen.curveTo((140, CAP), (60, CAP - 110), (60, CAP - 190))
        pen.curveTo((60, CAP - 270), (140, CAP - 360), (280, CAP - 360))
        pen.lineTo((500 - SW, CAP - 360))
        pen.closePath()
        pen.moveTo((500 - SW, CAP - HW))
        pen.lineTo((270, CAP - HW))
        pen.curveTo((190, CAP - HW), (140, CAP - 120), (140, CAP - 190))
        pen.curveTo((140, CAP - 270), (190, CAP - 360 + HW), (270, CAP - 360 + HW))
        pen.lineTo((500 - SW, CAP - 360 + HW))
        pen.closePath()
        draw_rounded_rect(pen, 80, BL, 300, CAP - 360, r=r)
    glyphs['uni042F'] = (draw_cyrillic_YA, 560)
    glyphs['uni044F'] = (draw_cyrillic_YA, 560)
    glyphs['\u042F'] = (draw_cyrillic_YA, 560)
    glyphs['\u044F'] = (draw_cyrillic_YA, 560)

    def draw_cyrillic_B(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        draw_rounded_rect(pen, 60, CAP - HW, 440, CAP, r=r)
        pen.moveTo((60 + SW, (CAP/2) + 20))
        pen.lineTo((280, (CAP/2) + 20))
        pen.curveTo((430, (CAP/2) + 20), (490, 100), (490, BL + 40))
        pen.curveTo((490, BL - OVS), (360, BL - OVS), (60 + SW, BL))
        pen.closePath()
        pen.moveTo((60 + SW, (CAP/2) - HW))
        pen.lineTo((270, (CAP/2) - HW))
        pen.curveTo((380, (CAP/2) - HW), (410, 120), (410, BL + HW))
        pen.curveTo((410, BL + HW), (340, BL + HW), (60 + SW, BL + HW))
        pen.closePath()
    glyphs['\u0411'] = (draw_cyrillic_B, 540)
    glyphs['\u0431'] = (draw_cyrillic_B, 540)

    def draw_cyrillic_G(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        draw_rounded_rect(pen, 60, CAP - HW, 420, CAP, r=r)
    glyphs['\u0413'] = (draw_cyrillic_G, 480)
    glyphs['\u0433'] = (draw_cyrillic_G, 480)

    def draw_cyrillic_soft_sign(pen):
        r = 16
        draw_rounded_rect(pen, 60, BL, 60 + SW, CAP, r=r)
        pen.moveTo((60 + SW, (CAP/2) + 20))
        pen.lineTo((280, (CAP/2) + 20))
        pen.curveTo((430, (CAP/2) + 20), (490, 100), (490, BL + 40))
        pen.curveTo((490, BL - OVS), (360, BL - OVS), (60 + SW, BL))
        pen.closePath()
        pen.moveTo((60 + SW, (CAP/2) - HW))
        pen.lineTo((270, (CAP/2) - HW))
        pen.curveTo((380, (CAP/2) - HW), (410, 120), (410, BL + HW))
        pen.curveTo((410, BL + HW), (340, BL + HW), (60 + SW, BL + HW))
        pen.closePath()
    glyphs['\u042C'] = (draw_cyrillic_soft_sign, 540)
    glyphs['\u044C'] = (draw_cyrillic_soft_sign, 540)

    # =========================================================================
    # CLINICAL & EMERGENCY TELEMETRY ICONS (PUA U+E001 - U+E006)
    # =========================================================================

    def draw_icon_heart_ecg(pen):
        pen.moveTo((300, 480))
        pen.curveTo((300, 560), (220, 620), (140, 620))
        pen.curveTo((60, 620), (20, 540), (20, 440))
        pen.curveTo((20, 320), (140, 180), (300, 40))
        pen.curveTo((460, 180), (580, 320), (580, 440))
        pen.curveTo((580, 540), (540, 620), (460, 620))
        pen.curveTo((380, 620), (300, 560), (300, 480))
        pen.closePath()
        pen.moveTo((40, 380))
        pen.lineTo((180, 380))
        pen.lineTo((240, 240))
        pen.lineTo((300, 540))
        pen.lineTo((360, 160))
        pen.lineTo((420, 420))
        pen.lineTo((460, 380))
        pen.lineTo((560, 380))
        pen.lineTo((560, 320))
        pen.lineTo((480, 320))
        pen.lineTo((420, 360))
        pen.lineTo((360, 100))
        pen.lineTo((300, 480))
        pen.lineTo((240, 180))
        pen.lineTo((180, 320))
        pen.lineTo((40, 320))
        pen.closePath()
    glyphs['icon_heart_ecg'] = (draw_icon_heart_ecg, 600)

    def draw_icon_spo2(pen):
        pen.moveTo((300, CAP - 40))
        pen.curveTo((380, 420), (480, 260), (480, 160))
        pen.curveTo((480, BL - OVS), (120, BL - OVS), (120, 160))
        pen.curveTo((120, 260), (220, 420), (300, CAP - 40))
        pen.closePath()
        pen.moveTo((300, CAP - 140))
        pen.curveTo((240, 380), (160, 240), (160, 160))
        pen.curveTo((160, BL + HW * 1.5), (440, BL + HW * 1.5), (440, 160))
        pen.curveTo((440, 240), (360, 380), (300, CAP - 140))
        pen.closePath()
    glyphs['icon_spo2'] = (draw_icon_spo2, 600)

    def draw_icon_glucose(pen):
        pen.moveTo((300, CAP - 40))
        pen.lineTo((520, 360))
        pen.lineTo((520, 120))
        pen.lineTo((300, BL - 40))
        pen.lineTo((80, 120))
        pen.lineTo((80, 360))
        pen.closePath()
        pen.moveTo((300, CAP - 120))
        pen.lineTo((130, 340))
        pen.lineTo((130, 140))
        pen.lineTo((300, BL + 40))
        pen.lineTo((470, 140))
        pen.lineTo((470, 340))
        pen.closePath()
        draw_oval_counter(pen, 300, 240, 60, 60, 0, 0)
    glyphs['icon_glucose'] = (draw_icon_glucose, 600)

    def draw_icon_aed_shock(pen):
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
        draw_oval_counter(pen, 300, 260, 220, 220, 220 - HW, 220 - HW)
        draw_oval_counter(pen, 300, 260, 140, 140, 140 - HW, 140 - HW)
        draw_oval_counter(pen, 300, 260, 50, 50, 0, 0)
    glyphs['icon_beacon_gps'] = (draw_icon_beacon_gps, 600)

    def draw_icon_cpr_coach(pen):
        draw_oval_counter(pen, 300, 260, 70, 70, 0, 0)
        draw_smooth_c_arc(pen, 300, 260, 160, 160, HW, 300, 420, 300, 100)
        draw_smooth_c_arc(pen, 300, 260, 160, 160, HW, 300, 100, 300, 420)
        draw_smooth_c_arc(pen, 300, 260, 240, 240, HW, 300, 500, 300, 20)
        draw_smooth_c_arc(pen, 300, 260, 240, 240, HW, 300, 20, 300, 500)
    glyphs['icon_cpr_coach'] = (draw_icon_cpr_coach, 600)

    return glyphs

def compile_precision_superfamily():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    base_font_path = os.path.join(typeface_root, 'PocketGull-VF.ttf')

    if not os.path.exists(base_font_path):
        print(f"Error: Base master font not found at {base_font_path}")
        sys.exit(1)

    print("🚀 Compiling Precision Superfamily from master vectors...")

    weights = [
        ('PocketGull-Fineliner.ttf', 300, 'Fineliner', 'PocketGull Fineliner', False),
        ('PocketGull-Bold.ttf', 700, 'Bold', 'PocketGull Bold', False),
        ('PocketGull-Chiseltip.ttf', 800, 'Chiseltip', 'PocketGull Chiseltip', False),
        ('PocketGull-Antigravity.ttf', 400, 'Antigravity', 'PocketGull Antigravity', False),
        ('PocketGullMono-Regular.ttf', 500, 'Regular', 'PocketGullMono Regular', True),
        ('PocketGull-Numerics.ttf', 600, 'Numerics', 'PocketGull Numerics', False),
    ]

    PUA_MAP = {
        'icon_heart_ecg': 0xE001,
        'icon_spo2': 0xE002,
        'icon_glucose': 0xE003,
        'icon_aed_shock': 0xE004,
        'icon_beacon_gps': 0xE005,
        'icon_cpr_coach': 0xE006,
    }

    CYRILLIC_HOMOGLYPHS = {
        0x0410: 'A',  # А
        0x0412: 'B',  # В
        0x0415: 'E',  # Е
        0x041A: 'K',  # К
        0x041C: 'M',  # М
        0x041D: 'H',  # Н
        0x041E: 'O',  # О
        0x0420: 'P',  # Р
        0x0421: 'C',  # С
        0x0422: 'T',  # Т
        0x0423: 'Y',  # У
        0x0425: 'X',  # Х
        0x0430: 'a',  # а
        0x0435: 'e',  # е
        0x043E: 'o',  # о
        0x0440: 'p',  # р
        0x0441: 'c',  # с
        0x0443: 'y',  # у
        0x0445: 'x',  # х
    }

    for filename, wght, style_name, full_name, is_mono in weights:
        font = TTFont(base_font_path)
        glyf_table = font['glyf']
        hmtx_table = font['hmtx']
        glyph_set = font.getGlyphSet()

        precision_extensions = create_precision_extensions(weight=wght)
        cmap = font.getBestCmap()

        for char_key, (draw_fn, aw) in precision_extensions.items():
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
            
            glyph_name = char_key
            if len(char_key) == 1:
                cp = ord(char_key)
                glyph_name = cmap.get(cp) or f"uni{cp:04X}"
            
            if glyph_name not in font.getGlyphOrder():
                font.setGlyphOrder(font.getGlyphOrder() + [glyph_name])

            glyf_table[glyph_name] = glyph
            hmtx_table.metrics[glyph_name] = (final_aw, 40)
            
            if len(char_key) == 1:
                cp = ord(char_key)
                for table in font['cmap'].tables:
                    table.cmap[cp] = glyph_name
            elif char_key.startswith('uni') and len(char_key) == 7:
                try:
                    cp = int(char_key[3:], 16)
                    for table in font['cmap'].tables:
                        table.cmap[cp] = char_key
                except ValueError:
                    pass

        # Map Cyrillic shared homoglyphs
        for cp, latin_char in CYRILLIC_HOMOGLYPHS.items():
            latin_cp = ord(latin_char)
            latin_gname = cmap.get(latin_cp) or latin_char
            for table in font['cmap'].tables:
                table.cmap[cp] = latin_gname

        # Inject PUA into all sub-cmap tables
        for table in font['cmap'].tables:
            for gname, ucode in PUA_MAP.items():
                if gname not in font.getGlyphOrder():
                    font.setGlyphOrder(font.getGlyphOrder() + [gname])
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
            gasp.gaspRange = {0xFFFF: 0x0F}
            font['gasp'] = gasp
        except Exception as e:
            print(f"  ⚠️ gasp table note: {e}")

        # Update metadata
        font['OS/2'].usWeightClass = wght
        font['head'].unitsPerEm = 1024
        font['hhea'].ascent = 1136
        font['hhea'].descent = -325
        font['OS/2'].sTypoAscender = 1136
        font['OS/2'].sTypoDescender = -325

        if is_mono:
            font['post'].isFixedPitch = 1
            font['OS/2'].panose.bProportion = 9
        else:
            font['post'].isFixedPitch = 0
            font['OS/2'].panose.bProportion = 0

        # Save TTF
        out_ttf_path = os.path.join(typeface_root, filename)
        font.save(out_ttf_path)
        print(f"  ✅ Saved TTF ({style_name}): {filename}")

        # Save WOFF2
        try:
            font.flavor = 'woff2'
            out_woff2_path = os.path.join(typeface_root, filename.replace('.ttf', '.woff2'))
            font.save(out_woff2_path)
            print(f"  📦 Saved WOFF2: {filename.replace('.ttf', '.woff2')}")
        except Exception as e:
            print(f"  ⚠️ WOFF2 note: {e}")

    print("🎉 Precision Superfamily compilation complete!")

if __name__ == '__main__':
    compile_precision_superfamily()
