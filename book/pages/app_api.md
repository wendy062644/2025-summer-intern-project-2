---
title: API
thebe: false
---

# ChatGPT API 翻譯

```{raw} html
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
        <label class="ts-label" for="modelSel">Model-1（翻譯）</label>
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
          <span class="ts-hint" style="margin-left:8px; font-size: 12px">挑最佳版本並進行格式校正</span>
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" for="modelSel2">Model-2（挑選/校對）</label>
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
        <label class="ts-label" for="limitN">處理筆數上限（僅計「需翻譯」）</label>
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

    <div class="ts-row-2" style="--ts-col1: 7fr; --ts-col2: 3fr; margin-top:10px;">
      <div class="ts-field">
        <label class="ts-label" for="oldTsFile">舊版 .ts（選用：已翻譯則跳過）</label>
        <div class="ts-input">
          <input type="file" id="oldTsFile" accept=".ts">
        </div>
      </div>
      <div class="ts-hint right-col" style="margin-top:26px;">
        同 <code>&lt;source&gt;</code> 且舊檔翻譯非 unfinished → 直接套用，不呼叫 API
      </div>
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

<script>
async function __tsui_init(){
  const __root = document.getElementById("ts-ui");
  if (!__root) return;

  if (__root.dataset.inited === "1") return;

  const $ = (id) => document.getElementById(id);

  const tsFile = $("tsFile");
  const limitN = $("limitN");
  const countInfo = $("countInfo");
  const runBtn = $("run-btn");
  const pauseBtn = $("pause-btn");
  const $msg = $("ts-ui-msg");

  if (!tsFile || !limitN || !countInfo || !runBtn || !pauseBtn || !$msg) {
    console.warn("[ts-ui] DOM not ready / missing nodes");
    return;
  }

  window.__TSUI_INITED__ = true;
  __root.dataset.inited = "1";

  // ---------- 1) 先綁定 UI 事件（不等 pyodide） ----------
  function needsTranslationJS(text){
    const t = (text ?? "").toString().trim();
    return t.length > 0;
  }

  // 計算「需翻譯」數量：source 可翻 + translation 缺/unfinished
  async function handleTsChange(){
    const file = tsFile.files && tsFile.files[0];
    if (!file){ countInfo.textContent = " / 0"; limitN.removeAttribute("max"); return; }

    try{
      const txt = await file.text();
      let total = 0;

      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(txt, "application/xml");
      const hasErr = xmlDoc.getElementsByTagName("parsererror").length > 0;

      if (!hasErr){
        const contexts = xmlDoc.getElementsByTagName("context");
        for (let c = 0; c < contexts.length; c++){
          const ctx = contexts[c];
          const messages = ctx.getElementsByTagName("message");
          for (let i = 0; i < messages.length; i++){
            const m = messages[i];
            const src = m.getElementsByTagName("source")[0];
            if (!src) continue;
            const s = src.textContent || "";
            if (!hasSource(s)) continue;
            total++;
          }
        }
      } else {
        // XML 解析失敗時的備案（較粗略）
        const srcMatches = txt.match(/<message[\s\S]*?<\/message>/g) || [];
        for (const block of srcMatches){
          const msrc = block.match(/<source>([\s\S]*?)<\/source>/);
          if (!msrc) continue;
          const s = msrc[1].replace(/<[^>]+>/g, "");
          if (!hasSource(s)) continue;
          total++;
        }
      }

      if (total > 0){
        limitN.value = String(total);
        limitN.max = String(total);
        countInfo.textContent = ` / ${total}`;
      } else {
        countInfo.textContent = " / 0";
        limitN.removeAttribute("max");
      }
    } catch(e){
      console.error(e);
      countInfo.textContent = " / 0";
      limitN.removeAttribute("max");
    }
  }

  function clampLimit(){
    const max = Number(limitN.max || "0");
    let v = Number(limitN.value || "0");
    if (max){
      if (v > max) v = max;
      if (v < 0) v = 0;
      limitN.value = v;
    } else if (v < 0){
      limitN.value = 0;
    }
  }

  tsFile.addEventListener("change", handleTsChange);
  limitN.addEventListener("input", clampLimit);

  // ✅ 新增：初始化後立刻跑一次（避免「檔案已存在但 UI 未刷新」）
  // 不會移除任何功能，只是補強初始化狀態
  try { await handleTsChange(); } catch(e){ console.warn(e); }

  (function setupModelCustom(){
    const sel = $("modelSel");
    const custom = $("modelCustom");
    function sync(){ custom.style.display = (sel.value === "__custom__") ? "block" : "none"; }
    sel.addEventListener("change", sync);
    sync();
  })();

  (function setupModelCustom2(){
    const sel = $("modelSel2");
    const custom = $("modelCustom2");
    function sync(){ custom.style.display = (sel.value === "__custom__") ? "block" : "none"; }
    sel.addEventListener("change", sync);
    sync();
  })();

  // 暫停邏輯
  window._TS_PAUSED = false;
  pauseBtn.addEventListener("click", () => {
    window._TS_PAUSED = !window._TS_PAUSED;
    if (window._TS_PAUSED){
      pauseBtn.textContent = "繼續";
      pauseBtn.style.background = "#059669";
    } else {
      pauseBtn.textContent = "暫停";
      pauseBtn.style.background = "#d97706";
    }
  });

  // ---------- 2) 載入 Pyodide（用動態 import，避免 Jupyter Book module/重排問題） ----------
  runBtn.disabled = true;
  runBtn.textContent = "環境載入中...";

  let pyodide;
  try{
    const mod = await import("https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.mjs");
    pyodide = await mod.loadPyodide();
    await pyodide.loadPackage("micropip");

    runBtn.disabled = true;
    runBtn.textContent = "翻譯器初始化中...";
  } catch(e){
    console.error(e);
    $msg.innerHTML = `<span style="color:#b00">Python 載入失敗：${String(e)}</span>`;
    // （可選）允許下次再初始化
    __root.dataset.inited = "";
    window.__TSUI_INITED__ = false;
    return;
  }

  try{
    await pyodide.runPythonAsync(String.raw`
