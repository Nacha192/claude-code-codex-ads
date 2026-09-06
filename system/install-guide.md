# Install the four all-in-one advertising skills

Choose the edition for the assistant where you start. Every edition already contains research, hooks, copywriting, static/video/voice workflows and the integrated second brain. You do not install the internal modules separately.

| Start in | Solo | Real two-assistant team |
|---|---|---|
| Codex | `meta-ads-codex` | `meta-ads-team-codex-and-claude-code` |
| Claude Code | `meta-ads-claude-code` | `meta-ads-team-claude-code-and-codex` |

## Repository installer (Python 3.10+)

Download the repository or clone it. From its directory:

```sh
python install.py --runtime codex
python install.py --runtime codex --apply
python install.py --runtime claude --apply
```

The first command previews only. The next two install the two editions for each host. Use `--mode solo` or `--mode team` to select one. The installer is offline, verifies copied hashes, accepts an identical repeat, and refuses to overwrite a different installed skill. It does not install provider tools, change global settings, purchase anything or connect accounts.

Default user locations: Codex `~/.agents/skills`; Claude Code `~/.claude/skills`. For a project use `--project /path/to/project` (Codex `.agents/skills`, Claude `.claude/skills`). For an existing host with a different configured skill directory, use `--target-root /exact/skills/directory`. Do not install the same named skill in multiple discovery locations unintentionally. Reload/restart skill discovery afterward. A symlinked installation target itself is refused; if your dotfile manager uses one, pass its resolved real directory with `--target-root`. Legitimate symlinked ancestors are resolved.

## ZIP installation without Python

Download one of the four `install-*.zip` archives at the repository root archives and extract its named folder into the appropriate skill directory. Keep `SKILL.md`, `references/`, `modules/`, `scripts/` and notices together. The root `SHA256SUMS` file provides archive checksums. ZIPs are skill folders, not browser extensions or provider accounts.

## Team prerequisite

For genuine two-CLI work, install/configure the existing [Agent Duet bridge](https://github.com/Nacha192/Codex-Claude-Code-team) for the runtimes you use, and authenticate both CLIs through their normal interfaces. Read the bridge's own installation/protocol documentation. The team skill then negotiates one real task-local bus and roles. It does not connect an offline peer merely because a ZIP was uploaded.

The advertising system is complete inside each pack; the bridge is a communication capability. Where only a fresh consultant is available, the team must disclose that topology. Solo editions do not auto-launch the other assistant.

## First use

Ask in your own language: "Use meta-ads-codex for this product. Research the market and propose hooks first; ask before generating media." For the team, name the matching team skill and request joint work. Provide a product URL or concise description, market and target ad language if they are not already known. The skill collects remaining essentials.

The integrated second brain can initialize private project records with its included `scripts/init_brain.py`. Its method is already part of the skill; only your business records are stored privately in `.ads-brain/`.

Official discovery references: [Codex skills](https://developers.openai.com/codex/skills), [Claude Code skills](https://code.claude.com/docs/en/skills). Verify locations if your host changes.
