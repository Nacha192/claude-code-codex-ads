# Creative QA: the pass no script can run

`inspect_video.py` decides whether the file is sound. This decides whether the ad is
worth money. They are different questions and an export can pass the first while
failing the second completely, which is the most expensive failure in this pack
because it looks like success.

Run this on the exported file, at playback size, with sound, then again muted. Not on
the timeline, not on the storyboard, not on your memory of building it.

Every failure produces a defect record with the seven fields in
[the manifest](motion-manifest.md), and lands in `qa.creative`.

---

## The grid

### The first two seconds

| Question | Fails when |
|---|---|
| Is the first frame understandable at thumbnail size? | You have to squint, or it is a logo, or it is black |
| Is the hook understood with the sound off? | The meaning lives only in the voice |
| Is there something to see at frame one, not only something to read? | The frame is a text card |
| Does the first second give a reason for the second one? | It opens on setup |

### The argument

| Question | Fails when |
|---|---|
| Does the promise arrive fast enough for this audience? | A cold viewer waits past 0:05 to learn what this is |
| Do the hook and the payoff talk about the same thing? | The end answers a question the opening did not ask |
| Does every scene move the argument forward? | A scene restates the previous one in new words |
| Does the video show proof, or only assert? | Every claim is spoken and none is demonstrated |
| Is the main objection addressed inside the ad? | The obvious doubt is never named |

### The craft

| Question | Fails when |
|---|---|
| Does the motion improve comprehension? | Removing an animation would change nothing |
| Is the visual hierarchy immediate? | The eye hunts for what matters |
| Are the captions readable? | Contrast, size, or they sit under the platform overlay |
| Does the art direction look specific to this brand? | Swap the logo and it fits a competitor |
| Do any shots look like a stock template? | Generic icons, floating shapes, default transitions |
| Are the rhythm changes motivated? | The pace changes because the editor got bored |

### Sound

| Question | Fails when |
|---|---|
| Does the voice sound human and right for the register? | Wrong energy, wrong age, uncanny delivery |
| Does the music support the rhythm without covering the voice? | You lean in to catch a word |
| Is silence used anywhere on purpose? | Wall-to-wall sound with no rest |

### The end

| Question | Fails when |
|---|---|
| Is the CTA clear, credible and visible? | It is implied, or it appears for under a second |
| Does the last frame leave the brand identifiable? | It could be anyone's ad |
| Does the destination keep the ad's promise? | The page says something else, or in other words |

### The two blind runs

| Run | The bar |
|---|---|
| **Muted, all the way through** | Every argument is still made. This is how most of it will be seen. |
| **Eyes closed, all the way through** | The audio alone still makes sense, and does not depend on unseen text |

An ad that only works in one of the two runs is an ad that works for half the
audience.

### The render itself

| Question | Fails when |
|---|---|
| Any artefact, jump, or broken detail? | Compression mush on a fast pan, a jumping baseline, a clipped glyph |
| Anything that looks like a bug rather than a choice? | A frozen frame, a flash, a stray element |

---

## Scoring it honestly

Three verdicts, and the vocabulary is the one in
[quality control](quality-control.md): `pass`, `pass_with_noted_risk`, `fail`.

A failure on any question in **the first two seconds** or **the end** is blocking. The
rest is severity by judgement, recorded with a reason.

**Do not average.** Twelve passes and one blocking failure is a fail, not a 92
percent. This is one artifact, not a scorecard.

---

## Who runs it

**Not the one who built it.** In the solo packs, run it after a real break, on the
exported file, having deliberately forgotten the intention. In the team editions the
other side runs it and signs it, per [working as two](team.md), and
`qa.creative.reviewed_by` records who.

A creative pass with no reviewer recorded is a warning in the manifest on purpose. It
is the field most likely to be filled by the person who wanted the answer to be yes.
