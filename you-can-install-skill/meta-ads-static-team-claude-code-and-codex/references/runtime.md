# First run: what this machine can actually do

A pack that assumes its tools are there discovers they are not halfway through a job,
with the brief written and nothing rendered. Find out first, once, and say what is
missing before it matters rather than after.

## One command

```sh
python scripts/check_setup.py --json --write .ads-brain/setup.json
```

It installs nothing. It reports, prints the exact command for this operating system,
and stops. Exit `0` means everything the scripts need is present, `1` means something
is missing and the report names it.

## When

Before the first script call in a project and before the first media generation,
whichever comes first. Once per project: skip it when `.ads-brain/setup.json` already
records a verdict. Run it again when a script fails to start, when a render refuses,
or when the user says they installed something.

## Three answers, never a fourth

**Present.** The binary is on PATH, the version is high enough, the filters exist.

**Missing.** Named, with the command that fixes it.

**Cannot be checked from a script.** A script sees a binary. It does not see whether an
account has credits, a connector is authorised, or a site is logged in. Guessing at
those is how a pack promises a capability it does not have, so the report lists them by
name and the assistant looks for them in the session instead.

| The script checks | Because |
|---|---|
| Python version and interpreter path | Every check in this pack is a Python script |
| `ffmpeg` and `ffprobe` on PATH | Motion packs only. No renderer, no file |
| The filters the pipeline issues, one by one | A build missing `drawtext` encodes perfectly and draws no text |
| `libx264` and `aac` encoders | A file nothing can play is not a deliverable |
| libfreetype, and a usable font file | Same reason, and it is the macOS failure in practice |

| Only the session can check | Because |
|---|---|
| Image generation | An account and a connector, not a binary |
| Speech provider | Same, and consent for a cloned voice is a human matter |
| Video model | Optional. The supplied engine composes stills, type and footage you give it |
| Meta Ad Library access | Public browser access is enough; no API key is needed to read it |
| Meta Marketing API or MCP | Never needed to make the creative. Only to read or write the account |

## Before the script: is there an interpreter at all

`check_setup.py` cannot report on a machine with no Python, so this one check comes
first. Try these in order and keep the first that answers, since the working command
differs by machine:

```sh
python3 --version
python --version
py -3 --version
```

Accept 3.10 or newer. Record the command that worked and use that same command for
every later script call instead of guessing again.

`py` is the Windows launcher and is not visible from every shell: a POSIX-style shell
on Windows can report `py: command not found` while `python` answers normally. A
failure on one of the three is not evidence that Python is absent. Only conclude
`missing` when all three fail. If they do, write `.ads-brain/setup.json` with your own
file tools, because you cannot run a script to write it.

## If something is missing

Present the whole gap in **one** message, not one question per item: what is missing,
what stops working because of it, and the exact command for this operating system.
Then ask once.

| System | Python | FFmpeg |
|---|---|---|
| Windows | `winget install -e --id Python.Python.3.12` | `winget install -e --id Gyan.FFmpeg` |
| macOS | `brew install python@3.12` | `brew install ffmpeg` |
| Debian, Ubuntu | `sudo apt update && sudo apt install python3` | `sudo apt update && sudo apt install ffmpeg` |
| Fedora, RHEL | `sudo dnf install python3` | `sudo dnf install ffmpeg` |

Take the **full** FFmpeg build. A minimal one encodes video and cannot draw text:
Homebrew's macOS bottle ships without libfreetype, so `drawtext` and `subtitles` do not
exist and the film would come out at the right duration with none of the words in it.
The engine refuses in that case and names the missing filters, which is the behaviour
to expect rather than a bug to work around.

A command with `sudo` asks for a password, which a non-interactive shell cannot answer.
Hand that command to the user to run in their own terminal rather than launching it and
hanging. On Windows the python.org installer needs "Add python.exe to PATH" ticked.

## Never

Never install silently. Installing software changes the user's machine and a skill has
no standing authorization to do that. Never pick a different package because the named
one failed without saying so, and never edit a shell profile or PATH without stating
exactly what changed. After an install, run the check again and record the real result.
Do not record `ok` on the strength of an install command that appeared to succeed.

## If the user declines

Record `declined` and **carry on**. That is the point of asking rather than blocking:
everything that does not need the missing part still works, and the delivery says
plainly what did not run. Without Python, research, strategy, hooks and copy are
unaffected and the automatic refusals do not happen. Without a full FFmpeg, the whole
film is designed, written, timed and specified, and no file is produced.

A skipped check is not a passed check, and an unrendered film is not a rendered one.
Say so in the delivery, once, without apologising for it.
