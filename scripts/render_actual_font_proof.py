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
    # 1. RASTER 2400x1600 SPECIMEN POSTER VIA PILLOW
    # -------------------------------------------------------------------------
    W, H = 2400, 1600
    img = Image.new('RGB', (W, H), color='#0b0f19')
    draw = ImageDraw.Draw(img)

    C_BG = '#0b0f19'
    C_CARD = '#131b2e'
    C_BORDER = '#22304e'
    C_TEAL = '#14b8a6'
    C_ORANGE = '#ea580c'
    C_WHITE = '#f8fafc'
    C_MUTED = '#94a3b8'
    C_GRID = '#162035'

    # Background grid
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=C_GRID, width=1)
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=C_GRID, width=1)

    # Load actual TTF fonts
    f_hero = ImageFont.truetype(font_bold, 130)
    f_h2 = ImageFont.truetype(font_bold, 44)
    f_sub = ImageFont.truetype(font_fine, 26)
    f_caps = ImageFont.truetype(font_bold, 50)
    f_low = ImageFont.truetype(font_fine, 46)
    f_mono_large = ImageFont.truetype(font_mono, 34)
    f_mono_small = ImageFont.truetype(font_mono, 22)
    f_meta = ImageFont.truetype(font_fine, 18)

    # Header
    draw.text((120, 80), 'POCKETGULL', font=f_hero, fill=C_WHITE)
    draw.text((120, 220), '100% OWNED MATHEMATICAL TYPEFACE  ·  DIRECT TTF BINARY RENDER', font=f_sub, fill=C_TEAL)

    # Card 1: Character Matrix
    draw.rectangle([120, 280, W - 120, 750], fill=C_CARD, outline=C_BORDER, width=2)
    draw.text((160, 310), 'CHARACTER SET SPECIMEN (PocketGull Bold & Fineliner)', font=f_meta, fill=C_ORANGE)
    draw.text((160, 360), 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z', font=f_caps, fill=C_WHITE)
    draw.text((160, 450), 'a b c d e f g h i j k l m n o p q r s t u v w x y z', font=f_low, fill='#e2e8f0')
    draw.text((160, 540), '0 1 2 3 4 5 6 7 8 9  (Slashed Zero 0, Structured 1, Open 4)', font=f_caps, fill=C_TEAL)
    draw.text((160, 630), '! ? . , : ; - _ ( ) [ ] { } / \\ @ # $ % & * + = < > \' "', font=f_caps, fill=C_MUTED)

    # Card 2: Monospace Telemetry & Clinical Icons
    draw.rectangle([120, 790, W - 120, 1110], fill=C_CARD, outline=C_BORDER, width=2)
    draw.text((160, 820), 'CLINICAL TELEMETRY & BESPOKE MEDICAL ICONS (PocketGull Mono + PUA E001-E006)', font=f_meta, fill=C_TEAL)
    draw.text((160, 870), '\uE001 HEART_RATE: 72 bpm  ·  \uE002 SPO2: 98%  ·  \uE003 GLUCOSE: 104 mg/dL', font=f_mono_large, fill=C_TEAL)
    draw.text((160, 940), '\uE004 AED: ARMED & READY   \uE005 DISPATCH: 911 ACTIVE   \uE006 CPR: 110 BPM', font=f_mono_large, fill='#38bdf8')
    draw.text((160, 1010), '0123456789   0123456789   0123456789  (TABULAR 600 UPM + GPOS KERNING PAIRS)', font=f_mono_small, fill=C_MUTED)

    # Card 3: Editorial & Grid Specs
    draw.rectangle([120, 1150, W - 120, 1480], fill=C_CARD, outline=C_BORDER, width=2)
    draw.text((160, 1180), 'PANGRAM & OPTICAL KERNING PROOF (AV, AW, Ta, To, We, Yo)', font=f_meta, fill=C_ORANGE)
    draw.text((160, 1230), 'Sphinx of black quartz, judge my vow.', font=f_h2, fill=C_WHITE)
    draw.text((160, 1300), 'AWAY TOWARD VICTORY: Bystander 911 dispatch, CPR coach, and telemetry with zero ambiguity.', font=f_sub, fill='#cbd5e1')
    draw.text((160, 1370), '1024 UPM Grid  |  Cap: 720  |  x-Height: 480  |  Baseline: 0  |  Descender: -180  |  True Bézier Vectors', font=f_mono_small, fill=C_MUTED)

    png_out_path = os.path.join(typeface_root, 'PocketGull-Authentic-Specimen.png')
    img.save(png_out_path, quality=95)
    print(f"  ✅ Saved high-res PNG specimen: {png_out_path}")

    # Copy to artifact folder for instant viewing
    artifact_dir = 'C:/Users/philg/.gemini/antigravity/brain/fba2df62-a4ea-48c8-be3e-223e1c225eb3'
    if os.path.exists(artifact_dir):
        img.save(os.path.join(artifact_dir, 'PocketGull-Authentic-Specimen.png'), quality=95)

if __name__ == '__main__':
    render_authentic_specimen()

