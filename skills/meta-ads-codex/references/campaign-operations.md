# Campaign plans, launch and recovery

This is an operating procedure, not an installed Meta connector. Inspect actual tools and account permissions. If the peer has access, use the team handoff; if neither has access, deliver an import-ready plan and clearly identify the unavailable execution step.

## Reviewable launch manifest

Capture objective, conversion/lead definition, account/Page/Instagram identity, destination, authorized placements, audience boundaries, special categories if applicable, budget/currency and units, total commitment, timezone/start/end dates, tracking event, attribution assumptions, creative IDs/versions, URLs/UTMs and authorizing user message. Check current provider schemas and Meta requirements. Never copy a connector-specific enum or "always activate this way" rule into a different API.

Verify the offer on the landing page, working forms/checkout, appropriate tracking/consent configuration and relevant category restrictions. The absence of explicit health words does not neutralize an implied health claim. Review personal-attribute phrasing, guarantees, comparisons and before/after imagery in their full context using current policy. Do not repeat obsolete universal rules such as a blanket 20% image-text limit. Distinguish platform recommendations from hard input limits.

Prepare the exact preview and budget arithmetic before seeking any missing launch approval. A previous explicit approval for these exact actions is sufficient; do not invent an additional permission ceremony. Prefer PAUSED remote drafts when creation is authorized but activation is not. Even paused remote creation is an external write. Activation requires covered account, assets, budget and schedule. Verify effective status of campaign, ad sets and ads after the action rather than assuming parent activation propagated.

## Single executor and durable intent

Assign one executor per account/campaign scope through the existing Agent Duet workboard. Other agents propose and review. Record an operation ID, artifact version/hash, authorization reference, provider/account, exact intended change and status before the call. Persist request/job IDs and returned remote IDs immediately. The bus is not a transaction coordinator for Meta.

Use provider-supported idempotency keys when available. A name suffix or tag is a reconciliation aid, not a guarantee of uniqueness. After a timeout or crash, read the remote state/job first. Adopt a confirmed matching object rather than recreating it. A negative search may be stale, incomplete or unsearchable; it does not by itself prove retry safety. Retry only when provider semantics establish that the first operation was not committed or safely deduplicate it. Otherwise mark `uncertain` and stop that mutation for explicit resolution.

Do not promise exactly-once remote effects. Do not replay the entire creation chain because the last step failed. Resume from verified IDs, and request only the missing step. Never delete unrelated objects to recover from a partial run. Any compensating edit/delete must itself be in scope.

## Credits and budgets

Keep media costs and ad spend in separate ledgers. Verify whether each tool uses currency units, minor units or credits; convert with the actual currency/provider rules, not an assumption that every currency has cents. Reserve for in-flight jobs before allowing further generation. Unknown cost must be bounded by a provider estimate/ceiling or a user-approved small pilot; "do your best" is not unlimited spend.

On credits exhaustion, stop new generation. Explain completed assets, remaining work and options. For Higgsfield specifically, offer the user switching to another legitimately owned funded account if they have one. Account changes require identity/scope revalidation and cannot be used to bypass trials, restrictions or quotas.

Finish with remote IDs, observed status, actual actions, spend settings, schedule and unresolved issues. A plan is not live. A skill cannot guarantee rejection-free delivery or remove every future bug in one review.
