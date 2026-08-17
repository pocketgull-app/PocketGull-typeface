#!/usr/bin/env python3
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

script_dir = os.path.dirname(os.path.abspath(__file__))
typeface_root = os.path.dirname(script_dir)
font_path = os.path.join(typeface_root, 'PocketGull-Bold.ttf')

font = TTFont(font_path)
cmap = font.getBestCmap()
glyf = font['glyf']

for ch in "PocketGull ABCXYZ 0123":
    cp = ord(ch)
    name = cmap.get(cp)
    has_glyf = name in glyf if name else False
    num_contours = glyf[name].numberOfContours if has_glyf else -1
    print(f"Char '{ch}' (U+{cp:04X}) -> Name: '{name}', in_glyf: {has_glyf}, num_contours: {num_contours}")
