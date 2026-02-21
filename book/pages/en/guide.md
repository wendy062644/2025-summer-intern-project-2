---
title: User Guide
---

# User Guide

## How to Open & Runtime Environment

1. We recommend using the latest **Chrome / Edge**.
2. From the sidebar, choose **[Online GPT](app_api)** or **[Local LLM](app_local)**.
3. Pick either **online API translation** or **local model translation** based on your needs.

> **Operational Differences**
> - **Online GPT (API)**: All settings, translation, execution, and result review are done in the browser. Best for quick translation and manual spot checks.
> - **Local LLM**: This page only generates a reproducible `.ipynb`; the actual translation runs on the user’s local machine (CPU / GPU).

---

## File Preparation & Basic Assumptions

- **`.ts` (Required)**  
  - Must be a valid, parseable Qt Linguist XML translation file.
  - The system uses `<context>` and `<source>` as the smallest processing unit.

- **Glossary (Optional)**  
  - Supports uploading multiple **CSV / ODS** files at the same time.
  - Column format must be `en, zh` or `English Term, Chinese Term`.
  - The system merges glossaries automatically; **for the same English term, the first occurrence wins**.

> The glossary is normalized and matched before being used in translation prompts.

---

## A. Online GPT (API) Workflow

### 1. Load Files

- Upload the **`.ts` file**.
- (Optional) Upload a **Glossary (CSV / ODS)**.
- The system parses `<source>` nodes in the `.ts` file and calculates the **number of translatable entries**:
  - Only `<source>` strings that can actually be sent for translation are counted.
  - Empty strings or entries without translatable content are excluded.
- The **Processing Limit** defaults to the total number of translatable entries and is shown as `current / total` in the UI.

### 2. Configure Parameters

- **API Settings**
  - `API Key`: key required to call the online model
  - `Base URL`: API service endpoint
  - `Model`: model name (dropdown)

- **Processing Parameters**
  - `Batch`: number of entries per request
  - `Processing Limit`: max number of entries processed in this run

> All settings are located in the top section: “API Settings / Processing Parameters / Input Files”.

### 3. Run Translation

- After clicking **Run Translation**:
  - The page shows a live **progress bar** and a **source/translation comparison table**
  - No refresh is needed during execution
- When finished, the message area provides a **download link** for the output file **`qgis_zh-Hant.ts`**.

### Format Protection

In Online GPT mode, you can assume:

- Placeholders (e.g., `%n`, `%1`, `%L1`, `{0}`) will not be lost or reordered
- HTML tags are preserved and restored correctly
- The `.ts` DOCTYPE and structure remain unchanged
- `numerus="yes"` with `<numerusform>` is written back correctly

The system runs structural checks before writing output. If a check fails, that entry is not written to the exported `.ts`.

---

## B. Local LLM Workflow

### 1. Configure Notebook Parameters

- **Files & Directories**
  - `Input filename (.ts)`
  - `Output filename (without extension)`
  - `ODS_DIR`: directory of glossary files

- **Model & API**
  - `Model`
  - `FALLBACK_MODEL` (optional)
  - `API Key or Token` (optional)
  - `API Base URL`

- **Other Parameters**
  - `Batch`
  - `Max Tokens`
  - `Min Tokens`

### 2. Generate Notebook & Review Settings

- Click **Download new .ipynb** to get the full notebook.
- The system inserts a **Config cell** at the very top.
- If you want to check settings first, use **Preview Config cell**.

### 3. Run Locally

- Open the `.ipynb` in **Jupyter / JupyterLab / VS Code**.
- Install dependencies and prepare model weights or API credentials as needed.
- You may modify the code (e.g., batch size, model switching, output filename) and then run cell by cell.

> Note: In Local LLM mode, the user is responsible for execution and environment correctness.  
> This page only helps generate a reproducible notebook configuration.

---

## C. Edit Translations (Edit)

**[Edit Translations](edit)** provides **manual selection and merging across multiple `.ts` results**,  
useful when you have multiple runs (different models or batches) and want to **choose the final version message by message**.

### Use Cases

- The same `.ts` was translated with different models / parameters
- You want to pick the “better” version per entry
- During review, you want to choose among multiple outputs instead of re-translating

### Workflow

1. Upload **one or more `.ts` files** (the first file is used as the base draft).
2. The system generates a table:
   - Each row represents one message (`context / source`)
   - Each column represents one `.ts` file’s translation output
3. Click a cell to select that version for the message.
4. Download the merged `.ts` file.

> This feature does not support per-character inline editing.  
> If you need to tweak text, create a new version first, then select/merge.

---

## D. Merge Files (Merge)

**[Merge Files](merge)** is for **continuing existing translation progress**.  
It applies **already-translated content** from one `.ts` file to a **newer, not-yet-complete `.ts`**  
so you don’t re-translate strings that were already done.

This is useful for version updates, collaborative “relay” translation, or resuming after interruptions.

### Use Cases

- **Continue progress**:  
  A newer `.ts` is incomplete; reuse translations from an older version.

- **Multi-person / multi-stage collaboration**:  
  Apply completed parts from other batches or contributors.

- **Cost control**:  
  Reuse existing results before running translation again.

### Merge Rules (Core Logic)

- The only matching condition is **exact `<source>` text equality**.
- Overwrite happens only when the source file’s matching `<source>` has a **non-empty `<translation>`**.
- The merge behavior:
  - Use the source file’s `<translation>` to fill the corresponding entry in the target file.
- Unmatched entries or empty source translations **remain unchanged**.

> This feature uses a **strict, exact-fill strategy** (no fuzzy matching or similarity guessing)  
> to avoid incorrect overwrites that could break UI string mappings.

### Workflow

1. Upload the **Target file (Target `.ts`)**  
   - Usually a newer version that is not fully translated.

2. Upload the **Source file (Source `.ts`)**  
   - Usually an older version or a file with partially completed translations.

3. Run merge and download the output file  
   - Reusable translations are filled into the target; everything else remains unchanged.

---

## Apply to QGIS

1. Install Qt tools (Debian/Ubuntu example)
   - `sudo apt-get install qttools5-dev-tools`
2. Convert `.ts` to binary `.qm`
   - `lrelease qgis_zh-Hant.ts`
3. Put `qgis_zh-Hant.qm` into the `QGIS 3.XX.X\apps\qgis-ltr\i18n` folder

---

## Parameter Reference (Key Items)

| Section | Parameter | Description |
|---|---|---|
| API | **API Key** | Key required for online models; can be empty for local mode. |
| API | **Base URL** | API endpoint. |
| API | **Model** | Model name to use. |
| Processing | **Batch** | Entries per request. |
| Processing | **Processing Limit** | Max entries to process in this run. |
| Files | **Glossary (CSV/ODS)** | Multiple files supported; auto-merged; columns `en, zh` or `English Term, Chinese Term`. |
| Local | **FALLBACK_MODEL** | Backup model if the primary model fails (optional). |
| Local | **Max/Min Tokens** | Token limits per response. |
| Local | **ODS_DIR** | Folder path for glossary files. |

---

## Security & Privacy Tips

- **API Keys are used only in the browser** and are sent only to your configured `Base URL`.  
  Do not share your key or publish pages containing it.
- If you have security/privacy requirements, use **Local LLM (offline)**.