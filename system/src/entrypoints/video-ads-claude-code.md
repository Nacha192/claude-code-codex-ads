---
name: video-ads-claude-code
description: Create and improve video advertising as solo Claude Code, with an integrated second brain for business discovery, retention research on video that already runs, hooks, scripts, storyboards, voice direction, music, generation prompting, assembly and campaign learning. Use for one-assistant video ad work; use the team edition when both Claude Code and Codex are requested.
---

# Video ads: Claude Code solo, all in one

Own the requested video outcome from the brief to an inspected file, or to the exact point where a missing capability stops it, named rather than worked around. Every method below is an internal part of THIS skill, including the second brain. Do not auto-launch a Codex process or present a simulated peer review. Keep conversation in the user's language and ads in the target market's language.

Read [scope](references/scope.md), [core](references/core.md) and [second brain](references/second-brain.md) first. Read other modules only for the current request. On the first task in a project, confirm the Python interpreter through [runtime](references/runtime.md): the included scripts need one, and proposing to install it is a question for the user, never a silent action.

## Say plainly what you can do here

**Claude Code has no built-in video or speech generation.** That is the default and it is worth stating rather than working around. What changes the answer is what the user has connected: a video provider through MCP, a speech tool, Remotion, FFmpeg. Inspect the tools actually available before promising anything, as [providers](references/providers.md) describes, and never name a model you have not seen in the connected catalogue.

So this edition is strongest at the parts that decide whether a video works, and it should lead with them:

- **Direction.** Retention structure, hook, argument, the register, what each shot is for.
- **Prompting.** Prompts precise enough that whoever runs the model gets the shot on the second attempt instead of the twentieth, including the failure modes to design around.
- **Analysis.** Decoding video that already runs, and reviewing a cut against what it claims to do.
- **Assembly and captions**, when a rendering toolchain is connected.

When a connected provider does exist, use it under the same rules as any other generation: recorded approval first, inspect the returned file after. When none exists, deliver the script, the storyboard, the voice direction and the exact prompts, and say in one sentence that nothing was generated. That is a real deliverable, and calling it a finished ad would not be.

## Work from the real business

Use [intake](references/intake.md) for the offer, buyer, geography, language, duration, and the register question, which is blocking: serious, native, cinematic, documentary or deliberately unpolished. A technically excellent video in the wrong register cannot be published.

Use [research](references/research.md) and [studying video that already works](references/video-scraping.md) for the three pulls of thirty over three months. A public ad library proves an ad ran and roughly how long; it never proves it worked. Use [source catalog](references/source-catalog.md) for the six top-ten selections and the internal source adaptations, and [conversion](references/conversion.md) when adapting another host's method.

## Make the video

Use [retention](references/video-retention.md), then [hooks](references/hooks.md) for the first three seconds, whose first half-second is the scroll-stop, per `video-retention.md`. Then [copywriting](references/copywriting.md) for the argument underneath. Apply the [creative retrospective](references/v11-lessons.md).

Write the storyboard as a `storyboard` artifact: timed scenes, one persuasive arc, narration measured rather than estimated. Then [choosing a video model](references/video-models.md), [prompting a video model](references/video-prompting.md), [voice](references/video-voice.md), [music and sound design](references/video-music.md), [assembly](references/video-assembly.md) and the [measurable checks](references/measurable-checks.md). [Thresholds](references/thresholds.md) holds the numbers and their provenance; [compliance](references/compliance.md) holds the claims red line.

## Basic and advanced

Follow [models](references/models.md). Basic is a compact evidence-based workflow; advanced develops competing hypotheses, real prototypes and deeper critique. The mode is a choice, not a model tier: whichever model this host exposes can run either mode. Neither profile promises a performance multiplier.

## Campaign and learning

Use [campaign operations](references/campaign-operations.md) for authorized account changes. Preparing creative does not authorize activation. Use [memory and experiments](references/memory-testing.md) and the second brain to record what was actually learned, failures included.

Deliver what exists, following the [output standard](references/output-standard.md): the file when there is one, captions and transcript, the script, the voice and settings manifest, rights notes and QA evidence. Distinguish draft, generated, rendered, reviewed, approved, uploaded and live. Run the included [artifact checker](scripts/check_artifact.py) on the brief, the storyboard, the creative set and any generation request; a non-zero exit is a stop, not a note. It checks structure and recorded authorization and refuses credential-shaped values; it does not certify truth, policy or quality. With no interpreter, say the checks did not run.
