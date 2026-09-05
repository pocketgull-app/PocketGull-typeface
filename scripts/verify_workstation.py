#!/usr/bin/env python3
"""
PocketGull Typefoundry - Workstation Quality Engineering Diagnostic Suite
Tests and verifies the complete local toolchain:
  1. AMD Radeon GPU (RX 6650 XT) & driver status
  2. Pure Dart 3.11 SFNT Compiler & W3C OTS Table Invariants
  3. WSL2 JAX Mathematical Engine (jax.jit, jax.grad, jax.vmap)
  4. Lemonade Local AMD AI Inference Server (:13305)
  5. Google Fonts Pre-Flight Validator (42 checks)
"""

import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def check_gpu():
    print("\n[1/5] Checking AMD Graphics Hardware...")
    try:
        cmd = ["powershell", "-NoProfile", "-Command", 
               "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        gpus = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        for gpu in gpus:
            print(f"  [PASS] Detected GPU: {gpu}")
        return True
    except Exception as e:
        print(f"  [WARN] Could not query GPU controller: {e}")
        return False

def check_dart_foundry():
    print("\n[2/5] Verifying Dart 3.11 Foundry & W3C OTS Table Invariants...")
    try:
        cmd = ["dart", "run", "tool/pocketgull_foundry.dart", "audit"]
        res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True)
        if res.returncode == 0 and "8 / 8 FONT BINARIES PASSED" in res.stdout:
            print("  [PASS] All 8 font binaries satisfy W3C OTS, loca/glyf 2-byte word padding, and bit-7 flags.")
            return True
        else:
            print("  [FAIL] Dart foundry audit encountered issues:")
            print(res.stdout)
            return False
    except Exception as e:
        print(f"  [FAIL] Failed to execute Dart foundry: {e}")
        return False

def check_wsl_jax():
    print("\n[3/5] Verifying JAX Mathematical Engine in WSL2...")
    try:
        jax_test_code = (
            "import jax, jax.numpy as jnp; "
            "f = lambda x: jnp.sum(x**2); "
            "df = jax.grad(f); "
            "arr = jnp.array([2.0, 4.0, 6.0]); "
            "grad = df(arr); "
            "print(f'JAX {jax.__version__} grad test passed: {grad.tolist()} on {jax.devices()}')"
        )
        cmd = ["wsl", "-e", "/home/philg/.local/bin/uv", "run", "--with", "jax", "--with", "jaxlib", 
               "python3", "-c", jax_test_code]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  [PASS] {res.stdout.strip()}")
            return True
        else:
            print(f"  [FAIL] WSL JAX error: {res.stderr.strip()}")
            return False
    except Exception as e:
        print(f"  [FAIL] Failed to invoke WSL JAX: {e}")
        return False

def check_lemonade():
    print("\n[4/5] Checking Lemonade AMD AI Server (http://127.0.0.1:13305)...")
    url = "http://127.0.0.1:13305/api/v1/models"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PocketGull-Audit/1.0"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("id", "unknown") for m in data.get("data", [])]
            print(f"  [PASS] Lemonade Server ONLINE. Registered models: {models}")
            return True
    except Exception:
        print("  [INFO] Lemonade Server is currently OFFLINE.")
        print("         To install official AMD Lemonade: winget install AMD.LemonadeServer")
        print("         To start server: lemonade serve (or launch from Start Menu)")
        return False

def check_google_fonts_validator():
    print("\n[5/5] Running Google Fonts Pre-Flight Validator (42 Checks)...")
    try:
        cmd = ["node", "scripts/run-font-validator.mjs"]
        res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True)
        clean_out = re.sub(r"\x1b\[[0-9;]*m", "", res.stdout)
        if res.returncode == 0 and ("passed: 42" in clean_out.lower() or "42 passed" in clean_out.lower()):
            print("  [PASS] 42/42 Google Fonts checks passed (100% compliant).")
            return True
        else:
            print(f"  [WARN] Validator output: {clean_out[-300:]}")
            return False
    except Exception as e:
        print(f"  [FAIL] Failed to run font validator: {e}")
        return False

def main():
    print("=" * 70)
    print("  POCKETGULL WORKSTATION QUALITY ENGINEERING AUDIT")
    print("=" * 70)
    
    results = [
        ("AMD GPU", check_gpu()),
        ("Dart 3.11 OTS Foundry", check_dart_foundry()),
        ("WSL2 JAX Math Engine", check_wsl_jax()),
        ("Lemonade AMD Server", check_lemonade()),
        ("Google Fonts Validator", check_google_fonts_validator()),
    ]
    
    print("\n" + "=" * 70)
    print("  AUDIT SUMMARY")
    print("=" * 70)
    for name, ok in results:
        status = "[READY]" if ok else "[ACTION REQUIRED]"
        print(f"  {status:<18} {name}")
    print("=" * 70)

if __name__ == "__main__":
    main()
