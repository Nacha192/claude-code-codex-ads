"""The reference motion engine: a real, runnable one, built on Python and FFmpeg.

This exists because a pack that can design and judge a video and cannot make one
sends the assistant looking for a renderer, and it finds whatever is nearest. That
is how every ad ends up a slideshow, or how a JavaScript toolchain becomes a
requirement nobody agreed to.

So the reference engine is the two things the packs already require: an interpreter
and FFmpeg. No package to install, no Node, no browser. **JavaScript is never
mandatory.** Remotion, After Effects, Blender and the rest stay first-class through
the adapter contract in `providers.md`; this one is the floor, not the ceiling.

What it draws, per format and per scene: gradient and solid grounds, image and video
layers with cover fitting, animated typography on a real type scale, shapes, camera
push and pull, parallax between planes, transitions, burned captions from the final
take, and an audio graph with music ducked under the voice and a declared loudness
target.

Every measurement it claims comes back out of `inspect_video.py`, never out of this
file. The engine renders; something else checks. That separation is the whole point.
"""
import hashlib, json, math, os, re, shutil, subprocess, sys
from pathlib import Path

BS = chr(92)
TIMEOUT = 1800
# Filters the reference pipeline actually issues. Checked before rendering, because
# a build without one of these produces a confusing failure halfway through a job.
REQUIRED_FILTERS = ['color', 'gradients', 'drawtext', 'drawbox', 'overlay', 'zoompan',
                    'scale', 'crop', 'format', 'fps', 'xfade', 'subtitles', 'tile',
                    'amix', 'sidechaincompress', 'loudnorm', 'afade', 'adelay',
                    'anullsrc', 'atrim', 'asplit', 'concat', 'tpad', 'asetnsamples', 'gblur']
# Ordered by preference. The first family whose file is found wins, so the look is
# stable on a machine that has the brand face and degrades to a known fallback.
FONT_PREFERENCE = ['Inter', 'Poppins', 'Montserrat', 'Helvetica', 'Arial',
                   'Liberation Sans', 'DejaVu Sans', 'Noto Sans']
FONT_DIRS = ['C:/Windows/Fonts', os.path.expanduser('~/AppData/Local/Microsoft/Windows/Fonts'),
             '/usr/share/fonts', '/usr/local/share/fonts', os.path.expanduser('~/.fonts'),
             '/System/Library/Fonts', '/System/Library/Fonts/Supplemental', '/Library/Fonts']
DEFAULT_DESIGN = {
    'palette': {'ink': '0x101820', 'paper': '0xF5F0E8', 'accent': '0xF5A623',
                'muted': '0x8A97A3', 'support': '0x2A4A6A'},
    'type': {'family_preference': FONT_PREFERENCE,
             # Fractions of the frame height, so type scales with the format instead
             # of being re-specified per ratio and drifting between them.
             'scale': {'display': 0.075, 'title': 0.050, 'body': 0.030, 'caption': 0.034}},
    'motion': {'enter_seconds': 0.45, 'ease': 'ease_out', 'camera_amount': 0.10},
    'grid': {'margin': 0.075, 'safe_top': 0.10, 'safe_bottom': 0.16}}


class EngineError(RuntimeError):
    """Something the engine cannot do. Raised instead of rendering a wrong file."""


# --------------------------------------------------------------------------- shell

