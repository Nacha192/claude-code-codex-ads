# Creation tools and capability checks

Documentation snapshot: 2026-09-06. Verify live model availability, account, credits, rights and schemas before production. A skill contains instructions; it does not add a paid subscription or connector. Do not claim an unavailable tool exists.

| Provider / tool | Appropriate job | Check before use |
|---|---|---|
| OpenAI image generation / ChatGPT Images | Generate or edit illustrative/product-context stills | Use the installed image tool when available; API model names and UI labels differ. Official API docs currently show `gpt-image-2`; verify the exact available model rather than assuming "ChatGPT Image 2+" is a callable ID. |
| Gemini / Nano Banana / Nano Banana 2 | Reference-based stills, image edits and contextual compositions | Official docs identify Nano Banana 2 as `gemini-3.1-flash-image` and Nano Banana as `gemini-2.5-flash-image`. Check supported references, output sizes, costs and model lifecycle at runtime. |
| Higgsfield | Approved image workflows through the account's available models | Model list, generation mode, credits and commercial rights are account-dependent. No Higgsfield endpoint or guaranteed capability is bundled here. At zero credits, ask whether the user wants to switch to another legitimately owned funded account. |
| Claude Design | Brand-grounded layouts, campaign visuals and editable explorations | Discover actual web/MCP access and export formats; a Claude Code login alone does not prove Design access. Shares account usage according to current provider documentation. |
| Blender | Product visualization that materially needs 3D | Check runtime, assets and render budget; preserve product truth. Optional, not a prerequisite for strong ads. |
| Licensed existing photography | Authentic demonstrations and real product situations | Consent, usage rights, release scope, source quality and edit approval. |

## Motion and voice routes

**Read this before the table.** The entries below were observed in one connected catalogue on 2026-09-06 and are dated examples, not a list of what you have. Model names, durations and resolutions move faster than any document. Inspect the catalogue actually connected to this session, and if none is, say so instead of naming a model.

| Provider / tool | Appropriate job | Check before use |
|---|---|---|
| Seedance (Bytedance) | Reference-driven motion, identity and product consistency, multi-SKU | One catalogue exposed `seedance_2_0` (4 to 15 s, 480p to 4k in `std`, native audio), `seedance_2_0_mini`, `seedance_2_5` (4 to 30 s, with video edit and extension modes) and `seedance1_5`. A distributor's app ID is not a ByteDance API name: verify the exact model, duration, rights and regional access in the catalogue you actually hold. |
| Kling | Cinematic motion, multi-shot, motion transfer | `kling3_0` (3 to 15 s, `std`/`pro`/`4k`), `kling2_6` (5 or 10 s) and `kling3_0_turbo` observed in the same catalogue. Official-site crawling was blocked during research; verify mode, duration, rights and credits in the connected provider rather than from memory. |
| Google Veo and Gemini Omni | Cinematic motion, reference-driven video with native audio | `veo3_1` (4, 6 or 8 s, quality tiers), `veo3`, `veo3_1_lite`, `gemini_omni` (4 to 10 s, 720p) and `gemini_omni_flash_1_1` (3 to 10 s, up to 4k, with an edit mode) observed. Both Gemini entries offered 16:9 and 9:16 only, which decides square placements for you. |
| Wan, MiniMax, Grok, FLUX video | Alternative motion routes, some with long durations or 2K | `wan3_0` and `wan3_0_prime` (2 to 30 s), `wan2_7`, `minimax_h3` (2K), `minimax_h3_max`, `grok_video_v15`, `flux_3_video` (5 to 20 s) observed. Availability varies by account far more than quality does. |
| Ad-specific modes | Product ads, UGC formats, variant multiplication | `marketing_studio_video` (12 to 15 s, avatar and product ids, UGC, tutorial, unboxing and review presets, and a reference-driven scenario mode) and `ad_multiplier` observed. These are not generic video models: route to them deliberately when the job is an ad, rather than burying them in a model list. |
| Post-production tools | Lipsync, upscaling, deflicker, background removal, clipping | `sync_so`, `topaz_video`, `bytedance_video_upscale`, `video_deflicker`, `sam_3_video` and `clipify` observed. A post tool cannot rescue a clip whose idea does not work. |
| ElevenLabs or the connected speech tool | Voice previews, directed TTS, licensed sound workflows | Inspect the actual connected tools, the real voices, language and accent, commercial rights, model controls, cost estimates and remaining credits. Agent-management tools alone do not generate narration. The voices in a connected catalogue are that provider's own, and are not ElevenLabs voices merely because someone called them that. |
| OpenAI speech | Directed synthetic narration when the host exposes speech generation | Verify the supported speech model, available voices, output format and current AI-voice disclosure requirements. Do not invent custom voice availability. |
| Superwhisper | Spoken briefs, notes and transcription | A dictation and transcription route, not the engine for final narration. The two are constantly confused and they are not the same product. |
| Remotion and FFmpeg | Editable motion, captions, compositing and final renders | Check installed versions, fonts, media codecs, render commands and commercial licensing. Render locally only within the approved creation scope. |
| Human recording or licensed footage | Authentic demonstrations and actual testimony | Consent, usage rights, release scope, source quality and edit approval. Still the strongest option for a service ad, and the most often skipped. |

Voice cloning has its own file, [voice](video-voice.md), because consent and storage are decided there rather than in a capability table.

## Runtime capability card

Before promising a media deliverable, record available/read-only/generate/upload status for each needed function. Include tool name from the actual catalog, provider, account alias (no secrets), supported input/output, credits/cost certainty and fallback. Prefer an already connected tool over installing a new service. If the only route is manual, prepare the exact prompt, settings and expected output; label the generation step as pending, not complete.

## Approval proposal

"I propose [provider/model], [N assets], [formats and sizes], using [approved sources]. Estimated cost is [estimate or unknown], with a ceiling of [credits/currency or bounded pilot]. The account is [non-secret alias]. May I produce this batch?"

Translate the proposal. When the user has already approved all these material parameters, proceed and record the existing authorization instead of repeating the question. Generation permission does not authorize a subscription purchase or campaign activation.

Record the approved parameters as a `generation_request` artifact and run `scripts/check_artifact.py` on it before the first call, as described in the [shared contract](core.md). Expanding the batch past the approved item count, or switching provider, model or account after approval, fails that check by design. The cost ceiling is a different thing: it is recorded as text so you and the user can compare it, and no script adds up what was spent. A zero-credit account fails it too: stop and ask the user, never fall back silently.

## Official references

- [OpenAI image generation](https://developers.openai.com/api/docs/guides/image-generation)
- [Gemini image generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Higgsfield](https://higgsfield.ai/): inspect the actual logged-in catalog.
- [Meta Ads Guide](https://www.facebook.com/business/ads-guide)
- [Meta Advertising Standards](https://transparency.meta.com/policies/ad-standards/): direct policy/library pages were not fully retrievable during this build; recheck for the actual campaign.
- [Meta AI advertising transparency](https://about.fb.com/news/2025/02/gen-ai-transparency-metas-ads-products/)

- [Claude Design official guide](https://support.claude.com/en/articles/14604416-get-started-with-claude-design)
- [OpenAI speech generation](https://developers.openai.com/api/docs/guides/text-to-speech)
- [ElevenLabs text to speech](https://elevenlabs.io/docs/capabilities/text-to-speech)
- [Superwhisper](https://superwhisper.com/)
- [Remotion documentation](https://www.remotion.dev/docs/)
- [Kling](https://klingai.com/): official-site crawling was blocked during research; treat any Kling detail here as unverified until seen in the connected provider.
