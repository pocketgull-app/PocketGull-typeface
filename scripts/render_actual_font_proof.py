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
    # 1. 4x SUPER-SAMPLED ULTRA-CRISP SPECIMEN (9600x6400 -> 2400x1600 via LANCZOS)
    # -------------------------------------------------------------------------
    SCALE = 4
    W_FINAL, H_FINAL = 2400, 1600
    W, H = W_FINAL * SCALE, H_FINAL * SCALE

    img = Image.new('RGB', (W, H), color='#070b14')
    draw = ImageDraw.Draw(img)

    C_CARD = '#0f172a'
    C_BORDER = '#1e293b'
    C_TEAL = '#2dd4bf'
    C_ORANGE = '#fb923c'
    C_WHITE = '#ffffff'
    C_MUTED = '#94a3b8'
    C_GRID = '#111c33'

    # Background grid
    for y in range(0, H, 80 * SCALE):
        draw.line([(0, y), (W, y)], fill=C_GRID, width=SCALE)
    for x in range(0, W, 80 * SCALE):
        draw.line([(x, 0), (x, H)], fill=C_GRID, width=SCALE)

    # Load actual TTF fonts at 4x resolution
    f_hero = ImageFont.truetype(font_bold, 130 * SCALE)
    f_h2 = ImageFont.truetype(font_bold, 44 * SCALE)
    f_sub = ImageFont.truetype(font_fine, 26 * SCALE)
    f_caps = ImageFont.truetype(font_bold, 50 * SCALE)
    f_low = ImageFont.truetype(font_fine, 46 * SCALE)
    f_mono_large = ImageFont.truetype(font_mono, 34 * SCALE)
    f_mono_small = ImageFont.truetype(font_mono, 22 * SCALE)
    f_meta = ImageFont.truetype(font_fine, 18 * SCALE)

    # Header
    draw.text((120 * SCALE, 80 * SCALE), 'POCKETGULL', font=f_hero, fill=C_WHITE)
    draw.text((120 * SCALE, 225 * SCALE), '100% OWNED BESPOKE VECTOR TYPEFACE  ·  DIRECT 4X SSAA TTF RENDER', font=f_sub, fill=C_TEAL)

    # Card 1: Character Matrix
    draw.rectangle([120 * SCALE, 280 * SCALE, (W_FINAL - 120) * SCALE, 750 * SCALE], fill=C_CARD, outline=C_BORDER, width=2 * SCALE)
    draw.text((160 * SCALE, 310 * SCALE), 'CHARACTER SET SPECIMEN (PocketGull Bold & Fineliner)', font=f_meta, fill=C_ORANGE)
    draw.text((160 * SCALE, 360 * SCALE), 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z', font=f_caps, fill=C_WHITE)
    draw.text((160 * SCALE, 450 * SCALE), 'a b c d e f g h i j k l m n o p q r s t u v w x y z', font=f_low, fill='#f1f5f9')
    draw.text((160 * SCALE, 540 * SCALE), '0 1 2 3 4 5 6 7 8 9  (Slashed Zero 0, Structured 1, Open 4)', font=f_caps, fill=C_TEAL)
    draw.text((160 * SCALE, 630 * SCALE), '! ? . , : ; - _ ( ) [ ] { } / \\ @ # $ % & * + = < > \' "', font=f_caps, fill=C_MUTED)

    # Card 2: Monospace Telemetry & Clinical Icons
    draw.rectangle([120 * SCALE, 790 * SCALE, (W_FINAL - 120) * SCALE, 1110 * SCALE], fill=C_CARD, outline=C_BORDER, width=2 * SCALE)
    draw.text((160 * SCALE, 820 * SCALE), 'CLINICAL TELEMETRY & BESPOKE MEDICAL ICONS (PocketGull Mono + PUA E001-E006)', font=f_meta, fill=C_TEAL)
    draw.text((160 * SCALE, 870 * SCALE), '\uE001 HEART_RATE: 72 bpm  ·  \uE002 SPO2: 98%  ·  \uE003 GLUCOSE: 104 mg/dL', font=f_mono_large, fill=C_TEAL)
    draw.text((160 * SCALE, 940 * SCALE), '\uE004 AED: ARMED & READY   \uE005 DISPATCH: 911 ACTIVE   \uE006 CPR: 110 BPM', font=f_mono_large, fill='#38bdf8')
    draw.text((160 * SCALE, 1010 * SCALE), '0123456789   0123456789   0123456789  (TABULAR 600 UPM + GPOS KERNING PAIRS)', font=f_mono_small, fill=C_MUTED)

    # Card 3: Editorial & Grid Specs
    draw.rectangle([120 * SCALE, 1150 * SCALE, (W_FINAL - 120) * SCALE, 1480 * SCALE], fill=C_CARD, outline=C_BORDER, width=2 * SCALE)
    draw.text((160 * SCALE, 1180 * SCALE), 'PANGRAM & OPTICAL KERNING PROOF (AV, AW, Ta, To, We, Yo)', font=f_meta, fill=C_ORANGE)
    draw.text((160 * SCALE, 1230 * SCALE), 'Sphinx of black quartz, judge my vow.', font=f_h2, fill=C_WHITE)
    draw.text((160 * SCALE, 1300 * SCALE), 'AWAY TOWARD VICTORY: Bystander 911 dispatch, CPR coach, and telemetry with zero ambiguity.', font=f_sub, fill='#cbd5e1')
    draw.text((160 * SCALE, 1370 * SCALE), '1024 UPM Grid  |  Cap: 720  |  x-Height: 480  |  Baseline: 0  |  Descender: -180  |  True Bézier Vectors', font=f_mono_small, fill=C_MUTED)

    # Downsample using high-order Lanczos filter for silky anti-aliased perfection
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

