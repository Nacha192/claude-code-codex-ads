# Installing `{{SKILL_NAME}}` for Codex

A skill is a **folder** containing a `SKILL.md` whose front matter carries a
`name` and a `description`. Nothing to register, nothing to restart.

## Where it goes

| Location | Scope |
|---|---|
| `<repo>/.agents/skills/{{SKILL_NAME}}/` | this repository, and therefore the team |
| `~/.codex/skills/{{SKILL_NAME}}/` | every project on this machine |

Unzip `INSTALL-{{DIST}}.zip` into one of them. The archive contains the folder,
so `{{SKILL_NAME}}/SKILL.md` ends up at the right depth.

```bash
mkdir -p ~/.codex/skills
unzip INSTALL-{{DIST}}.zip -d ~/.codex/skills/
```

## `agents/openai.yaml` belongs inside the skill folder

```
.agents/skills/{{SKILL_NAME}}/
  SKILL.md
  agents/openai.yaml      <- here, not at the skill root
  reference/
  scripts/
```

OpenAI's own bundled skills put it there. At the root it is ignored.

## Do not put this in `AGENTS.md`

`AGENTS.md` loads for **every** task, including the ones where ads are
irrelevant, and it would cost tokens on all of them. One line is enough:

```markdown
To build Meta ads, load the {{SKILL_NAME}} skill.
```

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
| An image or video generator | the generation route in `reference/generation-tools.md` |
| A browser | loading ad library pages, which lazy-load and need scrolling |

**None of these is a credential.** This skill never reads `.env`, never asks for
an access token, and needs neither to do its research.

## Checking it is visible

Ask for the skills list, or invoke it by name. If it does not appear, the usual
cause is a missing `name:` in the front matter, or `SKILL.md` sitting one level
too deep.

## Which of the four you want

| You are | Install |
|---|---|
| Codex, working alone | `codex-solo` |
| Codex, working with Claude Code | `codex-duo`, plus the `duo-claude-codex` channel skill |
| Claude Code, alone | `claude-code-solo` |
| Claude Code, with Codex | `claude-code-duo`, plus the channel skill |

The duo skills need the channel from
[Codex-Claude-Code-team](https://github.com/Nacha192/Codex-Claude-Code-team).
Install that first, or the two agents have a protocol and nothing to speak
through.
