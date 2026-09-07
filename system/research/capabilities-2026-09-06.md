# Capabilities actually observed, 2026-09-06

Recorded during the build by running commands and calling connectors, not from memory. Both assistants were asked on the same day. This is the `observed` layer: anything about a provider that is not here is at best `documented`, at worst `hypothesis`.

**This describes two machines, not the world.** Anyone installing these packs has a different set of tools. That is exactly why the packs detect a capability instead of promising one.

---

## Codex, in its CLI

Verified by Codex itself, by executing the commands rather than assuming them.

| Capability | Result |
|---|---|
| Video generation | **No.** No video provider exposed. Runway appears among available plugins but is not installed. |
| Voice or audio generation | **No.** No TTS, no cloning, no speech provider connected. |
| Image generation | Yes, raster images only. |
| Network | Yes through its web tool, a public GitHub API read succeeded. **No** from the shell: `curl` could not open an outbound connection. |
| ffmpeg | Yes, 8.1.1, real execution, exit 0. |
| python | Yes, CPython 3.11.15. |
| node | Yes, 26.3.0. |

Direct consequence: "Codex generates the video" was false **in this environment**. It stays true elsewhere, in an interface where a video model is connected. So the packs cannot write it as a fact.

---

## Claude Code, in one session

Verified by calling the connector rather than assuming it. A Higgsfield connector was attached and exposed real video, audio and voice models.

**This is a connector of that session, not a property of Claude Code.** Claude Code without it does not generate video, and that is the default case.

### Generative video models observed

Identifiers, durations and resolutions as the API declared them.

| Model | Provider | Duration | Resolutions | Native audio |
|---|---|---|---|---|
| `seedance_2_0` | Bytedance | 4 to 15 s | 480p, 720p, 1080p, 4k (`std`); 480p, 720p (`fast`) | yes |
| `seedance_2_0_mini` | Bytedance | 4 to 15 s | 480p, 720p | yes |
| `seedance_2_5` | Bytedance | 4 to 30 s | 480p, 720p, 1080p | yes |
| `seedance1_5` | Bytedance | 4, 8, 12 s | 480p, 720p, 1080p | yes |
| `veo3_1` | Google | 4, 6, 8 s | basic, high, ultra tiers | yes |
| `veo3` | Google | preview and fast variants | not declared | yes |
| `veo3_1_lite` | Google | 4, 6, 8 s | not declared | optional, costs more |
| `gemini_omni` | Google | 4 to 10 s | 720p | yes |
| `gemini_omni_flash_1_1` | Google | 3 to 10 s | 360p to 4k | yes |
| `kling3_0` | Kling | 3 to 15 s | std, pro, 4k modes | on/off |
| `kling2_6` | Kling | 5, 10 s | not declared | yes |
| `kling3_0_turbo` | Kling | 3 to 15 s | 720p, 1080p | not declared |
| `wan3_0`, `wan3_0_prime` | Wan | 2 to 30 s | 480p, 720p, 1080p | yes |
| `wan2_7` | Wan | 2 to 15 s | 720p, 1080p | yes |
| `wan2_6` | Wan | 5, 10, 15 s | 720p, 1080p | not declared |
| `minimax_h3` | MiniMax | 4 to 15 s | 2K | audio references |
| `minimax_h3_max` | MiniMax | 5 to 15 s | 480p, 768p | audio references |
| `minimax_hailuo` | Hailuo | 6, 10 s | 512, 768, 1080 | not declared |
| `flux_3_video` | Black Forest Labs | 5 to 20 s | 720p, 1080p | yes |
| `grok_video_v15` | xAI | 2 to 15 s | 480p, 720p, 1080p | audio references |
| `grok_video` | xAI | 1 to 15 s | not declared | yes |
| `happy_horse_video` | Happy Horse | 3 to 15 s | 720p, 1080p | not declared |
| `cinematic_studio_3_0` | Higgsfield | 4 to 15 s | 480p to 4k | optional |
| `cinematic_studio_video_v2` | Higgsfield | 3 to 12 s | pro and std modes | on/off |
| `marketing_studio_video` | Higgsfield | 12 to 15 s | 480p, 720p, 1080p | on by default |
| `ad_multiplier` | Higgsfield | 4 to 30 s | 480p, 720p, 1080p | yes |

### Non-generative video tools observed

`sync_so` (lipsync), `topaz_video`, `bytedance_video_upscale` and `video_upscale` (upscaling), `video_deflicker`, `sam_3_video` and `video_background_remover` (matting), `clipify` (one YouTube video cut into subtitled clips), `hf_mult_motion_control` and `hf_mult_replace_object` (motion transfer, object replacement).

### What this changes for advertising

`marketing_studio_video` is a direct route to a product ad with an avatar, UGC, tutorial, unboxing and product-review presets, and a reference mode that follows an existing ad's scenario. `ad_multiplier` turns one ad into variants. Neither has an equivalent in a generic video model, so the packs route to them deliberately instead of burying them in a model list.

### Voice

The connector exposed a voice catalogue with an identifier, a gender and a public preview per voice. Thirty were listed on a first page, with more behind a cursor.

**These are not ElevenLabs voices.** They are the connected provider's own. So "catalogue the ElevenLabs voices" reads, in the packs, as "catalogue the voices of the speech provider actually connected", ElevenLabs being one of them when the host exposes it. A public preview you can listen to beats a description found in a demo video, and it was available here.

The connector also exposed voice creation from a recording, which is exactly the cloning route the packs describe. It was not called: cloning waits for a recording and an explicit agreement from the person whose voice it is.

---

## What the packs take from this

1. No edition declares "I generate video" as a property. It discovers the answer when it needs it, and says what it found.
2. The list above is dated. It is an example of what a host can expose, never the reference list.
3. The identifiers, durations and resolutions in `video-models.md` come from here, labelled `observed`, with this date. Everything else carries its own label.
