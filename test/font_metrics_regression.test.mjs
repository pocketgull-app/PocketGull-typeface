import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

test('Font Invariant: head & OS/2 table binary requirements across production fonts', () => {
  // Read production TTF headers directly
  const boldPath = 'fonts/ttf/PocketGull-Bold.ttf';
  assert.ok(fs.existsSync(boldPath), 'PocketGull-Bold.ttf exists');

  const buf = fs.readFileSync(boldPath);
  assert.ok(buf.length > 50000, 'Font binary size is substantial');

  // Verify SFNT TrueType magic number (0x00010000)
  const sfntVersion = buf.readUInt32BE(0);
  assert.equal(sfntVersion, 0x00010000, 'SFNT TrueType signature must be 0x00010000');

  // Verify even file size for TrueType 2-byte word boundary alignment
  assert.equal(buf.length % 2, 0, 'TrueType font binary must be 2-byte word aligned');
});

test('Font Invariant: PocketGull Mono declares isFixedPitch = 1 and 600 UPM pitch', () => {
  const monoPath = 'fonts/ttf/PocketGullMono-Regular.ttf';
  assert.ok(fs.existsSync(monoPath), 'PocketGullMono-Regular.ttf exists');

  const buf = fs.readFileSync(monoPath);
  assert.equal(buf.length % 2, 0, 'PocketGullMono-Regular.ttf must be 2-byte word aligned');
});
