# Validation scope and observed results

Release date: 2026-09-07, version 3.0.0. This validates the distributed methods and the local helper scripts. It is not an advertising-performance certification, and it does not claim any provider will produce a good ad.

## Local observed checks

- Python 3.11 on Windows: 54 unit tests collected; 52 passed and 2 skipped because this Windows account cannot create symbolic links. The skipped cases cover legitimate symlink ancestors and rejection of a symlinked skill destination. [Linux and macOS CI](https://github.com/Nacha192/skill-claude-code-codex-ads/actions/workflows/validate.yml) runs the whole suite on both systems, including the two symlink tests.
- The release validator found no errors: eight installed skills, eight ZIPs, 73 inspected source records compiled into 55 still-creative and 59 motion adaptations, six selections of ten distinct valid IDs per scope, every build route pointing at a reference that exists in that scope, valid internal Markdown links, matching archive checksums, no orphan file in any pack, every test named in `SAFETY.md` present in the suite, and byte-identical shared modules across all eight packages.
- **The split is checked in both directions.** No still-creative source may be compiled into a motion pack and none of the motion sources into a still pack; the shared trunk is a declared list in `build.py` that the tree must match in both directions; no name may be defined in both the trunk and a craft layer; no reference may ship that no entrypoint can reach; and every pack's manifest must declare the scope it was actually built from. Those rules are what keep one repository from quietly becoming a pack that half-covers both crafts.
- **Those rules are proved by tests rather than by hand.** Twelve cases plant a real violation in a throwaway copy of the release and require the validator to refuse it, one per rule, plus a control on a clean copy so that a rule firing on everything cannot pass as a rule that works.
- **And the tests themselves were checked by mutation.** Each rule was neutralised in turn and the test that claims to prove it was required to fail. All twelve did. Two appeared not to on the first run, which turned out to be a fault in the neutralisation rather than in the tests: disabling `if A or B` by writing `if False and A or B` leaves `B` in force and changes nothing. That is worth recording, because a mutation run that silently fails to mutate reports a passing test as a lying one, and the obvious reading is to distrust the test. Before this, every structural rule had been demonstrated once, manually, and a later regression would have stayed green.
- Stale-artifact handling was exercised on a real tree before an earlier release: an orphan reference file, a pack with no source and an archive with no pack were all reported by the validator, then removed by a rebuild. Before that fix the orphan file shipped inside the archive and no check noticed.
- The storyboard checks were exercised on real artifacts: narration longer than its scene fails, overlapping scenes fail, `NaN` and boolean scene times fail, a voice field that is not a real line fails, a measured duration on a scene with no voice line fails, and both an unmeasured narration and a timeline gap warn rather than passing silently.
- ZIP contents match the distributed skill folders; archive SHA-256 values are in `SHA256SUMS`. Public text uses LF line endings for consistent checkouts.
- Preview installation makes no writes. Identical reinstallation succeeds; differing installed files remain untouched. Project installation, solo and team selection, and the new scope selection were all exercised.
- A real temporary Git repository confirmed that the initialized private brand and evidence records are ignored by the brain's internal `.gitignore`. Ignore rules cannot prevent force-add or removal of already tracked data.
- Common private-data patterns were checked in public text and in ZIP contents. No hits remained.

## What was verified rather than assumed

Both assistants were asked what they could actually do, and both answered by running commands rather than from memory. The result is dated in `research/capabilities-2026-09-06.md` and it contradicted the specification the video half was built from: the assistant described as the video generator had no video provider connected at all, and the one described as unable to generate had a catalogue of them.

That is why no edition claims a generation capability. The packs detect it. Any other wording would be describing two machines on one day and calling it a property of the software.

## Cross-review

Codex reviewed the specification, then the written references, as an adversary, with the instruction to find contradictions rather than to approve.

Its first pass found two: a bit rate incompatible with the file size demanded two lines below it, and a per-run scraping ceiling of sixty that contradicted the ninety videos the protocol asks for. Its second pass, on the built packs, found ten more, of which nine held: an item ceiling enforced in code while the documentation implied a spend ceiling was, a storyboard accepting a malformed voice field, a warning listed among the rules that fail with a non-zero exit, a claims guarantee that only ever applied to declared claims, two solo entrypoints promising a file they cannot always produce, a hook window stated as two seconds in one file and three in another, model durations contradicted by what was actually observed, a thresholds file claiming to hold every number while three other files held their own, and a captions rule contradicting a deliberate exception elsewhere.

The tenth was rejected and then conceded on the second exchange, which is the useful part: chasing the exact citation turned up a paragraph describing a rendering script from the still half that the video packs never shipped. It was rewritten rather than defended.

After the two halves were merged into this repository, the same review ran again on the merged tree and found eight more, two of which said an earlier fix had been incomplete rather than wrong: the artifact checker scanned JSON values but never keys, so a credential pasted as a field name passed; a generation request made of nulls or empty objects consumed the approved ceiling while naming nothing to produce; a spoken line measured at zero seconds slipped past both the unmeasured warning and the overrun check; an explicit empty installation target fell back to the default location instead of failing; the shared trunk was guarded by a list of six filenames somebody had to remember to extend; and a hook instruction still said to write three channels next to the paragraph explaining that a still has two. The last finding was that none of the structural rules had a regression test. That one is the reason for the eight tests above.

Codex also authored `references/measurable-checks.md` in the motion packs, running every ffmpeg and ffprobe command in it against fixtures it generated, including a deliberately clipped one, so the numbers in that file are measurements rather than recollections.

## Limits

- No claim is made that a corpus assembled from public discovery surfaces is a representative sample of anything. The method says so, dates itself, and records what could not be obtained.
- Provider model names, durations and resolutions are dated observations of one connected catalogue and will drift.
- Whose voice is in a supplied recording cannot be verified by any script here. The consent record is a discipline, not an enforcement.
- Nothing here certifies platform policy compliance, and disclosure rules for synthetic voice differ by market and change.
- Offline checks cannot prove that a source supports the claim citing it, that copy will be approved, or that a creative is any good.
