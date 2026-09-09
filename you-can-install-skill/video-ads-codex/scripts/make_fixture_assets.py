"""Generate the synthetic assets the shipped render example points at.

Everything this writes is synthetic and says so in its own file name. It exists so
the example manifest renders on a bare machine with nothing but FFmpeg, and so the
engine's image, video, voice, music and effects paths are all exercised by something
real rather than described.

The voice file is a stand-in, not speech. It is named `voice-standin` for that
reason, and the example manifest records it as a fixture. A pack that let a tone be
called narration would be doing the exact thing it tells the assistant never to do.

    python scripts/make_fixture_assets.py --out fixtures
"""
import argparse, shutil, subprocess, sys
from pathlib import Path


def ff(args, label):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostdin', '-v', 'error'] + args,
                       capture_output=True, text=True, errors='replace')
    if r.returncode != 0:
        lines = [l for l in (r.stderr or '').splitlines() if l.strip()]
        raise SystemExit('%s failed: %s' % (label, lines[-1] if lines else r.returncode))


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    ff(['-f', 'lavfi', '-i', 'gradients=s=1200x1200:c0=0x1B2A38:c1=0xF5A623:'
        'x0=200:y0=200:x1=1000:y1=1000:d=1', '-frames:v', '1',
        '-y', str(out / 'product-still.png')], 'product still')
    ff(['-f', 'lavfi', '-i', 'gradients=s=1400x1400:c0=0x101820:c1=0x2A4A6A:d=6:r=25:speed=0.06',
        '-t', '6', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
        '-pix_fmt', 'yuv420p', '-y', str(out / 'texture-loop.mp4')], 'texture loop')
    # Speech-band bursts with gaps, so the ducking sidechain has something to key on
    # and the gaps are where the music has to come back up.
    ff(['-f', 'lavfi', '-i',
        'sine=frequency=190:duration=17,tremolo=f=5.5:d=0.85,'
        'volume=0.55,highpass=f=90,lowpass=f=3400',
        '-af', 'afade=t=in:st=0:d=0.05,afade=t=out:st=16.6:d=0.3',
        '-ar', '48000', '-ac', '1', '-y', str(out / 'voice-standin.wav')], 'voice stand-in')
    ff(['-f', 'lavfi', '-i',
        'aevalsrc=0.30*sin(2*PI*110*t)+0.18*sin(2*PI*165*t)+0.10*sin(2*PI*220*t):'
        'd=20:s=48000', '-ac', '2', '-y', str(out / 'music-bed.wav')], 'music bed')
    ff(['-f', 'lavfi', '-i', 'sine=frequency=1200:duration=0.25',
        '-af', 'afade=t=out:st=0.05:d=0.2,volume=0.6', '-ar', '48000', '-ac', '2',
        '-y', str(out / 'accent-hit.wav')], 'accent hit')
    return sorted(p.name for p in out.iterdir() if p.is_file())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', default='fixtures')
    a = p.parse_args()
    if not shutil.which('ffmpeg'):
        print('ffmpeg is not on PATH, so nothing was generated. This is not a pass.',
              file=sys.stderr)
        return 3
    written = build(Path(a.out))
    print('\n'.join(written))
    return 0


if __name__ == '__main__':
    sys.exit(main())
