#!/usr/bin/env python3
"""Tests for the four skill distributions.

    python -m pytest tests/ -q
    python tests/test_skills.py          runs without pytest

These check the things that silently break a skill: missing front matter, a
reference file cited by SKILL.md that does not exist, an unsubstituted token, a
zip whose contents sit at the wrong depth, and a distribution edited by hand
instead of in _src.
"""

from __future__ import annotations

import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DISTS = {
    "codex-solo": "meta-ads-codex",
    "claude-code-solo": "meta-ads-claude-code",
    "codex-duo": "meta-ads-team-codex-and-claude-code",
    "claude-code-duo": "meta-ads-team-codex-and-claude-code",
}
FAILURES: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip()
    return out


def test_front_matter() -> None:
    """Every SKILL.md has a name matching its distribution, and a description."""
    for dist, skill in DISTS.items():
        path = ROOT / f"you-can-install-{dist}" / "SKILL.md"
        check(path.exists(), f"{dist}: SKILL.md missing")
        if not path.exists():
            continue
        fm = front_matter(path.read_text(encoding="utf-8"))
        check(fm.get("name") == skill, f"{dist}: name is {fm.get('name')!r}, expected {skill!r}")
        desc = fm.get("description", "")
        check(len(desc) > 60, f"{dist}: description too short to route on ({len(desc)} chars)")


def test_no_unsubstituted_tokens() -> None:
    """A leftover {{TOKEN}} means the build did not fill it in."""
    for dist in DISTS:
        for path in (ROOT / f"you-can-install-{dist}").rglob("*.md"):
            found = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", path.read_text(encoding="utf-8"))))
            check(not found, f"{dist}: {path.name} has unsubstituted {found}")


def test_referenced_files_exist() -> None:
    """Every reference/<name>.md and scripts/<name> cited by SKILL.md is present."""
    pattern = re.compile(r"`?(reference/[\w.-]+\.md|scripts/[\w.-]+)`?")
    for dist in DISTS:
        root = ROOT / f"you-can-install-{dist}"
        skill = root / "SKILL.md"
        if not skill.exists():
            continue
        for rel in sorted(set(pattern.findall(skill.read_text(encoding="utf-8")))):
            check((root / rel).exists(), f"{dist}: SKILL.md cites {rel}, which does not exist")


def test_model_tokens_are_per_runtime() -> None:
    """Codex distributions name GPT-5.6 and Astra-6. Claude Code ones name Opus 5."""
    for dist in DISTS:
        depth = (ROOT / f"you-can-install-{dist}" / "reference" / "depth-modes.md")
        if not depth.exists():
            check(False, f"{dist}: depth-modes.md missing")
            continue
        text = depth.read_text(encoding="utf-8")
        if dist.startswith("codex"):
            check("GPT-5.6" in text and "Astra-6" in text, f"{dist}: expected the Codex model names")
            check("Opus 5" not in text, f"{dist}: leaked a Claude Code model name")
        else:
            check("Opus 5" in text, f"{dist}: expected Opus 5")
            check("Astra-6" not in text, f"{dist}: leaked a Codex model name")


def test_duo_has_roles_and_handoffs() -> None:
    for dist in ("codex-duo", "claude-code-duo"):
        ref = ROOT / f"you-can-install-{dist}" / "reference"
        for name in ("roles.md", "handoffs.md"):
            check((ref / name).exists(), f"{dist}: reference/{name} missing")
    for dist in ("codex-solo", "claude-code-solo"):
        ref = ROOT / f"you-can-install-{dist}" / "reference"
        check(not (ref / "roles.md").exists(), f"{dist}: solo distribution should not ship roles.md")


def test_codex_yaml_location() -> None:
    """openai.yaml lives in agents/, inside the skill. At the root it is ignored."""
    for dist in ("codex-solo", "codex-duo"):
        root = ROOT / f"you-can-install-{dist}"
        check((root / "agents" / "openai.yaml").exists(), f"{dist}: agents/openai.yaml missing")
        check(not (root / "openai.yaml").exists(), f"{dist}: openai.yaml must not sit at the root")
    for dist in ("claude-code-solo", "claude-code-duo"):
        root = ROOT / f"you-can-install-{dist}"
        check(not (root / "agents").exists(), f"{dist}: Claude Code skills carry no agents/ folder")


