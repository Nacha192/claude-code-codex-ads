# Static ads

Two production routes. They are not interchangeable, and picking the wrong one
costs a day.

| Route | Use when | Cost per variant after setup |
|---|---|---|
| **The engine** — HTML/CSS templates rendered to PNG | you want many coherent variants, exact typography, exact character counts, and a red-line check that actually runs | minutes |
| **The generator** — an image model renders the whole creative | you need a scene or a subject that does not exist as a photograph, or a look no layout can produce | a call, and money, per image |

Most ecommerce batches want **the engine for layout and text**, and the
**generator for the photograph that goes inside it**. Text rendered by an image
model is the single most common reason a batch looks amateur: wrong kerning,
invented glyphs, a headline that says something slightly different from what you
asked, and a character count you cannot verify.

If you take one rule from this file: **generate the picture, typeset the words.**

---

## Route A — The engine

### The idea

You do not lay out each ad by hand. You write **one HTML file** containing every
layout as a CSS-styled template, selected by a URL parameter, and a headless
browser screenshots each one at each ratio.

```
ads/
  engine.html          every layout, every text string, one file
  render.mjs           headless browser → PNG, all ratios
  redline_check.py     runs on the RENDERED text
  img/                 photography, cutouts
  SOURCES.txt          where each image came from and under what licence
  out/
    4x5/  9x16/  1x1/  1.91x1/
```

`engine.html?ad=3&r=45` renders layout 3 at 4:5. `render.mjs` loops every
layout across `ratios.required_set` and writes PNGs at the pixel sizes in
`thresholds.md`.

### Why this beats a design tool for paid social

- **Twenty coherent variants in seconds**, because a variant is a string change.
- **Character counts are real**, because the string is in a file you can count.
- **The red line can be enforced mechanically** on what the ad actually
  displays. See `compliance.md`.
- **The whole batch is a diff**, so you can see what changed between v10 and v11
  and so can the next person.
- **Every ratio comes out of the same source**, so the 9:16 is not a crop of the
  4:5 with the headline sliced off.

### Setup

1. Copy `scripts/ad_engine_template.html` into the project as `engine.html`.
2. Set `:root` to the brand colours and fonts. Two colours and one typeface is
   almost always better than what you were about to do.
3. Set the canvas to the 4:5 base and let the render scale it. Do not change
   the base ratio per layout; change the layout.
4. Point the image constants at `img/`.
5. Write the layouts. Each is a small function returning HTML; the text lives in
   the function, so the whole batch is greppable and diffable.

### Rendering

```bash
node scripts/render_ads.mjs            # all layouts, all required ratios
node scripts/render_ads.mjs --ad 3 --ratio 9x16
python scripts/redline_check.py        # exits non-zero on a hit
```

Wire the red-line check **before** the export step. A violating creative must
not be able to reach `out/`.

### Typography that survives a phone

- **The hook is the largest thing on the canvas.** If a reader has to look for
  it, the layout has failed regardless of how good the line is.
- **One typeface**, two weights. A second family is a decision that needs a
  reason.
- **Never place text closer to an edge than `ratios.safe_margin`.** On 9:16,
  respect the top and bottom reserves too — the platform paints its interface
  over yours there, and your call to action ends up under a profile picture.
- **Test at thumbnail.** Shrink the export to 120 px wide and look at it. If the
  hook is unreadable, it is unreadable in the feed, because that is roughly the
  attention the first pass gives it.
- **Burned-in text is not the primary text.** They are two different messages
  with two different jobs. Repeating the caption on the image wastes the image.

### The layout library

Sixteen structures that cover almost every static brief. Each is a **layout**,
not an angle: the angle comes from `hooks.md` and drops into the layout.

