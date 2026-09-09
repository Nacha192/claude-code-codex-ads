# Migration from the initial distribution

## Version 4.3.0: two limits that were written down instead of fixed

The 4.1.0 notes listed line breaking as estimated and the render as not reproducible.
Both were real, both were stated honestly, and both were fixable. Writing a limit down
is not the same as accepting it.

**Line widths are read from the font.** The engine parses the `head`, `hhea`, `hmtx`
and `cmap` tables of the face that will actually draw the text, so a line breaks where
it reaches the column rather than where an assumed average character says it should.
Kerning is deliberately not applied, because `drawtext` does not apply it either;
matching the renderer matters more here than matching a typesetter.

The estimate it replaces was worse than "approximate". Checked against the pixels
`drawtext` puts on screen, the new measurement lands between 0.4% and 4.8% wide, and
never narrow. The old one read **96% too wide** on ten capital I and **41% too narrow**
on ten m, which is a line running most of the way out of the frame with nothing
measuring it. The test does that comparison rather than trusting the parser, so it
also holds on whatever face a Linux runner happens to have.

**Two renders of an unchanged manifest now produce identical bytes.** Neither cause
was visible in any output:

- `gradients` defaults to `seed=-1`, a new random gradient on every run. Seeds now come
  from the scene id, so scenes still differ from each other while each one repeats.
- `sidechaincompress` reads two streams whose framing varies between runs, so the
  ducking diverged and the audio re-encoded differently every time. Both sides are cut
  to identical frames first.

The video encoder was never the problem. Every scene clip, the assembly and the burned
captions were already byte-identical; it was the ducking underneath them. A hash
written into a manifest is now a fact about the project rather than about one
afternoon.

**CI installs ffmpeg on macOS as well as Linux.** The engine's job is to produce the
same three files on a machine that is not the author's, and a check that only ever ran
on one operating system was not testing that.

## Version 4.2.0: the manifest declared a reserve the engine never read

Every format has always carried `safe_zones`, the slice of the frame the platform
paints its own interface over. The engine read the project grid instead and applied
one pair of numbers to all three ratios. So the vertical's reserve, correctly the
largest, was also applied to the landscape, which threw away a tenth of a picture
nothing was ever going to cover, and the square kept a bottom margin sized for a
Reels caption bar it does not have.

The engine now reads each format's own zones and falls back to the grid only when a
format declares none. The shipped example was itself wrong on this and is corrected:
it declared 8% clear at the top of a 9:16 while `thresholds.md`, in the same pack,
asks for 14%. The validator now warns when a format undercuts that documented figure
and names the number, and refuses a zone written in pixels.

**Legibility is now checked rather than left to whoever opens the export.** Three
things that decide whether an ad is read were decidable all along and nothing decided
them:

- **Contrast.** Copy is measured against the ground the manifest names, on the WCAG
  ratio. Under 3:1 is an error, under 4.5:1 a warning. Over a picture nothing is
  computed, because a number invented from a token that was never on screen is worse
  than no number.
- **Reading rate.** A cue under 0.6 seconds is an error, one running faster than 22
  characters a second or longer than 42 characters is a warning. The rule that a cue
  is two to four words was written in `video-assembly.md` and enforced nowhere.
- **The first second.** Most impressions are muted and scrolled. A first scene whose
  text all arrives after one second warns, because a hook that exists only in the
  narration is not a hook.

None of this says the ad is good. It says the file can be read, which is the part that
is arithmetic. What is left is genuinely a human judgement and stays in
`creative-qa.md`.

**In the still packs**, `references/image-prompting.md` is new: the slot order a model
actually weights, the three ways a generated image fails as an ad, the parameters worth
setting deliberately, and the canvas trap. That last one is concrete. The guide's custom
sizes must be multiples of 16, and **1080, 1350 and 1920 are not**, so none of Meta's
canvases can be requested directly. The legal frames with the exact same ratios are
1088x1360, 1152x2048, 1088x1088 and 2048x1152, generated above the delivery size and
resampled down.

