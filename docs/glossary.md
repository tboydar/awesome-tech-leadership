# Glossary / 術語對照表

English terminology ↔ 繁體中文 — the vocabulary used across this repo.
（本 repo 各篇使用的英文術語與繁體中文對照。表格格式，非資源條目。）

## Methodologies / 方法論

| Term | 繁體中文 | One-liner / 一句話 |
|---|---|---|
| TDD (Test-Driven Development) | 測試驅動開發 | Red → green → refactor: write a failing test first. 先寫會失敗的測試，再讓它通過。 |
| BDD (Behavior-Driven Development) | 行為驅動開發 | Specify behavior in Given/When/Then examples everyone can read. 用 Given/When/Then 範例描述行為。 |
| ATDD (Acceptance TDD) | 驗收測試驅動開發 | Turn acceptance criteria into executable tests before coding. 先把驗收條件變成可執行測試。 |
| SDD (Spec-Driven Development) | 規格驅動開發 | Spec is the source of truth; code (and agents) implement it. 規格為單一事實來源，程式與 agent 依它實作。 |
| DDD (Domain-Driven Design) | 領域驅動設計 | Model software around the business domain and its language. 圍繞業務領域與其語言建模。 |
| Clean Architecture | 整潔架構 | Dependencies point inward; business rules know no frameworks. 依賴向內，業務規則不依賴框架。 |
| Hexagonal Architecture | 六角形架構 | Ports & adapters isolate the core from the outside world. 用 ports/adapters 隔離核心與外界。 |
| Event Storming | 事件風暴 | Collaboratively map a domain as a timeline of events. 用事件時間軸協作梳理領域。 |
| Event-Driven Architecture | 事件驅動架構 | Components communicate by publishing/subscribing to events. 元件以事件發布/訂閱溝通。 |
| Refactoring | 重構 | Change structure without changing behavior. 不改變行為下改善結構。 |
| SOLID | SOLID 原則 | Five principles for maintainable object-oriented design. 五個可維護物件導向設計原則。 |
| Design Patterns (GoF) | 設計模式 | Reusable solutions to recurring design problems. 反覆出現的設計問題之可重用解法。 |
| ADR (Architecture Decision Record) | 架構決策紀錄 | A short dated note recording one architecture decision and why. 記錄單一架構決策與理由的短文件。 |
| Trunk-Based Development | 主幹開發 | Small frequent merges to main behind feature flags. 小步頻繁合併主幹，搭配 feature flag。 |
| GitFlow | GitFlow 分支模型 | Long-lived branches with release/hotfix conventions. 以 release/hotfix 慣例管理長期分支。 |
| Agile / Scrum / Kanban | 敏捷／看板 | Iterative delivery frameworks. 迭代式交付流程框架。 |
| XP (Extreme Programming) | 極限規劃／極限編程 | Engineering-first agile: pair programming, TDD, CI. 工程實踐優先的敏捷。 |
| DevOps / Four Keys | DevOps／四大金鑰 | Measure delivery with four key metrics. 以四項關鍵指標度量交付效能。 |
| DORA metrics | DORA 指標 | Deploy frequency, lead time, change failure rate, MTTR. 部署頻率、前置時間、變更失敗率、平均修復時間。 |
| SPACE framework | SPACE 框架 | Satisfaction, Performance, Activity, Communication, Efficiency. 開發者效能的五構面。 |
| Team Topologies | 團隊拓撲 | Stream-aligned, platform, enabling, subsystem teams. 四種團隊型態與三種互動模式。 |
| Strangler Fig Pattern | 絞殺者模式 | Migrate legacy by routing traffic to a new system piece by piece. 逐步以新系統取代 legacy。 |
| Test Pyramid | 測試金字塔 | Many unit tests, fewer integration, few E2E. 底層單元測試多、E2E 少。 |
| Mutation Testing | 突變測試 | Score test quality by how well tests catch seeded bugs. 以測試抓出人工植入缺陷的能力評估品質。 |
| Property-Based Testing | 性質測試 | Assert invariants over generated random inputs. 對隨機產生輸入斷言不變性質。 |
| Contract Testing | 契約測試 | Verify API consumer/provider expectations without full integration. 以契約驗證前後端期望，不需全整合。 |
| Refactoring Legacy / Legacy Modernization | 遺留系統現代化 | Incrementally replace or wrap old systems. 漸進式替換或包裝舊系統。 |

## AI & Agents / AI 與代理

