# Copywriting

The ad's only job is to earn the click. Not to close the sale, not to educate
fully, not to be admired. Every rule below serves that one job.

---

## The three fields, and what each is for

| Field | Limit | Job |
|---|---|---|
| **Primary text** | first `limits.meta_primary_text_visible` characters carry it | qualify the reader and open the loop |
| **Headline** | `limits.meta_headline_visible`, target `limits.meta_headline_mobile_safe` | the promise, in one line, readable at a glance |
| **Description** | `limits.meta_description_visible` | reassurance. Often hidden entirely — put nothing load-bearing here |

Count the characters. In the shipped language. On the shipped string. See
`lang.count_in_target` — the same sentence runs about a fifth longer in French
or German than in English, so a headline that fits in your draft language will
be cut in the market's.

---

## Step 1 — Classify before writing

Four decisions. Get them from `ads/brief.md`; ask if they are missing. Writing
before these are settled produces copy that is competent and aimed at nobody.

**1. Awareness level.** From `intake-and-avatar.md`. It decides your opening,
your length, and where the click lands. It is the single most consequential
choice on this page.

**2. Temperature.** Cold, warm, retargeting. A cold ad and a retargeting ad for
the same angle are different jobs and are never ranked against each other.

**3. Sell the click, or sell the solution.**

- **Sell the click** — short text, curiosity in the image, little revealed. The
  landing page does the selling. Right for unaware and problem-aware readers,
  for products that need explaining, and for higher prices.
- **Sell the solution** — the ad itself does the work: demonstration, proof,
  specifics. The page only has to close. Right for solution-aware and above,
  simple products, visual products, lower prices.

The rule that follows and gets forgotten: **if you show the product, the viewer
becomes product-aware.** Never send a product-aware viewer to a page that
withholds what the product is. They have already seen it; the withholding now
reads as a trick.

**4. Format.** Static plus text, short first-person video, demonstration, story.
See `static-ads.md` and `video-ads.md`.

---

## Step 2 — The shape of the primary text

```
Line 1     the hook. Situation, not person. Under limits.first_line_words
           ── everything below this line is only read by people the hook caught ──
Body       the current workaround, and where it fails
Turn       the product enters, as the answer to that failure
Proof      one specific thing. A number with a source, or a physical detail
Offer      trial, return, shipping, code. Plainly, once
Call       one action
```

Notes that matter more than the shape:

- **The first line is the entire ad** for most impressions. Write it last, from
  the best material in the rest, then move it to the top.
- **The turn is where writers go soft.** "That's why we made…" is a hinge, not
  a sentence. Name the mechanism instead: what physically changed, and why that
  fixes the failure you just described.
- **One proof, not four.** Four proofs read as a brochure and each one weakens
  the others. Pick the one a sceptic would check.
- **The offer is not the angle.** A discount in a cold ad buys nobody who was
  not already interested. Discounts belong in retargeting.
- **One call to action.** Two is an unmade decision passed to the reader.

---

## Step 3 — Write in the market's language

`lang.write_native`. **Ads are written in the target language, not translated
into it.** Translation preserves meaning and loses rhythm, and rhythm is most of
a hook.

The workflow:

1. Write the hook **in the target language first**, from the buyer's own
   sentence where you have it.
2. Check idiom: would a person actually say this, here, out loud
   (`lang.idiom_check`)? Grammatically perfect and idiomatically dead is the
   standard failure of translated advertising, and it is invisible to the
   person who wrote it.
3. Check register. Formality, and how directly you may address a stranger, vary
   enormously between markets — and between variants of one language. Québécois
   French is not Parisian French; UK English is not US English.
4. Count characters **after** translation, never before.
5. If you cannot read the target language well enough to judge idiom, **say
   so**, and get a native check before it ships. That sentence costs you
   nothing and saves a campaign.

The back-translation into the operator's language is for their understanding
only, and it is labelled as such. It is never the artefact that ships.

---

## Step 4 — Do not sound like a machine

This is not a matter of taste. Machine-shaped copy underperforms because
readers have learned the shape and stop at it.

### Cut on sight

