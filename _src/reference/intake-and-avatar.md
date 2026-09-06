# Intake: who you are, what you sell, and who is on the other end

Nothing in this pack runs before this file has an answer. Not the scraping, not
the hooks, not a single generated image. An ad written without this is a
well-crafted sentence aimed at nobody, and it costs the same to run as a good
one.

---

## Part 1 — The three blocking questions

If any of these is unknown, **stop and ask**. Do not assume, do not infer from
the folder name, do not start with a placeholder and promise to fix it later.

**1. Market: which country, and which language do the ads run in?**
Everything downstream depends on it — the library search, the character counts,
the idiom, the compliance regime. "English" is not an answer; UK and US are
different markets with different spelling, different price psychology, and
different regulators.

**2. What is being sold, in one sentence a stranger would understand?**
Not the category. Not the brand promise. What arrives, and what it does. "A
memory-foam cushion held by a strap around the thigh, so it stays between the
knees all night" is an answer. "Premium sleep solutions" is not.

**3. What is your own brand called, including the aliases?**
Needed to exclude yourself from the competitive pull. Without it, you will
find your own ads, count them as market evidence, and conclude the market
agrees with you.

**Why exactly three.** Every other gap can be filled with a stated assumption
that a reader can check and overturn. These three cannot: a wrong answer here
does not degrade the output, it invalidates it.

---

## Part 2 — The essential set

Ask for these. If the user does not have them, **proceed with a stated
assumption**, labelled `hypothesis`, and put it in the output where a reader
will trip over it. Do not block.

| # | Question | Default if unknown |
|---|---|---|
| 4 | Who buys it — age band, situation, and the moment they start looking | Inferred from the product and the competitive pull. Always `hypothesis` |
| 5 | Price, and the offer around it (trial, return, shipping, code) | Ask before writing any offer line. Never invent a price or a guarantee |
| 6 | What the product replaces — the thing they do today instead | Inferred. See the workaround test below |
| 7 | Proof available: reviews, numbers, certifications, named customers | Assume none. Write copy that needs none, and mark anything that does |
| 8 | Destination: which page does the click land on | Ask. A campaign with no destination is not a campaign |
| 9 | Named competitors | Discovered by the scrape rather than asked |
| 10 | Brand constraints: banned words, tone, existing visual identity | Assume the red line in `compliance.md` and nothing more |
| 11 | Where the buying happens: platform, account access, who launches | Assume you produce files and a person launches them |

**Never invent 5 or 7.** A made-up price and a made-up review are the two
fabrications that reach the customer and become someone else's legal problem.

---

## Part 3 — The workaround test

Run this before writing a single hook. It is the fastest way to find out
whether your best selling point means anything.

> **You cannot sell headphones to someone who has no phone.**

Your product's advantage almost always assumes a **prior gesture** — something
the buyer already does. If the advantage of your cushion is a strap that stops
it sliding, the prior gesture is *already putting something between your knees
to sleep*. To a person who has never done that, the strap answers a question
they never asked. It is not a weak benefit; it is an invisible one.

So name three things and keep them apart, because they belong in three
different places in the ad:

| | What it is | Where it goes |
|---|---|---|
| **The lived problem** | what actually hurts, in situation terms | **the hook.** The big line |
| **The current workaround** | the fix they already improvised | the body. It qualifies the reader |
| **The failure of the workaround** | why their fix does not hold | the turn, where your product enters |

Opening on the failure of the workaround ("your pillow ends up on the floor")
is opening on a second-order subject. It only lands for the minority who
already have the pillow between their knees. The hook is always the lived
problem: *3 a.m. Third time.*

---

## Part 4 — The awareness ladder

Adapted from Eugene Schwartz. It decides your opening, your length, and where
the click goes. Getting it wrong is not a stylistic error; it is an ad talking
past its reader.

| Level | They know | The creative must | Length | Send to |
|---|---|---|---|---|
| **Unaware** | nothing, including that this is a problem | **reveal** — name the situation before naming any product | long | article or advertorial |
| **Problem-aware** | it hurts, no idea there is a fix | name the situation vividly, tease the mechanism | medium-long | advertorial or long-form video |
| **Workaround-aware** | the problem, and their own improvised fix | **confirm**, then show why the improvisation fails | medium | product page |
| **Solution-aware** | that products like yours exist | differentiate the mechanism, not the brand | medium | product page |
| **Product-aware** | you specifically, and they hesitate | remove risk: trial, return, guarantee, objection | short | product or checkout |

**Reveal and confirm are opposite movements.** A creative that confirms, shown
to someone unaware, is meaningless. A creative that reveals, shown to someone
who already knows, is condescending, and they can feel it in the first line.

### Classify every creative before spending on it

For each one, write the exact sentence that assumes something about the reader,
then place it on the ladder. This takes four minutes and routinely finds that a
"cold traffic" set contains one cold creative and three retargeting creatives
nobody labelled.

Then apply `coverage.awareness_spread`: **one awareness level per ad set.** If
all your creatives sit at the same level, run **one** ad set. Two ad sets halve
the speed at which you learn anything, and showing "you have already tried
wedging a pillow" to someone who never has is paying for nothing.

---

## Part 5 — The avatar, and the one rule about it

An avatar is worth writing when it is specific enough to rule things out. Four
short paragraphs beat a two-page persona document with a stock photo.

Write:

1. **The moment.** Not demographics. The specific minute when the problem is
   most present, described physically. Where they are, what time it is, what
   they just did.
2. **The sentence they say to themselves.** In their words, in their language,
   not in marketing language. This is the raw material for the hook.
3. **What they have already tried, and why it stopped working.** From the
   reviews of the products they tried, not from imagination.
4. **What would make them not buy.** The objection, stated as they would state
   it. Half of the ad set exists to answer it.

### The rule

> **The avatar is allowed to be in pain. The ad is not allowed to tell them so.**

The pain lives in your document, and it drives every choice. It never appears
in the creative as an attribute of the reader. That is not squeamishness, it is
`compliance.md`: naming a health, financial, or personal state as belonging to
the reader is a policy rejection, and in a regulated category it is worse than
that.

What goes in the ad instead: the hour, the position, the object, the movement,
the room. The reader supplies the pain themselves, and it lands harder because
they did.

---

## Part 6 — Recording it

Write the answers to a file in the project, not into the conversation. Suggested
`ads/brief.md`:

```markdown
# Ad brief — <product>
Market: <country> / <language>       Updated: <date>
Sells: <one sentence>
Our brand + aliases: <names>          (excluded from all library pulls)

## Essential
Buyer: <...>                          [notes|hypothesis]
Price and offer: <...>                [notes]
Replaces: <...>                       [notes|hypothesis]
Proof on hand: <...>                  [notes]
Destination: <url>                    [url]

## Workaround test
Lived problem: <...>
Current workaround: <...>
Why it fails: <...>

## Awareness target for this batch
Level: <...>   →  one ad set

## Red line
<10-20 forbidden terms, from compliance.md>

## Open assumptions
- <assumption> — would be overturned by <the input that would settle it>
```

Every later phase reads this file. When something in it turns out to be wrong,
correct it there rather than in the next conversation, or the correction is
lost the moment the session ends.
