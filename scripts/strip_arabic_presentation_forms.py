#!/usr/bin/env python3
"""
strip_arabic_presentation_forms.py
====================================
PocketGull GF Remediation -- Blocker 1 Fix
==========================================
Removes the deprecated Arabic Presentation Forms approach from PocketGull:

1. Strips all Arabic Presentation Forms codepoints from cmap:
   - U+FB50-U+FDFF  (Arabic Presentation Forms-A)
   - U+FE70-U+FEFF  (Arabic Presentation Forms-B)

2. Removes the 'arab' GSUB script record and all associated lookups.

3. Removes orphaned Presentation Forms glyph records from glyf/loca/GlyphOrder.

4. Retains Arabic BASE codepoints (U+0600-U+06FF) in cmap so isolated
   rendering remains possible -- but no shaping features fire.

DrvFS-safe: uses lazy=False + atomic temp-file saves (os.replace).
"""

import os
import sys

from fontTools.ttLib import TTFont

TARGET_FONTS = [
    "fonts/ttf/PocketGull-Bold.ttf",
    "fonts/ttf/PocketGull-Fineliner.ttf",
    "fonts/ttf/PocketGull-Chiseltip.ttf",
]

PRES_FORMS_RANGES = [
    (0xFB50, 0xFDFF),
    (0xFE70, 0xFEFF),
]

ARABIC_BASE_LO = 0x0600
ARABIC_BASE_HI = 0x06FF


def is_pres_forms(cp):
    return any(lo <= cp <= hi for lo, hi in PRES_FORMS_RANGES)


def collect_orphan_pres_glyphs(cmap):
    pres_names = set()
    base_names = set()
    for cp, name in cmap.items():
        if is_pres_forms(cp):
            pres_names.add(name)
        else:
            base_names.add(name)
    return pres_names - base_names


def strip_pres_forms_from_cmap(font):
    removed = 0
    for subtable in font["cmap"].tables:
        if not hasattr(subtable, "cmap"):
            continue
        to_remove = [cp for cp in subtable.cmap if is_pres_forms(cp)]
        for cp in to_remove:
            del subtable.cmap[cp]
            removed += 1
    return removed


def strip_arab_gsub(font):
    gsub = font.get("GSUB")
    if not gsub:
        return 0, 0
    table = gsub.table
    sl = table.ScriptList
    fl = table.FeatureList
    ll = table.LookupList

    # Collect arab feature indices
    arab_feat_indices = set()
    new_script_records = []
    scripts_removed = 0
    for sr in sl.ScriptRecord:
        if sr.ScriptTag == "arab":
            scripts_removed += 1
            if sr.Script.DefaultLangSys:
                arab_feat_indices.update(sr.Script.DefaultLangSys.FeatureIndex)
            for ls in sr.Script.LangSysRecord:
                arab_feat_indices.update(ls.LangSys.FeatureIndex)
        else:
            new_script_records.append(sr)

    if not scripts_removed:
        return 0, 0
    sl.ScriptRecord = new_script_records

    # Arab lookup indices
    arab_lk = set()
    for fi in arab_feat_indices:
        arab_lk.update(fl.FeatureRecord[fi].Feature.LookupListIndex)

    # Lookup indices used by non-arab features
    used_elsewhere = set()
    for i, fr in enumerate(fl.FeatureRecord):
        if i not in arab_feat_indices:
            used_elsewhere.update(fr.Feature.LookupListIndex)

    # Remove arab-only lookups (highest index first)
    to_remove = sorted(arab_lk - used_elsewhere, reverse=True)
    for idx in to_remove:
        if idx < len(ll.Lookup):
            del ll.Lookup[idx]
    lookups_removed = len(to_remove)

    # Rebuild feature list without arab features; build old->new index map
    new_feats = []
    old_to_new = {}
    for i, fr in enumerate(fl.FeatureRecord):
        if i in arab_feat_indices:
            continue
        old_to_new[i] = len(new_feats)
        new_feats.append(fr)
    fl.FeatureRecord = new_feats

    # Reindex remaining script LangSys feature references
    for sr in sl.ScriptRecord:
        if sr.Script.DefaultLangSys:
            sr.Script.DefaultLangSys.FeatureIndex = [
                old_to_new[i] for i in sr.Script.DefaultLangSys.FeatureIndex if i in old_to_new
            ]
        for ls in sr.Script.LangSysRecord:
            ls.LangSys.FeatureIndex = [
                old_to_new[i] for i in ls.LangSys.FeatureIndex if i in old_to_new
            ]

    # Reindex lookup references in remaining features
    removed_set = set(to_remove)
    lk_old_to_new = {}
    new_idx = 0
    total_old = len(ll.Lookup) + len(to_remove)
    for old in range(total_old):
        if old not in removed_set:
            lk_old_to_new[old] = new_idx
            new_idx += 1
    for fr in fl.FeatureRecord:
        fr.Feature.LookupListIndex = [
            lk_old_to_new[i] for i in fr.Feature.LookupListIndex if i in lk_old_to_new
        ]

    return scripts_removed, lookups_removed


