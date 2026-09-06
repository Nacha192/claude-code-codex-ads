# Depth modes: standard, and second brain

Two ways to run this pack. They differ in **what work actually happens**, not in
how much the output insists on its own quality.

| | Standard | Second brain |
|---|---|---|
| Model | `GPT-5.6` | `Astra-6` |
| Reasoning | ordinary | maximum the session allows |
| Passes | write, then the six checks | write, then **six additional passes**, then the six checks |
| Good for | one batch of variants, a rewrite, a copy fix, a render | a launch, a market you have not run before, a rebuild after a failed month, anything above a few hundred a day |
| Cost | minutes | tens of minutes, and it will disagree with you |

`The model names are the intended targets, not a guarantee. Inspect what your session actually offers, and never claim a model switch that was made only by writing its name in a prompt. Where the named model is unavailable, say so and ask the user which of the available ones to run.`

**Standard is the default.** Second brain is invoked, by the user or by a
trigger below. A pack that always runs at maximum depth gets switched off within
a week, and rightly.

### Escalate to second brain when

- The batch is the first for a product, a market, or a language.
- Money above a few hundred a day depends on it.
- The last batch failed and nobody can say why.
- Two people disagree about the angle.
- The category is regulated (`compliance.md`).
- The user asks for it.

### Do not escalate for

A copy fix, one more variant of a winner, a re-render at a new ratio, a
character-count correction. Deep mode on a mechanical task produces the same
output more slowly, with an essay attached.

---

## What second brain actually does

Six passes, in order, each producing a written artefact. If a pass produced no
artefact, it did not run, whatever the output claims.

### Pass 1 — Evidence

Every input gets a label from `output-standard.md` before anything is written.
Then the question that decides the ceiling: **what does this batch rest on?**

If the honest answer is "a library pull and a guess about the buyer", the
ceiling is `low`. Say it at the top of the output, not in a caveat at the
bottom.

**Watch the boundary here.** Where the *only* evidence is a public ad library,
`output-standard.md` allows no recommendation at all, and `test` is a
recommendation. The deliverable in that case is the structure, with the limit
stated and nothing attached to it. A `test` verdict needs at least one input the
library cannot give: the account's own export, the user's stated offer, a real
customer sentence. Say which one you have.

### Pass 2 — Counting

Everything countable is counted, never estimated:

- Characters per field, in the shipped language.
- Distinct angles, after collapsing with `coverage.angle_distinctness`.
- Creatives per awareness level.
- Ratios present per creative.
- Claims, and how many are sourced.
- Spoken words in each hook.

The counting pass is where most batches are found to be smaller than they look.
Twelve creatives collapse to three angles wearing four coats. That finding is
worth more than the twelve creatives.

### Pass 3 — Adversarial

Take the finished batch and attack it as somebody who wants it to fail. Not a
polite review. Four specific attacks, in writing:

1. **The buyer who has never done the prior gesture.** Which creatives are
   meaningless to them? (The workaround test, `intake-and-avatar.md`.)
2. **The compliance reviewer.** Which line asserts something about the reader?
   Which claim has no source? Which picture is the claim?
3. **The competitor.** Which of our lines could they run tomorrow without
   changing a word? Those lines are the category's, not ours, and they are
   doing no work.
4. **The person reading the results in six weeks.** Given how this batch is
   built, which question will they be unable to answer? If two variants differ
   in three ways, that question is "which change did it".

Write the answers. Every one of them will produce at least one cut.

### Pass 4 — Elimination

**Cut the batch to what earns its place.** This is the pass that makes the
difference, and it is the one that feels wrong to do.

A batch of twelve where four are strong is worse than a batch of four. The eight
split the budget, delay every reading past `test.volume_floor`, and teach
nothing. Volume is not coverage.

Rank, cut everything below the line, and **say what you cut and why**. If the
brief demanded twelve, deliver four and say plainly that eight would be paid
noise, and what would have to be true for them to be worth running.

### Pass 5 — Transfer

For every element in the batch, ask: **does this work because of the argument,
or because of us?**