Dated model facts are recorded rather than implied, because they expire: OpenAI's
Videos API and the `sora-2` and `sora-2-pro` models were notified for removal on
2026-03-24 and are listed for shutdown on **2026-09-24**, and `gpt-image-1` on
2026-10-23. A pipeline written against any of them has a deadline on it. This is also
the answer to "a model makes videos, so why compose anything": generation returns
shots, and an ad is shots cut to a duration, composed per placement, captioned from
the final take and mixed to a declared loudness. The generation route is the half that
expires; the composition step is the half that does not.

## Version 4.1.0: the pack could judge a video and not make one

Four releases of rules about rendering, and nothing in the repository rendered. The
manifest schema, the inspector, the QA grids and the correction loop all assumed a
renderer that the assistant was expected to find somewhere. That is why the honest
score on real motion production was 8.3, and why the failure mode was always the
same: a slideshow, or a JavaScript toolchain nobody agreed to install.

`scripts/render_motion.py` and `scripts/motion_engine.py` are that renderer, on
Python and FFmpeg alone. One command turns `motion-project.json` into real MP4 files,
one composition per ratio, and writes back what the decoder measured. **JavaScript is
never mandatory**, and the adapters in `references/providers.md` are unchanged: this
is the floor, not a replacement for a better route.

A sixteen second fixture ad ships with it, at `examples/motion-project.render.json`,
with the script that generates its synthetic assets. It renders to 1080x1920,
1080x1350 and 1920x1080, and the suite renders all three and measures them rather
than describing them.

**What changed for an existing manifest.** Nothing is required. `design` and
`scenes[].layers` are new and optional, and a manifest without them validates exactly
as before. If you add them, the validator now refuses a layer kind nothing can draw,
a picture layer naming an asset that does not exist, text with nothing to say, a
pixel count in a field that holds a fraction of the frame, and a layer starting after
its own scene has ended.

**Defects found and fixed while building it**, each one now covered by a test:

- `xfade` refuses two inputs whose timebases differ, with an error naming neither the
  scene nor the cause. Every branch is normalised before it is joined.
- Transitions were shortening the film by their own duration, so a correct sixteen
  second timeline rendered 15.35 seconds and the duration check failed on a timeline
  nobody got wrong. Each clip now carries a tail exactly as long as the transition
  that follows it.
- `-t` cuts at the last frame strictly before the mark, losing a frame per scene.
  Clips are cut to an exact frame count and padded on the last frame when an input
  ends a fraction of a frame early.
- The renderer and the resume check computed that frame count separately and
  disagreed by one, because `3.2 + 0.35` is not `3.55`. One function answers both.
- Resume discarded everything after an interruption. The plan fingerprint was written
  when a run finished, and an interrupted run never gets there. It is written before
  the first scene now, and a clip is reused only if its frames are counted and match.
- A run limited with `--formats` erased the export records of the formats it did not
  touch. Re-rendering a vertical is not a statement that the landscape never existed.
- Burned captions landed on the body copy, and long lines ran off the frame. Both
  were found by looking at a contact sheet, and neither was visible in any
  measurement.
- Text layers used one absolute vertical position shared by all three ratios, which
  is the crop problem in a different costume. Blocks are measured and stacked per
  format now, and a per-layer clamp that could place two blocks on the same line was
  removed: measuring first is what prevents the collision, not clamping after.

## Version 4.0.4: the history was never scanned

`validate_release.py` reads the tree that is checked out. A clone carries every
commit, so anything committed once and removed later is still published and was
invisible to every rule in this repository.

A full scan of all 73 commits, 739 blobs, found no credential of any kind, no
Windows user path, and a single commit identity throughout. It found one real
thing: the `LICENSE` in the two oldest commits carried a copyright line naming the
author beside the published handle. A history rewrite before publication had
cleaned three other files and left this one, and nothing was looking.

