#!/usr/bin/env python3
"""Red-line check, run on the text a reader actually sees.

Why this is not a grep over the source file: an ad engine's own comments quote
the forbidden terms in order to explain why they are forbidden. A grep fires on
its own documentation, gets a reputation for crying wolf, and is switched off
within a week. So this executes the engine's templates in a minimal DOM stub,
collects only what the templates emit, strips the markup, and checks that.

    python redline_check.py                       engine.html + redline.txt
    python redline_check.py --engine ads.html --terms my-redline.txt
    python redline_check.py --text "some copy"    check a string instead

Exit code 0 when clean, 1 on a hit, 2 on a setup problem. Wire it into the
render step so a violating creative cannot reach the export folder.

Requires Node.js for the engine mode. The --text mode is pure Python.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

# A minimal DOM stub. The engine writes into innerHTML; we keep every write.
# Deliberately tiny: anything the engine needs beyond this is a signal that the
# engine is doing too much, not that the stub is too small.
HARNESS = r"""
const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const scripts = [...src.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
let collected = [];
const stub = {
  body: { setAttribute() {}, classList: { add() {}, remove() {} }, dataset: {} },
  documentElement: { style: { setProperty() {} } },
  getElementById: () => ({
    set innerHTML(v) { collected.push(String(v)); },
    get innerHTML() { return ''; },
    setAttribute() {}, appendChild() {}, style: {}, classList: { add() {}, remove() {} },
  }),
  querySelector: () => null,
  querySelectorAll: () => [],
  createElement: () => ({ style: {}, setAttribute() {}, appendChild() {} }),
  addEventListener() {},
  fonts: { ready: Promise.resolve() },
};
const ids = JSON.parse(process.argv[3]);
for (const id of ids) {
  for (const js of scripts) {
    try {
      new Function('location', 'document', 'window', js)(
        { search: `?ad=${id}&ratio=4x5`, href: '' },
        stub,
        { AD_LAYOUTS: [], addEventListener() {}, matchMedia: () => ({ matches: false }) }
      );
    } catch (e) {
      // A template that throws produced no visible text; that is a render bug,
      // not a red-line hit. Report it so it is not mistaken for a clean pass.
      console.error(`layout ${id}: ${e.message}`);
    }
  }
}
process.stdout.write(JSON.stringify(collected));
"""

DEFAULT_TERMS_FILE = "redline.txt"


def fold(text: str) -> str:
    """Lowercase, strip accents, collapse whitespace. So 'Soulagé' matches 'soulage'."""
    text = html.unescape(text)
    text = re.sub(r"<[^>]*>", " ", text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text).strip().lower()


def load_terms(path: Path) -> list[str]:
    if not path.exists():
        print(f"No red-line file at {path}.", file=sys.stderr)
        print("Write one: 10-20 forbidden terms for this product, one per line,", file=sys.stderr)
        print("'#' for comments. See reference/compliance.md.", file=sys.stderr)
        sys.exit(2)
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            terms.append(fold(line))
    if not terms:
        print(f"{path} contains no terms.", file=sys.stderr)
        sys.exit(2)
    return terms


def rendered_text(engine: Path, ids: list[int]) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as fh:
        fh.write(HARNESS)
        harness = fh.name
    try:
        proc = subprocess.run(
            ["node", harness, str(engine), json.dumps(ids)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError:
        print("Node.js is required to execute the engine templates.", file=sys.stderr)
        sys.exit(2)
    finally:
        os.unlink(harness)

    if proc.stderr.strip():
        print(proc.stderr.strip(), file=sys.stderr)
    if proc.returncode != 0:
        print("The engine could not be executed.", file=sys.stderr)
        sys.exit(2)
    try:
        parts = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        print("The harness returned no usable output.", file=sys.stderr)
        sys.exit(2)
    return " ".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--engine", default="engine.html")
    ap.add_argument("--terms", default=DEFAULT_TERMS_FILE)
    ap.add_argument("--ids", default="1-16", help="layout ids, e.g. 1-16 or 1,4,8")
    ap.add_argument("--text", help="check this string instead of an engine")
    ap.add_argument("--show", action="store_true", help="print the visible text")
    args = ap.parse_args()

    terms = load_terms(Path(args.terms))

    if args.text is not None:
        visible = fold(args.text)
    else:
        engine = Path(args.engine)
        if not engine.exists():
            print(f"Engine not found: {engine}", file=sys.stderr)
            return 2
        if "-" in args.ids:
            lo, hi = args.ids.split("-", 1)
            ids = list(range(int(lo), int(hi) + 1))
        else:
            ids = [int(x) for x in args.ids.split(",") if x.strip()]
        visible = fold(rendered_text(engine, ids))

    if not visible:
        print("No visible text was produced. Nothing was checked, so this is", file=sys.stderr)
        print("NOT a pass. Fix the engine or the ids before shipping.", file=sys.stderr)
        return 2

    hits = sorted({t for t in terms if t in visible})

    if args.show:
        print("--- visible text ---")
        print(visible)
        print("--- end ---")

    if hits:
        print(f"RED LINE: {len(hits)} forbidden term(s) in the rendered text:")
        for h in hits:
            idx = visible.find(h)
            ctx = visible[max(0, idx - 45): idx + len(h) + 45]
            print(f"  - {h!r}  ...{ctx}...")
        return 1

    print(f"RED LINE: clean. {len(terms)} term(s) checked against "
          f"{len(visible)} characters of rendered text.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