import asyncio, json, re, io, base64, traceback, html, csv, zipfile
from typing import List, Tuple, Dict, Optional, Any
from xml.etree import ElementTree as ET
from js import document, window
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy

# 安裝 opencc（第一次會比較久）
import micropip
await micropip.install("opencc-python-reimplemented==0.1.7")
from opencc import OpenCC

_OPENCC = OpenCC("s2twp")

_TW_PROTECT_TERMS = ["演算法", "專案", "圖層", "外掛", "外掛程式", "巨集", "快取", "佈局", "拓撲", "向量", "網格", "波段"]
_COORD_RE = re.compile(r"坐標")

_MASK_PAT = re.compile(
    r'(</?[A-Za-z][^>]*>|&lt;/?[A-Za-z][^&]*?&gt;|&(?!\s)[A-Za-z#x0-9]+;)',
    re.IGNORECASE
)
_SEP_RE = re.compile(r"[-\s/_.\\]+")
_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[\\/_.-][A-Za-z0-9]+)*")

# 快捷鍵：&X（忽略 &&）
_MNEMONIC_RE = re.compile(r"(?<!&)&([A-Za-z0-9])")

# 用語偏好：後處理強制修正
_TERM_REPL: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"插件"), "外掛程式"),
    (re.compile(r"凸殼"), "凸包"),
    (re.compile(r"處理中"), "處理"),
    (re.compile(r"\bLineString\b", re.IGNORECASE), "線串"),
    (re.compile(r"\bBase\s+level\b", re.IGNORECASE), "基準值"),
    (re.compile(r"\bArrow\s+head\b", re.IGNORECASE), "箭頭端"),
    (re.compile(r"\bLine\s+alignment\b", re.IGNORECASE), "線條對齊"),
    (re.compile(r"\bModel\s+scale\b", re.IGNORECASE), "模型縮放比例"),
    (re.compile(r"\bRow\b", re.IGNORECASE), "列"),
    (re.compile(r"\bpixels\b", re.IGNORECASE), "像素"),
]

