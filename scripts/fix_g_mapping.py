"""
Task C: Fix g/G mapping.
The SVG wordmark 'g' is a display-capital letterform.
This script maps it to both G (uppercase) and g (lowercase) slots,
then re-copies the fixed fonts to the main app.
"""
import os
import hashlib
from fontTools.ttLib import TTFont
from fontTools.svgLib.path import SVGPath
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

BASELINE_SVG = 79.0
ASCENDER_FONT = 800
SCALE = ASCENDER_FONT / BASELINE_SVG
LSB = 40
RSB = 40
FONT_DIR = r'c:\Users\philg\Pocketgull\pocketgull-typeface'
APP_FONT_DIR = r'c:\Users\philg\Pocketgull\pocketgull\public\fonts'

# The g/G SVG path
G_PATH = "M196.1527,49.5175l-9.6026-.2105.0872-8.5363,15.8828-.2878c.6505-.0118,2.5194.4281,2.5219.9536l.0132,2.8092c.0504,10.7462-.2707,30.077-8.3798,32.9086-6.3173,2.2059-14.7639,2.1945-20.3556-2.2654-4.4845-3.5768-6.5955-10.3431-6.9251-15.9495-.7912-13.456-.6443-26.3988.9491-39.6623.738-6.1434,3.4314-12.0152,8.9481-15.0255,6.7244-3.6693,15.9115-2.634,21.4326,2.8673,3.0024,2.9916,3.503,8.197,3.7773,11.8503l-10.0943,1.569c-.4914-2.9384-.7341-5.1352-2.0439-7.4909-.9534-1.7148-4.8675-1.7553-6.9122-1.0087-1.7612.6431-3.5672,3.2099-4.0988,5.774-2.8583,13.7863-3.4015,32.7364-.032,46.0594.8582,3.3935,3.848,5.1082,6.7651,5.0968s6.5093-1.4308,6.8183-5.0051l1.2489-14.4465Z"


def get_svg_bounds(d_path):
    svg_path = SVGPath.fromstring(f'<path d="{d_path}"/>')
    bp = BoundsPen(None)
    svg_path.draw(bp)
    return bp.bounds


def compile_glyph(font, d_path, svg_bounds):
    svg_xMin = svg_bounds[0]
    svg_width = svg_bounds[2] - svg_bounds[0]
    dx = -svg_xMin * SCALE + LSB
    dy = BASELINE_SVG * SCALE

    svg_path = SVGPath.fromstring(f'<path d="{d_path}"/>')
    pen = TTGlyphPen(font.getGlyphSet())
    cu_pen = Cu2QuPen(pen, max_err=1.0)
    tpen = TransformPen(cu_pen, (SCALE, 0, 0, -SCALE, dx, dy))
    svg_path.draw(tpen)

    glyph = pen.glyph()
    advance_width = int(svg_width * SCALE + LSB + RSB)
    return glyph, advance_width, LSB


bounds = get_svg_bounds(G_PATH)

ttf_files = [f for f in os.listdir(FONT_DIR) if f.endswith('.ttf')]
for filename in sorted(ttf_files):
    filepath = os.path.join(FONT_DIR, filename)
    font = TTFont(filepath)
    
    # Compile G path into both 'G' and 'g' slots
    for slot in ['G', 'g']:
        glyph, aw, lsb = compile_glyph(font, G_PATH, bounds)
        font['glyf'][slot] = glyph
        font['hmtx'].metrics[slot] = (aw, lsb)
    
    font['head'].created = 0
    font['head'].modified = 0
    
    tmp = filepath + '.tmp'
    font.save(tmp)
    font.close()
    
    os.chmod(filepath, 0o666)
    os.remove(filepath)
    os.rename(tmp, filepath)
    
    # Also copy to main app
    app_path = os.path.join(APP_FONT_DIR, filename)
    if os.path.exists(app_path):
        os.chmod(app_path, 0o666)
    import shutil
    shutil.copy2(filepath, app_path)
    
    with open(filepath, 'rb') as f:
        sha = hashlib.sha256(f.read()).hexdigest()[:24]
    print(f"  {filename}: G+g mapped, SHA={sha}...")

print("\nDone. G/g fixed across all variants and copied to main app.")
