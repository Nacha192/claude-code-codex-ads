# Assembly

Turning a pile of shots into a video that ships. The stage where good material
is most often lost, because it feels like the easy part.

---

## Order of operations

Do these in this order. Every inversion costs a re-export.

1. **Lock the shot list** against the storyboard. Missing shots are named as
   missing, not filled with something close.
2. **Cut the picture, silent.** If it does not hold silent, no sound will save
   it. See the mute test in `video-retention.md`.
3. **Add captions.** They are part of the picture, not a garnish, and they change
   the pacing because the eye needs time to read.
4. **Add sound**: diegetic effects, then voice, then music under. See
   `video-music.md` and `video-voice.md`.
5. **Check the safe areas** at every ratio you will export.
6. **Choose the first frame.**
7. **Export per ratio from the edit.** Never by cropping an export.

The supplied engine does steps 2 to 7 in one command, composing each ratio from its
own frame so there is no master to crop from. See
[the reference motion engine](motion-engine.md). Any other renderer that meets the
same contract is equally valid; what is not valid is skipping the step and calling a
storyboard a video.

---

## Captions

Not optional. Most impressions are muted.

- **Burn them in.** Platform auto-captions are inconsistent, styled by the
  platform, positioned where you did not choose, and absent in some placements.
- **Two to four words per card**, one line, occasionally two. A full sentence
  on screen is read instead of watched.
- **They appear on the word**, not a beat late. Late captions feel wrong before
  a viewer can say why.
- **Keep them out of the platform's furniture.** On 9:16, the bottom fifth
  belongs to the interface. Captions there sit under a profile picture and a
  caption expander.
- **High contrast, no thin weights.** A stroke or a solid plate behind the text,
  not a drop shadow, which disappears on a busy frame.
- **Never let a caption transcribe the voice exactly** when the voice is
  carrying an aside. That is the one case where the two channels should differ,
  deliberately, and it is the single exception to the rule in `video-voice.md`
  that captions match the final take. Record it as a choice. See
  `video-music.md`.

---

## Safe areas, per ratio

From `thresholds.md`: `ratios.safe_margin` is 12 % of the short edge, on every
edge, and on 9:16 the **top 14 % and bottom 20 %** are additionally reserved.

| Ratio | Pixels | Where the platform paints over you |
|---|---|---|
| 4:5 | 1080 × 1350 | very little. The safest frame for feed |
| 9:16 | 1080 × 1920 | top: account and sound. Bottom: caption, buttons, expander |
| 1:1 | 1080 × 1080 | little |
| 1.91:1 | 1200 × 628 | little, but the frame is short: one line of text, no more |

Check this by exporting one frame and looking at it on a phone, in the app, if
you can. Fifteen seconds, and it catches the call to action sitting under a
button every time.

---

## Every ratio comes out of the edit

`ratios.crop_rule`. Missing a ratio does not remove you from that placement: the
platform transforms what you gave it, cropping, letterboxing, or padding with a
generated background, and delivers you in a frame you did not choose with your
text sometimes outside it.

So: **reframe each ratio in the timeline**, moving the subject, not the crop
tool on an export. A 9:16 built by centre-cropping a 16:9 loses the composition
in every shot, and it is visible.

**Each ratio carries its own composition**, and the manifest refuses one that does
not. Seven things are decided per ratio, not inherited:

| Per ratio | Because |
|---|---|
| Composition | What sits where. A vertical is not a horizontal with the sides removed |
| Typographic scale | A headline sized for 16:9 is unreadable at 9:16 and vice versa |
| Subject placement | The optical centre moves with the frame |
| Safe zones | Each surface puts its own interface in a different place |
| Caption placement | Under the subject in one ratio, beside it in another |
| CTA placement | It must survive the platform's own CTA overlay |
| Its own visual check | An approved 9:16 is not approval of an unseen 4:5 |

**The mandatory ratios are the ones in the brief.** `ratios.required_set` in
`thresholds.md` is a common starting pair, not a law: a brand buying only Reels
needs one, a brand running YouTube needs 16:9 that the pair does not include.
Compose what was asked for, and say which ones you could not.

---

## The first frame

The whole of your first impression on a scroll, and it is usually left to the
encoder.

- Choose it deliberately. It is a decision, like the hook.
- It should contain the scroll-stop element, not the setup that precedes it.
- Test it at 120 pixels wide. If nothing reads there, nothing reads in the feed.
- A frame of motion blur, a mid-blink face, or an empty establishing shot is a
  wasted impression.

---

## Encoding

Working targets, not laws. Platforms re-encode everything; the goal is to give
them something that survives it.

| | Target | Why |
|---|---|---|
| Codec | H.264, high profile | universally accepted, re-encodes predictably |
| Container | MP4 | same |
| Frame rate | match the source, usually 30 | mixed rates produce judder on cuts |
| Bit rate | 8 to 12 Mbps at 1080 | above this the platform's re-encode discards it anyway |
| Audio | AAC, 128 kbps, stereo | |
| File size | whatever the bit rate produces, roughly 15 to 25 MB per 15 seconds at 1080 | not a separate target. It is arithmetic: 10 Mbps for 15 seconds is about 19 MB. Chasing a smaller file means lowering the bit rate, which is the thing that softens text |

**Text softness is the symptom to watch.** If your burned-in captions look
slightly fuzzy after upload, the bit rate was too low or the strokes too thin,
not the platform being unfair. Raising the bit rate makes the file larger, and
that is the correct trade.

---

## Verification, before anything leaves the folder

Everything in this section that can be measured rather than judged has its exact
command in `measurable-checks.md`: duration against the intended cut, resolution
and ratio, frame rate, bit rate, audio tracks, loudness, true peak, clipping,
head and tail silence, and subtitle timing against the montage. Run those before
you start watching, so you spend the viewing on the things a command cannot see.

`gen.verify_on_disk` applies to video as it does to images. A successful export
dialog is not a file.

```bash
ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=width,height,codec_name,r_frame_rate \
  -of json out/9x16/ad-03.mp4
```

Check four things against what you intended: **duration, width, height, and
frame rate.** A 9:16 export that came out 1080 × 1080 because the sequence
setting did not change is silent, common, and ships.

Then watch it. All of it. On a phone if you can. Nobody wants to and everybody
should: the artefacts that matter are the ones a codec introduced after your
last preview.

---

## Naming and versioning

```
video/v3/
  script.md               the shot table
  shots/                  generated or filmed source, one file per shot
  edit.mp4                the master, at the base ratio
  out/
    9x16/ad-03-the-strap-holds.mp4
    4x5/ad-03-the-strap-holds.mp4
  music/  vo/  sfx/       each with SOURCES.txt
  README.md               what changed from v2, and why
```

Name the angle, never a number. `ad-03-the-strap-holds.mp4` beats
`final_v2_FINAL.mp4` by more than it looks, and in six weeks the account will
ask which creative was live in March.

**Never overwrite a previous version.** A batch that cannot be compared to the
one before it produces files, not learning.

---

## The pre-flight, for video

`compliance.md` owns the batch checklist. Four items are video-specific and are
run in addition:

1. **The mute test, on the final cut**, not on the storyboard. Things change in
   the edit.
2. **Every claim spoken aloud is still a claim.** A number said in a voice-over
   needs its source exactly as a written one does, and it is easier to miss
   because nobody reads audio.
3. **Music and voice licences recorded**, including the consent record for any
   cloned voice.
4. **Duration, dimensions, and frame rate read back with `ffprobe`** for every
   exported ratio.
