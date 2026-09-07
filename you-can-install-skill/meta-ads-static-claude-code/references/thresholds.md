# Thresholds

Every number that gates a decision lives here: platform limits, sample sizes,
spend gates, retention windows. Skills and reference files cite a key
(`limits.meta_primary_text_visible`) instead of restating a value, so there is
exactly one place to correct when a platform moves.

Craft settings stay with their craft file. Encoding targets are in
`video-assembly.md`, tempo and mix distances are in `video-music.md`, because
they are read while doing that job and nowhere else. The rule is about the
numbers that must not drift between files, not about every digit in the pack.

If you need a gating number that is not here, add it here first, then cite it.

## Every entry carries a tag

- `[platform]` — stated by the platform in its own documentation or interface.
  Can be checked. Moves when the platform moves.
- `[heuristic]` — a practitioner starting point. Defensible, not authoritative.
- `[ours]` — a rule this pack invented, usually a safety or cost gate. Nobody
  else is claiming it.

## A range is not a threshold

"Three to five variants" means two people applying the same rule to the same
account land two variants apart, both correctly, and neither can defend the
number. So every entry is **one** value plus, where it genuinely depends on the
account, the rule for moving it.

Use the default. When you move one, say in the output which key you moved, to
what, and why. An unexplained recalibration reads as a fact and is worse than
the default it replaced.

---

## Denominators

Half of a threshold is the number. The other half is what it is measured
against. These are fixed here rather than left to the reader.

| Term | Means | Does not mean |
|---|---|---|
| **creative** | one ad as the platform counts it: one ad ID, its own asset, its own delivery | a concept, a file, or an ad name. Two ads sharing an image with different copy are two creatives |
| **angle** | the argument for why to act, written as one sentence | the format, the offer, or the visual. "It does not slide off at night" is an angle. "Carousel" is not |
| **hook** | the first 3 seconds of a video, or the first line of feed text plus the image, judged together | the headline field |
| **variant** | one deliberate change from a named control | any other file in the folder |
| **impressions** | impressions on that creative, that placement, that date range | account impressions |
| **conversions** | the primary conversion action configured on the campaign | every reported conversion including secondary ones. Where the real-money subset is needed, say "purchases" |

---

## Character and field limits

| Key | Value | Tag | Notes |
|---|---|---|---|
| `limits.meta_primary_text_visible` | **125 characters** | [platform] | Where Meta truncates primary text behind "See more" on most feed placements. The exact cut moves by device. Treat it as where the reader stops, not as a hard maximum. **Count it. Do not estimate it.** |
| `limits.meta_headline_visible` | **40 characters** | [platform] | Meta's own recommendation before truncation risk. |
| `limits.meta_description_visible` | **30 characters** | [platform] | Frequently hidden entirely on mobile. Never put anything load-bearing here. |
| `limits.meta_headline_mobile_safe` | **27 characters** | [heuristic] | What survives on a narrow phone. Use as the target; use 40 as the ceiling. |
| `limits.first_line_words` | **12 words** | [heuristic] | A practical proxy for `limits.meta_primary_text_visible` while drafting. Verify by counting characters before shipping. |
| `limits.video_hook_seconds` | **3 seconds** | [heuristic] | The window the opening has to earn the rest of the view. Widely used; published by nobody as a rule. |
| `limits.hook_spoken_words` | **8 words** | [heuristic] | What fits in `limits.video_hook_seconds` at ordinary delivery. Count words in the spoken line only. The on-screen line is shorter and simultaneous. |
| `limits.onscreen_line_chars` | **32 characters** | [heuristic] | A burned-in hook line longer than this stops being readable at thumbnail size on a phone. |
| `limits.ugc_length_seconds` | **15 to 45 seconds** | [heuristic] | The band where a first-person ad holds. Longer needs a reason, not a habit. Stated as a band because it is a production brief, not a verdict input. |

## Aspect ratios and sizes

