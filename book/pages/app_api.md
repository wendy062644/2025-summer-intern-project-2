---
title: API
---

# ChatGPT API 翻譯

<!-- ===== 外層 UI ===== -->
<style>
  /* —— 全部樣式只限制在 #ts-ui，並且用 --ts-* 變數，避免和主題衝突 —— */
  #ts-ui{
    --ts-gap: 12px;
    --ts-pad: 14px;
    --ts-radius: 12px;
    --ts-border: #e5e7eb;
    --ts-bg: #fff;
    --ts-muted: #6b7280;
    --ts-text: #111827;
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

  /* 附屬區塊（ID 不變，但樣式仍只在 #ts-ui 作用） */
  #ts-ui #ts-progress-wrap{ margin:12px 0; }
  #ts-ui #compare-box{
    border:1px solid var(--ts-border); border-radius:12px; padding:8px 12px; margin-top:8px; background:var(--ts-bg);
  }
  #ts-ui #compare-box table{ width:100%; border-collapse:collapse; font-size:.95rem; }
  #ts-ui #compare-box th, #ts-ui #compare-box td{ padding:6px 6px; border-bottom:1px solid var(--ts-border); text-align:left; }
  #ts-ui #compare-box thead th{ font-weight:600; }
  #ts-ui #ts-ui-msg{ color:var(--ts-muted); font-size:.95rem; margin-top:8px; }

  /* 手機版：單欄 */
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

  /* 每一欄的欄位（標籤在上、輸入在下） */
  #ts-ui .ts-field{
    display: flex; flex-direction: column; gap: 6px;
  }
  #ts-ui .ts-field .ts-label{ margin: 0; }

  /* 手機版改為單欄堆疊 */
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

  /* 手機版改為單欄 */
  @media (max-width: 640px){
    #ts-ui .ts-row-3{ grid-template-columns: 1fr; }
  }
  #ts-ui .left-col{ grid-column: 1 / 3; }
  
  @media (max-width:640px){
    #ts-ui{
      grid-template-columns: 1fr; /* 單欄 */
    }
    #ts-ui .left-col,
    #ts-ui .right-col{
      grid-column: 1 / -1; /* 滿版 */
    }
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
      --ts-accent: #3b82f6;   /* 主要強調色：按鈕、progress */
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

  /* ===== Components inherit tokens ===== */
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

  /* 表格（即時對照） */
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

  /* 進度條（跨瀏覽器） */
  #ts-ui progress{ width:100%; height: 14px; background: var(--ts-progress-bg); border-radius: 8px; overflow: hidden; }
  #ts-ui progress::-webkit-progress-bar{ background: var(--ts-progress-bg); }
  #ts-ui progress::-webkit-progress-value{ background: var(--ts-accent); }
  #ts-ui progress::-moz-progress-bar{ background: var(--ts-accent); }

  /* code 與連結 */
  #ts-ui code{
    background: var(--ts-code-bg);
    color: var(--ts-code-fg);
    padding: .1em .35em;
    border-radius: .35em;
    border: 1px solid var(--ts-border);
  }
  #ts-ui a{ color: var(--ts-link); text-underline-offset: 2px; }

  /* 選取反白 */
  #ts-ui ::selection{
    background: color-mix(in oklab, var(--ts-accent) 35%, transparent);
  }

  /* 小螢幕微調（確保深色 token 同步生效） */
  @media (max-width:640px){
    html[data-theme="dark"] #ts-ui .ts-card,
    #ts-ui .ts-card{
      background: var(--ts-surface);
    }
  }
</style>

