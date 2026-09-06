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
  deliberately. See `video-music.md`.

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

`ratios.required_set` is 4:5 and 9:16. Add the others when the placement
genuinely wants them.

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
| File size | under about 4 MB per 15 seconds | heavier files get re-encoded harder and text goes soft |

**Text softness is the symptom to watch.** If your burned-in captions look
slightly fuzzy after upload, the file was too heavy or the text too thin, not
the platform being unfair.

---

## Verification, before anything leaves the folder

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
