# PocketGull Typefoundry Master 1-Click Build & Synchronization Pipeline
# Recompiles all 7 font variants, injects OpenType kerning, compiles variable tables,
# builds the PocketGull World Pan-Script codex, generates WOFF2, and syncs assets.

[CmdletBinding()]
param (
    [switch]$SkipAudit,
    [switch]$SkipSync
)

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  POCKETGULL TYPEFOUNDRY: MASTER BUILD PIPELINE (PowerShell)" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TypefaceRoot = Split-Path -Parent $ScriptDir
$PocketgullRoot = "C:\Users\philg\Pocketgull\pocketgull"
$BrandFontsDir = Join-Path $PocketgullRoot "public\brand\fonts"
$PublicFontsDir = Join-Path $PocketgullRoot "public\fonts"

# Step 1: Recompile Precision Superfamily
Write-Host "`n[1/5] Compiling Precision Vector Superfamily 1024 UPM..." -ForegroundColor Yellow
wsl -d Ubuntu -- bash -c "~/.local/bin/uv run --with fonttools --with brotli python3 /mnt/c/Users/philg/Pocketgull/pocketgull-typeface/scripts/compile_precision_superfamily.py"

# Step 2: Build Sacred Numerology & Telemetry Font
Write-Host "`n[2/5] Building Sacred Numerology and Telemetry Font..." -ForegroundColor Yellow
wsl -d Ubuntu -- bash -c "~/.local/bin/uv run --with fonttools --with brotli python3 /mnt/c/Users/philg/Pocketgull/pocketgull-typeface/scripts/build_numerology_font.py"

# Step 3: Inject OpenType GPOS Class-Kerning & GSUB Disambiguation
Write-Host "`n[3/5] Injecting OpenType GPOS Kerning and GSUB Features..." -ForegroundColor Yellow
wsl -d Ubuntu -- bash -c "~/.local/bin/uv run --with fonttools python3 /mnt/c/Users/philg/Pocketgull/pocketgull-typeface/scripts/apply_type_best_practices.py"

# Step 4: Compile PocketGull World Pan-Script & Biophysical Codex
Write-Host "`n[4/5] Compiling PocketGull World Pan-Script Extension..." -ForegroundColor Yellow
wsl -d Ubuntu -- bash -c "~/.local/bin/uv run --with fonttools --with brotli python3 /mnt/c/Users/philg/Pocketgull/pocketgull-typeface/scripts/build_pocketgull_world.py"

# Step 5: Run Unicode CMAP Audit & Quaker Quality Inspector
if (-not $SkipAudit) {
    Write-Host "`n[5/5] Running Unicode CMAP Audit and Quaker Quality Inspection..." -ForegroundColor Yellow
    wsl -d Ubuntu -- bash -c "~/.local/bin/uv run --with fonttools python3 /mnt/c/Users/philg/Pocketgull/pocketgull-typeface/scripts/audit_unicode_cmap.py"
    wsl -d Ubuntu -- bash -c "~/.local/bin/uv run --with fonttools python3 /mnt/c/Users/philg/Pocketgull/pocketgull-typeface/scripts/quaker_quality_inspector.py"
}

# Step 6: Synchronize Binaries to Web Application & Brand Kit
if (-not $SkipSync) {
    Write-Host "`nSynchronizing Font Binaries and Assets to Web Application..." -ForegroundColor Green
    
    $FontFiles = Get-ChildItem -Path $TypefaceRoot -Filter "*.ttf" -File
    $Woff2Files = Get-ChildItem -Path $TypefaceRoot -Filter "*.woff2" -File
    $AllFonts = $FontFiles + $Woff2Files

    foreach ($Dest in @($BrandFontsDir, $PublicFontsDir)) {
        if (Test-Path $Dest) {
            foreach ($Font in $AllFonts) {
                Copy-Item -Path $Font.FullName -Destination (Join-Path $Dest $Font.Name) -Force
            }
            Write-Host "  [OK] Synchronized $($AllFonts.Count) font files to $Dest" -ForegroundColor DarkGreen
        }
    }
}

Write-Host "`n=================================================================" -ForegroundColor Cyan
Write-Host "  POCKETGULL MASTER BUILD COMPLETE: ALL FONTS 100% READY!" -ForegroundColor Cyan
Write-Host "=================================================================`n" -ForegroundColor Cyan
