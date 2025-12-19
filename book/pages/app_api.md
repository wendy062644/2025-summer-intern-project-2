---
title: API
---

# ChatGPT API 翻譯

<style>
  .bd-sidebar-secondary { display: none !important; }
  .bd-content,
  .bd-article-container,
  .tex2jax_ignore.mathjax_ignore {
    max-width: 100% !important;
    width: 100% !important;
  }
  /* —— 全部樣式只限制在 #ts-ui —— */
  #ts-ui{
    --ts-gap: 12px;
    --ts-pad: 14px;
    --ts-radius: 12px;
    --ts-border: #e5e7eb;
    --ts-bg: #fff;
    --ts-muted: #6b7280;
    --ts-text: #111827;
    --ts-accent: #2563eb;
    --ts-on-accent: #ffffff;
    --ts-progress-bg: #e5e7eb;
    --ts-table-head-bg: #f3f4f6;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans", "PingFang TC", "Microsoft JhengHei", sans-serif;
    line-height: 1.35; margin: 8px 0 16px; color: var(--ts-text);
  }
  @media (prefers-color-scheme: dark){
    #ts-ui{
      --ts-border: #2b2f36;
      --ts-bg: #111418;
      --ts-muted: #9aa3af;
      --ts-text: #e5e7eb;
    }
  }
  #ts-ui *, #ts-ui *::before, #ts-ui *::after{ box-sizing: border-box; }
  #ts-ui .ts-card{
    border:1px solid var(--ts-border); background:var(--ts-bg);
    border-radius: var(--ts-radius); padding:16px; box-shadow:0 1px 2px rgba(0,0,0,.04);
  }
  #ts-ui .ts-title{ font-size:1.05rem; font-weight:600; margin:2px 0 10px; }
  #ts-ui .ts-grid{
    display:grid; grid-template-columns: 160px 1fr; gap:10px 14px; align-items:center;
  }
  #ts-ui .ts-label{ color:var(--ts-muted); font-size:.95rem; white-space:nowrap; }
  #ts-ui .ts-input input,
  #ts-ui .ts-input select{
    width:100%; padding:8px 10px; border:1px solid var(--ts-border);
    border-radius:10px; background:transparent; font-size:.95rem;
  }
  #ts-ui .ts-input select{
    appearance:none; -webkit-appearance:none; -moz-appearance:none;
  }
  #ts-ui .ts-input input[type="file"]{ padding:6px; }
  #ts-ui .ts-inline{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
  #ts-ui .ts-hint{ color:var(--ts-muted); font-size:.9rem; }
  #ts-ui .ts-toolbar{ margin-top:10px; display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
  #ts-ui .ts-btn-primary{
    appearance:none; border:1px solid var(--ts-border);
    background:#111827; color:#fff; border-radius:10px; padding:8px 14px; font-weight:600; cursor:pointer;
  }
  @media (prefers-color-scheme: dark){ #ts-ui .ts-btn-primary{ background:#e5e7eb; color:#111418; } }
  #ts-ui .ts-btn-primary:hover{ filter:brightness(0.95); }
  #ts-ui .ts-divider{ height:1px; background:var(--ts-border); margin:12px 0; border:0; }

  /* 附屬區塊 */
  #ts-ui #ts-progress-wrap{ margin:12px 0; }

  #ts-ui #compare-box{
    border:1px solid var(--ts-border);
    border-radius:12px;
    padding:8px 12px;
    margin-top:8px;
    background:var(--ts-bg);
  }

  #ts-ui #compare-box table{
    width:100%;
    border-collapse:collapse;
    font-size:.95rem;
    table-layout: fixed;
  }

  #ts-ui #compare-box th,
  #ts-ui #compare-box td{
    padding:6px 6px;
    border-bottom:1px solid var(--ts-border);
    text-align:left;
    word-break: break-word;
    overflow-wrap: anywhere;
    white-space: normal;
  }

  #ts-ui #compare-box thead th{ font-weight:600; }

  #ts-ui #ts-ui-msg{
    color:var(--ts-muted);
    font-size:.95rem;
    margin-top:8px;
  }

  @media (max-width: 640px){
    #ts-ui .ts-grid{ grid-template-columns: 1fr; }
    #ts-ui .ts-label{ margin-top:6px; }
  }

  #ts-ui .ts-row-2{
    display: grid;
    grid-template-columns: var(--ts-col1, 1fr) var(--ts-col2, 1fr);
    gap: 10px 14px;
    align-items: center;
  }
  #ts-ui .ts-6-4{ --ts-col1: 6fr; --ts-col2: 4fr; }
  #ts-ui .ts-4-6{ --ts-col1: 4fr; --ts-col2: 6fr; }

  #ts-ui .ts-field{
    display: flex; flex-direction: column; gap: 6px;
  }
  #ts-ui .ts-field .ts-label{ margin: 0; }

  @media (max-width: 640px){
    #ts-ui .ts-row-2{ grid-template-columns: 1fr; }
  }

  #ts-ui .ts-row-3{
    display: grid;
    grid-template-columns: var(--ts-col1, 1fr) var(--ts-col2, 1fr) var(--ts-col3, 1fr);
    gap: 10px 14px;
    align-items: center;
  }
  #ts-ui .ts-3-4-3{ --ts-col1: 3fr; --ts-col2: 4fr; --ts-col3: 3fr; }

  @media (max-width: 640px){
    #ts-ui .ts-row-3{ grid-template-columns: 1fr; }
  }
  #ts-ui .left-col{ grid-column: 1 / 3; }
  
  @media (max-width:640px){
    #ts-ui{ grid-template-columns: 1fr; }
    #ts-ui .left-col,
    #ts-ui .right-col{ grid-column: 1 / -1; }
  }

  @media (prefers-color-scheme: dark){
    #ts-ui{
      --ts-bg: #0f1115;
      --ts-surface: #111418;
      --ts-surface-2: #0b0f14;
      --ts-input-bg: #0b0f14;
      --ts-border: #2b2f36;
      --ts-text: #e7eaf0;
      --ts-muted: #a6afbd;
      --ts-link: #8ab4ff;
      --ts-code-bg: #0b0f14;
      --ts-code-fg: #e7eaf0;
      --ts-accent: #3b82f6;
      --ts-on-accent: #0b0f14;
      --ts-focus: 0 0 0 2px rgba(59,130,246,.35);
      --ts-progress-bg: #1a1f29;
      --ts-table-head-bg: #121621;
    }
  }
  html[data-theme="dark"] #ts-ui{
    --ts-bg: #0f1115;
    --ts-surface: #111418;
    --ts-surface-2: #0b0f14;
    --ts-input-bg: #0b0f14;
    --ts-border: #2b2f36;
    --ts-text: #e7eaf0;
    --ts-muted: #a6afbd;
    --ts-link: #8ab4ff;
    --ts-code-bg: #0b0f14;
    --ts-code-fg: #e7eaf0;
    --ts-accent: #3b82f6;
    --ts-on-accent: #0b0f14;
    --ts-focus: 0 0 0 2px rgba(59,130,246,.35);
    --ts-progress-bg: #1a1f29;
    --ts-table-head-bg: #121621;
  }

  #ts-ui .ts-card{
    background: var(--ts-surface);
    border-color: var(--ts-border);
    color: var(--ts-text);
  }

  #ts-ui .ts-label{ color: var(--ts-muted); }
  #ts-ui .ts-hint{ color: var(--ts-muted); }

  #ts-ui .ts-input input,
  #ts-ui .ts-input select{
    background: var(--ts-input-bg);
    color: var(--ts-text);
    border-color: var(--ts-border);
  }
  #ts-ui .ts-input input:focus,
  #ts-ui .ts-input select:focus{
    outline: none;
    box-shadow: var(--ts-focus);
    border-color: color-mix(in oklab, var(--ts-accent) 60%, var(--ts-border));
  }

  #ts-ui .ts-btn-primary{
    background: var(--ts-accent);
    color: var(--ts-on-accent);
    border: 1px solid var(--ts-border);
  }
  #ts-ui .ts-btn-primary:hover{ filter: brightness(1.06); }
  #ts-ui .ts-btn-primary:focus{ outline: none; box-shadow: var(--ts-focus); }
  
  /* 暫停按鈕樣式 */
  #ts-ui .ts-btn-warning{
    background: #d97706; /* Amber 600 */
    color: #fff;
    border: 1px solid var(--ts-border);
  }
  #ts-ui .ts-btn-warning:hover{ filter: brightness(1.1); }

  #ts-ui #compare-box{
    background: var(--ts-surface);
    border-color: var(--ts-border);
  }
  #ts-ui #compare-box thead th{
    background: var(--ts-table-head-bg);
    color: var(--ts-text);
  }
  #ts-ui #compare-box td,
  #ts-ui #compare-box th{
    border-bottom: 1px solid var(--ts-border);
  }

  #ts-ui progress{ width:100%; height: 14px; background: var(--ts-progress-bg); border-radius: 8px; overflow: hidden; }
  #ts-ui progress::-webkit-progress-bar{ background: var(--ts-progress-bg); }
  #ts-ui progress::-webkit-progress-value{ background: var(--ts-accent); }
  #ts-ui progress::-moz-progress-bar{ background: var(--ts-accent); }

  #ts-ui code{
    background: var(--ts-code-bg);
    color: var(--ts-code-fg);
    padding: .1em .35em;
    border-radius: .35em;
    border: 1px solid var(--ts-border);
  }
  #ts-ui a{ color: var(--ts-link); text-underline-offset: 2px; }
  #ts-ui ::selection{
    background: color-mix(in oklab, var(--ts-accent) 35%, transparent);
  }

  @media (max-width:640px){
    html[data-theme="dark"] #ts-ui .ts-card,
    #ts-ui .ts-card{
      background: var(--ts-surface);
    }
  }
  #ts-ui .ts-field:has(#useModel2){
    flex-direction: row;
    align-items: center;
    gap: 10px;
  }
  #ts-ui .ts-field:has(#useModel2) .ts-label{ margin: 0 6px 0 0; }
  #ts-ui .ts-field:has(#useModel2) .ts-input{
    display: flex;
    align-items: center;
    gap: 10px;
  }
  #ts-ui #useModel2{
    width: 16px; height: 16px; margin: 0; vertical-align: middle;
  }
  @media (max-width:640px){
    #ts-ui .ts-field:has(#useModel2){
      flex-direction: column;
      align-items: stretch;
    }
  }