Anything that depends on brand recognition, a licensed asset, a known face, a
price nobody else can match, or a catalogue you do not have, is marked as
non-transferable. This matters for two reasons: it stops you copying the part of
a competitor's ad that only works because they are them, and it tells you which
of your own wins will survive a rebrand.

### Pass 6 — Regret

One question, answered in writing before shipping:

> Six weeks from now, when this has underperformed, what will we wish we had
> checked today?

Then check the top two answers, or state plainly that you did not and why.

This pass exists because the standard failure of an ad batch is not a bad
creative. It is a batch built on an assumption nobody wrote down: the wrong
awareness level, a landing page nobody opened, a tracking event that never
fired, a price the market will not pay.

---

## The anti-slop contract

Deep mode's output must be **different in kind**, not just longer. These are
binding, and they are checkable.

1. **Nothing generic survives.** Any line that could run for a competitor
   without edits is cut in pass 3. Specificity is the deliverable.
2. **Every number is counted or cited.** No "roughly", no "around 125
   characters", no estimated word counts.
3. **The output says where it disagrees, and why.** With the brief, with the
   angle, with a competitor pattern, with an earlier decision.

   **Never manufacture a disagreement or a cut to satisfy this rule.** A
   fabricated objection is worse than none: it costs the reader a real decision
   and it teaches them to discount the next one. Where the passes genuinely
   found nothing to change, the honest output is an evidence-based no-change
   finding that names what was attacked and why it held. That is a valid result
   of a deep pass, and it is rare enough to be worth saying plainly.
4. **The cut list is part of the deliverable**, with reasons. And **never
   silently deliver fewer items than were asked for**: name what was rejected,
   why, and the size of the remaining gap, so the person who asked for twelve
   can decide whether to accept four or to change the brief.
5. **The limits are stated in section four**, per `output-standard.md`, with the
   specific decision each gap blocks.
6. **No em dashes, no template phrasing.** See `copywriting.md`. This applies to
   the analysis as well as to the ad copy.
7. **Length is not effort.** If the honest answer is four hooks and one cut, the
   output is four hooks and one cut.

---

## Second brain means it remembers

The other half of the name. A brain that starts from zero every session is a
very fast intern.

### The ledger

Deep mode maintains `ads/LEDGER.md` in the project, and reads it before writing
anything:

```markdown
# Ledger — <product>

## Decided, do not relitigate
- 2026-09-02  Awareness target for cold: workaround-aware. Reason: <...>
- 2026-09-04  Price stays off cold creatives. Reason: <...>

## Tried and failed
- v9 offer-led statics. 14 days, under volume floor. Read: inconclusive, not
  a loss. Do not re-run without more budget or fewer variants.

## Assumptions still open
- Buyer age band is inferred, not observed. Would be settled by: the account's
  own demographic breakdown.

## Numbers moved from thresholds.md
- coverage.angles_per_ad_set: 3 → 2. Reason: ad set under test.volume_floor.
```

Three rules for it:

- **A decision recorded here is not reopened** without a new fact. The most
  expensive failure mode of an agent with no memory is rediscovering, every
  fortnight, the thing you settled in March.
- **A failure is recorded with its reading.** "Inconclusive" and "lost" are
  different entries and lead to opposite next moves.
- **An assumption is recorded with what would settle it.** That is what turns it
  from a shrug into a task.

### What to write down, and where

| Fact | Home |
|---|---|
| Who we are, what we sell, the market | `ads/brief.md` |
| A decision, a failure, an open assumption | `ads/LEDGER.md` |
| A number moved from its default | `ads/LEDGER.md`, with the reason |
| Research pulls | `ads/research/<market>-<date>/` |
| What changed between batches | `ads/creatives/v<N>/README.md` |

Files in the project, not memory in a session. The session ends. The account
does not.

---

## Saying which mode ran

Every output opens with one line:

```
Mode: second brain (Astra-6) · passes 1-6 complete · ledger read and updated
```

or

```
Mode: standard (GPT-5.6) · six checks only · escalate if <the trigger that applies>
```

Never claim a pass that did not produce its artefact. An output labelled second
brain with no cut list and no disagreement is standard output wearing a badge,
and the person reading it will make a bigger bet than the work supports.
