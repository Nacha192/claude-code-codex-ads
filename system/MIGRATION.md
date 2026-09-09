# Migration from the initial distribution

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