</style>

<div id="ts-ui">
  <div class="ts-card">
    <div class="ts-title">API 設定</div>
    <div class="ts-field" style="margin-bottom:10px;">
      <label class="ts-label" for="apiKey">API Key</label>
      <div class="ts-input">
        <input type="password" id="apiKey" placeholder="sk-..." autocomplete="off">
      </div>
    </div>

    <div class="ts-row-2 ts-6-4" style="margin-top:10px;">
      <div class="ts-field">
        <label class="ts-label" for="baseUrl">Base URL</label>
        <div class="ts-input">
          <input type="text" id="baseUrl" value="https://api.openai.com/v1">
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" for="modelSel">Model-1（翻譯，會產生 3 版）</label>
        <div class="ts-input">
          <div class="ts-inline" style="width:100%;">
            <select id="modelSel" style="flex:1;min-width:220px;">
              <optgroup label="GPT-5">
                <option value="gpt-5">gpt-5</option>
                <option value="gpt-5-mini">gpt-5-mini</option>
                <option value="gpt-5-nano">gpt-5-nano</option>
              </optgroup>
              <optgroup label="GPT-4.1">
                <option value="gpt-4.1">gpt-4.1</option>
                <option value="gpt-4.1-mini">gpt-4.1-mini</option>
                <option value="gpt-4.1-nano">gpt-4.1-nano</option>
              </optgroup>
              <optgroup label="GPT-4o">
                <option value="gpt-4o">gpt-4o</option>
                <option value="gpt-4o-mini" selected>gpt-4o-mini</option>
              </optgroup>
              <optgroup label="Reasoning">
                <option value="o1-mini">o1-mini</option>
                <option value="o3-mini">o3-mini</option>
              </optgroup>
              <optgroup label="Legacy">
                <option value="gpt-4-turbo">gpt-4-turbo</option>
                <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
              </optgroup>
              <optgroup label="自訂">
                <option value="__custom__">其他</option>
              </optgroup>
            </select>
            <input id="modelCustom" type="text" placeholder="例如：my-org/gpt-xy" style="display:none;flex:1;">
          </div>
        </div>
      </div>
    </div>

    <div class="ts-row-2 ts-6-4" style="margin-top:10px;">
      <div class="ts-field">
        <div class="ts-input ts-inline">
          <label for="useModel2" class="ts-inline" style="gap:8px; align-items:center; white-space:nowrap;">
            <input type="checkbox" id="useModel2" checked>
            <span class="ts-label" style="margin:0;">第二模型（挑選 + 格式校正）</span>
          </label>
          <span class="ts-hint" style="margin-left:8px; font-size: 12px">會對 3 版譯文擇優修正</span>
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" for="modelSel2">Model-2（校對/擇優）</label>
        <div class="ts-input">
          <div class="ts-inline" style="width:100%;">
            <select id="modelSel2" style="flex:1;min-width:220px;">
              <optgroup label="GPT-5">
                <option value="gpt-5">gpt-5</option>
                <option value="gpt-5-mini">gpt-5-mini</option>
                <option value="gpt-5-nano">gpt-5-nano</option>
              </optgroup>
              <optgroup label="GPT-4.1">
                <option value="gpt-4.1">gpt-4.1</option>
                <option value="gpt-4.1-mini" selected>gpt-4.1-mini</option>
                <option value="gpt-4.1-nano">gpt-4.1-nano</option>
              </optgroup>
              <optgroup label="GPT-4o">
                <option value="gpt-4o">gpt-4o</option>
                <option value="gpt-4o-mini">gpt-4o-mini</option>
              </optgroup>
              <optgroup label="Reasoning">
                <option value="o1-mini">o1-mini</option>
                <option value="o3-mini">o3-mini</option>
              </optgroup>
              <optgroup label="Legacy">
                <option value="gpt-4-turbo">gpt-4-turbo</option>
                <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
              </optgroup>
              <optgroup label="自訂">
                <option value="__custom__">其他</option>
              </optgroup>
            </select>
            <input id="modelCustom2" type="text" placeholder="例如：my-org/gpt-xy" style="display:none;flex:1;">
          </div>
        </div>
      </div>
    </div>

    <hr class="ts-divider">
    <div class="ts-title">處理參數</div>
    <div class="ts-row-3 ts-3-4-3">
      <div class="ts-field">
        <label class="ts-label" for="batch">Batch</label>
        <div class="ts-input">
          <input type="number" id="batch" value="12" min="1" max="64">
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" for="limitN">處理筆數上限</label>
        <div class="ts-input ts-inline">
          <input type="number" id="limitN" value="0" style="max-width:220px;">
          <span id="countInfo" class="ts-hint"> / 0</span>
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" for="tsFile">.ts 檔（上傳）</label>
        <div class="ts-input">
          <input type="file" id="tsFile" accept=".ts">
        </div>
      </div>
    </div>

    <!-- ✅ 新增：舊版 TS -->
    <div class="ts-field" style="margin-top:10px;">
      <label class="ts-label" for="oldTsFile">舊版 .ts（可選）</label>
      <div class="ts-input">
        <input type="file" id="oldTsFile" accept=".ts">
      </div>
      <div class="ts-hint">若舊檔已有完成翻譯，會直接套用到本次輸出並跳過 API。</div>
    </div>

    <hr class="ts-divider">
    <div class="ts-title">輸入檔案</div>
    <div class="ts-row-2" style="--ts-col1: 7fr; --ts-col2: 3fr;">
      <div class="ts-field">
        <label class="ts-label" for="glsFile">glossary（CSV / ODS）</label>
        <div class="ts-input">
          <input type="file" id="glsFile" accept=".csv,.ods" multiple>
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" style="visibility:hidden;">執行翻譯</label>
        <div class="ts-input ts-inline" style="gap:6px;">
          <button id="run-btn" class="ts-btn-primary" style="flex:2;">執行翻譯</button>
          <button id="pause-btn" class="ts-btn-primary ts-btn-warning" style="flex:1; display:none;">暫停</button>
        </div>
      </div>
      <div class="ts-hint right-col" style="margin-top:6px;">
        欄位：<code>en, zh</code> 或 <code>英文名稱, 中文名稱</code>
      </div>
    </div>

    <div id="ts-progress-wrap" style="display:none;">
      <div class="ts-inline">
        <progress id="ts-progress" value="0" max="100" style="width:100%;"></progress>
        <span id="ts-progress-label" style="font-variant-numeric: tabular-nums;">0 / 0</span>
      </div>
    </div>

    <div id="compare-box" style="display:none;">
      <div style="font-size:0.95rem;color:var(--ts-text);margin-bottom:4px;">翻譯對照（即時刷新）</div>
      <div style="max-height: 360px; overflow:auto;">
        <table>
          <thead>
            <tr>
              <th style="width:50%;">原文 (Context)</th>
              <th style="width:50%;">譯文</th>
            </tr>
          </thead>
          <tbody id="compare-tbody"></tbody>
        </table>
      </div>
    </div>

    <div id="ts-ui-msg"></div>
  </div>
