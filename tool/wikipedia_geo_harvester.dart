// Copyright (c) 2026, The PocketGull Project Authors.
// All rights reserved. Use of this source code is governed by an OFL 1.1 license.

/// Wikipedia REST API Geographic & Linguistic Harvester
///
/// Complies with Wikimedia Foundation API User-Agent Policy:
/// User-Agent: PocketGullTypefoundry/2.0 (https://pocketgull.app; philgear@gmail.com)
library;

import 'dart:convert';
import 'dart:io';

Future<void> main() async {
  stdout.writeln('=== WIKIPEDIA REST API GEOGRAPHIC & LINGUISTIC HARVESTER ===');
  stdout.writeln('Location Target: Portland, Oregon (45.5152 N, -122.6784 W)');
  stdout.writeln('User-Agent: PocketGullTypefoundry/2.0 (https://pocketgull.app; philgear@gmail.com)');

  final client = HttpClient();
  
  // Coordinates for Portland, Oregon
  const lat = 45.5152;
  const lon = -122.6784;

  // 1. Wikipedia GeoSearch API: Find articles near Portland, Oregon
  final geoUrl = Uri.parse(
    'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord=$lat|$lon&gsradius=10000&gslimit=15&format=json'
  );

  stdout.writeln('\n[1/3] Querying Wikimedia GeoSearch API for locations closest to Portland, Oregon...');
  
  try {
    final request = await client.getUrl(geoUrl);
    request.headers.set('User-Agent', 'PocketGullTypefoundry/2.0 (https://pocketgull.app; philgear@gmail.com)');
    final response = await request.close();
    final body = await response.transform(utf8.decoder).join();
    final data = jsonDecode(body) as Map<String, dynamic>;

    final pages = (data['query']?['geosearch'] as List?) ?? [];
    stdout.writeln('[SUCCESS] Found ${pages.length} proximate geographic Wikipedia entries:\n');

    for (var i = 0; i < pages.length; i++) {
      final p = pages[i];
      final title = p['title'];
      final dist = (p['dist'] as num).toDouble();
      final pLat = p['lat'];
      final pLon = p['lon'];
      stdout.writeln('  ${(i + 1).toString().padLeft(2)}. $title (${dist.toStringAsFixed(0)} meters away) [lat: $pLat, lon: $pLon]');
    }

    // 2. Query Indigenous Linguistic heritage near Portland: Chinook Jargon / Chinuk Wawa / Duployan
    stdout.writeln('\n[2/3] Querying Wikipedia REST API for Indigenous Languages & Scripts closest to Portland, Oregon...');
    final indigenousArticles = [
      'Chinook_Jargon',
      'Chinuk_Wawa',
      'Duployan_shorthand',
      'Grand_Ronde_Community',
      'Cathlapotle',
    ];

    final summaryResults = <Map<String, dynamic>>[];

    for (final article in indigenousArticles) {
      final summaryUrl = Uri.parse('https://en.wikipedia.org/api/rest_v1/page/summary/$article');
      final sumReq = await client.getUrl(summaryUrl);
      sumReq.headers.set('User-Agent', 'PocketGullTypefoundry/2.0 (https://pocketgull.app; philgear@gmail.com)');
      final sumResp = await sumReq.close();
      if (sumResp.statusCode == 200) {
        final sumBody = await sumResp.transform(utf8.decoder).join();
        final sumJson = jsonDecode(sumBody) as Map<String, dynamic>;
        final title = sumJson['title'] ?? article;
        final extract = sumJson['extract'] ?? '';
        stdout.writeln('\n  • Article: $title');
        stdout.writeln('    Extract: ${extract.length > 180 ? extract.substring(0, 180) + '...' : extract}');
        summaryResults.add({
          'title': title,
          'extract': extract,
          'url': sumJson['content_urls']?['desktop']?['page'] ?? 'https://en.wikipedia.org/wiki/$article',
        });
      }
    }

    // 3. Save structured harvest to fonts/wikipedia_portland_harvest.json
    final out = {
      'timestamp': DateTime.now().toUtc().toIso8601String(),
      'anchor_location': {
        'city': 'Portland, Oregon',
        'latitude': lat,
        'longitude': lon,
      },
      'contact_email': 'philgear@gmail.com',
      'nearby_geographic_locations': pages,
      'closest_indigenous_scripts_and_languages': summaryResults,
    };

    final harvestFile = File('fonts/wikipedia_portland_harvest.json');
    harvestFile.writeAsStringSync(jsonEncode(out));
    stdout.writeln('\n[3/3] Structured geographic & linguistic harvest saved to ${harvestFile.path}');

  } catch (e) {
    stderr.writeln('[ERROR] Failed to query Wikipedia REST API: $e');
  } finally {
    client.close();
  }
}
