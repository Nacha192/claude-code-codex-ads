# Prompting a video model

How to ask for a shot and get it. Read `video-models.md` for which model to ask,
and `providers.md` for the gate that stands in front of all of them.

**One rule before all the others: ask for one shot, not one video.** Current
models hold a few seconds of coherence. A 30-second prompt returns 30 seconds of
drift. Generate short beats and cut them together, and write the edit so the
inevitable drift lands on a cut.

**3 to 6 seconds is an editing heuristic, not an API parameter.** It is the beat
length that cuts well and holds coherence. Every endpoint has its own accepted
durations, and some accept nothing near it. Read the schema of the model you are
actually calling, use a duration it accepts, and if that duration differs from
what was authorised — in length or in cost — say so before running, not after.

---

## The four-part prompt

Every usable prompt answers four questions. Missing one is where the model
invents.

**Subject** — what is in frame, concretely and singular.
**Look** — the light: its source, direction, quality, and time of day.
**Camera** — angle, distance, movement, depth of field.
**Technical** — ratio, duration, and the style register.

Written out:

```
Subject:   A glass bottle of amber serum on a marble counter, alone.
Look:      Soft morning light from the left, gentle highlights on the glass.
Camera:    Slow push-in, medium to close, shallow depth of field.
Technical: 9:16, 5 seconds, photorealistic product photography.
```

Four lines. It takes a minute and it removes most of the failure modes below.

---

## Stopping the model from inventing

Models hallucinate when a prompt is ambiguous, contradictory, or physically
impossible. Six rules, in order of how much they save you:

1. **Say what is NOT in frame.** This does more work than any adjective. "No
   text, no logo, no hands, no other objects on the surface" removes the four
   things models add by default.
2. **Be spatially explicit.** "The bottle on the left, the plant on the right",
   not "a bottle near a plant".
3. **Cap the entities at three.** More subjects means more merging and
   distortion. A crowd is one entity; four named objects are four.
4. **Describe what is there, not what is absent.** "An empty café with wooden
   chairs" works. "No people in the background" often produces people, because
   the word arrives without its negation attached.
5. **Anchor with a real reference.** "Lit like a magazine cover shoot" beats
   "beautiful professional lighting", which means nothing to a model.
6. **State quantities.** "Two cups", "a single person". "A person" routinely
   produces several.

### The failures worth designing around

| You asked for | You get | Do this instead |
|---|---|---|
| A person holding the product | distorted hands | close on the product on a surface, hands out of frame. Or image-to-video from a real photo |
| Text on the label | garbled glyphs | generate without text, typeset it after. See `static.md` |
| Several people talking | merged faces | one person per shot, composite in the edit |
| A brand logo | a distorted logo | overlay the real logo in post, never in the prompt |
| A complex physical interaction | physics breaks | split into two simpler shots and cut between them |
| A likeness of a real person | legal exposure and a poor result | describe attributes. Never name a real person |

That last row is not a quality note. A generated likeness of a real person in a
paid ad is an impersonation problem, and no disclaimer fixes it.

---

## Camera vocabulary

Models understand film terms better than casual description. Use them.

| Movement | What it does | Reach for it when |
|---|---|---|
| Push-in | moves toward the subject | building toward a detail |
| Pull-back | moves away | a reveal, or establishing context |
| Tracking | follows laterally | energy, movement |
| Pan / tilt | rotates on axis | scanning, revealing height |
| Orbit | circles the subject | a product turn |
| Handheld | slight natural instability | UGC, documentary |
| Static | nothing moves | product shots, clean compositions |
| Slow motion | reduced speed | emphasising an action, luxury |

| Angle | Reads as | Use for |
|---|---|---|
| Eye level | neutral, equal | talking head, demonstration |
| Low | powerful, aspirational | hero shots |
| High | overview, diminished | establishing, flat lay |
| Top-down | geometric, clean | flat lay, food, layouts |
| Over the shoulder | intimate, first person | unboxing, UGC |
| Dutch | unease | rarely. It is almost always wrong |

**One movement per shot.** A push-in that also orbits while the subject walks is
three instructions competing for four seconds, and the model resolves the
conflict by doing none of them.

---

## Registers

Ask for the register explicitly, because the default is "cinematic" and most
paid social does not want cinematic.