def run(cmd, timeout=TIMEOUT):
    """Run a tool. Returns (code, stdout, stderr) and never raises on tool failure."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           encoding='utf-8', errors='replace')
        return p.returncode, p.stdout or '', p.stderr or ''
    except subprocess.TimeoutExpired:
        return 124, '', 'timed out after %ds' % timeout
    except OSError as e:
        return 125, '', str(e)


def ffmpeg(args, label):
    """Run ffmpeg and turn a failure into a message that names what was being made."""
    code, _, err = run(['ffmpeg', '-hide_banner', '-nostdin', '-v', 'error'] + args)
    if code != 0:
        lines = [l for l in err.strip().splitlines() if l.strip()]
        raise EngineError('%s failed (ffmpeg exit %d): %s'
                          % (label, code, lines[-1] if lines else 'no message'))


# ------------------------------------------------------------------- capabilities

def find_fonts():
    """Every usable face on this machine, by lowercased file stem."""
    found = {}
    for directory in FONT_DIRS:
        base = Path(directory)
        if not base.is_dir():
            continue
        try:
            entries = list(base.rglob('*'))
        except OSError:
            continue
        for f in entries:
            if f.is_file() and f.suffix.lower() in ('.ttf', '.otf', '.ttc'):
                found.setdefault(f.stem.lower(), str(f))
    return found


def pick_font(preference, fonts, bold=True):
    """The first preferred family present, then any face, then nothing.

    Returns None rather than a guess when the machine has no font at all: text that
    silently does not render is worse than a job that stops and says why.
    """
    for family in list(preference or []) + FONT_PREFERENCE:
        key = family.lower().replace(' ', '')
        for suffix in (['bold', 'bd', '-bold', 'semibold'] if bold else ['regular', '', '-regular']):
            for stem, path in sorted(fonts.items()):
                if stem.replace(' ', '').replace('_', '') == key + suffix:
                    return path
        for stem, path in sorted(fonts.items()):
            if stem.replace(' ', '').replace('_', '').startswith(key):
                return path
    return sorted(fonts.values())[0] if fonts else None


def detect():
    """What this machine can actually do, read rather than assumed."""
    caps = {'ffmpeg': shutil.which('ffmpeg'), 'ffprobe': shutil.which('ffprobe'),
            'filters': [], 'missing_filters': [], 'encoders': {}, 'freetype': False,
            'fonts': 0, 'font_file': None, 'engine': 'ffmpeg-python-reference',
            'javascript_required': False}
    if not caps['ffmpeg'] or not caps['ffprobe']:
        caps['usable'] = False
        caps['reason'] = 'ffmpeg and ffprobe must both be on PATH'
        return caps
    _, out, _ = run(['ffmpeg', '-hide_banner', '-filters'])
    names = {line.split()[1] for line in out.splitlines()
             if len(line.split()) > 2 and not line.startswith('Filters')}
    caps['filters'] = sorted(names)
    caps['missing_filters'] = [f for f in REQUIRED_FILTERS if f not in names]
    _, enc, _ = run(['ffmpeg', '-hide_banner', '-encoders'])
    caps['encoders'] = {'libx264': 'libx264' in enc, 'aac': bool(re.search(r'\baac\b', enc))}
    _, ver, _ = run(['ffmpeg', '-hide_banner', '-version'])
    caps['freetype'] = 'freetype' in ver
    fonts = find_fonts()
    caps['fonts'] = len(fonts)
    caps['font_file'] = pick_font(FONT_PREFERENCE, fonts)
    caps['usable'] = (not caps['missing_filters'] and caps['encoders']['libx264']
                      and caps['encoders']['aac'] and caps['freetype']
                      and caps['font_file'] is not None)
    if not caps['usable']:
        why = []
        if caps['missing_filters']:
            why.append('missing filters: ' + ', '.join(caps['missing_filters']))
        if not caps['encoders']['libx264']:
            why.append('no libx264 encoder')
        if not caps['encoders']['aac']:
            why.append('no aac encoder')
        if not caps['freetype']:
            why.append('ffmpeg built without libfreetype, so no text can be drawn')
        if caps['font_file'] is None:
            why.append('no usable font file found on this machine')
        caps['reason'] = '; '.join(why)
    return caps


# ------------------------------------------------------------------------ escaping

def filter_path(p):
    """A path inside a filtergraph: forward slashes, and the drive colon escaped."""
    return str(p).replace(BS, '/').replace(':', BS + ':')


def expr(e):
    """An expression inside a filter option. Only the commas need escaping."""
    return e.replace(',', BS + ',')


def text_file(work, key, content):
    """Copy text to a file and point drawtext at it.

    `text=` has to survive the filtergraph parser, the option parser and drawtext's
    own expansion, three levels with different rules, and a price or an apostrophe
    breaks it. `textfile=` with expansion off has none of that: the bytes arrive as
    written. This is why no copy in this engine is ever escaped by hand.
    """
    path = work / ('text-%s.txt' % key)
    path.write_text(content, encoding='utf-8')
    return path


# -------------------------------------------------------------------------- design

def resolve_design(manifest):
    """Brand tokens over defaults, one level deep, so a brand may set only a colour."""
    design = json.loads(json.dumps(DEFAULT_DESIGN))
    given = manifest.get('design') or {}
    if not isinstance(given, dict):
        raise EngineError('design must be an object')
    for section, value in given.items():
        if isinstance(value, dict) and isinstance(design.get(section), dict):
            merged = dict(design[section])
            for k, v in value.items():
                if isinstance(v, dict) and isinstance(merged.get(k), dict):
                    inner = dict(merged[k]); inner.update(v); merged[k] = inner
                else:
                    merged[k] = v
            design[section] = merged
        else:
            design[section] = value
    return design


def colour(design, name, default='0xFFFFFF'):
    """A palette name, or a literal 0xRRGGBB passed straight through."""
    if isinstance(name, str) and name.startswith('0x'):
        return name
    return design['palette'].get(name, default)


def layout_for(fmt, design):
    """A composition per ratio, computed from the frame, not cropped from another.

    Portrait, square-ish and landscape are three different arrangements: where the
    media sits, where the type block starts, how large the display size is, and how
    much room the platform's own interface will steal. A vertical produced by
    cropping a horizontal is the failure this function exists to make impossible,
    because there is no master frame to crop from.
    """
    w, h = int(fmt['width']), int(fmt['height'])
    grid = design['grid']
    # The format's own safe zones win over the project grid. A vertical loses a fifth
    # of its height to the platform's interface and a feed square loses almost none,
    # so one pair of numbers for three ratios is a crop decision wearing a grid's
    # clothes. The manifest has always declared these per format; reading only the
    # grid meant the strictest ratio's reserve was applied to all three, and the
    # landscape lost a tenth of its frame to an interface that is not there.
    zones = fmt.get('safe_zones') or {}

    def zone(name, fallback):
        value = zones.get(name)
        return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool)             else float(grid[fallback])

    left = zone('left', 'margin')
    right = zone('right', 'margin')
    margin = int(w * left)
    margin_right = int(w * right)
    safe_top = int(h * zone('top', 'safe_top'))
    safe_bottom = int(h * zone('bottom', 'safe_bottom'))
    aspect = w / float(h)
    given = fmt.get('layout') or {}
    align = 'top'
    if aspect <= 0.7:
        shape = 'portrait'
        # The media takes the upper two fifths, not the upper half. A vertical loses
        # roughly a fifth of its height to the platform's own interface and another
        # slice to burned captions, so a media panel sized by eye leaves the copy a
        # column too shallow to hold a headline, and the type has to shrink to fit.
        media = {'x': 0, 'y': 0, 'w': w, 'h': int(h * 0.42)}
        text_x, text_top, text_w = margin, int(h * 0.46), w - margin - margin_right
        scale = 1.0
    elif aspect < 1.2:
        shape = 'square'
        media = {'x': 0, 'y': 0, 'w': w, 'h': int(h * 0.44)}
        text_x, text_top, text_w = margin, int(h * 0.48), w - margin - margin_right
        scale = 0.92
    else:
        shape = 'landscape'
        # Two columns. The type owns the left, the media owns the right, which is a
        # different composition from the portrait rather than the same one squeezed.
        media = {'x': int(w * 0.48), 'y': 0, 'w': int(w * 0.52), 'h': h}
        text_x, text_top, text_w = margin, safe_top + int(h * 0.08), int(w * 0.42) - margin
        scale = 1.25
        # The copy is centred in its column here and top-aligned in the verticals.
        # A left column top-aligned against a full-height picture reads as unfinished,
        # and this is precisely the sort of decision a crop of a master cannot make.
        align = 'center'
    sizes = {role: max(12, int(h * float(v) * scale))
             for role, v in design['type']['scale'].items()}
    # The band captions own, and the line below which copy may not go. Without this
    # the burned captions land on top of the body copy: both are legible on their
    # own and unreadable together, which is the defect a contact sheet shows in one
    # glance and a duration check never will.
    caption_band = int(sizes.get('caption', 34) * 2.4)
    copy_bottom = h - safe_bottom - caption_band
    out = {'shape': shape, 'width': w, 'height': h, 'margin': margin,
           'margin_right': margin_right,
           'safe_top': safe_top, 'safe_bottom': safe_bottom, 'media': media,
           'text_x': text_x, 'text_top': text_top, 'text_width': text_w,
           'type_scale': scale, 'caption_band': caption_band, 'stack_align': align,
           'copy_bottom': copy_bottom, 'sizes': sizes}
    for key, value in given.items():
        out[key] = value
    return out


# ---------------------------------------------------------------------- primitives

EASINGS = {
    # p is normalised progress, already clamped by the caller.
    'linear': '(P)',
    'ease_out': '(1-pow(1-(P),3))',
    'ease_in': '(pow((P),3))',
    'ease_in_out': '(if(lt((P),0.5),4*pow((P),3),1-pow(-2*(P)+2,3)/2))'}


def progress(start, seconds):
    """Clamped 0..1 progress expression starting at `start`, over `seconds`."""
    seconds = max(0.001, float(seconds))
    return 'min(1,max(0,(t-%.3f)/%.3f))' % (float(start), seconds)


def eased(start, seconds, ease='ease_out'):
    return EASINGS.get(ease, EASINGS['ease_out']).replace('P', progress(start, seconds))


def interpolate(a, b, start, seconds, ease='ease_out'):
    """An expression moving from a to b, eased."""
    return '%.3f+(%.3f)*%s' % (float(a), float(b) - float(a), eased(start, seconds, ease))


def camera_zoom(kind, amount, frames):
    """A zoompan z expression. Push adds pressure, pull gives context."""
    amount = max(0.0, float(amount))
    frames = max(1, int(frames))
    if kind == 'pull':
        return 'max(1,%.4f-%.6f*on)' % (1 + amount, amount / frames)
    if kind == 'push':
        return 'min(%.4f,1+%.6f*on)' % (1 + amount, amount / frames)
    return '1'


# ------------------------------------------------------------------- scene drawing

def stable_seed(key):
    """A repeatable seed from a name, so a rerun is a rerun and not a new draw.

    Python's own hash is salted per process, so it is exactly the wrong tool here:
    it would give the same scene a different gradient every time the script starts.
    """
    digest = hashlib.sha256(str(key).encode('utf-8')).digest()
    return int.from_bytes(digest[:4], 'big')


def scene_inputs(scene, assets, seconds, fps, layout):
    """ffmpeg inputs for this scene, and the filter chain fragments that place them."""
    args, chains, last = [], [], None
    background = scene.get('background') or {}
    w, h = layout['width'], layout['height']
    if background.get('kind') == 'gradient':
        # `gradients` defaults to seed=-1, which is a new random gradient on every
        # run. Two renders of the same manifest then differ in every byte, and a
        # hash in the manifest stops meaning anything. The seed comes from the scene
        # so scenes still differ from each other while each one is repeatable, and
        # the manifest can pin its own if a particular gradient is the one wanted.
        seed = background.get('seed')
        if not isinstance(seed, int) or isinstance(seed, bool):
            seed = stable_seed(scene.get('id', 'scene'))
        args += ['-f', 'lavfi', '-i',
                 'gradients=s=%dx%d:c0=%s:c1=%s:d=%.3f:r=%d:speed=0.02:seed=%d'
                 % (w, h, background.get('from', '0x101820'),
                    background.get('to', '0x2A4A6A'), seconds, fps, seed)]
    else:
        args += ['-f', 'lavfi', '-i', 'color=c=%s:s=%dx%d:d=%.3f:r=%d'
                 % (background.get('colour', '0x101820'), w, h, seconds, fps)]
    chains.append('[0:v]format=rgba,fps=%d[bg]' % fps)
    last = 'bg'
    return args, chains, last


def media_layer(index, layer, layout, seconds, fps, chains, last, assets):
    """An image or video placed in this format's media region, cover-fitted.

    Cover rather than fit: letterboxing inside a composition looks like a mistake,
    and stretching looks worse. The region differs per ratio, which is what makes
    this a composition and not a crop.
    """
    region = dict(layout['media'])
    for key in ('x', 'y', 'w', 'h'):
        if key in layer:
            region[key] = int(float(layer[key]) * (layout['width'] if key in 'xw' else layout['height']))
    rw, rh = max(2, region['w']), max(2, region['h'])
    amount = float(layer.get('camera_amount', 0.10))
    kind = layer.get('camera', 'none')
    frames = max(1, int(math.ceil(seconds * fps)))
    # Oversample before the camera move so the push never samples above native size.
    over = 1.0 + (amount if kind in ('push', 'pull') else 0.0)
    sw, sh = int(rw * over) + 2, int(rh * over) + 2
    label = 'm%d' % index
    chain = ('[%d:v]scale=%d:%d:force_original_aspect_ratio=increase,'
             'crop=%d:%d,setsar=1' % (index, sw, sh, sw, sh))
    # Depth, cheaply and honestly: a plane behind the subject is softened so the eye
    # is told where to look. Sigma is a fraction of the frame height, not a pixel
    # count, so one manifest reads the same at 1080 and at 1920 instead of being
    # re-tuned per ratio. It is applied before the camera move, because a lens blurs
    # the plane and the camera then travels through it, not the other way round.
    #
    # This is a fixed focus. `gblur` takes a number, not an expression, so a rack
    # focus that pulls during the shot is not available here and is not pretended at.
    softness = float(layer.get('blur', 0.0) or 0.0)
    if softness > 0:
        chain += ',gblur=sigma=%.2f' % max(0.1, min(120.0, softness * layout['height']))
    if kind in ('push', 'pull'):
        chain += (",zoompan=z='%s':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                  "d=%d:s=%dx%d:fps=%d" % (expr(camera_zoom(kind, amount, frames)),
                                           frames, rw, rh, fps))
    else:
        chain += ',scale=%d:%d,fps=%d' % (rw, rh, fps)
    chains.append(chain + '[%s]' % label)
    # Parallax: a plane that drifts slower than the one in front of it.
    drift = float(layer.get('parallax', 0.0))
    x_expr = str(region['x']) if not drift else expr('%d+%.2f*sin(t*0.6)' % (region['x'], drift * layout['width']))
    out = 'l%d' % index
    chains.append("[%s][%s]overlay=x='%s':y=%d:eval=frame:shortest=1[%s]"
                  % (last, label, x_expr, region['y'], out))
    return out


# ------------------------------------------------------------------ font metrics

# Line breaking used to divide the column by an assumed average character width. It
# is the sort of approximation that looks harmless and is not: the assumption was
# tuned on one machine's Arial, and DejaVu on a Linux runner is wider, so the same
# manifest wrapped at a different word and the layout was measured against a width
# nothing on screen had. The advance widths are in the font file. They are read.
#
# Kerning is deliberately not applied, because `drawtext` does not apply it either.
# Matching the renderer matters more here than matching a typesetter.
FONT_METRICS = {}


def _u16(data, at):
    return int.from_bytes(data[at:at + 2], 'big')


def _u32(data, at):
    return int.from_bytes(data[at:at + 4], 'big')


def _tables(data, index=0):
    """Table directory of a TTF, OTF, or one face of a collection."""
    base = 0
    if data[:4] == b'ttcf':
        count = _u32(data, 8)
        index = min(index, max(0, count - 1))
        base = _u32(data, 12 + 4 * index)
    out = {}
    for i in range(_u16(data, base + 4)):
        record = base + 12 + 16 * i
        out[data[record:record + 4]] = (_u32(data, record + 8), _u32(data, record + 12))
    return out


def _cmap(data, offset):
    """Codepoint to glyph id, from the most complete Unicode subtable present."""
    rank = {(3, 10): 5, (0, 4): 5, (0, 6): 5, (3, 1): 4, (0, 3): 4,
            (0, 2): 3, (0, 1): 3, (0, 0): 3}
    best = None
    for i in range(_u16(data, offset + 2)):
        record = offset + 4 + 8 * i
        key = (_u16(data, record), _u16(data, record + 2))
        score = rank.get(key, 1)
        if best is None or score > best[0]:
            best = (score, offset + _u32(data, record + 4))
    if best is None:
        return {}
    sub = best[1]
    kind = _u16(data, sub)
    table = {}
    if kind == 4:
        segments = _u16(data, sub + 6) // 2
        ends = sub + 14
        starts = ends + 2 * segments + 2
        deltas = starts + 2 * segments
        ranges = deltas + 2 * segments
        for s in range(segments):
            end = _u16(data, ends + 2 * s)
            start = _u16(data, starts + 2 * s)
            delta = _u16(data, deltas + 2 * s)
            range_offset = _u16(data, ranges + 2 * s)
            if start > end or end == 0xFFFF and start == 0xFFFF:
                continue
            for cp in range(start, min(end, 0xFFFE) + 1):
                if range_offset == 0:
                    gid = (cp + delta) & 0xFFFF
                else:
                    at = ranges + 2 * s + range_offset + 2 * (cp - start)
                    if at + 2 > len(data):
                        continue
                    gid = _u16(data, at)
                    if gid:
                        gid = (gid + delta) & 0xFFFF
                if gid:
                    table.setdefault(cp, gid)
    elif kind == 12:
        for g in range(_u32(data, sub + 12)):
            group = sub + 16 + 12 * g
            start, end = _u32(data, group), _u32(data, group + 4)
            first = _u32(data, group + 8)
            if end - start > 0x10000:
                end = start + 0x10000
            for cp in range(start, end + 1):
                table.setdefault(cp, first + cp - start)
    elif kind == 6:
        first, count = _u16(data, sub + 6), _u16(data, sub + 8)
        for n in range(count):
            table.setdefault(first + n, _u16(data, sub + 10 + 2 * n))
    return table


def font_metrics(path):
    """Units per em, advance widths by glyph, and the character map. Cached.

    Returns None when the file is not a font this can read, so the caller falls back
    rather than raising: an unusual face is a reason to estimate, not to stop.
    """
    key = str(path)
    if key in FONT_METRICS:
        return FONT_METRICS[key]
    metrics = None
    try:
        data = Path(path).read_bytes()
        tables = _tables(data)
        head, hhea, hmtx, cmap = (tables.get(t) for t in (b'head', b'hhea', b'hmtx', b'cmap'))
        if head and hhea and hmtx and cmap:
            units = _u16(data, head[0] + 18)
            count = _u16(data, hhea[0] + 34)
            if units > 0 and count > 0:
                advances = [_u16(data, hmtx[0] + 4 * i)
                            for i in range(min(count, hmtx[1] // 4))]
                if advances:
                    metrics = {'units': units, 'advances': advances,
                               'last': advances[-1], 'cmap': _cmap(data, cmap[0])}
    except (OSError, ValueError, IndexError, KeyError):
        metrics = None
    FONT_METRICS[key] = metrics
    return metrics


def measure_text(content, size, font):
    """Width in pixels of one line, at this size, in this face.

    None when the face cannot be read, which is the signal to estimate instead.
    """
    metrics = font_metrics(font) if font else None
    if not metrics:
        return None
    advances, cmap, units = metrics['advances'], metrics['cmap'], metrics['units']
    total = 0
    for ch in str(content):
        gid = cmap.get(ord(ch))
        if gid is None:
            gid = cmap.get(ord('?'), 0)
        total += advances[gid] if gid < len(advances) else metrics['last']
    return total * float(size) / units


ESTIMATED_EM = 0.52


def wrap_text(content, max_px, size, font=None):
    """Break a line to the column width, because drawtext will not.

    ffmpeg draws exactly what it is given and lets it run off the frame, which is
    how a subtitle-length sentence ends up with its last two words outside the
    picture.

    The width comes out of the font file when the face can be read, so a line breaks
    where it actually reaches the column. Falling back to an average character width
    is what this used to do always, and it was wrong in a way that only showed on
    someone else's machine: the average was tuned on one Arial, DejaVu on a Linux
    runner is wider, so the same manifest broke at a different word and the layout
    was measured against a width nothing on screen ever had.
    """
    metrics = font_metrics(font) if font else None
    lines, current = [], ''

    def fits(candidate):
        if metrics:
            return measure_text(candidate, size, font) <= max_px
        return len(candidate) <= max(8, int(max_px / max(1.0, size * ESTIMATED_EM)))

    for word in str(content).split():
        candidate = (current + ' ' + word).strip()
        if fits(candidate) or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return '\n'.join(lines)


def stack_items(scene, layout, sizes, design):
    """Measure every stacked block of a scene before a single one is placed.

    Measuring first is the whole point. Placing block by block and clamping each one
    to the bottom of the column looks like a safety net and is not: two blocks that
    both hit the clamp are given the same position, so the guard against overlap is
    what causes the overlap. Nothing here draws; it only returns heights.
    """
    items = []
    for n, layer in enumerate(scene.get('layers') or []):
        kind = layer.get('kind')
        if kind == 'text':
            content = str(layer.get('content', '')).strip()
            if not content or 'y' in layer:
                continue
            role = layer.get('role', 'body')
            size = int(layer.get('size_px') or sizes.get(role, sizes['body']))
            wrapped = wrap_text(content, layout['text_width'], size, layout.get('font'))
            lines = wrapped.count('\n') + 1
            # The same leading the drawing uses. It used to be a hard 1.25 here and
            # whatever the font's glyph box happened to be over there, which measured
            # 2.50 em: a wrapped block was written over by the one under it.
            items.append({'index': n, 'kind': 'text', 'size': size, 'content': wrapped,
                          'lead': int(size * float(layer.get('gap', 0.35))),
                          'height': int(size * leading_of(design) * lines),
                          'trail': 0})
        elif kind == 'shape':
            if 'y' in layer:
                continue
            lead = int(layout['height'] * float(layer.get('gap', 0.014)))
            items.append({'index': n, 'kind': 'shape', 'lead': lead, 'trail': lead,
                          'height': max(2, int(float(layer.get('h', 0.006))
                                               * layout['height']))})
    total = sum(i['lead'] + i['height'] + i['trail'] for i in items)
    return items, total


MIN_TYPE_FIT = 0.55


def fit_layout(layout, design, scenes, font=None):
    """Shrink the type until the tallest scene fits its column, once for the film.

    Per-scene fitting would give the same role a different size in every scene, which
    is not a type scale any more. So the tightest scene sets the scale and the rest
    follow it, exactly as a designer would size a set of frames together.
    """
    layout = dict(layout)
    if font:
        layout['font'] = font
    room = max(1, layout['copy_bottom'] - layout['text_top'])
    scale, sizes = 1.0, dict(layout['sizes'])
    worst = 0
    for _ in range(8):
        # Captions are not part of the copy column and never shrink with it. They
        # live in their own band, sized for reading on a phone at arm's length, and
        # a headline that runs long is no reason to make the subtitles smaller.
        sizes = {role: (base if role == 'caption' else max(12, int(round(base * scale))))
                 for role, base in layout['sizes'].items()}
        worst = max([stack_items(s, layout, sizes, design)[1] for s in scenes] or [0])
        if worst <= room or scale <= MIN_TYPE_FIT:
            break
        scale = max(MIN_TYPE_FIT, scale * (room / float(worst)) * 0.98)
    if worst > room:
        raise EngineError(
            'at %dx%d the copy needs %dpx and the column has %dpx, even at the '
            'smallest type this layout allows. Cut a line rather than let the '
            'renderer decide what to hide.' % (layout['width'], layout['height'],
                                               worst, room))
    out = dict(layout)
    out['sizes'] = sizes
    out['fit_scale'] = round(scale, 4)
    return out


def place_stack(scene, layout, design):
    """Where each stacked layer of this scene goes, top of the column downward."""
    items, total = stack_items(scene, layout, layout['sizes'], design)
    cursor = layout['text_top']
    if layout.get('stack_align') == 'center':
        room = layout['copy_bottom'] - layout['text_top']
        cursor += max(0, (room - total) // 2)
    placed = {}
    for item in items:
        y = cursor + item['lead']
        placed[item['index']] = dict(item, y=y)
        cursor = y + item['height'] + item['trail']
    return placed


LEADING = 1.25


def leading_of(design):
    """Line height as a brand token, not as a property of the font binary.

    `drawtext` advances multi-line text by the font's own maximum glyph height plus
    `line_spacing`. Measured on this machine that is 2.50 em where the layout had
    assumed 1.25, so a wrapped block was twice the height it had been measured at and
    the copy underneath was written over. It is not a constant to correct either: it
    comes out of the font file and the ffmpeg build, so it differs per machine.

    Every line is drawn on its own now, at a y this engine computes. The leading is a
    number the manifest sets, the measurement is right by construction, and a brand
    that wants tight display type and airy body copy can say so.
    """
    value = (design.get('type') or {}).get('leading')
    try:
        value = float(value)
    except (TypeError, ValueError):
        return LEADING
    return value if 0.8 <= value <= 3.0 else LEADING


def text_chain(layer, layout, design, font, work, key, seconds, chains, last, place=None):
    """One typographic layer: real type scale, real entrance, real position.

    One `drawtext` per line rather than one per block. Multi-line drawtext leads at
    the font's maximum glyph height, which no layout here can know in advance.
    """
    role = layer.get('role', 'body')
    size = int(place['size'] if place else
               (layer.get('size_px') or layout['sizes'].get(role, layout['sizes']['body'])))
    content = place['content'] if place else str(layer.get('content', '')).strip()
    if not content:
        return last
    if not place:
        content = wrap_text(content, layout['text_width'], size, font)
    at = float(layer.get('at', 0.0))
    enter_for = float(layer.get('enter_seconds', design['motion']['enter_seconds']))
    ease = layer.get('ease', design['motion']['ease'])
    fill = colour(design, layer.get('colour', 'paper'))
    x = layer.get('x')
    x_px = layout['text_x'] if x is None else int(float(x) * layout['width'])
    # A measured position, or the deliberate one-off the manifest asked for.
    y_px = place['y'] if place else int(float(layer['y']) * layout['height'])
    enter = layer.get('enter', 'rise')
    alpha = expr(eased(at, enter_for, 'linear'))
    step = int(size * leading_of(design))
    for n, line in enumerate(content.splitlines()):
        if not line.strip():
            continue
        top = y_px + n * step
        out = '%s_%d' % (key, n)
        path = text_file(work, out, line)
        if enter == 'rise':
            rise = int(layout['height'] * 0.045)
            x_option = 'x=%d' % x_px
            y_option = "y='%s'" % expr(interpolate(top + rise, top, at, enter_for, ease))
        elif enter == 'slide':
            slide = int(layout['width'] * 0.10)
            x_option = "x='%s'" % expr(interpolate(x_px - slide, x_px, at, enter_for, ease))
            y_option = 'y=%d' % top
        else:
            x_option = 'x=%d' % x_px
            y_option = 'y=%d' % top
        chains.append("[%s]drawtext=fontfile='%s':textfile='%s':expansion=none:"
                      "fontcolor=%s:fontsize=%d:%s:%s:alpha='%s'[%s]"
                      % (last, filter_path(font), filter_path(path), fill, size,
                         x_option, y_option, alpha, out))
        last = out
    return last


def shape_chain(layer, layout, design, key, chains, last, place=None):
    """A rule or a block, stacked in the type column like the copy around it.

    Without that, a rule declared at a fraction of the frame sits above the copy in
    one ratio and halfway down the picture in another, which is the same mistake as
    a shared text position: one number cannot describe three compositions. Declared
    between two text layers, an unanchored rule lands between them, because it takes
    its turn in the same measured stack.
    """
    w = (int(float(layer['w']) * layout['width']) if 'w' in layer
         else int(layout['text_width'] * 0.32))
    # A rule wider than the column it underlines is a defect in every ratio, and the
    # landscape column is less than half the frame, so the clamp is not theoretical.
    w = max(8, min(w, layout['text_width']))
    h = place['height'] if place else max(2, int(float(layer.get('h', 0.006))
                                                 * layout['height']))
    x = (int(float(layer['x']) * layout['width']) if 'x' in layer else layout['text_x'])
    y = place['y'] if place else int(float(layer['y']) * layout['height'])
    fill = colour(design, layer.get('colour', 'accent'))
    opacity = float(layer.get('opacity', 1.0))
    grow = layer.get('grow')
    if grow:
        at = float(layer.get('at', 0.0))
        for_s = float(layer.get('enter_seconds', 0.5))
        w_expr = expr(interpolate(0, w, at, for_s, 'ease_out'))
        chains.append("[%s]drawbox=x=%d:y=%d:w='%s':h=%d:color=%s@%.3f:t=fill[%s]"
                      % (last, x, y, w_expr, h, fill, opacity, key))
    else:
        chains.append('[%s]drawbox=x=%d:y=%d:w=%d:h=%d:color=%s@%.3f:t=fill[%s]'
                      % (last, x, y, w, h, fill, opacity, key))
    return key


def render_scene(scene, fmt, design, layout, font, assets, work, out_path, tail=0.0):
    """One scene of one format, as a real file on disk.

    `tail` is extra material past the scene's declared end, exactly as long as the
    transition into the next scene. A crossfade consumes it, so the finished film
    still runs for the timeline the manifest declares. Without it every transition
    would silently shorten the ad, and the duration check would then fail on a
    timeline nobody got wrong.
    """
    fps = int(fmt['fps'])
    declared = round(float(scene['end']) - float(scene['start']), 3)
    seconds = round(declared + max(0.0, float(tail)), 3)
    if declared <= 0:
        raise EngineError('scene %s has no duration' % scene.get('id'))
    args, chains, last = scene_inputs(scene, assets, seconds, fps, layout)
    index = 1
    placed = place_stack(scene, layout, design)
    for n, layer in enumerate(scene.get('layers') or []):
        kind = layer.get('kind')
        key = 'k%d_%d' % (n, index)
        if kind in ('image', 'video'):
            asset = assets.get(layer.get('asset'))
            if not asset:
                raise EngineError('scene %s references asset %r which has no path'
                                  % (scene.get('id'), layer.get('asset')))
            if kind == 'image':
                args += ['-loop', '1', '-t', '%.3f' % seconds, '-i', str(asset)]
            else:
                args += ['-t', '%.3f' % seconds, '-i', str(asset)]
            last = media_layer(index, layer, layout, seconds, fps, chains, last, assets)
            index += 1
        elif kind == 'text':
            last = text_chain(layer, layout, design, font, work,
                              '%s_%d' % (re.sub(r'[^A-Za-z0-9]', '', str(scene.get('id', 's'))), n),
                              seconds, chains, last, placed.get(n))
        elif kind == 'shape':
            last = shape_chain(layer, layout, design, key, chains, last, placed.get(n))
        else:
            raise EngineError('unknown layer kind %r in scene %s' % (kind, scene.get('id')))
    # `tpad` holds the last frame so the clip can always reach the exact count asked
    # for below. An input that ends a fraction of a frame early otherwise yields one
    # frame fewer than requested, silently, and only on some scenes: the timeline
    # then drifts and a resume rejects a clip that was in fact finished.
    chains.append('[%s]format=yuv420p,fps=%d,tpad=stop=-1:stop_mode=clone,'
                  'settb=AVTB,setpts=PTS-STARTPTS[v]' % (last, fps))
    # An exact frame count, not a duration. `-t` cuts at the last frame strictly
    # before the mark, which lost a frame per scene and drifted the whole timeline.
    frames = scene_frames(seconds, fps)
    ffmpeg(args + ['-filter_complex', ';'.join(chains), '-map', '[v]', '-an',
                   '-frames:v', str(frames), '-r', str(fps), '-c:v', 'libx264',
                   '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                   '-movflags', '+faststart', '-y', str(out_path)],
           'scene %s at %s' % (scene.get('id'), fmt['ratio']))
    return out_path


def scene_frames(seconds, fps):
    """How many frames a scene clip of `seconds` holds, as one answer for everyone.

    The renderer asks so it can pass `-frames:v`, and the resume check asks so it can
    tell a finished clip from a truncated one. Computed twice from the same floats it
    came out one frame apart, because `3.2 + 0.35` is not `3.55` and rounding half to
    even then disagrees with itself. A resume that rebuilds work it already has is the
    mild version of that bug; the loud version is a clip trusted because two wrong
    numbers happened to match.
    """
    return int(round(round(float(seconds), 3) * int(fps)))


def transition_tail(scenes, index):
    """How much extra material scene `index` owes the transition that follows it."""
    if index + 1 >= len(scenes):
        return 0.0
    nxt = scenes[index + 1]
    kind = str((nxt.get('transition') or 'cut')).lower()
    if kind in ('cut', '', 'none'):
        return 0.0
    return max(0.0, float(nxt.get('transition_seconds', 0.4)))


# ------------------------------------------------------------------------ assembly

TRANSITIONS = {'dissolve': 'fade', 'fade': 'fade', 'wipe': 'wiperight',
               'slide': 'slideleft', 'smooth': 'smoothleft', 'circle': 'circleopen'}


def assemble(clips, scenes, fmt, work, out_path):
    """Join the scene clips, honouring declared transitions and the declared length.

    Each clip already carries a tail as long as the transition that follows it, so
    the crossfade eats the tail rather than the film: the offsets are the scene
    starts the manifest declares, and the result runs for exactly the timeline.

    Every branch is normalised first. `concat` hands on a microsecond timebase while
    a decoded input carries the stream's own, and `xfade` refuses two inputs whose
    timebases differ, with an error that names neither the scene nor the cause.
    """
    fps = int(fmt['fps'])
    transitions = [str((s.get('transition') or 'cut')).lower() for s in scenes[1:]]
    args, chains = [], []
    for i, c in enumerate(clips):
        args += ['-i', str(c)]
        chains.append('[%d:v]fps=%d,format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS[n%d]'
                      % (i, fps, i))
    current = 'n0'
    # The running total of what the manifest declares, which is where the next
    # transition has to start. It never includes the tails.
    elapsed = round(float(scenes[0]['end']) - float(scenes[0]['start']), 3)
    for i in range(1, len(clips)):
        kind = transitions[i - 1]
        label = 'x%d' % i
        declared = round(float(scenes[i]['end']) - float(scenes[i]['start']), 3)
        if kind in ('cut', '', 'none'):
            chains.append('[%s][n%d]concat=n=2:v=1:a=0,settb=AVTB,setpts=PTS-STARTPTS[%s]'
                          % (current, i, label))
        else:
            duration = max(0.05, min(float(scenes[i].get('transition_seconds', 0.4)),
                                     elapsed - 0.05, declared - 0.05))
            chains.append('[%s][n%d]xfade=transition=%s:duration=%.3f:offset=%.3f,'
                          'settb=AVTB,setpts=PTS-STARTPTS[%s]'
                          % (current, i, TRANSITIONS.get(kind, 'fade'), duration,
                             elapsed, label))
        elapsed = round(elapsed + declared, 3)
        current = label
    chains.append('[%s]fps=%d,format=yuv420p[v]' % (current, fps))
    ffmpeg(args + ['-filter_complex', ';'.join(chains), '-map', '[v]', '-an',
                   '-frames:v', str(int(round(elapsed * fps))),
                   '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                   '-pix_fmt', 'yuv420p', '-y', str(out_path)],
           'assembly at %s' % fmt['ratio'])
    return out_path


# ------------------------------------------------------------------------ captions

def ass_time(seconds):
    seconds = max(0.0, float(seconds))
    h = int(seconds // 3600); m = int((seconds % 3600) // 60)
    s = seconds % 60
    return '%d:%02d:%05.2f' % (h, m, s)


def ass_colour(design, name, default):
    """A palette name to the &HAABBGGRR an ASS style wants.

    The captions were the one part of the film that ignored the brand: white fill and
    a hard-coded navy outline, whatever the palette said. On a light art direction
    that is white type over cream, saved only by its outline.
    """
    value = colour(design, name, default)
    try:
        n = int(str(value).replace('0x', ''), 16)
    except ValueError:
        n = int(str(default).replace('0x', ''), 16)
    return '&H00%02X%02X%02X' % (n & 0xFF, (n >> 8) & 0xFF, (n >> 16) & 0xFF)


def write_ass(captions, layout, design, font_name, path, style=None):
    """Captions as a subtitle file, styled per format.

    Burned from the manifest's cues, which the validator already requires to come
    from the final take rather than the script. The margin follows the format's own
    safe area, so nothing lands under the platform's interface.
    """
    size = layout['sizes'].get('caption', 34)
    style = style or {}
    fill = ass_colour(design, style.get('colour', 'paper'), '0xFFFFFF')
    edge = ass_colour(design, style.get('outline', 'ink'), '0x101820')
    margin_v = layout['safe_bottom']
    margin_l = layout['margin']
    margin_r = layout.get('margin_right', layout['margin'])
    head = ('[Script Info]\nScriptType: v4.00+\nWrapStyle: 2\n'
            'PlayResX: %d\nPlayResY: %d\nScaledBorderAndShadow: yes\n\n'
            '[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, '
            'BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV\n'
            'Style: Cap,%s,%d,%s,%s,&H80000000,-1,1,3,0,2,%d,%d,%d\n\n'
            '[Events]\nFormat: Layer, Start, End, Style, Text\n'
            % (layout['width'], layout['height'], font_name, size, fill, edge,
               margin_l, margin_r, margin_v))
    rows = []
    for cue in captions or []:
        text = str(cue.get('text', '')).replace('\n', BS + 'N')
        rows.append('Dialogue: 0,%s,%s,Cap,%s\n'
                    % (ass_time(cue.get('start', 0)), ass_time(cue.get('end', 0)), text))
    path.write_text(head + ''.join(rows), encoding='utf-8')
    return path


def burn_captions(video, ass_path, out_path, fmt):
    ffmpeg(['-i', str(video), '-vf', "subtitles='%s'" % filter_path(ass_path),
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
            '-pix_fmt', 'yuv420p', '-r', str(int(fmt['fps'])), '-y', str(out_path)],
           'captions at %s' % fmt['ratio'])
    return out_path


# --------------------------------------------------------------------------- audio

def build_audio(manifest, assets, seconds, work, out_path, loudness=None, measured=None):
    """Voice, music and effects into one track, music ducked under the voice.

    Ducking is a real sidechain compressor keyed on the voice, not a fixed music
    gain, so the music recovers in the gaps instead of sitting low throughout. The
    loudness target is whatever the manifest declares; this engine does not invent
    one, and `loudness_target.source` is required by the validator for that reason.
    """
    voice = (manifest.get('voice') or {}).get('file')
    music = (manifest.get('music') or {}).get('file')
    effects = [e for e in (manifest.get('sfx') or []) if isinstance(e, dict) and e.get('file')]
    args, chains, mix = [], [], []
    index = 0
    voice_label = None
    if voice:
        args += ['-i', str(assets.get(voice, voice))]
        chains.append('[%d:a]aresample=48000,atrim=0:%.3f,asetpts=N/SR/TB,'
                      'apad=whole_dur=%.3f[voice]' % (index, seconds, seconds))
        voice_label = 'voice'
        index += 1
    if music:
        args += ['-stream_loop', '-1', '-i', str(assets.get(music, music))]
        gain = float((manifest.get('music') or {}).get('gain_db', -18.0))
        chains.append('[%d:a]aresample=48000,atrim=0:%.3f,asetpts=N/SR/TB,'
                      'volume=%.2fdB,afade=t=in:st=0:d=0.4,afade=t=out:st=%.3f:d=0.6[musicraw]'
                      % (index, seconds, gain, max(0.0, seconds - 0.6)))
        index += 1
        if voice_label:
            # Both sides of the sidechain are cut into identical frames first. The
            # compressor's state depends on the frames it is handed, and two separate
            # inputs are not handed to it the same way twice: the same manifest then
            # encoded to different bytes on every run, which quietly makes the hash
            # recorded in the manifest a hash of one particular afternoon.
            chains.append('[%s]asetnsamples=n=1024:p=0,asplit=2[vout][vkey]' % voice_label)
            chains.append('[musicraw]asetnsamples=n=1024:p=0[musicfr]')
            chains.append('[musicfr][vkey]sidechaincompress=threshold=0.03:ratio=12:'
                          'attack=15:release=350:makeup=1[music]')
            mix = ['vout', 'music']
        else:
            chains.append('[musicraw]anull[music]')
            mix = ['music']
    elif voice_label:
        mix = [voice_label]
    for e in effects:
        args += ['-i', str(assets.get(e['file'], e['file']))]
        at = float(e.get('at', 0.0))
        gain = float(e.get('gain_db', -6.0))
        label = 'sfx%d' % index
        chains.append('[%d:a]aresample=48000,volume=%.2fdB,adelay=%d|%d[%s]'
                      % (index, gain, int(at * 1000), int(at * 1000), label))
        mix.append(label)
        index += 1
    if not mix:
        # No audio at all is a legitimate choice, and silence has to be deliberate
        # rather than an accident of a missing file, so it is written explicitly.
        args += ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']
        chains.append('[%d:a]atrim=0:%.3f,asetpts=N/SR/TB[mixed]' % (index, seconds))
    elif len(mix) == 1:
        chains.append('[%s]anull[mixed]' % mix[0])
    else:
        chains.append('%samix=inputs=%d:duration=longest:normalize=0[mixed]'
                      % (''.join('[%s]' % m for m in mix), len(mix)))
    target = loudness or {}
    integrated = float(target.get('value', -14.0))
    true_peak = float(target.get('true_peak', -1.5))
    lra = float(target.get('lra', 11.0))
    norm = 'loudnorm=I=%.2f:TP=%.2f:LRA=%.2f' % (integrated, true_peak, lra)
    if measured:
        # Second pass: hand loudnorm what the first pass measured, which is how the
        # target is actually hit rather than approached.
        norm += (':measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:'
                 'offset=%s:linear=true' % (measured['input_i'], measured['input_tp'],
                                            measured['input_lra'], measured['input_thresh'],
                                            measured.get('target_offset', '0.0')))
    chains.append('[mixed]%s,aresample=48000,atrim=0:%.3f,asetpts=N/SR/TB[a]'
                  % (norm, seconds))
    ffmpeg(args + ['-filter_complex', ';'.join(chains), '-map', '[a]',
                   '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
                   '-y', str(out_path)], 'audio track')
    return out_path


def measure_loudness(manifest, assets, seconds, work, loudness):
    """First loudnorm pass, so the second one can hit the declared target."""
    probe_out = work / 'loudness-probe.m4a'
    args = ['-hide_banner', '-nostdin']
    build_audio(manifest, assets, seconds, work, probe_out, loudness=loudness)
    code, _, err = run(['ffmpeg', '-hide_banner', '-nostdin', '-i', str(probe_out),
                        '-af', 'loudnorm=I=%.2f:TP=%.2f:LRA=%.2f:print_format=json'
                        % (float(loudness.get('value', -14.0)),
                           float(loudness.get('true_peak', -1.5)),
                           float(loudness.get('lra', 11.0))),
                        '-f', 'null', '-'])
    match = re.search(r'\{[^{}]*"input_i"[^{}]*\}', err, re.S)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except ValueError:
        return None


def mux(video, audio, out_path, fmt, seconds):
    ffmpeg(['-i', str(video), '-i', str(audio), '-map', '0:v:0', '-map', '1:a:0',
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest',
            '-t', '%.3f' % seconds, '-movflags', '+faststart',
            '-y', str(out_path)], 'mux at %s' % fmt['ratio'])
    return out_path


# ------------------------------------------------------------------- control views

def contact_sheet(video, out_path, columns=4, rows=3):
    """One image of the whole ad. The fastest way for a person to see a dead scene."""
    total = max(1, columns * rows)
    code, out, _ = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', str(video)])
    try:
        duration = float((out or '').strip())
    except ValueError:
        duration = 0.0
    rate = max(0.05, total / duration) if duration > 0 else 1.0
    ffmpeg(['-i', str(video), '-vf',
            'fps=%.4f,scale=320:-1:force_original_aspect_ratio=decrease,'
            'pad=320:ceil(ih/2)*2:(ow-iw)/2:(oh-ih)/2:color=0x101820,tile=%dx%d'
            % (rate, columns, rows),
            '-frames:v', '1', '-y', str(out_path)], 'contact sheet')
    return out_path


def control_frames(video, timecodes, out_dir):
    """Full-size frames at the moments a reviewer argues about."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for t in timecodes:
        target = out_dir / ('frame-%06dms.png' % int(float(t) * 1000))
        ffmpeg(['-ss', '%.3f' % float(t), '-i', str(video), '-frames:v', '1',
                '-y', str(target)], 'control frame at %.2fs' % float(t))
        written.append(target)
    return written
