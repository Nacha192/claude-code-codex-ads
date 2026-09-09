"""Measure an exported video file with ffprobe and ffmpeg. Standard library plus those two.

This is the half of quality control a machine can actually do: what the file is, not
whether the ad is good. Every threshold arrives as an argument, from the brief or the
manifest, because a number invented here would become a law nobody voted for.

It decodes the whole file. That is the point: a container that reports 20 seconds and
throws errors at 14 is the defect this catches and metadata alone never will.

Exit codes: 0 clean, 1 findings, 2 bad usage or unreadable file, 3 ffmpeg missing.
"""
import argparse,hashlib,json,math,re,shutil,subprocess,sys
from pathlib import Path

TIMEOUT=900

def tool(name):
    return shutil.which(name)

def digest_of(path):
    """Hash in chunks. Exports are videos, and reading a whole one into memory to
    hash it is how the measuring tool dies on the largest file it is given."""
    h=hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda:fh.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()

def run(cmd):
    """Run a command, return (returncode, stdout, stderr). Never raises on tool failure."""
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=TIMEOUT,encoding='utf-8',errors='replace')
        return p.returncode,p.stdout or '',p.stderr or ''
    except subprocess.TimeoutExpired:
        return 124,'','Timed out after %ds'%TIMEOUT
    except OSError as e:
        return 125,'',str(e)

