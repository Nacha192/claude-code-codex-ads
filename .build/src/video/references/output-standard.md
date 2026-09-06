# Output standard

The quality bar every phase of this skill answers to. It exists so that a
reader can tell, without asking, which parts of an output are observed, which
are guessed, and which are neither.

---

## Every deliverable states four things

1. **What it is** — one sentence. Not a preamble, not a restatement of the request.
2. **What it was built from** — the inputs, each with an evidence label.
3. **The work itself** — the copy, the creatives, the analysis.
4. **What it cannot tell you** — the gaps, and the specific decision each gap blocks.

Section 4 is the one that gets dropped. Keep it. An output with no stated limits
reads as complete, and a reader acts on it as though it were.

---

## Evidence labels

Every factual line carries one. No exceptions, including for lines that seem
obviously true.

| Label | Means |
|---|---|
| `export` | came from a downloaded report from the ad platform |
| `screenshot` | read off an interface |
| `url` | checked on a live page, with the URL cited |
| `library` | seen in a public ad library. Shows that an ad ran, and roughly how long. Nothing else |
| `notes` | supplied by the user in conversation |
| `hypothesis` | inferred, not observed |
| `needs_data` | cannot be assessed with what was provided |

`needs_data` is a real answer and is preferred to a confident guess. A column of
`needs_data` in a table is information: it tells the reader exactly which input
to go and find.

---

## Decision labels

Every recommendation ends in exactly one.

| Label | Means |
|---|---|
| `ship` | write it, launch it, no gate beyond normal review |
| `test` | launch it against a named control, with the control named |
| `rewrite` | the idea holds, the execution does not |
| `investigate` | the answer is outside the creative — the page, the offer, the tracking, the audience |
| `monitor` | leave it running, read it again on a stated date |
| `cut` | stop serving it |
| `approval_needed` | a person must approve before this runs |

`investigate` is not a soft `rewrite`. It says the creative is not the problem,
and rewriting it will waste a fortnight. Use it when the evidence points off the
creative, and name where it points.

### A decision label is a recommendation, never an authorisation

`ship`, `test`, `cut`, `monitor` describe what this analysis concludes. None of
them grants permission to launch an ad, spend money, pause a live creative, or
move a budget. Those are a person's decisions, made in the account, and holding
the access changes nothing about that. A pack that writes `cut` and then
switches something off has confused an opinion with a mandate.

---

## Confidence

`high`, `medium`, `low`. The ceilings in `thresholds.md` are binding: no output
carries a confidence above the ceiling its evidence allows, however convincing
the reasoning feels.

State the confidence **and** the thing that would raise it. "Low; a 14-day
export with per-creative video plays would make this medium" is useful.
"Low confidence" alone is a shrug.

---

## Skills that produce copy carry two extra obligations

**1. Every factual claim names its source, before the ad runs.**

A number, a comparison, an outcome, a superlative. Source means a document, a
dashboard, a named customer, or a live page. Not "the team said". Any line
without one is marked `[claim: needs source]` and is `approval_needed`,
whatever else its verdict says.

**The marker is never stripped to make a set look finished.** A marked line is
not shippable copy. It waits for the source, or it is rewritten without the
claim. Marked lines are ranked outside the shippable set, never inside it.

**2. Character limits are counted, not estimated.**

In the language being shipped, on the shipped string, including spaces. A
headline reported as fitting when it does not is a defect that reaches the
customer.

---

## Ranking is a judgement, and says so

When this skill ranks hooks, angles, or creatives before they have run, the
ranking is an opinion informed by pattern, and it is labelled `hypothesis`.
It is not a prediction of performance and must never be written as one.

The honest form: "Ranked on how specifically each opening names the reader's
situation. This is a judgement, not a measurement, and the account will
disagree with it about a third of the time."

---

## Never do these

- **Never invent an example and present it as observed.** No fabricated
  competitor ad, no invented review, no illustrative metric that reads like a
  real one. If you need an example to explain a structure, label it
  `illustration` and make it obviously generic.
- **Never report an asset as produced unless it is on disk** and its dimensions
  or duration were read back. A successful API response is not a file.
- **Never present a translated hook as a written one.** See `lang.write_native`.
- **Never fill a gap with a plausible value.** `needs_data` costs one line and
  saves a wrong decision.
- **Never carry a recommendation on evidence that cannot support one.** Where
  the only input is a public ad library, the output is the structure, with no
  ranking and no "worth testing" attached. A recommendation is a performance
  claim wearing a verb.
