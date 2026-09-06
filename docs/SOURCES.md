# Sources

This pack was built by reading what already exists, keeping the parts that
survive contact with a real ad account, and writing the rest from production
work.

**Nothing here is copied text.** Methods, thresholds, and structural ideas are
not copyrightable; prose is. Every file in this repository is written from
scratch. This page exists so that the people whose work shaped it are named,
and so you can go and read the originals, several of which are better than this
pack at the one thing they do.

Star counts and licences were read on 6 September 2026 and will have moved.

---

## What was taken, in one paragraph

The **evidence discipline** — labelling every line as observed, inferred, or
missing, and capping confidence at what the evidence allows — comes from
`mardab96/ad-creative-claude-skills`, which does it more rigorously than
anything else published. The **hook taxonomy** owes its shape to
`rediumvex/viral-hooks-skill`. The **awareness-first workflow** is Eugene
Schwartz by way of `robpalmer99/claude-code-copywriting-skills`. The **ad
library discipline** — never invent a pull, storyboard rather than transcribe,
stop and report rather than improvise a new method — is from
`backtrue/meta-ad-library-video-scraper`. The **mute test and modality split**
are sharpened by `Splitwolf1/adlab`.

Everything about the **HTML engine**, the **workaround test**, the **red line
run on rendered text**, the **generation gate**, and the **eight phases** comes
from production work on French ecommerce accounts, not from a repository.

---

## Static ads — Claude Code