| Key | Value | Tag | Notes |
|---|---|---|---|
| `ratios.required_set` | **4:5 and 9:16** | [heuristic] | Feed, and Reels/Stories. Two surfaces that genuinely want different frames. |
| `ratios.optional_set` | **1:1 and 1.91:1** | [heuristic] | Explore, Marketplace, right column, Audience Network, search results. Cheap to render if you already built the engine; skip them if you are hand-building each file. |
| `ratios.px.4x5` | **1080 × 1350** | [platform] | |
| `ratios.px.9x16` | **1080 × 1920** | [platform] | |
| `ratios.px.1x1` | **1080 × 1080** | [platform] | |
| `ratios.px.1.91x1` | **1200 × 628** | [platform] | |
| `ratios.crop_rule` | **missing 9:16 does not remove the vertical placements** | [platform] | With placement asset customisation off, which is the default, the platform transforms what you gave it: it crops, letterboxes, or pads with a generated background. You still get delivered, in a frame you did not choose, with your headline sometimes outside it. A missing ratio is a `rewrite` on the asset, never an `investigate` on delivery. |
| `ratios.safe_margin` | **12% of the short edge, on every edge** | [heuristic] | Nothing that must be read goes closer to an edge. On 9:16 also keep the **top 14% and bottom 20%** clear: that is where the platform paints its own interface over yours. |

---

## Coverage

| Key | Value | Tag | Notes |
|---|---|---|---|
| `coverage.angles_per_ad_set` | **3 angles** | [heuristic] | Below three live angles, a losing week cannot tell you whether the angle failed or the execution did. Drop to 2 only when the ad set is under `test.volume_floor`, because more variants on thin volume only splits it further. |
| `coverage.formats_per_angle` | **2 formats** | [heuristic] | One static, one video, per angle. Below this, a format effect reads as an angle effect. |
| `coverage.angle_distinctness` | **two angles are the same angle when they share their main claim AND their reason** | [heuristic] | "Saves you time" and "stop wasting hours" share both: one angle. "Saves you time" and "cheaper than the alternative" share neither: two. Applied **before** any angle is counted. An inflated angle count is the most flattering error an account makes about itself. |
| `coverage.awareness_spread` | **at most one awareness level per ad set** | [ours] | See `intake.md`. Revealing to someone who already knows is condescending; confirming to someone who does not know is meaningless. Creatives aimed at different levels belong in different ad sets, or in one ad set and one level. |

---

## Scraping the ad libraries

| Key | Value | Tag | Notes |
|---|---|---|---|
| `scrape.observation_floor` | **30 days of observed continuous running** | [heuristic] | Before a competitor ad's structure is worth decomposing. Roughly two learning periods, so an ad still live has survived at least one deliberate keep-or-kill decision by whoever pays for it. That is the whole of the reasoning and it is thin. Below it you are studying somebody's test, not their decision. |
| `scrape.lookback_window` | **90 days** | [ours] | Default search window. Long enough for `scrape.observation_floor` to mean something, short enough that the creative conventions still match the ones you are about to ship into. |
| `scrape.min_sample` | **15 ads across at least 5 advertisers** | [ours] | Below this you are describing one advertiser's taste and calling it a market pattern. If you cannot reach it, say so and label every pattern `hypothesis`. |
| `scrape.max_pull` | **60 ads per run** | [ours] | A cost and attention gate, not a data gate. Past sixty nobody reads the output, and the download volume starts to matter. Ask before exceeding it. Each of the three video pulls in `video-scraping.md` is its own run of thirty, so ninety videos across three runs never crosses this gate. Ninety in one run does. |
| `scrape.video_length_cap` | **60 seconds** | [ours] | Do not download or analyse longer than this unless the user explicitly asks. Long-form ads are a different craft and a much larger job. |
| `scrape.self_exclusion` | **the user's own brand is excluded before any pattern is counted** | [ours] | Requires knowing the brand name. This is one of the three blocking questions in `intake.md`. |
| `scrape.no_spend_rule` | **a public ad library shows that an ad ran and roughly how long** | [platform] | It does not show spend, results, or whether it worked. An ad running for months is evidence of a decision somebody kept making. Nothing more. Every performance statement derived from a library is `hypothesis`, and the output says so in its first line. |

