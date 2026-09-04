// Pure Dart 3 Asset Synchronizer
import 'dart:io';

void main() async {
  final brainDir = r'C:\Users\philg\.gemini\antigravity\brain\b0cfcd5e-71a2-47af-8d62-ae8f90a0c9ab';
  final typefaceMasterDir = r'C:\Users\philg\Pocketgull\pocketgull-typeface\documentation\masterworks';
  final phototrekDestDir = r'C:\Users\philg\Dev\pgphototrek\public\images\destinations';

  final assets = [
    // Pacific Northwest Suite
    (
      'kells_pnw_vexillology_1788498347160.jpg',
      '$typefaceMasterDir\\pacific_northwest\\kells_pnw_vexillology.jpg',
      '$phototrekDestDir\\kells\\kells-dest-pacific_northwest.jpg',
      '$phototrekDestDir\\kells\\kells-dest-pacific_northwest.webp',
    ),
    (
      'pebble_pnw_biodiversity_1788498479364.jpg',
      '$typefaceMasterDir\\pacific_northwest\\pebble_pnw_biodiversity.jpg',
      '$phototrekDestDir\\pebble\\pebble-dest-pacific_northwest.jpg',
      '$phototrekDestDir\\pebble\\pebble-dest-pacific_northwest.webp',
    ),
    (
      'rubaiyat_pnw_astrolabe_1788498507859.jpg',
      '$typefaceMasterDir\\pacific_northwest\\rubaiyat_pnw_astrolabe.jpg',
      '$phototrekDestDir\\rubaiyat\\rubaiyat-dest-pacific_northwest.jpg',
      '$phototrekDestDir\\rubaiyat\\rubaiyat-dest-pacific_northwest.webp',
    ),
    // Arctic / Nunavut Suite
    (
      'kells_arctic_vexillology_1788497878064.jpg',
      '$typefaceMasterDir\\inuktitut\\kells_arctic_vexillology.jpg',
      '$phototrekDestDir\\kells\\kells-dest-arctic_nunavut.jpg',
      '$phototrekDestDir\\kells\\kells-dest-arctic_nunavut.webp',
    ),
    (
      'pebble_arctic_biodiversity_1788497897356.jpg',
      '$typefaceMasterDir\\inuktitut\\pebble_arctic_biodiversity.jpg',
      '$phototrekDestDir\\pebble\\pebble-dest-arctic_nunavut.jpg',
      '$phototrekDestDir\\pebble\\pebble-dest-arctic_nunavut.webp',
    ),
    (
      'rubaiyat_arctic_astrolabe_1788497920624.jpg',
      '$typefaceMasterDir\\inuktitut\\rubaiyat_arctic_astrolabe.jpg',
      '$phototrekDestDir\\rubaiyat\\rubaiyat-dest-arctic_nunavut.jpg',
      '$phototrekDestDir\\rubaiyat\\rubaiyat-dest-arctic_nunavut.webp',
    ),
  ];

  stdout.writeln('=== SYNCHRONIZING MASTERWORKS TO PGPHOTOTREK & TYPEFACE REPO ===\n');

  for (final (sourceName, typefaceTarget, phototrekJpg, phototrekWebp) in assets) {
    final srcFile = File('$brainDir\\$sourceName');
    if (!srcFile.existsSync()) {
      stderr.writeln('⚠️ Source missing: $sourceName');
      continue;
    }

    // 1. Copy to typeface masterworks
    final tfFile = File(typefaceTarget);
    tfFile.parent.createSync(recursive: true);
    srcFile.copySync(typefaceTarget);
    stdout.writeln('✓ Typeface Masterwork: ${tfFile.path}');

    // 2. Copy to pgphototrek JPG destination
    final ptJpg = File(phototrekJpg);
    ptJpg.parent.createSync(recursive: true);
    srcFile.copySync(phototrekJpg);
    stdout.writeln('✓ PGPhotoTrek JPG: ${ptJpg.path}');

    // 3. Convert to WebP via WSL cwebp if available, or copy
    final wslSrc = srcFile.path.replaceAll(r'C:\', '/mnt/c/').replaceAll(r'\', '/');
    final wslDst = phototrekWebp.replaceAll(r'C:\', '/mnt/c/').replaceAll(r'\', '/');
    
    final cwebpRes = await Process.run('wsl', ['cwebp', '-q', '95', wslSrc, '-o', wslDst]);
    if (cwebpRes.exitCode == 0) {
      stdout.writeln('✓ PGPhotoTrek WebP (cwebp): $phototrekWebp');
    } else {
      srcFile.copySync(phototrekWebp);
      stdout.writeln('✓ PGPhotoTrek WebP (direct): $phototrekWebp');
    }
  }

  stdout.writeln('\n[SUCCESS] Masterworks successfully synchronized to pgphototrek destinations!');
}
