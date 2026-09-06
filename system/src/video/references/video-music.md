# Music and sound design

Sound is the channel most ads waste. It is muted for most viewers, so it cannot
carry the message, and it is then treated as decoration, so it carries nothing
at all.

It has exactly two jobs worth paying for: **it sets the pace of the edit**, and
**it gives the sound-on viewer something the sound-off viewer did not get.**

Read `video-voice.md` for the spoken channel. This file is everything else.

---

## Decide before the edit, not after

Music chosen after the cut is decoration laid over finished work. Music chosen
before the cut decides where the cuts go, and that is most of what it is for.

Pick the tempo first, in words: "cuts land about every second and a half, so
around 100 to 120 beats per minute". Then edit to it. An ad edited to a beat and
one edited to taste look different at a glance, and the difference is not
subtle.

---

## What sounds professional, and what does not

The distinction is not budget. It is whether the sound was **chosen for this
video** or **applied to it**.

### Reads as professional

- **The music has a shape that matches the video's shape.** It builds where the
  video builds and it lands where the offer lands.
- **It starts at the right place in the track.** Not at 0:00 of the file: at the
  bar that works for frame one. Most stock tracks have eight boring seconds
  before the part you actually want.
- **It ends.** A hard stop, a resolved bar, a fade that finishes before the last
  frame. A track cut mid-phrase at the end of the video is the single most
  common amateur tell in paid social.
- **It sits under.** Around 12 to 18 dB below the voice, and lower still under
  the first line, which is the one that has to be understood.
- **Sound effects are diegetic.** The strap clicking, the lid closing, the
  fabric moving. These come from the video, not from a library of whooshes.

### Reads as amateur

- **A whoosh on every cut.** The fastest way to make a good edit look like a
  template. One transition sound in a video is a choice; six is a preset.
- **Music louder than the voice**, or the same. If a viewer has to work to hear
  the words, they leave rather than adjust the volume.
- **A track that never resolves**, just stops when the video does.
- **Genre mismatch.** Corporate-uplifting under a documentary-register service
  ad. Trap under a law firm. The mismatch reads before the content does.
- **The same track as everyone else.** The most-used tracks in a stock library
  are recognisable to anyone who watches ads, and recognition here means "this
  is an ad made with the default".
- **Stock stingers and risers** from a preset pack, used because they were in
  the pack.

### The test

Play the video with the music and no voice. Does the music alone tell you where
the important moments are? If yes, it is doing its job. If it is a flat bed of
pleasant sound from start to finish, it is costing you a channel and adding
nothing.

---

## Sound design beats music, for a demonstration

Underrated and nearly free.

A product ad whose proof is a demonstration should let the demonstration make
its own noise. The click, the pour, the tear of the packaging, the closing seal.
That is **evidence delivered through a channel the picture cannot use**, and it
is far more convincing than any track.

Record it, or take it from a real recording. Generated foley usually sounds
approximately right, which in audio means wrong.

Where the product is silent, silence with one small real sound at the moment of
proof beats music under everything.

---

## The aside

The cheapest thing in this file, and almost nobody does it.

Burn the captions in, as always. Then have the voice say **one line the captions
do not carry**: the reason, the caveat, the joke, the thing you would say
quietly.

The sound-off viewer loses nothing. The sound-on viewer gets something they
were not expecting, which is the only actual argument for having audio in a feed
ad at all.

Four seconds. It is a gift to the minority who unmuted.

---

## Licensing, which is where this becomes expensive

The rule that catches people: **a trending track is licensed for organic
posting, not for a paid advertisement.** The platform's music library exists
precisely because the two are different, and using a popular track in a paid ad
is an infringement whatever the platform let you upload.

What is safe:

| Source | Safe for paid | Watch out for |
|---|---|---|
| The platform's own commercial music library | yes, on that platform | not portable to another platform's ads |
| A commercial stock licence you hold | yes, within its terms | check territory, duration, and whether "paid social" is named |
| Music you commissioned | yes, if the contract says so | a work-for-hire clause, not a handshake |
| Generated music | check the generator's terms | some grant commercial use, some do not, and it changes |
| A trending track from the platform's organic library | **no** | this is the one everybody gets wrong |
| Anything else | **no** | including "it's only 8 seconds" and "it's transformative" |

Record the licence next to the file, in the same `SOURCES.txt` as the images:

```
music/
  track-01.mp3
  SOURCES.txt   track, source, licence, its territory and term, date acquired
```

In eighteen months, when a platform sends a notice, that file is the only thing
that will remember.

---

## Loudness

- **Mix for a phone speaker**, not for headphones. Check it on one.
- **Do not mix hot.** A video noticeably louder than the feed reads as intrusive,
  gets muted, and you have lost the channel you paid for.
- **Duck the music under every spoken line**, not just the first. Automatic
  ducking is fine; no ducking is not.
- **Never start on a loud transient.** A viewer with sound on who is startled at
  frame one scrolls at frame two.

---

## Generated music

Useful for a draft, and increasingly usable for a final.

- **Ask for structure, not mood.** "Eight bars of tension, then a resolve at
  0:12" gets you something editable. "Upbeat and inspiring" gets you a bed.
- **Ask for stems** where the tool offers them. Being able to drop the drums
  under the voice line is worth more than a better track.
- **Check the terms for commercial use**, per the table above, and record what
  you found.
- The `gen.ask_before_first_call` gate applies: it costs money, so the user
  chooses the tool and confirms the run.

---

## Deliverables

```
video/v3/
  edit.mp4
  music/
    track.mp3        with the in-point noted: which bar frame one lands on
    SOURCES.txt      licence, territory, term
  sfx/
    SOURCES.txt      recorded, or licensed, per file
  mix-notes.md       music level under voice, where it ducks, where it ends
```

`mix-notes.md` is three lines and it saves the next person from re-deriving your
mix by ear.
