---
title: Background
---

# Background

Taiwan-localized OSS often suffers from **limited contributors, fragmented standards, and inconsistent quality**.  
In QGIS Traditional Chinese UI, you may see **mixed zh-Hant/zh-Hans, missing translations, and inconsistent terms**;**accelerator markers** (e.g., `(&C)`) and **placeholders** (e.g., `%n`, `{0}`) are also easy to break,which can cause UI issues and reduce user trust.

LLMs can improve speed and coverage in localization.But general models often struggle with **GIS terminology** and **strict formatting constraints**.In practice, this still leads to heavy review and rework.

## Motivation

So the key question is:

> Localization should not rely on a few volunteers; it should be a **sustainable, repeatable, handoff-friendly** workflow.

We combine **automation, community contribution, and domain knowledge** to build a Traditional Chinese workflow that balances **quality, speed, and maintainability**, lowering the burden for contributors.

---

## Pain Points

- **Low terminology consistency**  
  The same term is translated differently across modules(例如 *raster* 可能被翻為「光柵／網格／點陣圖」)，造成教學與實務操作上的理解落差。

- **UI behavior broken by translation**  
  快捷鍵標記、佔位符與特殊符號在翻譯時被更動或刪除，leading to UI issues and more errors.

- **High learning/teaching cost**  
  Beginners and instructors spend extra time explaining「哪一個才是較為正確或常用的譯法」，學習曲線被迫拉長，教材撰寫與課程準備也更為吃力。

- **Fragmented maintenance and hard handoff**  
  Review and fixes often rely on personal experience and ad-hoc coordination，缺乏標準化流程與工具支援，使得社群貢獻門檻偏高，長期維護不易。

- **Domain blind spots in general LLMs**  
  Without GIS context and format-safety design，模型在關鍵位置容易產生語意上看似合理、但在系統層面不正確的翻譯結果，如: 擅自改動 placeholder 或引入新的譯法，反而增加後續人工修正與審核負擔。

---

## What We Aim To Fix

本專題聚焦於以下幾項目標：

- **讓使用者看得懂、用得準**  
  在不同情境下維持術語與翻譯的一致性，同時確保快捷鍵與佔位符等功能性元素不被破壞，降低學習與溝通成本。

- **讓維護流程可持續、交接**  
  透過工具與流程設計，讓審核、修正與協作過程變得可重複、可追蹤，避免每一次翻譯都從零開始、仰賴少數人的「人海戰術」。

- **讓方法可以被複製與擴散**  
  將本計畫中累積的經驗、規則與工具整理為一套 **可重用的在地化翻譯方法與工作流程**，未來可延伸應用到其他開源專案與領域。

- **讓 LLM 成為「可靠助手」而非「額外負擔」**  
  透過結合領域詞彙庫、格式檢查與多階段評估機制，使 LLM 在翻譯過程中能遵守既定規範，實際減少人工修正工作量。

透過上述目標，我們希望逐步建立一個 **高品質、可維護且易於參與** 的在地化生態系，讓台灣在地開源社群能在有限人力下，維持穩定且可預期的翻譯品質。