# The reference motion engine

A pack that can design a video and judge a video, and cannot make one, sends the
assistant looking for a renderer. It finds whatever is nearest. That is how an ad
becomes a slideshow of stills with a fade between them, and how a JavaScript
toolchain becomes a requirement nobody agreed to install.

So this pack ships an engine that runs. It is built on the two things the pack
already requires: a Python interpreter and FFmpeg. No package to install, no Node,
no browser, no account.

**JavaScript is never mandatory.** Remotion, After Effects, Blender, a connected
video model and a human editor all stay first-class routes through the adapter
contract in [providers](providers.md). This engine is the floor, not the ceiling. It
exists so that "nothing was rendered" is never caused by the pack itself.

---

## One command

```bash
python scripts/render_motion.py motion-project.json --root . --apply
```

That reads the manifest, renders every declared format as its own composition,
decodes each file it wrote, corrects what it can, writes contact sheets and control
frames, and updates the manifest from the files that now exist.

| Flag | What it does |
|---|---|
| `--root DIR` | The project directory. Every asset and export path is resolved inside it, and a path that escapes it is refused |
| `--apply` | Actually render. Without it nothing is written and the manifest is untouched |
| `--resume` | Reuse the scene clips already on disk, after checking each one is complete |
| `--formats 9:16,4:5` | Render a subset. The other formats keep their existing export records |
| `--max-passes N` | Cap the correction loop. Three by default, and three is the contract |
| `--contact-sheet` | Also write a contact sheet and control frames per format |
| `--json` | Machine-readable report on stdout |

| Exit | Meaning |
|---|---|
| `0` | Rendered and every check passed |
| `1` | Rendered and findings are still open. They are in the report and in the manifest |
| `2` | The manifest is invalid, or the arguments are. Nothing rendered |
| `3` | This machine cannot render, and the reason names the missing part |
| `4` | The render failed partway. The reason is stated and nothing is claimed as delivered |

**`--root` is the only thing that decides where files are.** Every path in the manifest is resolved against it before ffmpeg is called, and refused if it climbs out of the project. That is true of the pictures and of `voice.file`, `music.file` and `sfx[].file`, which is worth saying because it was not always true of the last three: they used to reach ffmpeg as written and get resolved against the working directory of the process instead, so running from anywhere but the project root died on the audio with `--root` set correctly and every file present. Run it from wherever you like.

**Without `--apply` it renders nothing and changes nothing.** A preview that quietly
renders is how a paid provider gets called by accident.

### Try it before you need it

A complete sixteen second ad ships as `examples/motion-project.render.json`. Its
assets are synthetic and are generated locally, so the example runs on a bare machine
with nothing but FFmpeg:

```bash
python scripts/make_fixture_assets.py --out fixtures
python scripts/render_motion.py examples/motion-project.render.json --root . --apply --contact-sheet
```

That writes `exports/9x16`, `exports/4x5` and `exports/16x9`, each with an MP4, a
contact sheet and six control frames. The voice file it generates is a tone named
`voice-standin`, not speech, and the manifest records it as a fixture. A pack that
let a tone be called narration would be doing the exact thing it tells the assistant
never to do.

---

## What it needs, and how it finds out

The engine asks the machine rather than assuming. `motion_engine.detect()` returns
what is present and, when something is missing, one sentence naming which part:

- `ffmpeg` and `ffprobe` on PATH
- every filter the pipeline actually issues, checked by name against `ffmpeg -filters`
- the `libx264` and `aac` encoders
- an FFmpeg built with `libfreetype`, because without it no text is drawn at all
- at least one usable font file, preferring the brand family and degrading through a
  known list rather than to whatever sorts first

A run on a machine that cannot render stops with exit 3 and says why. It does not
render a version with no text and call it done.

**This is not hypothetical, and macOS is where it bites.** `brew install ffmpeg`
installed a build carrying libx264 and aac and no libfreetype or libass, so every
encode succeeded and `drawtext` and `subtitles` did not exist. An engine that trusted
"ffmpeg is installed" would have delivered a finished-looking ad with none of the
words in it, at the right duration and the right loudness, and every technical check
would have passed. If you are on a Mac and the run stops with that reason, install an
ffmpeg built with libfreetype and libass rather than working around the message.

---

## Three compositions, not one crop

Each format is composed from its own frame. There is no master to crop, which is the
only structural way to make cropping impossible.

| Ratio | Arrangement |
|---|---|
| Portrait, up to 0.7 | Picture across the top two fifths, copy column beneath it, captions in their own band above the platform interface |
| Square-ish, under 1.2 | Picture across the top, a shorter copy column, tighter type scale |
| Landscape | Two columns. Type on the left, picture filling the right. The copy is centred in its column, because a left column top-aligned against a full-height picture reads as unfinished |

The type scale, the margins, the safe areas and the caption band are all fractions of
the frame, so they are computed per format instead of being copied between formats
and drifting.

