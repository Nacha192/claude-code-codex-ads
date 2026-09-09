# The production contract: idea to inspected files, in one pass

This is the spine of the motion packs. Everything else here is a chapter of it.

The promise is narrow and it is the whole product: **from an imperfect input, reach
real video files that were rendered, measured, inspected and corrected, without
interrupting the person who asked more than once.**

One shot does not mean improvising. It means one compact round of genuinely blocking
questions, a reasonable decision on everything else, stated out loud, and then a run
that goes all the way to files and a QA report.

The state of the work lives in one object, `motion-project.json`, described in
[the manifest](motion-manifest.md). Every phase below writes into it. A phase that
did not write into it did not happen.

---

## Phase 1. Normalise the input

Accept whatever arrives: a sentence, an idea, a half-written script, a link to an ad
someone liked, a folder of assets, or a complete brief. All of them are valid
entry points and none of them is a brief yet.

Turn it into a structured brief and sort what is missing into three piles.

**Blocking.** Work built on a wrong answer here is rebuilt, not corrected.

| Blocking input | Why it cannot be assumed |
|---|---|
| Product or offer, in exact terms | Every claim and the CTA rest on it |
| Primary audience | The angle is chosen against a person, not a category |
| Conversion objective | A sale, a lead and an install are three different videos |
| Language and market | Ads are written in the market's language, never translated into it |
| Duration or duration range | Decides the number of scenes before anything is written |
| Formats requested | Decides how many compositions exist, per [assembly](video-assembly.md) |
| CTA destination | The ad promises what the destination has to keep |
| Brand constraints | Typeface, colour, what may never be shown |
| Proof available for the claims | Decides which claims are allowed at all, per [compliance](compliance.md) |
| Rights on supplied assets, voices and media | Decides what may be used, per [real production](live-action.md) |

**Assumable.** Pick a reasonable value, write it into `assumptions` with what it is,
why, and what changes if it is wrong. Tone within the agreed register, pacing, scene
count, music genre, caption style, colour weighting, the order of the proof.

**Optional.** Do not ask. If the answer would not change the work, it is not a
question, it is small talk.

**Ask the blocking ones once, together, numbered, in a single message.** The
interview, one question at a time, is what turns a one-hour job into three days.
See [one shot](one-shot.md) for the general rule; this table is its motion form.

---

## Phase 2. Creative lock

Before any production, freeze the argument. Thirteen fields, in `creative_lock`:

insight, problem, angle, promise, mechanism, proof, objection, cta, register,
emotion, hook, reason to keep watching, payoff.

The manifest refuses an empty one. That is deliberate: a video whose author cannot
name the main objection has not decided what it is arguing against, and it shows at
0:09 when the viewer thinks of it first.

**Hooks are generated in quantity and selected with a reason.** At least three, each
scored on seven criteria:

| Criterion | The question |
|---|---|
| Specificity | Would this fit a competitor with the name swapped? Then it is not a hook. |
| Speed of understanding | Is it understood before it is finished? |
| Audience fit | Does it speak to the person in the brief, or to the category? |
| Tension | Is there a reason for the next second to exist? |
| Continuity with payoff | Does the end answer this exact opening, or a different one? |
| Credibility | Does it survive the viewer's reflex that this is an ad? |
| First-frame strength | Is there something to see at frame one, not just something to read? |

Scoring is creative ranking. **It is not evidence of performance** and it never
becomes one, per [output standard](output-standard.md). The selected hook records
`why` it won and that sentence goes in the delivery.

---

## Phase 3. Script and storyboard

The script is written to be **spoken**, which is a different craft from written copy.
Read it aloud. If you would not say it, rewrite it.

- A reason to keep watching arrives before it is asked for.
- Something new arrives regularly: information, an image, a turn, a proof.
- The argument progresses. Restating is not progressing.
- The promise is made credible in the same breath it is made.
- Only claims that appear in `claims` with a real proof id.
- The CTA matches the actual offer, not a softened version of it.

The storyboard is scene by scene, and every scene carries all of it:

