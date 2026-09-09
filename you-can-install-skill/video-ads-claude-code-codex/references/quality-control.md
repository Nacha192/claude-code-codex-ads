# Quality control

Quality control is a pass made on the artifact, not on the intention. You are
not checking that you meant to do the right thing. You are checking the file
that exists, the words that will be read, and the numbers that will be acted
on.

It happens after the work and before the handover, every time, including when
the work went well. Especially then.

---

## Three layers, and only one of them is automatic

**What a script can decide.** Structure, character counts, dates, arithmetic,
declared prohibited terms against declared copy, whether a proof id exists,
whether an approval covers the batch. `scripts/check_artifact.py` does this.
A non-zero exit is a stop.

**What only an eye can decide.** Whether the image is legible on a phone,
whether the product in it is the real product, whether the hook lands, whether
the register is right, whether the page keeps the ad's promise. No script in
this pack, or any other, decides these.

**What nobody can decide yet.** Whether it performs. That is what the test is
for, per [memory and experiments](memory-testing.md).

Reporting layer one as if it covered layer two is the single most damaging
thing you can do here, because it produces a confident green light on work
nobody looked at.

---

## What the checker actually reads

`check_artifact.py` reads **a JSON manifest you wrote**. It never opens the
image, never decodes the video, never runs OCR, never hashes an asset.

The consequence is exact and worth stating plainly: **if your manifest does not
match what was rendered, the check passes and the ad is still wrong.** A
prohibited word burned into a generated image, absent from the manifest, exits
zero.

So the manifest is produced **from the render, not from the plan**. Export
first, read what is actually on the exported asset, write that into the copy
fields, then run the check. Writing the manifest from your intended copy and
then generating is the mistake this whole file exists to prevent.

The check is a manifest check. Media inspection is a separate, mandatory,
human-or-vision step that no exit code replaces.

---

## The inspection pass, per format

Open the exported file. Not the preview, not the API response, not the path
that was returned. **A successful API response is not a file.**

### Static and carousel

| Check | Fails when |
|---|---|
| Legibility at thumbnail size | Any word you need the reader to get is unreadable in a feed-size preview |
| Product truth | Geometry, colorway, label, material or scale differs from the real product |
| Text integrity | A generated image invented, misspelled or mangled letters, accents included |
| Safe zones | Text or product sits where the platform's own overlay lands |
| Crop per ratio | Every requested ratio was opened, not inferred from one approved frame |
| Copy match | On-image text equals the copy manifest, character for character |
| Offer qualifiers | Price, conditions and exclusions appear wherever the offer is stated |
| Destination | The link opens, and the page states the same offer in the same terms |

### Video

Everything above for the thumbnail frame, plus:

| Check | Fails when |
|---|---|
| First half-second | The scroll-stop is not in frame, per the pack's retention file |
| Audio present and levelled | Silence, clipping, or narration under the music bed |
| Caption sync and spelling | Captions drift, or contradict the spoken line |
| Narration fit | A line is measured, not estimated, and it exceeds its scene |
| Sound-off legibility | The ad makes no sense muted, which is how most of it will be seen |
| Rights | Every music, footage and voice element has a recorded usage right |
| Last frame | The CTA is readable and the brand is identifiable |

### Copy

| Check | Fails when |
|---|---|
| Language | Written in the market's language, not translated into it |
| Claims | A claim in the copy is absent from the claims list |
| Proof | A listed claim points at a proof id that does not exist or does not support it |
| Limits | Any field is over its declared character cap |
| Register | The vocabulary contradicts the register agreed at intake |

---

## Verdict vocabulary

Three words, and no others. "Looks good" is not a verdict.

- **Pass.** Every check above was run and cleared, and you name what you opened.
- **Pass with noted risk.** Cleared, but something is uncertain and the delivery
  says what, in one line, at the top. An unverified claim, an unread ratio, an
  untested destination.
- **Fail.** Something is wrong. It does not go out. Name the check, not the
  feeling.

Never soften a fail into a risk to avoid redoing work.

---

## In the team editions

**The one who built does not sign off.** Quality control is run by the other
side, on the exported artifact, without being told what to look at first.

That is the whole point of being two, and it is the part a single assistant
cannot fake. See [working as two](team.md). If the second side cannot open the
file, it says so and the pass is recorded as unrun rather than passed.

---

## What gets recorded

For every delivery, in the second brain:

- Which checks ran, which were skipped, and why.
- What was opened, by name, with the ratio or duration.
- The verdict, in the vocabulary above.
- Every risk accepted, and who accepted it.

An unrecorded quality pass did not happen. Six weeks later, the record is the
only thing that separates "we tested it" from "we think we tested it".
