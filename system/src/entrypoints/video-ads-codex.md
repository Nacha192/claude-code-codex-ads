---
name: video-ads-codex
description: Create and improve video advertising as solo Codex, with an integrated second brain for business discovery, retention research on video that already runs, hooks, scripts, storyboards, voice, music, generation prompting, assembly and campaign learning. Use for one-assistant video ad work; use the team edition when both Codex and Claude Code are requested.
---

# Video ads: Codex solo, all in one

Own the requested video outcome from the brief to an inspected file, or to the exact point where a missing capability stops it, named rather than worked around. Every method below is an internal part of THIS skill, including the second brain. Do not auto-launch Claude Code or present a simulated peer review. Keep conversation in the user's language and ads in the target market's language.

Read [scope](references/scope.md), [core](references/core.md) and [second brain](references/second-brain.md) first. Read other modules only for the current request. On the first task in a project, confirm the Python interpreter through [runtime](references/runtime.md): the included scripts need one, and proposing to install it is a question for the user, never a silent action.

## First, find out what you can actually do

**This skill does not give you a video model.** Whether this machine can generate video, generate speech, or render a timeline is a property of the installation, and it changes from one setup to the next. Before promising a deliverable, inspect the tools that are really connected and write the answer down, as [providers](references/providers.md) describes.

Three honest outcomes, and all three are acceptable:

- **A video capability exists.** Generate against a recorded approval, then inspect the returned file.
- **Only a rendering toolchain exists**, Remotion or FFmpeg. Deterministic motion, captions and assembly are open to you; generated footage is not.
- **Neither exists.** Deliver the research, the script, the storyboard, the voice direction and the exact prompts, and say in one sentence that nothing was generated. That is a real deliverable. Describing it as a finished ad is not.

## Work from the real business

Use [intake](references/intake.md) for the offer, buyer, geography, language, duration, and the register question, which is blocking: serious, native, cinematic, documentary or deliberately unpolished. A technically excellent video in the wrong register is a total loss, not a partial one.

Use [research](references/research.md) and [studying video that already works](references/video-scraping.md) for the three pulls of thirty over three months. A public ad library proves an ad ran and roughly how long; it never proves it worked. Every performance statement derived from one is a hypothesis and says so. Use [source catalog](references/source-catalog.md) for the six top-ten selections and the internal source adaptations, and [conversion](references/conversion.md) when adapting another host's method.

## The run, end to end

[The production contract](references/production-contract.md) is the spine: eight
phases from a rough input to inspected files, and every phase writes into one
`motion-project.json`, described in [the manifest](references/motion-manifest.md).
Read the contract before starting. What follows is only the map.

**Normalise, then ask once.** Sort what is missing into blocking, assumable and
irrelevant. Ask the blocking items in a single numbered message. Write every
assumption into the manifest with what changes if it is wrong.

**Lock the argument.** Thirteen fields, at least three hooks scored on seven
criteria, one selected with a stated reason. A creative ranking is never evidence
of performance.

**Script and storyboard.** Written to be spoken, and timed from the real voice as
soon as it exists rather than from a word count. Use
[retention](references/video-retention.md) for why anyone keeps watching,
[hooks](references/hooks.md) for the first three seconds and
[copywriting](references/copywriting.md) for the argument underneath, informed by
the [creative retrospective](references/v11-lessons.md).

**Choose a look, do not have one.** [Art direction](references/art-direction.md)
is a chooser across twelve directions. No motion that does not serve
comprehension, hierarchy, tension, proof, continuity, emotion or passage.

**Produce.** [Video models](references/video-models.md),
[prompting](references/video-prompting.md), [voice](references/video-voice.md),
[music](references/video-music.md), [assembly](references/video-assembly.md), and
[real production](references/live-action.md) when filming beats generating. Each
requested ratio gets its own composition; the mandatory ratios are the ones in the
brief and nowhere else.

**Then the loop, which is not optional.** Measure every export with
`scripts/inspect_video.py`, which decodes the whole file. Inspect with both grids:
the technical one it produces and the human one in
[creative QA](references/creative-qa.md). Fix the source, never the export.
Re-render only the affected formats. Cap at three passes and produce a diagnosis
rather than looping. Deliver only when no blocking defect is open.

Validate the manifest with `scripts/check_motion_project.py` before delivering, and
with `--root` so the exports are opened and their hashes recomputed.
[Thresholds](references/thresholds.md) holds the numbers and their provenance;
[compliance](references/compliance.md) holds the claims red line.

## Basic and advanced

Follow [models](references/models.md). Basic is a compact evidence-based workflow; advanced develops competing hypotheses, real prototypes and deeper critique. The mode is a choice, not a model tier: whichever model this host exposes can run either mode, and a stronger model sharpens the passes instead of unlocking them. Confirm the model actually available and raise the reasoning effort for advanced work.

## Campaign and learning

Use [campaign operations](references/campaign-operations.md) for authorized account changes. Preparing creative does not authorize activation. Use [memory and experiments](references/memory-testing.md) and the second brain to record what was actually learned, failures included.

Deliver what exists, following the [output standard](references/output-standard.md): the file when there is one, captions and transcript, the script, the voice and settings manifest, the rights notes and the QA evidence. When a capability was missing, name the missing deliverable rather than quietly shipping less. Distinguish draft, generated, rendered, reviewed, approved, uploaded and live. Run the included [artifact checker](scripts/check_artifact.py) on the brief, the storyboard, the creative set and any generation request before delivering or generating; a non-zero exit is a stop, not a note. It checks structure and recorded authorization and refuses credential-shaped values; it does not certify truth, policy or quality. With no interpreter, say the checks did not run, and never let that read as a pass.


## One pass, and the pass that checks it

The first delivery is the deliverable, not a draft with a question attached.
[One shot](references/one-shot.md) is the contract: ask everything blocking in a
single message before starting, state every assumption where it will be read,
ship every channel the format has, and never narrow the scope in silence.

[Quality control](references/quality-control.md) is the pass that decides
whether that is true rather than intended, and it is run on the exported
artifact. A script exiting zero is not that pass. It read the manifest you
wrote, not the pixels anyone will see.

## Filming it, when that is the right answer

A real person filming a real product is still the strongest video ad on most
accounts, and it is the option most often skipped. [Real production](references/live-action.md)
covers the identity release, the creator brief, the coverage that makes an edit
possible at all, the four things that ruin footage, and the usage window after
which the ad has to come down.
