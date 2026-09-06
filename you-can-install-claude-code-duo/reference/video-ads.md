# Video ads

A video ad is a hook with a body attached. Almost all of the money is decided in
`limits.video_hook_seconds`, and almost all of the effort usually goes
somewhere else.

---

## Decide the format before writing anything

| Format | Length | Carries | Costs |
|---|---|---|---|
| **UGC / talking head** | `limits.ugc_length_seconds` | trust, objection handling | a person, or a generated one with all the problems that brings |
| **Demonstration** | 8 to 20 s | a visible mechanism | a product that does something visible |
| **Motion static** | 4 to 10 s | a hook that was already strong as a still | almost nothing, if the engine exists |
| **Story** | 30 to 90 s | an unaware or problem-aware reader | a script that actually earns 90 seconds |
| **Rapid-fire** | 60 s and up | a warm audience that already knows the category | a lot of footage |

Match it to the awareness level from `intake-and-avatar.md`. A demonstration
shown to someone unaware demonstrates the answer to a question they have not
asked yet.

**Motion static is underrated.** A still that already works, with one push-in,
one text pop and a sound, is often the cheapest video in the account and beats
the elaborate one. Try it before commissioning a shoot.

---

## The two tests, run before production

**The mute test.** Play it with no sound. Do you understand it, and do you stay?
If no, it does not work in a feed, because the feed is muted by default
(`voice.sound_off_default`). This is not a preference — it is most of your
impressions.

**The thumbnail test.** Freeze frame one and shrink it to 120 px. Is there
anything there? The first frame is the whole of your first impression on a
scroll.

An ad that fails either of these is fixed at the storyboard, not in the edit.

---

## The opening: three channels in three seconds

Write these three lines together, before any body script exists:

1. **Spoken line** — `limits.hook_spoken_words`, counted in words, at ordinary
   delivery speed. Say it out loud with a timer once; you will cut two words.
2. **On-screen line** — `limits.onscreen_line_chars`. It must stand alone with
   sound off, and it must **not** transcribe the spoken line.
3. **Opening shot** — one sentence. Note whether the footage exists or must be
   produced; that difference decides whether the hook ships this week.

Then check the crop: a hook whose text or subject falls outside the frame at
9:16 has failed at the placement where most of it will be seen.

See `hooks.md` for the formula library and the scoring rubric. The score there
applies to video hooks unchanged.

---

## Structure

The shape that survives across formats:

| Beat | Seconds | Job |
|---|---|---|
| **Hook** | 0 – 3 | prove the ad is about their situation |
| **Escalation** | 3 – 6 | one new piece of information, or the hook was a bluff |
| **Workaround** | 6 – 12 | name what they do today, and where it fails |
| **Turn** | 12 – 18 | the product enters, as the answer to the failure |
| **Proof** | 18 – 30 | show it. A demonstration beats an adjective |
| **Offer + call to action** | last 5 | one action, stated once, plainly |

The **escalation** is the beat that gets skipped, and it is where retention
dies. At three seconds the platform has counted a view and the viewer is
deciding. If second four repeats second one — a logo, a slow pan, "hey guys" —
they are gone. Something must arrive by 0:03: a cut, new information, a second
hook, or visible progress.

Cite what is on screen **exactly at 0:03** when you review a script. If the
answer is "still the intro", rewrite.

---

## Writing the script

Write it as a shot table, not as prose. Prose scripts hide the fact that nothing
is happening on screen.

| # | Time | Shot | On-screen text | Spoken | Sound | Job |
|---|---|---|---|---|---|---|

Rules:

- **One idea per shot.** If a shot needs two sentences to explain, it is two
  shots.
- **Cut every 1 to 2 seconds in the first ten seconds** for UGC and rapid-fire.
  A static frame for six seconds is a scroll.
- **Burned-in captions on every spoken word.** Not a stylistic choice; it is the
  mute test.
- **The call to action is spoken once and shown once.** Twice reads as
  desperate and costs three seconds you could have spent on proof.
- **Never write a shot you cannot source.** Mark it `needs production` and let
  the person deciding see the cost.

---

## UGC without lying

UGC works because it reads as a person, not a brand. That is also exactly where
it goes wrong.

- **A generated person presented as a customer is a fabricated testimonial.**
  Not a grey area. See `compliance.md`.
- A generated or hired presenter demonstrating the product, speaking copy you
  wrote, is ordinary advertising and is fine — as long as nothing in the ad
  claims they are an independent customer.
- **A real customer needs written permission** before their face or words run in
  paid media.
- The details that make UGC land — the messy kitchen, the unbrushed hair, the
  bad light — are production choices you can make honestly. Do those.

---

## Generated video

Read `generation-tools.md` first, and honour `gen.ask_before_first_call`.

- **Shot by shot, not scene by scene.** Current video models hold a few seconds
  of coherence. Ask for 3 to 6 second shots and cut them together. A single
  30-second prompt returns 30 seconds of drift.
- **Continuity is the hard part.** Same subject, same wardrobe, same light
  across shots. Use reference images or a character sheet where the tool
  supports it, and accept that some drift will remain; write the edit so the
  drift lands on a cut.
- **Generate silent, add audio deliberately.** Model-generated audio is where
  the uncanny sits, and it is the channel you can most easily fix. See
  `voice.md`.
- **Product accuracy.** A generated shot of your product that shows a feature it
  does not have is a misleading advertisement, whatever the disclaimer says.
- **`gen.verify_on_disk`**: read back duration and dimensions before reporting a
  shot as produced.

---

## Editing

- **First frame is a decision.** Choose it; do not let the encoder choose it.
- **Cut on the beat** if there is music, and cut on the word if there is not.
- **Safe areas** from `thresholds.md`. On 9:16 the bottom fifth belongs to the
  platform.
- **Export per ratio from the edit**, not by cropping the export.
- **Under 4 MB per 15 seconds** as a working target for feed video; heavier
  files get re-encoded harder and your text goes soft.

---

## Reading a video ad afterwards

Two different failures, two different rewrites. Do not confuse them.

| Symptom | Key | Diagnosis | Fix |
|---|---|---|---|
| Nobody starts it | `early.hook_rate` | the opening does not stop the scroll | new hook: shot and line |
| They start and leave | `early.hold_rate` | the body does not pay off the opening | new body, keep the hook |

Three conditions before either read means anything, all in `thresholds.md`:

- **`early.min_exposure`.** Below it the creative has not had a chance, and its
  numbers are noise wearing a decimal point.
- **`early.duration_band`.** Compare within a band, never across one. Hold on a
  10-second ad and hold on a 45-second ad are different questions wearing one
  column name.
- **`early.median_stability_floor`.** Under five creatives in the band, the
  "median" is one middle number driving real cuts. The read is `needs_data`.

And `early.hold_rate` is defined on the 50% play, not on ThruPlay. ThruPlay is
completion **or** fifteen seconds, whichever comes first, so it means completion
on a short ad and fifteen seconds on a long one. A median mixing both is
meaningless.

Whatever these say, they carry `early.false_negative_rate` with them: roughly
one in five creatives cut this early would have gone on to win. That is the
trade being made for throughput, and the output states it rather than hiding it.
