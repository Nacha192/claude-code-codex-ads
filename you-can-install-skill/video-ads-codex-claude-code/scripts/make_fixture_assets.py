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
    # Every seed is pinned. `gradients` defaults to a random one, so without this the
    # fixture is a different film on every run and nothing downstream can be hashed.
    ff(['-f', 'lavfi', '-i', 'gradients=s=1200x1200:c0=0x1B2A38:c1=0xF5A623:'
        'x0=200:y0=200:x1=1000:y1=1000:d=1:seed=1201', '-frames:v', '1',
        '-y', str(out / 'product-still.png')], 'product still')
    ff(['-f', 'lavfi', '-i', 'gradients=s=1400x1400:c0=0x101820:c1=0x2A4A6A:d=6:r=25:speed=0.06:seed=1402',
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

    # The second art direction. One engine, one manifest schema, a palette and a type
    # scale that are the opposite of the first: light ground, dark ink, a cold accent,
    # a static camera. If the look were in the code rather than in the design block,
    # these two would come out looking like each other, which is the whole point of
    # shipping a second one.
    ff(['-f', 'lavfi', '-i', 'gradients=s=1600x1600:c0=0xEDE7DC:c1=0xCFC4B4:'
        'x0=100:y0=1500:x1=1500:y1=100:d=8:r=25:speed=0.03:seed=2101',
        '-t', '8', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
        '-pix_fmt', 'yuv420p', '-y', str(out / 'plate-linen.mp4')], 'linen plate')
    # Hard geometry, not a gradient. A blur is only visible against something that has
    # edges, so the plane meant to stay sharp is given edges to keep.
    boxes = ','.join(
        'drawbox=x=%d:y=%d:w=%d:h=%d:color=%s:t=fill' % b for b in (
            (80, 90, 900, 26, '0x6E1A24'), (80, 150, 520, 26, '0x1B1B1B'),
            (80, 300, 1040, 8, '0x1B1B1B'), (80, 380, 300, 300, '0x6E1A24'),
            (430, 380, 690, 300, '0x1B1B1B'), (80, 740, 1040, 8, '0x1B1B1B'),
            (80, 800, 700, 26, '0x1B1B1B'), (80, 860, 420, 26, '0x6E1A24')))
    ff(['-f', 'lavfi', '-i', 'color=c=0xF4F0E8:s=1200x1000',
        '-vf', boxes, '-frames:v', '1', '-y', str(out / 'object-still.png')],
       'object still')
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
