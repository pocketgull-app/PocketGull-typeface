import 'dart:io';

/// Cross-platform Headless Inkscape Runner.
/// Detects native system Inkscape (Windows, Linux, macOS) and falls back to WSL.
class InkscapeRunner {
  static Future<ProcessResult> exportPng({
    required File svgFile,
    required File pngFile,
    int? width,
    int? height,
    int dpi = 300,
  }) async {
    // 1. Check for native Inkscape on PATH
    if (await _canRun('inkscape')) {
      return Process.run('inkscape', [
        svgFile.path,
        '--export-type=png',
        '--export-filename=${pngFile.path}',
        '--export-dpi=$dpi',
        if (width != null) '-w',
        if (width != null) '$width',
        if (height != null) '-h',
        if (height != null) '$height',
      ]);
    }

    // 2. Check standard Windows path
    if (Platform.isWindows) {
      const standardWin = r'C:\Program Files\Inkscape\bin\inkscape.exe';
      if (File(standardWin).existsSync()) {
        return Process.run(standardWin, [
          svgFile.path,
          '--export-type=png',
          '--export-filename=${pngFile.path}',
          '--export-dpi=$dpi',
          if (width != null) '-w',
          if (width != null) '$width',
          if (height != null) '-h',
          if (height != null) '$height',
        ]);
      }
    }

    // 3. Fall back to WSL Inkscape
    final wslSvg = _toWslPath(svgFile.path);
    final wslPng = _toWslPath(pngFile.path);
    return Process.run('wsl', [
      '--',
      '/usr/bin/inkscape',
      wslSvg,
      '--export-type=png',
      '--export-filename=$wslPng',
      '--export-dpi=$dpi',
      if (width != null) '-w',
      if (width != null) '$width',
      if (height != null) '-h',
      if (height != null) '$height',
    ]);
  }

  static String _toWslPath(String path) {
    var p = path.replaceAll(r'\', '/');
    final match = RegExp(r'^([a-zA-Z]):').firstMatch(p);
    if (match != null) {
      final drive = match.group(1)!.toLowerCase();
      p = p.replaceFirst(RegExp(r'^[a-zA-Z]:'), '/mnt/$drive');
    }
    return p;
  }

  static Future<bool> _canRun(String cmd) async {
    try {
      final res = await Process.run(cmd, ['--version']);
      return res.exitCode == 0;
    } catch (_) {
      return false;
    }
  }
}