---

## Testing and reading results

These are the buying-side numbers. A creative skill that ignores them produces
ads nobody can learn from.

| Key | Value | Tag | Notes |
|---|---|---|---|
| `test.min_runtime` | **14 days** | [heuristic] | Minimum elapsed time before reading a creative test. State the window as dates, not as a duration. |
| `test.volume_floor` | **50 primary conversions per variant, across the whole test** | [heuristic] | Stated as a total on purpose: an export carries counts, not weeks, so a per-week floor cannot be evaluated by anything that reads it. Below the floor, no creative verdict goes above `low` confidence. |
| `test.click_floor` | **300 link clicks per variant** | [heuristic] | The fallback when the test is judged on click-through rather than conversions. |
| `test.material_gap` | **20% relative difference** | [heuristic] | The business relevance floor. Smaller than this is not worth acting on even when it is real. This is not a test of whether the difference exists. |
| `test.one_change_rule` | **one changed element per variant pair** | [heuristic] | Hook, image, offer, or format. Change one. A pair differing in two produces a result that transfers to nothing. |
| `test.enhancements_rule` | **automatic creative enhancements void the one-change rule** | [heuristic] | Text variation, image expansion, music, and animation change the asset per impression, so the creative that served is not the one you uploaded. Ask which are enabled and **when they changed** before reading anything across two windows. Unknown means the read stops at `low`. |
| `money.relevance_floor` | **a difference must move cost per acquisition by 10% or more** to justify a budget change | [heuristic] | The rate-side twin of `test.material_gap`. A creative can win on click-through and lose on cost per acquisition, and only one of those pays. |
| `money.budget_step_cap` | **20% of the ad set budget per step, one step per `test.min_runtime`** | [heuristic] | Larger steps destabilise delivery and make the next readout unreadable. **This pack never moves a budget.** It states the step it would recommend and hands it to a person. |

---

## Early signals on video

Read `video-voice.md` for what to do with these. They exist to separate two
different failures that look identical in a summary: nobody starts the video,
and everybody leaves after they start.

| Key | Value | Tag | Notes |
|---|---|---|---|
| `early.min_exposure` | **1,000 impressions AND spend of at least one target cost per acquisition** | [heuristic] | Nothing in this block fires below both. The spend half matters more: a creative that has not yet spent one target acquisition cost has not had a chance to produce a conversion, so its zero is not information. |
| `early.duration_band` | **under 15 seconds, 15 to 30 seconds, over 30 seconds** | [heuristic] | Every early median is computed **inside** a band, never across an ad set holding several. Video length is a required input; without it the hold read is `needs_data`. |
| `early.hook_rate` | **3-second plays divided by impressions, below 0.6× the ad set median** | [heuristic] | The opening is not stopping anyone. Only against the ad set's own median, never against a published benchmark from someone else's account. |
| `early.hold_rate` | **plays at 50% divided by 3-second plays, below 0.6× the band median** | [heuristic] | The opening works and the body does not. **Defined on the 50% play, not on ThruPlay**: ThruPlay is completion or fifteen seconds, whichever comes first, so it means completion on a short ad and fifteen seconds on a long one. A median mixing both measures nothing, and the cuts made from it are noise. |
| `early.median_stability_floor` | **5 creatives in the band** | [heuristic] | Below this the median is one middle number driving real decisions. Under the floor, the hook and hold reads are `needs_data` and no cut fires on them. |
| `early.false_negative_rate` | **assume roughly 1 in 5 creatives cut this early would have gone on to win** | [heuristic] | Stated rather than hidden, because that is the trade being made for throughput. A working assumption, not a measurement: an account that logs its early cuts and their eventual outcomes should replace it with its own number. |