| # | Layout | What it does | Watch out for |
|---|---|---|---|
| 1 | Feature quad | product plus four benefits in cards | reads as a spec sheet if the benefits are features |
| 2 | Without / with | two real photographs, side by side | the "without" must be genuinely recognisable, not a strawman |
| 3 | Testimonial | a real customer quote | needs a real review **and** written permission. See `compliance.md` |
| 4 | Before / after | the transformation | forbidden or restricted for bodies in most regulated categories |
| 5 | Offer | price, code, deadline | works in retargeting, rarely cold. A discount is not an angle |
| 6 | Social proof | rating, count, one quote | every number needs a source |
| 7 | Ugly ad | plain text, imperfect photo, native look | must actually be plain. A designed "ugly ad" fools nobody |
| 8 | Brand / values | origin, guarantee, commitment | only lands past the first click. Weak for cold |
| 9 | Reverse psychology | "do not buy this if…" | the disqualifier has to be true |
| 10 | Notice | a sign, a warning card, a label | reads as clickbait if the payoff is thin |
| 11 | Curiosity object | the product, isolated, oddly framed | needs a genuinely odd frame, not a packshot |
| 12 | The clock | a time, a state, nothing else | the strongest cold opener for a recurring problem |
| 13 | Projection | the desirable after-state as a scene | slides into stock-photo territory fast |
| 14 | Detail macro | one physical detail, very close | only if the detail is the reason to buy |
| 15 | Comparison table | you versus the workaround | never versus a named competitor without documentation |
| 16 | Native screenshot | a message, a note, a review, framed as itself | must never impersonate a real platform's interface or a real person |

Layouts 9 to 16 are single-idea concepts: one benefit, no price, no
specification list.

### Visual variants are V1/V2/V3, and they are a different axis from copy

This trips people, so the labels are deliberately different.

- **Copy variants are A, B, C.** Defined in `copywriting.md`: A is the
  reference, B changes the opening move, C changes the length.
- **Visual variants are V1, V2, V3.** V1 is the reference, V2 changes the
  headline treatment, V3 changes the colour or the image.

**Never cross the two axes in one test.** Shipping copy B with visual V3 against
copy A with visual V1 changes two elements, which violates
`test.one_change_rule` and produces a result that applies to nothing. Test one
axis at a time: hold the visual and vary the copy, or hold the copy and vary the
visual, and say in the file which you held.

Name the files accordingly: `ad-03-the-strap-holds--A-V1.png`. Ugly, and it is
the difference between a readable test and a fortnight of noise.

---

## Route B — The generator

Read `generation-tools.md` first. Nothing is generated before the user has
chosen the tool and confirmed the run (`gen.ask_before_first_call`).

### What to ask a generator for

**The photograph, not the advertisement.** Ask for a scene, a subject, a
material, a light. Then typeset the words over it in the engine.

Prompts that work for ad photography share a shape:

```
<subject, concrete and singular>, <what it is doing>, <where>,
<light: source, direction, quality>, <camera: lens, distance, angle>,
<mood in two words>, <what is NOT in frame>
```

Naming what is **not** in frame does more work than any adjective. "No text, no
logo, no hands, no other objects on the surface" removes the four things a model
adds by default.

### Rules

- **Aspect ratio at generation, not by cropping.** Ask for the frame you need.
  A 4:5 cropped out of a 16:9 loses the composition you paid for.
- **Reference images beat adjectives.** If the tool takes a reference, give it
  the product photo. Describing your product in words to an image model
  produces a different product.
- **Check the output against reality.** A generated version of a real product is
  a lie about the product if it shows features it does not have. This is not a
  style question; it is a misleading-advertising question.
- **Faces**: a generated face that resembles a real person is a likeness
  problem. A generated face presented as a customer is a fabricated
  testimonial. Neither is fixed by a disclaimer.
- **`gen.max_retries_per_asset` is two.** On the third failure the prompt is
  wrong, not unlucky. Stop and change the prompt, or change the approach.
- **`gen.verify_on_disk`**: read back the file and its dimensions before
  reporting anything as produced.

---

## The batch checklist

Before anything leaves `out/`:

1. Red-line check on rendered text: exit code 0.
2. Character counts verified in the shipped language, all fields.
3. Every ratio in `ratios.required_set` present for every creative.
4. Thumbnail test passed at 120 px.
5. Safe margins respected, including the 9:16 top and bottom reserves.
6. `SOURCES.txt` complete: every image, its origin, its licence.
7. Claims sourced, or marked and pulled from the shippable set.
8. Awareness levels counted (`coverage.awareness_spread`) and the ad set plan
   stated.
9. File names carry the angle, not a number:
   `ad-03-the-strap-holds.png` beats `final_v2_FINAL.png` by more than it looks.

---

## Versioning

Ship a batch as `v<N>`, never overwrite `v<N-1>`, and keep a one-page
`v<N>/README.md` recording what changed and why.

Two reasons, both learned the expensive way. The account will ask in six weeks
which creative was live in March. And a batch that cannot be compared to the
one before it produces no learning, only files.
