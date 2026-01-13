---
title: 使用說明
---

# 使用指南

## 開啟方式與執行環境

1. 建議使用最新版本的 **Chrome / Edge** 瀏覽器。
2. 於左側目錄選擇 **[Online GPT](app_api)** 或 **[Local LLM](app_local)**。
3. 依需求選擇 **線上 API 翻譯** 或 **本機模型翻譯**。

> **操作層差異說明**
> - **Online GPT(API)**：所有設定、翻譯、執行與結果檢視皆在瀏覽器頁面內完成，適合即時翻譯與人工抽檢。
> - **Local LLM(本機)**：本頁僅負責產生可重現的 `.ipynb`；實際翻譯需在使用者本機(CPU / GPU)環境中執行。

---

## 檔案準備與基本假設

- **`.ts`(必填)**  
  - 必須為可解析的 Qt Linguist XML 翻譯檔。
  - 系統會以 `<context>` 與 `<source>` 為最小處理單位。

- **Glossary 詞彙表(可選)**  
  - 支援 **CSV / ODS** 多檔同時上傳。
  - 欄位格式須為 `en, zh` 或 `英文名稱, 中文名稱`。
  - 系統會自動合併詞庫；**同一英文詞條以最先出現者為準**。

> Glossary 會先進行基本標準化與比對後，再用於翻譯提示。

---

## A. Online GPT (API) 流程

### 1. 載入檔案

- 上傳 **`.ts` 檔案**。
- (可選)上傳 **Glossary(CSV / ODS)**。
- 系統會解析 `.ts` 中的 `<source>` 節點，並計算「**可翻譯句數**」。
  - 僅實際可送出翻譯的 `<source>` 會被納入統計。
  - 空字串或不含可翻譯內容者不列入處理筆數。
- 「**處理筆數上限**」預設為可翻譯句數總量，並於介面顯示 `目前 / 總數`。

### 2. 設定參數

- **API 設定**
  - `API Key`：呼叫線上模型所需金鑰
  - `Base URL`：API 服務端點
  - `Model`：欲使用之模型名稱(下拉選單)

- **處理參數**
  - `Batch`：每批送出翻譯的句數
  - `處理筆數上限`：本次任務實際處理的最大句數

> 所有設定欄位位於頁面頂部的「API 設定 / 處理參數 / 輸入檔案」區塊。

### 3. 執行翻譯

- 點擊 **「執行翻譯」** 後：
  - 頁面會即時顯示 **進度條** 與 **原文 / 譯文對照表**
  - 過程中無需重新整理頁面
- 任務完成後，訊息列會提供 **下載連結**，取得輸出檔 **`qgis_zh-Hant.ts`**。

### 格式保護

在 Online GPT 模式下，使用者可假設：

- placeholder(如: `%n`、`%1`、`%L1`、`{0}`) 不會遺失或錯置
- HTML 標籤會被保留並正確還原
- `.ts` 的 DOCTYPE 與結構維持不變
- `numerus="yes"` 的 `<numerusform>` 能正確寫回

系統會於寫回前進行基本結構檢查；若檢查失敗，該筆翻譯不會被寫入輸出檔。

---

## B. Local LLM(本機) 流程

### 1. 設定 Notebook 參數

- **檔案與目錄**
  - `輸入檔名(.ts)`
  - `輸出檔名(不含副檔名)`
  - `ODS_DIR`：Glossary 所在目錄

- **模型與 API**
  - `Model`
  - `FALLBACK_MODEL`(可留空)
  - `API Key or Token`(可留空)
  - `API Base URL`

- **其他參數**
  - `Batch`
  - `Max Tokens`
  - `Min Tokens`

### 2. 產生 Notebook 與設定檢視

- 點擊 **「下載新的 .ipynb」** 以取得完整 Notebook。
- 系統會自動在 Notebook 最前方插入一段 **Config cell**。
- 若需先確認設定內容，可使用 **「預覽 Config cell」**。

### 3. 在本機執行

- 於 **Jupyter / JupyterLab / VS Code** 開啟該 `.ipynb`。
- 視模型需求安裝相依套件、準備權重或 API。
- 可自行調整程式碼(如: 批次大小、模型切換、輸出檔名) 後逐格執行。

> 注意：Local LLM 模式下，翻譯執行與環境設定的正確性由使用者自行負責；  
> 本頁僅協助產生可重現的 Notebook 設定。

---

## 套用至 QGIS 中
1. 安裝 Qt 工具(以下以 Debian/Ubuntu 為例)
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

## 常見問題(FAQ)

**Q1. 執行 Online GPT 時，頁面顯示「請輸入 API Key / 請上傳 .ts 檔」**  
A：這是前端檢查提示，請確認 API Key 與 `.ts` 檔已填入/上傳再按「執行翻譯」。

**Q2. Glossary 上傳多檔會不會衝突？**  
A：系統會自動**合併 & 去除重複內容**，相同英文詞以**先出現**的為主；建議把優先詞庫排在最前面上傳。
> Glossary 為提示機制，實際命中仍視模型輸出而定。

**Q3. `.ts` 裡的 HTML 與 `%1 / %n / {0}` 等佔位符會被改動嗎？**  
A：不會。系統會先標記，翻譯完再還原；同時保留 DOCTYPE 與 `<numerusform>`。

**Q4. Local LLM 一鍵下載的 Notebook 長怎樣？可以先看設定嗎？**  
A：頁面會把 **Config cell** 插在 Notebook 最前面；你可用「**預覽 Config cell**」先檢視，再下載執行。

---

## 安全性與隱私建議

- **API Key 僅在瀏覽器端使用**，並只會送到你設定的 `Base URL`；請勿把金鑰與頁面公開分享。  
- 若有安全與隱私需求，可以使用 **Local LLM(本機離線)**。