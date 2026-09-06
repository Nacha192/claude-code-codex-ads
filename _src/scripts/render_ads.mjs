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

    // gen.verify_on_disk: an asset does not exist until it is on disk AND its
    // dimensions were read back. A file of the right size at the wrong size is
    // the exact failure this pack warns about, and it is silent.
    const size = fs.statSync(file).size;
    const dims = pngSize(file);
    let ok = true;

    if (size < 1024) {
      console.error(`Suspiciously small render, ${size} bytes: ${file}`);
      ok = false;
    }
    if (!dims) {
      console.error(`Not a readable PNG: ${file}`);
      ok = false;
    } else if (dims.w !== w || dims.h !== h) {
      console.error(
        `WRONG SIZE ${dims.w}x${dims.h}, expected ${w}x${h}: ${file}\n` +
        `  A layout hard-coded to one width does this. Position against the CSS variables.`
      );
      ok = false;
    }
    if (!ok) process.exitCode = 1;

    written.push({ file, ratio, expected: `${w}x${h}`, actual: dims, bytes: size, ok });
    console.log(
      `${ok ? ' ' : '!'} ${ratio.padEnd(7)} ${layout.slug.padEnd(28)} ` +
      `${dims ? `${dims.w}x${dims.h}` : '??'}  ${size} bytes`
    );
  }
}

await browser.close();

const bad = written.filter((f) => !f.ok).length;
console.log(`\n${written.length} file(s) in ${outDir}${bad ? `, ${bad} FAILED verification` : ''}`);
if (bad) {
  console.error('Do not ship this batch. Fix the layout, re-render, verify again.');
} else {
  console.log('Next: run redline_check.py before anything leaves this folder.');
}

/**
 * Read width and height from a PNG header. Bytes 16-23 of the IHDR chunk, which
 * is always the first chunk. No dependency, and it fails loudly on a file that
 * is not a PNG rather than returning a plausible number.
 */
function pngSize(file) {
  let fd;
  try {
    fd = fs.openSync(file, 'r');
    const buf = Buffer.alloc(24);
    if (fs.readSync(fd, buf, 0, 24, 0) < 24) return null;
    const signature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
    if (!buf.subarray(0, 8).equals(signature)) return null;
    return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
  } catch {
    return null;
  } finally {
    if (fd !== undefined) fs.closeSync(fd);
  }
}
