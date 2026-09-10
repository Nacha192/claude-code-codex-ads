# Claude Code × Codex Ads

**Eight all-in-one advertising skills. Four build still creative, four build video. Two solo editions and two real-team editions on each side, with an integrated advertising second brain inside every one.**

Build campaigns around the actual business, buyer and evidence: research, hooks and copy, the creative itself, export review, business experiments, reusable learning.

## The eight packs

| Skill | Where you start | Builds |
|---|---|---|
| [meta-ads-static-codex](you-can-install-skill/meta-ads-static-codex/SKILL.md) | Codex | images and carousels, solo |
| [meta-ads-static-claude-code](you-can-install-skill/meta-ads-static-claude-code/SKILL.md) | Claude Code | images and carousels, solo |
| [meta-ads-static-team-codex-and-claude-code](you-can-install-skill/meta-ads-static-team-codex-and-claude-code/SKILL.md) | Codex | images and carousels, both assistants cross-reviewing |
| [meta-ads-static-team-claude-code-and-codex](you-can-install-skill/meta-ads-static-team-claude-code-and-codex/SKILL.md) | Claude Code | the same team mission, opposite starting host |
| [video-ads-codex](you-can-install-skill/video-ads-codex/SKILL.md) | Codex | video ads, solo |
| [video-ads-claude-code](you-can-install-skill/video-ads-claude-code/SKILL.md) | Claude Code | video ads, solo |
| [video-ads-codex-claude-code](you-can-install-skill/video-ads-codex-claude-code/SKILL.md) | Codex | video ads, both assistants cross-reviewing |
| [video-ads-claude-code-codex](you-can-install-skill/video-ads-claude-code-codex/SKILL.md) | Claude Code | the same team mission, opposite starting host |

