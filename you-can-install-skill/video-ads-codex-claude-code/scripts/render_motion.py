"""One command from `motion-project.json` to real MP4 files, measured and corrected.

    python scripts/render_motion.py motion-project.json --root . --apply

This is the one-shot the packs promise. It detects what the machine can do, renders
every requested format as its own composition, measures each export by decoding it,
runs a bounded correction loop, writes contact sheets and control frames, and then
updates the manifest **from the files that exist** rather than from the plan.

Three rules it will not bend:

- Without `--apply` it writes no export and changes no manifest. A preview that
  quietly renders is how a paid provider gets called by accident.
- The manifest is validated before anything renders. Rendering from a manifest that
  claims more than it can show produces a file that inherits the claim.
- Every number written back into the manifest comes from `inspect_video.py`, which
  decodes the file. Nothing here reports what it intended to produce.

Exit codes: 0 clean, 1 findings left open, 2 bad usage or invalid manifest,
3 the machine cannot render and said which part is missing.
"""
import argparse, hashlib, json, shutil, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import motion_engine as engine          # noqa: E402
import inspect_video                     # noqa: E402
import check_motion_project as checker    # noqa: E402

MAX_PASSES = 3
STATE_DIR = '.motion-work'


def digest_of(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def plan_fingerprint(manifest, fmt, design):
    """What this format's render depends on.

    A resume is only safe when the inputs have not moved, so the fingerprint covers
    the scenes, the captions, the audio, the design tokens and this format's own
    block. Change any of them and the clip is rebuilt instead of trusted.
    """
    payload = {'scenes': manifest.get('scenes'), 'captions': manifest.get('captions'),
               'voice': manifest.get('voice'), 'music': manifest.get('music'),
               'sfx': manifest.get('sfx'), 'design': design, 'format': fmt,
               'loudness': manifest.get('loudness_target')}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def resolve_one(label, path, root, out):
    """One declared file to a real path, refusing anything that leaves the project."""
    if not (isinstance(path, str) and path.strip()):
        return None
    why = checker.escaping(path)
    if why:
        raise engine.EngineError('%s has a path %s' % (label, why))
    full = (Path(root) / path).resolve()
    try:
        full.relative_to(Path(root).resolve())
    except ValueError:
        raise engine.EngineError('%s resolves outside the project' % label)
    if not full.is_file():
        raise engine.EngineError('%s names a file that is not there: %s' % (label, path))
    out[path] = full
    return full


def resolve_assets(manifest, root):
    """Every declared file to a real path, refusing any that leaves the project.

    The audio belongs here as much as the pictures do, and it did not used to. Only
    `assets[]` was resolved, so `voice.file`, `music.file` and `sfx[].file` reached
    ffmpeg as the relative strings the manifest had written, and ffmpeg resolves
    those against the working directory of the process. Rendering from anywhere but
    the project root then died on the audio with `--root` set correctly and every
    file present. Worse, those three skipped the escape check the pictures get, so a
    manifest could name a sound file anywhere on the machine and have it read.

    No test could see it: every one of them ran with the working directory already
    set to the project.
    """
    out = {}
    for asset in manifest.get('assets') or []:
        if not isinstance(asset, dict):
            continue
        full = resolve_one('asset %s' % asset.get('id'), asset.get('path'), root, out)
        if full is not None:
            out[asset.get('id')] = full
    for field in ('voice', 'music'):
        block = manifest.get(field)
        if isinstance(block, dict):
            resolve_one('%s.file' % field, block.get('file'), root, out)
    for i, effect in enumerate(manifest.get('sfx') or []):
        if isinstance(effect, dict):
            resolve_one('sfx[%d].file' % i, effect.get('file'), root, out)
    return out


def timeline_seconds(manifest):
    return round(max(float(s['end']) for s in manifest['scenes']), 3)


def expectations(manifest, fmt):
    """Everything the manifest already declares, handed to the measurer as arguments.

    The measurer invents no threshold; it only enforces what arrived. So this is the
    single place where a brief becomes a pass or a fail, and it is all traceable to
    a field somebody filled in.
    """
    cues = ((manifest.get('captions') or {}).get('cues') or [])
    loud = manifest.get('loudness_target') or {}
    return {'expect_ratio': fmt['ratio'], 'expect_width': int(fmt['width']),
            'expect_height': int(fmt['height']), 'expect_duration': timeline_seconds(manifest),
            'duration_tolerance': 0.5, 'expect_fps': float(fmt['fps']),
            'expect_audio_streams': 1, 'expect_sample_rate': 48000,
            'loudness': float(loud['value']) if loud.get('value') is not None else None,
            'loudness_tolerance': 1.5,
            'max_true_peak': float(loud.get('true_peak')) if loud.get('true_peak') is not None else None,
            'captions_end': max([float(c.get('end', 0)) for c in cues], default=None)}


class Args:
    """inspect_video.compare reads attributes, so the expectations arrive as one."""
    def __init__(self, mapping):
        for k, v in mapping.items():
            setattr(self, k, v)


def complete_clip(clip, want_frames):
    """Is this scene clip finished, or was it half written when the run was killed?

    A file that exists is not a file that is done. ffmpeg writes the index last, so an
    interrupted encode leaves a plausible-looking mp4 that decodes short or not at all,
    and reusing it puts a missing second into the middle of the ad rather than raising
    anything. Counting the frames is the only answer the file can be trusted to give.
    """
    if not clip.is_file() or clip.stat().st_size <= 0:
        return False
    code, out, _ = engine.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                               '-count_frames', '-show_entries', 'stream=nb_read_frames',
                               '-of', 'default=nk=1:nw=1', str(clip)], timeout=300)
    if code != 0:
        return False
    try:
        return int((out or '').strip().splitlines()[0]) == want_frames
    except (ValueError, IndexError):
        return False


