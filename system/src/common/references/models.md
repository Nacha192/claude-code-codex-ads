# Basic and advanced work modes

These are workflow profiles, not measured advertising benchmarks. Model availability is per host and account. Keep the user's chosen model; do not silently replace or impersonate one. Model names do not grant tools. Changing a Markdown instruction does not switch the running model.

## The mode is a choice, not a model tier

Basic and advanced describe how much work the assistant does, not which model is allowed to do it. Any model the host actually exposes can run either mode. A more capable model explores more inside a pass and writes a sharper artifact; it does not unlock the pass. Refusing the advanced mode because the smaller model is loaded would be an invented restriction.

| Mode | Operating pattern | Where the model matters |
|---|---|---|
| Basic | Compact brief, bounded relevant research, three distinct concepts, one critique and revision cycle, requested exports and the evidence behind them. | Little. This is a short path and any current model completes it. |
| Advanced | The five passes below, each producing a written artifact. | Inside the passes. Stronger reasoning finds better competing explanations and harder objections; the required artifacts are identical either way. |

Hosts expose different models. The Codex host used for this build lists `gpt-5.6-sol` and `gpt-6-astra`; Claude Code exposes its current model and `claude-opus-5`. Pick by what is actually available and by the user's usage budget, then pick the mode by what the task needs. Where the host offers a reasoning-effort setting, raise it for the advanced mode rather than switching model, and do not copy API effort values blindly into a CLI.

[OpenAI's model comparison](https://developers.openai.com/api/docs/models/compare) and [Anthropic's Opus 5 documentation](https://platform.claude.com/docs/en/models/opus-5/whats-new-opus-5) are the current references; verify access and supported settings on the target host.

## Advanced adds decisions, not verbosity

1. Write competing hypotheses about the buyer's friction and identify evidence that would distinguish them.
2. Build concept routes that differ in their persuasive argument and visual logic. Compare what each teaches, costs and risks; do not generate 50 interchangeable hooks by default.
3. Use a skeptical review against product facts and the destination. Record the strongest objection and a concrete repair, not an invented panel of experts.
4. Prototype the uncertain element cheaply, within approval scope. Spend on full production only after the direction is coherent.
5. Inspect finished exports and define a business test. Preserve useful learning for the next campaign.

A pass that produced no written artifact did not happen, whichever model ran it. Say which model and mode actually ran, and never claim a pass that was skipped.

Basic retains truthfulness, consent, generation approval, account boundaries and actual export QA. Advanced does not remove these requirements or promise human thought, better CPA, or a quality multiplier. Respect the user's time and usage budget; use retrieval and selective modules instead of loading the entire library.
