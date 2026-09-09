# Voice

The spoken channel, from choosing a voice to cloning one. Music, effects and the
mix are in `video-music.md`; how the take lands in the timeline is in
`video-assembly.md`. This file decides who speaks, whether they may, and what is
kept afterwards.

**Before anything here, find out whether you can speak at all.** A speech
capability is a property of the machine, not of the assistant. Check the
connected tools; if none generates audio, say so in one sentence and deliver the
script, the direction and the voice card instead. A written script described as
narration is the single most common lie in this craft.

---

## Does this ad need a voice

Ask before spending on one. `voice.worth_it_rule` in `thresholds.md`: a
voice-over earns its cost only when it carries something the picture cannot. A
voice reading the on-screen text aloud spends a channel to duplicate another
one, and the viewer with sound off loses nothing, which tells you the voice was
never doing work.

Three cases where it clearly earns its place: a mechanism that needs explaining
while something is shown, a service where the person talking *is* the product,
and a claim that needs a human to take responsibility for saying it.

---

## The voice catalogue

Build it from the provider actually connected, and keep it in the project. This
is the part people get wrong: a catalogue assembled from demo videos found
online describes voices you may not have, under names your provider may not use.

**The voices in a connected catalogue belong to that provider.** They are not
ElevenLabs voices because someone called them that. Record which provider they
came from, because the name is not portable.

Per voice, one row, and listen before you write it:

| Field | Why it is there |
|---|---|
| Voice id and provider | the only thing that reliably reselects it |
| Language and regional accent | an accent that does not match the market reads as an import, which can be right or fatal |
| Register | the two or three things it does well, said in plain words |
| What it cannot do | the useful half. A warm voice that cannot do urgency is a fact worth writing down |
| Commercial rights | whether it may run in a paid ad at all, checked at the provider, not assumed |
| Audition date | catalogues change under you |

Preview without generating where the provider allows it. Most expose a sample
per voice, and listening to twenty samples costs nothing while guessing costs a
reshoot.

---

## Directing a take

A voice card, written before the first generation:

Target language and regional accent. Perceived age and timbre, described without
naming a real person. Conversational energy, warmth, authority. Pace, where the
pauses go, which words carry the emphasis. A pronunciation lexicon for the brand
name, the product name and anything the model will otherwise mangle. The
mannerisms you do not want.

Tie all of it to the buyer and the offer. A trade-service explanation and an
intimate product story need opposite deliveries, and "more human" means
appropriate phrasing and performance, never random breaths or an imitation of
somebody real.

After approval, generate two or three readings of the same difficult passage
inside the batch ceiling and compare intelligibility, accent, pronunciation,
intent and fatigue. Choose by listening. Model prestige and price predict
nothing here.

Use only the controls the chosen model supports. Emotion tags, stability,
similarity and speed differ across providers, and an unsupported instruction is
sometimes read aloud in the take. Record the voice, the model and the exact
settings that produced the accepted file, or the next session cannot reproduce
it.

---

## Cloning the user's own voice

The pack clones the voice of the person asking, for their own material. The
protocol below is the whole of it.

### Ask for a sample that can act

When they ask for their voice, ask for a recording. Then ask for the right kind
of recording, and say why: the sample decides the ceiling. A clone made from one
flat paragraph reads everything in that one register forever, and no amount of
prompting recovers the range that was never in the sample.

Ask them to run through the range on purpose, in one take:

1. Normal speaking, two or three sentences, as if explaining something to a
   colleague.
2. The hook, with real energy.
3. A calm explanatory passage.
4. A question, asked as a question.
5. An objection answered, so the model hears the shift into reassurance.
6. The call to action.
7. Two sentences read flat and slowly.

**Ask for this even when they have already sent something.** A clip they had
lying around is one register, and the clone inherits exactly that register. Say
what the fuller recording buys them rather than making it a formality.

**If they decline, or do not have it, take what they gave.** A narrower clone is
still useful, and refusing to proceed over a nice-to-have is obstruction. Record
that the sample was narrow, so the next person knows why the delivery is flat
before they blame the direction.

### Record the consent, so it can be checked and withdrawn

Consent that exists only in a chat log is not consent anyone can verify later.
Write it into the project, next to the voice:

| Field | Value |
|---|---|
| Whose voice | the person, by the name the project already uses |
| Who asked | the same person, or this fails |
| The sample | which file produced the clone, and its date |
| Purpose | what it may be used for, in one sentence |
| Retention | how long it is kept, and what triggers deletion |
| Withdrawal | how they revoke it, and who acts on that |
| Territory | any regional restriction the provider states |

Withdrawal has to mean something. When they revoke it, delete the clone at the
provider, delete the stored sample, and record that both happened. A consent
record with no working delete is decoration.

### Keep it, so it is there in six months

Store the provider voice id, which sample produced it, the date, the observed
limits and the consent record. That is what makes the voice reusable months
later, when the conversation that created it is long gone.

