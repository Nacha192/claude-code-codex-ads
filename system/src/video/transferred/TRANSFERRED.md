# Non-static material removed from the static packs

Everything here was inside the four advertising packs and was taken out on 2026-09-06, so those packs cover still creative and nothing else. Nothing was deleted: it is staged here for the video pack, next to the references already written in `../references/`.

Read this before building the video entrypoints. Each section says where the material came from and what has to be re-wired.

## Whole files

| File | Was | Re-wire |
|---|---|---|
| `video-voice.md` | `src/common/references/video-voice.md`, shipped in all four packs | Becomes a video-pack reference. It overlaps with `../references/video-prompting.md` and `../references/video-assembly.md`; merge rather than shipping both. |
| `moved-module-ids.json` | the 18 source adaptations routed `video` or `voice` | The video build regenerates these cards from `system/research/sources.json` by selecting those two routes. The source records were never removed. |

## The two top-ten selections

They were `codex-video` and `claude-video` in `build.py`. Restore them in the video build, keeping the order:

```
codex-video: remotion-dev--remotion-best-practices, iart-ai--ad-creative-video,
  nyosegawa--remotion-promo-video-factory, openai--speech, gooseworks-ai--review-ugc-render,
  coreyhaines31--video, remotion-dev--remotion-captions, inference-sh--seedance,
  zubair-trabzada--ads-video, yaxeen--retention-audit

claude-video: iart-ai--ad-creative-video, zubair-trabzada--ads-video,
  nyosegawa--remotion-promo-video-factory, remotion-dev--remotion-best-practices,
  hyperfx-ai--video-generation, inference-sh--ai-marketing-videos,
  inference-sh--talking-head-production, openai--speech, iart-ai--launch-video,
  gooseworks-ai--review-ugc-render
```

The video build also needs the two route entries removed from `ROUTES` and `HOST`:

```python
ROUTES: 'video':'video-voice.md', 'voice':'video-voice.md'
HOST['video']=('Use installed motion/rendering tools or an approved video provider and inspect output.',
               'Use available rendering or video tools; transfer only an approved subtask to the real peer in team mode.')
HOST['voice']=('Use a verified speech tool, approved voice/script and bounded takes.',
               'Discover an actual TTS capability; the Codex speech tool does not arrive with this text.')
```

Three upstream repositories now contribute only to the video pack and must be credited there: `remotion-dev/skills`, `nyosegawa/skills`, `iart-ai/ad-video-skills`.

## The storyboard artifact kind

Removed from `check_artifact.py`, which now knows `brief`, `creative` and `generation_request`. Put it back in the video pack's checker, and restore the `storyboard` name in the kind error message and in `core.md`.

```python
    elif kind=='storyboard':
        scenes=data.get('scenes')
        if not isinstance(scenes,list) or not scenes:return errors+['Nonempty scenes array required'],warnings
        previous=0.0
        for i,s in enumerate(scenes):
            if not isinstance(s,dict):errors.append('Scene must be an object');continue
            start=s.get('start');end=s.get('end')
            valid=lambda n:isinstance(n,(int,float)) and not isinstance(n,bool) and math.isfinite(n)
            if not valid(start) or not valid(end) or start<0 or end<=start:errors.append(f'Scene {i}: invalid times');continue
            if start<previous:errors.append(f'Scene {i}: overlap; use explicit transition metadata in the source project instead')
            if start>previous:warnings.append(f'Scene {i}: timeline gap requires review')
            previous=end
            need(s,'visual')
            duration=s.get('measured_voice_seconds')
            if duration is not None and (not valid(duration) or duration<0):errors.append(f'Scene {i}: invalid measured voice duration')
            elif duration is not None and duration>end-start:errors.append(f'Scene {i}: voice exceeds available scene duration')
            elif s.get('voice') and duration is None:warnings.append(f'Scene {i}: narration fit not measured')
```

Its three tests, removed from `test_tools.py`:

```python
 def test_storyboard_measured_overrun(self):
  d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':2,'visual':'product','voice':'demo','measured_voice_seconds':3}]};self.assertTrue(checker.check(d)[0])
 def test_nan_and_bool_times(self):
  for value in [float('nan'),True]:
   d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':value,'end':2,'visual':'product'}]};self.assertTrue(checker.check(d)[0])
 def test_unmeasured_voice_warns(self):
  d={'schema_v':'1.0.0','kind':'storyboard','scenes':[{'start':0,'end':3,'visual':'product','voice':'demo'}]};e,w=checker.check(d);self.assertFalse(e);self.assertTrue(w)
```

The static suite keeps `test_storyboard_kind_is_no_longer_accepted`, which asserts the removal. Delete that test in the video pack, where the kind exists again.

## Provider rows

Removed from `providers.md`. The static pack keeps OpenAI images, Gemini, Higgsfield stills, Claude Design, Blender and licensed photography.

| Provider / tool | Appropriate job | Check before use |
|---|---|---|
| Seedance 2.0 | Generated motion clips through an available provider | Verify the distributor's actual model ID, duration, first/last-frame or reference modes, resolution, audio, rights and regional access. Do not assume a third-party app ID is a direct ByteDance API name. |
| ElevenLabs | Voice previews, directed TTS and licensed sound workflows | Inspect the connected creative/TTS tools, actual voices, language/accent, commercial rights, model controls, estimates and remaining credits. Agent-management tools alone do not generate narration. |
| OpenAI speech | Directed synthetic narration when the host exposes speech generation | Verify the supported speech model, available voices, output format and current AI-voice disclosure requirements. Do not invent custom voice availability. |
| Superwhisper | Spoken briefs, notes and transcription | It is a dictation/transcription route, not the TTS engine for final narration. |
| Remotion + FFmpeg | Editable motion, captions, compositing and final renders | Check installed versions, fonts, media codecs, render commands and commercial licensing. Render locally only within the approved creation scope. |
| Kling | Generated illustrative video where supported | Official-site crawling was blocked during research; verify actual model, mode, duration, rights and credits in the connected provider before promising delivery. |
| Human recording / licensed existing footage | Authentic demonstrations and actual testimony | Consent, usage rights, release scope, source quality and edit approval. |

Removed official-reference links: OpenAI speech generation, ElevenLabs text to speech, Superwhisper Voice to Text, Remotion documentation, Kling official site. The Higgsfield line also lost the note that exact Seedance documentation could not be verified during the build; that caveat belongs with Seedance in the video pack.

Removed rows from `you-can-install-tools.md`: Seedance and Kling as video routes, ElevenLabs or an available OpenAI speech tool for narration, Remotion and FFmpeg for assembly, and Superwhisper's transcription half.

## Sentences taken out of shared references

- `core.md`: storyboards in the list of work that can proceed without approval; voice choice in the production proposal; audio quality in the rendering caveat.
- `v11-lessons.md`, whole paragraph: *For the separate service-video case, the lesson is completion discipline: a motion draft without the requested narration is not the finished ad. Voice quality depends on audition, pronunciation, intent, actual timing, mix and export inspection. Access to a provider and credits must be checked rather than promised from a connector name.*
- `team.md`: *If a peer cannot generate audio but the other can, hand off the approved voice card, exact script, account/provider scope and remaining ceiling.* The static pack now states the same rule for any capability one peer lacks.
- `copywriting.md`: the demonstration angle referred to footage, and language review could use audio review.
- `intake.md`: duration and voice/accent in the production intake.
- `research.md`: video execution in the angle record.
- Entrypoints: the static-or-video routing sentence, the description frontmatter, and *a script, prompt or silent video is not a complete voiced ad*.

## Still to decide for the video pack

The user asked for ElevenLabs voice creation, voice cloning from a supplied sample, and a Superwhisper Pro transcription route. None of that exists yet in any file here: it has to be written against real provider documentation, with the same evidence labels as the rest, and with the consent question that voice cloning raises stated plainly rather than skipped.