def strip_orphan_pres_glyphs(font, orphan_names):
    if not orphan_names:
        return 0
    gorder = font.getGlyphOrder()
    font.setGlyphOrder([g for g in gorder if g not in orphan_names])
    glyf_table = font.get("glyf")
    if glyf_table:
        for name in orphan_names:
            if name in glyf_table.glyphs:
                del glyf_table.glyphs[name]
    return len(orphan_names)


def atomic_save(font, path):
    tmp = path + ".tmp"
    font.save(tmp)
    font.close()
    os.replace(tmp, path)


def process_font(path):
    print()
    print("=" * 60)
    print("Processing:", path)
    print("=" * 60)

    font = TTFont(path, lazy=False)
    cmap_before = font.getBestCmap() or {}
    pres_count = sum(1 for cp in cmap_before if is_pres_forms(cp))
    orphan_names = collect_orphan_pres_glyphs(cmap_before)
    print("  Pres Forms codepoints in cmap:", pres_count)
    print("  Orphan Pres Forms glyphs:", len(orphan_names))

    if pres_count == 0:
        print("  Nothing to strip -- skipping.")
        font.close()
        return

    removed_cps = strip_pres_forms_from_cmap(font)
    print("  Cmap: removed", removed_cps, "Pres Forms codepoints")

    sr, lr = strip_arab_gsub(font)
    print("  GSUB: removed", sr, "arab script record(s),", lr, "lookup(s)")

    gr = strip_orphan_pres_glyphs(font, orphan_names)
    print("  Glyphs: removed", gr, "orphan glyph records")

    cmap_after = font.getBestCmap() or {}
    arabic_base = sum(1 for cp in cmap_after if ARABIC_BASE_LO <= cp <= ARABIC_BASE_HI)
    pres_remain = sum(1 for cp in cmap_after if is_pres_forms(cp))
    print("  Arabic base (U+0600-06FF) retained:", arabic_base, "v")
    print("  Pres Forms remaining:", pres_remain, "(must be 0)")
    assert pres_remain == 0, "FAIL: Pres Forms still present!"

    gsub = font.get("GSUB")
    if gsub:
        for rec in gsub.table.ScriptList.ScriptRecord:
            assert rec.ScriptTag != "arab", "FAIL: arab GSUB still present!"
    print("  GSUB arab: confirmed absent v")

    atomic_save(font, path)
    print("  Saved:", path, "v")


print("PocketGull -- Arabic Presentation Forms Strip")
print("Option A: Honest scope declaration")
print("Retaining Arabic base cmap; removing Pres Forms GSUB")

for target in TARGET_FONTS:
    if not os.path.exists(target):
        print("WARNING: not found --", target)
        continue
    process_font(target)

print()
print("=" * 60)
print("COMPLETE")
print("=" * 60)
