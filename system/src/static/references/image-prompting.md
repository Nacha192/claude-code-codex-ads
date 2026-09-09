# Prompting an image model for an ad

Documentation snapshot: 2026-09-09, from the OpenAI image generation guide. Model
names and parameters move faster than any document. Inspect the tool actually
connected to this session before naming a model, and treat everything below as a
starting point to verify rather than a fact to quote.

A generated image fails as an ad in three specific ways, and all three are avoidable
in the prompt rather than in the retouch.

1. **It invents the product.** A model asked for "our water bottle" makes a bottle.
   It is not the one being sold, and the ad is now a claim about a product that does
   not exist. Composite the real product, or edit from a real photograph.
2. **It bakes the text in.** Type inside the pixels cannot be corrected, translated,
   re-sized for a second placement or made legally accurate. Prices and legal terms
   inside a generated image are the fastest route to an ad you have to pull.
3. **It fills the frame.** A beautiful centred composition with no quiet area leaves
   the headline nowhere to go, so the copy lands on top of the subject and both lose.

---

## The prompt, in the order the model reads it

Front-load what must be true. Models weight the beginning of a prompt more heavily,
and the last clause of a long sentence is the first thing dropped.

| Slot | What goes in it | Why it is not optional |
|---|---|---|
| **Subject** | The one thing the picture is of, in five words | A prompt with two subjects returns a compromise between them |
| **Product truth** | Geometry, colourway, label, material, scale, what it attaches to | This is the sentence that stops the model designing a competitor |
| **Framing** | Shot size and angle, and **where the empty area is** | The empty area is where the headline goes. Name it or lose it |
| **Light** | Direction, hardness, colour temperature, time of day | The single biggest lever on whether it reads as an ad or as stock |
| **Surface and context** | What it sits on, what is behind, how far back | Decides whether it looks like a situation or a cut-out |
| **Lens** | Focal length and depth of field, in real terms | "35mm, deep focus" beats "cinematic" every time |
| **Palette** | The brand tokens, as values | A model given hex values holds them; given "warm and premium" it does not |
| **Exclusions** | No text, no logo, no watermark, no extra hands | Say it. Every model adds text unasked when the subject is commercial |

A worked example, structured rather than poetic:

```
A stainless steel insulated flask, 750 ml, matte charcoal body with a brushed
steel collar and a black screw lid, no printed logo.
Framing: three-quarter view, product in the lower right third, upper left third
deliberately empty for a headline.
Light: single soft key from the upper left, hard-edged shadow to the right,
late afternoon, no fill.
Surface: raw concrete ledge, blurred kitchen depth behind it, two metres back.
Lens: 50mm, f/2.8, product fully sharp, background soft.
Palette: charcoal 0x2B2F33, steel 0xB8BEC4, one accent of 0xF5A623 in the
background only.
No text, no logo, no watermark, no packaging, no hands.
```

**Then edit rather than re-roll.** A second generation gives a different product. An
edit from the first, with the reference image and a mask, keeps it. This is what the
reference-based editing path with an input fidelity setting exists for, and it is the
difference between a campaign that looks like one product and a campaign that looks
like a catalogue of near-misses.

---

## Canvases, and the trap in them

The guide lists `1024x1024`, `1536x1024` and `1024x1536` as the recommended sizes,
plus custom `WIDTHxHEIGHT`. The custom rule it states: **both edges multiples of 16**,
aspect ratio between 1:3 and 3:1, no edge over 3840, and a total between 655,360 and
8,294,400 pixels.

That rule collides with Meta's canvases, and quietly. **1080 is not a multiple of 16**
(1080 ÷ 16 = 67.5), and neither is 1350 or 1920. So the sizes every ad guide tells you
to use cannot be requested directly. Generate at the nearest legal size with the
**exact same ratio** and resample down.

| Placement | Meta canvas | Ask the model for | Why that number |
|---|---|---|---|
| Feed portrait | 1080 × 1350 (4:5) | **1088 × 1360** | 64k × 80k with k = 17. Exactly 0.8 |
| Reels, Stories | 1080 × 1920 (9:16) | **1152 × 2048** | 144k × 256k with k = 8. Exactly 0.5625 |
| Feed square | 1080 × 1080 (1:1) | **1088 × 1088** | Or the native 1024 × 1024 |
| Landscape | 1920 × 1080 (16:9) | **2048 × 1152** | 256k × 144k with k = 8 |

Generate slightly **above** the delivery size and downscale. Upscaling a generated
image to reach a canvas softens exactly the edges the eye uses to judge whether a
product photograph is real. If the multiple-of-16 rule has changed since this snapshot,
the arithmetic above is how to recompute: pick the smallest whole `k` that clears your
delivery size.

---

## Parameters worth setting deliberately

Observed on the guide at the snapshot date. Verify against the connected tool.

| Parameter | Values | When it matters for an ad |
|---|---|---|
| `quality` | `low`, `medium`, `high`, `xhigh`, `max`, `auto` | Explore at `low`, deliver at `high` or above. Exploring at `max` burns the budget on compositions you will throw away |
| `background` | `transparent`, `opaque`, `auto` | `transparent` with a `png` or `webp` output is how you get a product cut-out to composite under real type |
| `output_format` | `png`, `jpeg`, `webp` | `png` for anything with transparency or hard edges, `jpeg` only for the final flattened upload |
| `output_compression` | 0 to 100, `jpeg` and `webp` | Leave it high. Compression artefacts around type look like a low-effort ad |
| `n` | 1 to 10 | Batch the exploration, not the delivery. Ten finals is ten times the spend on nine images nobody will use |
| `moderation` | `auto`, `low` | Leave it at `auto`. Lowering the filter on a commercial image is a decision you will have to explain |
| `input_fidelity` | for reference-based editing | The lever that keeps a real product looking like itself across a set |

Model families named in the guide at the snapshot: `gpt-image-2`, and the
`gpt-image-2.5-sunburst` and `gpt-image-2.5-flare` variants, the first oriented to
editing precision and the second to fast everyday generation. **Dated deprecations
worth knowing before writing a pipeline:** `gpt-image-1` is listed for shutdown on
2026-10-23, and `gpt-image-1-mini`, `gpt-image-1.5` and `chatgpt-image-latest` on
2026-12-01, with `gpt-image-2` named as the replacement. `dall-e-2` and `dall-e-3`
were shut down on 2026-05-12. A prompt library pinned to any of those has an expiry
date on it.

---

## The batch, and what it costs to get wrong

Explore wide and cheap, then commit. Four compositions at low quality cost less than
one at maximum, and the composition is what you are actually choosing between.

- **One variable at a time.** Changing the light and the framing together tells you
  nothing about which one helped.
- **Keep the seed of what worked**, and edit from it. A campaign is a set that looks
  related; four independent generations do not.
- **Every generated image is registered as an asset** with its rights, per the shared
  contract in [core](core.md). "The model made it" is not a rights statement.
- **Approval before spend**, recorded as a `generation_request` and checked by
  `scripts/check_artifact.py`. Changing provider, model or account after the approval
  fails that check by design, and it should.

## What the model cannot decide for you

Whether the picture argues for the product. A technically flawless image of the wrong
idea is the most expensive output in this whole pipeline, because it looks finished.
Go back to [static production](static.md) for the visual role the image is supposed to
play, and choose that before writing a prompt.
