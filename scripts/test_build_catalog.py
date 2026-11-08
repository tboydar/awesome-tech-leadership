#!/usr/bin/env python3
"""Unit tests for scripts/build_catalog.py (stdlib unittest, no deps)."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_catalog as bc  # noqa: E402

GOOD_ENTRY = """# Sample doc

## Section

### Test-Driven Development | TDD
<!-- entry:id=methodologies/tdd type=method roles=DEV,RD,QA tags=testing license=n/a last_verified=2026-11-08 -->
- **一句話**: Write the test first.
- **來源 Sources**: [Beck's book](https://example.com/tdd) — 書籍

### Some Tool | tool-x
<!-- entry:id=tools/tool-x type=tool roles=ALL tags=cli license=MIT last_verified=2026-11-08 -->
- **來源 Sources**: [repo](https://example.com/tool-x) — 開源 (MIT)
"""


class BuildCatalogTests(unittest.TestCase):
    def parse(self, text: str):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            (docs / "sample.md").write_text(text, encoding="utf-8")
            entries, errors = bc.parse_docs(docs)
            errors += bc.dedupe_check(entries)
            return entries, errors

    def test_parses_entries(self):
        entries, errors = self.parse(GOOD_ENTRY)
        self.assertEqual(errors, [])
        self.assertEqual(len(entries), 2)
        first = entries[0]
        self.assertEqual(first["id"], "methodologies/tdd")
        self.assertEqual(first["title"], "Test-Driven Development")
        self.assertEqual(first["title_short"], "TDD")
        self.assertEqual(first["roles"], ["DEV", "RD", "QA"])
        self.assertEqual(first["license"], "n/a")
        self.assertEqual(first["urls"], ["https://example.com/tdd"])

    def test_heading_without_metadata_is_error(self):
        entries, errors = self.parse("### Bare heading\n\nsome text\n")
        self.assertTrue(any("entry metadata" in e for e in errors))
        self.assertEqual(entries, [])

    def test_missing_required_keys_is_error(self):
        _, errors = self.parse(
            "### X | x\n<!-- entry:id=a/b type=method roles=ALL -->\n"
            "- [l](https://example.com)\n"
        )
        self.assertTrue(any("missing keys" in e for e in errors))

    def test_invalid_type_is_error(self):
        _, errors = self.parse(
            "### X | x\n<!-- entry:id=a/b type=vibes roles=ALL license=n/a last_verified=2026-11-08 -->\n"
            "- [l](https://example.com)\n"
        )
        self.assertTrue(any("invalid type" in e for e in errors))

    def test_entry_without_url_is_error(self):
        _, errors = self.parse(
            "### X | x\n<!-- entry:id=a/b type=method roles=ALL license=n/a last_verified=2026-11-08 -->\n"
            "- no links here\n"
        )
        self.assertTrue(any("no [Title]" in e for e in errors))

    def test_duplicate_id_is_error(self):
        entry = (
            "### X | x\n<!-- entry:id=dup/id type=method roles=ALL license=n/a last_verified=2026-11-08 -->\n"
            "- [l](https://example.com)\n\n"
        )
        entries, errors = self.parse(entry + entry)
        self.assertEqual(len(entries), 2)
        self.assertTrue(any("duplicate id" in e for e in errors))

    def test_stale_detection(self):
        entries = [{"id": "a/b", "source_file": "docs/x.md", "last_verified": "2020-01-01"}]
        warnings = bc.stale_entries(entries, today=date(2026, 11, 8))
        self.assertEqual(len(warnings), 1)
        fresh = [{"id": "c/d", "source_file": "docs/x.md", "last_verified": "2026-11-01"}]
        self.assertEqual(bc.stale_entries(fresh, today=date(2026, 11, 8)), [])

    def test_canonical_ignores_generated_at(self):
        a = {"generated_at": "2026-01-01T00:00:00Z", "entries": [1]}
        b = {"generated_at": "2027-05-05T09:09:09Z", "entries": [1]}
        self.assertEqual(bc.canonical(a), bc.canonical(b))

    def test_roundtrip_index_json(self):
        entries, errors = self.parse(GOOD_ENTRY)
        self.assertEqual(errors, [])
        index = bc.build_index(entries)
        parsed = json.loads(json.dumps(index, ensure_ascii=False))
        self.assertEqual(parsed["entry_count"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
