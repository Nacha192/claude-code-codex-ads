# Migration from the initial distribution

This rebuild replaces the initial four distributions while preserving their Git history. The earlier source and rendering helpers remain inspectable at [the previous revision](https://github.com/Nacha192/claude-code-codex-ads/tree/5880cca737db1b9e290d1d8d91d8ee220fb4bf7f). They are not silently executed or installed by this release.

The four current installation archives sit at the repository root, prefixed `install-`. Optional external tools are described in `you-can-install-tools.md`. Internal research, copywriting and second-brain modules are included in every pack.

The Claude-started team edition now has its own identifier, `meta-ads-team-claude-code-and-codex`. The Codex-started edition retains `meta-ads-team-codex-and-claude-code`. Both are complete advertising systems; their different entrypoints identify the starting host, not a permanent hierarchy.

## Version 1.2.0: the checker refuses more than it used to

`check_artifact.py` gained a `generation_request` kind and now refuses, in every kind, any value shaped like a credential. A `creative` is also checked against character limits and against the campaign's declared `prohibited_terms`. An artifact that passed under 1.1.0 can fail here, which is the point: a batch that grew past its approved ceiling, a provider swapped after approval, a zero-credit account, copy over the placement limit and a red-line term in rendered copy all stop the run instead of passing quietly. The artifact `schema_v` stays `1.0.0`, since nothing was removed or given a new meaning. [SAFETY.md](SAFETY.md) lists what each script enforces and what it cannot.

If an older skill is installed, back up that skill folder and any local edits before replacing it. The installer refuses to overwrite a differing folder. Do not leave conflicting editions with the same identifier in multiple skill-discovery locations. Preserve private campaign records separately; never replace them with templates from a new release. Existing memory formats are not automatically migrated: map relevant records to the included schema and retain provenance before using them.
