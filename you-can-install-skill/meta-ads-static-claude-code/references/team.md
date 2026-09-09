# Codex and Claude Code advertising team

Reuse [Agent Duet](https://github.com/Nacha192/Codex-Claude-Code-team), the existing communication bridge. Read the installed bridge's `SKILL.md`, protocol and command reference before use. Do not invent a transport, scrape global conversation histories or pretend that ZIP installation wakes another agent.

## Handshake

Choose one task-local bus path and one authorized goal. Each actual participant reports runtime/model as observed, tools/read/write/media/account access, limitations, relevant context, proposed contribution and exact workspace. Pick two active workers when both sessions can operate on the bus, otherwise a coordinator with fresh genuine consultations. If disconnected, say so and provide a scoped handoff that the user can relay.

Agree on roles by current evidence: research owner, concept/copy owner, production owner, reviewer and one campaign executor. One agent may hold several roles; do not assign them by presumed intrinsic superiority. Claims protect disjoint output paths, while both may discuss schema decisions. The author cannot accept its own work. A consultant sees only the supplied artifact and cannot attest to unseen assets or tools.

## Shared contract

Include `schema_v`, `core_v`, task ID, artifact version/hash, inputs/sources, output paths, acceptance criteria, dependencies and next action. Record authorization by reference to the real user's message and scope, not a fabricated approval object. Private facts and keys stay outside public artifacts and the bus whenever unnecessary.

Core-version divergence prompts comparison of the applicable rules. Incompatible schema major versions block machine consumption until reconciled; minor changes require checking required fields, not an automatic rejection of useful work. The shared contract in each pack is copied from the same canonical source and checked by the build validator.

Example handoff:

```json
{"schema_v":"1.0.0","core_v":"1.0.0","task_id":"creative-review-01","artifact":"campaign/creative-set.json","artifact_version":"3","sha256":"actual-artifact-hash","request":"Review buyer fit, evidence and spoken phrasing; return concrete repairs","authorization_ref":"user-approved research and draft scope","next":"Return review of this exact version; no generation or account edits"}
```

This is a template, not a real approval or hash. Fill it from observed state.

## The blind pass, before any role is assigned

The default failure of two assistants working together is not conflict, it is
agreement. One writes the diagnosis, the other reviews it, and the review is
already anchored on the first one's framing. You get one opinion, checked. Two
assistants that never disagree cost twice as much as one and are worth less,
because the second one's independence was spent reading the first one's answer.

So the first exchange is not a handoff. Both sides do the same work, alone,
before seeing anything from the other.

**Each side writes, without consulting the peer:**

1. The buyer's problem in one sentence, in the buyer's words.
2. The single obstacle that stops the purchase.
3. Three concepts, each with its angle, its mechanism and the proof it needs.
4. What it expects to be wrong about.

**Then both are put on the bus at the same time**, and only then are they read.
Sending yours after reading theirs is not a blind pass, and it is the one rule
here that is easy to break by accident. If the bus does not support it, exchange
the hashes first and the contents second.

**Then the synthesis is written, once, by whoever holds the integrator role**,
and it is a document, not a conversation:

| Section | What goes in it |
|---|---|
| Agreed | What both reached independently. This is the strongest thing you have, because nobody talked the other into it. |
| Disagreed | Both positions stated in their own terms, not summarised by the opponent. |
| Counter-case | For each disagreement, the case that would make the other side right. Written by the side that disagrees with it. |
| Missing evidence | What neither side knows, and which of the two positions it would settle. |
| Discriminating test | The cheapest experiment whose result changes the decision, with the outcome that kills each position. |

An unresolved disagreement is a normal output. Record it and run the test. What
is not acceptable is an unnoticed disagreement, or a disagreement dissolved by
whoever wrote last.

**Do the blind pass again** whenever the brief changes materially: a new offer,
a new market, a register reversal. Do not do it for a variant of work already
agreed on, where it is pure cost.

## Work loop

1. Run the blind pass above, then agree on the brief, facts and output contract before parallel edits. Use the bridge workboard and claims. Roles are assigned after the synthesis, not before, so that neither side's independent view was shaped by the role it was handed.
2. Owners produce independent artifacts. Send decisions/evidence, not hidden reasoning or filler chatter. Read and acknowledge actual messages at boundaries.
3. Reviewer identifies exact version, observable issue, evidence and repair. Strategic disagreements are resolved by evidence or a reversible experiment, not vote count.
4. Integrator applies accepted repairs and reruns affected checks. If reviewed files change materially, review the new version.
5. Executor follows campaign-operations for authorized external writes, and reports verified remote state. Tool access may be handed off; permission may not be bypassed.

Three fallbacks make the team worth more than either half. Use them explicitly, and say which one you are using. They are what to do when the two sides differ in capability, understanding or context; the blind pass above is what to do when they do not, and it is the more common case.

**Capability.** If a peer lacks a tool the other holds, hand off the approved brief, the exact inputs, the account/provider scope and the remaining ceiling. The receiving agent verifies tool and account state before calling. Do not re-generate an already completed job because an acknowledgement was lost. This is the common case here: one side may have a video provider and the other none.

**Comprehension.** If one peer has understood an instruction the other has not, the one who understood rewrites it as a clearer prompt and sends that, rather than repeating the original politely. Name the ambiguity that was resolved, so the misreading does not come back on the next task. Restating the same sentence louder is not a handoff.

**Context.** If one peer holds context the other lacks, brand, market, register, what was already rejected and why, it sends the context, not a conclusion drawn from it. If neither holds it, do not guess: ask the user, in one compact batch, and put the answer in the brief where both can read it.

Wait only while a real peer/job is active. After repeated timeouts, inspect the observed blocker and continue independent work; never launch duplicate peers or poll indefinitely. Do not kill unrelated sessions. Close the bridge only under its protocol, with actual completed reviews and outstanding messages acknowledged. Report limits honestly; collaboration does not guarantee a fourfold improvement.
