# Measurable checks for a finished video ad

These checks answer what a media file can. They do not prove persuasion, truth,
licensing, synchronization, or platform acceptance. Record the filename, checksum, command, output, and decision requirement.

All commands were executed against a synthetic FFmpeg fixture. They use relative
paths from the media directory. Replace `ad-test.mp4` with the final export.

## If FFmpeg is unavailable

Check both programs before reporting any result:

```console
ffmpeg -version
ffprobe -version
```

If either command is missing, stop automated media QA. A file manager property
panel, export dialog, successful render, or accepted browser upload is no substitute.
Name the checks that did not run and ask before installing software. If approved,
use official FFmpeg guidance or the system's trusted package manager, then rerun
both commands. Otherwise hand the file and checklist to a machine with both tools.
Label delivery `media QA pending` [ours] until the output has been measured.

## Establish the requirement first

Write down the placement, target duration, dimensions and display ratio, frame-rate
policy, audio-track count, caption deliverable, and current encoding constraints.
A measurement has no pass/fail meaning without that declared requirement.

Keep sources visible: `[platform]` for current platform documentation, `[ours]`
for a production decision, `[observed]` for output, and `[hypothesis]` when its
authority is unknown. Do not copy fixture results into a delivery requirement.

First confirm that every selected stream decodes. Exit status zero [observed] on
the fixture meant no decoder error was reported, not that quality was good:

```console
ffmpeg -hide_banner -v error -i ad-test.mp4 -map 0:v:0 -map 0:a? -f null -
```

## Duration against the intended cut

Measure container start and duration rather than trusting the filename:

```console
ffprobe -v error -show_entries format=start_time,duration -of default=noprint_wrappers=1 ad-test.mp4
```

The fixture returned start `0.000000` seconds [observed] and duration `4.000000`
seconds [observed]. Compare duration with the approved cut. Use a tolerance of at
most one delivered frame [ours] unless the platform is tighter [platform]. At
`30/1` fps [observed], that was `0.033333` seconds [observed]. Investigate any
unexplained excess or nonzero start time, which can shift subtitle packet times.

## Resolution, sample shape, and display ratio

```console
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,sample_aspect_ratio,display_aspect_ratio -of default=noprint_wrappers=1 ad-test.mp4
```

The fixture returned `1280` by `720` pixels [observed], sample ratio `1:1`
[observed], and display ratio `16:9` [observed]. Compare every field with the
specification. Dimensions check the stored frame; display ratio includes sample
shape. A square-pixel requirement of `1:1` [ours] fails if non-square samples
make otherwise incorrect dimensions look right during playback.

## Frame rate and decoded frame count

Read both declared rates:

```console
ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate,r_frame_rate -of default=noprint_wrappers=1 ad-test.mp4
```

Both fixture values were `30/1` fps [observed]. A mismatch does not by itself
prove variable frame rate, but it requires investigation [ours]. Count decoded
frames and retain stream duration for a second check:

```console
ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=duration,avg_frame_rate,nb_read_frames -of default=noprint_wrappers=1 ad-test.mp4
```

The fixture decoded `120` frames [observed] over `4.000000` seconds [observed],
agreeing with `30/1` fps [observed]. Compare with the declared rate policy. Do not
silently convert mixed sources.

## Video and container bit rate

```console
ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -show_entries format=bit_rate -of json ad-test.mp4
```

The fixture reported video bit rate `2057694` bit/s [observed] and container bit
rate `2167444` bit/s [observed]. The latter includes audio and overhead. Compare
video with the export brief or current placement documentation. Treat a missing
value as unknown [ours], not zero, and inspect encoder settings or calculate file
bits divided by measured duration.

## Presence and number of audio tracks

```console
ffprobe -v error -select_streams a -show_entries stream=index,codec_name,sample_rate,channels,channel_layout -of compact=p=0:nk=1 ad-test.mp4
```

This prints one row per audio stream. The fixture printed one row [observed]: index
`1` [observed], `aac` [observed], `48000` Hz [observed], one channel [observed],
and `mono` [observed]. Empty output means no audio stream [observed]. Compare row
count and layout with the deliverable. Unexpected or empty tracks fail [ours].

## Integrated loudness and true peak

Measure the exact delivered audio stream from beginning to end:

```console
ffmpeg -hide_banner -nostats -i ad-test.mp4 -map 0:a:0 -af ebur128=peak=true -f null -
```

Read the final `Summary`, not a momentary line. The fixture measured integrated
loudness `-24.1` LUFS [observed] and true peak `-19.9` dBFS [observed]. The displayed
target is an analysis reference, not this pack's target. No universal loudness
target is asserted here. Select one from current placement documentation
[platform], a broadcaster or client brief [ours], or accepted assets [observed].
Record the requirement, allowed tolerance, measurement, and decision.

## Clipping indicators

True peak identifies inter-sample risk. Sample statistics identify repeated
full-scale samples and flattened peaks. Run both `ebur128` above and:

```console
ffmpeg -hide_banner -nostats -i ad-test.mp4 -map 0:a:0 -af astats=metadata=0:reset=0 -f null -
```

The clean fixture measured peak level `-19.948124` dB [observed], flat factor
`0.000000` [observed], and absolute peak count `1` [observed]. A deliberately
clipped PCM fixture measured peak level `0.000265` dB [observed], flat factor
`31.214866` [observed], and absolute peak count `16000` [observed]. Values at or
within `0.1` dB of full scale [ours], especially with a large repeated peak count
or nonzero flat factor, trigger waveform inspection and listening [ours]. They
are indicators, not mathematical proof that every codec clipped. Reject audible
distortion and repair the mix before re-encoding [ours].

## Silence at the head or tail

```console
ffmpeg -hide_banner -nostats -i ad-test.mp4 -map 0:a:0 -af silencedetect=noise=-50dB:d=0.1 -f null -
```

The settings, `-50` dB [ours] for at least `0.1` seconds [ours], are a starting
definition, not a platform rule. Adjust and record them when room tone or fades
require it. The fixture found head silence from `0` to `0.400021` seconds [observed]
and tail silence from `3.6` to `4.010667` seconds [observed]. Compare
both with the sound design. Unplanned silence can delay impact or reveal an audio
edit that ended before the picture.

## Subtitle timing against the montage

For a sidecar or muxed subtitle stream, inspect every packet start and duration:

```console
ffprobe -v error -f srt -i captions.srt -show_entries packet=pts_time,duration_time -of csv=p=0
```

The fixture sidecar returned `0.000000,1.000000` seconds [observed] and
`3.000000,1.000000` seconds [observed] as start and duration. For every row, calculate
cue end as start plus duration. No cue may start before the montage start [ours]
or end after the measured montage end plus one delivered frame [ours]. The last
fixture cue ended at `4.000000` seconds [observed], matching the montage duration
`4.000000` seconds [observed]. Gaps are valid only where no caption is intended.

For muxed subtitles, omit `-f srt -i captions.srt`, use `-select_streams s:0`, and
query the media file. Compare packets with its measured `start_time` because
container offsets can shift times; do not assume zero [ours].

Burned-in text has no recoverable subtitle stream. Retain its exact SRT or ASS
source, check packets against final montage duration, and inspect
frames at the first and last cue boundaries. Without that source, caption duration
is not machine-verifiable [ours]; report it as pending. Finally watch the export
with sound and muted, since timing equality does not prove transcription accuracy.
