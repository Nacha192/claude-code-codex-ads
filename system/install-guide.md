# Install the eight all-in-one advertising skills

Choose what you are making, then the assistant where you start. Every edition already contains research, hooks, copywriting, its own craft workflow and the integrated second brain. You do not install the internal modules separately.

**Still creative, images and carousels:**

| Start in | Solo | Real two-assistant team |
|---|---|---|
| Codex | `meta-ads-static-codex` | `meta-ads-static-team-codex-and-claude-code` |
| Claude Code | `meta-ads-static-claude-code` | `meta-ads-static-team-claude-code-and-codex` |

**Video:**

| Start in | Solo | Real two-assistant team |
|---|---|---|
| Codex | `video-ads-codex` | `video-ads-codex-claude-code` |
| Claude Code | `video-ads-claude-code` | `video-ads-claude-code-codex` |

Installing both halves for one runtime is normal and they do not conflict: each says in its `references/scope.md` what it builds, and the assistant picks by what you asked for.

## Repository installer (Python 3.10+)

Download the repository or clone it. From its directory:

```sh
python system/install.py --runtime codex
python system/install.py --runtime codex --apply
python system/install.py --runtime claude --scope motion --apply
```

The first command previews only. The second installs the four editions for Codex, both halves. Use `--scope static` or `--scope motion` for one craft, and `--mode solo` or `--mode team` for one edition; combine them to install exactly one pack. The installer is offline, verifies copied hashes, accepts an identical repeat, and refuses to overwrite a different installed skill. It does not install provider tools, change global settings, purchase anything or connect accounts.

Default user locations: Codex `~/.agents/skills`; Claude Code `~/.claude/skills`. For a project use `--project /path/to/project` (Codex `.agents/skills`, Claude `.claude/skills`). For an existing host with a different configured skill directory, use `--target-root /exact/skills/directory`. Do not install the same named skill in multiple discovery locations unintentionally. Reload or restart skill discovery afterward. A symlinked installation target itself is refused; if your dotfile manager uses one, pass its resolved real directory with `--target-root`. Legitimate symlinked ancestors are resolved.

## ZIP installation without Python

Download one of the eight `install-*.zip` archives at the repository root and extract its named folder into the appropriate skill directory. Keep `SKILL.md`, `references/`, `modules/`, `scripts/` and the notices together. The root `SHA256SUMS` file provides checksums for all eight archives. ZIPs are skill folders, not browser extensions or provider accounts.

This route installs the pack without needing Python, but the included checks still need it. On its first task in a project the skill verifies the interpreter, and if none is there it says what stops working and asks before installing anything. See `references/runtime.md` inside the pack.

## What the skill still needs from you

The pack contains the method. It does not contain a video model, a speech provider, a renderer or an ad account, and it does not pretend to.

| Capability | Without it |
|---|---|
| A connected image provider | No generated stills in the static packs. Layout, copy and composition direction still work. |
| A connected video provider | No generated footage. Direction, prompts and storyboard still work. |
| A connected speech provider | No narration and no voice cloning. The voice card and script still work. |
| Remotion or FFmpeg | No assembly, no captions burned in, and none of the measurable audio checks. |
| An authorized Meta account | No campaign operations. The full campaign artifact is still produced. |

The pack detects each of these before promising a deliverable, and names the missing one instead of quietly producing less.

## Team prerequisite

For genuine two-CLI work, install and configure the existing [Agent Duet bridge](https://github.com/Nacha192/Codex-Claude-Code-team) for the runtimes you use, and authenticate both CLIs through their normal interfaces. Read the bridge's own installation and protocol documentation. The team skill then negotiates one real task-local bus and roles. It does not connect an offline peer merely because a ZIP was uploaded.

The team edition is worth most when the two sides differ: one has a video provider and the other does not, one understood an instruction the other misread, one holds context the other lacks. Those three fallbacks are the point of it.

## First use

Ask in your own language: "Use meta-ads-static-codex for this product", or "Use video-ads-codex for this product. Study what is running first, propose hooks, and ask before generating anything." For the team, name the matching team skill and request joint work. Provide a product URL or a concise description, the market and the target ad language if they are not already known. The skill collects the remaining essentials, and it will ask one blocking question about register: serious, native, cinematic, documentary or deliberately unpolished. Answer it, because creative in the wrong register cannot be published.

The integrated second brain can initialize private project records with its included `scripts/init_brain.py`. Its method is already part of the skill; only your business records are stored privately in `.ads-brain/`.

Official discovery references: [Codex skills](https://developers.openai.com/codex/skills), [Claude Code skills](https://code.claude.com/docs/en/skills). Verify locations if your host changes.
