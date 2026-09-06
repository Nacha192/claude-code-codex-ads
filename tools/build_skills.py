#!/usr/bin/env python3
"""Assemble the four skill distributions from _src, then zip them.

    python tools/build_skills.py            build folders and zips
    python tools/build_skills.py --check    verify the folders match _src, build nothing

_src holds each file once. This script copies the shared brain into all four
distributions and substitutes the per-runtime tokens, so a correction to
reference/thresholds.md lands in every skill instead of in one of them.

--check is what CI runs: it rebuilds into a temporary directory and compares.
A drift means somebody edited a distribution instead of _src, and the next
build would silently revert their work.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"

SHARED_REFERENCE = [
    "intake-and-avatar.md",
    "scraping.md",
    "hooks.md",
    "copywriting.md",
    "static-ads.md",
    "video-ads.md",
    "voice.md",
    "generation-tools.md",
    "thresholds.md",
    "compliance.md",
    "output-standard.md",
    "depth-modes.md",
]

SCRIPTS = [
    "ad_library_url.mjs",
    "ad_engine_template.html",
    "render_ads.mjs",
    "redline_check.py",
]

CODEX_TOKENS = {
    "{{STANDARD_MODEL}}": "GPT-5.6",
    "{{DEEP_MODEL}}": "Astra-6",
    "{{DEPTH_NOTE}}": (
        "The model names are the intended targets, not a guarantee. Inspect what "
        "your session actually offers, and never claim a model switch that was "
        "made only by writing its name in a prompt. Where the named model is "
        "unavailable, say so and ask the user which of the available ones to run."
    ),
    "{{SELF}}": "Codex",
    "{{OTHER}}": "Claude Code",
}

CLAUDE_TOKENS = {
    "{{STANDARD_MODEL}}": "Opus 5",
    "{{DEEP_MODEL}}": "Opus 5, maximum reasoning effort",
    "{{DEPTH_NOTE}}": (
        "Both modes run on the same model here. The depth comes from the reasoning "
        "effort and from the six passes below, not from a different model, so the "
        "difference is entirely in work performed. Never claim a depth mode whose "
        "passes produced no artefact."
    ),
    "{{SELF}}": "Claude Code",
    "{{OTHER}}": "Codex",
}

# dist name -> (skill name, runtime, kind)
DISTS = {
    "codex-solo": ("meta-ads-codex", "codex", "solo"),
    "claude-code-solo": ("meta-ads-claude-code", "claude", "solo"),
    "codex-duo": ("meta-ads-team-codex-and-claude-code", "codex", "duo"),
    "claude-code-duo": ("meta-ads-team-codex-and-claude-code", "claude", "duo"),
}


def substitute(text: str, tokens: dict[str, str], dist: str, skill: str) -> str:
    text = text.replace("{{SKILL_NAME}}", skill).replace("{{DIST}}", dist)
    for token, value in tokens.items():
        text = text.replace(token, value)
    return text


def check_no_tokens(path: Path, text: str) -> list[str]:
    import re

    leftover = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", text)))
    return [f"{path}: unsubstituted {t}" for t in leftover]


def build_one(dist: str, target: Path) -> list[str]:
    skill, runtime, kind = DISTS[dist]
    tokens = CODEX_TOKENS if runtime == "codex" else CLAUDE_TOKENS
    problems: list[str] = []

    root = target / f"you-can-install-{dist}"
    if root.exists():
        shutil.rmtree(root)
    (root / "reference").mkdir(parents=True)
    (root / "scripts").mkdir(parents=True)

    # SKILL.md
    if kind == "solo":
        skill_src = SRC / runtime / "SKILL-solo.md"
    else:
        skill_src = SRC / "duo" / "SKILL-duo.md"
    body = substitute(skill_src.read_text(encoding="utf-8"), tokens, dist, skill)
    problems += check_no_tokens(root / "SKILL.md", body)
    (root / "SKILL.md").write_text(body, encoding="utf-8")

    # INSTALLATION.md
    install_src = SRC / "install" / f"INSTALLATION-{'codex' if runtime == 'codex' else 'claude'}.md"
    body = substitute(install_src.read_text(encoding="utf-8"), tokens, dist, skill)
    problems += check_no_tokens(root / "INSTALLATION.md", body)
    (root / "INSTALLATION.md").write_text(body, encoding="utf-8")

    # agents/openai.yaml, Codex only
    if runtime == "codex":
        (root / "agents").mkdir()
        yaml = (SRC / "codex" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        if kind == "duo":
            yaml = (
                yaml.replace("Meta Ads for Codex", "Meta Ads, Codex and Claude Code")
                .replace(
                    "Research, write and verify Meta ad creatives",
                    "Build Meta ads as a pair, by declared capability",
                )
                .replace("$meta-ads-codex", "$meta-ads-team-codex-and-claude-code")
                .replace("allow_implicit_invocation: true", "allow_implicit_invocation: false")
            )
        (root / "agents" / "openai.yaml").write_text(yaml, encoding="utf-8")

    # shared reference
    for name in SHARED_REFERENCE:
        body = substitute((SRC / "reference" / name).read_text(encoding="utf-8"), tokens, dist, skill)
        problems += check_no_tokens(root / "reference" / name, body)
        (root / "reference" / name).write_text(body, encoding="utf-8")

    # duo-only reference
    if kind == "duo":
        for name in ("roles.md", "handoffs.md"):
            body = substitute((SRC / "duo" / name).read_text(encoding="utf-8"), tokens, dist, skill)
            problems += check_no_tokens(root / "reference" / name, body)
            (root / "reference" / name).write_text(body, encoding="utf-8")
        card = (SRC / "codex" / "CAPACITES.md").read_text(encoding="utf-8")
        (root / "reference" / "capability-card-example.md").write_text(card, encoding="utf-8")

    # scripts
    for name in SCRIPTS:
        shutil.copy2(SRC / "scripts" / name, root / "scripts" / name)

    return problems


def make_zip(dist: str) -> Path:
    skill = DISTS[dist][0]
    folder = ROOT / f"you-can-install-{dist}"
    out = ROOT / f"INSTALL-{dist}.zip"
    if out.exists():
        out.unlink()
    # The archive contains the SKILL folder, so unzipping into a skills
    # directory lands SKILL.md at the right depth.
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                zf.write(path, Path(skill) / path.relative_to(folder))
    return out


def compare(a: Path, b: Path) -> list[str]:
    diff = filecmp.dircmp(a, b)
    out = []

    def walk(d: filecmp.dircmp, prefix: str = "") -> None:
        for name in d.left_only:
            out.append(f"only in built output: {prefix}{name}")
        for name in d.right_only:
            out.append(f"only in repository: {prefix}{name}")
        for name in d.diff_files:
            out.append(f"differs from _src: {prefix}{name}")
        for name, sub in d.subdirs.items():
            walk(sub, f"{prefix}{name}/")

    walk(diff)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="verify, do not write")
    args = ap.parse_args()

    if not SRC.is_dir():
        print(f"_src not found at {SRC}", file=sys.stderr)
        return 2

    if args.check:
        problems: list[str] = []
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            for dist in DISTS:
                problems += build_one(dist, tmpdir)
                built = tmpdir / f"you-can-install-{dist}"
                shipped = ROOT / f"you-can-install-{dist}"
                if not shipped.exists():
                    problems.append(f"missing distribution: you-can-install-{dist}")
                    continue
                problems += [f"{dist}: {p}" for p in compare(built, shipped)]
        if problems:
            print("BUILD CHECK FAILED")
            for p in problems:
                print(f"  - {p}")
            print("\nEdit _src, then run: python tools/build_skills.py")
            return 1
        print(f"BUILD CHECK: {len(DISTS)} distributions match _src.")
        return 0

    problems = []
    for dist in DISTS:
        problems += build_one(dist, ROOT)
        z = make_zip(dist)
        n = sum(1 for p in (ROOT / f"you-can-install-{dist}").rglob("*") if p.is_file())
        print(f"{dist:20} {n:>3} files  ->  {z.name} ({z.stat().st_size // 1024} KB)")

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(f"  - {p}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
