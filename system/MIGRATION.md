# Migration from the initial distribution

## Version 2.1.0: the packs check for Python before relying on it

The scripts that enforce the approval gate, the credential refusal and the copy limits are Python. A ZIP install can land on a machine with no interpreter, which turned those guarantees into silence. Each pack now checks once per project, before the first script call or the first generation, and records the result in `.ads-brain/runtime.json`. If Python is missing it says what stops working, proposes the install route for that operating system and asks; it never installs anything on its own. If the user declines, the pack keeps doing research and copy and states that the checks did not run.

## Version 2.0.0: renamed, and static by name

The four skills say what they build. Update any script or documentation that names the old identifiers.

| Old identifier | New identifier |
|---|---|
| `meta-ads-codex` | `meta-ads-static-codex` |
| `meta-ads-claude-code` | `meta-ads-static-claude-code` |
| `meta-ads-team-codex-and-claude-code` | `meta-ads-static-team-codex-and-claude-code` |
| `meta-ads-team-claude-code-and-codex` | `meta-ads-static-team-claude-code-and-codex` |

The archives follow the same pattern, `install-meta-ads-static-*.zip`, and the repository is now `claude-code-codex-ads-static`. GitHub redirects the previous repository URL, but update your remotes anyway. An installed old skill is not migrated automatically: back it up, remove it once you have copied any local edits, then install the renamed pack. Leaving both installed gives the assistant two overlapping skills to choose between.

Basic and advanced are also stated as modes rather than model tiers in this release. Any model the host exposes can run either mode; a stronger model sharpens each pass instead of unlocking it. Nothing about the required artifacts changed.

This rebuild replaces the initial four distributions while preserving their Git history. The earlier source and rendering helpers remain inspectable at [the previous revision](https://github.com/Nacha192/claude-code-codex-ads-static/tree/5880cca737db1b9e290d1d8d91d8ee220fb4bf7f). They are not silently executed or installed by this release.

The four current installation archives sit at the repository root, prefixed `install-`. Optional external tools are described in `you-can-install-tools.md`. Internal research, copywriting and second-brain modules are included in every pack.

The Claude-started team edition now has its own identifier, `meta-ads-static-team-claude-code-and-codex`. The Codex-started edition retains `meta-ads-static-team-codex-and-claude-code`. Both are complete advertising systems; their different entrypoints identify the starting host, not a permanent hierarchy.

## Version 1.3.0: these four packs are still creative only

Everything non-static left. The `video-voice.md` reference, the `codex-video` and `claude-video` top-ten selections, the 18 source adaptations routed to video or voice, the video and speech providers, and the `storyboard` artifact kind are no longer in these packs. They are staged in the [dynamic repository](https://github.com/Nacha192/claude-code-codex-ads-dynamic), with a note saying where each piece came from. Nothing was deleted, and the research record still lists all 73 inspected entrypoints; the packs now carry the 55 adaptations that apply to images and carousels.

If you were using one of these packs for video work, that path is gone rather than degraded, which is the point: a half-covered video workflow was worse than an explicit boundary. Ask for the video edition instead. If you kept `storyboard` artifacts, the checker now rejects the kind; the removed branch and its three tests are reproduced in that repository's `staging/transferred/TRANSFERRED.md`.

## Version 1.2.0: the checker refuses more than it used to

`check_artifact.py` gained a `generation_request` kind and now refuses, in every kind, any value shaped like a credential. A `creative` is also checked against character limits and against the campaign's declared `prohibited_terms`. An artifact that passed under 1.1.0 can fail here, which is the point: a batch that grew past its approved ceiling, a provider swapped after approval, a zero-credit account, copy over the placement limit and a red-line term in rendered copy all stop the run instead of passing quietly. The artifact `schema_v` stays `1.0.0`, since nothing was removed or given a new meaning. [SAFETY.md](SAFETY.md) lists what each script enforces and what it cannot.

If an older skill is installed, back up that skill folder and any local edits before replacing it. The installer refuses to overwrite a differing folder. Do not leave conflicting editions with the same identifier in multiple skill-discovery locations. Preserve private campaign records separately; never replace them with templates from a new release. Existing memory formats are not automatically migrated: map relevant records to the included schema and retain provenance before using them.
