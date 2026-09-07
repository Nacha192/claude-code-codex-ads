# First-run check: is Python actually here

The checks this pack promises are Python scripts. `scripts/check_artifact.py` and `scripts/init_brain.py` do not run without an interpreter, and the pack can be installed from a ZIP on a machine that has none. Verify once, early, rather than discovering it when a check was supposed to block something.

## When

Before the first script call in a project, and before the first media generation, whichever comes first. Once per project. Skip it when `.ads-brain/runtime.json` already records a working interpreter. Run it again if a script fails to start.

## How

Try these in order and keep the first that answers, since the working command differs by machine:

```sh
python3 --version
python --version
py -3 --version
```

Accept 3.10 or newer, which is what these scripts require. Record the command that worked; use that same command for every later script call instead of guessing again.

`py` is the Windows launcher and is not visible from every shell: a POSIX-style shell on Windows can report `py: command not found` while `python` answers normally. A failure on one of the three is not evidence that Python is absent. Only conclude `missing` when all three fail.

Write the result to `.ads-brain/runtime.json` in the project:

```json
{"schema_v":"1.0.0","python":{"status":"ok","command":"python3","version":"3.12.4","checked_at":"2026-09-06"}}
```

`status` is `ok`, `missing`, `too_old` or `declined`. Write this file with your own file tools: if Python is absent you cannot run a script to write it.

## If Python is missing or too old

Stop and say plainly what stops working: the artifact checker that refuses unapproved generation, credential-shaped values, unproven claims and over-limit copy, and the second-brain initialiser. Research, strategy, hooks and copy still work; the automatic refusals do not.

Then propose the install for the actual operating system and **ask before running anything**. Installing software changes the user's machine, and a skill has no standing authorization to do that.

| System | Route |
|---|---|
| Windows | `winget install -e --id Python.Python.3.12`, or the installer from [python.org](https://www.python.org/downloads/) with "Add python.exe to PATH" ticked |
| macOS | `brew install python@3.12`, or the [python.org](https://www.python.org/downloads/) installer. The system Python that ships with macOS may be older than 3.10 |
| Debian, Ubuntu | `sudo apt update && sudo apt install python3` |
| Fedora, RHEL | `sudo dnf install python3` |

A command with `sudo` asks for a password, which a non-interactive shell cannot answer. Hand that command to the user to run in their own terminal rather than launching it and hanging.

Never install silently, never pick a different package because the named one failed without saying so, and never edit a shell profile or PATH without stating exactly what changed. After an install, run the version check again and record the real result. Do not record `ok` on the strength of an install command that appeared to succeed.

## If the user declines

Record `declined` and continue. Everything that does not need an interpreter still works, and this is the honest part: say in the delivery that the artifact checks did not run, and do not describe copy as checked. A skipped check is not a passed check.
