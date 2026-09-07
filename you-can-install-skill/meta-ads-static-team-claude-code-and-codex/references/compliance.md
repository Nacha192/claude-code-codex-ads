# Compliance, claims, and the red line

Two different things get confused here constantly, so separate them first.

- **Policy rejection** costs you a day and an appeal. Annoying.
- **A regulatory problem** costs you the account, the product listing, or a
  visit from a consumer-protection authority. Not annoying.

A creative can sail through platform review and still be illegal. Review is a
filter, not a permission.

---

## The personal attributes trap

This is the single most common way a good ad gets killed, and it is invisible
to the person who wrote it.

Meta prohibits copy that **asserts or implies knowledge of a personal
attribute** of the reader: a health condition, a financial situation, a
criminal record, a sexual orientation, a religion, a disability.

The trap is that the strongest-feeling line is usually the prohibited one:

| Prohibited | Why | Allowed instead |
|---|---|---|
| "Back pain keeping you up?" | attributes a medical condition to the reader | "3 a.m. You turn over again." |
| "Struggling with debt?" | attributes a financial state | "The minimum payment is not the payment." |
| "Tired of being single?" | attributes a relationship status | "Saturday, and the group chat is quiet." |
| "Your acne is ruining your confidence" | attributes a condition **and** a feeling | "The ring light knows. The mirror knows." |

**The rule that generalises:** describe the **situation**, never the **person**.
The hour, the position, the object, the movement, the room. The reader connects
it to their own condition without help, and it lands harder than the version
that named it, because they did the work.

A **sensation** passes. A **symptom** does not.

This applies to the picture as well as the words. A before-and-after of a body
is an assertion about the reader in most restricted categories, whatever the
caption says.

---

## Restricted categories

Health and wellness, finance and credit, employment, housing, dating, politics
and social issues, alcohol, gambling, weight loss, cryptocurrency, and anything
addressed to minors.

Every major platform documents special requirements for these, and the
requirements change. **This pack does not issue verdicts in a restricted
category.** It routes you to the platform's current policy page and to a
qualified human, and it says which category it hit and why.

What it will do is flag the line that put you there. That is usually more
useful than the policy citation.

---

## The red line, and why you write it down

A **red line** is the list of words and constructions that must never appear in
your creatives for this product. It comes from three places:

1. **Regulation for your category.** In the EU, a non-medical product that
   claims a therapeutic effect becomes a medical device by claim, with the
   documentation burden that implies. In the US, the equivalent trap is a
   structure-function claim that crosses into a disease claim.
2. **Platform policy.** The personal attributes list above.
3. **The product's own honesty.** Words that describe something your product
   does not do, however commercially convenient.

Write the list once, per product, before the first creative. Ten to twenty
terms. Then enforce it mechanically.

### Enforce it on the rendered text, not the source file

This is the part everyone gets wrong. Grepping the source of an ad engine or a
copy document is worthless: the comments in the file quote the forbidden terms
in order to explain why they are forbidden, so the check fires on its own
documentation and then gets disabled for crying wolf.

**Render the creative, extract the text a human would actually see, and check
that.** For an HTML ad engine, execute the templates and read the produced
string. For an image, read the text you supplied to the generator, plus the
text visible in the output.

`scripts/check_artifact.py` runs the check, on a `creative` artifact: put the
rendered strings in the copy fields, list the terms in `prohibited_terms`, and
it exits non-zero on a hit. It matches whole words, case-insensitively, on the
copy you hand it, so handing it the template source instead of the rendered
output is the mistake described above, not a shortcut.

It also warns, every time, that the list only catches the terms you declared: a
paraphrase carrying the same forbidden meaning passes. That warning is not
noise to be silenced. Wire the check into the render step so a violating
creative cannot reach the export folder, and read the warning.

---

## Claims that need a source

Every number, comparison, outcome, and superlative, before the ad runs.

- **Numbers.** "Ships in 24 hours" is a claim. "Used by 4,000 people" is a
  claim. "Up to 40% quieter" is a claim and also a superlative.
- **Comparisons.** Naming or clearly implying a competitor invites a fight you
  have to be able to document. An unnamed comparison ("unlike ordinary X") is
  still a comparison and still needs a basis.
- **Superlatives.** "Best", "fastest", "the only", "number one". Qualified and
  sourced is fine. Bare is not.
- **Outcomes.** "Sleep through the night" is an outcome claim about a person.
  In a restricted category it is also a health claim.

Unsourced lines are marked `[claim: needs source]` and are `approval_needed`.
See `output-standard.md`.

---

## Reviews and testimonials

Three separate gates, and passing one does not pass the others.

1. **The review must be real.** Fabricating consumer reviews is illegal in the
   EU under the Unfair Commercial Practices Directive as amended by the
   Omnibus Directive, and in the US under the FTC's rule on fake reviews. Not a
   grey area, not a platform policy — a fine.
2. **You must have written permission** to use a named customer, their words,
   their face, or their logo in paid media. The permission is theirs to give,
   not the marketer's to assume. Always `approval_needed`.
3. **The claim inside the testimonial is still your claim.** "It cured my
   insomnia" in quotation marks is a health claim you published.

If a creative concept needs a review and you do not have one, **cut the
concept**. Do not soften it into an implied review ("people are saying…"),
which fails all three gates at once and adds dishonesty.

---

## Images and licensing, on an ad that will scale

Paid media is commercial use at volume with your brand attached, so the usual
casual sourcing does not survive it.

- **Never** an image carrying a stock watermark. It is not a placeholder you
  forgot to replace, it is evidence of the infringement, printed on the
  infringement.
- **Never** a competitor's product photography, packshot, or lifestyle image.
- **Never** an identifiable person's face without a model release, including
  faces that arrived in a "free" pack.
- **Generated imagery**: check the terms of the specific generator for
  commercial use, and be aware that a generated face that resembles a real
  person is still a likeness problem.
- **Fine**: your own photography, your client's, and genuinely
  commercial-use-licensed stock, with the licence recorded next to the file.

Record the source of every image in a `SOURCES.txt` alongside the assets. In
eighteen months, when someone asks, the file is the only thing that will
remember.

---

## The pre-flight check

Run before any creative leaves the folder. Eight lines. Do not skip it because
the batch is small.

1. Red-line check run **on rendered text**, exit code 0.
2. Every claim sourced, or marked and pulled from the shippable set.
3. No personal attribute asserted or implied, in words or in picture.
4. Character counts verified in the shipped language, against `thresholds.md`.
5. Restricted category identified, and routed if hit.
6. Image licences recorded for every asset used.
7. Reviews: real, permitted, and their claims sourced.
8. Landing page carries the same promise, offer, and call to action as the ad.
   A mismatch here is a refund request and a policy flag, not a nuance.
