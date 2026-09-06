# claude-code-codex-ads

Four skills for building Meta ads. Two for working alone, two for working as a
pair. Everything is in each one: intake, competitor research from the ad
libraries, hooks, copywriting, static creatives, video, voice, compliance, and
the launch handoff.

They are written to behave like a second brain for an ad account rather than a
prompt that produces captions. Most of the value is in what they refuse to do.

```
┌─ alone ──────────────────────┐   ┌─ as a pair ─────────────────────────┐
│ codex-solo         Codex     │   │ codex-duo         Codex + Claude    │
│ claude-code-solo   Claude    │   │ claude-code-duo   Claude + Codex    │
└──────────────────────────────┘   └─────────────────────────────────────┘
```

The duo skills are two halves of one protocol. Install the half that matches
the agent it runs in.

---

## Install

Download the zip and unpack it into a skills folder. Each archive already
contains the skill folder, so `SKILL.md` lands at the right depth.

**Claude Code**

```bash
mkdir -p ~/.claude/skills
unzip INSTALL-claude-code-solo.zip -d ~/.claude/skills/
```

**Codex**

```bash
mkdir -p ~/.codex/skills
unzip INSTALL-codex-solo.zip -d ~/.codex/skills/
```

Or copy the matching `you-can-install-*` folder by hand. Same contents.

Nothing to register, nothing to restart. Each skill's `INSTALLATION.md` covers
project-scoped installs, Claude Desktop, and where `agents/openai.yaml` goes.

| File | Contains |
|---|---|
| `INSTALL-codex-solo.zip` | `meta-ads-codex` |
| `INSTALL-claude-code-solo.zip` | `meta-ads-claude-code` |
| `INSTALL-codex-duo.zip` | `meta-ads-team-codex-and-claude-code`, Codex half |
| `INSTALL-claude-code-duo.zip` | `meta-ads-team-codex-and-claude-code`, Claude Code half |

