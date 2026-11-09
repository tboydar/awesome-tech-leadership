# TODO / 待辦清單

> Concretely actionable follow-ups from the 2026-11-09 launch.
> 建置（2026-11-09 上線）後續的具體待辦。Roadmap-level items live in
> [feature-plan.md](feature-plan.md)；這裡只放可直接開工的項目。

## 1. 來源補遺與保鮮 / Source gaps & freshness

- [ ] **重試研究階段剔除的 UNVERIFIED 項目**（找到官方來源就收錄，找不到維持不收）：
  - [ ] DataOps Manifesto — 原 URL 連線失敗，找官網或作者正式發布頁
  - [ ] IDP Maturity Model — 同上
  - [ ] Amazon Working Backwards — 尋找 AWS 官方文件/官方白皮書
  - [ ] SAP clean core / Fit-to-Standard — help.sap.com 文件當時無法驗證，重試並確認直鏈
  - [ ] QwQ-32B / DeepSeek-V4.1-Flash 等第三方 arXiv ID — 以官方 model card 的論文連結為準
- [ ] **xAI 工程分享追蹤** — 目前無 engineering blog、無論文（docs/04 已誠實標註）；每季複查 x.ai 官方發布管道
- [ ] **Star 快照更新** — docs/02 的 stars 是 2026-11-08 快照；建立自動更新（見 feature-plan v0.5）或手動每季刷新一次 `last_verified`
- [ ] **403 bot 牆站台人工複驗** — openai.com / sap.com / netsuite.com / perplexity.ai / oreilly.com / acm.org / iso.org / npmjs.com 的連結 CI 視為通過（403=bot 牆），每季用瀏覽器人工抽點確認頁面仍存在
- [ ] **90 天保鮮循環** — `python3 scripts/build_catalog.py --check` 的 [STALE] 清單開始出現後（2027-02 起），逐批重驗並 bump `last_verified`

## 2. 品質檢查 / Quality

- [ ] **簡體字全檔掃描** — 轉檔 agents 各自檢查過，但沒跑過全 repo 自動掃描（可用 `rg -P '[\x{4e00}-\x{9fff}]'` 搭配簡體字表過濾）
- [ ] **雙語一致性抽檢** — 條目「一句話 / 一句話（繁中）」成對性（scripts/build_catalog.py 可加 `--check` 規則：每個條目須含兩行）
- [ ] **內部 anchor 連結驗證** — README「快速上手」表連到 docs/ 的相對連結、條目內互引；lychee 查 HTTP 但不查頁內 anchor
- [ ] **條目長度一致性** — 各 doc 的條目資訊量落差（03 的 57 條 vs 05 的 123 條），抽檢是否有過短條目需要補充

## 3. 安全與治理 / Security & governance

- [ ] **mail-link fixture 驗證** — 安全審查建議：用含 `a@b.co`（裸郵箱）、`<a@b.co>`、`MAILTO:a@b.co`、`[x](mailto:a@b.co)` 的測試檔跑一次 lychee，實證 v0.24 opt-in mail 檢查不會誤傷（一次性驗證即可，記錄結果在本檔）
- [ ] **CODEOWNERS** — `docs/` 各篇指定 owner，PR 自動指派 review
- [ ] **fork PR 的渲染資安 policy 記錄** — Mermaid render job 會執行 fork PR 的圖（puppeteer 已保留 Chrome sandbox；若要更嚴，改為 render job 只跑 push、PR 僅靜態檢查）
- [ ] **依賴釘版** — `npm i -g @mermaid-js/mermaid-cli` 改釘版本，避免上游變更打掛 CI

## 4. 社群與推廣 / Community

- [ ] 開啟 GitHub Discussions（[CONTRIBUTING](CONTRIBUTING.md) 與 issue 範本已指向它）
- [ ] 申請 [awesome 清單 badge](https://github.com/sindresorhus/awesome/blob/main/pull_request_template.md)（若要列入 awesome 索引）
- [ ] 首月社群反饋收集：哪個角色章節最常被引用、哪些條目被回報失效

---

維護方式：勾選完成的項目；「找到來源就收、找不到維持不收」是硬規則（見
[CONTRIBUTING.md](CONTRIBUTING.md) 的 Ground rules）。/ 完成請勾選；收錄標準不變。
