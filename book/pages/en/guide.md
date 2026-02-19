---
title: User Guide
---

# User Guide

## How to open & runtime

1. Use the latest **Chrome / Edge** if possible.
2. In the left sidebar, choose **[Online GPT](app_api)** or **[Local LLM](app_local)**.
3. Pick **online API translation** or **local model translation**.

> **Mode differences**
> - **Online GPT(API)**：Everything runs in the browser; good for quick runs and spot checks.
> - **Local LLM(本機)**：This page only generates a reproducible `.ipynb`; translation runs on your machine (CPU / GPU).

---

## Files & assumptions

- **`.ts` (required)**  
  - Must be a valid Qt Linguist XML translation file.
  - The unit of work is `<context>` + `<source>`.

- **Glossary (optional)**  
  - Supports uploading multiple **CSV / ODS** files.
  - Columns must be `en, zh` or `English, Chinese`.
  - Glossaries are merged; **the first occurrence wins** for duplicates.

> The glossary is lightly normalized and matched before prompting.

---

## A. Online GPT (API) flow

### 1. Load files

- Upload the **`.ts` file**.
- (Optional) Upload **Glossary (CSV / ODS)**.
- The system parses `<source>` nodes and counts **translatable entries**.
  - Only `<source>` entries that can actually be sent for translation are counted.
  - Empty strings or non-translatable content are excluded.
- The **max items** defaults to the total and is shown as `current / total`.

### 2. Configure

- **API settings**
  - `API Key`: key/token for calling the online model
  - `Base URL`: API endpoint
  - `Model`: model name (dropdown)

- **Run settings**
  - `Batch`: number of entries per request
  - `Max items`: maximum entries to process in this run

> All fields are in the top section (API settings / run settings / input files).

### 3. Run translation

- After you click **Run translation**:
  - The page shows a **progress bar** and a **source/translation table** in real time
  - No refresh is needed during the run
- When done, you'll get a **download link** for **`qgis_zh-Hant.ts`**.

### Format safety

In Online GPT mode, you can expect:

- Placeholders (e.g., `%n`、`%1`、`%L1`、`{0}` ) are not lost or reordered
- HTML tags are preserved and restored correctly
- The `.ts` DOCTYPE and structure remain unchanged
- `<numerusform>` (for `numerus="yes"`) is written back correctly

Before write-back, basic checks run; failed items are skipped.

---

## B. Local LLM flow

### 1. Notebook config

- **Files & folders**
  - `Input file (.ts)`
  - `Output name (no extension)`
  - `ODS_DIR`: directory for glossary files

- **Model & API**
  - `Model`
  - `FALLBACK_MODEL` (optional)
  - `API Key or Token` (optional)
  - `API Base URL`

- **Other settings**
  - `Batch`
  - `Max Tokens`
  - `Min Tokens`

### 2. Generate notebook & preview

- Click **Download new .ipynb** to get the full notebook.
- 系統會自動在 Notebook 最前方插入一段 **Config cell**。
- To review settings first, use **Preview Config cell**.

### 3. Run locally

- Open the `.ipynb` in **Jupyter / JupyterLab / VS Code**.
- Install dependencies and prepare weights / API access as needed.
- You can tweak batch size, model, output name, etc., then run cell by cell.

> 注意：Local LLM 模式下，翻譯執行與環境設定的正確性由使用者自行負責；  
> 本頁僅協助產生可重現的 Notebook 設定。

---

## C. 編輯翻譯檔(Edit)

**[編輯翻譯檔](edit)** 提供「**多版本 `.ts` 翻譯結果的人工選擇與合併**」，  
適合在多次翻譯、不同模型或不同批次結果之間，**由人工逐句決定最終採用版本**。

### 使用情境

- 同一份 `.ts` 曾以不同模型 / 不同參數翻譯
- 想逐句挑選「反而翻得比較好」的版本
- 人工審稿時，需要在多個翻譯結果間做選擇，而非重新翻譯

### 操作流程

