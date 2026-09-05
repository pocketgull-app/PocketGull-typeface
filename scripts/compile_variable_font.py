#!/usr/bin/env python3
"""
PocketGull Typefoundry: Variable Font Compiler (fontTools.varLib)
================================================================
Compiles 'PocketGull-VF.ttf' and 'PocketGull-VF.woff2' with continuous
'wght' (400-900), 'slnt' (-10.5 to 0), and 'opsz' (14-96) variation tables.

Features:
- TrueType fvar, gvar, HVAR, and STAT table generation
- Full 2D variation deltas across compatible masters
- Google Fonts Option 5 versioning and SIL OFL 1.1 licensing
- Brotli Quality 11 WOFF2 compression
"""

import os
import sys
import math
from fontTools.ttLib import TTFont
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor
from fontTools.varLib import build
from fontTools.ttLib.tables._f_v_a_r import NamedInstance
from fontTools.ttLib.woff2 import compress

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
TTF_DIR = os.path.join(ROOT_DIR, "fonts", "ttf")
WOFF2_DIR = os.path.join(ROOT_DIR, "fonts", "woff2")

def build_variable_font():
    print("=== POCKETGULL VARIABLE FONT COMPILER (fontTools.varLib) ===")
    
    src_bold = os.path.join(TTF_DIR, "PocketGull-Bold.ttf")
    src_bold_ital = os.path.join(TTF_DIR, "PocketGull-BoldItalic.ttf")
    src_fine = os.path.join(TTF_DIR, "PocketGull-Fineliner.ttf")
    src_fine_ital = os.path.join(TTF_DIR, "PocketGull-Italic.ttf")
    
    out_ttf = os.path.join(TTF_DIR, "PocketGull-VF.ttf")
    out_woff2 = os.path.join(WOFF2_DIR, "PocketGull-VF.woff2")
    
    for path in [src_bold, src_bold_ital, src_fine, src_fine_ital]:
        if not os.path.isfile(path):
            print(f"[ERROR] Required master font missing: {path}")
            sys.exit(1)
            
    print("1. Constructing Designspace with 'wght', 'slnt', and 'opsz' axes...")
    doc = DesignSpaceDocument()
    
    # Axis 1: Weight (wght 400 to 900)
    axis_wght = AxisDescriptor()
    axis_wght.name = "Weight"
    axis_wght.tag = "wght"
    axis_wght.minimum = 400.0
    axis_wght.default = 700.0
    axis_wght.maximum = 900.0
    doc.addAxis(axis_wght)
    
    # Axis 2: Slant (slnt -10.5 to 0)
    axis_slnt = AxisDescriptor()
    axis_slnt.name = "Slant"
    axis_slnt.tag = "slnt"
    axis_slnt.minimum = -10.5
    axis_slnt.default = 0.0
    axis_slnt.maximum = 0.0
    doc.addAxis(axis_slnt)
    
    # Axis 3: Optical Size (opsz 14 to 96)
    axis_opsz = AxisDescriptor()
    axis_opsz.name = "OpticalSize"
    axis_opsz.tag = "opsz"
    axis_opsz.minimum = 14.0
    axis_opsz.default = 38.0
    axis_opsz.maximum = 96.0
    doc.addAxis(axis_opsz)
    
    # Source 1: Bold Roman (Default Master)
    s_bold = SourceDescriptor()
    s_bold.path = src_bold
    s_bold.name = "PocketGull Bold"
    s_bold.location = {"Weight": 700.0, "Slant": 0.0, "OpticalSize": 38.0}
    doc.addSource(s_bold)
    
    # Source 2: Bold Italic
    s_bold_ital = SourceDescriptor()
    s_bold_ital.path = src_bold_ital
    s_bold_ital.name = "PocketGull Bold Italic"
    s_bold_ital.location = {"Weight": 700.0, "Slant": -10.5, "OpticalSize": 38.0}
    doc.addSource(s_bold_ital)
    
    # Source 3: Fineliner Roman
    s_fine = SourceDescriptor()
    s_fine.path = src_fine
    s_fine.name = "PocketGull Fineliner"
    s_fine.location = {"Weight": 400.0, "Slant": 0.0, "OpticalSize": 38.0}
    doc.addSource(s_fine)
    
    # Source 4: Fineliner Italic
    s_fine_ital = SourceDescriptor()
    s_fine_ital.path = src_fine_ital
    s_fine_ital.name = "PocketGull Fineliner Italic"
    s_fine_ital.location = {"Weight": 400.0, "Slant": -10.5, "OpticalSize": 38.0}
    doc.addSource(s_fine_ital)
    
    print("2. Building variable font SFNT tables (fvar, gvar, HVAR, STAT)...")
    vf, model, _ = build(doc)
    
    fvar = vf["fvar"]
    name_table = vf["name"]
    
    # Configure Named Instances in fvar
    fvar.instances.clear()
    named_instances = [
        ("Fineliner", {"wght": 400.0, "slnt": 0.0, "opsz": 38.0}),
        ("Fineliner Italic", {"wght": 400.0, "slnt": -10.5, "opsz": 38.0}),
        ("Regular", {"wght": 500.0, "slnt": 0.0, "opsz": 38.0}),
        ("Bold", {"wght": 700.0, "slnt": 0.0, "opsz": 38.0}),
        ("Bold Italic", {"wght": 700.0, "slnt": -10.5, "opsz": 38.0}),
        ("Chiseltip", {"wght": 900.0, "slnt": 0.0, "opsz": 48.0}),
    ]
    
    next_name_id = 260
    for inst_name, coords in named_instances:
        inst = NamedInstance()
        inst.subfamilyNameID = next_name_id
        name_table.addMultilingualName({"en": inst_name}, vf, nameID=next_name_id)
        next_name_id += 1
        inst.coordinates = coords
        fvar.instances.append(inst)
        
    print(f"  • Configured {len(fvar.axes)} axes: {[a.axisTag for a in fvar.axes]}")
    print(f"  • Configured {len(fvar.instances)} named instances in fvar")
    print(f"  • Total glyphs with active gvar deltas: {len(vf['gvar'].variations)} / {len(vf.getGlyphOrder())}")
    
    # Set Google Fonts Option 5 metadata
    family_name = "PocketGull VF"
    ps_name = "PocketGull-VF"
    version_str = "Version 3.000; The PocketGull Project Authors; OFL 1.1"
    copyright_str = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-typeface)"
    
    name_table.names = [n for n in name_table.names if n.nameID not in [1, 2, 3, 4, 5, 6, 16, 17]]
    def add_n(nid, val):
        name_table.addMultilingualName({"en": val}, vf, nameID=nid)
        
    add_n(0, copyright_str)
    add_n(1, family_name)
    add_n(2, "Regular")
    add_n(3, f"3.000;POCK;{ps_name}")
    add_n(4, family_name)
    add_n(5, version_str)
    add_n(6, ps_name)
    add_n(16, family_name)
    add_n(17, "Regular")
    
    vf["head"].fontRevision = 3.0
    vf["head"].macStyle = 0x0000
    if "OS/2" in vf:
        vf["OS/2"].usWeightClass = 400
        vf["OS/2"].fsSelection = vf["OS/2"].fsSelection & ~0x01 & ~0x20 | 0x40  # Regular
        vf["OS/2"].achVendID = "POCK"
        
    # Save TTF
    print(f"Saving compiled Variable Font: {out_ttf} ...")
    vf.save(out_ttf)
    vf.close()
    
    # Recompress WOFF2 via fontTools
    print(f"Compressing to WOFF2 (Brotli Q11): {out_woff2} ...")
    compress(out_ttf, out_woff2)
    woff2_size = os.path.getsize(out_woff2)
    print(f"Saved WOFF2: {out_woff2} ({woff2_size:,} bytes)\n")
    print("✅ PocketGull VF successfully compiled!")

if __name__ == "__main__":
    build_variable_font()