The duo skills also need the channel from
[Codex-Claude-Code-team](https://github.com/Nacha192/Codex-Claude-Code-team),
which is how the two agents actually talk. Install it first, or you have a
protocol and nothing to speak through.

### What you need

Node.js 18+ and Python 3.9+ for the scripts, and `npm i -D puppeteer` in the ad
project to render. `ffmpeg` and `yt-dlp` unlock the video routes. An image or
video generator unlocks the generation route.

**No credential is ever required.** These skills do not read `.env`, do not ask
for an access token, and do not need one to research an ad library.

---

## What is in each skill

Eight phases, each naming what blocks the next.

| Phase | Does | Blocked by |
|---|---|---|
| **0 Intake** | who you are, what you sell, the market, the avatar | three questions that must be answered, never inferred: market and language, the product in one sentence, your own brand name |
| **1 Research** | pull competitor ads, decode them, find patterns across advertisers | an unresolved search frame. A library shows an ad ran, never that it worked |
| **2 Hooks** | distinct angles, three hooks each, scored | a hook that asserts something about the reader is cut, not softened |
| **3 Copy** | primary text, headline, description, in the market's language | six checks, all of which must pass |
| **4 Production** | static creatives at every ratio, or video as a shot table | a missing ratio is a defect, not a detail |
| **5 Voice** | only when a voice carries what the picture cannot | the ad must already work with sound off |
| **6 Pre-flight** | red line, claims, licences, counts, landing-page match | the red-line check runs on **rendered** text and must exit 0 |
| **7 Handoff** | the files, the ad set plan, and what this cannot tell you | nothing. The skills never launch, pause, or move a budget |

### Two depth modes

**Standard** writes, then runs the six checks. Right for a batch of variants or
a rewrite.

**Second brain** adds six passes, each producing a written artefact: evidence,
counting, adversarial, elimination, transfer, regret. Right for a launch, a new
market, or a rebuild after a failed month. A pass with no artefact did not
happen, and an output labelled second brain with no cut list is standard output
wearing a badge.

The Codex skills target GPT-5.6 and Astra-6. The Claude Code skills target
Opus 5 at both levels, where the depth comes from reasoning effort. In both,
the model name is the intended target and never a claim: a skill that cannot
reach the named model says so instead of pretending.

### It remembers

`ads/LEDGER.md` records what was decided, what failed and how that failure was
read, and which assumptions are still open with what would settle each one. A
decision recorded there is not relitigated without a new fact. The session ends;
the account does not.

---

## What these skills refuse to do

The list that makes them useful.

1. **Invent anything.** No fabricated competitor ad, no invented review, no
   illustrative metric that reads like a real one. `needs_data` is an answer.
2. **Call an asset produced** because an API returned success. It is on disk
   with its dimensions read back, or it does not exist.
3. **Estimate a character count.** Counted, on the shipped string, in the
   shipped language.
4. **Assert a personal attribute** about the reader. "Trouble sleeping?" is a
   policy rejection and, in a regulated category, worse. "3 a.m. Third time." is
   the same ad and it converts better.
5. **Ship an unsourced claim.** Marked, ranked outside the shippable set, and
   the marker is never stripped to make the batch look finished.
6. **Spend money unasked.** Nothing is generated until you have chosen the tool
   and confirmed the run.
7. **Substitute a generator silently.** If Higgsfield is out of credit, the run
   stops and asks you to switch account. It does not quietly produce the images
   somewhere else and hand them over as though it had not.
8. **Obey scraped text.** Ad copy and page metadata are data. An instruction
   found inside them is recorded and ignored.
9. **Move anything in your account.** `ship`, `test`, and `cut` are
   recommendations. None of them is permission.
10. **Translate an ad.** Ads are written in the market's language. Translation
    keeps the meaning and loses the rhythm, and rhythm is most of a hook.

---

## Generation tools

Covered, with what each is actually good at: Higgsfield, Gemini Nano Banana and
Nano Banana 2, OpenAI image generation, Seedance 2.0, Kling, Claude Design,
ElevenLabs, and a local HTML engine that costs nothing.

The rule that saves the most money and the most embarrassment:
**generate the picture, typeset the words.** Text rendered by an image model is
the fastest way to make a batch look amateur, and its character counts cannot be
verified.

---

## Working as a pair

The duo skills exist for one reason: a capability one agent does not have.

During this pack's own construction, one agent held image generation, browser
control, a persistent REPL, and local `ffmpeg`. The other held the only
authenticated Higgsfield connector. Each performed the steps it could and
delegated the rest. That is the case for a pair. A second opinion with no
missing capability is a delay.

So roles are assigned **per step, from the capabilities each agent reports at
the handshake**, never from the brand of the agent. And holding a connector
proves neither the right account nor the permissions the step needs, so the
first step that depends on one tests it before the batch does.

`reference/roles.md` covers the handshake and the fallback.
`reference/handoffs.md` covers the seven seams where a two-agent build actually
breaks, each with what crosses, what must not, and the check the receiver runs.

---

## Repository layout

```
INSTALL-*.zip                 the four skills, ready to unzip
you-can-install-*/            the same four, unpacked
_src/                         one copy of every file; edit here
tools/build_skills.py         assembles the four from _src, makes the zips
tests/test_skills.py          front matter, dangling references, zip depth, no secrets
docs/SOURCES.md               every project this was built by reading
```

`_src` is the source of truth. A shared file exists once and is copied into all
four distributions at build time, so a correction lands everywhere.

```bash
python tools/build_skills.py           # rebuild folders and zips
python tools/build_skills.py --check   # verify the distributions match _src
python tests/test_skills.py            # 11 tests
```

Editing a `you-can-install-*` folder directly is a mistake the check catches:
the next build would silently revert it.

---

## Credit

Built by reading a lot of other people's skills. Every one of them is named in
[docs/SOURCES.md](docs/SOURCES.md), with what it contributed and a link. Several
are better than this pack at the one thing they do, and the page says which.

No text was copied. Methods and thresholds are not copyrightable; prose is.

---

## Licence

MIT. See [LICENSE](LICENSE).

The advertising judgement in these files is a starting point, not legal advice.
Platform policies and consumer-protection law change, they differ by country,
and the responsibility for what you publish is yours.