def apply_term_preferences(s: str) -> str:
    if not s: return s
    out = s
    for pat, rep in _TERM_REPL:
        out = pat.sub(rep, out)
    return out

def apply_mnemonic_rule(src: str, zh: str) -> str:
    if not src or not zh: return zh
    m = _MNEMONIC_RE.search(src)
    if not m:
        return zh
    key = m.group(1)
    suffix = f"(&{key})"

    t = zh.strip()

    # 移除既有尾端快捷鍵（不論是哪個）
    t = re.sub(r"\s*\(&[A-Za-z0-9]\)\s*$", "", t).strip()
    # 移除內文中同 key 的 & 標記
    t = t.replace(f"&{key}", "")
    # 再補上正確 suffix
    return (t + suffix)

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
    if not s:
        return ""
    return s.replace("（", "(").replace("）", ")").replace("：", ":").strip()

def strip_all_newlines(s: Optional[str]) -> str:
    if not s: return ""
    return s.replace("\\n", "").replace("\\r", "").replace("\n", "").replace("\r", "")

# 避免把 Context 當成翻譯、保護 enum/代號
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
    if re.fullmatch(r"[A-Za-z0-9_]+", src) and not re.search(r"[\u4e00-\u9fff]", zhs):
        return src
    return zh

# ====== Placeholder handling (KEEP ONLY ONE VERSION) ======
_PLACEHOLDER_PAT = re.compile(r"(%L\d+|%\d+|%[sdn]|\{\d+\})")

def _ph_list(s: str) -> List[str]:
    return _PLACEHOLDER_PAT.findall(s or "")

def validate_placeholders(src: str, trans: str) -> bool:
    # 必須逐序一致（避免 %1/%2 對調）
    return _ph_list(src) == _ph_list(trans)

def repair_placeholders(src: str, trans: str) -> tuple[str, bool]:
    src_ph = _ph_list(src)
    tr_ph  = _ph_list(trans)

    if not src_ph and not tr_ph:
        return trans, True
    if len(src_ph) != len(tr_ph):
        return trans, False

    out: List[str] = []
    last = 0
    for i, m in enumerate(_PLACEHOLDER_PAT.finditer(trans or "")):
        out.append((trans or "")[last:m.start()])
        out.append(src_ph[i])
        last = m.end()
    out.append((trans or "")[last:])

    fixed = "".join(out)
    return fixed, (_ph_list(fixed) == src_ph)


def restore_leading_symbols(src: str, trans: str) -> str:
    m = re.match(r"^([)\]};:,.|]+)", src or "")
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