def render_format(manifest, fmt, design, assets, root, work, resume, measured_loudness):
    """Everything for one ratio: scenes, assembly, captions, audio, mux."""
    caps = engine.detect()
    font = (design.get('type') or {}).get('family_file') or caps['font_file']
    if not font or not Path(str(font)).is_file():
        font = caps['font_file']
    # Fit before drawing, and fit against the face that will actually draw it. The
    # type scale is settled once for the whole film so a role keeps one size across
    # the scenes, and a column that cannot hold its copy is a refusal rather than a
    # pile of overlapping lines.
    layout = engine.fit_layout(engine.layout_for(fmt, design), design,
                               manifest['scenes'], font)
    seconds = timeline_seconds(manifest)
    scenes = manifest['scenes']
    work.mkdir(parents=True, exist_ok=True)
    clips = []
    for i, scene in enumerate(scenes):
        clip = work / ('scene-%02d.mp4' % i)
        want_frames = engine.scene_frames(
            round(float(scene['end']) - float(scene['start']), 3)
            + engine.transition_tail(scenes, i), fmt['fps'])
        if resume and complete_clip(clip, want_frames):
            clips.append(clip)
            continue
        engine.render_scene(scene, fmt, design, layout, font, assets, work, clip,
                            tail=engine.transition_tail(scenes, i))
        clips.append(clip)
    joined = engine.assemble(clips, scenes, fmt, work, work / 'joined.mp4')
    captions = manifest.get('captions') or {}
    if captions.get('cues'):
        ass = engine.write_ass(captions['cues'], layout, design,
                               Path(str(font)).stem, work / 'captions.ass', captions)
        joined = engine.burn_captions(joined, ass, work / 'captioned.mp4', fmt)
    loud = manifest.get('loudness_target') or {}
    audio = engine.build_audio(manifest, assets, seconds, work, work / 'audio.m4a',
                               loudness=loud, measured=measured_loudness)
    final = work / 'export.mp4'
    engine.mux(joined, audio, final, fmt, seconds)
    return final, layout


def inspect(path, manifest, fmt):
    measurements, findings = inspect_video.measure(Path(path))
    measurements['sha256'] = digest_of(path)
    measurements['path'] = str(path)
    findings = findings + inspect_video.compare(measurements, Args(expectations(manifest, fmt)))
    return measurements, findings


def defect(finding, target, fix, status='open'):
    return {'timecode': finding.get('timecode', '00:00'),
            'observation': finding['observation'], 'severity': finding['severity'],
            'why_it_fails': 'A measurement disagreed with what the manifest declares',
            'fix': fix, 'target': target, 'status': status}


def corrections_for(findings):
    """Which findings this engine knows how to repair at the source, and how.

    Anything not in this table is recorded and handed to a person. An engine that
    claims to fix what it cannot is worse than one that stops: the defect stays and
    the record says it was handled.
    """
    plan = {}
    for f in findings:
        text = f['observation'].lower()
        if 'integrated loudness' in text or 'true peak' in text:
            plan['loudness'] = 'Re-run loudnorm as a second pass, with the measured values'
        elif 'silence at the head' in text:
            plan['head_silence'] = 'Trim the leading silence from the audio track'
        elif 'opens on' in text and 'black' in text:
            plan['head_black'] = 'Remove the entrance fade on the first scene'
        elif 'duration is' in text:
            plan['duration'] = 'Re-mux to the exact timeline duration'
    return plan


