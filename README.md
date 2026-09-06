# Claude Code × Codex Ads

**Four all-in-one advertising skills. Two solo editions. Two real-team editions. An integrated advertising second brain inside every one.**

Build campaigns around the actual business, buyer and evidence: research → hooks and copy → static or video creative → voice and export review → business experiments → reusable learning.

| Skill | Where you start | How it works |
|---|---|---|
| [meta-ads-codex](skills/meta-ads-codex/SKILL.md) | Codex | Complete solo workflow; Sol basic and Astra advanced profiles |
| [meta-ads-claude-code](skills/meta-ads-claude-code/SKILL.md) | Claude Code | Complete solo workflow; available Claude model and Opus 5 advanced profile |
| [meta-ads-team-codex-and-claude-code](skills/meta-ads-team-codex-and-claude-code/SKILL.md) | Codex | Both real assistants contribute and cross-review |
| [meta-ads-team-claude-code-and-codex](skills/meta-ads-team-claude-code-and-codex/SKILL.md) | Claude Code | Same complete team mission, opposite starting host |

There is **no separate copywriting, research or second-brain skill to install**. All are internal modules. Each pack includes the complete shared methods and its host-specific entrypoint. The team uses the real [Agent Duet bridge](https://github.com/Nacha192/Codex-Claude-Code-team) and available tools; it never impersonates the other assistant.

## Install

Follow [install-guide.md](install-guide.md), or choose one of the four ZIPs. Existing users should read [migration notes](MIGRATION.md):

- [Install Codex solo](dist/install-meta-ads-codex.zip)
- [Install Claude Code solo](dist/install-meta-ads-claude-code.zip)
- [Install team starting in Codex](dist/install-meta-ads-team-codex-and-claude-code.zip)
- [Install team starting in Claude Code](dist/install-meta-ads-team-claude-code-and-codex.zip)

Optional capabilities are listed in [you-can-install-tools.md](you-can-install-tools.md). Provider subscriptions, credits and authenticated access are not included.

## What is inside

- Business discovery, niche and buyer/awareness analysis; questions only for missing essentials.
- Meta library research with market, language, date-window, query and sampling records.
- Hooks and complete copywriting grounded in actual offer truths and buyer tensions.
- Static/carousel layouts, video/motion, UGC-style execution, directed narration, captions, music/effects and real export QA.
- Routes for OpenAI images, Gemini/Nano Banana, Higgsfield, Seedance, Kling, Claude Design, ElevenLabs and suitable local rendering tools.
- An integrated second brain: connected reasoning, evidence, contradictions, creative genealogy, experiments and retrieval of relevant lessons. The method, schemas and initializer ship inside each pack. Private business records stay in that user's project.
- Account-operation boundaries, single-executor team handoffs and ambiguous-write reconciliation.

Instructions are English. The assistant keeps the user's conversation language; ads use the target market's language. Public files contain reusable methods and synthetic templates, not private business data or client creatives.

## Research and adaptation

A fresh GitHub search on **2026-09-06** produced a reviewed corpus of **73 SKILL.md entrypoints**. The [internal source catalog](skills/meta-ads-codex/references/source-catalog.md) contains eight top-ten selections: hooks, static, video and copywriting, each for Codex and Claude Code. The 80 positions deliberately overlap. Codex-compatible does not falsely mean Codex-native. Supporting skills are identified.

Each source has a pinned revision, hash, date, provenance, caveat and original functional adaptations for both hosts. See [source inventory](research/sources.json), [discovery](research/discovery.json) and [attribution](THIRD_PARTY_NOTICES.md). These are reasoned task-fit selections, not an objective world ranking or proof of ad performance. Upstream tools and full unlicensed skill text are not bundled.

Original craft lessons from earlier static and motion projects are generalized in the internal retrospective. They are not published case studies or performance endorsements.

## Approval and quality

The assistant prepares a concrete proposal and asks before NEW media generation unless an existing scoped approval already covers it. It also respects actual account/spend authorization. A request to research does not launch campaigns. Real provider access and current specifications are checked before use.

Advanced modes add competing hypotheses, stronger prototypes and deeper review. They do not claim human consciousness, guaranteed 10× performance, guaranteed platform approval or elimination of every possible bug.

## Build and validation

Python 3.10+; standard library for included scripts:

```sh
python scripts/build.py
python -m unittest discover -s tests -v
python scripts/validate_release.py
```

See [VALIDATION.md](VALIDATION.md) for actual checks, peer-review scope and known limits. Read-only/offline checks cannot prove source truth, aesthetic quality or provider access. No live ad campaign or paid media generation is performed by the tests.

MIT for original work; upstream rights remain separate. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