Never the audio file in a public place, never the provider credentials, never
the voice id in a repository that will be published. Treat the voice id like an
account identifier, because that is what it is: whoever holds it can speak as
that person on that provider.

Reuse it only for that person's own work, and confirm before using it on
something new. Agreeing to create a clone is not agreeing to be the voice of
everything the project makes for the next year.

### The line

The voice of the person asking, for their own material. Not a third party's, not
a public figure's, not a voice lifted from a video, whatever reason is offered
and however easy it would be. A person's voice taken from a recording is that
person cloned without their consent, and the fact that the recording was public
changes nothing about that.

If the request is for someone else's voice, say no in one sentence, offer the
catalogue and a directed take that gets the same feeling honestly, and move on.

Check the provider's current rules and disclosure obligations before production.
Synthetic-voice disclosure requirements change, and they change by market.

---

## Voice in: dictated and transcribed briefs

A spoken brief is often better than a typed one, because people explain their
own business more precisely out loud than in a form. Superwhisper and equivalent
tools do this.

**Transcription is not narration.** A dictation route turns speech into text; it
does not generate a voice. The two get confused constantly and they are
different products. Never present a transcript as a produced take.

When you transcribe: record the language, keep the timestamps if the tool gives
them, keep who is speaking when there are several, and keep the raw transcript
next to the cleaned one. The raw version holds the customer's own vocabulary,
which is worth more for copy than the tidy version. A transcript of a customer
call is that customer's words: it is private project material, it never goes in
a public artifact, and a quote pulled from it still needs their agreement before
it runs in an ad.

If transcription fails or the audio is unusable, say so and ask for the brief in
writing. Do not reconstruct what you think they said.

---

## The audio pipeline, end to end

Thirteen steps, and the manifest records the result of each one. Skipping a step is
allowed; pretending it ran is not.

| Step | What it produces |
|---|---|
| Voice archetype | Who is speaking, in one sentence, recorded in `voice.archetype` |
| Pace, energy, accent, register | The direction given, not adjectives after the fact |
| Generation or recording | A real take, from a detected capability or a human |
| Duration measurement | The take against the script, per below |
| Comparison with the final script | The words said equal the words written, or the script is updated |
| Breath and pause placement | Where the read stops, deliberately |
| Scene synchronisation | `measured_voice_seconds` per scene, from the file |
| Level | The mix against the declared target |
| True peak | Measured, with the ceiling declared |
| Clipping | Checked, not assumed from the meter |
| Unintended silence | Head and tail, and anywhere the take dropped |
| Music ducking | The bed sits under the voice, with a recovery time |
| Licence and consent | For the voice, the music, and every effect |

`scripts/inspect_video.py` measures level, true peak, clipping risk and silence on
the finished export in one pass. The rest is judgement and it is recorded, not
inferred.

## Captions come from the take, never from the script

The script is what you meant to say. The take is what was said. Between them sit
a rephrase, a dropped word and half a second of breath, and captions built from
the script drift from the read within the first three cues.

Derive cues from the final take, keep them to short groups, respect a readable
pace, hold enough contrast, stay inside the safe zone for the ratio, and never let
them cover the subject or the CTA. Check them at their own boundaries, not in the
middle of a cue, because a caption that is one frame late is visible exactly at its
edges.

[The manifest](motion-manifest.md) refuses `captions.derived_from` set to anything
but `final_take`, and refuses a cue that ends past the end of the timeline.

## Measuring the take

Estimate the fit before generating, then replace the estimate with the measured
duration. Word-rate heuristics are language-specific warnings, not arithmetic.

Once the take exists, measure it and write the number into the storyboard as
`measured_voice_seconds`. `scripts/check_artifact.py` refuses a scene whose
narration is longer than the scene, and warns when narration was never measured,
because a line that reads fine on the page and runs two seconds long is the
usual way an ad misses its own cut.

When a line is rushed, shorten the line or lengthen the scene. Do not speed up
the take: accelerated speech is audible, and it reads as a mistake rather than
as energy.

Then listen end to end, once, without doing anything else:

- mispronunciations, especially the brand and product names;
- cut syllables and swallowed word endings;
- glitches, repeated words, unnatural stress, pauses that land wrong;
- intelligibility over the music bed, not in isolation;
- clipping and loudness, measured with an actual audio tool.

No universal loudness target is implied here. Choose the delivery requirement
for the placement, document it, and measure against that. Review the ad three
times: sound off with captions, sound on through speakers or headphones, and at
phone size. Captions must match the final take, not the script it came from. The one
deliberate exception is the aside in `video-assembly.md`: when the voice carries
something the caption should not repeat, the two channels differ on purpose.
That is a decision you record, not drift you discover at the end.

---

## What ships

The final file, the captions and transcript, the final script, the voice and
settings manifest, the consent record when a clone was used, and the rights
notes for anything licensed.

"Script ready" and "rendered, no voice yet" are incomplete statuses when a
voiced ad was requested. Say which one it is rather than delivering it as done.