| Pattern | Why it fails |
|---|---|
| "In today's fast-paced world" and every cousin | says nothing, costs you the first line |
| "Say goodbye to X, say hello to Y" | recognisable as filler in every language |
| "Unlock", "elevate", "revolutionise", "game-changer", "seamless", "effortless" | category words with no content |
| "It's not just X, it's Y" | a construction, not a thought |
| "But here's the thing:" | manufactured suspense |
| Three adjectives in a row | one adjective is a choice; three is padding |
| Rhetorical question openers with no answer | the reader answers "no" and leaves |
| An emoji doing a word's job | reads as a template |
| A tidy summarising last line | ads end on an action, not on a bow |

### Structural tells

- **Every sentence the same length.** Real speech varies. Two words. Then a
  longer one that carries the actual information and takes its time getting
  there.
- **Every paragraph three lines.** A visible template.
- **Perfect parallelism** across bullets. People do not write that way.
- **No specifics.** The reliable difference between human and machine copy is
  the concrete detail: the hour, the material, the number, the room. Machines
  generalise because generalising is safe.
- **Nothing at stake.** Copy that could not offend anyone persuades nobody.

### Punctuation

**Do not use em dashes.** They are the single most recognisable machine-writing
tell in 2026, in every language. Use a comma, a full stop, or restructure the
sentence. Parentheses and colons are fine.

Keep exclamation marks to zero or one per ad. Ellipses to zero.

### The test

Read it aloud. Where you stumble, a reader stops. Where you would not say it to
one person across a table, rewrite it.

---

## Step 5 — Six checks before it ships

Run all six on every piece. This is where copy becomes shippable, or does not.

1. **Counted.** Every field, in the shipped language, against `thresholds.md`.
2. **Situation, not person.** No asserted personal attribute, in words or
   picture. See `compliance.md`. This one is a cut, not a rewrite.
3. **Sourced.** Every number, comparison, outcome, and superlative names its
   source, or carries `[claim: needs source]` and leaves the shippable set.
4. **Specific.** At least one concrete detail a competitor could not have
   written. If nothing here is specific to this product, you have written the
   category's ad, not yours.
5. **One change.** Variants of one another differ in exactly one element
   (`test.one_change_rule`), and you can name it.
6. **Match.** The landing page carries the same promise, the same offer, and the
   same call to action. A mismatch is a refund and a policy flag, not a nuance.

---

## Variants that produce a finding

Three per angle. Each differs from A in **one** thing:

- **A** the reference.
- **B** the opening move changes. Same angle, same offer, different way in.
- **C** the length changes. Same angle, same opening move, short against long.

Three variants differing in two things each produce a result that applies to
nothing. Note the changed element next to each one, in the file, so the person
reading the results in three weeks does not have to reconstruct it.

Check `coverage.angle_distinctness` before counting angles: two lines sharing
their main claim **and** their reason are one angle wearing two hats.

---

## Frameworks worth keeping

Not a menu to fill in. Use one when you are stuck, then delete the scaffolding.

- **Awareness first** (Schwartz). The reader's knowledge decides the opening.
  If you keep one idea from any framework, keep this.
- **Problem, workaround, failure, mechanism.** The spine of nearly every good
  direct-response ad, and the reason the workaround test in
  `intake-and-avatar.md` exists.
- **One reader.** Write to a single person you can picture, in a specific room,
  at a specific hour. Copy written to a segment sounds like it.
- **Sell the gap.** People buy the distance between where they are and where
  they want to be. Name both ends concretely and the product sells itself in
  between.
- **The sceptic's question.** After every claim, ask "why should I believe
  that", and answer it in the next line or cut the claim.

---

## Output

```markdown
### Angle <n> — <the argument, one sentence>
Awareness: <level>   Temperature: <cold|warm|retargeting>
Strategy: <sell the click | sell the solution>   Destination: <url>

**A — reference**
Primary text:
> <text>
First line: <n> chars   Headline: `<text>` (<n>)   Description: `<text>` (<n>)
Call to action: <button>
Claims: <sourced, or listed with [claim: needs source]>

**B — <the one changed element>**
...

**C — <the one changed element>**
...

Six checks: 1 ✓  2 ✓  3 ✓  4 ✓  5 ✓  6 <✓ or the mismatch>
Language written natively: <yes | translated, needs native check>
```
