# The production manifest

One file, `motion-project.json`, holds the whole job: the brief, the argument, the
scenes, the voice, the captions, the rights, the engine actually used, the render
commands, the exported files with their hashes, and both QA verdicts.

It exists because the alternative is a conversation. Six weeks later nobody can say
which claim had a source, which voice was licensed for what, or whether the vertical
was composed or cropped. The manifest is what survives the conversation.

**Validate it with `scripts/check_motion_project.py`.** A non-zero exit is a stop,
not a note. A complete valid example ships at `examples/motion-project.example.json`.

```
python scripts/check_motion_project.py motion-project.json
python scripts/check_motion_project.py motion-project.json --root .
```

With `--root`, every export path is opened and its `sha256` recomputed. Use it before
delivering: it is the difference between a manifest that describes files and a
manifest that describes intentions.

**Paths stay inside the project.** An export or asset path that is absolute, or that
climbs with `..`, is refused, and so is one that is textually clean but resolves out
of the tree through a link. A manifest names the files this job produced. A hash that
matches something else on the machine proves nothing about this delivery, and without
that rule a manifest written anywhere could pass by pointing at a file nobody here
made.

---

## The state machine

`state` is one of eight, in order, and it is what the delivery is judged on.

| State | Means |
|---|---|
| `planned` | Brief, lock, scenes exist. Nothing has been made. |
| `generated` | Media or voice was produced. Nothing is assembled. |
| `rendered` | Files exist on disk, listed in `exports` with hashes. |
| `measured` | `inspect_video.py` ran on every export. |
| `inspected` | Both QA grids ran, technical and creative. |
| `corrected` | Defects were fixed at the source and the affected formats re-rendered. |
| `approved` | No blocking defect is open, both verdicts stand. |
| `delivered` | Handed over with everything in the output standard. |

The validator ties the state to the evidence. From `rendered` on, exports must exist
and carry a `sha256`. From `inspected` on, both QA blocks must carry a verdict from
`pass`, `pass_with_noted_risk`, `fail`. At `approved` and beyond, a failed verdict or
an open blocking defect is an error.

**Never advance the state to describe an intention.** The state is a claim about the
world, and it is the one claim in this pack a script can actually check.

---

## Sections

| Section | Holds | Refused when |
|---|---|---|
| `brief` | offer, audience, objective, market, ad_language, cta_destination, duration_seconds, formats | Any of those is empty, or a format is not a ratio |
| `assumptions` | what was decided without an answer, why, and what changes if wrong | An assumption with no `changes_if_wrong` |
| `evidence` | id, type, source, what it supports | Duplicate ids |
| `claims` | text plus `proof_ids` into evidence | No proof, unknown proof, or proof typed `hypothesis` |
| `creative_lock` | the thirteen fields of phase 2 | Any one of them empty |
| `hooks_considered` | at least three, each scored on the seven criteria, exactly one selected with a `why` | Fewer than three, no reason, or a lock hook that is not the selected one |
| `script` | the spoken text and the word count | |
| `scenes` | the storyboard fields, per [the production contract](production-contract.md) | Overlaps, a scene ending before it starts, narration longer than its scene, a timeline outside the brief |
| `voice` | archetype, source, provider, measured seconds, consent reference | Narration exists with no voice object, or a cloned voice with no consent |
| `captions` | `derived_from`, style, cues with start, end, text | `derived_from` is not `final_take`, or a cue ending past the timeline |
| `music`, `sfx` | what plays, and the rights for it | |
| `assets` | id, path, rights, and for people the release and its expiry | An asset with no rights, a person with no release or no expiry, or a path that leaves the project |
| `loudness_target` | value, unit, and **where the number came from** | No `source` |
| `engine` | kind, name, version, `detected: true`, and why it was chosen | `detected` is not literally true |
| `formats` | ratio, width, height, fps, safe zones and **its own composition** | Dimensions that contradict the ratio, an empty composition, a brief format never composed |
| `render` | the commands, verbatim | |
| `exports` | ratio, path, sha256, state, measurements | Missing hash, a path that leaves the project, missing file when `--root` is given, a composed format never exported |
| `qa.technical`, `qa.creative` | verdict, defects, and for creative the reviewer | A failed verdict on an approved project, a blocking defect left open |
| `human_decisions_pending` | what a person still has to decide | Reported as a warning at delivery, never hidden |

---

## The defect record

Every defect, in either grid, carries seven fields. All seven are required, because
each one is a question someone will ask later.

| Field | The question it answers |
|---|---|
| `timecode` | Where exactly |
| `observation` | What was seen, not what was inferred |
| `severity` | `blocking`, `high`, `medium`, `low` |
| `why_it_fails` | Which rule or effect it breaks |
| `fix` | The concrete change, not "improve it" |
| `target` | The scene, the field, or the file to change |
| `status` | `open`, `fixed`, `accepted`, `deferred` |

`accepted` is a real outcome. Recording a deliberate choice as accepted stops the
next reviewer from repairing it by mistake.

---

## What the validator cannot do

It reads JSON. It never opens a video, never runs OCR, never looks at a frame. A
manifest built from the plan instead of from the render passes every rule here while
describing an asset nobody watched.

That is why `state` from `measured` onward requires `inspect_video.py` to have run,
and why the creative grid exists at all. The two scripts and the human pass cover
three different failures, and none of them covers the other two.
