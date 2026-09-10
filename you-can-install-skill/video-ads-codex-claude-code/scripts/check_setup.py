"""What this machine can actually do, checked once before the first job.

There are three answers here and never a fourth: **present**, **missing**, and
**cannot be checked from a script**. The last one is the honest answer for a connected
tool, an account, a credit balance or a website login, and a pack that pretends
otherwise is promising a capability it does not have. Those are listed by name so the
assistant checks them in the session, where they can actually be seen.

Nothing here installs anything. Installing software changes the user's machine, and a
skill has no standing authorization to do that. This prints the exact command for the
operating system it is running on, and stops.

    python scripts/check_setup.py            # for a person
    python scripts/check_setup.py --json     # for the assistant
    python scripts/check_setup.py --json --write .ads-brain/setup.json

Exit codes: 0 everything the scripts need is here, 1 something is missing and is
named, 2 the arguments were wrong.
"""
import argparse, importlib.util, json, os, platform, shutil, subprocess, sys
from pathlib import Path

MIN_PYTHON = (3, 10)
HERE = Path(__file__).resolve().parent

INSTALL = {
    'ffmpeg': {
        'Windows': 'winget install -e --id Gyan.FFmpeg',
        'Darwin': 'brew install ffmpeg',
        'Linux': 'sudo apt update && sudo apt install ffmpeg',
        'note': ("Take the full build. A minimal one encodes video and cannot draw "
                 "text: Homebrew's macOS bottle ships without libfreetype, so "
                 "`drawtext` and `subtitles` do not exist and an ad renders with none "
                 "of the words in it."),
    },
    'python': {
        'Windows': 'winget install -e --id Python.Python.3.12',
        'Darwin': 'brew install python@3.12',
        'Linux': 'sudo apt update && sudo apt install python3',
        'note': ("A command with `sudo` asks for a password, which a non-interactive "
                 "shell cannot answer. Hand it to the user rather than launching it."),
    },
    'fonts': {
        'Windows': 'Fonts are already present on Windows.',
        'Darwin': 'Fonts are already present on macOS.',
        'Linux': 'sudo apt install fonts-inter fonts-dejavu-core',
        'note': 'The engine needs one usable face, not a particular one.',
    },
}

# A script can see a binary on PATH. It cannot see whether an account has credits, a
# connector is authorised, or a site is logged in. These are checked in the session.
IN_SESSION = [
    {'name': 'Image generation',
     'why': 'Still ads, and the image layers of a video',
     'how': 'Look for a connected image tool in this session before promising a visual'},
    {'name': 'Speech provider',
     'why': 'Narration, and cloning the user own voice with a consent record',
     'how': 'Without one the film carries on-screen copy and no voice, and says so'},
    {'name': 'Video model',
     'why': 'Generated shots',
     'how': 'Optional. The supplied engine composes stills, type and footage you give it'},
    {'name': 'Meta Ad Library',
     'why': 'Real competitor observations rather than recollection',
     'how': 'Public browser access is enough; no API key is required to read it'},
    {'name': 'Meta Marketing API or MCP',
     'why': 'Account data and authorised campaign operations',
     'how': 'Never needed to make the creative. Only to read or write the account'},
]


def python_state():
    version = '%d.%d.%d' % sys.version_info[:3]
    ok = sys.version_info[:2] >= MIN_PYTHON
    return {'status': 'ok' if ok else 'too_old', 'version': version,
            'command': sys.executable,
            'need': '%d.%d or newer' % MIN_PYTHON}


