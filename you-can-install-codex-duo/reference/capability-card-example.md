# Codex capability card

Inspected 2026-09-06. Session snapshot, not a universal product claim. Yes means exposed or the specific local check passed; it does not imply an authenticated generation succeeded. approval: never; sandbox: workspace-write; restricted network. Actual writes to the proposed destination were denied. No external request, paid generation or private account read was made for this inspection.

| Capability | Status | Observed evidence and limit |
|---|---|---|
| Image generation/editing | Yes | image_gen.imagegen exposed; ElevenLabs creative_generate_image and creative_edit_image in actual tool inventory. No generation executed. |
| Video generation | Depends | ElevenLabs creative_generate_video and creative_generate_in_flow exposed. Correct account, model access, credits and successful execution unverified. |
| Browser control | Yes | mcp__cua_repl.js exposes supported browser surfaces. Connection not opened. Native desktop control explicitly disabled. |
| Persistent REPL | Yes | mcp__node_repl__js exposed; CUA also persists JavaScript state. functions.exec itself is a fresh isolate per call. No REPL execution probe performed. |
| Background tasks | Yes | exec_command supports running sessions with write_stdin; functions.exec supports yielding and wait continuation. No guarantee of durable scheduling or future model wakeups. |
| Subagents | Depends | collaboration.spawn_agent exposed, four total slots including parent. Session requires explicit user or applicable skill/AGENTS authorization for delegation. None spawned. |
| Authenticated connectors | Depends | ElevenLabs and Sites tools exposed. Authentication, intended account, permissions and balance unverified. No established Meta, Shopify, Gmail or Higgsfield access. |
| Local image inspection | Yes | view_image exposed with image-return support. No image inspection needed for this task. |
| ffmpeg | Yes | ffmpeg -version succeeded, exit 0, version 8.1.1-full_build-www.gyan.dev. Specific encoding workflows not tested. |
| Headless browser | Depends | Node root-workspace probe resolved neither playwright nor puppeteer. Other install locations were not ruled out; no headless launch tested. Hidden CUA tabs do not prove a local headless renderer. |

Higgsfield is recommended but not installed in this session, with no callable tool found. Gemini, Seedance, Kling and Claude Design access is not established. Do not silently substitute ElevenLabs for a chosen provider. Roles follow verified access per step, never agent brand. Correct this card when new observations contradict it. This run hands off and returns control rather than watching the channel.
