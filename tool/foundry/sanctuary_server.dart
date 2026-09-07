import 'dart:io';
import 'dart:convert';
import 'dart:async';
import 'phinney_auditor.dart';

/// PocketGull Native Dart Sanctuary Server & Live Telemetry Service
class SanctuaryServer {
  final Directory projectRoot;
  final int port;
  final List<WebSocket> _clients = [];

  SanctuaryServer({required this.projectRoot, this.port = 8770});

  Future<void> start() async {
    HttpServer? server;
    int bindPort = port;

    for (var offset = 0; offset < 10; offset++) {
      try {
        server = await HttpServer.bind(InternetAddress.loopbackIPv4, bindPort + offset);
        bindPort = bindPort + offset;
        break;
      } catch (_) {}
    }

    if (server == null) {
      print('[ERROR] Could not bind Sanctuary Server to any local port.');
      exitCode = 1;
      return;
    }

    print('\n======================================================================');
    print('  🕊️  POCKETGULL DART SANCTUARY SERVER & LIVE TELEMETRY (DART 3.11)');
    print('======================================================================');
    print('  Specimen Web App:      http://localhost:$bindPort/index.html');
    print('  Healing Games Parlor:  http://localhost:$bindPort/parlor_sanctuary.html');
    print('  Gameboard Studio:      http://localhost:$bindPort/gameboard.html');
    print('  Live Telemetry API:    http://localhost:$bindPort/api/status');
    print('  Forensic Audit API:    http://localhost:$bindPort/api/audit');
    print('  The World Tarot API:   http://localhost:$bindPort/api/tarot/world');
    print('  WebSocket Hot-Reload:  ws://localhost:$bindPort/ws/live');
    print('  Serving Directory:     ${projectRoot.path}');
    print('  Cache Control:         Zero-CORS, Instant Refresh');
    print('  Press Ctrl+C to terminate.\n');

    _setupFileWatcher();

    await for (HttpRequest request in server) {
      _handleRequest(request);
    }
  }

  void _setupFileWatcher() {
    try {
      projectRoot.watch(recursive: true).listen((event) {
        final path = event.path.toLowerCase();
        if (path.endsWith('.html') || path.endsWith('.css') || path.endsWith('.js') || path.endsWith('.ttf') || path.endsWith('.woff2')) {
          final filename = event.path.split(Platform.pathSeparator).last;
          _broadcastReload(filename);
        }
      });
    } catch (_) {
      // File watching might not be supported on all environments
    }
  }

  void _broadcastReload(String changedFile) {
    final msg = jsonEncode({
      'event': 'reload',
      'file': changedFile,
      'timestamp': DateTime.now().toIso8601String(),
    });
    for (final ws in List<WebSocket>.from(_clients)) {
      try {
        ws.add(msg);
      } catch (_) {
        _clients.remove(ws);
      }
    }
  }

  Future<void> _handleRequest(HttpRequest request) async {
    final path = request.uri.path;

    // CORS & Headers
    request.response.headers.add('Access-Control-Allow-Origin', '*');
    request.response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    request.response.headers.add('Access-Control-Allow-Headers', 'Content-Type');
    request.response.headers.add('TDM-Reservation', '1');
    request.response.headers.add('X-Content-Type-Options', 'nosniff');

    if (request.method == 'OPTIONS') {
      request.response.statusCode = HttpStatus.ok;
      await request.response.close();
      return;
    }

    // 1. WebSocket endpoint
    if (path == '/ws/live' && WebSocketTransformer.isUpgradeRequest(request)) {
      final ws = await WebSocketTransformer.upgrade(request);
      _clients.add(ws);
      ws.listen(
        (data) {},
        onDone: () => _clients.remove(ws),
        onError: (_) => _clients.remove(ws),
      );
      return;
    }

    // 2. REST APIs
    if (path.startsWith('/api/')) {
      await _handleApiRequest(request, path);
      return;
    }

    // 3. Static file delivery
    await _handleStaticFile(request, path);
  }