1. 上傳 **一個以上的 `.ts` 檔案**(第 1 個檔案作為預設底稿)。
2. 系統會產生一個表格：
   - 每一列代表一個訊息(context / source)
   - 每一欄代表一個 `.ts` 檔案的翻譯結果
3. 點選任一儲存格，即表示該訊息採用該版本的譯文。
4. 完成選擇後，下載合併後的 `.ts` 檔案。

> 此功能不提供逐字 inline 編輯；  
> 若需文字內容微調，建議先產生新版本再進行選擇合併。

---

## D. 檔案合併(Merge)

**[檔案合併](merge)** 用於「**延續既有翻譯進度**」  
將**已完成翻譯的 `.ts` 檔內容**，套用至一份**尚未完全翻譯的新版本 `.ts`**  
以避免重複翻譯已完成的字串。

可用於版本更新、多人接力翻譯，或翻譯流程中斷後的續作。

### 使用情境

- **翻譯進度延續**：  
  新版本 `.ts` 尚未翻譯完成，欲沿用舊版本中已完成的翻譯內容。

- **多人／多階段翻譯接力**：  
  將前人或其他批次已翻譯完成的內容，補齊至目前版本。

- **翻譯成本控管**：  
  在再次呼叫翻譯流程前，先套用既有成果以降低重複翻譯。

### 合併規則(核心邏輯)

- 系統以 **`<source>` 文字內容完全相同** 作為唯一匹配條件。
- 僅當 **來源檔中該 `<source>` 已包含非空的 `<translation>`** 時，才進行覆蓋。
- 合併行為為：
  - 使用來源檔的 `<translation>`，補齊目標檔中對應的翻譯內容。
- 未匹配或來源翻譯為空的項目，**維持目標檔原狀**。

> 本功能採用「**精準補齊**」策略，不進行模糊比對或相似度推斷  
> 以避免錯誤覆蓋導致 UI 字串對應錯亂

### 操作流程

1. 上傳 **目標檔（Target `.ts`）**  
   - 通常為**較新版本、尚未完全翻譯完成**的 `.ts`。

2. 上傳 **來源檔（Source `.ts`）**  
   - 通常為**舊版本或前人已完成部分翻譯**的 `.ts`。

3. 執行合併並下載輸出檔  
   - 系統會將可沿用的翻譯內容補齊至目標檔中，其餘部分保持不變。

---

## 套用至 QGIS 中
1. 安裝 Qt 工具(以下以 Debian/Ubuntu 為例)
   - sudo apt-get install qttools5-dev-tools
2. 將 `.ts` 檔案轉成二進位的 `.qm` 檔
   - lrelease qgis_zh-Hant.ts
3. 將 `qgis_zh-Hant.qm` 放進 `QGIS 3.XX.X\apps\qgis-ltr\i18n` 資料夾中

---

## 參數對照（重點）

| 區塊 | 參數 | 說明 |
|---|---|---|
| API | **API Key** | 呼叫線上模型所需的金鑰；若走本機模型可留空。 |
| API | **Base URL** | API 連結。 |
| API | **Model** | 要使用的模型名稱。 |
| 處理 | **Batch** | 每批送出的句數； |
| 處理 | **處理筆數上限** | 控制本次處理的句數。 |
| 檔案 | **Glossary(CSV/ODS)** | 可上傳多個檔案；自動合併，欄位相容 `en, zh` 或 `英文名稱, 中文名稱`。 |
| 本機 | **FALLBACK_MODEL** | 主要模型失敗時的備用模型（可留空）。 |
| 本機 | **Max/Min Tokens** | 控制單次回應的 token 上下限。 |
| 本機 | **ODS_DIR** | 中英對照表之資料夾路徑。|

---

## 安全性與隱私建議

- **API Key 僅在瀏覽器端使用**，並只會送到你設定的 `Base URL`；請勿把金鑰與頁面公開分享。  
- 若有安全與隱私需求，可以使用 **Local LLM(本機離線)**。