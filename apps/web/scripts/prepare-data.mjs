import { copyFile, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const appRoot = path.resolve(here, '..');
const repoRoot = path.resolve(appRoot, '..', '..');
const publicDir = path.join(appRoot, 'public');

await mkdir(publicDir, { recursive: true });
await copyFile(
  path.join(repoRoot, 'examples', 'mini-essay', 'analysis.json'),
  path.join(publicDir, 'example-analysis.json'),
);
await copyFile(
  path.join(repoRoot, 'examples', 'mini-essay', 'source.md'),
  path.join(publicDir, 'example-source.md'),
);
