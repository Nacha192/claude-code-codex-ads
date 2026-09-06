# Campaign memory and learning

Use a project-local `.ads-brain/` directory only when persistence helps the user. It is private operational data and should be ignored by Git. Do not write campaign facts back into an installed public skill.

The canonical record layout and update rules are in [the integrated second brain](second-brain.md). Use that schema and the included initializer; do not create a second competing memory layout.

Before a new campaign, retrieve only relevant facts and past tests. Expire stale prices, promos, provider limits and product assertions. Resolve contradictory facts before generating. Cross-client reuse is limited to anonymous methods; never mix proof or customer data.

## Test for a business outcome

State one falsifiable hypothesis per test. Define the control, variant, audience/unit of assignment, exposure, primary outcome, guardrails, budget, minimum useful effect and stopping rule. Separate hook testing from simultaneous changes in offer, landing page and audience unless testing the complete bundle deliberately.

For lead generation, define a qualified lead, deduplication, response time, appointment/show rate and downstream sale where available. Cheap form fills can be poor business. For ecommerce, distinguish revenue ROAS from contribution after goods, fulfillment, returns and acquisition costs. Use advertiser-provided data with common timezones, currency, attribution windows and conversion lag.

Do not label a winner from a handful of clicks or uncontrolled before/after results. At low volume, report directional evidence and what additional information would change the decision. Avoid universal spend or sample thresholds. When statistical design matters, calculate using the actual baseline and assumptions. Separate simultaneous platform auction effects from causal conclusions.

Record losing hypotheses too: what failed, plausible confounders, what to retain and what to change next. A model review score and a long-running competitor ad are not results. Revisit creative fatigue with actual delivery/performance trends, not asset age alone.
