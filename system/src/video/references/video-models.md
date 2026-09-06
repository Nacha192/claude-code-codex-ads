# Choosing a video model

Which model for which shot, and what each one fails at.

---

## Read this first, it is the point of the file

**Everything below is `url` evidence: read from public documentation and
comparisons, not observed by anyone in this pack running the model.** Nobody
here has generated a shot on Sora, Veo, Wan, or Higgsfield and measured the
result. Treat every line as a starting hypothesis to test cheaply, not as a
finding.

That distinction is not pedantry. A routing table presented as experience sends
somebody to spend real money on the wrong model, and the confident tone is what
does the damage.

**Two things go stale faster than anything else in this pack:** the version
numbers and the prices. Both moved several times in 2026 alone. Check the
model's own documentation before a batch, and when you find this file wrong,
correct it and record the change in `ads/LEDGER.md`.

### Availability is not access

A tool being *exposed* in your session proves neither the right account, nor
credits, nor access to a specific model behind that tool. Probe, then test on
one cheap shot before a batch depends on it. See `providers.md`.

---

## Routing

| The shot | Reach for | Why |
|---|---|---|
| Your **real product**, moving | image-to-video, from a real photograph | the only way the object stays your object. A described product is a different product |
| A **short cinematic beat** from text alone | Sora, or Veo | strongest text-to-video coherence per the comparisons |
| **High volume of short beats**, budget matters | Kling | reported around $0.029 per second on one host, several times cheaper than the alternatives |
| A shot that must **match a reference video's look** | Seedance | its multimodal reference system is the differentiator: images, video and audio as inputs |
| **Motion applied to a still** you already validated | Higgsfield motion tools | cheapest route from a static that works to a video that works |
| **A consistent presenter** across many shots | a character-consistency tool, or one real person | drift across shots is the hardest problem in generated video |
| The **still** that feeds image-to-video | Nano Banana, or an OpenAI image model | product fidelity and text handling live here, not in the video model |

**The single highest-value habit:** validate a static first, then animate it.
A still you have already judged, animated with one movement, beats a text-to-video
gamble on both cost and hit rate.

---

## What is reported about each

Version numbers move. The **shapes** below have been stable through several
releases; the numbers have not.

### Seedance
Reported maximum around **15 seconds**, and described as holding stability
across the full duration rather than degrading toward the end. Its distinguishing
feature is a multimodal reference system: text, image, audio and video as inputs
together, with a reported ceiling around a dozen reference assets, addressed by
tagging them from inside the prompt.

**Reach for it** when you have a reference you want matched: a look, a motion, a
video whose grammar you are deliberately echoing.

### Kling
Reported as accepting much longer clips than the others, up to minutes, **with
the caveat that matters more than the number**: coherence is reported to
degrade well before the maximum, with limbs drifting, backgrounds warping, and
faces losing consistency in longer generations.

Treat the maximum as a capability, not a recommendation. Generate short beats
regardless. Reported to be the cheapest per second of the majors, which makes it
the natural choice for volume.

### Veo
Reported maximum around **8 seconds**, no multimodal reference input, strong
resolution, and motion quality described as varying considerably with the prompt.

That last point is a workflow instruction, not a criticism: budget for more
attempts, and write the camera movement precisely rather than atmospherically.

### Sora
Reported around **12 seconds**, and repeatedly described as the strongest raw
cinematic quality from a text-only prompt.

Which is also the reason to be careful with it for direct response: cinematic
reads as "advertisement" in the first frame, and most paid social does not want
that. Ask for the register explicitly. See `video-prompting.md`.

### Wan
Appears in the pricing comparisons as a cost-effective option for longer clips.
Nothing more specific is established here.

### Higgsfield
An orchestration layer over several models plus its own motion, character and
upscaling tools, rather than a single model. Its value in this pipeline is
**motion applied to an existing still** and **character consistency across
shots**.

Runs on a credit balance. On zero, `providers.md` applies: stop, report
the balance and the run cost, and ask the user to switch account or top up.
Never substitute silently.

### Nano Banana, and image models generally
Not video models. They belong in this table because the image is where product
fidelity and any legible text are actually decided, and because an image-to-video
route is only as good as the still it starts from.

Generate the still, judge the still, **then** animate it.

---

## Duration is an endpoint parameter, not a preference

The **3 to 6 second beat** in `video-prompting.md` is an editing heuristic: the
length that cuts well and holds coherence. It is not an API enum.

Every endpoint accepts its own set of durations, and some accept nothing near
that range. So:

1. Read the schema of the endpoint you are actually calling.
2. Use a duration it accepts.
3. **If that duration differs from what the user authorised**, in length or in
   cost, say so **before** running, not after. A run that quietly became three
   times longer and three times more expensive is a broken gate, not a detail.

---

## What no model does well yet

Design around these rather than discovering them. Every one is a paid failure.

- **Hands doing something.** Keep them out of frame, or use image-to-video from
  a real photograph of real hands.
- **Legible text.** Generate without it and typeset afterwards. See
  `static.md`.
- **A logo.** Overlay the real file in post. Never in the prompt.
- **Several people interacting.** One person per shot, composite in the edit.
- **Complex physics.** Split into two simpler shots and cut between them.
- **Continuity across shots.** Repeat the invariant clause verbatim, use a
  reference where the model takes one, and write the edit so the drift lands on
  a cut.
- **A real person's likeness.** Not a quality problem. An impersonation problem,
  and no disclaimer fixes it.

---

## Cost discipline

`providers.md` owns the gate. Three things specific to video:

- **Video is the most expensive thing in this pack per attempt.** A batch of
  shots at two attempts each is a real invoice, and the user is entitled to see
  it coming.
- **Draft on the cheap model, finish on the expensive one.** Block the
  composition and the timing where a second costs a fraction, then regenerate
  only the surviving shots at the quality you will ship.
- **`gen.max_retries_per_asset` is two.** The third failure is the prompt, not
  luck. Change the prompt or change the shot.

And log, per shot: the model and version, the exact prompt, the reference, the
duration, the number of attempts, what changed between them, and the verdict.
Without that you cannot reproduce the shot that worked, which is the only shot
you will want again.

---

## Sources

Read September 2026. All `url` evidence.

- [Seedance vs Kling vs Sora vs Veo](https://www.atlascloud.ai/blog/guides/seedance-vs-kling-vs-sora-vs-veo) and
  [the API comparison](https://www.atlascloud.ai/blog/tips/seedance-2-vs-sora-2-vs-kling-3-comparison), Atlas Cloud
- [AI video model pricing comparison](https://www.eggstriker.com/en/blog/ai-video-model-pricing-comparison-2026), EggStriker
- [Seedance 2.5 vs Veo, Sora and Kling](https://lushbinary.com/blog/seedance-2-5-vs-veo-sora-kling-ai-video-comparison/), Lushbinary
- [Seedance 2.0 vs Kling 3.0](https://filmora.wondershare.com/video-editor-review/seedance-2-0-vs-kling-3-0.html), Filmora
- [AI video API pricing](https://devtk.ai/en/blog/ai-video-generation-pricing-2026/), DevTk

These are third-party comparisons, not vendor documentation. They disagree with
each other on specifics, which is itself informative. **The vendor's own current
documentation outranks every one of them, and outranks this file.**
