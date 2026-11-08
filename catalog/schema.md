# Catalog Schema / 索引格式說明

`catalog/index.json` is **generated** — never edit it by hand. Run
`python3 scripts/build_catalog.py` after editing `docs/*.md`.

`catalog/index.json` 為**自動生成**，請勿手動修改。編輯 `docs/*.md` 後執行
`python3 scripts/build_catalog.py` 重新產生。

## Entry metadata / 條目中繼資料

Each catalog entry lives in `docs/*.md` as a level-3 heading followed by an
HTML comment carrying machine-readable metadata:

每則條目以三級標題 + HTML 註解承載機器可讀中繼資料：

```markdown
### Test-Driven Development | TDD
<!-- entry:id=methodologies/tdd type=method roles=DEV,RD,QA tags=testing,agile license=n/a last_verified=2026-11-08 -->
- **一句話**: Write the test first, then the minimum code to pass it.
- **一句話（繁中）**: 先寫測試，再寫剛好讓測試通過的程式碼。
- **來源 Sources**: [Test-Driven Development by Example (book)](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530) — 書籍
```

## Fields / 欄位

| Field | Required | Values / Format | 說明 |
|---|---|---|---|
| `id` | yes | `<category>/<slug>` unique | stable identifier, used for cross-references |
| `type` | yes | `method` `skill` `mcp` `prompt` `loop` `tool` `platform` `paper` `guide` `policy` `benchmark` | resource kind |
| `roles` | yes | comma list of: `PM` `QA` `DEV` `RD` `SRE` `PLATFORM` `ERP` `EM` `DATA` `ALL` | who this is for |
| `tags` | no | comma list, lowercase kebab-case | free-form topic tags |
| `license` | yes | SPDX id (e.g. `MIT`, `Apache-2.0`), `n/a` for non-code, or `proprietary` | open-source compliance |
| `last_verified` | yes | `YYYY-MM-DD` | date a maintainer last confirmed the links resolve |

## Generated index / 產生的索引

```json
{
  "generated_at": "2026-11-08T00:00:00Z",
  "entries": [
    {
      "id": "methodologies/tdd",
      "title": "Test-Driven Development",
      "title_short": "TDD",
      "type": "method",
      "roles": ["DEV", "RD", "QA"],
      "tags": ["testing", "agile"],
      "license": "n/a",
      "last_verified": "2026-11-08",
      "source_file": "docs/01-methodologies.md",
      "urls": ["https://www.amazon.com/..."]
    }
  ]
}
```

## Freshness rule / 保鮮規則

CI runs `build_catalog.py --check`:

1. every `### ` heading in `docs/*.md` must carry a valid `<!-- entry:... -->` line;
2. `catalog/index.json` must match a freshly generated one;
3. entries with `last_verified` older than 90 days are reported (warning) so
   maintainers re-verify the links.

CI 執行 `build_catalog.py --check`：驗證每則條目 metadata 完整、索引同步、
並列出超過 90 天未驗證的條目供維護者重新查核連結。