def engine_module():
    """The motion engine, when this is a video pack. Still packs do not ship it."""
    path = HERE / 'motion_engine.py'
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location('motion_engine', path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:                      # a broken copy is a finding, not a crash
        return {'error': str(e)}
    return module


def render_state():
    module = engine_module()
    if module is None:
        return {'status': 'not_needed',
                'why': 'This is a still-creative pack; it renders no video'}
    if isinstance(module, dict):
        return {'status': 'broken', 'why': module['error']}
    caps = module.detect()
    out = {'status': 'ok' if caps.get('usable') else 'missing',
           'ffmpeg': caps.get('ffmpeg'), 'ffprobe': caps.get('ffprobe'),
           'freetype': caps.get('freetype'),
           'missing_filters': caps.get('missing_filters') or [],
           'encoders': caps.get('encoders') or {},
           'fonts': caps.get('fonts'), 'font_file': caps.get('font_file')}
    if not caps.get('usable'):
        out['why'] = caps.get('reason', 'unknown')
    return out


def ffmpeg_version():
    if not shutil.which('ffmpeg'):
        return None
    try:
        p = subprocess.run(['ffmpeg', '-hide_banner', '-version'], capture_output=True,
                           text=True, timeout=30, errors='replace')
        return (p.stdout or '').splitlines()[0] if p.stdout else None
    except (OSError, subprocess.SubprocessError):
        return None


def report():
    system = platform.system()
    out = {'schema_v': '1.0.0', 'system': system,
           'python': python_state(), 'render': render_state(),
           'ffmpeg_version': ffmpeg_version(),
           'cannot_be_checked_from_a_script': IN_SESSION, 'missing': [], 'install': {}}
    if out['python']['status'] != 'ok':
        out['missing'].append('python')
    render = out['render']
    if render['status'] == 'missing':
        out['missing'].append('ffmpeg' if not render.get('ffmpeg') or
                              render.get('missing_filters') or not render.get('freetype')
                              else 'render')
        if render.get('fonts') == 0:
            out['missing'].append('fonts')
    for name in out['missing']:
        block = INSTALL.get(name)
        if block:
            out['install'][name] = {'command': block.get(system, block.get('Linux')),
                                    'note': block['note']}
    out['verdict'] = ('ready' if not out['missing'] else
                      'blocked' if 'python' in out['missing'] else 'partial')
    return out


def human(data):
    lines = ['Setup check on %s' % data['system'], '']
    p = data['python']
    lines.append('  Python      %s  %s (needs %s)' % (
        'ok     ' if p['status'] == 'ok' else 'TOO OLD', p['version'], p['need']))
    r = data['render']
    if r['status'] == 'not_needed':
        lines.append('  Rendering   n/a      still-creative pack, nothing to render')
    elif r['status'] == 'ok':
        lines.append('  Rendering   ok       %s, %d fonts' % (
            (data.get('ffmpeg_version') or 'ffmpeg').split(' Copyright')[0], r.get('fonts') or 0))
    else:
        lines.append('  Rendering   MISSING  %s' % r.get('why', 'unknown'))
    lines.append('')
    if data['missing']:
        lines.append('Missing, and the command that fixes it. Ask before running any of them:')
        for name in data['missing']:
            block = data['install'].get(name)
            if block:
                lines.append('  %-8s %s' % (name, block['command']))
                lines.append('           %s' % block['note'])
        lines.append('')
    lines.append('Not checkable from a script. Look for these in the session instead:')
    for item in data['cannot_be_checked_from_a_script']:
        lines.append('  %-24s %s' % (item['name'], item['why']))
        lines.append('  %-24s %s' % ('', item['how']))
    lines.append('')
    lines.append('Verdict: %s' % data['verdict'])
    if data['verdict'] == 'partial':
        lines.append('Everything that does not need the missing part still works, and the')
        lines.append('job says plainly what did not run rather than pretending it did.')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--json', action='store_true', help='machine-readable report')
    ap.add_argument('--write', help='also write the report to this path')
    a = ap.parse_args()
    data = report()
    print(json.dumps(data, indent=2) if a.json else human(data))
    if a.write:
        target = Path(a.write)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    return 0 if not data['missing'] else 1


if __name__ == '__main__':
    sys.exit(main())