</div>

<script type="module">
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.mjs";

/* =========================
 * 1) UI 先綁定（不等待 pyodide）
 * ========================= */
(function setupTsCounter(){
  const tsFile    = document.getElementById('tsFile');
  const limitN    = document.getElementById('limitN');
  const countInfo = document.getElementById('countInfo');
  countInfo.textContent = ' / 0';
  
  function needsTranslationJS(text){
    if (!text) return false;
    const t = String(text).trim();
    if (!t) return false;
    if (/^[\s\d\W%{}]+$/u.test(t)) return false;
    return true;
  }

  async function handleTsChange(){
    const file = tsFile.files && tsFile.files[0];
    if (!file){ countInfo.textContent = ' / 0'; limitN.removeAttribute('max'); return; }
    try{
      const txt = await file.text();
      let total = 0;
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(txt, 'application/xml');
      const hasErr = xmlDoc.getElementsByTagName('parsererror').length > 0;
      
      if (!hasErr){
        const sources = xmlDoc.getElementsByTagName('source');
        for (let i = 0; i < sources.length; i++){
          const s = sources[i].textContent || '';
          if (needsTranslationJS(s)) total++;
        }
      } else {
        const matches = txt.match(/<source>([\s\S]*?)<\/source>/g) || [];
        for (const m of matches){
          const inner = m.replace(/^<source>|<\/source>$/g, '');
          if (needsTranslationJS(inner)) total++;
        }
      }
      
      if (total > 0){
        limitN.value = total;
        limitN.max   = String(total);
        if (Number(limitN.value) < 1) limitN.value = 1;
        countInfo.textContent = ` / ${total}`;
      } else {
        countInfo.textContent = ' / 0';
        limitN.removeAttribute('max');
      }
    } catch(e){
      console.error(e);
      countInfo.textContent = ' / 0';
      limitN.removeAttribute('max');
    }
  }

  function clampLimit(){
    const max = Number(limitN.max || '0');
    let v = Number(limitN.value || '0');
    if (max){
      if (v > max) v = max;
      if (v < 0) v = 0;
      limitN.value = v;
    } else if (v < 0){
      limitN.value = 0;
    }
  }
  tsFile.addEventListener('change', handleTsChange);
  limitN.addEventListener('input', clampLimit);
})();

(function setupModelCustom(){
  const sel = document.getElementById('modelSel');
  const custom = document.getElementById('modelCustom');
  function sync(){ custom.style.display = (sel.value === '__custom__') ? 'block' : 'none'; }
  sel.addEventListener('change', sync);
  sync();
})();

(function setupModelCustom2(){
  const sel = document.getElementById('modelSel2');
  const custom = document.getElementById('modelCustom2');
  function sync(){ custom.style.display = (sel.value === '__custom__') ? 'block' : 'none'; }
  sel.addEventListener('change', sync);
  sync();
})();

// 暫停
window._TS_PAUSED = false;
const pauseBtn = document.getElementById("pause-btn");
pauseBtn.addEventListener("click", function(){
  window._TS_PAUSED = !window._TS_PAUSED;
  if(window._TS_PAUSED){
    pauseBtn.textContent = "繼續";
    pauseBtn.style.background = "#059669";
  } else {
    pauseBtn.textContent = "暫停";
    pauseBtn.style.background = "#d97706";
  }
});

/* =========================
 * 2) 載入 Pyodide
 * ========================= */
const $msg = document.getElementById("ts-ui-msg");
let pyodide;

const runBtn = document.getElementById("run-btn");
runBtn.disabled = true;
runBtn.textContent = "環境載入中...";