That blob has been rewritten out of every commit. The delivered tree is unchanged,
byte for byte; only the history metadata moved.

`scripts/scan_history.py` now walks every blob of every commit for credential
shapes and Windows user paths, checks every commit identity against the publishing
one, and requires each `LICENSE` copyright line to name the published handle and
nothing else. That last rule is shape-based on purpose: no credential pattern can
catch a person's name, and writing the name into a scanner to look for it would
republish the thing being removed. CI runs it with the full history checked out,
because `actions/checkout` fetches a single commit by default and the check would
otherwise pass by having nothing to read.

**What this does not undo.** The repository had 160 clones from 59 unique cloners
in the fourteen days before the fix. Everyone who cloned holds the original
commits. A rewrite changes what GitHub serves from now on, it does not retrieve
what was taken. GitHub also keeps unreachable objects addressable by their SHA
until it collects them, which needs a request to support.

## Version 4.0.3: resolve both sides of a path, or neither

Fixing the archive order moved the integration failure from Linux to macOS, where
it exposed a second defect of the same family. A temporary directory on macOS lives
under `/var`, which is a symlink to `/private/var`. `reachable()` in the release
validator resolved the link targets it followed and left the pack path unresolved,
so `relative_to` raised `ValueError` and every one of the thirteen release rules
errored at once. No local run could produce it, because it needs a redirected
ancestor. The pack is resolved now, and a test builds that exact shape with a
symlink where one is allowed and a directory junction otherwise.

Every other pairing of `resolve()` and `relative_to` in the repository was audited
and each one already resolved both sides or neither. This was the only mismatch.

The CI matrix no longer fails fast. The first failure was cancelling the other
runner, which threw away half the information about a cross-platform defect exactly
when it was needed.

## Version 4.0.2: the archive order depended on the operating system

Continuous integration had been red on every commit for five releases and nobody,
me included, had looked at it. The failing test was the build determinism one, and
the cause was real.

**The ZIP entry order was platform-dependent.** `build.py` sorted `Path` objects.
Path comparison is case-insensitive on Windows and case-sensitive everywhere else,
so `examples/` was written before `LICENSE` on Windows and after it on Linux. The
same sources produced two different archives with two different checksums depending
on who ran the build. `validate_release` compared archive contents as a dictionary,
so the order never registered, and the ZIP check passed while the archives differed.
The build now sorts by the archive name.

**The determinism test claimed something no repository can promise.** It compared a
fresh build against the committed archives, so it asserted byte equality across
machines. DEFLATE output belongs to the zlib the interpreter was linked against,
which the workflow file already said in a comment while the test contradicted it. It
now compares two builds in the same environment, which is the property that makes a
checksum meaningful, and two portable rules were added beside it: each archive must
carry exactly the committed pack, and its entry order must be the same everywhere.

**CI now installs ffmpeg on Linux.** Seven measurement tests were skipping there, so
the half of quality control this repository is about was never exercised in
integration.

## Version 4.0.1: the defects an adversarial pass found in 4.0.0

Six fixes in the two motion scripts and one in the release validator. No file was
removed, no field changed name, and a manifest that was valid before is still valid
unless it named a file outside its own project.

**Export and asset paths must stay inside the project.** This is the one that
mattered. `--root` used to join the declared path to the root and read whatever it
landed on, so an absolute path or one climbing with `..` reached anywhere on the
machine, and a manifest that pointed at an unrelated file with a matching hash passed
the export check with zero errors while nothing produced by the job had been verified.
Absolute paths and `..` are refused outright, and the resolved path is required to
stay under the root, which also catches a symlink or a Windows junction that is
textually clean and still leaves the tree.

**A malformed section no longer takes the checker down.** `assets` given as a number
raised `TypeError` and killed the process; given as a string it was iterated letter by
letter and produced a report about single characters. Every list-shaped section is now
refused with a message.

