---
title: Welcome
description: Project Overview & Quick Start
---

# Quick Guide

> This project was conducted by **Yu-Lin Chen** at **Institute of Information Science, Academia Sinica (2025)**.  
> Use the sidebar to switch chapters, or click the links below for key sections.  
> The goal is to build a **scalable, handoff-friendly, controllable, and verifiable** Qt `.ts` translation workflow.

- Start with **[Software Overview](intro.md)** and **[User Guide](guide.md)** to understand features and FAQs  
- Choose a translation mode: **[Online GPT](app_api)** or **[Local LLM](app_local)**

---

## Quick Start

1. Go to **[Online GPT](app_api)** (or use [Local LLM](app_local)).
2. Configure the translation model:
   - Online: enter your `API Key`, confirm `Base URL` and `Model`
   - Local: configure the model and generate a Notebook for local execution
3. Upload the `.ts` file to be translated.
4. (Optional) Upload a **Glossary** (`CSV / ODS`, columns: `en, zh` or `English Term, Chinese Term`).
5. (Optional) Upload a **previous `.ts` file**: when `<source>` is identical, existing translations will be reused to reduce cost.
6. Set `Batch` mode and the **maximum number of entries**, and run a small test first.
7. After confirming format and results, increase the batch size and download the output `qgis_zh-Hant.ts`.

```{tip}
You may upload multiple glossary files; they will be merged automatically.  
It is recommended to test with a small sample (e.g., 100–300 entries) before running the full translation.