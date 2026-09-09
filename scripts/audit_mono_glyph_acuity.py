#!/usr/bin/env python3
"""
PocketGull Typefoundry: Forensic Monospace Acuity & Optical Height Auditor
=========================================================================
Audits PocketGullMono glyph heights against proportional counterparts,
flagging any non-Latin / Indigenous letters that suffer from naive
isotropic downscaling (h < 500 UPM) violating Invariant Pillar 8.
"""

from pathlib import Path
import sys
import unicodedata
from fontTools.ttLib import TTFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

def audit_mono(mono_name, prop_name):
    mono_path = TTF_DIR / mono_name
    prop_path = TTF_DIR / prop_name
    
    mono_font = TTFont(mono_path)
    prop_font = TTFont(prop_path)
    
    mono_glyf = mono_font['glyf']
    mono_cmap = mono_font.getBestCmap()
    prop_glyf = prop_font['glyf']
    prop_cmap = prop_font.getBestCmap()
    
    flagged = []
    
    for cp, gname in sorted(mono_cmap.items()):
        if cp not in prop_cmap:
            continue
            
        char = chr(cp)
        cat = unicodedata.category(char)
        # Focus on Letters and letter-like numbers
        if not cat.startswith(('L', 'N')):
            continue
            
        # Skip small modifiers, superscripts, subscripts, phonetic modifiers
        name = unicodedata.name(char, '')
        if 'MODIFIER' in name or 'SUPER' in name or 'SUBSCRIPT' in name or 'SMALL' in name:
            continue
        if 0x02B0 <= cp <= 0x02FF or 0x1D00 <= cp <= 0x1DBF or 0x2070 <= cp <= 0x209F:
            continue
            
        mg = mono_glyf[gname]
        pg = prop_glyf[prop_cmap[cp]]
        
        if mg.numberOfContours <= 0 or pg.numberOfContours <= 0:
            continue
            
        m_coords = list(mg.coordinates)
        p_coords = list(pg.coordinates)
        
        m_ys = [pt[1] for pt in m_coords]
        p_ys = [pt[1] for pt in p_coords]
        
        m_h = max(m_ys) - min(m_ys)
        p_h = max(p_ys) - min(p_ys)
        
        # If proportional master is substantial (h >= 540 UPM, e.g. cap-height or full x-height)
        # but monospace cut has shrunken to h < 500 UPM
        if p_h >= 540 and m_h < 480:
            ratio = m_h / p_h
            flagged.append({
                'cp': cp,
                'char': char,
                'name': name,
                'gname': gname,
                'mono_h': m_h,
                'prop_h': p_h,
                'ratio': ratio,
            })
            
    mono_font.close()
    prop_font.close()
    return flagged

if __name__ == "__main__":
    flagged = audit_mono("PocketGullMono-Regular.ttf", "PocketGull-Regular.ttf")
    print(f"=== MONOSPACE OPTICAL HEIGHT FORENSIC AUDIT ===")
    print(f"Total letters/numerics audited in PocketGullMono-Regular.ttf")
    print(f"Flagged abnormally shrunken glyphs (mono_h < 480 UPM while prop_h >= 540 UPM): {len(flagged)}\n")
    
    # Group by Unicode Block
    blocks = {}
    for item in flagged:
        cp = item['cp']
        b = f"U+{(cp >> 8):02X}xx"
        if b not in blocks:
            blocks[b] = []
        blocks[b].append(item)
        
    for b, items in sorted(blocks.items()):
        print(f"--- Block {b} ({len(items)} glyphs) ---")
        for it in items[:6]:
            print(f"  U+{it['cp']:04X} ({it['char']}) {it['name'][:35]:35s} | Mono: {it['mono_h']:3d} UPM vs Prop: {it['prop_h']:3d} UPM (Ratio: {it['ratio']:.2f})")
        if len(items) > 6:
            print(f"  ... and {len(items) - 6} more in this block")