def test_zip_depth() -> None:
    """Unzipping must produce <skill-name>/SKILL.md, not a bare SKILL.md."""
    for dist, skill in DISTS.items():
        z = ROOT / f"INSTALL-{dist}.zip"
        check(z.exists(), f"{dist}: INSTALL-{dist}.zip missing")
        if not z.exists():
            continue
        with zipfile.ZipFile(z) as zf:
            names = zf.namelist()
        check(f"{skill}/SKILL.md" in names, f"{dist}: zip does not contain {skill}/SKILL.md")
        check(
            all(n.startswith(f"{skill}/") for n in names),
            f"{dist}: zip has entries outside {skill}/",
        )


def test_no_secrets_shipped() -> None:
    """Nothing that looks like a credential, and no .env, reaches a distribution."""
    pattern = re.compile(
        r"(sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}"
        r"|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
    )
    for dist in DISTS:
        for path in (ROOT / f"you-can-install-{dist}").rglob("*"):
            if not path.is_file():
                continue
            check(path.name != ".env", f"{dist}: a .env file is in the distribution")
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            check(not pattern.search(text), f"{dist}: {path.name} contains a credential-shaped value")


def test_thresholds_keys_resolve() -> None:
    """Every threshold key cited anywhere is defined in thresholds.md."""
    # A key, not a file name: voice.md is a reference file, voice.worth_it_rule is a key.
    key = re.compile(
        r"`((?:limits|ratios|coverage|scrape|test|money|gen|voice|lang|early|fatigue)"
        r"\.(?!md\b)[a-z_0-9.]+)`"
    )
    for dist in DISTS:
        root = ROOT / f"you-can-install-{dist}"
        thresholds = root / "reference" / "thresholds.md"
        if not thresholds.exists():
            continue
        defined = set(key.findall(thresholds.read_text(encoding="utf-8")))
        for path in root.rglob("*.md"):
            for cited in set(key.findall(path.read_text(encoding="utf-8"))):
                check(
                    cited in defined,
                    f"{dist}: {path.name} cites `{cited}`, undefined in thresholds.md",
                )


def test_build_is_reproducible() -> None:
    """The shipped folders match what _src produces. Edit _src, never a distribution."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_skills.py"), "--check"],
        capture_output=True,
        text=True,
    )
    check(result.returncode == 0, f"build check failed:\n{result.stdout}{result.stderr}")


def test_redline_check_runs() -> None:
    """The red-line script exits 0 on clean text and non-zero on a hit."""
    script = ROOT / "you-can-install-codex-solo" / "scripts" / "redline_check.py"
    if not script.exists():
        check(False, "redline_check.py missing from the distribution")
        return
    terms = ROOT / "tests" / "_terms.tmp"
    terms.write_text("forbidden\nelastique\n", encoding="utf-8")
    try:
        clean = subprocess.run(
            [sys.executable, str(script), "--text", "3 a.m. It is still there.", "--terms", str(terms)],
            capture_output=True, text=True,
        )
        check(clean.returncode == 0, f"clean text should exit 0, got {clean.returncode}")
        hit = subprocess.run(
            [sys.executable, str(script), "--text", "A forbidden claim.", "--terms", str(terms)],
            capture_output=True, text=True,
        )
        check(hit.returncode == 1, f"a hit should exit 1, got {hit.returncode}")
    finally:
        terms.unlink(missing_ok=True)


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        before = len(FAILURES)
        fn()
        status = "ok" if len(FAILURES) == before else "FAIL"
        print(f"{status:>4}  {fn.__name__}")
    if FAILURES:
        print(f"\n{len(FAILURES)} failure(s):")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print(f"\n{len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
