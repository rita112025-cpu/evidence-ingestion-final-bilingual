
# Evidence-First Document Ingestion
### MarkItDown + Crawl4AI + Browser Use + Scrapy

> 基於 Polanco IA 的 10 工具勘誤版，縮成工程可用的 4 核心。
> 核心原則：原檔才是 Evidence，Markdown 是衍生資料 (Extraction Layer)。

## 架構

D:\文件 / PDF / Excel / Office
          │
          ▼
     MarkItDown -> Markdown (衍生) + evidence.json
          │
          ├─→ LLM 分析
          └─→ SQLite / JSON
                         ▲
網站 ──► Crawl4AI ───────┘

需要登入 / 點擊 / JS  ──► Browser Use
未來大量批次 ──► Scrapy / Crawlee

## 選型修正 (已驗證)

| 工具 | 修正後資訊 |
|------|------------|
| MarkItDown | 保留結構供 LLM，非完美排版 / MIT / ~122k+ stars |
| Crawl4AI | ~83.4k stars / Apache-2.0 / 網頁→Markdown |
| Firecrawl | ~166k stars / AGPL-3.0 core, MIT SDK / 商業注意 AGPL |
| Browser Use | ~112k stars / MIT / Agent browser automation |
| Scrapling | BSD-3-Clause 非 MIT |
| scrcpy | ~149.9k stars / Apache-2.0 / Android control |
| curl-impersonate | TLS/HTTP fingerprint 非真人行為 |
| AutoScraper | 依範例學 extraction rules |

## Evidence Layer 設計

每個檔案都會產生對應的 evidence.json，包含：
- source_path / source_url : 原始來源
- sha256 / file_hash : baseline hash
- timestamp : 擷取時間 UTC
- revision : 版本號
- extraction_tool : 用哪個工具抽的
- derived_path : 產出的 Markdown 路徑
- mime_type, file_size

原 PDF/Excel 永遠保留，Markdown 只是衍生。

## 快速開始

pip install -r requirements.txt
python examples/main.py --input D:/文件 --output ./evidence

## 上傳到 GitHub

cd github_ingestion_template
git init
git add .
git commit -m "feat: evidence-first ingestion template"
gh repo create your-name/evidence-ingestion --public --source=. --push

## Docs (雙語 + 暗亮版)

- `docs/index.html` : 最新版 - EDH 卡片風格，支援 繁中/EN + 暗/亮 雙切換 (本次最終版)
- `docs/legacy-dark-light.html` : 第一版暗亮版文件
- `docs/edh-v1.html` : EDH 風格單語版

部署 GitHub Pages: Settings > Pages > Deploy from main / docs folder
