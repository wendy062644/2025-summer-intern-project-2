---
title: Software Overview
---

# Software Overview

This project is a **frontend-first translation system** designed for **Qt Linguist `.ts` workflows**. It integrates Large Language Models (LLMs) while **keeping the format safe, the process controllable, and the output reliably compatible with the original project**.

It supports two translation approaches:

1. **Online GPT API**  
   Translate directly in the browser via an OpenAI-compatible API.

2. **Local LLM**  
   Generate an executable Jupyter Notebook and run translation offline on the user’s machine (CPU / GPU).

Both approaches provide **glossary guidance**, **format + placeholder protection**, **batch processing with progress tracking**, and a **live source/translation comparison** to help convert strings in projects like QGIS into **Traditional Chinese**.

---

## Which option should I choose?

| Option | How it works | Best for | Highlights & limits |
|---|---|---|---|
| **Online GPT API** | Calls your configured API in the browser | Quick setup, translate directly on the web | Built-in progress + comparison table, one-click `.ts` export |
| **Local LLM** | Generates a configurable `.ipynb` and runs locally | Offline use, your own GPU, testing open models | Highly customizable, but you must set up the environment |

---

## Quick Start

### A. Online GPT API (recommended to try first)
1. Open the **ChatGPT API Translation page** ([`app_api`](app_api)).
2. Set **API Key**, **Base URL**, and **Model**.
3. Upload the `.ts` file to translate.
4. (Optional) Upload a **Glossary** (`CSV / ODS`, columns: `en, zh` or `English Term, Chinese Term`).
5. Set **Batch** and the **maximum number of entries** for a small test run.
6. Run translation and review the live source/translation table and progress.
7. After verifying format safety, download **`qgis_zh-Hant.ts`**.

### B. Local LLM (offline)
1. Open the **Local LLM page** ([`app_local`](app_local)).
2. Configure model settings, batch size, token limits, glossary path, etc.
3. Download the generated `.ipynb`.
4. Install dependencies and run the notebook in your local Jupyter environment.

---

## Core Features

### Translation & terminology consistency

- Batch-based translation to keep input/output aligned.
- **Glossary + LCS matching** to detect key terms in the source text and nudge the model to use fixed translations  
  (e.g., `raster → 網格`) to reduce terminology drift.

### Format & structure protection

- Automatically protects and restores:
  - HTML tags and entities
  - Placeholders (`%n`, `%1`, `{0}`, etc.)
  - Original `.ts` structure and `DOCTYPE`
- Correct handling for `numerus="yes"` and `<numerusform>` output.

### Batch processing & review

- Configure batch size and an entry limit.
- Live progress bar and source/translation comparison table for quick spot checks.

### Export & integration

- Exports `.ts` via browser download (no backend server required).
- Works with `.qm` compilation and later merge/version workflows.

---

## Pre-export validation (what the system guarantees)

Before exporting the `.ts` file, the system checks:

- XML is parseable
- `<numerusform>` entries are complete for `numerus="yes"`
- Placeholders are not missing or mismatched in count
- HTML tags are not broken or unclosed

If validation fails, that entry will **not** be written back, preventing broken `.ts` outputs.

```{note}
This project runs in the browser via **Pyodide** and does not require a server or a local Python runtime.