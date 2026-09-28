import { access, readFile } from 'node:fs/promises';
import { constants } from 'node:fs';
import { spawnSync } from 'node:child_process';

const files = ['index.html', 'github-pages.css', 'github-pages.js'];
for (const file of files) await access(file, constants.R_OK);
const html = await readFile('index.html', 'utf8');
for (const asset of ['github-pages.css', 'github-pages.js']) {
  if (!html.includes(`./${asset}`)) throw new Error(`index.html verwijst niet naar ${asset}`);
}
const check = spawnSync(process.execPath, ['--check', 'github-pages.js'], { stdio: 'inherit' });
if (check.status !== 0) process.exit(check.status ?? 1);
if (!html.includes('id="demo"') || !html.includes('id="demo-content"')) throw new Error('Interactieve demo ontbreekt in index.html');
console.log('GitHub Pages static demo checks passed');