  Future<void> _handleApiRequest(HttpRequest request, String path) async {
    request.response.headers.contentType = ContentType.json;

    if (path == '/api/status' || path == '/api/health') {
      final ttfDir = Directory('${projectRoot.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}ttf');
      final fontCount = ttfDir.existsSync() ? ttfDir.listSync().where((f) => f.path.endsWith('.ttf')).length : 0;
      final payload = {
        'service': 'PocketGull Sanctuary Telemetry',
        'status': 'HEALTHY',
        'dartVersion': Platform.version,
        'activeFonts': fontCount,
        'connectedWebSockets': _clients.length,
        'qualityPillars': [
          '1000 UPM Em-Square',
          '2-Byte Word Alignment',
          'Bit-7 Flag Masking',
          'ISMP Clinical Disambiguation',
          'Full 256 Braille Coverage',
          'Monospace Pitch Invariant (600 UPM)',
          'DirectWrite ClearType Antialiasing (GASP)'
        ],
        'timestamp': DateTime.now().toIso8601String(),
      };
      request.response.write(jsonEncode(payload));
      await request.response.close();
      return;
    }

    if (path == '/api/audit') {
      final ttfDir = Directory('${projectRoot.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}ttf');
      final results = <Map<String, dynamic>>[];
      if (ttfDir.existsSync()) {
        final files = ttfDir.listSync().whereType<File>().where((f) => f.path.endsWith('.ttf'));
        for (final f in files) {
          final res = ThomasPhinneyAuditor.audit(f);
          results.add({
            'font': f.path.split(Platform.pathSeparator).last,
            'passed': res.passed,
            'glyphs': res.totalGlyphs,
            'oddLoca': res.oddLocaOffsets,
            'badBit7': res.badBit7Flags,
            'message': res.message,
          });
        }
      }
      request.response.write(jsonEncode({
        'total': results.length,
        'passed': results.where((r) => r['passed'] == true).length,
        'results': results,
      }));
      await request.response.close();
      return;
    }

    if (path == '/api/tarot/world') {
      final payload = {
        'arcana': 'Major Arcana XXI',
        'name': 'The World (Le Monde)',
        'symbolism': 'Cosmic Wholeness, Completion, Integration, and Infinite Renewal',
        'mandorla': {
          'geometry': 'Vesica Piscis Laurel Wreath',
          'colors': ['#10b981 (Celtic Emerald)', '#f59e0b (24k Gold)'],
          'lemniscates': 'Dual red infinity loops at zenith and nadir',
        },
        'guardians': [
          {'element': 'Air', 'totem': 'Angel', 'quadrant': 'Top-Left', 'frequencyHz': 432, 'quality': 'Intellect & Breath'},
          {'element': 'Water', 'totem': 'Eagle', 'quadrant': 'Top-Right', 'frequencyHz': 528, 'quality': 'Intuition & Flow'},
          {'element': 'Fire', 'totem': 'Lion', 'quadrant': 'Bottom-Left', 'frequencyHz': 660, 'quality': 'Willpower & Vitality'},
          {'element': 'Earth', 'totem': 'Bull', 'quadrant': 'Bottom-Right', 'frequencyHz': 330, 'quality': 'Somatic Grounding'},
        ],
        'dancingAnima': {
          'attributes': 'Dual spiral balance wands rotating in harmonic equilibrium',
          'center': 'Radiant Heart (♥)',
          'wholenessOrbit': 7,
        }
      };
      request.response.write(jsonEncode(payload));
      await request.response.close();
      return;
    }

    request.response.statusCode = HttpStatus.notFound;
    request.response.write(jsonEncode({'error': 'Endpoint not found', 'path': path}));
    await request.response.close();
  }

  Future<void> _handleStaticFile(HttpRequest request, String rawPath) async {
    var path = rawPath;
    if (path == '/' || path.isEmpty) path = '/index.html';
    final targetPath = '${projectRoot.path}${path.replaceAll('/', Platform.pathSeparator)}';
    final targetFile = File(targetPath);

    final ext = path.contains('.') ? path.split('.').last.toLowerCase() : '';
    final isHtml = ext == 'html';
    final isFont = ext == 'woff2' || ext == 'ttf' || ext == 'otf';
    final isStaticAsset = ext == 'css' || ext == 'js' || ext == 'svg' || ext == 'png' || ext == 'webp' || ext == 'ico' || ext == 'json';

    if (isFont) {
      request.response.headers.set(HttpHeaders.cacheControlHeader, 'public, max-age=31536000, immutable');
    } else if (isStaticAsset) {
      request.response.headers.set(HttpHeaders.cacheControlHeader, 'public, max-age=86400');
    } else {
      request.response.headers.set(HttpHeaders.cacheControlHeader, 'no-cache, no-store, must-revalidate');
    }

    if (await targetFile.exists()) {
      if (path.endsWith('.html')) request.response.headers.contentType = ContentType.html;
      if (path.endsWith('.css')) request.response.headers.contentType = ContentType('text', 'css', charset: 'utf-8');
      if (path.endsWith('.js')) request.response.headers.contentType = ContentType('application', 'javascript', charset: 'utf-8');
      if (path.endsWith('.json')) request.response.headers.contentType = ContentType('application', 'json', charset: 'utf-8');
      if (path.endsWith('.woff2')) request.response.headers.contentType = ContentType('font', 'woff2');
      if (path.endsWith('.ttf')) request.response.headers.contentType = ContentType('font', 'ttf');
      if (path.endsWith('.svg')) request.response.headers.contentType = ContentType('image', 'svg+xml');
      if (path.endsWith('.png')) request.response.headers.contentType = ContentType('image', 'png');
      if (path.endsWith('.webp')) request.response.headers.contentType = ContentType('image', 'webp');

      if (request.method == 'HEAD') {
        request.response.statusCode = HttpStatus.ok;
        await request.response.close();
        return;
      }

      final isCompressible = isHtml || ext == 'css' || ext == 'js' || ext == 'svg' || ext == 'json';
      final acceptEncoding = request.headers.value(HttpHeaders.acceptEncodingHeader) ?? '';
      if (isCompressible && acceptEncoding.contains('gzip')) {
        request.response.headers.set(HttpHeaders.contentEncodingHeader, 'gzip');
        request.response.headers.set(HttpHeaders.varyHeader, 'Accept-Encoding');
        await targetFile.openRead().transform(gzip.encoder).pipe(request.response);
      } else {
        await targetFile.openRead().pipe(request.response);
      }
    } else {
      request.response.statusCode = HttpStatus.notFound;
      request.response.write('404 Not Found: $path');
      await request.response.close();
    }
  }
}
