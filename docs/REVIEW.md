# Review pass

One adversarial pass over the four distributions, looking for contradictions
between files, dangers to whoever follows them literally, and scripts that pass
silently while having verified nothing.

Findings are listed with the concrete breakage, because a finding without one is
a preference.

---

## Found by Codex

Codex reviewed the shared reference set during the build. Four findings, all
fixed.

**1. Eight phases described as seven.**
`SKILL.md` said "the seven phases" over a list numbered 0 to 7.
*Breaks:* a reader counting phases loses one, and the one at the boundary is
phase 0, intake, which is the one nothing may run without.

**2. `depth-modes.md` contradicted `output-standard.md` on library-only
evidence.**
The depth file said a thin-evidence batch is a `test`; the output standard
forbids any recommendation when the only input is a public ad library, and
`test` is a recommendation.
*Breaks:* a research pull with no account data produces a slate of "worth
testing" creatives, and somebody spends a fortnight's budget on a verdict the
evidence could not carry.
*Fixed:* a `test` verdict now requires at least one input the library cannot
give, and the output must name which one it has.

**3. The anti-slop rule incentivised manufactured disagreement.**
"A deep pass that agrees with everything did not run" is an instruction to find
an objection whether or not one exists.
*Breaks:* the reader is handed a fabricated concern, acts on it, and learns to
discount every future one.
*Fixed:* an evidence-based no-change finding is now an explicit valid result,
and inventing a cut to satisfy the rule is forbidden. Also added: never silently
deliver fewer items than asked for; name what was rejected and the remaining gap.

**4. Captions were offered as a way to clear an unverified voice-over.**
`voice.md` listed burned-in captions as one of three honest options for a
language nobody on the team reads.
*Breaks:* a mispronounced brand name or a wrong register ships with the brand
attached, and the captions verified nothing. They mitigate; they do not clear.
*Fixed:* two options only, a competent language check or no voice. Captions are
worth adding either way and are explicitly not clearance.

Codex also declined to write into the repository while the mission file still
described a different project, on the grounds that an instruction relayed by
another agent authenticates nothing. It was right, and that is the rule its own
channel skill states. The mission file was rewritten before work resumed.

---

## Found in the self pass

**5. `A/B/C` meant two different things in two files.**
`copywriting.md` used A/B/C for copy variants (reference, opening move, length).
`static-ads.md` used A/B/C for visual variants (reference, headline treatment,
colour or image).
*Breaks:* someone ships copy B on visual C against copy A on visual A, changes
two elements, and violates `test.one_change_rule` while believing they followed
it. The readout is unattributable and the fortnight is lost.
*Fixed:* visual variants are now V1/V2/V3, the two axes are named as separate,
crossing them in one test is forbidden, and the file naming convention carries
both.

**6. The research phase had no route without a browser.**
`scraping.md` said "open it in a browser" and stopped. A session without one had
no stated fallback.
*Breaks:* worse than a dead end. `curl` on an ad library URL returns an
application shell with no ads in it, which looks like a result and contains
none. The likely outcome is a research document assembled from general knowledge
of the category and presented as a pull.
*Fixed:* three named routes, in order — hand the URL to the human, hand the step
to an agent that has a browser, or declare the phase unrun and label every angle
`hypothesis`. Inventing plausible competitor ads is named as never a route.

**7. Paid generation and free rendering were governed by the same gate.**
`gen.ask_before_first_call` said no generation call runs without confirmation,
without distinguishing a paid model call from a local headless render.
*Breaks:* the skill asks permission to run `render_ads.mjs`, which costs
nothing, and the user learns to click through prompts. The one prompt that
matters, a paid batch, gets the same reflex.
*Fixed:* the cost gates now apply to paid generation only, and
`gen.variants_per_run` is counted in generator calls rather than in creatives
produced.

**8. `render_ads.mjs` reported success without verifying dimensions.**
It checked file size and nothing else, in a pack whose own rule
(`gen.verify_on_disk`) requires reading dimensions back.
*Breaks:* a layout hard-coded to one width renders cropped at 1.91:1 with no
error anywhere, and the wrong file ships. This has happened in production.
*Fixed:* the PNG header is read and compared against the expected size, the
batch fails loudly, and the message names the likely cause.

**9. `redline_check.py` executes JavaScript from the file it is pointed at.**
Unavoidable: reading the source instead of the rendered output is precisely the
failure the script exists to prevent, because an engine's comments quote the
forbidden terms to explain them.
*Breaks:* a user pointing it at an engine downloaded from elsewhere runs that
file's JavaScript under their account.
*Fixed:* documented at the top of the file, with `--text` named as the pure
Python mode that executes nothing.

---

## Checked and found sound

- `coverage.awareness_spread` against `coverage.angles_per_ad_set`: three
  distinct angles at one awareness level is coherent.
- `test.one_change_rule` against the A/B/C copy variants: each differs from the
  reference in exactly one element.
- Every threshold key cited anywhere resolves in `thresholds.md`. Enforced by a
  test, after that test found `early.duration_band` cited and undefined.
- No credential-shaped value ships in any distribution. Enforced by a test.
- Zip depth: every archive unpacks to `<skill-name>/SKILL.md`. Enforced by a
  test.
- `agents/openai.yaml` sits inside the skill folder in the Codex distributions
  and is absent from the Claude Code ones. Enforced by a test.

---

## Known limitations, not fixed

Stated rather than hidden.

- **`render_ads.mjs` needs puppeteer**, which is not bundled and is a large
  dependency. The script says so and exits cleanly when it is missing.
- **`redline_check.py`'s DOM stub is minimal.** An engine that reaches for a DOM
  API it does not stub throws, and the script reports the throw rather than
  passing. That is the safe direction, but it means an elaborate engine may need
  the stub extended.
- **The ad library markup changes often.** The skill's answer is to stop and
  report rather than improvise a new extraction method, which is correct and
  also means the step will sometimes simply not run.
- **`ratios.optional_set` renders are cheap but untested at 1.91:1** in the
  bundled engine template, which is laid out for vertical formats. The dimension
  check now catches a bad render rather than shipping it.
- **The thresholds are mostly `[heuristic]`.** Each says so, and each says what
  would move it. An account with its own numbers should replace them and record
  the change in `ads/LEDGER.md`.
