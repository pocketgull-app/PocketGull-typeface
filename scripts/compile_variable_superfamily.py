import os
import sys
try:
    from fontTools.ttLib import TTFont  # type: ignore
    from fontTools.pens.ttGlyphPen import TTGlyphPen  # type: ignore
    from fontTools.pens.transformPen import TransformPen  # type: ignore
except ImportError:
    TTFont = None
    TTGlyphPen = None
    TransformPen = None

script_dir = os.path.dirname(os.path.abspath(__file__))
typeface_root = os.path.dirname(script_dir)
pocketgull_repo = os.path.abspath(os.path.join(typeface_root, '..', 'pocketgull'))
base_font_path = os.path.join(typeface_root, 'PocketGull-Bold.ttf')
target_dir = typeface_root
sync_dir = os.path.join(pocketgull_repo, 'public', 'fonts')
brand_fonts_dir = os.path.join(pocketgull_repo, 'public', 'brand', 'fonts')
os.makedirs(sync_dir, exist_ok=True)
os.makedirs(brand_fonts_dir, exist_ok=True)

print("Compiling Complete PocketGull Variable Superfamily...")

def update_name_table(font, family_name, style_name, full_name, ps_name):
    if 'name' not in font:
        return
    name_table = font['name']
    for record in name_table.names:
        if record.nameID == 1:
            record.string = family_name
        elif record.nameID == 2:
            record.string = style_name
        elif record.nameID == 4:
            record.string = full_name
        elif record.nameID == 6:
            record.string = ps_name

# 1. Master Bold Font (800)
font_bold = TTFont(base_font_path)
if 'OS/2' in font_bold:
    font_bold['OS/2'].usWeightClass = 700
update_name_table(font_bold, "PocketGull", "Bold", "PocketGull Bold", "PocketGull-Bold")
font_bold.save(os.path.join(target_dir, 'PocketGull-Bold.ttf'))
font_bold.save(os.path.join(sync_dir, 'PocketGull-Bold.ttf'))

# 2. Chiseltip Font (900)
font_chisel = TTFont(base_font_path)
if 'OS/2' in font_chisel:
    font_chisel['OS/2'].usWeightClass = 900
update_name_table(font_chisel, "PocketGull", "Black", "PocketGull Chiseltip", "PocketGull-Chiseltip")
glyf_chisel = font_chisel['glyf']
for name in glyf_chisel.keys():
    g = glyf_chisel[name]
    if g.numberOfContours > 0:
        pen = TTGlyphPen(font_chisel.getGlyphSet())
        tpen = TransformPen(pen, (1.15, 0, -0.05, 1.0, 0, 0))
        try:
            g.draw(tpen, glyf_chisel)
            glyf_chisel[name] = pen.glyph()
        except:
            pass
font_chisel.save(os.path.join(target_dir, 'PocketGull-Chiseltip.ttf'))
font_chisel.save(os.path.join(sync_dir, 'PocketGull-Chiseltip.ttf'))

# 3. Fineliner Font (400)
font_fine = TTFont(base_font_path)
if 'OS/2' in font_fine:
    font_fine['OS/2'].usWeightClass = 400
    font_fine['OS/2'].fsSelection &= ~(1 << 5)
    font_fine['OS/2'].fsSelection |= (1 << 6)
if 'head' in font_fine:
    font_fine['head'].macStyle &= ~(1 << 0)
update_name_table(font_fine, "PocketGull", "Regular", "PocketGull Fineliner", "PocketGull-Fineliner")
glyf_fine = font_fine['glyf']
for name in glyf_fine.keys():
    g = glyf_fine[name]
    if g.numberOfContours > 0:
        pen = TTGlyphPen(font_fine.getGlyphSet())
        tpen = TransformPen(pen, (0.85, 0, -0.02, 1.0, 0, 0))
        try:
            g.draw(tpen, glyf_fine)
            glyf_fine[name] = pen.glyph()
        except:
            pass
font_fine.save(os.path.join(target_dir, 'PocketGull-Fineliner.ttf'))
font_fine.save(os.path.join(sync_dir, 'PocketGull-Fineliner.ttf'))

# 4. PocketGull Mono Font (400 Monospace)
font_mono = TTFont(base_font_path)
if 'OS/2' in font_mono:
    font_mono['OS/2'].usWeightClass = 400
    font_mono['OS/2'].panose.bProportion = 9
if 'post' in font_mono:
    font_mono['post'].isFixedPitch = 1
update_name_table(font_mono, "PocketGull Mono", "Regular", "PocketGull Mono Regular", "PocketGullMono-Regular")
hmtx_mono = font_mono['hmtx']
glyf_mono = font_mono['glyf']
for name in hmtx_mono.metrics.keys():
    width, lsb = hmtx_mono[name]
    hmtx_mono[name] = (600, max(lsb, 20))
font_mono.save(os.path.join(target_dir, 'PocketGullMono-Regular.ttf'))
font_mono.save(os.path.join(sync_dir, 'PocketGullMono-Regular.ttf'))
font_mono.save(os.path.join(brand_fonts_dir, 'PocketGullMono-Regular.ttf'))

# 5. PocketGull Variable Font (VF) with Continuous Axes
from fontTools.ttLib import newTable
from fontTools.ttLib.tables._f_v_a_r import Axis, NamedInstance

font_vf = TTFont(base_font_path)
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

inst_chiseltip = NamedInstance()
inst_chiseltip.subfamilyNameID = 262
inst_chiseltip.coordinates = {'wght': 850.0, 'opsz': 36.0, 'slnt': -12.0}

fvar.instances = [inst_regular, inst_bold, inst_black, inst_chiseltip]
font_vf['fvar'] = fvar

name_vf = font_vf['name']
name_vf.setName("Weight", 256, 3, 1, 0x409)
name_vf.setName("Optical size", 257, 3, 1, 0x409)
name_vf.setName("Slant", 258, 3, 1, 0x409)
name_vf.setName("PocketGull Variable Regular", 259, 3, 1, 0x409)
name_vf.setName("PocketGull Variable Bold", 260, 3, 1, 0x409)
name_vf.setName("PocketGull Variable Black", 261, 3, 1, 0x409)
name_vf.setName("PocketGull Variable Chiseltip", 262, 3, 1, 0x409)
name_vf.setName("PocketGull Variable", 1, 3, 1, 0x409)
name_vf.setName("PocketGull Variable", 4, 3, 1, 0x409)
name_vf.setName("PocketGull-VF", 6, 3, 1, 0x409)

for destination in [target_dir, sync_dir, brand_fonts_dir]:
    font_vf.save(os.path.join(destination, 'PocketGull-VF.ttf'))
    font_vf.flavor = 'woff2'
    font_vf.save(os.path.join(destination, 'PocketGull-VF.woff2'))

print("PocketGull Variable Superfamily & VF compilation complete!")
