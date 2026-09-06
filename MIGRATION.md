# Migration from the initial distribution

This rebuild replaces the initial four distributions while preserving their Git history. The earlier source and rendering helpers remain inspectable at [the previous revision](https://github.com/Nacha192/claude-code-codex-ads/tree/5880cca737db1b9e290d1d8d91d8ee220fb4bf7f). They are not silently executed or installed by this release.

The four current installation archives are under `dist/`, prefixed `install-`. Optional external tools are described in `you-can-install-tools.md`. Internal research, copywriting and second-brain modules are included in every pack.

The Claude-started team edition now has its own identifier, `meta-ads-team-claude-code-and-codex`. The Codex-started edition retains `meta-ads-team-codex-and-claude-code`. Both are complete advertising systems; their different entrypoints identify the starting host, not a permanent hierarchy.

If an older skill is installed, back up that skill folder and any local edits before replacing it. The installer refuses to overwrite a differing folder. Do not leave conflicting editions with the same identifier in multiple skill-discovery locations. Preserve private campaign records separately; never replace them with templates from a new release. Existing memory formats are not automatically migrated: map relevant records to the included schema and retain provenance before using them.
