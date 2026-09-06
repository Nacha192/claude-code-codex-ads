#!/usr/bin/env node
/**
 * Render an HTML ad engine to PNG, at every required ratio.
 *
 *   npm i -D puppeteer
 *   node render_ads.mjs                      all layouts, all required ratios
 *   node render_ads.mjs --ad 3               one layout
 *   node render_ads.mjs --ratio 9x16         one ratio
 *   node render_ads.mjs --engine engine.html --out out --all-ratios
 *
 * Reads the layout list from the engine's `window.AD_LAYOUTS` array, so the
 * engine stays the single source of truth for how many ads exist and what they
 * are called. File names carry the layout slug, never a bare number.
 *
 * One bug this deliberately avoids: rendering every ratio in one browser page
 * by resizing it. A page laid out at one width and screenshotted at another
 * comes out cropped, silently, with no error. Each ratio gets its own page.
 */

import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const RATIOS = {
  '4x5': { w: 1080, h: 1350, required: true },
  '9x16': { w: 1080, h: 1920, required: true },
  '1x1': { w: 1080, h: 1080, required: false },
  '1.91x1': { w: 1200, h: 628, required: false },
};

const flags = new Map();
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a.startsWith('--')) {
    const next = process.argv[i + 1];
    if (next && !next.startsWith('--')) {
      flags.set(a.slice(2), next);
      i++;
    } else {
      flags.set(a.slice(2), true);
    }
  }
}

const enginePath = path.resolve(flags.get('engine') || 'engine.html');
const outDir = path.resolve(flags.get('out') || 'out');
const scale = Number.parseFloat(flags.get('scale') || '2.5');

if (!fs.existsSync(enginePath)) {
  console.error(`Engine not found: ${enginePath}`);
  console.error('Copy ad_engine_template.html into the project as engine.html first.');
  process.exit(1);
}

let puppeteer;
try {
  puppeteer = (await import('puppeteer')).default;
} catch {
  console.error('puppeteer is not installed. Run: npm i -D puppeteer');
  process.exit(1);
}

const wantedRatios = flags.get('ratio')
  ? [String(flags.get('ratio'))]
  : Object.entries(RATIOS)
      .filter(([, r]) => (flags.get('all-ratios') ? true : r.required))
      .map(([k]) => k);

for (const r of wantedRatios) {
  if (!RATIOS[r]) {
    console.error(`Unknown ratio: ${r}. Known: ${Object.keys(RATIOS).join(', ')}`);
    process.exit(1);
  }
}

const browser = await puppeteer.launch({ headless: 'new' });
const probe = await browser.newPage();
await probe.goto(pathToFileURL(enginePath).href, { waitUntil: 'networkidle0' });

const layouts = await probe.evaluate(() => (window.AD_LAYOUTS || []).map((l, i) => ({
  id: l.id ?? i + 1,
  slug: l.slug ?? `ad-${String(l.id ?? i + 1).padStart(2, '0')}`,
})));
await probe.close();

if (layouts.length === 0) {
  console.error('The engine exposes no window.AD_LAYOUTS. Nothing to render.');
  await browser.close();
  process.exit(1);
}

const selected = flags.get('ad')
  ? layouts.filter((l) => String(l.id) === String(flags.get('ad')))
  : layouts;

if (selected.length === 0) {
  console.error(`No layout with id ${flags.get('ad')}.`);
  await browser.close();
  process.exit(1);
}

const written = [];

for (const ratio of wantedRatios) {
  const { w, h } = RATIOS[ratio];
  const dir = path.join(outDir, ratio);
  fs.mkdirSync(dir, { recursive: true });

  for (const layout of selected) {
    // A fresh page per ratio. Never resize a laid-out page: it crops silently.
    const page = await browser.newPage();
    await page.setViewport({
      width: Math.round(w / scale),
      height: Math.round(h / scale),
      deviceScaleFactor: scale,
    });
    const url = `${pathToFileURL(enginePath).href}?ad=${layout.id}&ratio=${ratio}`;
    await page.goto(url, { waitUntil: 'networkidle0' });
    await page.evaluate(() => document.fonts && document.fonts.ready);

    const file = path.join(dir, `${layout.slug}.png`);
    await page.screenshot({ path: file });
    await page.close();

    // gen.verify_on_disk: an asset does not exist until it is on disk.
    const size = fs.statSync(file).size;
    if (size < 1024) {
      console.error(`Suspiciously small render, ${size} bytes: ${file}`);
      process.exitCode = 1;
    }
    written.push({ file, ratio, expected: `${w}x${h}`, bytes: size });
    console.log(`${ratio.padEnd(7)} ${layout.slug.padEnd(28)} ${size} bytes`);
  }
}

await browser.close();

console.log(`\n${written.length} file(s) in ${outDir}`);
console.log('Next: run redline_check.py before anything leaves this folder.');