Install the one that matches what you are making and where you sit. There is **no separate copywriting, research or second-brain skill to install**: they are internal modules, and every pack carries the complete shared method plus its host-specific entrypoint. The team editions use the real [Agent Duet bridge](https://github.com/Nacha192/Codex-Claude-Code-team) and actual tools; they never impersonate the other assistant.

## Why two halves rather than one skill

A still ad and a video ad are different crafts, and a pack that half-covers the other one gives confident advice about a job it cannot finish. So the split is enforced by the build: no still-creative source is compiled into a motion pack, and no motion source into a still pack. What both crafts share, the contract, the research method, the hooks, the thresholds, the compliance red line, the second brain, is written once in a shared trunk and copied into all eight, so a correction reaches every pack at the same time.

**No pack generates media by virtue of being installed.** Whether the machine can generate an image, a video, a voice or render a timeline is a property of the installation. The packs detect it, say what they found, and never describe a script or a silent draft as a finished ad.

## Where things are

| At the root | What it is for |
|---|---|
| [`you-can-install-skill/`](you-can-install-skill/) | the eight packs unpacked and readable. Read a `SKILL.md` here before installing anything |
| `install-meta-ads-static-*.zip` | the four still-creative editions |
| `install-video-ads-*.zip` | the four video editions |
| `SHA256SUMS` | checksums for the eight archives, so you can verify what you downloaded |
| [`system/`](system/) | everything that builds the packs: the sources, the research records behind every attribution, the installer, the build and validation scripts, and the tests |
| `README.md` | this file |
| `LICENSE` | MIT for the original work. Upstream rights stay separate, see the notices |
| `.gitattributes` | keeps git from corrupting the ZIP archives, and normalises line endings |
| `.gitignore` | paths git must never track |
| `.github/workflows/` | rebuilds and validates the release on every push |

Inside `system/src/`, `common/` is what every pack receives, `static/` and `motion/` are the two craft layers, and `entrypoints/` holds the eight `SKILL.md` sources.

## Install

Follow [install-guide.md](system/install-guide.md), or download one ZIP and extract its folder into your skill directory. Existing users should read the [migration notes](system/MIGRATION.md), which record what changed in each release and, for every defect found, what it was and how it was caught.

```sh
python system/install.py --runtime codex --scope static --apply
python system/install.py --runtime claude --scope motion --apply
```

Without `--apply` it previews and writes nothing. Omit `--scope` to install both halves for that runtime.

On the first task in a project, each pack runs `python scripts/check_setup.py`. It
reports what is present, what is missing with the exact command for this operating
system, and what no script can see at all, such as a connected image tool or an account
with credits. It installs nothing: the assistant presents the whole gap in one message,
asks once, installs only if you agree, and if you decline it records that and does the
job anyway while saying plainly what did not run.

The included checks are Python scripts and need Python 3.10 or newer. A pack installed from a ZIP verifies this on its first task in a project and asks before installing anything; without an interpreter it keeps working for research and copy and says plainly that the checks did not run. Optional capabilities are listed in [you-can-install-tools.md](system/you-can-install-tools.md). Provider subscriptions, credits and authenticated access are not included.

## What is inside

Shared by all eight:

- Business discovery, niche and buyer/awareness analysis; questions only for missing essentials, including the blocking one about register.
- Meta library research with market, language, date-window, query and sampling records, and an explicit account of what a public library can and cannot prove.
- Hooks and complete copywriting grounded in actual offer truths and buyer tensions.
- Thresholds with a tag on every number saying where it came from, and a compliance red line matched on the rendered copy.
- An integrated second brain: connected reasoning, evidence, contradictions, creative genealogy, experiments and retrieval of relevant lessons. Private business records stay in that user's project.
- Account-operation boundaries, single-executor team handoffs and ambiguous-write reconciliation.
- Three named team fallbacks: one side lacks the tool, one side misread the instruction, one side lacks the context.

Only in the still packs: image and carousel layout, product-context composition, real export QA, and routes for OpenAI images, Gemini and Nano Banana, Higgsfield stills and Claude Design.

Only in the video packs: **a production system**, not a strategy document. An
eight-phase contract from a rough idea to inspected files, one `motion-project.json`
holding the whole job, an art-direction chooser across twelve directions instead of a
house style, per-ratio compositions, a correction loop capped at three passes, real
filming when that beats generating, and scripts that decide rather than advise.

### A reference engine is supplied, and it runs

```console
python scripts/make_fixture_assets.py --out fixtures
python scripts/render_motion.py examples/motion-project.render.json --root . --apply --contact-sheet
```

Those two commands ship inside every video pack and they are the ones this repository
is tested with. The second turns a manifest into finished files: one composition per
ratio, a contact sheet and control frames beside each export, and the manifest updated
from what was actually written rather than from what was planned. Python and FFmpeg
only. **No JavaScript, no Node, no account, no network.**

The shipped sixteen second fixture renders 1080x1920, 1080x1350 and 1920x1080, 480
frames each at 30 fps, measured at -14.0 LUFS by the decoder rather than claimed by the
renderer. The three are three compositions and not one crop: the portrait puts the
picture across the top two fifths with the copy beneath, the landscape is two columns
with the copy in the left one, and each ratio can override the safe zones the grid
gives it. **There are two shipped examples and they do not look alike**: a dark, warm,
camera-driven direction, and a light editorial one with dark ink, one cold accent,
tighter leading, a static camera and a softened plane behind a sharp one. Same engine,
same schema, same command, and a test compares a frame from each because a design
system nobody has pointed anywhere else is an assumption. Rendering the same manifest
twice produces the same bytes. An interrupted run
resumes by counting the frames of the clips it already has, so a half written one is
rebuilt and a finished one is not.

Before drawing anything it checks what the machine can actually do and refuses by name
rather than shipping something broken. Homebrew's ffmpeg on macOS carries libx264 and
aac and no libfreetype, so `drawtext` does not exist: the run stops with exit 3 naming
the missing filters instead of delivering an ad at the right duration with none of the
words in it.

Then the two scripts that judge:

```console
python scripts/check_motion_project.py motion-project.json --root .
python scripts/inspect_video.py out/ad-9x16.mp4 --expect-ratio 9:16 --expect-duration 20 --json
```

The first refuses a manifest that claims more than it can show: a state with no files,
a claim with no source, a ratio the brief asked for that nobody composed, captions
written from the script instead of the take, an engine that was assumed. It also reads the parts
nothing used to look at, and it separates what is wrong from what is risky. Text whose
colour and ground the manifest both names is measured against WCAG: under 3:1 it is an
error, under 4.5:1 a warning, and over a photograph nothing is claimed at all because
nothing can be measured. A caption held under 0.6 seconds is an error, since it is gone
before it is read. A caption over 42 characters or over 22 characters a second is a
warning. A safe zone that is not a fraction of the frame is an error; one tighter than
the floor for its ratio is a warning, and the floor is per ratio: 9:16 keeps 14% clear
at the top and 20% at the bottom, 16:9 keeps 5% at each. The second
decodes each export in full and measures duration, dimensions, ratio, sample aspect,
frame rate, frame count, codec, bitrate, audio tracks, sample rate, loudness, true
peak, clipping risk, head and tail silence, decode errors, black frames and frozen
frames. Every threshold it enforces arrives as an argument, from the brief or the
manifest; it invents none.

Also in the video packs, and unchanged in substance: retention structure, a protocol
for studying video that already runs, choosing and prompting a video model, voice
including cloning the user's own with a consent record, music and sound design, and
assembly.

**The supplied engine is the floor, not the ceiling.** The manifest names the engine it
was rendered with, so a better renderer replaces the reference one without touching the
rest of the job. JavaScript is never required. The packs detect eight
capabilities and choose a pipeline from what is actually installed: a video model, a
deterministic compositor such as Remotion or an FFmpeg filter graph, speech, music,
captions, rendering, inspection and multi-format adaptation. When a capability is
missing the pack says which one and delivers everything up to that wall. Nothing here
calls a plan a video.

Instructions are English. The assistant keeps the user's conversation language; ads use the target market's language. Public files contain reusable methods and synthetic templates, not private business data or client creatives.

## Research and adaptation

A fresh GitHub search on **2026-09-06** produced a reviewed corpus of **73 SKILL.md entrypoints**. Each half compiles the ones its craft needs: 55 in the still packs, 59 in the video packs. Each pack carries six top-ten selections in its internal source catalog, and the 60 positions deliberately overlap. Codex-compatible does not falsely mean Codex-native, and supporting skills are identified as such.

Each source has a pinned revision, hash, date, provenance, caveat and original functional adaptations for both hosts. See [source inventory](system/research/sources.json), [discovery](system/research/discovery.json) and [attribution](system/THIRD_PARTY_NOTICES.md). These are reasoned task-fit selections, not an objective world ranking or proof of ad performance. Upstream tools and full unlicensed skill text are not bundled.

Provider model names, durations and resolutions in the video packs are **dated observations of one connected catalogue**, not a promise about what any account exposes. Verify them in the catalogue you actually hold.

## One shot, and what it does not mean

The video packs are built to run from an imperfect input to finished files without an
interview. One compact numbered message asking only what genuinely blocks, a stated
assumption for everything else, then produce, measure, inspect, correct and deliver.

One shot is not improvisation. It is the opposite: the questions are asked once
because they were sorted first, and the assumptions are written down where the reader
will see them rather than discovered later.

Two grids close the run, and neither replaces the other. The technical grid is a
script and it decides whether the file is sound. The creative grid is eighteen
questions a person answers by watching the export, muted and then with eyes closed,
and it decides whether the ad is worth money. A file can pass every automatic check in
this repository and still be an ad nobody would watch.

## Approval and quality

The approval is recorded as a `generation_request` artifact and checked by a script: generating without a recorded approval, past the approved item ceiling, on a different provider or account, or on a zero-credit account all fail that check. The assistant prepares a concrete proposal and asks before NEW media generation unless an existing scoped approval already covers it. A request to research does not launch campaigns.

Advanced is a mode, not a model tier: any exposed model can run it, and a stronger one sharpens the passes rather than unlocking them. Neither mode claims human consciousness, guaranteed performance multiples, guaranteed platform approval or the elimination of every possible bug.

## Build and validation

Python 3.10+; standard library only for the included scripts:

```sh
python system/scripts/build.py
python -m unittest discover -s system/tests -v
python system/scripts/validate_release.py
```

The suite is 173 tests and the three platforms do not run the same thing, which is
stated rather than averaged into one green tick. Linux CI runs all 173 with a complete
ffmpeg, and that is where the end to end render, the byte reproducibility and the
interrupted resume are actually exercised. macOS collects 157 and skips 4, each
printing `this ffmpeg cannot draw: missing filters: drawtext, subtitles`. Windows skips
2 for a symlink privilege the account does not hold. A skip says why it skipped.

[SAFETY.md](system/SAFETY.md) separates the rules a script actually enforces, each with the test that covers it, from the ones that depend on a model behaving well, and from the ones nothing here can enforce. The middle list is longer for video, because video touches consent and identity, and it is written out rather than glossed over. See [VALIDATION.md](system/VALIDATION.md) for the checks that were actually run, the cross-review scope and the known limits. Offline checks cannot prove source truth, aesthetic quality or provider access, and no live campaign or paid generation happens in the tests.
