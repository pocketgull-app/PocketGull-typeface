"""
PocketGull Type Designer Agent
Generates SVG glyph outlines from skeletons using the nib engine,
then compiles them into the font alongside the 9 master SVG glyphs.
"""
import os
import sys
import hashlib
import shutil

# Add scripts dir to path for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from fontTools.ttLib import TTFont
from fontTools.svgLib.path import SVGPath
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

from nib_engine import StrokeExpander, POCKETGULL_NIB
from glyph_skeletons import get_all_skeletons

# ─────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────
BASELINE_SVG = 79.0
ASCENDER_FONT = 800
SCALE = ASCENDER_FONT / BASELINE_SVG  # ~10.127
LSB = 40
RSB = 40

FONT_DIR = os.path.dirname(SCRIPT_DIR)
APP_FONT_DIR = os.path.abspath(os.path.join(FONT_DIR, '..', 'pocketgull', 'public', 'fonts'))
BRAND_FONT_DIR = os.path.abspath(os.path.join(FONT_DIR, '..', 'pocketgull', 'public', 'brand', 'fonts'))

# Master SVG paths (from the original wordmark — these take priority)
MASTER_PATHS = {
    'P': "M12.3774,78.2247l-10.6363.539c-1.0299.0522-1.0654-1.9957-1.0618-3.2533l.0682-23.9046L0,4.2922l15.9781-1.8972c5.2085-.6184,11.3528-.0727,15.6852,2.6997,6.996,4.4768,7.9626,12.5212,7.2141,20.092-.7384,7.4681-4.7398,12.9561-12.6058,14.3846-4.5638.8288-9.8724.8405-14.6992.7813l.805,37.8721ZM23.3856,11.9225l-12.5362-.239.4084,20.6907,7.0349-.1314c3.0425-.0568,6.1524-.8601,8.0174-2.8765,4.5186-4.8856,2.1707-17.3466-2.9245-17.4438Z",
    'o': "M54.1176,75.9705c-6.6018,4.2596-15.2607,4.4551-20.8514-1.2403-3.0268-3.0835-3.9006-8.3698-3.8652-12.558l.0897-10.614c.0297-3.51.4773-7.908,2.6311-10.8275,5.3068-7.1932,16.3394-8.1015,22.6686-1.7502,2.6704,2.6797,3.2518,7.4675,3.3093,11.0673l.1829,11.4513c.0828,5.1831-1.169,9.7951-4.1649,14.4713ZM47.985,45.9357c-.336-1.8815-2.3187-3.6686-3.9084-3.7777-1.2337-.0847-4.0325,1.3265-4.2235,2.6144l-1.1091,7.4776c-1.0924,7.3652-.7522,18.687,4.6653,19.9189,6.6863,1.5204,6.4137-15.9424,4.5758-26.2331Z",
    'c': "M78.9789,66.3963c1.6234-1.6446,5.9064-2.2229,8.6012-1.6798.8391,4.2044-.2906,9.2356-3.9069,11.8752-5.7381,4.1885-14.4611,3.1168-19.2277-2.207-4.8179-5.3811-4.3934-22.0405-2.4064-30.7899,1.339-5.8959,6.5748-9.444,12.3783-9.9086,6.9666-.5577,13.0487,3.6713,13.2375,10.9799-2.6647.9568-5.5755,1.4739-8.3501,1.5473-.4309-2.6953-2.0659-5.2871-4.1351-5.7307-1.3655-.2927-3.9435,1.9507-4.1525,3.2083-1.7209,10.356-2.0152,28.8656,4.528,27.8226,2.2567-.3597,3.009-1.9651,3.4336-5.1174Z",
    'k': "M110.9035,77.7205l-10.8948-22.1012.2332,21.9387-10.2298.1982c1.1959-11.3402.8582-22.0661.6576-33.6001l-.3655-21.0132-.6585-15.2478,10.0504-2.582.2615,36.2483,9.9255-12.5789c3.1845-.3447,6.1716-.3454,10.4783.1605l-14.6734,17.4289,14.4498,27.486,1.3186,3.2166-10.5529.4461Z",
    'e': "M136.0613,68.2649l1.5035-3.9409,8.1078.8255c.2935,7.6111-5.4883,12.7852-12.696,12.7056-7.5673-.0836-13.1446-4.9327-13.6463-12.6783-1.0186-15.726-2.4648-32.0826,13.5502-33.0748,5.1399-.3185,8.8824,1.6939,10.8861,6.6122,1.8825,4.6207,2.1353,9.7262,1.8903,15.2683l-18.0748,2.8283,2.5795,10.9651c.1813.7708,1.7413,2.0033,2.5016,2.2416.9124.286,3.052-.8456,3.398-1.7524ZM137.2873,49.4212c-.393-2.7843-1.0426-7.0275-3.1103-9.4438-1.7172-2.0067-5.9162.1411-6.0865,2.4052l-.6413,8.5292,9.838-1.4906Z",
    't': "M167.8955,76.5618c-4.8555,2.5153-10.6732,2.8542-14.9286-.9607-1.6163-1.4489-2.6764-5.7241-2.6795-8.1789l-.0417-33.0461-5.5745-.0601-.2127-7.0223,6.0601-.3361.0269-8.9567,9.0089-3.0097-.3207,11.9859,6.6881-.4121.4348,7.4823-7.4199.3543.4237,31.562c.351,1.0938.9235,3.5135,1.8441,3.646s2.4841-.1871,4.4717-.5068c1.135,1.2079,1.9425,4.4914,2.2192,7.459Z",
    'g': "M196.1527,49.5175l-9.6026-.2105.0872-8.5363,15.8828-.2878c.6505-.0118,2.5194.4281,2.5219.9536l.0132,2.8092c.0504,10.7462-.2707,30.077-8.3798,32.9086-6.3173,2.2059-14.7639,2.1945-20.3556-2.2654-4.4845-3.5768-6.5955-10.3431-6.9251-15.9495-.7912-13.456-.6443-26.3988.9491-39.6623.738-6.1434,3.4314-12.0152,8.9481-15.0255,6.7244-3.6693,15.9115-2.634,21.4326,2.8673,3.0024,2.9916,3.503,8.197,3.7773,11.8503l-10.0943,1.569c-.4914-2.9384-.7341-5.1352-2.0439-7.4909-.9534-1.7148-4.8675-1.7553-6.9122-1.0087-1.7612.6431-3.5672,3.2099-4.0988,5.774-2.8583,13.7863-3.4015,32.7364-.032,46.0594.8582,3.3935,3.848,5.1082,6.7651,5.0968s6.5093-1.4308,6.8183-5.0051l1.2489-14.4465Z",
    'u': "M209.1422,68.4496l-.6151-9.6405-.2755-25.0952,9.4489.0693c-.7423,10.5626-2.4638,33.1237,2.2059,35.6762.8902.4866,3.2203-.2328,4.0631-1.0389,2.0142-1.9265,1.6903-4.6469,1.6575-7.2096l-.345-26.9487c2.6953-1.1954,6.6895-1.4305,9.4194-.8004l-.2046,14.3924c-.1393,9.7997-1.8975,19.407,1.243,28.8777l-8.9625,1.6587-1.1408-3.7358c-3.034,2.8692-7.606,4.3866-11.7063,2.3124-2.7939-1.4134-4.5731-5.1476-4.7881-8.5176Z",
    'l': "M238.4993,77.9034l.0864-21.4524c.0511-12.6775.7401-25.0515-.1302-37.74l-.798-11.6338,10.2181-3.3643-.795,42.9925,1.329,31.4307-9.9104-.2327Z",
}

