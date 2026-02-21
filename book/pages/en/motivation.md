---
title: Background
---

# Background

Open-source software localization in Taiwan has long faced structural challenges, including **limited contributors, inconsistent terminology, and uneven quality**.

Using QGIS as an example, the Traditional Chinese interface often shows **mixed Simplified/Traditional Chinese, missing translations, and inconsistent terminology**. In addition, **accelerator markers (e.g., `(&C)`)** and **placeholders (e.g., `%n`, `{0}`)** are easily altered or removed during translation. This may break UI behavior and reduce users’ trust in interface correctness and stability.

In recent years, Large Language Models (LLMs) have been introduced into localization workflows, improving speed and coverage. However, most general-purpose models lack sufficient understanding of **GIS-specific terminology** and **strict format constraints**, making it difficult to balance semantic accuracy with structural integrity. As a result, significant manual review and rework are still required, limiting the overall efficiency gains from automation.

## Motivation

In this context, our core question is:

> Localization should not rely on scattered volunteer efforts, but become a **sustainable, transferable, and reproducible** workflow.

By combining **automation tools, community collaboration, and domain knowledge**, we aim to build a Traditional Chinese localization workflow for QGIS and similar projects that balances **quality, efficiency, and maintainability**, while lowering the barrier for contributors to participate systematically in translation and review.

---

## Pain Points We Observed

- **Inconsistent terminology**  
  The same term may be translated differently across modules (e.g., *raster* as “光柵 / 網格 / 點陣圖”), causing confusion in teaching and practice.

- **Broken functionality after translation**  
  Modifying or removing accelerator markers, placeholders, or special symbols may cause UI errors and disrupt user workflows.

- **High learning and teaching costs**  
  Instructors and beginners must clarify which translation is correct or commonly used, increasing learning friction and preparation effort.

- **Fragmented maintenance process**  
  Review and revision often depend on individual experience and ad hoc coordination, making handover and long-term maintenance difficult.

- **Domain gaps in general LLMs**  
  Without GIS context and format protection mechanisms, models may produce linguistically fluent but system-level incorrect translations (e.g., altering placeholders or introducing inconsistent terms), increasing manual correction workload.

---

## What We Aim to Fix

This project focuses on the following goals:

- **Clarity and reliability for users**  
  Maintain consistent terminology across contexts and ensure functional elements (accelerators, placeholders) remain intact.

- **A sustainable and transferable workflow**  
  Design tools and processes that make review and collaboration repeatable and traceable, reducing reliance on a few core contributors.

- **A reusable methodology**  
  Consolidate rules, tools, and experience into a **replicable localization workflow** that can be extended to other open-source projects and domains.

- **Make LLM a reliable assistant**  
  Integrate domain glossaries, structural validation, and multi-stage evaluation so that LLMs follow predefined constraints and genuinely reduce manual workload.

Through these efforts, we aim to build a **high-quality, maintainable, and community-friendly** localization ecosystem that enables stable and predictable translation quality under limited resources.