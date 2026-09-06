#!/usr/bin/env python3
"""
PocketGull Typefoundry: Marker Raw Display Font Compiler v3.3 (Optical Harmony & Sprezzatura)
=============================================================================================
Calibrates both width and height of Phil Gear's cardstock wordmark letters
to optically match the Chiseltip proportion while preserving 100% of the hand-drawn
paper-fiber texture, felt ink bleed, and organic wabi-sabi character.
"""

import os
import sys
import math
import brotli
import pyclipper
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.basePen import BasePen
from fontTools.svgLib.path import SVGPath

ROOT_DIR = r"c:\Users\philg\Pocketgull\pocketgull-typeface"

# Phil Gear's original hand-lettered cardstock wordmark SVG paths (y=79 baseline)
MASTER_WORDMARK_PATHS = {
    'P': "M12.3774,78.2247l-10.6363.539c-1.0299.0522-1.0654-1.9957-1.0618-3.2533l.0682-23.9046L0,4.2922l15.9781-1.8972c5.2085-.6184,11.3528-.0727,15.6852,2.6997,6.996,4.4768,7.9626,12.5212,7.2141,20.092-.7384,7.4681-4.7398,12.9561-12.6058,14.3846-4.5638.8288-9.8724.8405-14.6992.7813l.805,37.8721ZM23.3856,11.9225l-12.5362-.239.4084,20.6907,7.0349-.1314c3.0425-.0568,6.1524-.8601,8.0174-2.8765,4.5186-4.8856,2.1707-17.3466-2.9245-17.4438Z",
    'o': "M54.1176,75.9705c-6.6018,4.2596-15.2607,4.4551-20.8514-1.2403-3.0268-3.0835-3.9006-8.3698-3.8652-12.558l.0897-10.614c.0297-3.51.4773-7.908,2.6311-10.8275,5.3068-7.1932,16.3394-8.1015,22.6686-1.7502,2.6704,2.6797,3.2518,7.4675,3.3093,11.0673l.1829,11.4513c.0828,5.1831-1.169,9.7951-4.1649,14.4713ZM47.985,45.9357c-.336-1.8815-2.3187-3.6686-3.9084-3.7777-1.2337-.0847-4.0325,1.3265-4.2235,2.6144l-1.1091,7.4776c-1.0924,7.3652-.7522,18.687,4.6653,19.9189,6.6863,1.5204,6.4137-15.9424,4.5758-26.2331Z",
    'c': "M78.9789,66.3963c1.6234-1.6446,5.9064-2.2229,8.6012-1.6798.8391,4.2044-.2906,9.2356-3.9069,11.8752-5.7381,4.1885-14.4611,3.1168-19.2277-2.207-4.8179-5.3811-4.3934-22.0405-2.4064-30.7899,1.339-5.8959,6.5748-9.444,12.3783-9.9086,6.9666-.5577,13.0487,3.6713,13.2375,10.9799-2.6647.9568-5.5755,1.4739-8.3501,1.5473-.4309-2.6953-2.0659-5.2871-4.1351-5.7307-1.3655-.2927-3.9435,1.9507-4.1525,3.2083-1.7209,10.356-2.0152,28.8656,4.528,27.8226,2.2567-.3597,3.009-1.9651,3.4336-5.1174Z",
    'k': "M110.9035,77.7205l-10.8948-22.1012.2332,21.9387-10.2298.1982c1.1959-11.3402.8582-22.0661.6576-33.6001l-.3655-21.0132-.6585-15.2478,10.0504-2.582.2615,36.2483,9.9255-12.5789c3.1845-.3447,6.1716-.3454,10.4783.1605l-14.6734,17.4289,14.4498,27.486,1.3186,3.2166-10.5529.4461Z",
    'e': "M136.0613,68.2649l1.5035-3.9409,8.1078.8255c.2935,7.6111-5.4883,12.7852-12.696,12.7056-7.5673-.0836-13.1446-4.9327-13.6463-12.6783-1.0186-15.726-2.4648-32.0826,13.5502-33.0748,5.1399-.3185,8.8824,1.6939,10.8861,6.6122,1.8825,4.6207,2.1353,9.7262,1.8903,15.2683l-18.0748,2.8283,2.5795,10.9651c.1813.7708,1.7413,2.0033,2.5016,2.2416.9124.286,3.052-.8456,3.398-1.7524ZM137.2873,49.4212c-.393-2.7843-1.0426-7.0275-3.1103-9.4438-1.7172-2.0067-5.9162.1411-6.0865,2.4052l-.6413,8.5292,9.838-1.4906Z",
    't': "M167.8955,76.5618c-4.8555,2.5153-10.6732,2.8542-14.9286-.9607-1.6163-1.4489-2.6764-5.7241-2.6795-8.1789l-.0417-33.0461-5.5745-.0601-.2127-7.0223,6.0601-.3361.0269-8.9567,9.0089-3.0097-.3207,11.9859,6.6881-.4121.4348,7.4823-7.4199.3543.4237,31.562c.351,1.0938.9235,3.5135,1.8441,3.646s2.4841-.1871,4.4717-.5068c1.135,1.2079,1.9425,4.4914,2.2192,7.459Z",
    'G': "M196.1527,49.5175l-9.6026-.2105.0872-8.5363,15.8828-.2878c.6505-.0118,2.5194.4281,2.5219.9536l.0132,2.8092c.0504,10.7462-.2707,30.077-8.3798,32.9086-6.3173,2.2059-14.7639,2.1945-20.3556-2.2654-4.4845-3.5768-6.5955-10.3431-6.9251-15.9495-.7912-13.456-.6443-26.3988.9491-39.6623.738-6.1434,3.4314-12.0152,8.9481-15.0255,6.7244-3.6693,15.9115-2.634,21.4326,2.8673,3.0024,2.9916,3.503,8.197,3.7773,11.8503l-10.0943,1.569c-.4914-2.9384-.7341-5.1352-2.0439-7.4909-.9534-1.7148-4.8675-1.7553-6.9122-1.0087-1.7612.6431-3.5672,3.2099-4.0988,5.774-2.8583,13.7863-3.4015,32.7364-.032,46.0594.8582,3.3935,3.848,5.1082,6.7651,5.0968s6.5093-1.4308,6.8183-5.0051l1.2489-14.4465Z",
    'u': "M209.1422,68.4496l-.6151-9.6405-.2755-25.0952,9.4489.0693c-.7423,10.5626-2.4638,33.1237,2.2059,35.6762.8902.4866,3.2203-.2328,4.0631-1.0389,2.0142-1.9265,1.6903-4.6469,1.6575-7.2096l-.345-26.9487c2.6953-1.1954,6.6895-1.4305,9.4194-.8004l-.2046,14.3924c-.1393,9.7997-1.8975,19.407,1.243,28.8777l-8.9625,1.6587-1.1408-3.7358c-3.034,2.8692-7.606,4.3866-11.7063,2.3124-2.7939-1.4134-4.5731-5.1476-4.7881-8.5176Z",
    'l': "M238.4993,77.9034l.0864-21.4524c.0511-12.6775.7401-25.0515-.1302-37.74l-.798-11.6338,10.2181-3.3643-.795,42.9925,1.329,31.4307-9.9104-.2327Z",
}

