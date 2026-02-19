---
title: Overview
---

# Overview

This project is a **front-end oriented translation system** for the **Qt Linguist `.ts` workflow**. It uses LLMs while keeping the process **format-safe, controllable, and able to write back reliably**.  

It supports two modes:  
1. **Online GPT API**  
   Translate in the browser via an OpenAI-compatible API.

2. **本機 LLM(Local LLM)**  
   Generate a runnable Jupyter Notebook and translate locally (CPU / GPU).

In both modes, it provides **詞彙表提示**、**格式與佔位符保護**、**批次處理與進度追蹤**、以及 **即時原文 / 譯文對照** 等能力，**to help**projects like QGIS translate strings into **Traditional Chinese** reliably.

---

## Which mode should I use?

| Option | How it works | Best for | Notes |
|---|---|---|---|
| **Online GPT API** | Call your configured API in the browser | Quick start; do everything on the web | Built-in progress + compare table; one-click `.ts` export |
| **本機 LLM** | Generate an `.ipynb` with a config block and run locally | Offline use, your GPU, or testing open models | Highly customizable, but you manage the environment |

---

## Quick Start

### A. Online GPT API (recommended first)
1. Open the **ChatGPT API translation page**（[`app_api`](app_api)）。
2. Set **API Key**, **Base URL**, and **Model**.
3. Upload the `.ts` file to translate.
4. (可選)上傳 **Glossary**（`CSV / ODS`，欄位為 `en, zh` 或 `英文名稱, 中文名稱`）。
5. Set **Batch** and **max items**; start with a small test.
6. Run translation and review progress + side-by-side compare.
7. If it looks good, download **`qgis_zh-Hant.ts`**.

### B. Local LLM (offline)
1. 進入 **本機 LLM 翻譯頁面**（[`app_local`](app_local)）。
2. Configure model, batch size, token limits, glossary path, etc.
3. 下載系統產生的 `.ipynb`。
4. Install dependencies and run the notebook locally.

---

## Core features

### Translation & terminology consistency

- Batch translation keeps inputs/outputs aligned.
- Uses **Glossary + LCS matching** to nudge preferred term translations  
  （例如：`raster → 網格`），and reduce drift.

### Format & structure safety

- Automatically protects and restores:
  - HTML 標籤與實體
  - placeholder（`%n`、`%1`、`{0}` 等）
  - `.ts` 原始結構與 `DOCTYPE`
- 支援 `numerus="yes"` 與 `<numerusform>` 的正確寫回。

### 批次處理與可檢視性

- 可設定 Batch 與翻譯筆數上限。
- 提供即時進度條與原文 / 譯文對照表，方便人工抽檢。

### 匯出與整合

- 以瀏覽器下載方式產出 `.ts`，不需後端伺服器。
- 可直接用於後續編譯 `.qm` 或版本合併流程。

---

## 寫回前驗證（系統保證範圍）

在輸出 `.ts` 檔案前，系統會檢查：

- XML 是否可正常解析
- `numerus="yes"` 的 `<numerusform>` 是否完整
- placeholder 是否遺失或數量不符
- HTML 標籤是否未閉合或被破壞

若驗證失敗，該筆翻譯不會直接寫回，以避免產生不可用的 `.ts`。

```{note}
本專題以 **瀏覽器 + Pyodide** 執行，不依賴伺服器 及 Python 環境。