| Term | 繁體中文 | One-liner / 一句話 |
|---|---|---|
| Prompt | 提示詞 | The instruction text sent to a model. 送給模型的指令文字。 |
| Prompt Engineering | 提示工程 | Designing instructions that elicit reliable model behavior. 設計能引導穩定輸出的指令。 |
| Context Engineering | 上下文工程 | Curating what (and how much) enters the model's context. 精選進入模型上下文的內容與份量。 |
| Chain-of-Thought (CoT) | 思維鏈 | Ask the model to reason step by step. 讓模型逐步推理。 |
| ReAct | ReAct 推理-行動 | Interleave reasoning with tool actions. 推理與工具行動交錯進行。 |
| Tree-of-Thought (ToT) | 思維樹 | Explore multiple reasoning branches and pick the best. 探索多條推理分支再擇優。 |
| Few-shot Prompting | 少樣本提示 | Teach by example inside the prompt. 在提示中以範例教學。 |
| LLM-as-Judge | LLM 當評審 | Use a model to grade model outputs. 用模型評分模型輸出。 |
| Agent | 代理／智慧體 | A model looped with tools and a goal until done. 模型搭配工具與目標循環執行到完成。 |
| Agent Loop | 代理迴圈 | The plan → act → observe cycle of an agent. 規劃→行動→觀察的循環。 |
| Subagent / Multi-agent | 子代理／多代理 | Delegate subtasks to specialized agents. 將子任務委派給專門代理。 |
| Orchestrator-Worker | 編排者-工作者 | One coordinator dispatches tasks to worker agents. 一個協調者派工給工作者代理。 |
| Skill (Agent Skill) | 技能包 | Packaged instructions (SKILL.md) an agent can load on demand. 代理可按需載入的打包指令（SKILL.md）。 |
| Hook | 鉤子 | User-defined shell commands triggered by agent events. 由代理事件觸發的自訂指令。 |
| Slash Command | 斜線指令 | A reusable prompt/command invoked as /name. 以 /名稱 呼叫的可重用指令。 |
| MCP (Model Context Protocol) | 模型上下文協定 | Open standard for wiring tools/data into AI apps. 將工具與資料接入 AI 應用的開放標準。 |
| MCP Server / Client | MCP 伺服器／用戶端 | The tool provider / the host app. 工具提供方／宿主應用。 |
| Tool Use / Function Calling | 工具呼叫 | Let the model call structured functions. 讓模型呼叫結構化函式。 |
| Structured Output | 結構化輸出 | Force valid JSON/schema output. 強制輸出符合 schema 的 JSON。 |
| Constrained Decoding | 約束解碼 | Grammar-level guarantee of output format. 文法層級保證輸出格式。 |
| RAG (Retrieval-Augmented Generation) | 檢索增強生成 | Retrieve documents and ground answers in them. 檢索文件並據以回答。 |
| Embedding | 向量嵌入 | Numeric vectors for semantic search. 用於語意搜尋的數值向量。 |
| Compaction / Context Window | 壓縮／上下文視窗 | Summarize history to keep long runs within limits. 以摘要延續長任務不超出上下文。 |
| Human-in-the-Loop (HITL) | 人在迴圈 | Insert human approval gates into agent runs. 在代理流程插入人工核准關卡。 |
| Stop Hook | 停止鉤子 | A check that blocks an agent from ending prematurely. 阻止代理過早結束的檢查。 |
| Vibe Coding | 氛圍式開發 | Code by intent, guided conversationally by AI. 以意圖對話式引導 AI 產碼。 |
| Hallucination | 幻覺 | Confident but fabricated model output. 模型自信但虛構的輸出。 |
| Prompt Injection | 提示注入 | Malicious input that hijacks agent instructions. 劫持代理指令的惡意輸入。 |
| Jailbreak | 越獄 | Bypassing a model's safety policies. 繞過模型安全政策。 |
| Token | 詞元 | The unit of text billing & context. 文字計費與上下文的單位。 |
| Inference | 推理 | Running the model on an input. 模型對輸入的執行。 |
| Fine-tuning | 微調 | Continue-training a model on your data. 以自有資料續訓模型。 |
| Distillation | 蒸餺 | Train a small model to mimic a big one. 讓小模型模仿大模型。 |
| Reasoning Model | 推理模型 | A model trained to think longer before answering. 訓練為先思考再回答的模型。 |
| AI Eval / Benchmark | AI 評估／基準 | Measured quality of models or agents. 對模型或代理的量化品質衡量。 |
| Golden Dataset | 黃金資料集 | Curated expected inputs/outputs for regression. 用於迴歸測試的精選輸入輸出集。 |
| Observability (Observability/OTel) | 可觀測性 | Traces, metrics, logs for AI runs. AI 執行的追蹤、指標、日誌。 |
| LLMOps | LLMOps | Ops practices for LLM systems in production. LLM 系統上線維運實踐。 |
| AI Governance | AI 治理 | Policies and controls for compliant AI use. 合規 AI 使用的政策與控制。 |
| EU AI Act | 歐盟 AI 法案 | Risk-tiered regulation for AI systems in the EU. 歐盟風險分級 AI 法規。 |
| NIST AI RMF | NIST AI 風險管理框架 | Govern / Map / Measure / Manage AI risk. 治理／繪製／衡量／管理 AI 風險。 |
| OWASP LLM Top 10 | OWASP LLM 十大風險 | Top application-security risks for LLM apps. LLM 應用的十大資安風險。 |
| SPDX License | SPDX 授權標識 | Standard license identifiers for open source. 開源授權標準標識碼。 |
