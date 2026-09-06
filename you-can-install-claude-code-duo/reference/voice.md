# Voice and audio

Most ads do not need a voice. This file is about deciding when they do, and
about not shipping a voice-over you cannot verify.

---

## The gate

`voice.worth_it_rule`: **a voice-over earns its cost only when it carries
information the picture cannot.**

A voice reading the on-screen text aloud wastes a channel. If the burned-in
captions already say it, the voice should be saying something else — the
reason, the aside, the objection, the tone that a caption cannot carry.

And `voice.sound_off_default`: the ad must already work muted before a voice is
commissioned. The voice is an upgrade for the minority with sound on, never the
load-bearing channel. Commissioning voice first, and then discovering the ad
fails the mute test, is the standard way this money gets wasted.

---

## Three roles a voice can play

| Role | What it does | Length |
|---|---|---|
| **Presenter** | a person addressing the viewer. Carries UGC and founder ads | the whole ad |
| **Narrator** | an unseen voice over demonstration footage | 10 to 30 s |
| **Aside** | one spoken line the captions deliberately do not repeat | 2 to 4 s |

The **aside** is the cheapest and the most underused. One line, said once, that
the text does not carry. It gives the sound-on viewer something the sound-off
viewer did not get, which is the entire argument for having audio at all.

---

## Tools

Ask before generating (`gen.ask_before_first_call`). Voice generation costs
money and, for cloning, carries consent obligations.

| Tool | Good for | Watch out for |
|---|---|---|
| **ElevenLabs** | synthetic narration, many languages, voice cloning, dubbing | cloning a real voice requires that person's documented consent. Cloning a public figure's voice for an ad is an impersonation problem, not a style choice |
| **Higgsfield** (audio / dubbing) | audio inside a video pipeline you are already running there | check the balance first; see `generation-tools.md` |
| **OpenAI TTS** | fast, cheap narration for drafts and timing tests | voice range is narrower than a dedicated tool's |
| **SuperWhisper / Whisper** | **transcription**, not synthesis | dictate the script, do not synthesise with it. Useful for capturing a real person's phrasing before you write |
| **A real person** | anything that must not sound synthetic | a day of turnaround, and the best option more often than the tool list suggests |

**On SuperWhisper specifically:** it is a dictation tool. Its place in this
pipeline is *input* — dictate the founder's actual phrasing, transcribe a
customer call, capture the sentence a buyer used. Copy written from a
transcript of a real person beats copy written to sound like one.

---

## Direction: what to specify

Voice models take direction badly when the direction is adjectives. Specify
mechanics instead.

- **Pace** in words per minute, or by naming a reference: "conversational, about
  as fast as someone explaining something to a friend".
- **Where the pauses are.** Mark them in the script. A pause before the turn is
  the single most effective piece of voice direction available.
- **Which words carry the stress.** Underline them in the script you feed the
  tool.
- **The relationship**: talking to one person, not to a room. Ads read to a room
  sound like ads.
- **What it is not**: not announcer, not upbeat-corporate, not "excited". Naming
  the failure mode works better than naming the target.

Generate two or three takes and pick. Do not regenerate more than
`gen.max_retries_per_asset` times chasing a delivery — at that point change the
words, because the script is what is wrong.

---

## Languages you do not read

`voice.native_speaker_rule`. Generated speech in a language you do not read can
be fluent, confident, and wrong: a mispronounced product name, a register that
is too formal for the market, an idiom that reads as machine translation.

You have two honest options, and one thing that is not one:

1. **A competent language check** before it ships, by a person who speaks it.
   Cheapest insurance in the pipeline, and the only one that actually verifies
   the recording.
2. **No voice.** Music, captions, and a demonstration carry a very large share
   of ads in every market.

**Captions are not the third option.** Burning in the intended text mitigates
the damage — a viewer can read what was meant — but it verifies nothing about
what the audio actually says, and a wrong or offensive delivery still ships with
your brand on it. Captions are worth adding either way. They do not clear an
unverified voice-over, and treating them as clearance is how one gets shipped.

What is not an option: shipping an unverified voice-over into a market you
cannot read, and calling the risk a rounding error. It is your brand saying
something you have not heard.

**Pronunciation of the brand name** is the specific thing that goes wrong most
often. Check it first, every time, in every language.

---

## Music and sound design

- **Sound effects beat music** for a demonstration. The strap clicking, the
  fabric moving, the lid closing. It is proof, delivered through a channel the
  picture cannot use.
- **Music decides pace**, so pick it before the edit, not after.
- **Licensing applies to audio too.** A trending track is licensed for organic
  posting, not for a paid ad. Using it in paid media is an infringement that the
  platform's own music library exists to prevent. Record the licence in
  `SOURCES.txt` next to the images.
- **Loudness**: mixes that are hot relative to the feed read as intrusive and
  get muted, which loses you the channel you paid for.

---

## Output

Store audio next to the video, never only inside the edit:

```
video/v3/
  script.md          the shot table, with pauses and stress marked
  vo/
    en-take1.wav  en-take2.wav  fr-take1.wav
    SOURCES.txt    tool, voice id, date, and consent record for any cloned voice
  music/
    SOURCES.txt    track, licence, and the licence's scope
```

The consent record for a cloned voice is not optional bookkeeping. If it is not
written down, it does not exist when someone asks.
