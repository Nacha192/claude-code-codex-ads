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

## Work loop

1. Agree on the brief, facts and output contract before parallel edits. Use the bridge workboard and claims.
2. Owners produce independent artifacts. Send decisions/evidence, not hidden reasoning or filler chatter. Read and acknowledge actual messages at boundaries.
3. Reviewer identifies exact version, observable issue, evidence and repair. Strategic disagreements are resolved by evidence or a reversible experiment, not vote count.
4. Integrator applies accepted repairs and reruns affected checks. If reviewed files change materially, review the new version.
5. Executor follows campaign-operations for authorized external writes, and reports verified remote state. Tool access may be handed off; permission may not be bypassed.

Three fallbacks make the team worth more than either half. Use them explicitly, and say which one you are using.

**Capability.** If a peer lacks a tool the other holds, hand off the approved brief, the exact inputs, the account/provider scope and the remaining ceiling. The receiving agent verifies tool and account state before calling. Do not re-generate an already completed job because an acknowledgement was lost. This is the common case here: one side may have a video provider and the other none.

**Comprehension.** If one peer has understood an instruction the other has not, the one who understood rewrites it as a clearer prompt and sends that, rather than repeating the original politely. Name the ambiguity that was resolved, so the misreading does not come back on the next task. Restating the same sentence louder is not a handoff.

**Context.** If one peer holds context the other lacks, brand, market, register, what was already rejected and why, it sends the context, not a conclusion drawn from it. If neither holds it, do not guess: ask the user, in one compact batch, and put the answer in the brief where both can read it.

Wait only while a real peer/job is active. After repeated timeouts, inspect the observed blocker and continue independent work; never launch duplicate peers or poll indefinitely. Do not kill unrelated sessions. Close the bridge only under its protocol, with actual completed reviews and outstanding messages acknowledged. Report limits honestly; collaboration does not guarantee a fourfold improvement.