class ContourExtractor(BasePen):
    def __init__(self):
        super().__init__()
        self.polys = []
        self.curr = []

    def _moveTo(self, pt):
        if self.curr:
            self.polys.append(self.curr)
        self.curr = [pt]

    def _lineTo(self, pt):
        self.curr.append(pt)

    def _curveToOne(self, p1, p2, p3):
        p0 = self.curr[-1]
        for s in range(1, 10):
            t = s / 9.0
            x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
            y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
            self.curr.append((x, y))

    def _qCurveToOne(self, p1, p2):
        p0 = self.curr[-1]
        for s in range(1, 8):
            t = s / 7.0
            x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t**2*p2[0]
            y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t**2*p2[1]
            self.curr.append((x, y))

    def _closePath(self):
        if self.curr:
            self.polys.append(self.curr)
            self.curr = []

    def _endPath(self):
        self._closePath()

def parse_svg_to_polys(d_string, scale=10.2, dx=0, dy=79.0 * 10.2):
    pen = ContourExtractor()
    svg = SVGPath.fromstring(f'<path d="{d_string}"/>')
    svg.draw(pen)
    
    transformed_contours = []
    for c in pen.polys:
        tc = []
        for x, y in c:
            tx = x * scale + dx
            ty = dy - y * scale
            tc.append((round(tx), round(ty)))
        transformed_contours.append(tc)
    return transformed_contours