def _compare_add(src_text:str, zh_text:str, context_info:str="", tag:str=""):
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
    meta = []
    if tag:
        meta.append(tag)
    if context_info:
        meta.append(context_info)

    if meta:
        header = " | ".join(meta)
        display_src = (
            "<div style='font-size:0.8em; color:#666; margin-bottom:2px; "
            "padding:1px 4px; background:#f3f4f6; border-radius:4px; display:inline-block;'>"
            f"{html.escape(header)}</div><br>{html.escape(src_text)}"
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
    # 只有空白/數字/符號（含 % {}）就不用翻
    if re.fullmatch(r"[\s\d\W%{}]+", en_text):
        return False
    return True

def soft_norm(s:str) -> str:
    return _SEP_RE.sub(" ", s.lower()).strip()

# ====== glossary：LCS-ish ======
class LCSMatcher:
    def __init__(self, pairs: List[Tuple[str,str]], min_token_len:int=4, min_lcs_len:int=4):
        rows = []
        for en, zh in pairs:
            en = (en or "").strip()
            zh = (zh or "").strip()
            if en and zh:
                en_norm = en.lower()
                charset = set(re.sub(r"\s+", "", en_norm))
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

# ===== OpenAI API 呼叫 =====
async def call_api(api_key, base_url, model, payload, retries=1):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    url = base_url.rstrip("/") + "/chat/completions"

    mname = (model or "").lower()
    is_o1_o3 = mname.startswith("o1") or mname.startswith("o3")
    is_gpt5  = mname.startswith("gpt-5")

    if is_o1_o3:
        new_msgs = []
        for m in payload.get("messages", []):
            if m["role"] == "system":
                new_msgs.append({"role": "user", "content": f"[System Instruction]\\n{m['content']}"} )
            else:
                new_msgs.append(m)
        payload["messages"] = new_msgs

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
            if choice["message"].get("tool_calls"):
                arg_str = choice["message"]["tool_calls"][0]["function"]["arguments"]
                return json.loads(arg_str)
            if choice["message"].get("content"):
                return json.loads(choice["message"]["content"])
        except Exception as e:
            if _ == retries:
                return None
            await asyncio.sleep(1)
    return None

# ===== TS 工具 =====
def _read_doctype(xml_text: str) -> str:
    m = re.search(r'<!DOCTYPE[^>]+>', xml_text or "")
    return m.group(0) if m else ""

def _strip_doctype(xml_text: str) -> str:
    return re.sub(r'<!DOCTYPE[^>]+>', '', xml_text or '')

def is_translation_filled(msg: ET.Element) -> bool:
    if msg is None: return False
    tr = msg.find("translation")
    numerus = (msg.get("numerus") == "yes")
    if tr is None: return False
    if tr.get("type") == "unfinished":
        return False
    if numerus:
        forms = tr.findall("numerusform")
        if forms:
            return all((f.text or "").strip() for f in forms)
        return bool((tr.text or "").strip())
    else:
        return bool((tr.text or "").strip())

def set_translation(msg: ET.Element, text_or_list: Any):
    tr = msg.find("translation")
    if tr is None:
        tr = ET.SubElement(msg, "translation")
    # 移除 unfinished
    tr.attrib.pop("type", None)

    numerus = (msg.get("numerus") == "yes")
    if numerus:
        forms = tr.findall("numerusform")
        if not forms:
            # 建一個至少
            forms = [ET.SubElement(tr, "numerusform")]
        if isinstance(text_or_list, list):
            # 對齊數量（不足用最後一個補）
            vals = text_or_list[:]
            if len(vals) < len(forms):
                vals += [vals[-1] if vals else ""] * (len(forms) - len(vals))
            for f, v in zip(forms, vals):
                f.text = v
        else:
            # 單字串：全部 forms 用同一個
            for f in forms:
                f.text = str(text_or_list)
    else:
        tr.text = str(text_or_list)

def build_old_index(old_ts_text: str) -> Dict[str, Dict[str, Any]]:
    # source -> ctx_name -> translation (str or list)
    idx: Dict[str, Dict[str, Any]] = {}
    if not old_ts_text:
        return idx

    s = _strip_doctype(old_ts_text)
    try:
        root = ET.fromstring(s)
    except Exception:
        return idx

    for ctx in root.findall("context"):
        ctx_name_node = ctx.find("name")
        ctx_name = (ctx_name_node.text if (ctx_name_node is not None and ctx_name_node.text) else "").strip()

        for m in ctx.findall("message"):
            src_node = m.find("source")
            if src_node is None or src_node.text is None:
                continue
            src_text = src_node.text
            if not (src_text and src_text.strip()):
                continue

            tr = m.find("translation")
            if tr is None:
                continue
            if tr.get("type") == "unfinished":
                continue

            numerus = (m.get("numerus") == "yes")
            if numerus:
                forms = tr.findall("numerusform")
                if forms:
                    vals = [(f.text or "").strip() for f in forms]
                    if not all(vals):
                        continue
                    val: Any = vals
                else:
                    val = (tr.text or "").strip()
                    if not val:
                        continue
            else:
                val = (tr.text or "").strip()
                if not val:
                    continue

            idx.setdefault(src_text, {})[ctx_name] = val

    return idx

def pick_old_translation(old_map: Dict[str, Dict[str, Any]], src: str, ctx_name: str) -> Optional[Any]:
    if not old_map or not src:
        return None
    per_ctx = old_map.get(src)
    if not per_ctx:
        return None
    if ctx_name in per_ctx:
        return per_ctx[ctx_name]

    # 若同 source 在舊檔只有一種唯一譯文（跨 context 都一樣），則可安全套用
    uniq = []
    for _, v in per_ctx.items():
        if v not in uniq:
            uniq.append(v)
    if len(uniq) == 1:
        return uniq[0]
    return None

# ====== 主流程 ======
async def _read_file_text(input_id: str) -> Optional[str]:
    files = document.getElementById(input_id).files
    if not files or files.length == 0:
        return None
    buf = await files.item(0).arrayBuffer()
    return bytes(buf.to_py()).decode("utf-8", "ignore")

async def run_translation_pipeline_async(
    api_key:str, base_url:str, model1:str,
    ts_text:str,
    glossary_pairs:List[Tuple[str,str]],
    batch_size:int=32,
    limit_n:int=0,
    use_model2:bool=False,
    model2:str="",
    old_ts_text: Optional[str]=None
) -> bytes:
    doctype = _read_doctype(ts_text)
    ts_no_dt = _strip_doctype(ts_text)
    root = ET.fromstring(ts_no_dt)

    old_map = build_old_index(old_ts_text or "")

    matcher = LCSMatcher(glossary_pairs, min_token_len=4, min_lcs_len=4)

    tasks = []
    reused = 0

    # 先掃描：若舊檔有譯文就套用；剩下才進 tasks
    for ctx in root.findall("context"):
        ctx_name_node = ctx.find("name")
        ctx_name = (ctx_name_node.text if (ctx_name_node is not None and ctx_name_node.text) else "").strip()

        for m in ctx.findall("message"):
            src_node = m.find("source")
            if src_node is None or src_node.text is None:
                continue
            src_text = src_node.text

            if not needs_translation(src_text):
                continue

            # 若本來就有翻譯（非 unfinished 且有內容），直接跳過
            if is_translation_filled(m):
                continue

            # 舊檔套用
            old_val = pick_old_translation(old_map, src_text, ctx_name)
            if old_val is not None:
                set_translation(m, old_val)
                reused += 1
                # 顯示一下（可註解掉）
                _compare_add(src_text, str(old_val[0] if isinstance(old_val, list) and old_val else old_val), f"介面: {ctx_name}", tag="沿用舊版")
                continue

            # 需要翻譯者
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

            tasks.append({
                "node": m,
                "src": src_text,
                "context": ctx_str,
                "ctx_name": ctx_name,
                "numerus": (m.get("numerus") == "yes"),
            })

            if limit_n > 0 and len(tasks) >= limit_n:
                break
        if limit_n > 0 and len(tasks) >= limit_n:
            break

    total = len(tasks)
    finished = 0

    if total == 0:
        xml_bytes = ET.tostring(root, encoding="utf-8")
        head = b'<?xml version="1.0" encoding="utf-8"?>'
        if doctype:
            xml_bytes = head + b"\n" + doctype.encode("utf-8") + b"\n" + xml_bytes
        else:
            xml_bytes = head + b"\n" + xml_bytes
        return xml_bytes

    _compare_reset()
    _progress_setup(total)

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

    # 翻譯系統提示：加入快捷鍵規則、用語偏好
    sys_prompt = (
        "你是台灣 GIS 在地化譯者。"
        " 對於每一個項目，只翻譯 text 欄位中的英文內容成繁體中文（台灣用語）。"
        " 可以參考 context 與 glossary 來判斷，但不要把 context 的文字（例如「介面: .」「註釋: .」）當成輸出的一部分。"
        " 請呼叫工具 set_results，並只在 results 陣列中依序填入翻譯後的字串。"
        " 保留所有 ASCII 半形符號（例如 ()[]{};:,.?+/\\\\*& 等），數量與順序都必須與原文完全一致。"
        " 務必保留所有 ⟦M數字⟧ 變數與 %1、{0} 這類 placeholder，不可遺失或改變順序。"
        " 若字串看起來是程式碼變數、常數、enum 名稱、函式名稱、人名或英文縮寫，優先保留原文不翻。"
        " 若原文字串含有快捷鍵標記 &X（X 為字母或數字），譯文中不要出現 &X；請在譯文最後加上 ( &X )（不含空格），且 X 必須與原文一致。"
        " 用語偏好（若語意相同，優先使用）：插件→外掛程式、凸殼→凸包、處理中→處理、LineString→線串、Base level→基準值、"
        " Arrow head→箭頭端、Line alignment→線條對齊、Model scale→模型縮放比例、Row→列、pixels→像素。"
        " 若沒有合適或確定的中文翻譯，寧可保留英文原文，不要亂造詞。"
    )

    # 若沒勾 Model-2：本地挑選 A/B/C（以 placeholder 完整度與格式一致為主）
    def local_pick_best(src: str, cands: List[str]) -> str:
        if not cands:
            return ""
        best = cands[0]
        best_score = -10**9
        for cand in cands:
            if not cand:
                continue
            sc = 0
            if validate_placeholders(src, cand):
                sc += 1000
            # 較少全形標點加分（很粗略）
            if "（" not in cand and "）" not in cand and "：" not in cand:
                sc += 30
            # 長度過長稍微扣分
            sc -= max(0, len(cand) - len(src)) // 10
            if sc > best_score:
                best_score = sc
                best = cand
        return best

    def _postprocess_one(src_text: str, raw_zh: str, mp: Dict[str, str], ctx_str: str) -> str:
        zh = (raw_zh or "").strip()
        zh = _et_ready(zh)
        zh = strip_all_newlines(zh)

        zh = _unmask_text(zh, mp)

        zh = to_zh_tw(zh)
        zh = normalize_zh(zh)
        zh = apply_term_preferences(zh)
        zh = fix_zh_punct(zh)

        zh = apply_mnemonic_rule(src_text, zh)

        zh = fix_context_leak(src_text, zh, ctx_str)

        zh = restore_leading_symbols(src_text, zh)
        fixed, ok = repair_placeholders(src_text, zh)
        if ok:
            zh = fixed

        if not validate_placeholders(src_text, zh):
            zh = src_text

        return zh


    for start in range(0, total, batch_size):
        while window._TS_PAUSED:
            await asyncio.sleep(0.2)

        batch = tasks[start:start + batch_size]
        masked_inputs: List[str] = []
        maps: List[Dict[str, str]] = []
        context_list: List[str] = []
        gls_list: List[List[str]] = []

        for item in batch:
            src_text = item["src"]
            g = matcher.build_glossary_sentence_first(src_text)
            gls_list.append([f"{k}->{v}" for k, v in g.items()])

            m_txt, mp = _mask_text(src_text)
            masked_inputs.append(m_txt)
            maps.append(mp)

            context_list.append(item["context"])

        items_json = json.dumps(
            [{"id": k, "text": txt, "context": ctx, "glossary": gls}
             for k, (txt, ctx, gls) in enumerate(zip(masked_inputs, context_list, gls_list))],
            ensure_ascii=False
        )
        user_prompt = f"請逐一翻譯下列項目，僅翻譯 text 欄位內容，輸出陣列 results：\n{items_json}"

        # =========================================================
        # 取得 zh_list（raw）
        # =========================================================
        zh_list: List[str] = []

        if use_model2 and model2:
            # --- Model-1：A/B/C 三次 ---
            temps = [0.2, 0.7, 1.0]
            payloads = [{
                "model": model1,
                "temperature": t,
                "tools": tools_schema,
                "tool_choice": {"type": "function", "function": {"name": "set_results"}},
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            } for t in temps]

            resA, resB, resC = await asyncio.gather(
                call_api(api_key, base_url, model1, payloads[0]),
                call_api(api_key, base_url, model1, payloads[1]),
                call_api(api_key, base_url, model1, payloads[2]),
            )

            listA = (resA.get("results", []) if resA else [])
            listB = (resB.get("results", []) if resB else [])
            listC = (resC.get("results", []) if resC else [])

            def _pad(lst: List[str]) -> List[str]:
                if len(lst) < len(batch):
                    lst = lst + [""] * (len(batch) - len(lst))
                return lst[:len(batch)]

            listA, listB, listC = _pad(listA), _pad(listB), _pad(listC)

            # --- Model-2：仲裁 + 格式校正（一次） ---
            sel_items = [{
                "id": i,
                "src": it["src"],
                "context": it["context"],
                "glossary": gls_list[i],
                "A": listA[i],
                "B": listB[i],
                "C": listC[i],
            } for i, it in enumerate(batch)]

            sel_payload = {
                "model": model2,
                "temperature": 0.1,
                "tools": tools_schema,
                "tool_choice": {"type": "function", "function": {"name": "set_results"}},
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "你是嚴格的校對與仲裁員。"
                            " 針對每筆資料，從 A/B/C 中選出最好的譯文，必要時合併優點並修正。"
                            " 必須：placeholder 完整、ASCII 半形符號數量與順序一致、不可加入全形標點。"
                            " 不可把 context 文字輸出。"
                            " 若原文含快捷鍵 &X，請在譯文最後加上(&X)，且譯文中不要出現其他 &X。"
                            " 用語偏好：插件→外掛程式、凸殼→凸包、處理中→處理、LineString→線串、Base level→基準值、"
                            " Arrow head→箭頭端、Line alignment→線條對齊、Model scale→模型縮放比例、Row→列、pixels→像素。"
                            " 若不確定翻譯，寧可輸出原文。"
                            " 請呼叫 set_results 並輸出 results 陣列（只含字串）。"
                        )
                    },
                    {"role": "user", "content": json.dumps(sel_items, ensure_ascii=False)}
                ]
            }

            res_final = await call_api(api_key, base_url, model2, sel_payload)
            zh_list = (res_final.get("results", []) if res_final else [])

            # fallback：若 model2 失敗，就用本地挑選 A/B/C
            if not zh_list:
                zh_list = [local_pick_best(it["src"], [listA[i], listB[i], listC[i]]) for i, it in enumerate(batch)]

        else:
            # --- 沒勾第二模型：Model-1 只翻譯一次 ---
            payload = {
                "model": model1,
                "temperature": 0.2,
                "tools": tools_schema,
                "tool_choice": {"type": "function", "function": {"name": "set_results"}},
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            res1 = await call_api(api_key, base_url, model1, payload)
            zh_list = (res1.get("results", []) if res1 else [])

        # 對齊長度
        if len(zh_list) < len(batch):
            zh_list = zh_list + [""] * (len(batch) - len(zh_list))
        zh_list = zh_list[:len(batch)]

        # =========================================================
        # 寫回 XML + 更新進度/UI
        # =========================================================
        for i, item in enumerate(batch):
            src_text = item["src"]
            ctx_str = item["context"]
            ctx_name = item.get("ctx_name", "") or ""

            zh_raw = zh_list[i]
            zh_final = _postprocess_one(src_text, zh_raw, maps[i], ctx_str)

            set_translation(item["node"], zh_final)
            finished += 1
            _progress_tick(finished, total)

            _compare_add(src_text, zh_final, f"介面: {ctx_name}" if ctx_name else "", tag="翻譯")

        _set_ui_msg(f"處理進度：{finished}/{total}（另已沿用舊版 {reused} 筆）")

    xml_bytes = ET.tostring(root, encoding="utf-8")
    head = b'<?xml version="1.0" encoding="utf-8"?>'
    if doctype:
        xml_bytes = head + b"\n" + doctype.encode("utf-8") + b"\n" + xml_bytes
    else:
        xml_bytes = head + b"\n" + xml_bytes
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

        old_text = await _read_file_text("oldTsFile")

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
            old_ts_text=old_text
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

    runBtn.disabled = false;
    runBtn.textContent = "執行翻譯";
  } catch(e){
    console.error(e);
    $msg.innerHTML = `<span style="color:#b00">翻譯器初始化失敗：${String(e)}</span>`;
    runBtn.disabled = true;
    runBtn.textContent = "初始化失敗";
    __root.dataset.inited = "";
    window.__TSUI_INITED__ = false;
    return;
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  await __tsui_init();
});

if (document.readyState !== "loading") {
  __tsui_init();
}

document.addEventListener("turbo:load", () => { __tsui_init(); });
document.addEventListener("pjax:complete", () => { __tsui_init(); });

</script>
```