| Field | Why it is not optional |
|---|---|
| start, end | The timeline is the only thing that makes narration fit checkable |
| narration | The exact words, not a summary of them |
| on_screen | What is burned in, which is a separate channel from the voice |
| role | hook, mechanism, proof, objection, payoff. A scene with no role is a scene to cut |
| composition | Where things are, in words precise enough to build from |
| subject | What the eye is meant to land on |
| primary_motion | The movement that carries the meaning |
| secondary_motion | The movement that carries depth |
| transition | And why it is that one |
| assets | Ids that must exist in `assets` |
| sound | Effect, music change, or deliberate silence |
| reframing | What changes in the other ratios, not "crop it" |
| legibility_risk | The thing most likely to be unreadable here |
| acceptance | The observable condition that decides this scene passed |

**Timing comes from the voice as soon as the voice exists.** Word counts estimate;
a rendered take measures. `measured_voice_seconds` is filled from the file, and the
manifest refuses a line that measures longer than the scene holding it.

---

## Phase 4. Art direction

Choose a direction from [art direction](art-direction.md) against the brand, the
audience, the offer and the channel. There is no house style here, and imposing one
would make every client's ad look like every other client's ad.

The rule that survives every direction: **no motion for motion's sake.** Every
animation earns its place by serving comprehension, hierarchy, tension, proof,
continuity, emotion, or the passage to the next idea. If it serves none of them, it
is decoration and it costs attention.

---

## Phase 5. Rhythm and retention

Read [retention](video-retention.md). The pacing follows the material, not a rule:
information density, the voice, the register, the audience's awareness level, visual
complexity, duration, channel, and how tired the previous ten seconds already made
the eye.

**A cut is one attention reset among many.** A new composition, a scale change, a
sound break, a proof, a tempo change, a reveal, a new point of view, a deliberate
silence, or a sudden simplification all do the same job, and several of them do it
without the exhausting chop that makes an ad look like every other ad.

---

## Phase 6. Voice, captions, audio

Full pipeline in [voice](video-voice.md) and [music](video-music.md). The contract
here: the voice archetype is chosen and recorded, the take is measured against the
script, captions are derived **from the final take** and never from the script, the
music ducks under the voice, and the loudness target is declared with its origin.

The manifest refuses `derived_from` set to anything but `final_take`, and refuses a
loudness target with no `source`. A number with no origin is a preference wearing the
costume of a standard.

---

## Phase 7. Multi-format production

Every requested ratio gets **its own composition**, per [assembly](video-assembly.md).

Never produce a vertical by blind-cropping a horizontal master. The manifest refuses
a format whose `composition` is empty, and the formats that are mandatory are the
ones the brief asked for. There is no universal required ratio, and inventing one
would be this pack imposing its taste as a platform requirement.

---

## Phase 8. The correction loop

The first render is not the deliverable. It is the input to this loop.

1. **Measure** every export with `scripts/inspect_video.py`. It decodes the whole
   file, because a container claiming 20 seconds and failing at 14 is exactly what
   metadata will not tell you. [Measurable checks](measurable-checks.md) explains
   each measurement and gives the single command behind it, for the times a result
   has to be understood or reproduced by hand.
2. **Inspect** with both grids: the technical one the script produces, and the
   human one in [creative QA](creative-qa.md). They are separate and neither
   substitutes for the other.
3. **Record** every defect with a timecode, an observation, a severity, why it
   fails, the concrete fix, the file or scene to change, and a status.
4. **Fix the source**, never the export. Patching a rendered file makes the next
   render undo the fix.
5. **Re-render only the affected formats.** Re-rendering all of them wastes time and
   hides which one was broken.
6. **Re-run every check that touched the change.**
7. **Deliver only when no blocking defect is open.**

**Cap the loop.** Three passes. If a defect survives three passes, stop and produce a
diagnosis: what the defect is, what was tried, why it did not work, and what a human
would need to decide. An unbounded loop is not persistence, it is a hang.

---

## What may never be claimed

- **A file that does not exist.** If nothing was rendered, say so. A prompt, a
  storyboard and a script are a real deliverable; calling them a video is not.
- **A check that did not run.** No interpreter, no ffmpeg, no capability: say which,
  and that the checks did not run. Silence reads as a pass.
- **A technically valid export as a good ad.** Every threshold in
  `inspect_video.py` can pass on an ad nobody would watch. The technical grid says
  the file is sound. Only the creative grid, run by someone looking at it, says the
  ad is worth putting money behind.
