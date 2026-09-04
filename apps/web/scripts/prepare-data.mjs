import { copyFile, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const appRoot = path.resolve(here, '..');
const repoRoot = path.resolve(appRoot, '..', '..');
const publicDir = path.join(appRoot, 'public');

await mkdir(publicDir, { recursive: true });
const copies = [
  ['examples/mini-essay/analysis.json', 'example-analysis.json'],
  ['examples/mini-essay/source.md', 'example-source.md'],
  ['benchmark/cases/mill-on-liberty/reference-a.json', 'mill-reference-a.json'],
  ['benchmark/cases/mill-on-liberty/reference-b.json', 'mill-reference-b.json'],
  ['benchmark/cases/mill-on-liberty/alignment-a-b.json', 'mill-alignment-a-b.json'],
];
for (const [source, target] of copies) {
  await copyFile(path.join(repoRoot, ...source.split('/')), path.join(publicDir, target));
}