---

## Generation cost gates

These exist because an image or video model will happily spend real money in a
loop while producing worse output each pass.

**They apply to paid generation only.** Assembling an approved clip, burning
captions, running ffprobe, running the red-line check or building a library URL
costs nothing, invents nothing, and is deterministic. None of it needs a **new**
confirmation: it is already covered by the approval that produced the assets it
works on, as `core.md` says. Asking again before every local render trains the
user to click through the one prompt that actually matters.

What this does not mean is that local work escapes approval entirely. The
footage, the voice and the music being assembled came from somewhere, and that
somewhere was approved or it was not.

| Key | Value | Tag | Notes |
|---|---|---|---|
| `gen.ask_before_first_call` | **always** | [ours] | No **paid** image, video, or voice generation call is made before the user has chosen the tool and confirmed the run. Not once per session: once per run. Local rendering of assets you already have is not a generation call. See `providers.md`. |
| `gen.variants_per_run` | **4 paid generations** | [ours] | Default batch, counted in calls to a generator, not in creatives produced. Twenty engine renders from four generated photographs is one batch of four, not twenty. More than four and nobody compares them; they get skimmed. Raising it needs an explicit ask, and the ask states the cost. |
| `gen.max_retries_per_asset` | **2** | [ours] | Two regenerations of the same asset. On the third failure, stop and report what is wrong with the prompt rather than paying for another sample of the same mistake. |
| `gen.no_silent_fallback` | **never substitute one generator for another** | [ours] | If the chosen tool is out of credit, blocked, or missing, **stop and say so**. Do not quietly produce the asset elsewhere: the user believes they are looking at the output of the tool they chose, and every downstream judgement inherits that belief. |
| `gen.verify_on_disk` | **an asset does not exist until it is on disk and its dimensions were read back** | [ours] | Never report a render as done from the fact that a call returned 200. |

---

## Voice and audio

| Key | Value | Tag | Notes |
|---|---|---|---|
| `voice.worth_it_rule` | **a voice-over earns its cost only when the script carries information the picture cannot** | [ours] | A voice reading the on-screen text aloud is a wasted channel. See `video-voice.md`. |
| `voice.sound_off_default` | **assume sound off** | [heuristic] | Feed autoplay is muted. Every video must survive the mute test before a voice is commissioned, not after. |
| `voice.native_speaker_rule` | **a voice-over in a language you do not read is unverifiable** | [ours] | Generated speech in an unfamiliar language can be fluent and wrong. Either get a native check, or ship burned-in captions written by the same pass that wrote the script, so the reader can see what was meant. |

---

## Language

| Key | Value | Tag | Notes |
|---|---|---|---|
| `lang.write_native` | **ads are written in the target market's language, not translated into it** | [ours] | Translation preserves meaning and loses rhythm, and rhythm is most of a hook. Write the hook in the target language first. If the working language differs, the back-translation is for the operator's understanding, and it is labelled as such. |
| `lang.count_in_target` | **character and word limits are counted on the shipped language** | [ours] | The same sentence is routinely 20% longer in French or German than in English. A headline that fits in the draft language and not in the shipped one is a headline that will be truncated. |
| `lang.idiom_check` | **every hook gets one pass against the question: would a person actually say this here** | [ours] | Grammatically perfect and idiomatically dead is the standard failure of a translated ad. |

---

## Confidence ceilings

| Situation | Ceiling |
|---|---|
| Anything derived only from a public ad library | `low`, and labelled `hypothesis` |
| Variants co-existing in one ad set, not split-tested | `medium`, whatever the volume — delivery allocates by predicted performance, so the arms are not randomly assigned |
| Below `test.volume_floor` | `low` |
| Automatic creative enhancements unknown or changed mid-window | `low` |
| A real platform split test above `test.volume_floor`, one changed element | `high` |