<div id="ts-ui">
  <div class="ts-card">
    <div class="ts-title">API 設定（第一階段：翻譯）</div>
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
        <label class="ts-label" for="modelSel">Model</label>
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
                <option value="gpt-4.1-mini" selected>gpt-4.1-mini</option>
                <option value="gpt-4.1-nano">gpt-4.1-nano</option>
              </optgroup>
              <optgroup label="GPT-4o">
                <option value="gpt-4o">gpt-4o</option>
                <option value="gpt-4o-mini">gpt-4o-mini</option>
              </optgroup>
              <optgroup label="Reasoning">
                <option value="o4-mini">o4-mini</option>
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
            <!-- 選「其他」時顯示 -->
            <input id="modelCustom" type="text"
                   placeholder="例如：my-org/gpt-xy-2025-10-15"
                   style="display:none;flex:1;">
          </div>
        </div>
      </div>
    </div>

    <hr class="ts-divider">

    <div class="ts-title">API 設定（第二階段：格式修正）</div>
    <div class="ts-row-2 ts-6-4">
      <div class="ts-field">
        <label class="ts-label" for="enableStage2">啟用第二階段</label>
        <div class="ts-input ts-inline">
          <input type="checkbox" id="enableStage2" checked>
          <span class="ts-hint">基於第一階段結果，修正譯文格式以符合原文（半形括號、分隔符、%1、{0}、%n 等佔位符，避免全形）。</span>
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" for="apiKey2">API Key（第二階段）</label>
        <div class="ts-input">
          <input type="password" id="apiKey2" placeholder="若留空則沿用第一階段" autocomplete="off">
        </div>
      </div>
    </div>
    <div class="ts-row-2 ts-6-4">
      <div class="ts-field">
        <label class="ts-label" for="baseUrl2">Base URL（第二階段）</label>
        <div class="ts-input">
          <input type="text" id="baseUrl2" placeholder="若留空則沿用第一階段">
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" for="modelSel2">Model（第二階段）</label>
        <div class="ts-input">
          <div class="ts-inline" style="width:100%;">
            <select id="modelSel2" style="flex:1;min-width:220px;">
              <optgroup label="GPT-5">
                <option value="gpt-5">gpt-5</option>
                <option value="gpt-5-mini" selected>gpt-5-mini</option>
                <option value="gpt-5-nano">gpt-5-nano</option>
              </optgroup>
              <optgroup label="GPT-4.1">
                <option value="gpt-4.1">gpt-4.1</option>
                <option value="gpt-4.1-mini">gpt-4.1-mini</option>
                <option value="gpt-4.1-nano">gpt-4.1-nano</option>
              </optgroup>
              <optgroup label="GPT-4o">
                <option value="gpt-4o">gpt-4o</option>
                <option value="gpt-4o-mini">gpt-4o-mini</option>
              </optgroup>
              <optgroup label="Reasoning">
                <option value="o4-mini">o4-mini</option>
                <option value="o3-mini">o3-mini</option>
              </optgroup>
              <optgroup label="Legacy">
                <option value="gpt-4-turbo">gpt-4-turbo</option>
                <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
              </optgroup>
              <optgroup label="自訂">
                <option value="__custom2__">其他</option>
              </optgroup>
            </select>
            <input id="modelCustom2" type="text"
                   placeholder="例如：my-org/format-fixer-2025-10"
                   style="display:none;flex:1;">
          </div>
        </div>
      </div>
    </div>

    <hr class="ts-divider">

    <div class="ts-title">處理參數</div>
    <div class="ts-row-3 ts-3-4-3">
      <!-- 左：Batch (3) -->
      <div class="ts-field">
        <label class="ts-label" for="batch">Batch</label>
        <div class="ts-input">
          <input type="number" id="batch" value="32" min="1" max="64">
        </div>
      </div>
      <!-- 中：處理筆數上限 (3) -->
      <div class="ts-field">
        <label class="ts-label" for="limitN">處理筆數上限</label>
        <div class="ts-input ts-inline">
          <input type="number" id="limitN" value="0" style="max-width:220px;">
          <span id="countInfo" class="ts-hint"> / 0</span>
        </div>
      </div>
      <!-- 右：.ts 檔（上傳） (4) -->
      <div class="ts-field">
        <label class="ts-label" for="tsFile">.ts 檔（上傳）</label>
        <div class="ts-input">
          <input type="file" id="tsFile" accept=".ts">
        </div>
      </div>
    </div>

    <hr class="ts-divider">

    <div class="ts-title">輸入檔案</div>
    <div class="ts-row-2" style="--ts-col1: 7fr; --ts-col2: 3fr;">
      <!-- 左：檔案上傳 -->
      <div class="ts-field">
        <label class="ts-label" for="glsFile">glossary（CSV / ODS）</label>
        <div class="ts-input">
          <input type="file" id="glsFile" accept=".csv,.ods" multiple>
        </div>
      </div>
      <!-- 右：執行翻譯（滿寬按鈕） -->
      <div class="ts-field">
        <label class="ts-label" style="visibility:hidden;">執行翻譯</label>
        <div class="ts-input">
          <button id="run-btn" class="ts-btn-primary" style="width:100%;">執行翻譯</button>
        </div>
      </div>
      <!-- 底下補一行提示：對齊右欄 -->
      <div class="ts-hint right-col" style="margin-top:6px;">
        欄位：<code>en, zh</code> 或 <code>英文名稱, 中文名稱</code>
      </div>
    </div>
  </div>

  <!-- 進度條（ID 保持不變） -->
  <div id="ts-progress-wrap" style="display:none;">
    <div class="ts-inline">
      <progress id="ts-progress" value="0" max="100" style="width:100%;"></progress>
      <span id="ts-progress-label" style="font-variant-numeric: tabular-nums;">0 / 0</span>
    </div>
  </div>

  <!-- 對照表（ID 保持不變） -->
  <div id="compare-box" style="display:none;">
    <div style="font-size:0.95rem;color:var(--ts-text);margin-bottom:4px;">翻譯對照（即時刷新）</div>
    <div style="max-height: 360px; overflow:auto;">
      <table>
        <thead>
          <tr>
            <th style="width:40%;">原文</th>
            <th style="width:30%;">第一階段</th>
            <th style="width:30%;">第二階段</th>
          </tr>
        </thead>
        <tbody id="compare-tbody"></tbody>
      </table>
    </div>
  </div>

  <div id="ts-ui-msg"></div>