**Each format keeps its own reserve for the platform's interface**, read from that
format's `safe_zones` in the manifest and falling back to the project grid only when a
format declares none. This matters more than it sounds: a vertical loses about a fifth
of its height to the interface and a feed square loses almost nothing, so one pair of
numbers applied to three ratios is a crop decision wearing a grid's clothes. It also
costs real frame: applied to the landscape, a vertical's reserve throws away a tenth of
a picture nothing was ever going to cover.

### The fit pass

Before anything is drawn, every scene's stack of blocks is **measured**: wrapped line
count, block height, the gap above each block. If the tallest scene does not fit its
column, the type scale shrinks until it does, once for the whole film so a role keeps
one size across scenes. If it still does not fit at the smallest scale the layout
allows, the run stops and says which format and by how much.

Measuring first is the point. Placing block by block and clamping each one to the
bottom of the column looks like a safety net and is the opposite: two blocks that
both hit the clamp get the same position, so the guard against overlap is what
produces the overlap.

---

## What a scene can contain

```json
{
  "id": "s3",
  "start": 6.6,
  "end": 9.8,
  "transition": "dissolve",
  "transition_seconds": 0.3,
  "background": {"kind": "gradient", "from": "ink", "to": "support"},
  "camera": {"move": "push", "amount": 0.08},
  "layers": [
    {"kind": "image", "asset": "still-1", "fit": "cover", "parallax": 0.02},
    {"kind": "text", "role": "display", "content": "391 / 412", "at": 0.1},
    {"kind": "shape", "h": 0.008, "colour": "accent", "grow": true, "at": 0.45},
    {"kind": "text", "role": "body", "content": "reglees en une seule visite", "at": 0.8}
  ]
}
```

| Layer | Fields |
|---|---|
| `image` | `asset`, `fit`, `parallax`, and the scene camera applies to it |
| `video` | `asset`, `fit`, `parallax`, trimmed to the scene |
| `text` | `role` (`display`, `title`, `body`), `content`, `at`, `enter` (`rise`, `slide`, `fade`), `enter_seconds`, `ease`, `colour`, `gap`, and `size_px` or `x`/`y` for a deliberate one-off |
| `shape` | `w`, `h`, `colour`, `opacity`, `grow`, `at` |

Positions, sizes and opacities are **fractions of the frame between 0 and 1**, never
pixels. `check_motion_project.py` refuses a value outside that range, because `0.075`
and `75` look alike in a manifest and not on screen.

Layers with no explicit `y` stack in the copy column in declaration order, so a rule
declared between two lines of type lands between them in all three formats.

Text is written to a file and drawn with `textfile=` and `expansion=none`. That
removes an entire class of bug: an apostrophe, a comma, a percent sign or a colon in
French ad copy otherwise needs three levels of escaping, and gets one of them wrong.

---

## Motion primitives

Reusable, and all of them are expressions evaluated per frame rather than pre-rendered
sequences.

| Primitive | What it gives |
|---|---|
| `progress(start, seconds)` | Clamped 0 to 1 progress from a timecode |
| `eased(...)` | `linear`, `ease_out`, `ease_in`, `ease_in_out`, clamped at both ends |
| `interpolate(a, b, ...)` | Any value moving from a to b on that curve |
| `camera_zoom(kind, amount, frames)` | A bounded push or pull, so a long scene cannot zoom past its own frame |
| Parallax | Planes offset by different amounts against the camera, which is what reads as depth |
| Animated type scale | A transparent text plane scaled and composited, because an animated `fontsize` expression crashes some FFmpeg builds outright |
| Transitions | `dissolve`, `fade`, `wipe`, `slide`, `smooth`, `circle`, or a straight `cut` |

**Each scene clip is rendered with a tail exactly as long as the transition that
follows it**, so the crossfade consumes the tail rather than the film. Without that,
every transition silently shortens the ad and the duration check then fails on a
timeline nobody got wrong.

Clips are cut to an exact frame count, not a duration, and padded on the last frame
if an input ends a fraction of a frame early. `-t` cuts at the last frame strictly
before the mark, which loses a frame per scene and drifts the whole timeline.

---

## The design system

One `design` block per project, and every colour, size and motion default in the
engine reads from it. Nothing is hard-coded to a look.

```json
"design": {
  "palette": {"ink": "0x101820", "paper": "0xF5F0E8", "accent": "0xF5A623",
              "muted": "0x8A97A3", "support": "0x2A4A6A"},
  "type": {"family_preference": ["Inter", "Poppins"],
           "scale": {"display": 0.075, "title": 0.050, "body": 0.030, "caption": 0.034}},
  "motion": {"enter_seconds": 0.45, "ease": "ease_out", "camera_amount": 0.10},
  "grid": {"margin": 0.075, "safe_top": 0.10, "safe_bottom": 0.16}
}
```

Layers name a palette token, not a hex value, so a brand change is one block. A token
that does not exist falls back to a stated default rather than rendering an invisible
line.

---

## Sound

One audio graph per film, built from the manifest and not from taste.

1. Voice, delayed to its cue, and the film's spine.
2. Music, **ducked under the voice with a real sidechain compressor**, not a static
   volume drop. The gaps between lines are where the bed comes back up, which is what
   ducking is for.
