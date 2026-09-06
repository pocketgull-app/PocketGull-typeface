name: "Pocket Gull"
designer: "Phil Gear"
license: "OFL"
category: "SANS_SERIF"
date_added: "2026-08-04"
fonts {
  name: "Pocket Gull"
  style: "normal"
  weight: 400
  filename: "PocketGull-Regular.ttf"
  post_script_name: "PocketGull-Regular"
  full_name: "Pocket Gull Regular"
  copyright: "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-typeface)"
}
fonts {
  name: "Pocket Gull"
  style: "normal"
  weight: 700
  filename: "PocketGull-Bold.ttf"
  post_script_name: "PocketGull-Bold"
  full_name: "Pocket Gull Bold"
  copyright: "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-typeface)"
}
fonts {
  name: "Pocket Gull"
  style: "normal"
  weight: 900
  filename: "PocketGull-Black.ttf"
  post_script_name: "PocketGull-Black"
  full_name: "Pocket Gull Black"
  copyright: "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-typeface)"
}
subsets: "cyrillic"
subsets: "cyrillic-ext"
subsets: "greek"
subsets: "greek-ext"
subsets: "latin"
subsets: "latin-ext"
subsets: "vietnamese"
subsets: "menu"
primary_script: "Latn"
stroke: "SANS_SERIF"
classifications: "SANS_SERIF"
classifications: "DISPLAY"
minisite_url: "https://pocketgull.app"
source {
  repository_url: "https://github.com/pocketgull-app/pocketgull-typeface"
  branch: "main"
}

# ── KNOWN LIMITATIONS (Reviewed and Intentional) ─────────────────────────────
#
# 1. Variable Font Coverage Gap
#    PocketGull-VF.ttf covers 5,111 glyphs (Latin + Braille + Duployan axis).
#    Static instances cover 13,739 glyphs (additionally: UCAS/Inuktitut,
#    Tifinagh, Cherokee, Ethiopic, Adlam, Vai, Arabic base codepoints).
#    Full VF axis interpolation for all scripts is deferred to v4.0.
#    GF Onboarding: VF is submitted as Latin + Braille + Duployan only.
#
# 2. Arabic Script — No Cursive Shaping
#    Arabic base codepoints (U+0600–U+06FF) are present in cmap for isolated
#    rendering contexts. Arabic cursive shaping (init/medi/fina/isol positional
#    variants via GSUB LookupType 6) is NOT implemented.
#    Arabic Presentation Forms (U+FB50–U+FDFF, U+FE70–U+FEFF) have been
#    removed per Unicode deprecation advisory (deprecated block, pre-Unicode
#    Presentation Forms approach). Arabic/Farsi text should use Noto Sans Arabic.
#
# 3. CJK — No Coverage
#    CJK Unified Ideographs, Hiragana, Katakana, Hangul are not covered.
#    PocketGull is a Latin + Indigenous Scripts superfamily. CJK rendering
#    in clinical environments should use Noto Sans CJK or system fonts.
#
# ─────────────────────────────────────────────────────────────────────────────