</div>

<!-- ===== Pyodide ===== -->
<script type="module">
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.mjs";
const pyodide = await loadPyodide();
await pyodide.loadPackage("micropip");

(function setupTsCounter(){
  const tsFile   = document.getElementById('tsFile');
  const limitN   = document.getElementById('limitN');
  const countInfo= document.getElementById('countInfo');

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
  const sel1 = document.getElementById('modelSel');
  const custom1 = document.getElementById('modelCustom');
  function sync1(){ custom1.style.display = (sel1.value === '__custom__') ? 'block' : 'none'; }
  sel1.addEventListener('change', sync1); sync1();

  const sel2 = document.getElementById('modelSel2');
  const custom2 = document.getElementById('modelCustom2');
  function sync2(){ custom2.style.display = (sel2.value === '__custom2__') ? 'block' : 'none'; }
  sel2.addEventListener('change', sync2); sync2();
})();

const $msg = document.getElementById("ts-ui-msg");
try {
  await pyodide.runPythonAsync(String.raw`
import asyncio, json, re, io, base64, traceback, html, csv, zipfile
from typing import List, Tuple, Dict, Optional
from xml.etree import ElementTree as ET
from js import document
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy

try:
    from opencc import OpenCC
except ModuleNotFoundError:
    import micropip
    await micropip.install("opencc-python-reimplemented==0.1.7")
    from opencc import OpenCC

_OPENCC = OpenCC("s2twp")  # 簡→繁（台灣用語）

_TW_PROTECT_TERMS = [
    "演算法",
]

def to_zh_tw(s: Optional[str]) -> str:
    if not s:
        return ""
    text = s
    placeholders = {}
    for i, term in enumerate(_TW_PROTECT_TERMS):
        key = f"⟦TWTERM{i}⟧"
        placeholders[key] = term
        text = text.replace(term, key)
    try:
        text = _OPENCC.convert(text)
    except Exception:
        pass
    for key, term in placeholders.items():
        text = text.replace(key, term)
    return text

_COORD_RE = re.compile(r"坐標")

def normalize_zh(s: Optional[str]) -> str:
    if not s:
        return ""
    try:
        return _COORD_RE.sub("座標", s)
    except Exception:
        return s

# ===== UI：訊息列 =====

def _set_ui_msg(msg_html: str):
    document.getElementById("ts-ui-msg").innerHTML = msg_html

# ===== UI：進度條 & 對照表 =====

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

def _compare_add(src_text:str, zh1_text:str, zh2_text:str):
    box = document.getElementById("compare-box")
    box.style.display = "block"
    tbody = document.getElementById("compare-tbody")
    tr = document.createElement("tr")

    def _td(txt):
        td = document.createElement("td")
        td.style.padding = "4px"
        td.style.borderBottom = "1px solid #eee"
        td.textContent = txt
        return td

    tr.appendChild(_td(src_text or ""))
    tr.appendChild(_td(zh1_text or ""))
    tr.appendChild(_td(zh2_text or ""))
    tbody.appendChild(tr)

    try:
        scroller = box.children.item(1)
        if scroller:
            scroller.scrollTop = scroller.scrollHeight
    except Exception:
        pass

# ===== 讀取上傳檔 =====
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
                txt = b.decode("utf-8", "ignore")
                pairs_all.extend(load_glossary_csv_text(txt))
        except Exception as e:
            print(f"[glossary] 讀取 {f.name} 失敗：{e}")

    seen, dedup = set(), []
    for en, zh in pairs_all:
        if en not in seen:
            dedup.append((en, zh))
            seen.add(en)
    return dedup

async def _read_file_text(input_id: str)->Optional[str]:
    files = document.getElementById(input_id).files
    if not files or files.length==0: return None
    buf = await files.item(0).arrayBuffer()
    return bytes(buf.to_py()).decode("utf-8", "ignore")

# ===== 保留 DOCTYPE =====

def _read_doctype(xml_text: str) -> str:
    m = re.search(r'<!DOCTYPE[^>]+>', xml_text)
    return m.group(0) if m else ""

# ===== 遮罩/還原（HTML/實體/%n/%1/%L1/{0} 等）=====
_MASK_PAT = re.compile(
    r'(</?[A-Za-z][^>]*>|&lt;/?[A-Za-z][^&]*?&gt;|%L\d+|%\d+|%n|\{\d+\}|&(?:[A-Za-z]+|#\d+|#x[0-9A-Fa-f]+);)',
    re.IGNORECASE
)

def _mask_text(s:str):
    idx=0; mapping={}
    def _repl(m):
        nonlocal idx
        k=f"⟦MASK{idx}⟧"; mapping[k]=m.group(0); idx+=1; return k
    return _MASK_PAT.sub(_repl, s), mapping


def _unmask_text(s:str, mapping:Dict[str,str])->str:
    for k,v in mapping.items():
        s = s.replace(k,v)
    return s


def _et_ready(s:str)->str:
    try: return html.unescape(s)
    except Exception: return s


def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip():
        return False
    if re.fullmatch(r"[\s\d\W%{}]+", en_text):
        return False
    return True

# ===== LCS 詞庫匹配（簡版）=====
_SEP_RE = re.compile(r"[-\s/_.\\]+")

def soft_norm(s:str)->str: return _SEP_RE.sub(" ", s.lower()).strip()
_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[\\/_.-][A-Za-z0-9]+)*")

class LCSMatcher:
    def __init__(self, pairs: List[Tuple[str,str]], min_token_len:int=4, min_lcs_len:int=4):
        rows = []
        for en, zh in pairs:
            en = (en or "").strip(); zh = (zh or "").strip()
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

    def build_glossary_sentence_first(self, text:str, *, limit:int=12, per_word_k:int=3, min_lcs_len:int=4)->Dict[str,str]:
        text_clean = _MASK_PAT.sub(" ", text)
        tokens = _TOKEN_RE.findall(text_clean)
        toks_lc = [t.lower() for t in tokens]
        n=len(toks_lc); covered=[False]*n; glossary={}
        def _mark(i,j):
            for k in range(i,j): covered[k]=True
        win_max = min(n, self.max_soft_len)
        for w in range(win_max, 0, -1):
            if len(glossary)>=limit: break
            for i in range(0, n-w+1):
                if any(covered[k] for k in range(i,i+w)): continue
                phrase=" ".join(toks_lc[i:i+w]); key=soft_norm(phrase)
                if key in self.soft_index:
                    en, zh = self.soft_index[key]
                    if en not in glossary:
                        glossary[en]=zh; _mark(i,i+w)
                        if len(glossary)>=limit: break
        return glossary

# ===== 讀 CSV / ODS =====

def load_glossary_csv_text(csv_text: Optional[str]) -> List[Tuple[str,str]]:
    if not csv_text:
        return []
    rdr = csv.DictReader(io.StringIO(csv_text))
    if not rdr.fieldnames:
        return []
    col_en = col_zh = None
    for c in rdr.fieldnames or []:
        cc = (c or "").strip()
        if cc in ("en", "英文名稱"): col_en = c
        if cc in ("zh", "中文名稱"): col_zh = c
    if not col_en or not col_zh:
        return []
    pairs, seen = [], set()
    for row in rdr:
        en = (row.get(col_en) or "").strip()
        zh = (row.get(col_zh) or "").strip()
        if en and zh and en not in seen:
            zh = normalize_zh(to_zh_tw(zh))
            pairs.append((en, zh))
            seen.add(en)
    return pairs


def load_glossary_ods_bytes(ods_bytes: bytes)->List[Tuple[str,str]]:
    with zipfile.ZipFile(io.BytesIO(ods_bytes)) as z:
        xml = z.read("content.xml")
    ns = {
        "office":"urn:oasis:names:tc:opendocument:xmlns:office:1.0",
        "table":"urn:oasis:names:tc:opendocument:xmlns:table:1.0",
        "text":"urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    }
    root = ET.fromstring(xml)
    table = root.find(".//table:table", ns)
    if table is None: return []
    rows = table.findall("table:table-row", ns)
    def cell_text(cell):
        parts=[]
        for p in cell.findall(".//text:p", ns):
            parts.append("".join(p.itertext()))
        return (parts[0] if parts else "").strip()
    if not rows: return []
    header_cells = rows[0].findall("table:table-cell", ns)
    headers = [cell_text(c) for c in header_cells]
    def _find_idx(names:set):
        for i,h in enumerate(headers):
            if (h or "").strip().lower() in names: return i
        return -1
    idx_en = _find_idx({"英文名稱","en"})
    idx_zh = _find_idx({"中文名稱","zh"})
    if idx_en<0 or idx_zh<0: return []
    pairs=[]; seen=set()
    for r in rows[1:]:
        cells = r.findall("table:table-cell", ns)
        if idx_en>=len(cells) or idx_zh>=len(cells): continue
        en = cell_text(cells[idx_en]).strip()
        zh = cell_text(cells[idx_zh]).strip()
        if en and zh and en not in seen:
            zh = normalize_zh(to_zh_tw(zh))
            pairs.append((en, zh)); seen.add(en)
    return pairs

# ===== OpenAI Chat/Responses 呼叫（共用）=====
async def _post_json(base_url:str, api_key:str, path:str, body:dict):
    resp = await pyfetch(base_url.rstrip("/") + path,
                         method="POST",
                         headers={"Authorization": f"Bearer {api_key}", "Content-Type":"application/json"},
                         body=json.dumps(body))
    data = await resp.json()
    return resp.status, data


def _family_and_tokens(model:str):
    m = (model or "").lower()
    new_family = m.startswith(("gpt-5", "gpt-4.1", "o4", "o3"))
    # chat.completions：舊家族多用 max_tokens，新家族常要求 max_completion_tokens
    chat_tokens_key = "max_completion_tokens" if new_family else "max_tokens"
    resp_tokens_key = "max_output_tokens"
    return new_family, chat_tokens_key, resp_tokens_key


def _extract_tool_args_from_chat(obj:dict)->Optional[str]:
    try:
        msg = obj["choices"][0]["message"]
        tcalls = msg.get("tool_calls") or []
        if not tcalls: return None
        return tcalls[0]["function"]["arguments"]
    except Exception:
        return None


def _deep_find_arguments(o):
    if isinstance(o, dict):
        if "arguments" in o and isinstance(o["arguments"], str):
            return o["arguments"]
        for v in o.values():
            r = _deep_find_arguments(v)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = _deep_find_arguments(v)
            if r is not None: return r
    return None


async def call_batch_function(api_key:str, base_url:str, model:str, *, system_prompt:str, items:List[dict], function_name:str, out_key:str, tokens:int=2048):
    new_family, chat_tokens_key, resp_tokens_key = _family_and_tokens(model)

    tools = [{
      "type": "function",
      "function": {
        "name": function_name,
        "description": "結構化輸出",
        "parameters": {
          "type": "object",
          "properties": {
            out_key: {"type": "array", "items": {"type": "string"}}
          },
          "required": [out_key],
          "additionalProperties": False
        }
      }
    }]

    user_prompt = "items = " + json.dumps(items, ensure_ascii=False)

    def build_chat_body():
        body = {
          "model": model,
          "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
          ],
          "tools": tools,
          "tool_choice": {"type": "function", "function": {"name": function_name}},
        }
        for k in ("max_tokens", "max_completion_tokens", "max_output_tokens"):
            body.pop(k, None)
        body[chat_tokens_key] = tokens
        return body

    def build_responses_body():
        body = {
          "model": model,
          "input": [
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {"role": "user",   "content": [{"type": "input_text", "text": user_prompt}]}
          ],
          "tools": tools,
          "tool_choice": {"type": "function", "function": {"name": function_name}},
        }
        for k in ("max_tokens", "max_completion_tokens", "max_output_tokens"):
            body.pop(k, None)
        body[resp_tokens_key] = tokens
        if model.lower().startswith(("gpt-5", "o4", "o3")):
            body.setdefault("reasoning", {"effort": "medium"})
        return body

    tried = []
    async def try_responses():
        status, data = await _post_json(base_url, api_key, "/responses", build_responses_body())
        tried.append(("responses", status, data))
        if status == 400:
            msg = (data.get("error", {}) or {}).get("message", "")
            if "max_output_tokens" in msg and "Unsupported" in msg:
                body = build_responses_body()
                body.pop(resp_tokens_key, None)
                body["max_completion_tokens"] = tokens
                return await _post_json(base_url, api_key, "/responses", body)
            if "reasoning" in msg.lower():
                body = build_responses_body()
                body.pop("reasoning", None)
                return await _post_json(base_url, api_key, "/responses", body)
        return status, data

    async def try_chat():
        status, data = await _post_json(base_url, api_key, "/chat/completions", build_chat_body())
        tried.append(("chat", status, data))
        if status == 400:
            msg = (data.get("error", {}) or {}).get("message", "")
            if ("Unsupported parameter" in msg or "not supported" in msg) and "max_tokens" in msg:
                body = build_chat_body()
                if chat_tokens_key == "max_completion_tokens":
                    body.pop("max_completion_tokens", None); body["max_tokens"] = tokens
                else:
                    body.pop("max_tokens", None); body["max_completion_tokens"] = tokens
                return await _post_json(base_url, api_key, "/chat/completions", body)
            if "not compatible with the chat.completions" in msg.lower():
                return await try_responses()
        return status, data

    if new_family:
        status, data = await try_responses()
        if status >= 400:
            status2, data2 = await try_chat()
            if status2 >= 400:
                raise RuntimeError(f"API Error {status2}: {data2}")
            status, data = status2, data2
    else:
        status, data = await try_chat()
        if status >= 400:
            status2, data2 = await try_responses()
            if status2 >= 400:
                raise RuntimeError(f"API Error {status2}: {data2}")
            status, data = status2, data2

    args_raw = _extract_tool_args_from_chat(data)
    if args_raw is None and "output" in data:
        args_raw = _deep_find_arguments(data["output"])
    if args_raw is None and "response" in data:
        args_raw = _deep_find_arguments(data["response"])
    if not args_raw:
        raise ValueError("模型未呼叫 function（找不到結構化輸出）。")

    parsed = json.loads(args_raw)
    arr = parsed.get(out_key)
    if not (isinstance(arr, list) and all(isinstance(x, str) for x in arr)):
        raise ValueError(f"function 參數不符合 {{{out_key}: string[]}} 格式")
    return arr

# ===== 第一階段：翻譯 =====
async def stage1_translate(api_key:str, base_url:str, model:str, masked_texts:List[str], glossaries:List[Dict[str,str]]):
    items = [{"id": i, "text": t, "glossary": [f"{en} -> {zh}" for en, zh in g.items()]}
             for i,(t,g) in enumerate(zip(masked_texts, glossaries))]
    system_prompt = """你是台灣 GIS 在地化譯者，將多個獨立英文片段翻為自然專業的繁體中文（台灣）。\n規則：\n• 保留所有 ⟦MASK數字⟧；\n• 不要解釋；\n• 不要改動任何 HTML 標籤或 HTML 實體；\n• 只輸出與輸入等長、同序的結果。"""
    return await call_batch_function(api_key, base_url, model,
                                     system_prompt=system_prompt,
                                     items=items,
                                     function_name="return_translations",
                                     out_key="translations",
                                     tokens=min(4000, 220*max(4, len(items))))

# ===== 第二階段：格式修正 =====
async def stage2_fix_format(api_key:str, base_url:str, model:str, src_texts:List[str], zh_texts:List[str]):
    # 交給模型的 items：原文 + 第一階段譯文
    items = [{"id": i, "src": s, "zh": z} for i,(s,z) in enumerate(zip(src_texts, zh_texts))]

    system_prompt = """你是資深在地化工程師。請根據原文 src，將 zh 修改為「格式完全對齊原文」的繁體中文。\n嚴格規則：\n1) 保留所有 ⟦MASK數字⟧。\n2) 保持與原文相同的佔位符與括號、引號、冒號等格式（例如 %n、%1、%L1、{0}、{1}、%d、%s、[ ]、( )、{ }、:、;、, 皆用半形，禁止全形）。\n3) 只改動格式與標點，不增刪意義內容。\n4) 不要改動任何 HTML 標籤或 HTML 實體。\n5) 回傳與輸入等長、同序的結果。"""

    return await call_batch_function(api_key, base_url, model,
                                     system_prompt=system_prompt,
                                     items=items,
                                     function_name="return_fixed",
                                     out_key="fixed",
                                     tokens=min(4000, 160*max(4, len(items))))

# ===== 主流程（加入雙階段與即時三欄對照）=====
async def run_translation_pipeline_async(api_key:str, base_url:str, model:str,
                                         api_key2:str, base_url2:str, model2:str,
                                         enable_stage2:bool,
                                         ts_text:str, glossary_pairs:List[Tuple[str,str]],
                                         batch_size:int=32, limit_n:int=0) -> bytes:
    doctype = _read_doctype(ts_text)
    root = ET.fromstring(ts_text)
    messages = root.findall(".//message")
    matcher = LCSMatcher(glossary_pairs, min_token_len=4, min_lcs_len=4)

    tasks=[]
    for m in messages:
        src=m.find("source")
        if src is None or src.text is None: continue
        if needs_translation(src.text):
            tasks.append((m, src.text, m.get("numerus")=="yes"))
        if limit_n > 0 and len(tasks) >= limit_n:
            break

    finished=0; total=len(tasks)
    if total==0:
        return ET.tostring(root, encoding="utf-8")

    _compare_reset()
    _progress_setup(total)

    for start in range(0, total, batch_size):
        batch = tasks[start:start+batch_size]
        glossaries=[]; masked_texts=[]; maps=[]; src_plain=[]
        for _, src_text, _ in batch:
            g = matcher.build_glossary_sentence_first(src_text, limit=12, per_word_k=3, min_lcs_len=4)
            glossaries.append(g)
            masked, mp = _mask_text(src_text)
            masked_texts.append(masked); maps.append(mp)
            src_plain.append(src_text)

        # 第一階段翻譯
        try:
            zh_list = await stage1_translate(api_key, base_url, model, masked_texts, glossaries)
        except Exception as e:
            # 逐筆回退
            zh_list=[]
            for masked, g in zip(masked_texts, glossaries):
                one = await stage1_translate(api_key, base_url, model, [masked], [g])
                zh_list.append(one[0])

        # 解除遮罩 + OpenCC/正規化
        zh_stage1 = [normalize_zh(to_zh_tw(_et_ready(_unmask_text(z, mp)))) for z, mp in zip(zh_list, maps)]

        # 第二階段（可選）
        if enable_stage2:
            key2 = (api_key2 or api_key).strip()
            url2 = (base_url2 or base_url).strip() or "https://api.openai.com/v1"
            try:
                zh_stage2 = await stage2_fix_format(key2, url2, model2 or model, src_plain, zh_stage1)
            except Exception:
                # 逐筆回退
                zh_stage2=[]
                for s, z in zip(src_plain, zh_stage1):
                    one = await stage2_fix_format(key2, url2, model2 or model, [s], [z])
                    zh_stage2.append(one[0])
        else:
            zh_stage2 = zh_stage1

        # 寫回 XML，並顯示三欄對照
        for (m, src_text, is_num), zh1, zh2 in zip(batch, zh_stage1, zh_stage2):
            trans = m.find("translation")
            if trans is None:
                trans = ET.SubElement(m, "translation")
            final_zh = zh2
            if is_num:
                forms = trans.findall("numerusform")
                if not forms:
                    forms=[ET.SubElement(trans, "numerusform")]
                for f in forms:
                    f.text = final_zh
            else:
                trans.text = final_zh
            if "type" in trans.attrib: trans.attrib.pop("type", None)

            _compare_add(src_text, zh1, final_zh)

            finished += 1
            _progress_tick(finished, total)

        _set_ui_msg(f"處理進度：{finished}/{total}")

    xml_bytes = ET.tostring(root, encoding="utf-8")
    head = b'<?xml version="1.0" encoding="utf-8"?>'
    if doctype: xml_bytes = head + (doctype).encode("utf-8") + xml_bytes
    else: xml_bytes = head + b"\n" + xml_bytes
    return xml_bytes

# ===== 點擊事件 =====
_BUSY=False
async def _on_click(evt=None):
    global _BUSY
    if _BUSY:
        _set_ui_msg("<span style='color:#b00'>正在處理，請稍候…</span>"); return
    _BUSY=True; _set_ui_msg("")
    try:
        api = document.getElementById("apiKey").value.strip()
        base_url = document.getElementById("baseUrl").value.strip() or "https://api.openai.com/v1"
        sel = document.getElementById("modelSel")
        model = sel.value
        if model == "__custom__":
            model = document.getElementById("modelCustom").value.strip()
        if not model:
            _set_ui_msg("<span style='color:#b00'>請選擇或輸入 model id（第一階段）</span>")
            return

        enable2 = bool(document.getElementById("enableStage2").checked)
        api2 = document.getElementById("apiKey2").value.strip() or api
        base_url2 = document.getElementById("baseUrl2").value.strip() or base_url
        sel2 = document.getElementById("modelSel2")
        model2 = sel2.value
        if model2 == "__custom2__":
            model2 = document.getElementById("modelCustom2").value.strip()
        if enable2 and not model2:
            _set_ui_msg("<span style='color:#b00'>請選擇或輸入 model id（第二階段）</span>")
            return

        batch = int(document.getElementById("batch").value or "32")
        limitN = int(document.getElementById("limitN").value or "200")
        if not api:
            _set_ui_msg("<span style='color:#b00'>請輸入 API Key（第一階段）</span>"); return
        ts_text = await _read_file_text("tsFile")
        if not ts_text:
            _set_ui_msg("<span style='color:#b00'>請上傳 .ts 檔</span>"); return

        pairs = await read_glossaries_from_file_input("glsFile")

        _set_ui_msg("⏳ 連線中…")
        xml_bytes = await run_translation_pipeline_async(
            api_key=api, base_url=base_url, model=model,
            api_key2=api2, base_url2=base_url2, model2=model2,
            enable_stage2=enable2,
            ts_text=ts_text, glossary_pairs=pairs,
            batch_size=batch, limit_n=limitN
        )

        out_name = "qgis_zh-Hant.ts"
        link = '<a download="' + out_name + '" href="data:application/octet-stream;base64,' + __import__('base64').b64encode(xml_bytes).decode('utf-8') + '">⬇️ 下載 ' + out_name + '</a>'
        _set_ui_msg(link + "　<span style='color:#0a0'>完成！</span>")
    except Exception as e:
        _set_ui_msg(f"<span style='color:#b00'>發生錯誤：{html.escape(str(e))}</span>")
        traceback.print_exc()
    finally:
        _BUSY=False

from pyodide.ffi import create_proxy
_BTN_PROXY = create_proxy(lambda evt: asyncio.ensure_future(_on_click(evt)))
document.getElementById("run-btn").addEventListener("click", _BTN_PROXY)
`);
} catch (e) {
  console.error(e);
  $msg.innerHTML = `<span style="color:#b00">Python 載入失敗：${String(e)}</span>`;
}
</script>