**UGC.** Phone camera quality, natural indoor light, slightly imperfect framing,
handheld. Say **"phone camera, not cinematic"** outright. Models trend toward
polish, and polish is what makes a UGC ad read as an ad.

**Demonstration.** Static or locked off, even light, the object filling a third
of frame, nothing else on the surface. Boring on purpose. Clarity is the whole
job.

**Cinematic.** Golden hour, long shadows, shallow depth, anamorphic flare if you
must. Right for brand, usually wrong for direct response, and expensive in
attention: it signals "advertisement" in the first frame.

**Editorial.** Soft natural light, one subject, generous negative space, muted
palette. The register that ages best.

### Three formulas that work

Fill in the brackets. Do not ship them as written; they are a starting shape.

**Unboxing**
```
A [age range] person sitting [location], opening a [colour] package.
Natural [time of day] light from a window, warm.
Medium close-up, slightly shaky handheld, phone camera quality.
Genuine surprise. 5 seconds, 9:16.
Not in frame: text, logos, other people.
```

**Demonstration**
```
[Product] on a [surface], centred, alone.
Even soft light, no strong shadows.
Static locked-off shot, product fills one third of the frame.
[The single action, in one clause]. 5 seconds, 9:16.
Not in frame: hands, text, other objects.
```

**Service, the work itself**
```
A [role] at [the actual workplace], [doing the specific action].
Natural light from [direction], realistic, not styled.
Medium shot, gentle handheld, shallow depth.
5 seconds, 9:16. Documentary register, not corporate.
Not in frame: stock-photo gestures, handshakes, meeting tables.
```

---

## Continuity across shots

The hard part, and the reason most generated ads look assembled rather than
filmed.

- **Repeat the invariant clause verbatim** in every prompt of a sequence: the
  same wardrobe, the same room, the same light direction, the same lens. Any
  paraphrase is a change.
- **Use a reference image** where the model accepts one. It beats every
  adjective you could write, especially for a real product.
- **Accept some drift and edit around it.** Put a cut, a text card, or a
  different angle at the moment the drift would be visible.
- **Generate the product shots from a real photograph**, image to video, not
  from a description. A described product is a different product, and shipping
  it is a misleading advertisement.

---

## The three-pass check, before anything reaches the edit

Every generated asset. Thirty seconds total.

**Physics.** Does gravity hold? Do shadows match the light source? Are
reflections plausible? Are proportions right?

**Detail.** Hands: the right number of fingers, in natural positions? Text:
readable, or garbled and to be replaced? Faces: symmetrical, expressions not
uncanny? Edges: clean between objects?

**Brand and truth.** Does the light match the brand? Is the palette right? And
the one that matters most: **does this shot show the product doing something it
actually does?** A generated feature the object does not have is not a style
choice.

> **A synthetic demonstration is not evidence that the product works.** A
> generated shot of the strap holding, the stain lifting, the seal closing, is a
> drawing of a claim, not a test of it. It may be used to *illustrate* a
> behaviour you have verified in the real world; it may never be the basis for
> asserting one. If nobody has watched the real object do the thing, the claim
> has no source and `output-standard.md` applies: mark it, and keep it out of
> the shippable set. This is the fastest way a generated ad becomes a
> misleading one, and it happens without anyone deciding to lie.

Failing any pass means regenerating with an adjusted prompt, not fixing it in
post. Post is slower and the result is worse.

`gen.max_retries_per_asset` is two. On the third failure the prompt is wrong,
not unlucky. Change the prompt or change the approach.

---

## Audio

**Generate silent.** Model-generated speech and ambient audio are where the
uncanny sits, and audio is the channel you can most cheaply fix afterwards.

Add the voice deliberately, per `video-voice.md`, and the music per `video-music.md`.
The one exception is a model whose whole point is synchronised dialogue, and even
then, check the pronunciation of the brand name before anything else.

---

## What to record next to every generation

Without this you cannot reproduce the shot that worked, which is the only shot
you will want again.

```
shot-03.mp4
  prompt:     <the exact text, verbatim>
  model:      <name and version>
  reference:  <image path, if any>
  seed:       <if the tool exposes one>
  duration:   <seconds>   ratio: <9:16>
  attempts:   <how many, and what changed between them>
  verdict:    <kept | cut, and why in one line>
```

The "what changed between them" line is the one that teaches you the model. It
is also the first thing everybody stops writing down.
