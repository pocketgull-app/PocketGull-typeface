#!/usr/bin/env python3
"""
PocketGull: Terminal Healing Cinema (24-bit TrueColor ANSI Engine)
Paced to 0.1 Hz Resonant Respiration (6 Breaths / Minute)
Zero GPU overhead - 100% CPU safe terminal telemetry.
"""

import sys
import time
import math
import os

# Ensure UTF-8 output across Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Enable VT100 processing on Windows
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def oklch_to_rgb(hue_deg, lightness=0.75, chroma=0.18):
    """
    Fast analytical approximation of OKLCH hue arc to 24-bit RGB.
    Produces rich, luminous cinematic transitions without muddy dead zones.
    """
    rad = math.radians(hue_deg)
    # Approximate chromatic coordinates in perceptual lab
    a = chroma * math.cos(rad)
    b = chroma * math.sin(rad)
    
    # Linear sRGB transformation matrix approximation
    l_ = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_ = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_ = lightness - 0.0894841775 * a - 1.2914855480 * b

    l = l_ ** 3
    m = m_ ** 3
    s = s_ ** 3

    r = +4.0767434770 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    def clamp(v):
        v = max(0.0, min(1.0, v))
        # Gamma correction
        return int(255 * (12.92 * v if v <= 0.0031308 else 1.055 * (v ** (1.0 / 2.4)) - 0.055))

    return clamp(r), clamp(g), clamp(b)

def colorize(text, r, g, b):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def render_frame(t, width=76):
    period = 10.0 # 0.1 Hz breathing
    phase = (t % period) / period
    breath = 0.5 * (1.0 - math.cos(2.0 * math.pi * phase))
    
    # Weight simulation (400 -> 850)
    sim_weight = int(400 + breath * 450)
    hue = (t * 18.0) % 360.0
    
    # Determine phase label
    if phase < 0.45:
        phase_label = "INHALING · SWELLING OPTICAL MASS"
        indicator = "▲" * int(1 + breath * 12)
    elif phase < 0.55:
        phase_label = "LUNG STABILIZATION · 5:1 RATIO"
        indicator = "◆" * 13
    elif phase < 0.95:
        phase_label = "EXHALING · RELEASING TENSION"
        indicator = "▼" * int(1 + (1.0 - breath) * 12)
    else:
        phase_label = "REST INTERVAL · RECOVERY"
        indicator = "━" * 4

    r_base, g_base, b_base = oklch_to_rgb(hue, lightness=0.82, chroma=0.20)
    r_dim, g_dim, b_dim = oklch_to_rgb(hue + 30, lightness=0.45, chroma=0.10)

    # Telemetry Waveform (ECG + Breath Modulation)
    ecg_chars = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    wave_line = ""
    for col in range(54):
        w_phase = (col / 54.0 * 2.0 * math.pi) + (t * 2.5)
        # Add ECG QRS spike simulation
        spike = math.exp(-((col % 18 - 9) ** 2) / 2.0) if (col % 18 == 9) else 0.0
        val = 0.5 + 0.35 * math.sin(w_phase) + 0.4 * spike
        val = max(0.0, min(0.99, val))
        idx = int(val * len(ecg_chars))
        char_r, char_g, char_b = oklch_to_rgb((hue + col * 4) % 360, lightness=0.75, chroma=0.18)
        wave_line += colorize(ecg_chars[idx], char_r, char_g, char_b)

    lines = []
    lines.append(colorize("┌" + "─" * (width - 2) + "┐", r_dim, g_dim, b_dim))
    
    # Title Bar
    title = f" ⚕ POCKETGULL HEALING CINEMA · 0.1 Hz RESONANCE "
    lines.append(colorize("│", r_dim, g_dim, b_dim) + colorize(title.center(width - 2), r_base, g_base, b_base) + colorize("│", r_dim, g_dim, b_dim))
    lines.append(colorize("├" + "─" * (width - 2) + "┤", r_dim, g_dim, b_dim))
    
    # Core Typographic Film
    lines.append(colorize("│", r_dim, g_dim, b_dim) + " " * (width - 2) + colorize("│", r_dim, g_dim, b_dim))
    
    text_act = f"[ ACT {int((t // 15) % 4) + 1} ]  TACTILE HUMANIST WARMTH"
    lines.append(colorize("│", r_dim, g_dim, b_dim) + colorize(text_act.center(width - 2), 148, 163, 184) + colorize("│", r_dim, g_dim, b_dim))
    
    hero_msg = "INHALE STILLNESS. DISAMBIGUATE CHAOS."
    lines.append(colorize("│", r_dim, g_dim, b_dim) + colorize(hero_msg.center(width - 2), r_base, g_base, b_base) + colorize("│", r_dim, g_dim, b_dim))
    
    sub_msg = f"500 mg · IL-6 Biomarker · cv08: [0] · ss02: [I] · cv05: [l]"
    lines.append(colorize("│", r_dim, g_dim, b_dim) + colorize(sub_msg.center(width - 2), 203, 213, 225) + colorize("│", r_dim, g_dim, b_dim))
    
    lines.append(colorize("│", r_dim, g_dim, b_dim) + " " * (width - 2) + colorize("│", r_dim, g_dim, b_dim))
    
    # Dynamic Respiration Pacer Bar
    pacer_line = f"{indicator:<14}  {phase_label}  {indicator:>14}"
    lines.append(colorize("│", r_dim, g_dim, b_dim) + colorize(pacer_line.center(width - 2), r_base, g_base, b_base) + colorize("│", r_dim, g_dim, b_dim))
    
    lines.append(colorize("│", r_dim, g_dim, b_dim) + " " * (width - 2) + colorize("│", r_dim, g_dim, b_dim))
    
    # Waveform Canvas
    wave_block = f"   ECG/RESP: [{wave_line}]   "
    lines.append(colorize("│", r_dim, g_dim, b_dim) + wave_block.center(width + 42) + colorize("│", r_dim, g_dim, b_dim))
    
    lines.append(colorize("├" + "─" * (width - 2) + "┤", r_dim, g_dim, b_dim))
    
    # Telemetry Footer
    footer = f" wght: {sim_weight} UPM  │  OKLCH Hue: {hue:5.1f}°  │  Pitch: 600 UPM Fixed  │  OTS: 100% "
    lines.append(colorize("│", r_dim, g_dim, b_dim) + colorize(footer.center(width - 2), 56, 189, 248) + colorize("│", r_dim, g_dim, b_dim))
    lines.append(colorize("└" + "─" * (width - 2) + "┘", r_dim, g_dim, b_dim))
    
    return "\n".join(lines)

def main():
    print("\033[?25l") # Hide cursor
    try:
        # Clear screen once
        os.system('cls' if os.name == 'nt' else 'clear')
        start = time.time()
        # Run demonstration loop for 10 seconds (one complete 0.1 Hz respiratory cycle)
        # or indefinitely if run in an interactive session
        target_frames = 120 # ~10 seconds at 12 fps
        for frame in range(target_frames):
            now = time.time() - start
            buf = render_frame(now)
            # Home cursor without flicker
            sys.stdout.write("\033[H" + buf)
            sys.stdout.flush()
            time.sleep(0.08) # ~12.5 fps smooth terminal pacing
    except KeyboardInterrupt:
        pass
    finally:
        print("\033[?25h") # Restore cursor
        print("\n\n[POCKETGULL] Healing Cinema terminal sequence complete.\n")

if __name__ == '__main__':
    main()