# Also map G to the same path as g (display capital form)
MASTER_PATHS['G'] = MASTER_PATHS['g']


def get_svg_bounds(d_path):
    """Parse an SVG path and return its bounding box."""
    svg_path = SVGPath.fromstring(f'<path d="{d_path}"/>')
    bp = BoundsPen(None)
    svg_path.draw(bp)
    return bp.bounds


def compile_svg_glyph(font, d_path, svg_bounds):
    """Compile a raw SVG path d-attribute into a TrueType glyph."""
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


def compile_generated_glyph(font, svg_d, skeleton_width):
    """Compile a generated SVG path (from nib engine) into a TrueType glyph."""
    # The generated SVG is already in the wordmark coordinate space
    bounds = get_svg_bounds(svg_d)
    if bounds is None:
        return None, 0, 0
    return compile_svg_glyph(font, svg_d, bounds)


def main():
    print("=" * 60)
    print("POCKETGULL TYPE DESIGNER AGENT")
    print("=" * 60)
    
    # Phase 1: Generate SVG paths from skeletons
    print("\n[Phase 1] Expanding glyph skeletons with nib engine...")
    expander = StrokeExpander(POCKETGULL_NIB)
    skeletons = get_all_skeletons()
    
    generated_paths = {}
    for char, skeleton in sorted(skeletons.items()):
        svg_d = expander.expand_glyph(skeleton)
        if svg_d:
            generated_paths[char] = svg_d
            n_strokes = len(skeleton.strokes)
            print(f"  '{char}' (U+{ord(char):04X}): {n_strokes} strokes -> {len(svg_d)} bytes SVG path")
        else:
            print(f"  '{char}' (U+{ord(char):04X}): FAILED - empty path")
    
    print(f"\n  Generated {len(generated_paths)} glyphs from skeletons")
    
    # Merge: master paths take priority over generated
    all_paths = {}
    for char, svg_d in generated_paths.items():
        if char in MASTER_PATHS:
            print(f"  '{char}': using MASTER (SVG wordmark) over generated")
            all_paths[char] = ('master', MASTER_PATHS[char])
        else:
            all_paths[char] = ('generated', svg_d)
    
    # Add master paths that have no skeleton
    for char, svg_d in MASTER_PATHS.items():
        if char not in all_paths:
            all_paths[char] = ('master', svg_d)
    
    master_count = sum(1 for src, _ in all_paths.values() if src == 'master')
    gen_count = sum(1 for src, _ in all_paths.values() if src == 'generated')
    print(f"\n  Total: {len(all_paths)} glyphs ({master_count} master + {gen_count} generated)")
    
    # Phase 2: Compile into all font variants
    print("\n[Phase 2] Compiling into font variants...")
    
    ttf_files = sorted(f for f in os.listdir(FONT_DIR) if f.endswith('.ttf'))
    
    for filename in ttf_files:
        filepath = os.path.join(FONT_DIR, filename)
        font = TTFont(filepath)
        
        glyf_table = font['glyf']
        hmtx_metrics = font['hmtx'].metrics
        
        compiled = 0
        failed = 0
        
        for char, (source, svg_d) in sorted(all_paths.items()):
            try:
                bounds = get_svg_bounds(svg_d)
                if bounds is None:
                    failed += 1
                    continue
                
                glyph, aw, lsb = compile_svg_glyph(font, svg_d, bounds)
                
                # Verify glyph has valid contours
                if glyph.numberOfContours == 0:
                    failed += 1
                    continue
                
                glyf_table[char] = glyph
                hmtx_metrics[char] = (aw, lsb)
                compiled += 1
                
            except Exception as ex:
                print(f"    ERROR '{char}': {ex}")
                failed += 1
        
        # Freeze timestamps
        font['head'].created = 0
        font['head'].modified = 0
        font['head'].fontRevision = 2.0
        
        # Save
        tmp = filepath + '.tmp'
        font.save(tmp)
        font.close()
        
        os.chmod(filepath, 0o666)
        os.remove(filepath)
        os.rename(tmp, filepath)
        
        # Copy to main app & brand fonts
        app_path = os.path.join(APP_FONT_DIR, filename)
        brand_path = os.path.join(BRAND_FONT_DIR, filename)
        if os.path.exists(app_path):
            os.chmod(app_path, 0o666)
        shutil.copy2(filepath, app_path)
        os.makedirs(BRAND_FONT_DIR, exist_ok=True)
        shutil.copy2(filepath, brand_path)
        
        with open(filepath, 'rb') as f:
            sha = hashlib.sha256(f.read()).hexdigest()[:24]
        
        print(f"  {filename}: {compiled} compiled, {failed} failed, SHA={sha}...")
    
    print(f"\n{'='*60}")
    print("TYPE DESIGNER AGENT COMPLETE")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
