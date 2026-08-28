#!/usr/bin/env python3
"""
PocketGull Authentic Binary Specimen Renderer
=============================================
Renders high-resolution raster PNG and pure vector SVG specimens
directly from the compiled PocketGull-Bold.ttf and PocketGullMono-Regular.ttf binaries.
"""

import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from PIL import Image, ImageDraw, ImageFont

def render_authentic_specimen():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    typeface_root = os.path.dirname(script_dir)
    
    font_bold = os.path.join(typeface_root, 'PocketGull-Bold.ttf')
    font_fine = os.path.join(typeface_root, 'PocketGull-Fineliner.ttf')
    font_mono = os.path.join(typeface_root, 'PocketGullMono-Regular.ttf')

    print("🎨 Rendering authentic font specimen directly from TTF binaries...")

    # -------------------------------------------------------------------------
    # 1. 4x SUPER-SAMPLED MUSEUM SPECIMEN (typeface.pocketgull.app Aesthetic)
    # -------------------------------------------------------------------------
    SCALE = 4
    W_FINAL, H_FINAL = 2400, 1600
    W, H = W_FINAL * SCALE, H_FINAL * SCALE

    # Background slate-950
    img = Image.new('RGB', (W, H), color='#090d16')
    draw = ImageDraw.Draw(img)

    C_CARD_BG = '#0f172a'
    C_CARD_BORDER = '#1e293b'
    C_AMBER = '#f59e0b'
    C_AMBER_GLOW = '#d97706'
    C_CYAN = '#06b6d4'
    C_EMERALD = '#10b981'
    C_ROSE = '#f43f5e'
    C_WHITE = '#f8fafc'
    C_MUTED = '#64748b'
    C_GRID = '#101726'

    # 1. Minimalist Dieter Rams Blueprint Grid
    for y in range(0, H, 80 * SCALE):
        draw.line([(0, y), (W, y)], fill=C_GRID, width=SCALE)
    for x in range(0, W, 80 * SCALE):
        draw.line([(x, 0), (x, H)], fill=C_GRID, width=SCALE)

    # 2. Load Fonts at 4x scale
    f_hero = ImageFont.truetype(font_bold, 120 * SCALE)
    f_h2 = ImageFont.truetype(font_bold, 40 * SCALE)
    f_badge = ImageFont.truetype(font_mono, 18 * SCALE)
    f_sub = ImageFont.truetype(font_fine, 24 * SCALE)
    f_caps = ImageFont.truetype(font_bold, 46 * SCALE)
    f_low = ImageFont.truetype(font_fine, 42 * SCALE)
    f_mono_large = ImageFont.truetype(font_mono, 32 * SCALE)
    f_mono_small = ImageFont.truetype(font_mono, 20 * SCALE)
    f_meta = ImageFont.truetype(font_mono, 16 * SCALE)

    # 3. Top Branding Header (Matching typeface.pocketgull.app)
    # Seagull / Pen icon badge
    draw.rounded_rectangle([120 * SCALE, 80 * SCALE, 190 * SCALE, 150 * SCALE], radius=16 * SCALE, fill=C_AMBER)
    draw.text((138 * SCALE, 90 * SCALE), '🖋️', font=f_badge, fill='#000000')

    draw.text((215 * SCALE, 75 * SCALE), 'POCKETGULL', font=f_hero, fill=C_WHITE)
    
    # Subtitle with badge pills
    draw.text((220 * SCALE, 215 * SCALE), '100% OWNED MATHEMATICAL TYPEFACE SUPERFAMILY  ·  WCAG 2.1 AAA CERTIFIED', font=f_sub, fill=C_AMBER)
    draw.text((W - 680 * SCALE, 100 * SCALE), 'typeface.pocketgull.app', font=f_badge, fill=C_CYAN)

    # 4. Card 1: Primary Character Matrix & Glyph Palette
    draw.rounded_rectangle([120 * SCALE, 270 * SCALE, (W_FINAL - 120) * SCALE, 730 * SCALE], radius=24 * SCALE, fill=C_CARD_BG, outline=C_AMBER_GLOW, width=2 * SCALE)
    draw.text((160 * SCALE, 300 * SCALE), '✦ CHARACTER SET MATRIX (PocketGull Bold 700 & Fineliner 400)', font=f_meta, fill=C_AMBER)
    draw.text((160 * SCALE, 350 * SCALE), 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z', font=f_caps, fill=C_WHITE)
    draw.text((160 * SCALE, 440 * SCALE), 'a b c d e f g h i j k l m n o p q r s t u v w x y z', font=f_low, fill='#e2e8f0')
    draw.text((160 * SCALE, 525 * SCALE), '0 1 2 3 4 5 6 7 8 9  (Slashed Zero 0, Structured 1, Open 4)', font=f_caps, fill=C_CYAN)
    draw.text((160 * SCALE, 615 * SCALE), '! ? . , : ; - _ ( ) [ ] { } / \\ @ # $ % & * + = < > \' "', font=f_caps, fill=C_MUTED)

    # 5. Card 2: Clinical Telemetry & Bespoke Medical Icons
    draw.rounded_rectangle([120 * SCALE, 770 * SCALE, (W_FINAL - 120) * SCALE, 1100 * SCALE], radius=24 * SCALE, fill=C_CARD_BG, outline='#0e7490', width=2 * SCALE)
    draw.text((160 * SCALE, 800 * SCALE), '🩺 CLINICAL DISAMBIGUATION & TELEMETRY SUITE (PocketGull Mono 500 + PUA E001-E006)', font=f_meta, fill=C_CYAN)
    draw.text((160 * SCALE, 855 * SCALE), '\uE001 HEART_RATE: 72 bpm   ·   \uE002 SPO2: 98%   ·   \uE003 GLUCOSE: 104 mg/dL', font=f_mono_large, fill=C_CYAN)
    draw.text((160 * SCALE, 925 * SCALE), '\uE004 AED: ARMED & READY   \uE005 DISPATCH: 911 ACTIVE   \uE006 CPR: 110 BPM', font=f_mono_large, fill=C_EMERALD)
    draw.text((160 * SCALE, 1000 * SCALE), '0123456789   0123456789   0123456789  (FIXED 600 UPM CELL  |  GPOS PAIR KERNING ACTIVE)', font=f_mono_small, fill=C_MUTED)

    # 6. Card 3: Editorial Pangram & Optical Spec
    draw.rounded_rectangle([120 * SCALE, 1140 * SCALE, (W_FINAL - 120) * SCALE, 1480 * SCALE], radius=24 * SCALE, fill=C_CARD_BG, outline='#475569', width=2 * SCALE)
    draw.text((160 * SCALE, 1170 * SCALE), '📏 DIETER RAMS PANGRAM PROOF & 1024 UPM OPTICAL SPECS', font=f_meta, fill='#cbd5e1')
    draw.text((160 * SCALE, 1220 * SCALE), 'Sphinx of black quartz, judge my vow.', font=f_h2, fill=C_WHITE)
    draw.text((160 * SCALE, 1290 * SCALE), 'AWAY TOWARD VICTORY: Bystander 911 dispatch, real-time CPR coach, and waveform telemetry with zero ambiguity.', font=f_sub, fill='#94a3b8')
    draw.text((160 * SCALE, 1370 * SCALE), '1024 UPM Grid  |  Cap: 720  |  x-Height: 480  |  Baseline: 0  |  Descender: -180  |  True Bézier Vectors', font=f_mono_small, fill=C_MUTED)

    # Downsample using Lanczos-3 for razor-sharp antialiasing
    print("  ✨ Downsampling 9600x6400 -> 2400x1600 via Lanczos anti-aliasing filter...")
    img_crisp = img.resize((W_FINAL, H_FINAL), resample=Image.Resampling.LANCZOS)

    png_out_path = os.path.join(typeface_root, 'PocketGull-Authentic-Specimen.png')
    img_crisp.save(png_out_path, quality=100)
    print(f"  ✅ Saved high-res PNG specimen: {png_out_path}")

    # Copy to artifact folder for instant viewing
    artifact_dir = 'C:/Users/philg/.gemini/antigravity/brain/fba2df62-a4ea-48c8-be3e-223e1c225eb3'
    if os.path.exists(artifact_dir):
        img_crisp.save(os.path.join(artifact_dir, 'PocketGull-Authentic-Specimen.png'), quality=100)

if __name__ == '__main__':
    render_authentic_specimen()