def ratio_of(w,h):
    g=math.gcd(int(w),int(h)) or 1
    return '%d:%d'%(int(w)//g,int(h)//g)

def rational(value):
    """ffprobe writes rates as '30000/1001'. Return a float, or None."""
    if not isinstance(value,str) or not value.strip():return None
    try:
        if '/' in value:
            a,b=value.split('/',1);b=float(b)
            return float(a)/b if b else None
        return float(value)
    except ValueError:return None

def probe(path):
    code,out,err=run(['ffprobe','-v','error','-print_format','json','-show_format','-show_streams',str(path)])
    if code!=0:return None,err.strip() or 'ffprobe failed'
    try:return json.loads(out),None
    except json.JSONDecodeError as e:return None,'ffprobe returned unreadable JSON: '+str(e)

def measure(path):
    """Everything that can be read or decoded. Returns (measurements, findings)."""
    m={};f=[]
    def fail(severity,what):f.append({'severity':severity,'observation':what})

    info,error=probe(path)
    if info is None:return m,[{'severity':'blocking','observation':'Cannot probe the file: '+str(error)}]

    fmt=info.get('format',{}) or {}
    m['container']=fmt.get('format_name')
    m['duration_seconds']=rational(fmt.get('duration'))
    m['declared_bitrate']=rational(fmt.get('bit_rate'))
    size=fmt.get('size')
    m['size_bytes']=int(size) if isinstance(size,str) and size.isdigit() else None

    video=[s for s in info.get('streams',[]) if s.get('codec_type')=='video']
    audio=[s for s in info.get('streams',[]) if s.get('codec_type')=='audio']
    m['video_streams']=len(video);m['audio_streams']=len(audio)
    if not video:
        fail('blocking','No video stream in the file')
    else:
        v=video[0]
        m['codec']=v.get('codec_name')
        m['width']=v.get('width');m['height']=v.get('height')
        if m['width'] and m['height']:m['ratio']=ratio_of(m['width'],m['height'])
        m['sample_aspect_ratio']=v.get('sample_aspect_ratio')
        if m['sample_aspect_ratio'] not in (None,'1:1','0:1'):
            fail('high','Non-square pixels (SAR %s): the frame will be stretched by some players'%m['sample_aspect_ratio'])
        m['fps']=rational(v.get('avg_frame_rate')) or rational(v.get('r_frame_rate'))
        frames=v.get('nb_frames')
        m['frame_count']=int(frames) if isinstance(frames,str) and frames.isdigit() else None
        if m['frame_count'] is None and m['fps'] and m['duration_seconds']:
            m['frame_count_estimated']=round(m['fps']*m['duration_seconds'])
        m['pixel_format']=v.get('pix_fmt')
    if audio:
        a=audio[0]
        m['audio_codec']=a.get('codec_name')
        m['sample_rate']=rational(a.get('sample_rate'))
        m['channels']=a.get('channels')

    # Full decode. Metadata lies; the decoder does not.
    code,_,err=run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'])
    lines=[l for l in err.splitlines() if l.strip()]
    m['decode_errors']=len(lines)
    if code!=0 or lines:
        for line in lines[:5]:fail('blocking','Decode error: '+line.strip())
        if len(lines)>5:fail('blocking','%d further decode errors'%(len(lines)-5))
        # A nonzero exit with an empty stderr would otherwise leave decode_errors at
        # zero and no finding at all, which reads exactly like a clean decode.
        if not lines:fail('blocking','ffmpeg exited %d while decoding and reported nothing; treat the file as unreadable'%code)

    if audio:
        code,_,err=run(['ffmpeg','-nostats','-i',str(path),'-af','ebur128=peak=true','-f','null','-'])
        integrated=re.findall(r'I:\s*(-?\d+(?:\.\d+)?)\s*LUFS',err)
        peak=re.findall(r'Peak:\s*(-?\d+(?:\.\d+)?)\s*dBFS',err)
        if integrated:m['loudness_lufs']=float(integrated[-1])
        if peak:m['true_peak_dbfs']=float(peak[-1])
        if m.get('true_peak_dbfs') is not None and m['true_peak_dbfs']>-0.1:
            fail('high','True peak %.1f dBFS: clipping is likely on playback'%m['true_peak_dbfs'])
        code,_,err=run(['ffmpeg','-nostats','-i',str(path),'-af','silencedetect=noise=-50dB:d=0.25','-f','null','-'])
        starts=[float(x) for x in re.findall(r'silence_start:\s*(-?\d+(?:\.\d+)?)',err)]
        ends=[float(x) for x in re.findall(r'silence_end:\s*(-?\d+(?:\.\d+)?)',err)]
        m['silence_regions']=len(starts)
        if starts and starts[0]<=0.05:
            m['leading_silence']=ends[0] if ends else None
            if m['leading_silence'] and m['leading_silence']>0.4:
                fail('high','%.2fs of silence at the head: the first second is the whole ad'%m['leading_silence'])
        if starts and m.get('duration_seconds'):
            tail=starts[-1]
            closed=len(ends)>=len(starts)
            if not closed or (ends and ends[-1]>=m['duration_seconds']-0.05):
                trailing=m['duration_seconds']-tail
                m['trailing_silence']=trailing
                if trailing>0.75:fail('medium','%.2fs of silence at the tail'%trailing)
    else:
        m['loudness_lufs']=None
        fail('high','No audio stream: check that this is deliberate')

    # Unexpected black. A black first frame is a scroll, whatever the rest does.
    code,_,err=run(['ffmpeg','-nostats','-i',str(path),'-vf','blackdetect=d=0.12:pix_th=0.10','-f','null','-'])
    black=[(float(a),float(b)) for a,b in re.findall(r'black_start:(\d+(?:\.\d+)?)\s+black_end:(\d+(?:\.\d+)?)',err)]
    m['black_regions']=len(black)
    for start,end in black:
        if start<=0.05:fail('blocking','The video opens on %.2fs of black'%(end-start))
        elif m.get('duration_seconds') and end>=m['duration_seconds']-0.05 and end-start>0.5:
            fail('medium','%.2fs of black at the tail'%(end-start))
        elif end-start>0.35:fail('high','Black frames from %.2fs to %.2fs'%(start,end))

    code,_,err=run(['ffmpeg','-nostats','-i',str(path),'-vf','freezedetect=noise=-60dB:duration=2','-f','null','-'])
    frozen=re.findall(r'freeze_start:\s*(-?\d+(?:\.\d+)?)',err)
    m['freeze_regions']=len(frozen)
    for start in frozen:
        fail('medium','The frame stops moving at %.2fs for at least 2s; deliberate or a render fault'%float(start))

    return m,f

def compare(m,args):
    """Every expectation here arrived as an argument. Nothing is assumed."""
    out=[]
    def fail(severity,what):out.append({'severity':severity,'observation':what})
    if args.expect_ratio:
        if m.get('ratio')!=args.expect_ratio:
            fail('blocking','Ratio is %s and %s was requested'%(m.get('ratio'),args.expect_ratio))
    if args.expect_width and m.get('width') and int(m['width'])!=args.expect_width:
        fail('blocking','Width is %s and %d was requested'%(m.get('width'),args.expect_width))
    if args.expect_height and m.get('height') and int(m['height'])!=args.expect_height:
        fail('blocking','Height is %s and %d was requested'%(m.get('height'),args.expect_height))
    if args.expect_duration is not None and m.get('duration_seconds') is not None:
        gap=abs(m['duration_seconds']-args.expect_duration)
        if gap>args.duration_tolerance:
            fail('blocking','Duration is %.2fs and %.2fs was requested, %.2fs outside the %.2fs tolerance'%(
                m['duration_seconds'],args.expect_duration,gap,args.duration_tolerance))
    if args.expect_fps and m.get('fps') and abs(m['fps']-args.expect_fps)>0.02:
        fail('high','Frame rate is %.3f and %.3f was requested'%(m['fps'],args.expect_fps))
    if args.expect_audio_streams is not None and m.get('audio_streams')!=args.expect_audio_streams:
        fail('blocking','%s audio stream(s) present, %d expected'%(m.get('audio_streams'),args.expect_audio_streams))
    if args.expect_sample_rate and m.get('sample_rate') and int(m['sample_rate'])!=args.expect_sample_rate:
        fail('medium','Sample rate is %s and %d was requested'%(int(m['sample_rate']),args.expect_sample_rate))
    if args.loudness is not None and m.get('loudness_lufs') is not None:
        gap=abs(m['loudness_lufs']-args.loudness)
        if gap>args.loudness_tolerance:
            fail('high','Integrated loudness is %.1f LUFS against a declared target of %.1f'%(
                m['loudness_lufs'],args.loudness))
    if args.max_true_peak is not None and m.get('true_peak_dbfs') is not None:
        if m['true_peak_dbfs']>args.max_true_peak:
            fail('high','True peak %.1f dBFS is above the declared ceiling of %.1f'%(
                m['true_peak_dbfs'],args.max_true_peak))
    if args.captions_end is not None and m.get('duration_seconds') is not None:
        if args.captions_end>m['duration_seconds']+0.001:
            fail('blocking','The last caption ends at %.2fs, past the %.2fs of video'%(
                args.captions_end,m['duration_seconds']))
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('path')
    p.add_argument('--expect-ratio');p.add_argument('--expect-width',type=int);p.add_argument('--expect-height',type=int)
    p.add_argument('--expect-duration',type=float);p.add_argument('--duration-tolerance',type=float,default=0.5)
    p.add_argument('--expect-fps',type=float)
    p.add_argument('--expect-audio-streams',type=int)
    p.add_argument('--expect-sample-rate',type=int)
    p.add_argument('--loudness',type=float,help='Declared integrated target in LUFS, from the brief or the platform')
    p.add_argument('--loudness-tolerance',type=float,default=1.5)
    p.add_argument('--max-true-peak',type=float)
    p.add_argument('--captions-end',type=float,help='End of the last caption cue, in seconds')
    p.add_argument('--json',action='store_true')
    a=p.parse_args()

    for name in ['ffprobe','ffmpeg']:
        if not tool(name):
            print(json.dumps({'error':name+' is not on PATH','measurements':{},'findings':[]}))
            print('%s is not installed, so nothing was measured. This is not a pass.'%name,file=sys.stderr)
            return 3
    path=Path(a.path)
    if not path.is_file():
        print('No such file: '+str(path),file=sys.stderr);return 2
    # Absolute from here on: a relative name beginning with "-" would be read as an
    # option by ffprobe, which takes its input as a positional argument.
    path=path.resolve()

    m,findings=measure(path)
    try:m['sha256']=digest_of(path)
    except OSError as e:
        print('Cannot read the file to hash it: '+str(e),file=sys.stderr);return 2
    m['path']=str(path)
    findings=findings+compare(m,a)
    blocking=[f for f in findings if f['severity']=='blocking']
    report={'measurements':m,'findings':findings,
            'verdict':'fail' if blocking else ('pass_with_noted_risk' if findings else 'pass')}
    if a.json:print(json.dumps(report,indent=2))
    else:
        for k in sorted(m):print('  %-24s %s'%(k,m[k]))
        for f in findings:print('%-9s %s'%(f['severity'],f['observation']))
        print(report['verdict'])
    return 1 if findings else 0

if __name__=='__main__':sys.exit(main())