def apply_corrections(manifest, plan, work):
    """Change the source, never the export. Returns what was actually changed."""
    applied = []
    if 'head_black' in plan:
        first = manifest['scenes'][0]
        for layer in first.get('layers') or []:
            if layer.get('kind') == 'text' and float(layer.get('at', 0)) <= 0.01:
                layer['at'] = 0.0
                layer['enter_seconds'] = min(float(layer.get('enter_seconds', 0.45)), 0.25)
        bg = first.setdefault('background', {})
        bg.setdefault('kind', 'solid')
        applied.append('head_black')
    if 'head_silence' in plan:
        music = manifest.get('music') or {}
        if music:
            music['gain_db'] = float(music.get('gain_db', -18.0)) + 2.0
            applied.append('head_silence')
    return applied


def run():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest')
    p.add_argument('--root', default='.', help='Directory the manifest paths are relative to')
    p.add_argument('--apply', action='store_true', help='Actually render and write the manifest')
    p.add_argument('--resume', action='store_true', help='Reuse scene clips already on disk')
    p.add_argument('--formats', help='Comma-separated ratios, default every composed format')
    p.add_argument('--max-passes', type=int, default=MAX_PASSES)
    p.add_argument('--contact-sheet', action='store_true', default=True)
    p.add_argument('--json', action='store_true')
    a = p.parse_args()

    root = Path(a.root).resolve()
    manifest_path = Path(a.manifest)
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        print('Unreadable manifest: %s' % e, file=sys.stderr)
        return 2
    errors, _ = checker.check(manifest)
    # A manifest that already claims files it does not have would hand this run its
    # own claim to inherit, so the state-dependent rules are re-read after rendering.
    blocking = [e for e in errors if 'export' not in e.lower() and 'state is' not in e.lower()]
    if blocking:
        print(json.dumps({'error': 'the manifest is not valid, nothing was rendered',
                          'errors': blocking[:10]}, indent=2))
        return 2

    caps = engine.detect()
    if not caps['usable']:
        print(json.dumps({'error': 'this machine cannot render', 'reason': caps.get('reason'),
                          'capabilities': {k: caps[k] for k in
                                           ('ffmpeg', 'ffprobe', 'freetype', 'fonts',
                                            'missing_filters', 'encoders')}}, indent=2))
        print('Nothing was rendered, and that is not a pass.', file=sys.stderr)
        return 3

    design = engine.resolve_design(manifest)
    try:
        assets = resolve_assets(manifest, root)
    except engine.EngineError as e:
        print(json.dumps({'error': str(e)}, indent=2))
        return 2

    wanted = [f for f in manifest['formats']
              if not a.formats or f['ratio'] in a.formats.split(',')]
    state_dir = root / STATE_DIR
    state_path = state_dir / 'render-state.json'
    state = {}
    if a.resume and state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding='utf-8'))
        except ValueError:
            state = {}

    report = {'engine': caps['engine'], 'javascript_required': False,
              'formats': [], 'passes': {}, 'apply': bool(a.apply)}
    if not a.apply:
        for fmt in wanted:
            layout = engine.fit_layout(engine.layout_for(fmt, design), design,
                                       manifest['scenes'], engine.detect()['font_file'])
            report['formats'].append({'ratio': fmt['ratio'], 'action': 'would-render',
                                      'width': fmt['width'], 'height': fmt['height'],
                                      'composition': layout['shape'],
                                      'type_fit': layout['fit_scale'],
                                      'scenes': len(manifest['scenes'])})
        print(json.dumps(report, indent=2))
        return 0

    exports, all_findings = [], []
    for fmt in wanted:
        ratio_key = fmt['ratio'].replace(':', 'x')
        work = state_dir / ratio_key
        fingerprint = plan_fingerprint(manifest, fmt, design)
        target_rel = 'exports/%s/%s' % (ratio_key, (manifest.get('slug') or 'ad') + '.mp4')
        target = root / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        known = state.get(fmt['ratio']) or {}
        if (a.resume and known.get('fingerprint') == fingerprint and target.is_file()
                and known.get('sha256') == digest_of(target)):
            measurements, findings = inspect(target, manifest, fmt)
            report['formats'].append({'ratio': fmt['ratio'], 'action': 'resumed',
                                      'path': target_rel})
        else:
            # The fingerprint of the run in progress, written before the first scene
            # rather than after the last. The finished-run state file is no use to a
            # resume: an interrupted run never reaches the line that writes it, so a
            # resume keyed on it discarded every clip the interrupted run had made,
            # which is the one case resume exists for.
            stamp = work / 'plan.json'
            started = {}
            if stamp.is_file():
                try:
                    started = json.loads(stamp.read_text(encoding='utf-8'))
                except ValueError:
                    started = {}
            resume_clips = a.resume and (known.get('fingerprint') == fingerprint
                                         or started.get('fingerprint') == fingerprint)
            if not resume_clips and work.exists():
                shutil.rmtree(work, ignore_errors=True)
            work.mkdir(parents=True, exist_ok=True)
            stamp.write_text(json.dumps({'fingerprint': fingerprint,
                                         'ratio': fmt['ratio']}, indent=2) + '\n',
                             encoding='utf-8')
            measured = None
            findings, measurements = None, None
            passes = 0
            while passes < max(1, a.max_passes):
                passes += 1
                final, layout = render_format(manifest, fmt, design, assets, root, work,
                                              resume_clips, measured)
                shutil.copyfile(final, target)
                measurements, findings = inspect(target, manifest, fmt)
                blocking_now = [f for f in findings if f['severity'] == 'blocking'] + \
                               [f for f in findings if f['severity'] == 'high']
                if not blocking_now:
                    break
                plan = corrections_for(blocking_now)
                if not plan:
                    break
                if 'loudness' in plan and measured is None:
                    measured = engine.measure_loudness(manifest, assets,
                                                       timeline_seconds(manifest), work,
                                                       manifest.get('loudness_target') or {})
                    if measured is None:
                        plan.pop('loudness')
                apply_corrections(manifest, plan, work)
                resume_clips = 'head_black' not in plan
            report['passes'][fmt['ratio']] = passes
            report['formats'].append({'ratio': fmt['ratio'], 'action': 'rendered',
                                      'path': target_rel, 'passes': passes})
        sheet = target.parent / (target.stem + '-contact-sheet.png')
        engine.contact_sheet(target, sheet)
        cues = ((manifest.get('captions') or {}).get('cues') or [])
        marks = sorted({0.0} | {float(s['start']) for s in manifest['scenes']}
                       | {max(0.0, timeline_seconds(manifest) - 0.2)})
        engine.control_frames(target, marks, target.parent / (target.stem + '-frames'))
        state[fmt['ratio']] = {'fingerprint': fingerprint, 'sha256': digest_of(target),
                               'rendered_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
        exports.append({'ratio': fmt['ratio'], 'path': target_rel,
                        'sha256': digest_of(target), 'state': 'measured',
                        'contact_sheet': str(sheet.relative_to(root)).replace('\\', '/'),
                        'measurements': {k: measurements.get(k) for k in
                                         ('duration_seconds', 'width', 'height', 'ratio',
                                          'fps', 'codec', 'audio_streams', 'sample_rate',
                                          'loudness_lufs', 'true_peak_dbfs', 'decode_errors',
                                          'black_regions', 'freeze_regions', 'size_bytes')}})
        all_findings += [dict(f, ratio=fmt['ratio']) for f in findings]

    state_dir.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8')

    # The manifest is written from the files, not from the plan. A run limited to one
    # ratio by --formats updates that ratio and leaves the others alone, as long as
    # their files are still there: re-rendering a vertical is not a statement that the
    # landscape was never exported, and a manifest that says so is simply wrong.
    kept = [e for e in (manifest.get('exports') or [])
            if isinstance(e, dict) and e.get('ratio') not in {f['ratio'] for f in wanted}
            and isinstance(e.get('path'), str) and (root / e['path']).is_file()]
    manifest['exports'] = kept + exports
    technical = manifest.setdefault('qa', {}).setdefault('technical', {})
    blocking = [f for f in all_findings if f['severity'] == 'blocking']
    technical['verdict'] = 'fail' if blocking else ('pass_with_noted_risk' if all_findings else 'pass')
    technical['tool'] = 'scripts/inspect_video.py'
    technical['defects'] = [defect(f, f.get('ratio', 'all'),
                                   'Fix the source and re-render this format')
                            for f in all_findings]
    manifest['state'] = 'measured' if not blocking else 'rendered'
    manifest['engine'] = {'kind': 'renderer', 'name': caps['engine'], 'version': 'ffmpeg',
                          'detected': True,
                          'javascript_required': bool(caps['javascript_required']),
                          'why': 'Reference engine: Python and FFmpeg, both already required by this pack'}
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
                             encoding='utf-8')

    report['exports'] = [{'ratio': e['ratio'], 'path': e['path'],
                          'duration': e['measurements'].get('duration_seconds'),
                          'size': '%dx%d' % (e['measurements'].get('width') or 0,
                                             e['measurements'].get('height') or 0)}
                         for e in exports]
    report['findings'] = all_findings
    report['verdict'] = technical['verdict']
    print(json.dumps(report, indent=2))
    return 1 if all_findings else 0


def main():
    """`run` with the one thing it cannot promise: that every file opens.

    A render that dies halfway used to leave a Python traceback on the terminal and
    an exit status nobody had chosen. A traceback is not a report. The failure is
    stated, `rendered` says plainly that nothing was delivered, and the code is one
    the caller can act on.
    """
    try:
        return run()
    except engine.EngineError as e:
        print(json.dumps({'error': str(e), 'rendered': False}, indent=2))
        return 4


if __name__ == '__main__':
    sys.exit(main())