**A manifest that is not UTF-8 exits 2 instead of printing a traceback.** The handler
caught `json.JSONDecodeError` and let `UnicodeDecodeError` through.

**Fractional pixel dimensions are refused.** 1080.5 pixels wide passed.

**ffmpeg failing silently is a blocking finding.** A nonzero exit with an empty stderr
left `decode_errors` at zero and produced no finding at all, which reads exactly like
a clean decode. Silence reading as a pass is the failure this pack exists to refuse,
and it was in the pack.

**Exports are hashed in chunks.** Both scripts read the whole file into memory to hash
it. Exports are videos, and that is how a checker dies on the largest file it is
handed.

**The release validator no longer crashes on a markdown file that is not UTF-8.** Two
loops read `.md` files without a handler.

**The installer refuses a Windows junction, not only a symlink.** `is_symlink()`
returns False for a directory junction, so the rule that refuses a redirected
installation target was walked straight past by the cheaper of the two
redirections: a junction needs no privilege to create, a symlink does. The two
existing symlink tests skip on Windows for exactly that missing privilege, so the
rule was going unproven on the platform where it was broken. Both new tests use a
symlink where one is allowed and a junction otherwise, and they run everywhere.

Each of the six rules is proved by mutation: neutralise the rule, and the test that
claims to prove it must fail. All six failed. The seventh, the crash on non-UTF-8
markdown, is covered by the release suite.

## Version 4.0.0: the video packs become a production system

Nothing was removed and no existing file stopped working, but the four video packs
changed character enough to earn a major number: they went from explaining how a good
video ad is made to running the job and refusing to sign off on it.

**The contract.** `production-contract.md` is the spine: eight phases from an
imperfect input to inspected files. Normalise the input and sort what is missing into
blocking, assumable and irrelevant. Ask the blocking items once, numbered, in a single
message. Lock thirteen fields of the argument. Score at least three hooks on seven
criteria and say why one won. Write a storyboard whose scenes carry fourteen fields
each. Choose an art direction. Produce. Then the correction loop.

**The manifest.** `motion-project.json` holds the whole job in one object, described
in `motion-manifest.md`, validated by `scripts/check_motion_project.py`, with a
complete worked example at `examples/motion-project.example.json`. Its `state` is one
of eight in order and it is a claim about the world: from `rendered` on, the exports
must exist and carry a hash, and with `--root` the files are opened and the hashes
recomputed. From `inspected` on, both QA grids must carry a verdict.

**The inspector.** `scripts/inspect_video.py` decodes each export in full and measures
duration, dimensions, ratio, sample aspect, frame rate, frame count, codec, bitrate,
audio tracks, sample rate, loudness, true peak, clipping risk, head and tail silence,
decode errors, black frames and frozen frames. Every threshold arrives as an argument.
With no expectation given it invents none, and that is a test.

**Two QA grids instead of one.** `creative-qa.md` is eighteen questions a person
answers by watching the file, including a full muted run and a full eyes-closed run.
It is separate from the technical grid on purpose, because a technically valid export
is not a good ad and treating the exit code as an opinion is how that gets forgotten.

**Art direction became a chooser.** `art-direction.md` holds twelve directions with
what each is good at, what it costs and how it fails, plus the frame-building rules
that separate a made ad from a generated one. There is no house style, because a pack
with a house style makes every client look like the pack.

**Absolute rules became heuristics.** "Five and only five" scroll-stops is now five
that work and an open list. "A cut every one to two seconds" is now a table of eight
things that decide rhythm and nine attention resets of which a cut is one. "Never show
the form" and "naming the price kills the lead" are now judgement calls with the case
for each side, because both are true in some categories and expensive in others. The
required ratio pair is a starting point; the mandatory ratios are the ones in the
brief.

