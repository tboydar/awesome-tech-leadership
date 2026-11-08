#!/usr/bin/env python3
"""Validate Mermaid diagram blocks in all Markdown files.

Static checks (always): blocks are non-empty and start with a known diagram type.
Render checks (--render): every block actually renders via mermaid-cli (mmdc).

Usage:
    python3 scripts/check_mermaid.py              # static checks only
    python3 scripts/check_mermaid.py --render     # + full render validation (needs mmdc)
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

KNOWN_TYPES = {
    "flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram",
    "stateDiagram-v2", "erDiagram", "journey", "gantt", "pie", "mindmap",
    "timeline", "gitGraph", "quadrantChart", "requirementDiagram", "C4Context",
    "C4Container", "C4Component", "C4Dynamic", "C4Deployment", "sankey-beta",
    "xychart-beta", "block-beta", "packet-beta", "kanban",
}
FENCE_RE = re.compile(r"^```mermaid\s*$")
STATIC_HEAD_RE = re.compile(
    r"^\s*(?:" + "|".join(re.escape(t) for t in sorted(KNOWN_TYPES)) + r")\b"
)


def find_blocks() -> list[tuple[Path, int, list[str]]]:
    blocks: list[tuple[Path, int, list[str]]] = []
    for md in sorted(REPO_ROOT.rglob("*.md")):
        if "node_modules" in md.parts or ".git" in md.parts:
            continue
        lines = md.read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(lines):
            if FENCE_RE.match(lines[i]):
                start = i + 1
                body: list[str] = []
                i += 1
                while i < len(lines) and not lines[i].startswith("```"):
                    body.append(lines[i])
                    i += 1
                blocks.append((md, start, body))
            i += 1
    return blocks


def static_check(blocks) -> list[str]:
    errors = []
    for md, start, body in blocks:
        loc = f"{md.name}:{start}"
        text = "\n".join(body).strip()
        if not text:
            errors.append(f"{loc}: empty mermaid block")
        elif not STATIC_HEAD_RE.match(text):
            head = text.splitlines()[0][:40]
            errors.append(f"{loc}: unknown diagram type in first line: '{head}'")
    return errors


def render_check(blocks) -> list[str]:
    errors = []
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        for idx, (md, start, body) in enumerate(blocks):
            src = tmpdir / f"block-{idx}.mmd"
            dst = tmpdir / f"block-{idx}.svg"
            src.write_text("\n".join(body) + "\n", encoding="utf-8")
            proc = subprocess.run(
                ["mmdc", "-i", str(src), "-o", str(dst)],
                capture_output=True, text=True,
            )
            if proc.returncode != 0:
                loc = f"{md.name}:{start}"
                tail = (proc.stderr or proc.stdout).strip().splitlines()[-3:]
                errors.append(f"{loc}: render failed — {' | '.join(tail)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true",
                        help="render every block with mermaid-cli (mmdc must be installed)")
    args = parser.parse_args()

    blocks = find_blocks()
    errors = static_check(blocks)
    if args.render and not errors:
        try:
            subprocess.run(["mmdc", "--version"], capture_output=True, check=True)
        except (OSError, subprocess.CalledProcessError):
            print("ERROR: mmdc not found — install with: npm i -g @mermaid-js/mermaid-cli",
                  file=sys.stderr)
            return 2
        errors += render_check(blocks)

    if errors:
        print("Mermaid errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    mode = "static+render" if args.render else "static"
    print(f"OK: {len(blocks)} mermaid blocks valid ({mode} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
