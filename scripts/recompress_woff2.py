#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIRS = [
    ROOT_DIR / "fonts" / "woff2",
    ROOT_DIR.parent / "pocketgull" / "public" / "fonts",
]

stems = [
    "PocketGull-Regular",
    "PocketGull-Bold",
    "PocketGull-Black",
    "PocketGull-BoldItalic",
    "PocketGull-Fineliner",
    "PocketGull-Italic",
    "PocketGull-Chiseltip",
    "PocketGull-MarkerRaw",
    "PocketGull-CondensedBold",
    "PocketGull-Micro",
    "PocketGull-Soft",
    "PocketGullMono-Regular",
    "PocketGullMono-Bold",
    "PocketGullMono-Italic",
    "PocketGull-VF",
]

for stem in stems:
    src = TTF_DIR / f"{stem}.ttf"
    if src.is_file():
        for woff2_dir in WOFF2_DIRS:
            if woff2_dir.exists():
                dst = woff2_dir / f"{stem}.woff2"
                compress(str(src), str(dst))
                print(f"  • {stem}.woff2 -> {dst} ({dst.stat().st_size} bytes)")
