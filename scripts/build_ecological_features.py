#!/usr/bin/env python3
import sys, os
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._f_v_a_r import Axis, NamedInstance
from fontTools.ttLib.tables import otTables as ot

def add_name(font, text, preferred_id=None):
    name_table = font['name']
    max_id = max([r.nameID for r in name_table.names] + [256])
    target_id = preferred_id if (preferred_id and preferred_id > max_id) else (max_id + 1)
    for r in name_table.names:
        if r.toUnicode() == text:
            return r.nameID
    name_table.setName(text, target_id, 3, 1, 0x409)
    name_table.setName(text, target_id, 1, 0, 0)
    return target_id

def augment_variable_font(vf_path):
    print(f'• Augmenting Variable Font: {vf_path}')
    font = TTFont(vf_path)
    if 'fvar' not in font:
        return
    fvar = font['fvar']
    existing_tags = [a.axisTag for a in fvar.axes]
    if 'CARB' not in existing_tags:
        carb_id = add_name(font, 'Carbon Intensity')
        ax = Axis()
        ax.axisTag = 'CARB'
        ax.minValue = 0.0
        ax.defaultValue = 0.0
        ax.maxValue = 100.0
        ax.flags = 0
        ax.axisNameID = carb_id
        fvar.axes.append(ax)
        print('  [OK] Added axis CARB: 0.0 -> 100.0 (Carbon Intensity)')
    if 'ALBD' not in existing_tags:
        albd_id = add_name(font, 'Solar Albedo')
        ax = Axis()
        ax.axisTag = 'ALBD'
        ax.minValue = 0.0
        ax.defaultValue = 0.0
        ax.maxValue = 100.0
        ax.flags = 0
        ax.axisNameID = albd_id
        fvar.axes.append(ax)
        print('  [OK] Added axis ALBD: 0.0 -> 100.0 (Solar Albedo)')

    # Ensure all existing instances have CARB and ALBD coordinates
    for inst in fvar.instances:
        if 'CARB' not in inst.coordinates:
            inst.coordinates['CARB'] = 0.0
        if 'ALBD' not in inst.coordinates:
            inst.coordinates['ALBD'] = 0.0

    inst_names = [font['name'].getDebugName(inst.subfamilyNameID) for inst in fvar.instances]
    if 'Zero-Carbon Solar Sanctuary' not in inst_names:
        inst_id = add_name(font, 'Zero-Carbon Solar Sanctuary')
        inst = NamedInstance()
        inst.subfamilyNameID = inst_id
        inst.flags = 0
        inst.coordinates = dict(fvar.instances[0].coordinates)
        inst.coordinates['wght'] = 500.0
        inst.coordinates['CARB'] = 0.0
        inst.coordinates['ALBD'] = 100.0
        fvar.instances.append(inst)
        print('  [OK] Added instance: Zero-Carbon Solar Sanctuary')

    if 'High-Grid Fossil Peak (Ultra-Lean)' not in inst_names:
        inst_id = add_name(font, 'High-Grid Fossil Peak (Ultra-Lean)')
        inst = NamedInstance()
        inst.subfamilyNameID = inst_id
        inst.flags = 0
        inst.coordinates = dict(fvar.instances[0].coordinates)
        inst.coordinates['wght'] = 400.0
        inst.coordinates['CARB'] = 100.0
        inst.coordinates['ALBD'] = 0.0
        fvar.instances.append(inst)
        print('  [OK] Added instance: High-Grid Fossil Peak (Ultra-Lean)')

    font.save(vf_path)
    print(f'  [SAVED] {vf_path} updated.')

def augment_gsub_features(font_path):
    print(f'• Augmenting GSUB features: {font_path}')
    font = TTFont(font_path)
    if 'GSUB' not in font:
        return
    gsub = font['GSUB'].table
    existing_feats = [r.FeatureTag for r in gsub.FeatureList.FeatureRecord]
    eco_features = {
        'ss01': 'Regenerative Ink-Saving Spore Traps',
        'ss12': 'Wildlife Sanctuary Dark Canopy',
        'ss15': 'Slow Typography Cognitive De-Escalation',
    }
    for tag, desc in eco_features.items():
        if tag not in existing_feats:
            feature_rec = ot.FeatureRecord()
            feature_rec.FeatureTag = tag
            feature = ot.Feature()
            feature.FeatureParams = None
            feature.LookupListIndex = []
            feature_rec.Feature = feature
            gsub.FeatureList.FeatureRecord.append(feature_rec)
            gsub.FeatureList.FeatureCount = len(gsub.FeatureList.FeatureRecord)
            print(f'  [OK] Registered GSUB feature {tag}: {desc}')
    font.save(font_path)
    print(f'  [SAVED] {font_path} updated.')

vf_target = os.path.join('fonts', 'ttf', 'PocketGull-VF.ttf')
if os.path.exists(vf_target):
    augment_variable_font(vf_target)
    augment_gsub_features(vf_target)

for style in ['Bold', 'Regular', 'Fineliner']:
    target = os.path.join('fonts', 'ttf', f'PocketGull-{style}.ttf')
    if os.path.exists(target):
        augment_gsub_features(target)

print('[DONE] Ecological features successfully compiled.')