| # | Repository | ★ | Licence | Worth reading for |
|---|---|---|---|---|
| 1 | [mardab96/ad-creative-claude-skills](https://github.com/mardab96/ad-creative-claude-skills) | 1 | MIT | Sixteen narrow skills, one thresholds file, and blocking rules where one skill's answer invalidates another's. The most disciplined ad pack published. Its insistence that a range is not a threshold is the single best idea here |
| 2 | [hyperfx-ai/marketing-skills](https://github.com/hyperfx-ai/marketing-skills) | 83 | MIT | `ad-creative-generation` with separate references for brand extraction and per-platform creative specs |
| 3 | [OpenClaudia/openclaudia-skills](https://github.com/OpenClaudia/openclaudia-skills) | 678 | MIT | 34 marketing skills; `facebook-ads`, `icp-builder`, `ai-image-gen` are the relevant ones |
| 4 | [kostja94/marketing-skills](https://github.com/kostja94/marketing-skills) | 952 | MIT | 160+ skills. Worth studying for how a large pack is organised without collapsing |
| 5 | [adkit/ads-skills](https://github.com/adkit/ads-skills) | 23 | custom | Campaign structure, targeting, and budget alongside creative |
| 6 | [Maxymize/maxym-ai-ads](https://github.com/Maxymize/maxym-ai-ads) | 2 | — | One unified paid-advertising skill rather than a pack |
| 7 | [efesorjm/creative-brief](https://github.com/efesorjm/creative-brief) | 3 | — | Grades and pressure-tests briefs and hooks instead of writing them |
| 8 | [kkoppenhaver/cc-nano-banana](https://github.com/kkoppenhaver/cc-nano-banana) | 369 | — | The minimal shape of an image-generation skill |
| 9 | [kingbootoshi/nano-banana-2-skill](https://github.com/kingbootoshi/nano-banana-2-skill) | 408 | — | Green-screen transparency and reference images, which is what ad production actually needs |
| 10 | [YouMind-OpenLab/ai-image-prompts-skill](https://github.com/YouMind-OpenLab/ai-image-prompts-skill) | 967 | — | A large prompt corpus across image models |

## Ad skills that already run on Codex

Judged on carrying `agents/openai.yaml` or an explicit Codex path, not on
whether a README mentions Codex.

| # | Repository | ★ | Licence | Worth reading for |
|---|---|---|---|---|
| 1 | [nowork-studio/notfair-plugin](https://github.com/nowork-studio/notfair-plugin) | 3453 | MIT | The most complete Codex-native paid-ads set: creative, launch, optimise, integrations, each with its own `openai.yaml` |
| 2 | [backtrue/meta-ad-library-video-scraper](https://github.com/backtrue/meta-ad-library-video-scraper) | 2 | — | Codex-first, and the best execution contract published: retry the same step, then stop and report, never invent a replacement workflow |
| 3 | [Humblytics/humblytics-marketing-skills](https://github.com/Humblytics/humblytics-marketing-skills) | 83 | MIT | Twelve skills targeting Claude and Codex from one source |
| 4 | [Splitwolf1/adlab](https://github.com/Splitwolf1/adlab) | 0 | — | Ships both `.claude-plugin` and `.codex-plugin`. Clean dual-runtime packaging |
| 5 | [JasonColapietro/suede-creator-skills](https://github.com/JasonColapietro/suede-creator-skills) | — | — | `suede-ad-creative` with a Codex agent manifest |
| 6 | [bestagentkits/agency-skills](https://github.com/bestagentkits/agency-skills) | — | — | Shows one skill maintained in both formats side by side |
| 7 | [TheMadBotterINC/Claude-Agents](https://github.com/TheMadBotterINC/Claude-Agents) | — | — | A `codex/skills/` tree parallel to the Claude one |
| 8 | [kocakburhan/Marketonomy](https://github.com/kocakburhan/Marketonomy) | — | — | A marketing agent with a Codex-compatible ad-creative skill |
| 9 | [BusyBee3333/viral-video-edit-skills](https://github.com/BusyBee3333/viral-video-edit-skills) | 3 | — | Beat-synced short-form editing, for Claude and Codex |
| 10 | [agent-sh/agentsys](https://github.com/agent-sh/agentsys) | 982 | — | 44 skills across Claude Code and Codex. Useful as a packaging reference |

## Video and non-static

| # | Repository | ★ | Licence | Worth reading for |
|---|---|---|---|---|
| 1 | [AKCodez/higgsfield-claude-skills](https://github.com/AKCodez/higgsfield-claude-skills) | 343 | — | Nineteen skills over Higgsfield and Seedance 2.0, split by genre. The closest published thing to this pack's video route |
| 2 | [charlesdove977/UGC-Factory](https://github.com/charlesdove977/UGC-Factory) | 70 | MIT | UGC ads end to end, fifteen genre styles |
| 3 | [rediumvex/viral-hooks-skill](https://github.com/rediumvex/viral-hooks-skill) | 83 | MIT | 100 hook formulas across ten psychological triggers, each with the reason it works |
| 4 | [iart-ai/ad-video-skills](https://github.com/iart-ai/ad-video-skills) | 7 | MIT | One motion-graphics template into batches of on-brand ads |
| 5 | [Splitwolf1/adlab](https://github.com/Splitwolf1/adlab) | 0 | — | The teardown framework: scroll-stop, hook, the 3-second rule, and the mute-and-blind modality test |
| 6 | [backtrue/meta-ad-library-video-scraper](https://github.com/backtrue/meta-ad-library-video-scraper) | 2 | — | The storyboard standard: shot, framing, on-screen text, script function, viewer job |
| 7 | [yaxeen/storytelling-skills](https://github.com/yaxeen/storytelling-skills) | 12 | — | Six psychology-based storytelling levers across short-form |
| 8 | [smixs/visual-skills](https://github.com/smixs/visual-skills) | 295 | — | Cinematic direction plus exact prompt syntax for video models |
| 9 | [alphaparkinc/genpark-longform-video-viral-short-repurposing-agent-skill](https://github.com/alphaparkinc/genpark-longform-video-viral-short-repurposing-agent-skill) | 8 | — | Long-form into vertical shorts with hook detection |
| 10 | [iliyanivanovmp-stack/seedance-ugc-ad-generator](https://github.com/iliyanivanovmp-stack/seedance-ugc-ad-generator) | 0 | — | Multi-shot UGC from one product photo. The shot-by-shot discipline this pack adopts |

## Copywriting

| # | Repository | ★ | Licence | Worth reading for |
|---|---|---|---|---|
| 1 | [robpalmer99/claude-code-copywriting-skills](https://github.com/robpalmer99/claude-code-copywriting-skills) | 27 | CC-BY-4.0 | Schwartz awareness levels driving length and destination, sell-the-click against sell-the-solution, and a compliance checker with a trigger-word list. **Attribution requested by the author and given here** |
| 2 | [boraoztunc/skills](https://github.com/boraoztunc/skills) | 289 | Apache-2.0 | The largest general copywriting set |
| 3 | [thalesholleben/copy-thief](https://github.com/thalesholleben/copy-thief) | 16 | — | High-conversion copy for Meta cold traffic, in Portuguese. A reminder that ad craft is language-specific |
| 4 | [avectats7/copy-that-sells](https://github.com/avectats7/copy-that-sells) | 11 | — | Print, out-of-home, headlines. Discipline that transfers to a 40-character field |
| 5 | [mikefutia/conversion-copywriter-skill](https://github.com/mikefutia/conversion-copywriter-skill) | 9 | — | Long-form Facebook ads, built on Harry Dry's specificity rules |
| 6 | [oathdriven/rymac-skills](https://github.com/oathdriven/rymac-skills) | 16 | — | Sales pages and VSLs alongside ad copy |
| 7 | [aixarizzo/kill-slop](https://github.com/aixarizzo/kill-slop) | 17 | — | Audits text against the user's own voice rather than a generic style |
| 8 | [199-biotechnologies/humanise-text-skill](https://github.com/199-biotechnologies/humanise-text-skill) | 12 | — | A 507-entry banned-word list and structural pattern detection. The anti-slop section owes it |
| 9 | [artgas1/infostyle-skill](https://github.com/artgas1/infostyle-skill) | 28 | — | Ilyakhov's information style. Cutting until only information remains |
| 10 | [elkadrinaoufal1996/hormozi-marketing-ultimate](https://github.com/elkadrinaoufal1996/hormozi-marketing-ultimate) | 12 | — | Offer construction, which decides more than copy does |

## Collections worth browsing

[ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) ·
[VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) ·
[travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) ·
[huggingface/upskill](https://github.com/huggingface/upskill)

---

## On "converting a Claude Code skill to Codex"

Worth being precise, because the phrase suggests more than it is.

A skill is a folder with a `SKILL.md` carrying `name` and `description` front
matter. Both runtimes read that. The differences are four:

1. **Where the folder goes.** `.claude/skills/` or `~/.claude/skills/` against
   `.agents/skills/` or `~/.codex/skills/`.
2. **`agents/openai.yaml`**, which Codex reads for the display name and whether
   the skill may be invoked implicitly. It belongs **inside** the skill folder,
   in `agents/`. At the root it is ignored.
3. **Tool vocabulary.** A skill that names `Read`, `Bash`, or an MCP tool by
   name is describing one runtime's furniture. Skills that describe *what must
   happen* rather than *which tool does it* port with no changes at all.
4. **Capabilities.** The real difference, and the one no conversion fixes. One
   session has image generation and a browser; another has an authenticated
   connector the first cannot reach. That is why this pack ships duo skills
   whose first act is to ask the other agent what it can actually do, rather
   than a table asserting what each runtime has.

So most of a good skill converts by copying it. The parts that do not convert
are the parts that should not have been written that way.

---

## Sources outside GitHub

- **Eugene Schwartz**, *Breakthrough Advertising* — the awareness ladder.
- **Meta's advertising policies**, particularly personal attributes and the
  restricted categories. Read the current page; the rules move.
- **EU Regulation 2017/745** on medical devices, and the Unfair Commercial
  Practices Directive as amended by the Omnibus Directive, for review rules.
- **The FTC rule on fake reviews and testimonials**, for the same in the US.
- Production work on French ecommerce accounts through 2026, which is where the
  engine, the workaround test, and the red-line discipline actually came from.
