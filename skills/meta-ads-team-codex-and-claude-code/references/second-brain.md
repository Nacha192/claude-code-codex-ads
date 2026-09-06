# Integrated advertising second brain

This system is INSIDE every skill: its reasoning method, schemas, templates, retrieval and learning procedure ship with the pack. It is not a fifth skill or optional add-on. Private records are created for each business in its own project; the public skill contains no preloaded personal information.

## Think in connected decisions

Before creating an ad, connect five things: the buyer's situation, the evidence for that situation, the offer's relevant truth, the creative argument, and what outcome would test it. A new task should start from useful prior lessons and unresolved contradictions, not from a fresh generic persona. The system is an AI working method; it does not claim consciousness or guaranteed performance multipliers.

Use this chain as an internal decision record:

`source → buyer friction → hypothesis → concept → asset version → experiment → qualified outcome → lesson`

For the most consequential assumption, write a concise counter-case and the observation that could change the decision. Do not expose private chain-of-thought or generate pages of artificial debate. If the evidence is weak, label the hypothesis and choose a small informative test. Do not invent customer quotations to complete the chain.

## Included memory structure

Resolve scripts relative to this installed skill directory, not the project working directory. Use `scripts/init_brain.py` for a preview, then apply it to the selected project when persistence is appropriate. It creates the following private skeleton without overwriting an existing brain:

```text
.ads-brain/
  .gitignore
  index.md
  brand.json
  buyers.json
  evidence.jsonl
  research.jsonl
  hypotheses.jsonl
  creatives.jsonl
  experiments.jsonl
  decisions.jsonl
  contradictions.jsonl
  operations.jsonl
  lessons.md
```

Before recording private business data, add `.ads-brain/` to the project's ignore rules and verify coverage. Check again before publication. The initializer includes an internal `.gitignore` containing `*`; it does not modify the project's Git configuration or parent ignore file. Verify coverage: ignore rules do not remove already tracked files or prevent an explicit force-add. If files already exist, read and update only relevant records; never reset the brain to a template. Keep each business/client in a separate root. For a quick one-off task, apply the same reasoning inline without pretending durable storage exists.

Every JSONL record includes `schema_v`, a stable `id`, `recorded_at`, `source_refs` and `status`. Append changes using `supersedes` rather than silently rewriting evidence. Record deletion/redaction requests without retaining the deleted private content. The bridge workboard governs tasks and edit claims; this memory governs marketing facts and decisions. They are not competing transports.

## Record contracts

| Record | Required decision-bearing content |
|---|---|
| Brand | Actual offer/category, country, ad language/register, product truths, constraints, asset references, unknowns and updated date |
| Buyer | Buying trigger, workaround, tension, awareness hypothesis, objections, sourced vocabulary, decision criteria and legitimate poor-fit cases |
| Evidence | Exact proposition supported, source type/URL or private file reference, observed date, scope, limitations, review trigger and confidence |
| Research | Query, filters, date semantics, capture, ad/Page IDs, observed creative pattern and coverage gaps |
| Hypothesis | Buyer/offer relationship, supporting and contrary evidence IDs, prediction, falsification, status and linked creative IDs |
| Creative | Parent ID, exact mutation, argument, hook, format, source assets, proof IDs, version/hash, provider actually used, approval reference and QA state |
| Experiment | Control/treatment, primary business outcome, diagnostic metrics, assignment/attribution assumptions, window, spend, source data, confounds and conclusion |
| Decision | Choice, brief rationale, alternatives, evidence, owner and conditions that would reverse it |
| Contradiction | Conflicting propositions/sources, affected claims/assets, proposed resolution, status and resolution evidence |
| Operation | Exact authorized remote change, account alias, approval reference, request/object IDs, state and reconciliation evidence; no credentials |

Evidence source types are `user_stated`, `product_observed`, `customer_quote`, `measurement`, `public_observation`, `derived` and `hypothesis`. These describe provenance, not an automatic hierarchy of truth. Reading a health claim on a website does not validate efficacy. A user statement reliably establishes their intent but may still need evidence for an objective advertising claim. A measurement requires its definition and context; a derived number needs the inputs and calculation. Confidence never turns a hypothesis into proof.

## Retrieve selectively

1. Identify the business/project; inspect the index and relevant brand/buyer fields.
2. Retrieve only lessons, hypotheses and contradictory/stale facts relevant to this niche, offer, language and format. Follow evidence IDs when needed.
3. State a short working brief with the important knowns and gaps. Reuse confirmed answers; do not ask confirmation merely because a fact was stored.
4. If a critical fact is stale or contradictory, resolve that fact before using it in production. Continue unaffected research and drafting.

Recheck price, promotion eligibility, stock, destination, provider credits and tool schemas at the actual decision, not every fixed 30 days. Other facts may use context-appropriate review dates. Capturing a new timestamp without rereading the source is not a recheck.

## Learn without fooling yourself

Store what changed between creative versions. A higher result alone does not prove that the mutation caused it: inspect audience, spend, placement, offer, conversion lag, seasonality and attribution. Mark conclusions `supported_in_context`, `refuted_in_context` or `inconclusive`, not universally proven. CTR/watch time can diagnose a hook; qualified leads, purchases or the user's stated business outcome determine business usefulness.

Write each lesson as: `In [context], [change] was associated with [observed result], supported by [experiment/source], with [limits]. Reuse when [conditions]; reconsider if [trigger].` Preserve useful negative findings. Do not promote competitor ad longevity or model review scores into experiment results.

## Critique loop

Before production, inspect whether the opening is a worthwhile idea or a specification label; whether the visual adds meaning; whether the offer can pay off the hook; whether a buyer objection has actually been answered; and whether a qualification is truthful. Competitor substitution is a diagnostic question, not a rigid rejection rule. The destination must honor the promise, not repeat identical words mechanically.

After production, inspect the real export. Connect every defect to a repair: unreadable qualification → redesign; mispronounced brand → regenerate the approved take within scope and retime; unsupported outcome → remove or substantiate the claim. Stop when the brief is fulfilled and remaining uncertainty needs a real experiment.

In team mode, one owner commits a given memory artifact at a time under the bridge claim. Both assistants contribute evidence and critique; shared lessons require traceable review. In solo mode, use the same system without inventing a peer. Report self-review as self-review; the user is the acceptance authority for requested sign-off. This does not impose a new approval gate on ordinary authorized drafts.
