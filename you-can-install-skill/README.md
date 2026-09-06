# The four skills, unpacked

Read them here. Install them from the `install-*.zip` archives at the
repository root, or with `python system/install.py`.

Each folder is a complete, self-contained skill: its `SKILL.md` entrypoint, the
`references/` it reads on demand, the `modules/` adapted from the researched
sources, its own `scripts/`, and its licence and attribution notices. Nothing
here needs another skill installed alongside it.

## Start here

| Skill | Entrypoint | You start in | What it is |
|---|---|---|---|
| meta-ads-codex | [SKILL.md](meta-ads-codex/SKILL.md) | Codex | The complete solo workflow. Basic and advanced reasoning profiles |
| meta-ads-claude-code | [SKILL.md](meta-ads-claude-code/SKILL.md) | Claude Code | The same solo workflow, Claude Code tools and models |
| meta-ads-team-codex-and-claude-code | [SKILL.md](meta-ads-team-codex-and-claude-code/SKILL.md) | Codex | Both assistants contribute and cross-review, starting from Codex |
| meta-ads-team-claude-code-and-codex | [SKILL.md](meta-ads-team-claude-code-and-codex/SKILL.md) | Claude Code | The same team mission, opposite starting host |

Install the one that matches where you actually work. The two team editions are
two halves of one protocol, not two products: they differ in which assistant
opens the mission.

## What is inside one of them

Using `meta-ads-codex` as the example. The other three carry the same shape.

| Path | Holds |
|---|---|
| [`SKILL.md`](meta-ads-codex/SKILL.md) | the entrypoint. Short on purpose: it routes to the references rather than repeating them |
| [`references/core.md`](meta-ads-codex/references/core.md) | the shared contract every other reference answers to |
| [`references/intake.md`](meta-ads-codex/references/intake.md) | establishing the real offer, buyer, market and language before anything is written |
| [`references/research.md`](meta-ads-codex/references/research.md) | ad library and competitor scans, with the window, the sample plan, and what a library cannot prove |
| [`references/copywriting.md`](meta-ads-codex/references/copywriting.md) | buyer friction, hook, mechanism, proof, call to action |
| [`references/static.md`](meta-ads-codex/references/static.md) | images and carousels |
| [`references/providers.md`](meta-ads-codex/references/providers.md) | the actual generation tools, and the approval gate in front of them |
| [`references/second-brain.md`](meta-ads-codex/references/second-brain.md) | memory: what was decided, what failed, what is still an open assumption |
| [`references/source-catalog.md`](meta-ads-codex/references/source-catalog.md) | the six top-ten selections, each source pinned to a revision and a hash |
| [`references/v11-lessons.md`](meta-ads-codex/references/v11-lessons.md) | craft lessons generalised from real static work |
| [`modules/`](meta-ads-codex/modules) | one card per researched source, with its original adaptation for both hosts |
| [`scripts/`](meta-ads-codex/scripts) | the artifact checker and the memory initialiser |

Start with `SKILL.md`. It is deliberately short, and it names which reference to
open for the task in front of you. Loading all of them for a small job wastes
context and makes the skill worse, not better.
