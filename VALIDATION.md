# Validation scope and observed results

Release date: 2026-09-06. This is a validation of the distributed methods and local helper scripts, not an advertising-performance certification.

## Local observed checks

- Python 3.11 on Windows: 21 unit tests collected; 19 passed and 2 skipped because this Windows account cannot create symbolic links. The skipped cases cover legitimate symlink ancestors and rejection of a symlinked skill destination. The published [Linux/macOS CI run](https://github.com/Nacha192/claude-code-codex-ads/actions/runs/34026601326) then passed all 21 tests on each system, including both symlink tests. The downloaded job logs confirmed no skips.
- The skill-creator frontmatter validator accepted all four installed `SKILL.md` entrypoints.
- The release validator found no errors: exactly four installed skills, four ZIPs, 73 unique source records, eight selections of ten distinct valid IDs, valid internal Markdown links, and byte-identical shared modules across all four packages.
- ZIP contents match the distributed skill folders; archive SHA-256 values are included in `dist/SHA256SUMS`. Public text uses LF line endings for consistent checkouts.
- Preview installation makes no writes. Identical reinstallation succeeds; differing installed files remain untouched. Project installation and solo/team selections were exercised.
- A real temporary Git repository confirmed that the initialized private brand and evidence records are ignored by the brain's internal `.gitignore`. Ignore rules cannot prevent force-add or remove already tracked data.
- Common private-data patterns and task-specific private markers were checked in public text and ZIP contents. No hits remained. Private conversations, client creatives, credentials and collaboration-bus files are excluded.

## Genuine Claude Code collaboration

Codex coordinated the build and ran the checks. The real Claude Code CLI supplied authored workflow material and reviewed explicitly transmitted file contents as a fresh consultant. It did not have repository or media tools in these consultations; it did not execute the tests or independently verify the supplied hashes.

The first review exposed a Windows argument-transport problem that stripped quotes/truncated a long prompt. The coordinator switched the local consultation transport to stdin; Claude then confirmed receipt of all five files and intact JSON. The corrected behavioral submission was accepted. Solo self-review, approval provenance and privacy ordering were clarified following that exchange.

The technical review requested support for legitimate system symlink ancestors and an internal Git ignore file for private memory. Both were implemented with regression tests. Claude accepted the final four-script technical submission with no blockers. The final review left execution of the two Windows-skipped symlink cases to Linux/macOS CI; both were subsequently executed successfully there.

## Limits

The source inventory documents inspected entrypoints and original adaptations, not a security audit of every upstream executable. The top-ten lists are editorial task-fit selections with overlap, not global rankings or measured conversion results. Repositories without a clear redistribution license are not copied wholesale.

No paid media generation, live provider integration, voice authenticity verification or live Meta campaign was tested. Current account access, provider models, credits, platform rules and export quality must be checked during real use. A structural validator cannot establish claim truth, authentic quotations, policy approval, causal performance or visual/audio quality. Partial installation failures preserve files for inspection rather than deleting them automatically.
