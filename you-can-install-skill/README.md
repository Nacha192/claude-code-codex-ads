# The eight skills, unpacked

Read them here. Install them from the `install-*.zip` archives at the
repository root, or with `python system/install.py`.

Each folder is a complete, self-contained skill: its `SKILL.md` entrypoint, the
`references/` it reads on demand, the `modules/` adapted from the researched
sources, its own `scripts/`, and its licence and attribution notices. Nothing
here needs another skill installed alongside it.

## Start here

Four build still creative.

| Skill | Entrypoint | You start in | What it is |
|---|---|---|---|
| meta-ads-static-codex | [SKILL.md](meta-ads-static-codex/SKILL.md) | Codex | The complete solo workflow. Basic and advanced reasoning profiles |
| meta-ads-static-claude-code | [SKILL.md](meta-ads-static-claude-code/SKILL.md) | Claude Code | The same solo workflow, Claude Code tools and models |
| meta-ads-static-team-codex-and-claude-code | [SKILL.md](meta-ads-static-team-codex-and-claude-code/SKILL.md) | Codex | Both assistants contribute and cross-review, starting from Codex |
| meta-ads-static-team-claude-code-and-codex | [SKILL.md](meta-ads-static-team-claude-code-and-codex/SKILL.md) | Claude Code | The same team mission, opposite starting host |

Four build video, and carry a motion engine that runs.

| Skill | Entrypoint | You start in | What it is |
|---|---|---|---|
| video-ads-codex | [SKILL.md](video-ads-codex/SKILL.md) | Codex | The complete solo video workflow, from brief to inspected files |
| video-ads-claude-code | [SKILL.md](video-ads-claude-code/SKILL.md) | Claude Code | The same solo workflow, Claude Code tools and models |
| video-ads-codex-claude-code | [SKILL.md](video-ads-codex-claude-code/SKILL.md) | Codex | Both assistants contribute and cross-review, starting from Codex |
| video-ads-claude-code-codex | [SKILL.md](video-ads-claude-code-codex/SKILL.md) | Claude Code | The same team mission, opposite starting host |

Install the one that matches what you are making and where you actually work.
The two team editions on each side are two halves of one protocol, not two
products: they differ in which assistant opens the mission.

## What is inside one of them

Using `meta-ads-static-codex` as the example. All eight carry the same shape,
and the rows above the line are identical in every pack.

| Path | Holds |
|---|---|
| [`SKILL.md`](meta-ads-static-codex/SKILL.md) | the entrypoint. Short on purpose: it routes to the references rather than repeating them |
| [`references/core.md`](meta-ads-static-codex/references/core.md) | the shared contract every other reference answers to |
| [`references/intake.md`](meta-ads-static-codex/references/intake.md) | establishing the real offer, buyer, market and language before anything is written |
| [`references/research.md`](meta-ads-static-codex/references/research.md) | ad library and competitor scans, with the window, the sample plan, and what a library cannot prove |
| [`references/copywriting.md`](meta-ads-static-codex/references/copywriting.md) | buyer friction, hook, mechanism, proof, call to action |
| [`references/image-prompting.md`](meta-ads-static-codex/references/image-prompting.md) | prompting an image model: the slot order it weights, the canvases it will accept, and why 1080 is not one of them |
| [`references/providers.md`](meta-ads-static-codex/references/providers.md) | the actual generation tools, and the approval gate in front of them |
| [`references/second-brain.md`](meta-ads-static-codex/references/second-brain.md) | memory: what was decided, what failed, what is still an open assumption |
| [`references/source-catalog.md`](meta-ads-static-codex/references/source-catalog.md) | the six top-ten selections, each source pinned to a revision and a hash |
| [`references/v11-lessons.md`](meta-ads-static-codex/references/v11-lessons.md) | craft lessons generalised from real static work |
| [`modules/`](meta-ads-static-codex/modules) | one card per researched source, with its original adaptation for both hosts |
| [`scripts/`](meta-ads-static-codex/scripts) | the artifact checker and the memory initialiser |

Only in a still pack: [`references/static.md`](meta-ads-static-codex/references/static.md),
images and carousels.

## What a video pack carries on top

Using `video-ads-codex` as the example.

| Path | Holds |
|---|---|
| [`references/production-contract.md`](video-ads-codex/references/production-contract.md) | the eight phases from a rough idea to inspected files |
| [`references/motion-manifest.md`](video-ads-codex/references/motion-manifest.md) | `motion-project.json`, the one file that holds the whole job |
| [`references/motion-engine.md`](video-ads-codex/references/motion-engine.md) | the supplied engine: the one command, the layer vocabulary, the design tokens, resume, and its honest limits |
| [`references/art-direction.md`](video-ads-codex/references/art-direction.md) | a chooser across twelve directions, instead of a house style |
| [`references/video-models.md`](video-ads-codex/references/video-models.md) | choosing a video model, with dated observations rather than promises |
| [`references/video-voice.md`](video-ads-codex/references/video-voice.md) | narration, including cloning the user's own voice with a consent record |
| [`references/live-action.md`](video-ads-codex/references/live-action.md) | filming, for when that beats generating |
| [`scripts/render_motion.py`](video-ads-codex/scripts/render_motion.py) | the one shot: manifest in, real files out, one composition per ratio |
| [`scripts/motion_engine.py`](video-ads-codex/scripts/motion_engine.py) | the engine itself: capability detection, layout, filter graphs, audio |
| [`scripts/check_motion_project.py`](video-ads-codex/scripts/check_motion_project.py) | refuses a manifest that claims more than it can show |
| [`scripts/inspect_video.py`](video-ads-codex/scripts/inspect_video.py) | decodes an export in full and measures it |
| [`examples/`](video-ads-codex/examples) | a documented manifest, and the sixteen second fixture this repository is tested with |

Try the engine before you need it, on a real client job with a deadline:

```console
python scripts/make_fixture_assets.py --out fixtures
python scripts/render_motion.py examples/motion-project.render.json --root . --apply --contact-sheet
```

That writes three real MP4 files at 1080x1920, 1080x1350 and 1920x1080, with a
contact sheet beside each. It needs Python and FFmpeg, nothing else. If this
machine cannot draw text, it says so by name and writes nothing, which is the
answer you want before the deadline rather than during it.

## Reading order

Start with `SKILL.md`. It is deliberately short, and it names which reference to
open for the task in front of you. Loading all of them for a small job wastes
context and makes the skill worse, not better.
