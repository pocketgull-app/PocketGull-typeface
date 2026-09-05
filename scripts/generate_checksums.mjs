import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, '..');

const ttfDir = path.join(root, 'fonts', 'ttf');
const woff2Dir = path.join(root, 'fonts', 'woff2');

const sha256Lines = [];
const sriManifest = {};

function processDir(dirPath, relativeDir) {
  if (!fs.existsSync(dirPath)) return;
  const files = fs.readdirSync(dirPath).sort();
  for (const file of files) {
    const filePath = path.join(dirPath, file);
    const stat = fs.statSync(filePath);
    if (!stat.isFile()) continue;

    const data = fs.readFileSync(filePath);
    const sha256Hex = crypto.createHash('sha256').update(data).digest('hex');
    const sha384Base64 = crypto.createHash('sha384').update(data).digest('base64');
    const relPath = path.join(relativeDir, file).replace(/\\/g, '/');

    sha256Lines.push(`${sha256Hex}  ${relPath}`);
    sriManifest[relPath] = {
      size: stat.size,
      sha256: sha256Hex,
      sri: `sha384-${sha384Base64}`
    };
  }
}

processDir(ttfDir, 'fonts/ttf');
processDir(woff2Dir, 'fonts/woff2');

const sha256Content = sha256Lines.join('\n') + '\n';
const sha256Path = path.join(root, 'fonts', 'SHA256SUMS');
fs.writeFileSync(sha256Path, sha256Content, 'utf8');
console.log(`Generated ${sha256Path} (${sha256Lines.length} entries)`);

const sriPath = path.join(root, 'fonts', 'sri-hashes.json');
fs.writeFileSync(sriPath, JSON.stringify(sriManifest, null, 2) + '\n', 'utf8');
console.log(`Generated ${sriPath} (${Object.keys(sriManifest).length} entries)`);
