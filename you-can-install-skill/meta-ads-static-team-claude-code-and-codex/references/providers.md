# Creation tools and capability checks

Documentation snapshot: 2026-09-06. Verify live model availability, account, credits, rights and schemas before production. A skill contains instructions; it does not add a paid subscription or connector. Do not claim an unavailable tool exists.

| Provider / tool | Appropriate job | Check before use |
|---|---|---|
| OpenAI image generation / ChatGPT Images | Generate or edit illustrative/product-context stills | Use the installed image tool when available; API model names and UI labels differ. The guide named `gpt-image-2` plus the `gpt-image-2.5-sunburst` and `gpt-image-2.5-flare` variants on 2026-09-09, with `gpt-image-1` listed for shutdown on 2026-10-23 and `gpt-image-1-mini`, `gpt-image-1.5` and `chatgpt-image-latest` on 2026-12-01. Verify the exact available model rather than assuming a label is a callable ID. Prompt structure, legal canvases and parameters are in [image prompting](image-prompting.md). |
| Gemini / Nano Banana / Nano Banana 2 | Reference-based stills, image edits and contextual compositions | Official docs identify Nano Banana 2 as `gemini-3.1-flash-image` and Nano Banana as `gemini-2.5-flash-image`. Check supported references, output sizes, costs and model lifecycle at runtime. |
| Higgsfield | Approved image workflows through the account's available models | Model list, generation mode, credits and commercial rights are account-dependent. No Higgsfield endpoint or guaranteed capability is bundled here. At zero credits, ask whether the user wants to switch to another legitimately owned funded account. |
| Claude Design | Brand-grounded layouts, campaign visuals and editable explorations | Discover actual web/MCP access and export formats; a Claude Code login alone does not prove Design access. Shares account usage according to current provider documentation. |
| Blender | Product visualization that materially needs 3D | Check runtime, assets and render budget; preserve product truth. Optional, not a prerequisite for strong ads. |
| Licensed existing photography | Authentic demonstrations and real product situations | Consent, usage rights, release scope, source quality and edit approval. |

Video and voice providers are not listed here on purpose. Seedance, Kling, ElevenLabs, OpenAI speech, Superwhisper and Remotion belong to the video pack, with the checks that go with them. Naming a video provider from this pack would promise a workflow it does not carry.

## Runtime capability card

Before promising a media deliverable, record available/read-only/generate/upload status for each needed function. Include tool name from the actual catalog, provider, account alias (no secrets), supported input/output, credits/cost certainty and fallback. Prefer an already connected tool over installing a new service. If the only route is manual, prepare the exact prompt, settings and expected output; label the generation step as pending, not complete.

## Approval proposal

"I propose [provider/model], [N assets], [formats and sizes], using [approved sources]. Estimated cost is [estimate or unknown], with a ceiling of [credits/currency or bounded pilot]. The account is [non-secret alias]. May I produce this batch?"

Translate the proposal. When the user has already approved all these material parameters, proceed and record the existing authorization instead of repeating the question. Generation permission does not authorize a subscription purchase or campaign activation.

Record the approved parameters as a `generation_request` artifact and run `scripts/check_artifact.py` on it before the first call, as described in the [shared contract](core.md). Expanding the batch past the ceiling, or switching provider, model or account after approval, fails that check by design. A zero-credit account fails it too: stop and ask the user, never fall back silently.

## Official references

- [OpenAI image generation](https://developers.openai.com/api/docs/guides/image-generation)
- [Gemini image generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Higgsfield](https://higgsfield.ai/): inspect the actual logged-in catalog.
- [Meta Ads Guide](https://www.facebook.com/business/ads-guide)
- [Meta Advertising Standards](https://transparency.meta.com/policies/ad-standards/): direct policy/library pages were not fully retrievable during this build; recheck for the actual campaign.
- [Meta AI advertising transparency](https://about.fb.com/news/2025/02/gen-ai-transparency-metas-ads-products/)

- [Claude Design official guide](https://support.claude.com/en/articles/14604416-get-started-with-claude-design)
