# Meta ad research and hook intelligence

Read intake first. Research competitor mechanisms, offers and creative patterns to inform original work, not to duplicate creative expression or claim access to competitors' results.

## Access ladder

1. Use a connected read-only Meta Ad Library tool or an official API whose actual market/category coverage and credentials have been checked.
2. Use the public Ad Library interface through an available browser tool. Respect access restrictions and reasonable query limits.
3. Use a user-authorized third-party provider only after checking its inputs, billing and current coverage.
4. If blocked, analyze user-provided exports, ad URLs, screenshots or recordings. Report the missing coverage. Never fabricate rows or imply a screenshot is a live API observation.

Meta Ad Library and Marketing API are different surfaces. Account Insights require account authorization. Public commercial-library access does not promise global historical data or CPA/ROAS/spend figures. Verify current official coverage at https://www.facebook.com/ads/library/api/ and the actual connected tool schema. If documentation is inaccessible, state that limitation. Do not guess endpoints, field names, pagination tokens or historical scope from an old skill.

## Query and sampling plan

Build query families from the actual offer: product name/category; buyer's problem words in the target language; mechanism and workaround; competitor Page names; outcome terms. Record literal queries and Page IDs so namesakes can be excluded. Keep countries and languages separate; a multilingual country is not a single-language sample.

Start with a bounded exploratory sample (for example up to 30 distinct ads across 5 relevant advertisers), then expand only when coverage requires it and the budget allows. This is a convenience sample, not a market census. Preserve pagination/cursor, filter settings, retrieved count, exclusions, duplicates, missing media and truncation. Stop on repeated cursors, no new IDs, the declared sample ceiling, access errors or cost ceiling.

Canonical deduplication key is the provider's ad/archive ID plus platform. Preserve Page ID and source URL. Group identical creative separately from different ads; do not count regional duplicates as independent ideas. For reposts and variants, retain lineage rather than erasing the differences.

## Observation record

Each row: record ID, source URL, captured_at UTC, provider, archive/ad ID, Page ID/name, country filter, observed language, active status, start/end dates as supplied, retrieval window semantics, format, literal short hook excerpt or paraphrase, visual premise, opening action/timecode, mechanism, proof type shown, offer, CTA, destination, accessibility/coverage notes. Unknown metrics remain null, never zero. Do not collect personal contact information for a creative scan.

Label columns `observed`, `inferred` and `unavailable`. Longevity, repeated variants and frequency in this sample are research signals only. They are not verified spend, audience targeting or conversion performance. Use "promising to investigate" rather than "winning" without advertiser-owned evidence.

## Synthesis

Make a pattern matrix: buyer situation × hook mechanism × proof × format. Count patterns with a denominator and note source concentration. Select divergent examples: a dominant convention, a meaningful exception, a poorly served objection and an original route suited to this offer. Explain why a copied competitor claim would not transfer.

For each proposed angle supply: source observation, buyer friction, original premise, available proof, uncertainty, the execution in the format this pack actually builds, a still frame or a shot list, and a falsifiable test. Distinguish the observed hook from the new hook. A library report should link each example, disclose sampling gaps and end with actionable hypotheses, not a wall of downloaded ads.

For monitoring, save query settings and compare new/changed/removed IDs on subsequent authorized runs. A skill does not run on a schedule by itself; use an actual scheduler only when requested. Stay quiet when nothing meaningful changes unless the user requested periodic reports.
