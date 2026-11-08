#!/usr/bin/env python3
"""Build catalog/index.json from entry metadata in docs/*.md.

Single source of truth: docs/*.md (human-readable, bilingual).
Generated artifact: catalog/index.json (machine-readable, for search/tooling).

Usage:
    python3 scripts/build_catalog.py            # regenerate catalog/index.json
    python3 scripts/build_catalog.py --check    # verify metadata + index in sync
    python3 scripts/build_catalog.py --check --strict   # also fail on stale entries

Entry grammar (see catalog/schema.md):
    ### <Title> | <Short Name>
    <!-- entry:id=<category>/<slug> type=<type> roles=<A,B> tags=<t1,t2> license=<SPDX|n/a|proprietary> last_verified=YYYY-MM-DD -->
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
INDEX_PATH = REPO_ROOT / "catalog" / "index.json"

VALID_TYPES = {
    "method", "skill", "mcp", "prompt", "loop", "tool", "platform",
    "paper", "guide", "policy", "benchmark",
}
VALID_ROLES = {"PM", "QA", "DEV", "RD", "SRE", "PLATFORM", "ERP", "EM", "DATA", "ALL"}
REQUIRED_KEYS = {"id", "type", "roles", "license", "last_verified"}
STALE_DAYS = 90

HEADING_RE = re.compile(r"^###\s+(?P<title>.+?)\s*$")
ENTRY_RE = re.compile(r"^<!--\s*entry:(?P<meta>.*?)\s*-->\s*$")
KV_RE = re.compile(r"(\w+)=(\S+)")
URL_RE = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)")


def parse_meta(meta_str: str) -> dict[str, str]:
    return {k: v for k, v in KV_RE.findall(meta_str)}


def rel(path: Path) -> str:
    """Path relative to repo root; fall back to the filename outside it (tests)."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return path.name


def split_title(raw: str) -> tuple[str, str]:
    if "|" in raw:
        title, short = (part.strip() for part in raw.split("|", 1))
        return title, short
    return raw, raw


def parse_docs(docs_dir: Path) -> tuple[list[dict], list[str]]:
    entries: list[dict] = []
    errors: list[str] = []
    for md_file in sorted(docs_dir.glob("*.md")):
        lines = md_file.read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(lines):
            m = HEADING_RE.match(lines[i])
            if not m:
                i += 1
                continue
            title_raw = m.group("title")
            loc = f"{rel(md_file)}:{i + 1}"
            if i + 1 >= len(lines):
                errors.append(f"{loc}: heading '{title_raw}' has no entry metadata line")
                i += 1
                continue
            em = ENTRY_RE.match(lines[i + 1])
            if not em:
                errors.append(
                    f"{loc}: heading '{title_raw}' must be followed by an entry metadata line: "
                    f"'<!-- entry:id=... type=... roles=... license=... last_verified=... -->'"
                )
                i += 1
                continue
            meta = parse_meta(em.group("meta"))
            missing = REQUIRED_KEYS - meta.keys()
            if missing:
                errors.append(f"{loc}: entry '{title_raw}' missing keys: {sorted(missing)}")
            if "type" in meta and meta["type"] not in VALID_TYPES:
                errors.append(f"{loc}: invalid type '{meta['type']}' (allowed: {sorted(VALID_TYPES)})")
            roles = [r.strip().upper() for r in meta.get("roles", "").split(",") if r.strip()]
            bad_roles = [r for r in roles if r not in VALID_ROLES]
            if bad_roles:
                errors.append(f"{loc}: invalid roles {bad_roles} (allowed: {sorted(VALID_ROLES)})")
            if "last_verified" in meta:
                try:
                    date.fromisoformat(meta["last_verified"])
                except ValueError:
                    errors.append(f"{loc}: last_verified must be YYYY-MM-DD, got '{meta['last_verified']}'")

            body: list[str] = []
            j = i + 2
            while j < len(lines) and not lines[j].startswith("## "):
                if HEADING_RE.match(lines[j]):
                    break
                body.append(lines[j])
                j += 1
            urls = sorted({u for line in body for u in URL_RE.findall(line)})
            if not urls:
                errors.append(f"{loc}: entry '{title_raw}' has no [Title](https://...) source link")

            title, short = split_title(title_raw)
            entries.append({
                "id": meta.get("id", ""),
                "title": title,
                "title_short": short,
                "type": meta.get("type", ""),
                "roles": roles,
                "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
                "license": meta.get("license", ""),
                "last_verified": meta.get("last_verified", ""),
                "source_file": rel(md_file),
                "urls": urls,
            })
            i = j
    return entries, errors


def dedupe_check(entries: list[dict]) -> list[str]:
    errors: list[str] = []
    seen: dict[str, str] = {}
    for e in entries:
        if not e["id"]:
            continue
        if e["id"] in seen:
            errors.append(f"duplicate id '{e['id']}' in {e['source_file']} (also in {seen[e['id']]})")
        seen[e["id"]] = e["source_file"]
    return errors


def stale_entries(entries: list[dict], today: date | None = None) -> list[str]:
    today = today or date.today()
    warnings: list[str] = []
    for e in entries:
        if not e["last_verified"]:
            continue
        verified = date.fromisoformat(e["last_verified"])
        age = (today - verified).days
        if age > STALE_DAYS:
            warnings.append(f"[STALE {age}d] {e['id']} ({e['source_file']}) — re-verify links and bump last_verified")
    return warnings


def build_index(entries: list[dict]) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "entry_count": len(entries),
        "entries": sorted(entries, key=lambda e: (e["source_file"], e["id"])),
    }


def canonical(index: dict) -> str:
    body = {k: v for k, v in index.items() if k != "generated_at"}
    return json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify instead of writing")
    parser.add_argument("--strict", action="store_true", help="with --check, fail on stale entries too")
    args = parser.parse_args()

    if not DOCS_DIR.is_dir():
        print(f"ERROR: docs directory not found: {DOCS_DIR}", file=sys.stderr)
        return 2

    entries, errors = parse_docs(DOCS_DIR)
    errors += dedupe_check(entries)
    warnings = stale_entries(entries)

    if errors:
        print("Metadata errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
    if warnings:
        print(f"Stale entries (>{STALE_DAYS} days since last_verified):")
        for warn in warnings:
            print(f"  - {warn}")

    if args.check:
        if errors:
            return 1
        if not INDEX_PATH.is_file():
            print(f"ERROR: {INDEX_PATH} missing — run scripts/build_catalog.py", file=sys.stderr)
            return 1
        existing = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        if canonical(existing) != canonical(build_index(entries)):
            print("ERROR: catalog/index.json is out of date — run scripts/build_catalog.py", file=sys.stderr)
            return 1
        if warnings and args.strict:
            print("ERROR: --strict mode, stale entries present", file=sys.stderr)
            return 1
        print(f"OK: {len(entries)} entries, metadata valid, index in sync")
        return 0

    if errors:
        return 1
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(
        json.dumps(build_index(entries), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {INDEX_PATH.relative_to(REPO_ROOT)} with {len(entries)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
