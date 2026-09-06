# Installing `meta-ads-claude-code` for Claude Code

A skill is a **folder** containing a `SKILL.md` whose front matter carries a
`name` and a `description`. Nothing to register, nothing to restart.

## Where it goes

| Location | Scope |
|---|---|
| `<project>/.claude/skills/meta-ads-claude-code/` | this project only |
| `~/.claude/skills/meta-ads-claude-code/` | every project on this machine |

Unzip `INSTALL-claude-code-solo.zip` into one of them. The archive contains the folder,
so `meta-ads-claude-code/SKILL.md` ends up at the right depth.

```bash
mkdir -p ~/.claude/skills
unzip INSTALL-claude-code-solo.zip -d ~/.claude/skills/
```

The skill appears in the available-skills list in the next session, and loads
when a task matches its `description` or when you invoke it by name.

## Claude Desktop and claude.ai

Settings → Capabilities → Skills accepts the **same ZIP**. The archive already
has the folder at its root, which is what the interface expects.

**A caveat worth knowing:** the production route in this skill runs a headless
browser and a Python check on your machine. Claude Desktop may have neither.
The method, the references, and the copywriting work read perfectly there; the
render and the red-line check need a terminal.

## What you need installed

Required for the full pipeline. The skill degrades honestly without them: it
says which step it cannot run rather than routing around it.

| Tool | Needed for | Install |
|---|---|---|
| **Node.js 18+** | the ad library URL builder, the render script, the red-line harness | nodejs.org |
| **Python 3.9+** | `redline_check.py` | python.org |
| **puppeteer** | rendering the HTML engine to PNG | `npm i -D puppeteer` in the ad project |

Optional, and each unlocks one route rather than the whole pack:

| Tool | Unlocks |
|---|---|
| `ffmpeg` / `ffprobe` | video verification, frame extraction, duration read-back |
| `yt-dlp` | downloading a public ad video for storyboard analysis |
| An image or video generator, via MCP | the generation route in `reference/generation-tools.md` |
| A browser, or a second agent that has one | loading ad library pages, which lazy-load and need scrolling |

**None of these is a credential.** This skill never reads `.env`, never asks for
an access token, and needs neither to do its research.

## Checking it is visible

Ask for the skills list, or type the skill name as a slash command. If it does
not appear, the usual cause is a missing `name:` in the front matter, or
`SKILL.md` sitting one level too deep.

## Which of the four you want

| You are | Install |
|---|---|
| Claude Code, working alone | `claude-code-solo` |
| Claude Code, working with Codex | `claude-code-duo`, plus the `duo-claude-codex` channel skill |
| Codex, alone | `codex-solo` |
| Codex, with Claude Code | `codex-duo`, plus the channel skill |

The duo skills need the channel from
[Codex-Claude-Code-team](https://github.com/Nacha192/Codex-Claude-Code-team).
Install that first, or the two agents have a protocol and nothing to speak
through.