**Engine independence.** `providers.md` gained a capability-and-adapter table. Eight
capabilities, several possible adapters each, detection before choice. JavaScript is
never mandatory, and the engine that was actually found is recorded in the manifest
with `detected: true`, which the validator requires to be literally true.

**Team integrity.** The two team video entrypoints now require a real capability card
from each side, an author and a reviewer named per artifact version, the hash of the
exact file that was reviewed, and a review that dies when the file changes after it.
The fallback to the solo skill when the peer is genuinely unreachable is explicit, and
it may never be described as a cross-review.

If you are upgrading from 3.x, nothing you were doing breaks. The manifest is new
work, not a migration: a project that never writes one still validates as it did, and
the checks that ran before still run.

## Version 3.1.0: the first pass, the check on it, and filming

Three references were added and nothing was removed, so nothing that worked in
3.0.0 stops working.

- `one-shot.md`, in all eight packs. The first delivery is the deliverable: ask
  everything blocking in one message before starting, state assumptions where
  they are read, ship every channel the format has, never narrow scope in
  silence.
- `quality-control.md`, in all eight packs. The inspection pass on the exported
  artifact, per format, with a three-word verdict vocabulary, and an exact
  statement of what the checker does and does not read.
- `live-action.md`, in the four video packs. Filming it for real: identity
  release, creator brief, mandatory coverage, reshoot criteria, usage window.

The four team editions changed shape. `team.md` gained a **blind pass** that runs
before any role is assigned: both sides write the buyer's problem, the blocking
obstacle and three concepts alone, exchange them simultaneously, and only then
read each other. The synthesis records what was agreed independently, what was
not, the counter-case for each disagreement written by the side that disagrees
with it, and the cheapest test that settles it. Until now the second side
reviewed the first side's artifact, which meant it reasoned from the first
side's framing and the pair produced one opinion checked twice. Roles are now
assigned after the synthesis rather than before.

Three corrections went with them. `compliance.md` no longer implies that wiring
the checker into the render step stops a violating creative from being exported;
it stops a violating *manifest*, and the difference is now stated. The buying
numbers in `thresholds.md` are declared defaults that a calculation from the
real baseline overrides, which is what `memory-testing.md` asked for all along.
And a public ad library may now support a test hypothesis, never a performance
verdict, in one rule instead of two that disagreed.

## Version 3.0.0: one repository, eight packs, and the video half arrives

The repository is `skill-claude-code-codex-ads`, renamed on 2026-09-07 when the two halves became one. GitHub redirects both earlier names, `claude-code-codex-ads` and `claude-code-codex-ads-static`, but update your remotes anyway.

Four video packs join the four still ones: `video-ads-codex`, `video-ads-claude-code`, `video-ads-codex-claude-code` and `video-ads-claude-code-codex`. The still packs keep their identifiers, and an installed one keeps working; nothing about its workflow was removed.

What changed underneath is that both halves are now built from **one shared trunk**. The contract, the intake, the team procedure, the hooks, the thresholds, the compliance red line, the output standard and the artifact checker are written once and copied into all eight packs. Two consequences for existing users of the still packs:

- Several files improved because the video half needed them to. The team procedure now names three fallbacks instead of one, the intake asks the blocking question about register, and the shared contract stops treating a zero exit code as proof that a render is good.
- The artifact checker knows `storyboard` again. It was removed from the still packs when the video material was pulled out, and it comes back because the code is shared. Producing a storyboard from a still pack is still out of scope; the scope file in each pack says so.

Every pack now carries `references/scope.md`, which states what that pack builds and what it deliberately leaves to its sibling. Read it first if you are unsure which one you installed.

The installer takes a `--scope` flag: `static`, `motion`, or both by default.

```sh
python system/install.py --runtime codex --scope motion --apply
```

## Version 2.1.0: the packs check for Python before relying on it

