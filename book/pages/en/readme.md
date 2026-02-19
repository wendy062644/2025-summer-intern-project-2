---
title: Welcome
description: Project tour and quick start
---

# Quick Tour

> This is **Yu-Lin Chen**'s **Academia Sinica 2025** project.  
> Use the left sidebar to navigate, or jump via the links below.  
> Goal: a Qt `.ts` translation workflow that is **batch-friendly, handoff-ready, controllable, and verifiable**.

- Start with **[Overview](intro.md)** and **[User Guide](guide.md)** for features and FAQs  
- Pick a mode: **[Online GPT](app_api)** or **[Local LLM](app_local)**

---

## Quick Start

1. Open **[Online GPT](app_api)** (or use [Local LLM](app_local)).
2. Choose translation settings
   - Online: set `API Key`, confirm `Base URL` and `Model`
   - Local: configure the model and generate a notebook to run locally
3. Upload the `.ts` file to translate.
4. (Optional) Upload a **Glossary** (`CSV / ODS`, columns: `en, zh` or `English, Chinese`).
5. (Optional) Upload an **older `.ts`**: if `<source>` matches exactly, reuse existing translations to save cost.
6. Set `Batch` and the **max items**; run a small test first.
7. After checking the output, scale up and download `qgis_zh-Hant.ts`.

```{tip}
You can upload multiple glossary files; they will be merged automatically.  
Tip: spot-check a small batch (e.g., 100–300 items) before a full run.