3. Effects, each at its own timecode.
4. Two-pass `loudnorm` to the declared integrated loudness and true peak.

The measured result comes back out of `inspect_video.py`, which decodes the finished
file. The engine never reports the level it aimed for.

Captions are burned from the cues in the manifest, styled from the design tokens,
and placed in the caption band that the copy column is forbidden to enter, inside that
format's own left and right margins. Both are
legible alone and unreadable on top of each other, which is a defect a contact sheet
shows in one glance and a duration check never will.

---

## Render, inspect, correct

Three passes, and three is the cap.

1. Render the format.
2. Decode the export with `inspect_video.py` against the thresholds the **manifest**
   declares. The measurer invents no threshold.
3. If a finding has a mechanical correction, apply it to the render plan and go
   again. If it does not, stop and report it.

Findings that survive three passes are written into `qa.technical` as open defects
with a timecode and a fix. An unbounded loop is not persistence, it is a hang.

---

## Contact sheets and control frames

`--contact-sheet` writes a twelve-cell grid per format plus six full-size frames.
This is not decoration. Every layout defect found while building this engine, and
there were several, was found by looking at a contact sheet. None of them was found
by a measurement, because each frame was individually valid.

Look at the sheet before delivering. The technical grid says the file is sound. Only
someone looking at it says the ad is worth money.

---

## The same manifest gives the same bytes

Two renders of an unchanged project produce identical files, and the hash written
into the manifest is therefore a fact about the project rather than about one
afternoon. Two things had to be fixed for that to be true, and neither was visible in
any output:

- **`gradients` defaults to `seed=-1`**, a new random gradient on every run. Seeds are
  now derived from the scene id, so scenes still differ from each other while each one
  repeats, and a manifest can pin its own.
- **`sidechaincompress` reads two streams whose framing varies between runs.** The
  compressor's state follows the frames it is handed, so the ducking diverged and the
  audio encoded differently every time. Both sides are now cut to identical frames
  first.

The video encoder was never the problem. Every scene clip, the assembly and the burned
captions were already byte-identical; it was the ducking underneath them.

## Resume

`--resume` reuses the scene clips already on disk. Two rules make that safe:

- The plan fingerprint is written **before the first scene renders**, not after the
  last. An interrupted run never reaches the end, so a resume keyed on a finished-run
  state file discards exactly the work the interruption left behind.
- A clip is reused only if its frames are counted and match. A file that exists is
  not a file that is finished: FFmpeg writes the index last, so a killed encode
  leaves a plausible mp4 that decodes short, and reusing it puts a missing second in
  the middle of the ad without raising anything.

---

## The manifest is updated from the files

After a run, `exports` carries the real path, the real SHA-256, and the measurements
that came out of the decoder. `state` becomes `measured`. `engine` records the engine
that ran and that JavaScript was not required.

A run limited with `--formats` updates those ratios and leaves the others alone, as
long as their files are still there. Re-rendering a vertical is not a statement that
the landscape was never exported.

Validate afterwards with `--root`, which opens each export and recomputes its hash:

```bash
python scripts/check_motion_project.py motion-project.json --root .
```

---

## Using a different engine

This one is the reference, not a requirement. Any renderer that can do the following
is a legitimate route, and the manifest records which one ran:

- compose each ratio from its own frame
- animate type, layers and camera on a timeline
- burn captions from the final take
- mix voice, music and effects to a declared loudness
- export a file that `inspect_video.py` can decode and measure

Record the choice in `engine` with `detected: true` and one sentence on why.
[Providers](providers.md) has the capability table and what to say when a capability
is genuinely absent.

---

## What it does not do

Honest limits, stated once here rather than discovered late.

- **It does not generate footage.** It composes what you give it and what FFmpeg can
  synthesise: gradients, solids, shapes, type. Generated footage comes from a video
  model, through the adapters.
- **It does not speak.** A voice comes from a speech tool or a person. The shipped
  fixture uses a synthetic tone named `voice-standin` precisely so nothing can mistake
  it for narration.
- **Line breaking is measured, not estimated**, and this is the one place the engine
  reads a file format itself: advance widths and the character map come out of the
  `head`, `hhea`, `hmtx` and `cmap` tables of the actual face. Kerning is not applied,
  deliberately, because `drawtext` does not apply it either. A face this cannot parse
  falls back to an average-width estimate rather than failing, and that estimate is
  poor: on ten capital I it reads 96% too wide, on ten m it reads 41% too narrow.
- **No 3D, no particle systems, no shader effects.** Those need a different engine,
  and the adapter contract is how you reach one.
- **Rendering costs minutes, not seconds**, and it scales with format count and
  duration. `--resume` exists for that reason.
- **What it does not decide is whether the ad is any good.** The validator now
  measures contrast, caption reading rate and whether the first second carries
  anything readable, because those are arithmetic. Everything past that is
  [creative QA](creative-qa.md), run by a person looking at the contact sheet.
