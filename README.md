# Claude Code × Codex Ads

**Four all-in-one advertising skills. Two solo editions. Two real-team editions. An integrated advertising second brain inside every one.**

Build campaigns around the actual business, buyer and evidence: research, hooks and copy, static creative, export review, business experiments, reusable learning.

| Skill | Where you start | How it works |
|---|---|---|
| [meta-ads-static-codex](you-can-install-skill/meta-ads-static-codex/SKILL.md) | Codex | Complete solo static workflow; basic and advanced modes on whichever model the host exposes |
| [meta-ads-static-claude-code](you-can-install-skill/meta-ads-static-claude-code/SKILL.md) | Claude Code | The same solo static workflow, on the current Claude model or Opus 5 |
| [meta-ads-static-team-codex-and-claude-code](you-can-install-skill/meta-ads-static-team-codex-and-claude-code/SKILL.md) | Codex | Both real assistants contribute and cross-review |
| [meta-ads-static-team-claude-code-and-codex](you-can-install-skill/meta-ads-static-team-claude-code-and-codex/SKILL.md) | Claude Code | Same complete team mission, opposite starting host |

There is **no separate copywriting, research or second-brain skill to install**. All are internal modules. Each pack includes the complete shared methods and its host-specific entrypoint. The team uses the real [Agent Duet bridge](https://github.com/Nacha192/Codex-Claude-Code-team) and available tools; it never impersonates the other assistant.

## Where things are

| At the root | What it is for |
|---|---|
| [`you-can-install-skill/`](you-can-install-skill/) | the four packs unpacked and readable, with an index. Read a `SKILL.md` here before installing anything |
| `install-meta-ads-static-codex.zip` | install this one to work in Codex, alone |
| `install-meta-ads-static-claude-code.zip` | install this one to work in Claude Code, alone |
| `install-meta-ads-static-team-codex-and-claude-code.zip` | both assistants on one mission, opened from Codex |
| `install-meta-ads-static-team-claude-code-and-codex.zip` | the same team mission, opened from Claude Code |
| `SHA256SUMS` | checksums for the four archives, so you can verify what you downloaded |
| [`system/`](system/) | everything that builds the packs: the sources, the research records behind every attribution, the installer, the build and validation scripts, and the tests |
| `README.md` | this file |
| `LICENSE` | MIT for the original work. Upstream rights stay separate, see the notices |
| `.gitattributes` | keeps git from corrupting the ZIP archives, and normalises line endings |
| `.gitignore` | paths git must never track |
| `.github/workflows/` | rebuilds and validates the release on every push |

## Install

Follow [install-guide.md](system/install-guide.md), or choose one of the four ZIPs. Existing users should read [migration notes](system/MIGRATION.md):

- [Install Codex solo](install-meta-ads-static-codex.zip)
- [Install Claude Code solo](install-meta-ads-static-claude-code.zip)
- [Install team starting in Codex](install-meta-ads-static-team-codex-and-claude-code.zip)
- [Install team starting in Claude Code](install-meta-ads-static-team-claude-code-and-codex.zip)

Optional capabilities are listed in [you-can-install-tools.md](system/you-can-install-tools.md). Provider subscriptions, credits and authenticated access are not included.

## What is inside

- Business discovery, niche and buyer/awareness analysis; questions only for missing essentials.
- Meta library research with market, language, date-window, query and sampling records.
- Hooks and complete copywriting grounded in actual offer truths and buyer tensions.
- Static image and carousel layouts, product-context composition and real export QA. Motion, narration and music are not in this pack; they belong to the video edition.
- Routes for OpenAI images, Gemini/Nano Banana, Higgsfield and Claude Design. Video and voice providers belong to the video pack.
- An integrated second brain: connected reasoning, evidence, contradictions, creative genealogy, experiments and retrieval of relevant lessons. The method, schemas and initializer ship inside each pack. Private business records stay in that user's project.
- Account-operation boundaries, single-executor team handoffs and ambiguous-write reconciliation.

Instructions are English. The assistant keeps the user's conversation language; ads use the target market's language. Public files contain reusable methods and synthetic templates, not private business data or client creatives.

## Research and adaptation

A fresh GitHub search on **2026-09-06** produced a reviewed corpus of **73 SKILL.md entrypoints**. The [internal source catalog](you-can-install-skill/meta-ads-static-codex/references/source-catalog.md) contains six top-ten selections: hooks, static and copywriting, each for Codex and Claude Code. The 60 positions deliberately overlap. The two video selections moved to the video pack with the rest of the non-static material. Codex-compatible does not falsely mean Codex-native. Supporting skills are identified.

Each source has a pinned revision, hash, date, provenance, caveat and original functional adaptations for both hosts. See [source inventory](system/research/sources.json), [discovery](system/research/discovery.json) and [attribution](system/THIRD_PARTY_NOTICES.md). These are reasoned task-fit selections, not an objective world ranking or proof of ad performance. Upstream tools and full unlicensed skill text are not bundled.

Original craft lessons from earlier static projects are generalized in the internal retrospective. They are not published case studies or performance endorsements.

## Approval and quality

The approval is recorded as a `generation_request` artifact and checked by a script: generating without a recorded approval, past the approved ceiling, on a different provider or account, or on a zero-credit account all fail that check. The assistant prepares a concrete proposal and asks before NEW media generation unless an existing scoped approval already covers it. It also respects actual account/spend authorization. A request to research does not launch campaigns. Real provider access and current specifications are checked before use.

Advanced is a mode, not a model tier: any exposed model can run it, and a stronger one sharpens the passes rather than unlocking them. Advanced adds competing hypotheses, stronger prototypes and deeper review. They do not claim human consciousness, guaranteed 10× performance, guaranteed platform approval or elimination of every possible bug.

## Build and validation

Python 3.10+; standard library for included scripts:

```sh
python system/scripts/build.py
python -m unittest discover -s system/tests -v
python system/scripts/validate_release.py
```

[SAFETY.md](system/SAFETY.md) separates the rules a script actually enforces, each with the test that covers it, from the ones that depend on a model behaving well, and from the ones nothing here can enforce. See [VALIDATION.md](system/VALIDATION.md) for actual checks, peer-review scope and known limits. Read-only/offline checks cannot prove source truth, aesthetic quality or provider access. No live ad campaign or paid media generation is performed by the tests.

MIT for original work; upstream rights remain separate. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](system/THIRD_PARTY_NOTICES.md).