def get_bounds(polys):
    all_x = [pt[0] for poly in polys for pt in poly]
    all_y = [pt[1] for poly in polys for pt in poly]
    if not all_x:
        return 0, 0, 0, 0
    return min(all_x), min(all_y), max(all_x), max(all_y)

def translate_polys(polys, dx, dy):
    return [[(round(pt[0] + dx), round(pt[1] + dy)) for pt in poly] for poly in polys]

def scale_polys(polys, sx, sy, cx=0, cy=0):
    return [[(round(cx + (pt[0] - cx) * sx), round(cy + (pt[1] - cy) * sy)) for pt in poly] for poly in polys]

def union_polys(*poly_lists):
    pc = pyclipper.Pyclipper()
    for plist in poly_lists:
        for poly in plist:
            if len(poly) >= 3:
                pc.AddPath(poly, pyclipper.PT_SUBJECT, True)
    return pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)

def apply_wabi_sabi_ink_bleed(polys, seed_val=0, dilation=9.0):
    transformed = []
    shear = math.tan(math.radians(1.6))
    
    for poly_idx, poly in enumerate(polys):
        t_poly = []
        for i, (x, y) in enumerate(poly):
            xs = x + y * shear
            phase = (i * 7.3 + poly_idx * 17.1 + seed_val * 31.7)
            wobble_x = math.sin(phase) * 3.6 + math.cos(phase * 1.7) * 1.8
            wobble_y = math.cos(phase * 1.3) * 3.0 + math.sin(phase * 2.3) * 1.6
            t_poly.append((round(xs + wobble_x), round(y + wobble_y)))
        transformed.append(t_poly)

    pco = pyclipper.PyclipperOffset()
    for poly in transformed:
        if len(poly) >= 3:
            pco.AddPath(poly, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
    expanded = pco.Execute(dilation)
    return expanded

def polys_to_glyph(font, polys, target_lsb=50, target_adv=None):
    b = get_bounds(polys)
    width = b[2] - b[0] if b[2] > b[0] else 500
    dx = -b[0] + target_lsb

    tt_pen = TTGlyphPen(font.getGlyphSet())
    cu2qu_pen = Cu2QuPen(tt_pen, max_err=1.2)

    for poly in polys:
        if len(poly) < 3:
            continue
        p0 = (poly[0][0] + dx, poly[0][1])
        cu2qu_pen.moveTo(p0)
        for pt in poly[1:]:
            cu2qu_pen.lineTo((pt[0] + dx, pt[1]))
        cu2qu_pen.closePath()

    glyph = tt_pen.glyph()
    if glyph.numberOfContours > 0:
        coords = list(glyph.coordinates)
        flags = list(glyph.flags)
        endPts = list(glyph.endPtsOfContours)
        new_coords = []
        new_flags = []
        new_endPts = []
        start = 0
        for end in endPts:
            pts = coords[start:end+1]
            flgs = flags[start:end+1]
            filtered_pts = []
            filtered_flgs = []
            for i in range(len(pts)):
                if not filtered_pts or pts[i] != filtered_pts[-1]:
                    filtered_pts.append(pts[i])
                    filtered_flgs.append(flgs[i] & 0x3F)
            if len(filtered_pts) > 1 and filtered_pts[0] == filtered_pts[-1]:
                filtered_pts = filtered_pts[:-1]
                filtered_flgs = filtered_flgs[:-1]
            if len(filtered_pts) >= 3:
                new_coords.extend(filtered_pts)
                new_flags.extend(filtered_flgs)
                new_endPts.append(len(new_coords) - 1)
            start = end + 1
        glyph.coordinates = GlyphCoordinates(new_coords)
        glyph.flags = bytearray(new_flags)
        glyph.endPtsOfContours = new_endPts

    glyph.recalcBounds(font['glyf'])
    adv_width = target_adv if target_adv is not None else int(width + target_lsb * 2)
    return glyph, adv_width

def build_wabi_sabi_font():
    src_ttf = os.path.join(ROOT_DIR, 'fonts', 'ttf', 'PocketGull-Chiseltip.ttf')
    out_ttf = os.path.join(ROOT_DIR, 'fonts', 'ttf', 'PocketGull-MarkerRaw.ttf')
    out_woff2 = os.path.join(ROOT_DIR, 'fonts', 'woff2', 'PocketGull-MarkerRaw.woff2')

    print("==================================================================")
    print("PocketGull Marker Raw Compiler v3.3: Optical Proportion Balance")
    print("==================================================================")
    print(f"[INFO] Loading source template: {src_ttf} ...")
    font = TTFont(src_ttf)
    glyf = font['glyf']
    hmtx = font['hmtx']

    # 1. Parse authentic cardstock wordmark letters (P, o, c, k, e, t, G, u, l)
    print("[1/4] Calibrating authentic cardstock letters to typographic em-box...")
    masters = {}
    for char, d in MASTER_WORDMARK_PATHS.items():
        polys = parse_svg_to_polys(d)
        b = get_bounds(polys)
        norm = translate_polys(polys, -b[0], -b[1])
        masters[char] = norm

    # Chiseltip target optical metrics for each letter
    target_metrics = {
        'P': (518, 714, 632, 60),
        'G': (621, 724, 740, 55),
        'o': (552, 563, 637, 45),
        'c': (472, 563, 539, 45),
        'k': (593, 760, 659, 55),
        'e': (534, 563, 618, 45),
        't': (403, 664, 460, 35),
        'u': (539, 553, 670, 65),
        'l': (191, 760, 323, 65),
    }

    cardstock_scaled = {}
    for char, (tgt_w, tgt_h, tgt_adv, tgt_lsb) in target_metrics.items():
        b = get_bounds(masters[char])
        cur_w = b[2] - b[0]
        cur_h = b[3] - b[1]
        sx = tgt_w / cur_w
        sy = tgt_h / cur_h
        cardstock_scaled[char] = (scale_polys(masters[char], sx, sy), tgt_adv, tgt_lsb)

    # Authentic single-story humanist lowercase 'g' from cardstock broadside
    # o bowl + sweeping parabolic descender
    o_bowl, _, _ = cardstock_scaled['o']
    b_ob = get_bounds(o_bowl)
    g_desc_pts = [
        (b_ob[2] - 15, b_ob[3] - 10),
        (b_ob[2], 100),
        (b_ob[2] - 10, -60),
        (b_ob[2] - 60, -200),
        ((b_ob[0] + b_ob[2]) / 2.0, -240),
        (b_ob[0] + 20, -180),
        (b_ob[0] + 10, -110),
    ]
    def make_calligraphic_descender(points, stroke_w=170):
        dense = []
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i+1]
            for s in range(12):
                t = s / 12.0
                dense.append((p1[0]*(1-t) + p2[0]*t, p1[1]*(1-t) + p2[1]*t))
        dense.append(points[-1])
        l_pts = []
        r_pts = []
        r = stroke_w / 2.0
        for i in range(len(dense)):
            x, y = dense[i]
            if i == 0: dx, dy = dense[1][0] - x, dense[1][1] - y
            elif i == len(dense)-1: dx, dy = x - dense[i-1][0], y - dense[i-1][1]
            else: dx, dy = dense[i+1][0] - dense[i-1][0], dense[i+1][1] - dense[i-1][1]
            L = math.hypot(dx, dy)
            if L < 1e-5: nx, ny = 0, r
            else: nx, ny = -dy/L*r, dx/L*r
            l_pts.append((round(x + nx), round(y + ny)))
            r_pts.append((round(x - nx), round(y - ny)))
        return [l_pts + list(reversed(r_pts))]

    g_loop = make_calligraphic_descender(g_desc_pts, stroke_w=170)
    cardstock_scaled['g'] = (union_polys(o_bowl, g_loop), 643, 45)

    print("\n[2/4] Infusing full superfamily glyphs with wabi-sabi felt-marker edge flow...")
    
    char_to_glyphname = {
        'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G',
        'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N',
        'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U',
        'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z',
        'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g',
        'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n',
        'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u',
        'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z',
        '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
        '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
        '.': 'period', ',': 'comma', ':': 'colon', ';': 'semicolon',
        '!': 'exclam', '?': 'question', '-': 'hyphen', '/': 'slash',
        '(': 'parenleft', ')': 'parenright', '&': 'ampersand',
    }

    injected = 0
    for char, gname in char_to_glyphname.items():
        seed_val = ord(char)
        
        if char in cardstock_scaled:
            raw_polys, tgt_adv, tgt_lsb = cardstock_scaled[char]
            styled_polys = apply_wabi_sabi_ink_bleed(raw_polys, seed_val=seed_val, dilation=5.0)
            glyph, adv = polys_to_glyph(font, styled_polys, target_lsb=tgt_lsb, target_adv=tgt_adv)
        else:
            extractor = ContourExtractor()
            glyf[gname].draw(extractor, glyf)
            raw_polys = extractor.polys
            styled_polys = apply_wabi_sabi_ink_bleed(raw_polys, seed_val=seed_val, dilation=11.5)
            orig_adv, orig_lsb = hmtx[gname]
            target_adv = int(orig_adv * 1.02)
            target_lsb = max(35, int(orig_lsb * 0.95))
            glyph, adv = polys_to_glyph(font, styled_polys, target_lsb=target_lsb, target_adv=target_adv)

        glyf[gname] = glyph
        hmtx[gname] = (adv, glyph.xMin)
        injected += 1
        if char in "POCKTGUL":
            print(f"  • Injected '{char}' ({gname}): adv={adv} UPM, {glyph.numberOfContours} contours, box=({glyph.xMin},{glyph.yMin},{glyph.xMax},{glyph.yMax})")

    print(f"  -> Injected {injected} master wabi-sabi glyphs into 'glyf' & 'hmtx'.")

    # 3. Metadata
    print("\n[3/4] Updating OpenType metadata & Option 5 naming table...")
    family_name = "PocketGull Marker Raw"
    style_name = "Regular"
    full_name = "PocketGull Marker Raw"
    ps_name = "PocketGull-MarkerRaw"
    version_str = "Version 3.300; The PocketGull Project Authors; OFL 1.1"
    copyright_str = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-typeface)"

    name_table = font['name']
    name_table.names = [n for n in name_table.names if n.nameID not in [1, 2, 3, 4, 5, 6, 16, 17]]

    def add_name(name_id, text):
        name_table.addMultilingualName({'en': text}, font, nameID=name_id)

    add_name(0, copyright_str)
    add_name(1, family_name)
    add_name(2, style_name)
    add_name(3, f"3.300;POCK;{ps_name}")
    add_name(4, full_name)
    add_name(5, version_str)
    add_name(6, ps_name)
    add_name(16, family_name)
    add_name(17, style_name)

    font['head'].fontRevision = 3.3
    font['head'].macStyle = 0x0000

    if 'OS/2' in font:
        font['OS/2'].usWeightClass = 900
        font['OS/2'].fsSelection = font['OS/2'].fsSelection & ~0x01 & ~0x20 | 0x40
        font['OS/2'].achVendID = 'POCK'

    print(f"Saving compiled TTF: {out_ttf} ...")
    font.save(out_ttf)
    font.close()

    ttf_reopen = TTFont(out_ttf)
    ttf_reopen.flavor = 'woff2'
    ttf_reopen.save(out_woff2)
    ttf_reopen.close()
    print(f"Saved WOFF2: {out_woff2}")
    print("[SUCCESS] PocketGull Marker Raw v3.3 successfully compiled with optical balance!")

if __name__ == '__main__':
    build_wabi_sabi_font()
