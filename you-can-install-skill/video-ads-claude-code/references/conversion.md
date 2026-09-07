# Converting skills between Codex and Claude Code

This pack supplies original functional adaptations of selected public skill ideas, not a verbatim merger, full translation of every upstream file, or redistribution of their tools. Each source card records what transfers and the two host-specific routes. Read only the relevant card.

## Conversion contract

Preserve the upstream task's useful inputs, output contract, decision points and evidence checks. Rewrite execution around the target host's actual capabilities. Resolve dependencies or supply a clearly stated manual fallback. Never merely replace "Claude" with "Codex" in a file and call it tested.

| Concern | Codex target | Claude Code target |
|---|---|---|
| Discovery | `SKILL.md` with name/description; project `.agents/skills`, or a configured user skill directory | `SKILL.md`; project/personal `.claude/skills` |
| Context | Inspect declared project context and user-authorized source files; do not assume `.claude/` exists | Inspect declared project context; do not assume Codex app tools or private `.codex/` files exist |
| Tool calls | Discover actual host tools/connectors; replace Bash-only examples with host-appropriate calls | Discover built-in tools/MCP; map Codex tool concepts to actual available tools |
| Permissions | Respect host approval and existing user authorization; never import a permissions bypass | Same; an `allowed-tools` field is not user permission to spend or publish |
| Subagents | Use only actual authorized delegation; no Claude impersonation | Use actual Claude agents or a real Codex bridge; no simulated peer approval |
| Paths | Resolve relative references from the installed skill; use workspace intermediates/output conventions | Resolve from the installed skill and the selected project; no developer-specific paths |
| Commands | Validate local help, arguments, OS quoting and dependencies | Validate the same; never carry unsupported Codex UI commands into Claude |
| Artifacts | Use portable JSON/Markdown and real files, with source versions and QA status | Same contract; host-specific presentation should not change campaign facts |
| Model choice | Select an available Codex model through the host, if authorized | Select an available Claude model; Sol/Astra requires a real Codex peer |

## Intentionally not carried over

Do not inherit hard-coded vendor credentials, automatic paid tool installation, platform specs without a date, mandatory huge batches, "winning" claims without data, provider-specific budget units, rigid stylistic scoring or imported blanket permission rules unrelated to the task. Anthropic brand styling is not a general advertiser brand kit. Reference-source model names and third-party CLI IDs are not universal APIs.

## Compatibility evidence

This release validates package structure, references, offline scripts, installation and representative behavior. It does not claim live generation through every provider, a complete audit of upstream scripts or live Meta campaign testing. For a new runtime/provider pair, run a research-only task first, a scoped local draft second, then a small explicitly approved production pilot. Preserve actual failure evidence and update only the relevant adapter.