try {
  pyodide = await loadPyodide();
  await pyodide.loadPackage("micropip");

  runBtn.disabled = false;
  runBtn.textContent = "執行翻譯";

  await pyodide.runPythonAsync(String.raw`
import asyncio, json, re, io, base64, traceback, html, csv, zipfile, copy
from collections import defaultdict
from typing import List, Tuple, Dict, Optional
from xml.etree import ElementTree as ET
from js import document, window
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy

# 安裝 opencc
import micropip
await micropip.install("opencc-python-reimplemented==0.1.7")
from opencc import OpenCC

_OPENCC = OpenCC("s2twp")

# 常見台灣用語保護（避免 OpenCC 亂換）
_TW_PROTECT_TERMS = ["演算法", "專案", "圖層", "外掛", "外掛程式", "巨集", "快取", "佈局", "拓撲", "向量", "網格", "波段"]

_COORD_RE = re.compile(r"坐標")

# 遮罩：HTML tag / entity
_MASK_PAT = re.compile(
    r'(</?[A-Za-z][^>]*>|&lt;/?[A-Za-z][^&]*?&gt;|&(?!\s)[A-Za-z#x0-9]+;)',
    re.IGNORECASE
)
_SEP_RE = re.compile(r"[-\s/_.\\\\]+")
_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[\\\\/_.-][A-Za-z0-9]+)*")

# === 你的「硬提示/術語」 ===
HARD_GLOSSARY = {
    "plugin": "外掛程式",
    "plugins": "外掛程式",
    "Convex hull": "凸包",
    "convex hull": "凸包",
    "LineString": "線串",
    "Base level": "基準值",
    "Arrow head": "箭頭端",
    "Line alignment": "線條對齊",
    "Model scale": "模型縮放比例",
    "Row": "列",
    "rows": "列",
    "pixels": "像素",
    "pixel": "像素",
}

# 你的「常見錯譯」矯正（中文→中文）
POST_ZH_REPLACE = {
    "插件": "外掛程式",
    "凸殼": "凸包",
    "處理中": "處理",
}

# 快捷鍵：source 內含 &x（排除 &&）
_ACCEL_RE = re.compile(r"(?<!&)&([A-Za-z0-9])")

# ====== 基本工具 ======

def to_zh_tw(s: Optional[str]) -> str:
    if not s: return ""
    text = s
    placeholders = {}
    for i, term in enumerate(_TW_PROTECT_TERMS):
        key = f"⟦TP{i}⟧"
        placeholders[key] = term
        text = text.replace(term, key)
    try:
        text = _OPENCC.convert(text)
    except Exception:
        pass
    for key, term in placeholders.items():
        text = text.replace(key, term)
    return text

def normalize_zh(s: Optional[str]) -> str:
    if not s: return ""
    try:
        return _COORD_RE.sub("座標", s)
    except Exception:
        return s

def fix_zh_punct(s: Optional[str]) -> str:
    if not s: return ""
    return s.replace("（","(").replace("）",")").replace("：", ": ").strip()

def strip_all_newlines(s: Optional[str]) -> str:
    if not s: return ""
    return s.replace("\\n", "").replace("\\r", "").replace("\\n", "").replace("\\r", "").replace("\n", "").replace("\r", "")

def apply_zh_post_replace(s: str) -> str:
    out = s or ""
    for k, v in POST_ZH_REPLACE.items():
        out = out.replace(k, v)
    return out

def extract_accel_key(src: str) -> Optional[str]:
    if not src:
        return None
    m = _ACCEL_RE.search(src)
    if not m:
        return None
    return m.group(1)

def enforce_accel_suffix(src: str, zh: str) -> str:
    """
    規則：若 source 含 &x（且非 &&），翻譯結尾必須有 (&x)
    """
    if not zh:
        return zh
    key = extract_accel_key(src)
    if not key:
        return zh

    # 若譯文中有 &x（可能誤保留），先去掉 &（避免重複）
    zh2 = re.sub(r"(?<!&)&([A-Za-z0-9])", r"\\1", zh)

    suffix = f"(&{key})"
    # 已經正確結尾
    if zh2.endswith(suffix):
        return zh2

    # 若已經有 (&.) 結尾但不同，替換
    zh2 = re.sub(r"\\(&[A-Za-z0-9]\\)$", suffix, zh2)

    if zh2.endswith(suffix):
        return zh2

    # 若中間已經包含同樣 suffix，就不再加（但你要的是「後面加上」—這裡仍優先保證結尾）
    if suffix in zh2 and not zh2.endswith(suffix):
        zh2 = zh2.replace(suffix, "")
        zh2 = zh2.rstrip()

    return zh2.rstrip() + suffix

# ====== 翻譯後修正：避免把 Context 當成翻譯，以及保護 enum 名稱 ======
def fix_context_leak(src: str, zh: str, context: str) -> str:
    if not zh:
        return zh
    zhs = zh.strip()
    ctx = (context or "").strip()
    ctx_head = ctx.split("|", 1)[0].strip() if ctx else ""

    if ctx_head and (zhs == ctx_head or zhs.startswith(ctx_head)):
        return src
    if zhs.startswith("介面:"):
        return src
    if re.fullmatch(r"[A-Za-z0-9_]+", src) and not re.search(r"[\\u4e00-\\u9fff]", zhs):
        return src
    return zh

def repair_placeholders(src: str, trans: str) -> tuple[str, bool]:
    pat = re.compile(r"(%L\\d+|%\\d+|%[sdn]|\\{\\d+\\})")

    src_list = pat.findall(src)
    tr_list  = pat.findall(trans)

    if not src_list and not tr_list:
        return trans, True

    if len(src_list) != len(tr_list):
        return trans, False

    fixed = trans
    for s_ph, t_ph in zip(src_list, tr_list):
        if s_ph != t_ph:
            fixed = fixed.replace(t_ph, s_ph, 1)

    return fixed, (pat.findall(fixed) == src_list)

def restore_leading_symbols(src: str, trans: str) -> str:
    m = re.match(r"^([)\\]};:,.|]+)", src)
    if not m:
        return trans
    head = m.group(1)
    if trans.startswith(head):
        return trans
    for i in range(len(head)):
        suffix = head[i:]
        if trans.startswith(suffix):
            return head[:i] + trans
    return head + trans

# ====== UI Functions ======
def _set_ui_msg(msg_html: str):
    document.getElementById("ts-ui-msg").innerHTML = msg_html

def _progress_setup(total:int):
    wrap = document.getElementById("ts-progress-wrap")
    bar = document.getElementById("ts-progress")
    lab = document.getElementById("ts-progress-label")
    wrap.style.display = "block"
    bar.value = 0
    bar.max = max(1, total)
    lab.innerText = f"0 / {total}"

def _progress_tick(done:int, total:int):
    bar = document.getElementById("ts-progress")
    lab = document.getElementById("ts-progress-label")
    bar.value = done
    lab.innerText = f"{done} / {total}"

def _compare_reset():
    box = document.getElementById("compare-box")
    box.style.display = "block"
    tbody = document.getElementById("compare-tbody")
    while tbody.firstChild:
        tbody.removeChild(tbody.firstChild)

def _compare_add(src_text:str, zh_text:str, context_info:str=""):
    box = document.getElementById("compare-box")
    box.style.display = "block"
    tbody = document.getElementById("compare-tbody")
    tr = document.createElement("tr")
    
    def _td(txt, is_html=False):
        td = document.createElement("td")
        td.style.padding = "4px"
        td.style.borderBottom = "1px solid #eee"
        if is_html:
            td.innerHTML = txt
        else:
            td.textContent = txt
        return td

    display_src = src_text
    if context_info:
        display_src = (
            "<div style='font-size:0.8em; color:#666; margin-bottom:2px; "
            "padding:1px 4px; background:#f3f4f6; border-radius:4px; display:inline-block;'>"
            f"{html.escape(context_info)}</div><br>{html.escape(src_text)}"
        )
        tr.appendChild(_td(display_src, is_html=True))
    else:
        tr.appendChild(_td(src_text))

    tr.appendChild(_td(zh_text))
    tbody.appendChild(tr)

# ====== 遮罩 ======
def _mask_text(s:str):
    idx = 0
    mapping = {}
    def _repl(m):
        nonlocal idx
        k = f"⟦M{idx}⟧"
        mapping[k] = m.group(0)
        idx += 1
        return k
    return _MASK_PAT.sub(_repl, s), mapping

def _unmask_text(s:str, mapping:Dict[str,str]) -> str:
    for k,v in mapping.items():
        s = s.replace(k,v)
    return s

def _et_ready(s:str) -> str:
    try:
        return html.unescape(s)
    except Exception:
        return s

def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip():
        return False
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        return False
    return True

def soft_norm(s:str) -> str:
    return _SEP_RE.sub(" ", s.lower()).strip()

class LCSMatcher:
    def __init__(self, pairs: List[Tuple[str,str]], min_token_len:int=4, min_lcs_len:int=4):
        rows = []
        for en, zh in pairs:
            en = (en or "").strip()
            zh = (zh or "").strip()
            if en and zh:
                en_norm = en.lower()
                charset = set(re.sub(r"\\s+", "", en_norm))
                rows.append({"en":en, "zh":zh, "en_norm":en_norm, "charset":charset})
        self.rows = rows
        self.min_token_len = min_token_len
        self.min_lcs_len = min_lcs_len
        self.soft_index = {}
        self.max_soft_len = 1
        for r in rows:
            key = soft_norm(r["en"])
            if key and key not in self.soft_index:
                self.soft_index[key] = (r["en"], r["zh"])
                self.max_soft_len = max(self.max_soft_len, len(key.split()))

    def build_glossary_sentence_first(self, text:str, *, limit:int=12, per_word_k:int=3, min_lcs_len:int=4) -> Dict[str,str]:
        text_clean = _MASK_PAT.sub(" ", text)
        tokens = _TOKEN_RE.findall(text_clean)
        toks_lc = [t.lower() for t in tokens]
        n = len(toks_lc)
        covered = [False]*n
        glossary = {}

        def _mark(i,j):
            for k in range(i,j):
                covered[k] = True

        win_max = min(n, self.max_soft_len)
        for w in range(win_max, 0, -1):
            if len(glossary) >= limit:
                break
            for i in range(0, n-w+1):
                if any(covered[k] for k in range(i,i+w)):
                    continue
                phrase = " ".join(toks_lc[i:i+w])
                key = soft_norm(phrase)
                if key in self.soft_index:
                    en, zh = self.soft_index[key]
                    if en not in glossary:
                        glossary[en] = zh
                        _mark(i,i+w)
                        if len(glossary) >= limit:
                            break

        for idx, tok in enumerate(tokens):
            if len(glossary) >= limit:
                break
            if covered[idx]:
                continue
            if len(tok) < min_lcs_len:
                continue
            for r in self._topk_for_word(tok, k=per_word_k):
                if r["lcs_len"] >= min_lcs_len and r["en"] not in glossary:
                    glossary[r["en"]] = r["zh"]
                    covered[idx] = True
                    if len(glossary) >= limit:
                        break
        return glossary
        
    def _topk_for_word(self, token:str, k:int=3) -> List[Dict]:
        t_norm = token.lower()
        if len(t_norm) < self.min_token_len:
            return []
        t_chars = set(t_norm)
        cand = [r for r in self.rows if len(t_chars & r["charset"]) > 0]
        res = []
        def anchored_prefix_sub_in(token_norm:str, cand_norm:str):
            if not token_norm or not cand_norm:
                return 0,""
            max_k = min(len(token_norm), len(cand_norm))
            for kk in range(max_k,0,-1):
                sub = token_norm[:kk]
                if sub in cand_norm:
                    return kk, sub
            return 0,""
        for r in cand:
            kk, sub = anchored_prefix_sub_in(t_norm, r["en_norm"])
            if kk >= self.min_lcs_len:
                res.append({"token":token,"en":r["en"],"zh":r["zh"],"lcs_len":kk})
        res.sort(key=lambda d: (-d["lcs_len"], len(d["en"])) )
        return res[:k]

# ===== 讀 CSV / ODS =====
def load_glossary_csv_text(csv_text: Optional[str]) -> List[Tuple[str,str]]:
    if not csv_text:
        return []
    rdr = csv.DictReader(io.StringIO(csv_text))
    if not rdr.fieldnames:
        return []
    col_en = col_zh = None
    for c in rdr.fieldnames or []:
        cc = (c or "").strip().lower()
        if cc in ("en", "英文名稱"):
            col_en = c
        if cc in ("zh", "中文名稱"):
            col_zh = c
    if not col_en or not col_zh:
        return []
    pairs = []
    seen = set()
    for row in rdr:
        en = (row.get(col_en) or "").strip()
        zh = (row.get(col_zh) or "").strip()
        if en and zh and en not in seen:
            zh = normalize_zh(to_zh_tw(zh))
            pairs.append((en, zh))
            seen.add(en)
    return pairs

def load_glossary_ods_bytes(ods_bytes: bytes) -> List[Tuple[str,str]]:
    with zipfile.ZipFile(io.BytesIO(ods_bytes)) as z:
        xml = z.read("content.xml")
    ns = {
        "office":"urn:oasis:names:tc:opendocument:xmlns:office:1.0",
        "table":"urn:oasis:names:tc:opendocument:xmlns:table:1.0",
        "text":"urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    }
    root = ET.fromstring(xml)
    table = root.find(".//table:table", ns)
    if table is None:
        return []
    rows = table.findall("table:table-row", ns)
    def cell_text(cell):
        parts = []
        for p in cell.findall(".//text:p", ns):
            parts.append("".join(p.itertext()))
        return (parts[0] if parts else "").strip()
    if not rows:
        return []
    header_cells = rows[0].findall("table:table-cell", ns)
    headers = [cell_text(c) for c in header_cells]
    def _find_idx(names:set):
        for i,h in enumerate(headers):
            if (h or "").strip().lower() in names:
                return i
        return -1
    idx_en = _find_idx({"英文名稱","en"})
    idx_zh = _find_idx({"中文名稱","zh"})
    if idx_en < 0 or idx_zh < 0:
        return []
    pairs = []
    seen = set()
    for r in rows[1:]:
        cells = r.findall("table:table-cell", ns)
        if idx_en >= len(cells) or idx_zh >= len(cells):
            continue
        en = cell_text(cells[idx_en]).strip()
        zh = cell_text(cells[idx_zh]).strip()
        if en and zh and en not in seen:
            zh = normalize_zh(to_zh_tw(zh))
            pairs.append((en, zh))
            seen.add(en)
    return pairs

def merge_hard_glossary(pairs: List[Tuple[str,str]]) -> List[Tuple[str,str]]:
    out = []
    seen = set()
    for en, zh in pairs or []:
        if en and zh and en not in seen:
            out.append((en, zh))
            seen.add(en)
    for en, zh in HARD_GLOSSARY.items():
        if en not in seen:
            out.append((en, zh))
            seen.add(en)
    return out

# ===== OpenAI API 呼叫 (整合版) =====
async def call_api(api_key, base_url, model, payload, retries=1):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    url = base_url.rstrip("/") + "/chat/completions"

    mname = (model or "").lower()
    is_o1_o3   = mname.startswith("o1") or mname.startswith("o3")
    is_gpt5    = mname.startswith("gpt-5")

    # o1/o3 不接受 system → 轉 user
    if is_o1_o3:
        new_msgs = []
        for m in payload.get("messages", []):
            if m["role"] == "system":
                new_msgs.append({"role": "user", "content": f"[System Instruction]\\n{m['content']}"})
            else:
                new_msgs.append(m)
        payload["messages"] = new_msgs

    # gpt-5 / o1/o3 某些參數不收
    if is_o1_o3 or is_gpt5:
        payload.pop("temperature", None)
        payload.pop("top_p", None)
        payload.pop("presence_penalty", None)
        payload.pop("frequency_penalty", None)
        payload.pop("logit_bias", None)
        if "max_tokens" in payload and "max_completion_tokens" not in payload:
            payload["max_completion_tokens"] = payload.pop("max_tokens")

    for _ in range(retries + 1):
        try:
            resp = await pyfetch(url, method="POST", headers=headers, body=json.dumps(payload))
            data = await resp.json()
            if resp.status >= 400:
                raise Exception(f"API Error {resp.status}: {data.get('error', {}).get('message')}")

            choice = data["choices"][0]
            # tool_call → arguments JSON
            if choice["message"].get("tool_calls"):
                arg_str = choice["message"]["tool_calls"][0]["function"]["arguments"]
                return json.loads(arg_str)
            # content JSON
            if choice["message"].get("content"):
                return json.loads(choice["message"]["content"])
        except Exception:
            if _ == retries:
                return None
            await asyncio.sleep(1)
    return None

# ===== 舊檔套用邏輯 =====
def message_has_done_translation(msg: ET.Element) -> bool:
    trans = msg.find("translation")
    if trans is None:
        return False
    if trans.get("type") == "unfinished":
        return False
    if msg.get("numerus") == "yes":
        forms = trans.findall("numerusform")
        if not forms:
            return False
        return all((f.text or "").strip() for f in forms)
    return bool((trans.text or "").strip())

def finalize_zh_for_copy(src_text: str, zh: str) -> str:
    zh = _et_ready(zh or "")
    zh = strip_all_newlines(zh)
    zh = fix_zh_punct(zh)
    zh = apply_zh_post_replace(normalize_zh(to_zh_tw(zh)))
    zh, _ = repair_placeholders(src_text, zh)
    zh = fix_context_leak(src_text, zh, "")
    zh = restore_leading_symbols(src_text, zh)
    zh = enforce_accel_suffix(src_text, zh)
    return zh

def apply_translation_element(msg: ET.Element, trans_elem: ET.Element, src_text: str):
    old = msg.find("translation")
    if old is not None:
        msg.remove(old)

    new_trans = copy.deepcopy(trans_elem)
    new_trans.attrib.pop("type", None)

    if msg.get("numerus") == "yes":
        forms = new_trans.findall("numerusform")
        for f in forms:
            f.text = finalize_zh_for_copy(src_text, f.text or "")
    else:
        new_trans.text = finalize_zh_for_copy(src_text, new_trans.text or "")

    msg.append(new_trans)

def extract_old_translation_maps(old_root: ET.Element):
    ctx_map = {}
    by_src = defaultdict(list)  # source -> list of (canon, trans_elem)

    for ctx in old_root.findall("context"):
        ctx_name = (ctx.findtext("name") or "")
        for m in ctx.findall("message"):
            src_text = m.findtext("source")
            if not src_text:
                continue
            if not needs_translation(src_text):
                continue
            if not message_has_done_translation(m):
                continue
            trans = m.find("translation")
            if trans is None:
                continue

            elem = copy.deepcopy(trans)
            ctx_map[(ctx_name, src_text)] = elem
            canon = ET.tostring(elem, encoding="unicode")
            by_src[src_text].append((canon, elem))

    src_map = {}
    for src_text, items in by_src.items():
        canons = {c for c, _ in items}
        if len(canons) == 1:
            src_map[src_text] = copy.deepcopy(items[0][1])

    return ctx_map, src_map

def preview_translation_text(msg: ET.Element) -> str:
    trans = msg.find("translation")
    if trans is None:
        return ""
    if msg.get("numerus") == "yes":
        forms = trans.findall("numerusform")
        return (forms[0].text or "") if forms else ""
    return trans.text or ""

# ===== 讀檔 =====
async def read_glossaries_from_file_input(input_id: str) -> List[Tuple[str,str]]:
    files = document.getElementById(input_id).files
    if not files or files.length == 0:
        return []
    pairs_all: List[Tuple[str,str]] = []
    for i in range(files.length):
        f = files.item(i)
        name = (f.name or "").lower()
        try:
            buf = await f.arrayBuffer()
            raw = buf.to_py()
            b = raw if isinstance(raw, (bytes, bytearray)) else bytes(raw)
            if name.endswith(".ods"):
                pairs_all.extend(load_glossary_ods_bytes(b))
            elif name.endswith(".csv"):
                pairs_all.extend(load_glossary_csv_text(b.decode("utf-8","ignore")))
        except Exception as e:
            print(f"Glossary error: {e}")

    seen = set()
    dedup = []
    for en, zh in pairs_all:
        if en not in seen:
            dedup.append((en, zh))
            seen.add(en)
    return dedup

async def _read_file_text(input_id: str) -> Optional[str]:
    files = document.getElementById(input_id).files
    if not files or files.length == 0:
        return None
    buf = await files.item(0).arrayBuffer()
    return bytes(buf.to_py()).decode("utf-8", "ignore")

def _read_doctype(xml_text: str) -> str:
    m = re.search(r'<!DOCTYPE[^>]+>', xml_text)
    return m.group(0) if m else ""

# ===== 主流程 =====
async def run_translation_pipeline_async(api_key:str, base_url:str, model1:str,
                                         ts_text:str, glossary_pairs:List[Tuple[str,str]],
                                         batch_size:int=32, limit_n:int=0,
                                         use_model2:bool=False, model2:str="",
                                         old_ts_text: Optional[str]=None) -> bytes:
    doctype = _read_doctype(ts_text)
    root = ET.fromstring(ts_text)

    # 舊檔 map（可選）
    old_ctx_map, old_src_map = {}, {}
    if old_ts_text:
        try:
            old_root = ET.fromstring(old_ts_text)
            old_ctx_map, old_src_map = extract_old_translation_maps(old_root)
        except Exception:
            old_ctx_map, old_src_map = {}, {}

    glossary_pairs = merge_hard_glossary(glossary_pairs)
    matcher = LCSMatcher(glossary_pairs, min_token_len=4, min_lcs_len=4)

    tasks = []
    prefill = []
    candidate_count = 0

    for ctx in root.findall("context"):
        ctx_name = (ctx.findtext("name") or "")

        for m in ctx.findall("message"):
            src_text = m.findtext("source")
            if not src_text:
                continue
            if not needs_translation(src_text):
                continue

            # 本檔已完成翻譯 → 跳過
            if message_has_done_translation(m):
                continue

            candidate_count += 1

            extras = []
            if ctx_name:
                extras.append(f"介面: {ctx_name}")
            cmt = m.find("comment")
            if cmt is not None and cmt.text:
                extras.append(f"註釋: {cmt.text}")
            ext = m.find("extracomment")
            if ext is not None and ext.text:
                extras.append(f"說明: {ext.text}")
            ctx_str = " | ".join(extras)

            numerus = (m.get("numerus") == "yes")

            # 先 (context, source) 命中，再 source-only（僅限舊檔同 source 翻譯一致）
            old_trans = old_ctx_map.get((ctx_name, src_text)) or old_src_map.get(src_text)

            if old_trans is not None:
                prefill.append({"node": m, "src": src_text, "context": ctx_str, "numerus": numerus, "old_trans": old_trans})
            else:
                tasks.append({"node": m, "src": src_text, "context": ctx_str, "numerus": numerus})

            if limit_n > 0 and candidate_count >= limit_n:
                break
        if limit_n > 0 and candidate_count >= limit_n:
            break

    total_work = len(prefill) + len(tasks)
    if total_work == 0:
        return ET.tostring(root, encoding="utf-8")

    _compare_reset()
    _progress_setup(total_work)
    finished = 0

    # 先套用舊檔翻譯（跳過 API）
    for item in prefill:
        apply_translation_element(item["node"], item["old_trans"], item["src"])
        _compare_add(item["src"], preview_translation_text(item["node"]), item["context"])
        finished += 1
        _progress_tick(finished, total_work)

    _set_ui_msg(f"已從舊檔套用 {len(prefill)} 筆；需 API 翻譯 {len(tasks)} 筆")

    tools_schema = [{
        "type": "function",
        "function": {
            "name": "set_results",
            "description": "Save translations",
            "parameters": {
                "type": "object",
                "properties": {
                    "results": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["results"]
            }
        }
    }]

    # ===== 翻譯批次 =====
    for start in range(0, len(tasks), batch_size):
        while window._TS_PAUSED:
            await asyncio.sleep(0.2)

        batch = tasks[start:start+batch_size]

        masked_inputs = []
        maps = []
        context_list = []
        gls_list = []

        for item in batch:
            src_text = item["src"]
            g = matcher.build_glossary_sentence_first(src_text)
            gls_list.append([f"{k}->{v}" for k, v in g.items()])

            m_txt, mp = _mask_text(src_text)
            masked_inputs.append(m_txt)
            maps.append(mp)
            context_list.append(item["context"])

        items_json = json.dumps([
            {"id": k, "text": txt, "context": ctx, "glossary": gls}
            for k, (txt, ctx, gls) in enumerate(zip(masked_inputs, context_list, gls_list))
        ], ensure_ascii=False)

        sys_prompt_base = (
            "你是台灣 GIS 軟體在地化譯者。"
            " 對於每一個項目，只翻譯 text 欄位中的英文內容成繁體中文（台灣用語）。"
            " 可以參考 context 與 glossary，但不要把 context 的文字（例如「介面: ...」「註釋: ...」）當成輸出的一部分。"
            " 請呼叫工具 set_results，並只在 results 陣列中依序填入翻譯後的字串。"
            " 必須保留所有 ⟦M數字⟧ 變數與 %1、{0} 這類 placeholder，不可遺失或改變順序。"
            " 保留所有 ASCII 半形符號（例如 ()[]{};:,.?+/\\\\*& 等）。"
            " 若字串看起來是程式碼變數、常數、enum 名稱、函式名稱、人名或英文縮寫，優先保留原文不翻。"
            " 若沒有合適或確定的中文翻譯，寧可保留英文原文，不要亂造詞。"
            " 【快捷鍵規則】若原文包含 &x（x 為英數，且不是 &&），表示快捷鍵。翻譯請把快捷鍵移到最後，形式為 (&x)。"
            " 【術語優先】plugin->外掛程式；Convex hull->凸包；LineString->線串；Base level->基準值；Arrow head->箭頭端；Line alignment->線條對齊；Model scale->模型縮放比例；Row->列；pixels->像素。"
        )

        user_prompt = f"請逐一翻譯下列項目（只翻譯 text），輸出 results：\\n{items_json}"

        def _mk_payload(variant_tag: str, temp: float):
            return {
                "model": model1,
                "temperature": temp,
                "tools": tools_schema,
                "tool_choice": {"type":"function", "function":{"name":"set_results"}},
                "messages": [
                    {"role":"system", "content": sys_prompt_base + f"\\n【版本】{variant_tag}：請用不同措辭與風格提出候選譯文，但仍必須符合格式規則。"},
                    {"role":"user", "content": user_prompt + f"\\n(variant={variant_tag})"}
                ]
            }

        zh_list = []

        try:
            if use_model2 and model2:
                # === Model-1 生成 3 版（3 次 API）===
                payload_a = _mk_payload("A", 0.2)
                payload_b = _mk_payload("B", 0.8)
                payload_c = _mk_payload("C", 1.2)

                res_a, res_b, res_c = await asyncio.gather(
                    call_api(api_key, base_url, model1, payload_a),
                    call_api(api_key, base_url, model1, payload_b),
                    call_api(api_key, base_url, model1, payload_c),
                )

                list_a = res_a.get("results", []) if res_a else [""] * len(batch)
                list_b = res_b.get("results", []) if res_b else [""] * len(batch)
                list_c = res_c.get("results", []) if res_c else [""] * len(batch)

                # 補齊長度
                if len(list_a) < len(batch): list_a += [""] * (len(batch) - len(list_a))
                if len(list_b) < len(batch): list_b += [""] * (len(batch) - len(list_b))
                if len(list_c) < len(batch): list_c += [""] * (len(batch) - len(list_c))

                # === Model-2：擇優 + 校正（1 次 API）===
                sel_items = [
                    {
                        "id": k,
                        "src": t["src"],
                        "context": t["context"],
                        "glossary": gls_list[k],
                        "A": list_a[k],
                        "B": list_b[k],
                        "C": list_c[k],
                    }
                    for k, t in enumerate(batch)
                ]

                sel_payload = {
                    "model": model2,
                    "temperature": 0.1,
                    "tools": tools_schema,
                    "tool_choice": {"type":"function", "function":{"name":"set_results"}},
                    "messages": [
                        {
                            "role":"system",
                            "content": (
                                "你是嚴格的校對員與審稿者。"
                                " 對每筆資料，從 A/B/C 中選最好的，必要時融合修改，輸出最終譯文。"
                                " 必須檢查：1) placeholder 完整且順序一致（%1、{0}、⟦M⟧）；"
                                " 2) ASCII 半形符號完整（括號、分號等）；"
                                " 3) 不可把 context/註釋文字帶入譯文；"
                                " 4) 若原文含 &x（非 &&），最終譯文結尾必須有 (&x)；"
                                " 5) 术语优先：plugin->外掛程式、Convex hull->凸包、LineString->線串、Base level->基準值、Arrow head->箭頭端、Line alignment->線條對齊、Model scale->模型縮放比例、Row->列、pixels->像素。"
                                " 6) 若不確定翻譯，保留英文原文。"
                                " 只呼叫 set_results 並輸出 results 陣列。"
                            )
                        },
                        {"role":"user", "content": json.dumps(sel_items, ensure_ascii=False)}
                    ]
                }

                res_final = await call_api(api_key, base_url, model2, sel_payload)
                zh_list = res_final.get("results", []) if res_final else list_a
            else:
                # 沒開 Model-2：只跑 1 次（省 API）
                payload = {
                    "model": model1,
                    "temperature": 0.2,
                    "tools": tools_schema,
                    "tool_choice": {"type":"function", "function":{"name":"set_results"}},
                    "messages": [
                        {"role":"system", "content": sys_prompt_base},
                        {"role":"user", "content": user_prompt}
                    ]
                }
                res = await call_api(api_key, base_url, model1, payload)
                zh_list = res.get("results", []) if res else [""] * len(batch)

        except Exception as e:
            print(f"Batch failed: {e}")
            zh_list = [""] * len(batch)

        # 寫回 XML
        for k, zh_raw in enumerate(zh_list):
            if k >= len(batch):
                break
            item = batch[k]
            if not zh_raw:
                continue

            zh = _unmask_text(zh_raw, maps[k])
            zh = _et_ready(zh)
            zh = strip_all_newlines(zh)
            zh = fix_zh_punct(zh)
            zh = apply_zh_post_replace(normalize_zh(to_zh_tw(zh)))

            zh, ok_ph = repair_placeholders(item["src"], zh)
            zh = fix_context_leak(item["src"], zh, item["context"])
            zh = restore_leading_symbols(item["src"], zh)
            zh = enforce_accel_suffix(item["src"], zh)

            if not ok_ph:
                zh = f"[變數錯誤] {zh}"

            m = item["node"]
            trans = m.find("translation")
            if trans is None:
                trans = ET.SubElement(m, "translation")

            if item["numerus"]:
                forms = trans.findall("numerusform")
                if not forms:
                    forms = [ET.SubElement(trans, "numerusform")]
                for f in forms:
                    f.text = zh
            else:
                trans.text = zh

            if "type" in trans.attrib:
                trans.attrib.pop("type", None)

            _compare_add(item["src"], zh, item["context"])
            finished += 1
            _progress_tick(finished, total_work)

        _set_ui_msg(f"處理進度：{finished}/{total_work}")

    xml_bytes = ET.tostring(root, encoding="utf-8")
    head = b'<?xml version="1.0" encoding="utf-8"?>'
    if doctype:
        xml_bytes = head + doctype.encode("utf-8") + xml_bytes
    else:
        xml_bytes = head + b"\\n" + xml_bytes
    return xml_bytes

# ===== 事件入口 =====
_BUSY = False

async def _on_click(evt=None):
    global _BUSY
    if _BUSY:
        _set_ui_msg("<span style='color:#b00'>正在處理，請稍候...</span>")
        return
    _BUSY = True
    _set_ui_msg("")
    document.getElementById("pause-btn").style.display = "block"

    try:
        api = document.getElementById("apiKey").value.strip()
        base_url = document.getElementById("baseUrl").value.strip() or "https://api.openai.com/v1"

        sel1 = document.getElementById("modelSel")
        model1 = sel1.value
        if model1 == "__custom__":
            model1 = document.getElementById("modelCustom").value.strip()

        use2 = bool(document.getElementById("useModel2").checked)
        sel2 = document.getElementById("modelSel2")
        model2 = sel2.value
        if model2 == "__custom__":
            model2 = document.getElementById("modelCustom2").value.strip()

        batch = int(document.getElementById("batch").value or "32")
        limitN = int(document.getElementById("limitN").value or "0")

        if not api:
            _set_ui_msg("<span style='color:#b00'>請輸入 API Key</span>")
            return
        if not model1:
            _set_ui_msg("<span style='color:#b00'>請選擇或輸入 Model-1</span>")
            return
        if use2 and not model2:
            _set_ui_msg("<span style='color:#b00'>請選擇或輸入 Model-2</span>")
            return

        ts_text = await _read_file_text("tsFile")
        if not ts_text:
            _set_ui_msg("<span style='color:#b00'>請上傳 .ts 檔</span>")
            return

        old_ts_text = await _read_file_text("oldTsFile")  # ✅ 新增

        pairs = await read_glossaries_from_file_input("glsFile")

        _set_ui_msg("連線中...")
        xml_bytes = await run_translation_pipeline_async(
            api_key=api,
            base_url=base_url,
            model1=model1,
            ts_text=ts_text,
            glossary_pairs=pairs,
            batch_size=batch,
            limit_n=limitN,
            use_model2=use2,
            model2=model2,
            old_ts_text=old_ts_text
        )

        out_name = "qgis_zh-Hant.ts"
        b64 = base64.b64encode(xml_bytes).decode("ascii")
        link = f'<a download="{out_name}" href="data:application/octet-stream;base64,{b64}">下載 {out_name}</a>'
        _set_ui_msg(link + "　<span style='color:#0a0'>完成！</span>")
        document.getElementById("pause-btn").style.display = "none"

    except Exception as e:
        _set_ui_msg(f"<span style='color:#b00'>發生錯誤：{html.escape(str(e))}</span>")
        traceback.print_exc()
        document.getElementById("pause-btn").style.display = "none"
    finally:
        _BUSY = False

_BTN_PROXY = create_proxy(lambda evt: asyncio.ensure_future(_on_click(evt)))
document.getElementById("run-btn").addEventListener("click", _BTN_PROXY)
  `);

} catch (e) {
  console.error(e);
  $msg.innerHTML = `<span style="color:#b00">Python 載入失敗：${String(e)}</span>`;
}
</script>
