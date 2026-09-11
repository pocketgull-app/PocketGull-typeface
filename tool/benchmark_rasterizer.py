import time
import string
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONTS = {
    "PocketGull Fineliner (Unhinted Direct Curve)": r"c:\Users\philg\Pocketgull\pocketgull-typeface\fonts\ttf\PocketGull-Fineliner.ttf",
    "PocketGull Bold (Unhinted Direct Curve)": r"c:\Users\philg\Pocketgull\pocketgull-typeface\fonts\ttf\PocketGull-Bold.ttf",
    "PocketGull Mono (Fixed 600 UPM Telemetry)": r"c:\Users\philg\Pocketgull\pocketgull-typeface\fonts\ttf\PocketGullMono-Regular.ttf",
    "Arial (Hinted Bytecode VM)": r"C:\Windows\Fonts\arial.ttf",
    "Calibri (Hinted Bytecode VM)": r"C:\Windows\Fonts\calibri.ttf",
    "Times New Roman (Hinted Bytecode VM)": r"C:\Windows\Fonts\times.ttf",
    "Segoe UI (Hinted Bytecode VM)": r"C:\Windows\Fonts\segoeui.ttf",
}

# Clinical corpus representing real-world EHR telemetry and pharmacy labels
CORPUS = (
    "Vitals Restored: Peaceful Sinus Rhythm 72 bpm • Amoxicillin 500 mg Completed • BP 120/80 mmHg. "
    "Active RX: Cefazolin 2 g IV Q8H • 18G Cannula Right Antecubital • ALLERGY: PENICILLIN. "
    "Bedside Telemetry HUD: [HR: 72] [SpO2: 99%] [MAP: 93] [ETCO2: 38 mmHg] [GCS: 15]. "
    "Restorative Care Directive: Hydration & Rest • Full Strength Returning • Safe Discharge Confirmed."
)

SIZES = [14, 24, 48]
ITERATIONS = 200

def benchmark():
    print("=" * 78)
    print("  POCKETGULL SCIENTIFIC FONT BENCHMARK: RASTERIZATION THROUGHPUT & LATENCY")
    print("=" * 78)
    print(f"Corpus: {len(CORPUS)} characters per iteration x {ITERATIONS} iterations = {len(CORPUS) * ITERATIONS:,} glyphs per test\n")
    
    results = {}
    
    for label, path_str in FONTS.items():
        p = Path(path_str)
        if not p.exists():
            continue
            
        font_results = {}
        for size in SIZES:
            font = ImageFont.truetype(str(p), size)
            img = Image.new('L', (1200, 300), 0)
            draw = ImageDraw.Draw(img)
            
            # Warm-up run
            for _ in range(5):
                draw.text((10, 10), CORPUS[:50], font=font, fill=255)
                
            # Timed run
            t0 = time.perf_counter()
            for _ in range(ITERATIONS):
                draw.text((10, 10), CORPUS, font=font, fill=255)
            t1 = time.perf_counter()
            
            elapsed = t1 - t0
            total_glyphs = len(CORPUS) * ITERATIONS
            glyphs_per_sec = total_glyphs / elapsed
            microsec_per_glyph = (elapsed / total_glyphs) * 1_000_000
            
            font_results[size] = (glyphs_per_sec, microsec_per_glyph, elapsed)
            
        results[label] = font_results

    # Print summary table
    print(f"{'Font Family':44s} | {'Size':5s} | {'Throughput (glyphs/sec)':24s} | {'Latency/Glyph':14s}")
    print("-" * 92)
    for label, size_data in results.items():
        for size, (gps, us, el) in size_data.items():
            print(f"{label:44s} | {size:2d} pt | {gps:18,.0f} glyphs/s  | {us:7.2f} µs/glyph")
        print("-" * 92)

if __name__ == "__main__":
    benchmark()
