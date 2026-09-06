#!/usr/bin/env node
/**
 * Build a Meta Ad Library search URL.
 *
 * The point is reproducibility: the same frame every run, and a URL you can
 * paste next to the results as the only durable evidence of what you searched.
 *
 *   node ad_library_url.mjs "<keyword>" [COUNTRY] [DAYS] [--media all|video|image]
 *
 *   node ad_library_url.mjs "knee pillow" US 90
 *   node ad_library_url.mjs "coussin genoux" FR 90 --media video
 *
 * DAYS is the look-back window (scrape.lookback_window, default 90). It bounds
 * the ads to those that STARTED running before that date, which is how you
 * approximate scrape.observation_floor from the library's own filters.
 *
 * This script only builds a URL. It does not fetch, log in, or read any
 * credential, and it must never be extended to do so.
 */

const argv = process.argv.slice(2);
const flags = new Map();
const positional = [];

for (let i = 0; i < argv.length; i++) {
  if (argv[i].startsWith('--')) {
    flags.set(argv[i].slice(2), argv[i + 1] ?? '');
    i++;
  } else {
    positional.push(argv[i]);
  }
}

const [keywordArg, countryArg = 'US', daysArg = '90'] = positional;

if (!keywordArg || keywordArg.trim().length < 2) {
  console.error(
    'Usage: ad_library_url.mjs "<keyword>" [COUNTRY=US] [DAYS=90] [--media all|video|image]'
  );
  process.exit(1);
}

const keyword = keywordArg.trim();
const country = countryArg.trim().toUpperCase();

if (!/^[A-Z]{2}$/.test(country)) {
  console.error(`Country must be a two-letter code. Got: ${countryArg}`);
  process.exit(1);
}

const days = Number.parseInt(daysArg, 10);
if (!Number.isFinite(days) || days <= 0) {
  console.error(`DAYS must be a positive integer. Got: ${daysArg}`);
  process.exit(1);
}

const mediaArg = (flags.get('media') || 'all').toLowerCase();
const MEDIA = { all: 'all', video: 'video', image: 'image' };
if (!MEDIA[mediaArg]) {
  console.error(`--media must be one of: all, video, image. Got: ${mediaArg}`);
  process.exit(1);
}

const url = new URL('https://www.facebook.com/ads/library/');
url.searchParams.set('active_status', 'all');
url.searchParams.set('ad_type', 'all');
url.searchParams.set('country', country);
url.searchParams.set('media_type', MEDIA[mediaArg]);
url.searchParams.set('q', `"${keyword}"`);
url.searchParams.set('search_type', 'keyword_exact_phrase');

const bound = new Date();
bound.setDate(bound.getDate() - days);
url.searchParams.set('start_date[max]', ymd(bound));

console.log(url.toString());
console.error(
  `# frame: country=${country} media=${MEDIA[mediaArg]} started_before=${ymd(bound)} (${days}d look-back)`
);

function ymd(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}
