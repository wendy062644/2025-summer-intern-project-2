---
title: 操作頁面
---

# 操作頁面（使用指南）

## 開啟方式
1. 建議使用最新 **Chrome / Edge**。
2. 在側邊目錄點選 **[Online GPT](app_api)** 或 **[Local LLM](app_local)**。
3. 依需求選擇 **線上 API** 或 **本地模型** 執行翻譯。

> **兩種模式差異**  
> - **Online GPT（API）**：直接在瀏覽器端以 **Pyodide** 呼叫你設定的 API，提供進度條與即時原文/譯文對照，完成後一鍵下載 `qgis_zh-Hant.ts`。  
> - **Local LLM（本機）**：頁面會幫你**生成含參數設定的 `.ipynb`**，在本機開啟該 Notebook 後執行。

---

## 檔案準備

- **`.ts`（必填）**：需為 XML 的 Qt 翻譯檔。  
- **Glossary 詞彙表（可選）**：可上傳 **CSV / ODS** 多檔，欄位建議：  
  - `en, zh` 或 `英文名稱, 中文名稱`  
  - 介面會自動**合併**，同一英文字詞以**最先出現**者為準（可藉由上傳順序控制優先權）。

> 小提醒：Glossary 會先做簡單標準化與對比。

---

## A. Online GPT（API）流程（建議先試用）

1. **載入檔案**  
   - 上傳 **`.ts` 檔**。  
   - （可選）上傳 **Glossary（CSV/ODS）**。  
   - 系統會解析 `.ts` 內 `<source>`，自動計算**可翻譯句數**，並把「**處理筆數上限**」預設為總數，右側顯示 `目前/總數`。

2. **設定參數**  
   - **API 設定**：`API Key`、`Base URL`、`Model`（下拉可選）。  
   - **處理參數**：`Batch`（每批句數）、`處理筆數上限`（本次要處理的最大句數）。  
   - 以上欄位都在頁面頂部的 **「API 設定 / 處理參數 / 輸入檔案」** 區塊內。

3. **執行翻譯**  
   - 點 **「執行翻譯」**，可即時看到 **進度條** 與 **原文/譯文對照表**，過程中不需重新整理頁面。  
   - 完成後，訊息列會出現 **下載連結**，直接取得 **`qgis_zh-Hant.ts`**。

### Online GPT 的格式保護
- 內建**格式保護**機制，會保留並還原：**HTML、%n、%1、%L1、{0}**…等特殊字詞。  
- 會保留 `.ts` 的 **DOCTYPE** 與原始結構；對於複數型 `<numerusform>` 也能正確寫回。

---

## B. Local LLM（本機）流程

1. **設定 Notebook 參數**
   - 檔名與目錄：`輸入檔名（.ts）`、`輸出檔名（不含副檔名）`、`ODS_DIR（中英對照表之目錄）`。  
   - 模型與 API：`Model`、`FALLBACK_MODEL（可留空）`、`API Key or Token（可留空）`、`API Base URL`。  
   - 參數：`Batch`、`Max Tokens`、`Min Tokens`。

2. **產生 Notebook / 預覽設定**
   - 點 **「下載新的 .ipynb」** 下載完成版 Notebook（系統會把一段 **Config cell** 加到最前面）。  
   - 想先檢查設定，可點 **「預覽 Config cell」**。

3. **在本機執行**
   - 於 Jupyter / JupyterLab / VS Code 開啟該 `.ipynb`。  
   - 視情況安裝相依套件、準備模型或 API。  
   - 可自行調整程式碼參數（如：批次大小、輸出檔名、模型切換等），再逐格執行。

---

## 套用至 QGIS 中
1. 安裝所需 library
   - sudo apt-get install qttools5-dev-tools
2. 將 `.ts` 檔案轉成二進位的 `.qm` 檔
   - lrelease qgis_zh-Hant.ts
3. 將 `qgis_zh-Hant.qm` 放進 `QGIS 3.XX.X\apps\qgis-ltr\i18n` 資料夾中


## 參數對照（重點）

| 區塊 | 參數 | 說明 |
|---|---|---|
| API | **API Key** | 呼叫線上模型所需的金鑰；若走本機模型可留空。 |
| API | **Base URL** | API 連結。 |
| API | **Model** | 要使用的模型名稱。 |
| 處理 | **Batch** | 每批送出的句數； |
| 處理 | **處理筆數上限** | 控制本次處理的句數。 |
| 檔案 | **Glossary（CSV/ODS）** | 可上傳多個檔案；自動合併，欄位相容 `en, zh` 或 `英文名稱, 中文名稱`。 |
| 本機 | **FALLBACK_MODEL** | 主要模型失敗時的備用模型（可留空）。 |
| 本機 | **Max/Min Tokens** | 控制單次回應的 token 上下限。 |
| 本機 | **ODS_DIR** | 中英對照表之資料夾路徑。|

---

## 常見問題（FAQ）

**Q1. 執行 Online GPT 時，頁面顯示「請輸入 API Key / 請上傳 .ts 檔」**  
A：這是前端檢查提示，請確認 API Key 與 `.ts` 檔已填入/上傳再按「執行翻譯」。

**Q2. Glossary 上傳多檔會不會衝突？**  
A：系統會自動**合併 & 去除重複內容**，相同英文詞以**先出現**的為主；建議把優先詞庫排在最前面上傳。

**Q3. `.ts` 裡的 HTML 與 `%1 / %n / {0}` 等佔位符會被改動嗎？**  
A：不會。系統會先標記，翻譯完再還原；同時保留 DOCTYPE 與 `<numerusform>`。

**Q4. Local LLM 一鍵下載的 Notebook 長怎樣？可以先看設定嗎？**  
A：頁面會把 **Config cell** 插在 Notebook 最前面；你可用「**預覽 Config cell**」先檢視，再下載執行。

---

## 安全性與隱私建議

- **API Key 僅在瀏覽器端使用**，並只會送到你設定的 `Base URL`；請勿把金鑰與頁面公開分享。  
- 若有安全與隱私需求，可以使用 **Local LLM（本機離線）**。

---

## 懶人包：三步驟摘要（Online GPT）

1) 上傳 `.ts`（與可選的 Glossary），介面會自動統計**可翻譯句數**。  
2) 設定 `API Key / Base URL / Model` 與 `Batch / 處理筆數上限`。  
3) 按 **執行翻譯** → 看 **進度條與對照表** → 下載 `qgis_zh-Hant.ts`。

---

## 懶人包：三步驟摘要（Local LLM）

1) 在頁面設定 **檔名/模型/參數**。  
2) 點 **下載新的 .ipynb**（可先用 **預覽 Config cell** 檢查）。  
3) 於本機開啟 Notebook、安裝相依套件後執行，離線完成翻譯。