The scripts that enforce the approval gate, the credential refusal and the copy limits are Python. A ZIP install can land on a machine with no interpreter, which turned those guarantees into silence. Each pack now checks once per project, before the first script call or the first generation, and records the result in `.ads-brain/runtime.json`. If Python is missing it says what stops working, proposes the install route for that operating system and asks; it never installs anything on its own. If the user declines, the pack keeps doing research and copy and states that the checks did not run.

## Version 2.0.0: renamed, and static by name

The four skills say what they build. Update any script or documentation that names the old identifiers.

| Old identifier | New identifier |
|---|---|
| `meta-ads-codex` | `meta-ads-static-codex` |
| `meta-ads-claude-code` | `meta-ads-static-claude-code` |
| `meta-ads-team-codex-and-claude-code` | `meta-ads-static-team-codex-and-claude-code` |
| `meta-ads-team-claude-code-and-codex` | `meta-ads-static-team-claude-code-and-codex` |

The archives follow the same pattern, `install-meta-ads-static-*.zip`, and the repository is now `claude-code-codex-ads-static`. GitHub redirects the previous repository URL, but update your remotes anyway. An installed old skill is not migrated automatically: back it up, remove it once you have copied any local edits, then install the renamed pack. Leaving both installed gives the assistant two overlapping skills to choose between.

Basic and advanced are also stated as modes rather than model tiers in this release. Any model the host exposes can run either mode; a stronger model sharpens each pass instead of unlocking it. Nothing about the required artifacts changed.

This rebuild replaces the initial four distributions while preserving their Git history. The earlier source and rendering helpers remain inspectable at [the previous revision](https://github.com/Nacha192/skill-claude-code-codex-ads/tree/7982c9c99540302ee2a6ea3fec912f084c22b016). They are not silently executed or installed by this release.

That release published four installation archives at the repository root, prefixed `install-`; since 3.0.0 there are eight. Optional external tools are described in `you-can-install-tools.md`. Internal research, copywriting and second-brain modules are included in every pack.

The Claude-started team edition now has its own identifier, `meta-ads-static-team-claude-code-and-codex`. The Codex-started edition retains `meta-ads-static-team-codex-and-claude-code`. Both are complete advertising systems; their different entrypoints identify the starting host, not a permanent hierarchy.

## Version 1.3.0: these four packs are still creative only

Everything non-static left. The `video-voice.md` reference, the `codex-video` and `claude-video` top-ten selections, the 18 source adaptations routed to video or voice, the video and speech providers, and the `storyboard` artifact kind are no longer in these packs. They were staged in a separate repository at the time, and as of 3.0.0 they are back in this one, in the four video packs. Nothing was deleted, and the research record still lists all 73 inspected entrypoints; the packs now carry the 55 adaptations that apply to images and carousels.

If you were using one of these packs for video work, that path is gone rather than degraded, which is the point: a half-covered video workflow was worse than an explicit boundary. Ask for the video edition instead. If you kept `storyboard` artifacts, note that 1.3.0 rejected the kind and 3.0.0 accepts it again, with stricter checks than before.

## Version 1.2.0: the checker refuses more than it used to

`check_artifact.py` gained a `generation_request` kind and now refuses, in every kind, any value shaped like a credential. A `creative` is also checked against character limits and against the campaign's declared `prohibited_terms`. An artifact that passed under 1.1.0 can fail here, which is the point: a batch that grew past its approved ceiling, a provider swapped after approval, a zero-credit account, copy over the placement limit and a red-line term in rendered copy all stop the run instead of passing quietly. The artifact `schema_v` stays `1.0.0`, since nothing was removed or given a new meaning. [SAFETY.md](SAFETY.md) lists what each script enforces and what it cannot.

If an older skill is installed, back up that skill folder and any local edits before replacing it. The installer refuses to overwrite a differing folder. Do not leave conflicting editions with the same identifier in multiple skill-discovery locations. Preserve private campaign records separately; never replace them with templates from a new release. Existing memory formats are not automatically migrated: map relevant records to the included schema and retain provenance before using them.
