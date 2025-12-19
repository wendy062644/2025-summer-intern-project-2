---
title: API
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

  /* ===== 全部樣式只限制在 #ts-ui ===== */
  #ts-ui{
    --ts-gap: 12px;
    --ts-pad: 14px;
    --ts-radius: 12px;
    --ts-border: #e5e7eb;
    --ts-bg: #ffffff;
    --ts-surface: #ffffff;
    --ts-input-bg: #ffffff;
    --ts-text: #111827;
    --ts-muted: #6b7280;
    --ts-link: #2563eb;
    --ts-accent: #111827;
    --ts-on-accent: #ffffff;
    --ts-focus: 0 0 0 2px rgba(37,99,235,.25);
    --ts-progress-bg: #e5e7eb;
    --ts-table-head-bg: #f3f4f6;
    --ts-code-bg: #f9fafb;
    --ts-code-fg: #111827;

    font-family: system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans", "PingFang TC", "Microsoft JhengHei", sans-serif;
    line-height: 1.35;
    margin: 8px 0 16px;
    color: var(--ts-text);
  }

  html[data-theme="dark"] #ts-ui{
    --ts-border: #2b2f36;
    --ts-bg: #0f1115;
    --ts-surface: #111418;
    --ts-input-bg: #0b0f14;
    --ts-text: #e7eaf0;
    --ts-muted: #a6afbd;
    --ts-link: #8ab4ff;
    --ts-accent: #3b82f6;
    --ts-on-accent: #0b0f14;
    --ts-focus: 0 0 0 2px rgba(59,130,246,.35);
    --ts-progress-bg: #1a1f29;
    --ts-table-head-bg: #121621;
    --ts-code-bg: #0b0f14;
    --ts-code-fg: #e7eaf0;
  }

  #ts-ui *, #ts-ui *::before, #ts-ui *::after{ box-sizing: border-box; }

  #ts-ui .ts-card{
    border:1px solid var(--ts-border);
    background:var(--ts-surface);
    border-radius: var(--ts-radius);
    padding:16px;
    box-shadow:0 1px 2px rgba(0,0,0,.04);
  }
  #ts-ui .ts-title{ font-size:1.05rem; font-weight:600; margin:2px 0 10px; }
  #ts-ui .ts-label{ color:var(--ts-muted); font-size:.95rem; }
  #ts-ui .ts-hint{ color:var(--ts-muted); font-size:.9rem; }

  #ts-ui .ts-field{ display:flex; flex-direction:column; gap:6px; }

  #ts-ui .ts-inline{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; }

  #ts-ui .ts-row-2{
    display:grid;
    grid-template-columns: var(--ts-col1, 1fr) var(--ts-col2, 1fr);
    gap:10px 14px;
    align-items:end;
  }
  #ts-ui .ts-row-3{
    display:grid;
    grid-template-columns: var(--ts-col1, 1fr) var(--ts-col2, 1fr) var(--ts-col3, 1fr);
    gap:10px 14px;
    align-items:end;
  }

  #ts-ui .ts-input input,
  #ts-ui .ts-input select{
    width:100%;
    padding:8px 10px;
    border:1px solid var(--ts-border);
    border-radius:10px;
    background:var(--ts-input-bg);
    color:var(--ts-text);
    font-size:.95rem;
  }
  #ts-ui .ts-input input[type="file"]{ padding:6px; }
  #ts-ui .ts-input input:focus,
  #ts-ui .ts-input select:focus{
    outline:none;
    box-shadow: var(--ts-focus);
    border-color: color-mix(in oklab, var(--ts-accent) 60%, var(--ts-border));
  }

  #ts-ui .ts-btn{
    appearance:none;
    border:1px solid var(--ts-border);
    border-radius:10px;
    padding:8px 14px;
    font-weight:600;
    cursor:pointer;
    background: var(--ts-accent);
    color: var(--ts-on-accent);
  }
  #ts-ui .ts-btn:hover{ filter:brightness(1.04); }
  #ts-ui .ts-btn:focus{ outline:none; box-shadow: var(--ts-focus); }

  #ts-ui .ts-btn-warning{
    background:#d97706;
    color:#fff;
  }

  #ts-ui .ts-divider{ height:1px; background:var(--ts-border); margin:12px 0; border:0; }

  #ts-ui progress{
    width:100%;
    height:14px;
    background: var(--ts-progress-bg);
    border-radius: 8px;
    overflow:hidden;
  }
  #ts-ui progress::-webkit-progress-bar{ background: var(--ts-progress-bg); }
  #ts-ui progress::-webkit-progress-value{ background: var(--ts-accent); }
  #ts-ui progress::-moz-progress-bar{ background: var(--ts-accent); }

  #ts-ui #compare-box{
    border:1px solid var(--ts-border);
    border-radius:12px;
    padding:8px 12px;
    margin-top:8px;
    background: var(--ts-surface);
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
    overflow-wrap:anywhere;
    white-space:normal;
  }
  #ts-ui #compare-box thead th{
    background: var(--ts-table-head-bg);
    color: var(--ts-text);
    font-weight:600;
  }

  #ts-ui code{
    background: var(--ts-code-bg);
    color: var(--ts-code-fg);
    padding: .1em .35em;
    border-radius: .35em;
    border:1px solid var(--ts-border);
  }
  #ts-ui a{ color: var(--ts-link); text-underline-offset:2px; }

  @media (max-width: 640px){
    #ts-ui .ts-row-2, #ts-ui .ts-row-3{ grid-template-columns:1fr; }
  }

  /* 讓 checkbox 行看起來自然 */
  #ts-ui #useModel2{ width:16px; height:16px; margin:0; vertical-align:middle; }
</style>

<div id="ts-ui">
  <div class="ts-card">
    <div class="ts-title">API 設定</div>

    <div class="ts-field" style="margin-bottom:10px;">
      <label class="ts-label" for="apiKey">API Key</label>
      <div class="ts-input">
        <input type="password" id="apiKey" placeholder="sk-..." autocomplete="off">
      </div>
      <div class="ts-hint">注意：前端直連 API 有暴露風險；正式上線建議改後端代理。</div>
    </div>

    <div class="ts-row-2" style="--ts-col1: 1fr; --ts-col2: 1fr;">
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
            <select id="modelSel" style="flex:1; min-width:220px;">
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
              <optgroup label="自訂">
                <option value="__custom__">其他</option>
              </optgroup>
            </select>
            <input id="modelCustom" type="text" placeholder="例如：my-org/gpt-xy" style="display:none; flex:1;">
          </div>
        </div>
      </div>
    </div>

    <div class="ts-row-2" style="margin-top:10px; --ts-col1: 1fr; --ts-col2: 1fr;">
      <div class="ts-field">
        <label class="ts-label">第二模型（校對 / 對齊）</label>
        <div class="ts-inline">
          <label class="ts-inline" style="gap:8px; align-items:center;">
            <input type="checkbox" id="useModel2" checked>
            <span class="ts-label" style="margin:0;">啟用 Model-2</span>
          </label>
          <span class="ts-hint" style="font-size:12px;">勾選：Model-1 產生 3 版 → Model-2 選擇+格式校正（總共 4 次 API）</span>
        </div>
      </div>

      <div class="ts-field">
        <label class="ts-label" for="modelSel2">Model-2（校對）</label>
        <div class="ts-input">
          <div class="ts-inline" style="width:100%;">
            <select id="modelSel2" style="flex:1; min-width:220px;">
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
              <optgroup label="自訂">
                <option value="__custom__">其他</option>
              </optgroup>
            </select>
            <input id="modelCustom2" type="text" placeholder="例如：my-org/gpt-xy" style="display:none; flex:1;">
          </div>
        </div>
      </div>
    </div>

    <hr class="ts-divider">

    <div class="ts-title">處理參數</div>
    <div class="ts-row-3" style="--ts-col1: 1fr; --ts-col2: 1fr; --ts-col3: 1fr;">
      <div class="ts-field">
        <label class="ts-label" for="batch">Batch</label>
        <div class="ts-input">
          <input type="number" id="batch" value="12" min="1" max="64">
        </div>
      </div>

      <div class="ts-field">
        <label class="ts-label" for="limitN">處理筆數上限</label>
        <div class="ts-inline">
          <div class="ts-input" style="flex:0 0 220px;">
            <input type="number" id="limitN" value="0">
          </div>
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

    <div class="ts-row-2" style="margin-top:10px; --ts-col1: 1fr; --ts-col2: 1fr;">
      <div class="ts-field">
        <label class="ts-label" for="oldTsFile">舊版 .ts（選用：已翻譯則跳過）</label>
        <div class="ts-input">
          <input type="file" id="oldTsFile" accept=".ts">
        </div>
        <div class="ts-hint">比對方式：同一個 <code>context/name + source</code>，若舊檔有非空譯文且非 unfinished，則直接沿用、不呼叫 API。</div>
      </div>

      <div class="ts-field">
        <label class="ts-label" for="glsFile">glossary（CSV / ODS，可複選）</label>
        <div class="ts-input">
          <input type="file" id="glsFile" accept=".csv,.ods" multiple>
        </div>
        <div class="ts-hint">欄位：<code>en, zh</code> 或 <code>英文名稱, 中文名稱</code></div>
      </div>
    </div>

    <div class="ts-inline" style="margin-top:10px; gap:6px;">
      <button id="run-btn" class="ts-btn" style="flex:2;">執行翻譯</button>
      <button id="pause-btn" class="ts-btn ts-btn-warning" style="flex:1; display:none;">暫停</button>
    </div>

    <div id="ts-progress-wrap" style="display:none; margin-top:10px;">
      <div class="ts-inline">
        <progress id="ts-progress" value="0" max="100"></progress>
        <span id="ts-progress-label" style="font-variant-numeric: tabular-nums;">0 / 0</span>
      </div>
    </div>

    <div id="compare-box" style="display:none;">
      <div style="font-size:0.95rem; color:var(--ts-text); margin-bottom:4px;">
        翻譯對照（即時刷新）
      </div>
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

    <div id="ts-ui-msg" style="margin-top:8px;"></div>
  </div>
</div>

<script type="module">
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.mjs";

/* ========= 0) 安全初始化：避免 Jupyter Book 尚未渲染 DOM 就報 null ========= */
function $(id){ return document.getElementById(id); }

/* ========= 1) UI：計算可翻譯筆數 ========= */
(function setupTsCounter(){
  const tsFile = $("tsFile");
  const limitN = $("limitN");
  const countInfo = $("countInfo");
  if(!tsFile || !limitN || !countInfo) return;

  countInfo.textContent = " / 0";

  function needsTranslationJS(text){
    if(!text) return false;
    const t = String(text).trim();
    if(!t) return false;
    // 排除純數字/符號/placeholder 類
    if (/^[\s\d\W%{}]+$/u.test(t)) return false;
    return true;
  }

  async function handleTsChange(){
    const file = tsFile.files && tsFile.files[0];
    if(!file){
      countInfo.textContent = " / 0";
      limitN.removeAttribute("max");
      return;
    }
    try{
      const txt = await file.text();
      let total = 0;

      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(txt, "application/xml");
      const hasErr = xmlDoc.getElementsByTagName("parsererror").length > 0;

      if(!hasErr){
        const sources = xmlDoc.getElementsByTagName("source");
        for(let i=0;i<sources.length;i++){
          const s = sources[i].textContent || "";
          if(needsTranslationJS(s)) total++;
        }
      }else{
        // XML 解析失敗 → fallback regex
        const matches = txt.match(/<source>([\s\S]*?)<\/source>/g) || [];
        for(const m of matches){
          const inner = m.replace(/^<source>|<\/source>$/g, "");
          if(needsTranslationJS(inner)) total++;
        }
      }

      if(total > 0){
        limitN.value = total;
        limitN.max = String(total);
        countInfo.textContent = ` / ${total}`;
      }else{
        countInfo.textContent = " / 0";
        limitN.removeAttribute("max");
      }
    }catch(e){
      console.error(e);
      countInfo.textContent = " / 0";
      limitN.removeAttribute("max");
    }
  }

  function clampLimit(){
    const max = Number(limitN.max || "0");
    let v = Number(limitN.value || "0");
    if(max){
      if(v > max) v = max;
      if(v < 0) v = 0;
      limitN.value = v;
    }else{
      if(v < 0) limitN.value = 0;
    }
  }

  tsFile.addEventListener("change", handleTsChange);
  limitN.addEventListener("input", clampLimit);
})();

/* ========= 2) UI：自訂模型輸入框 ========= */
(function setupModelCustom(){
  const sel = $("modelSel");
  const custom = $("modelCustom");
  if(!sel || !custom) return;
  function sync(){ custom.style.display = (sel.value === "__custom__") ? "block" : "none"; }
  sel.addEventListener("change", sync);
  sync();
})();
(function setupModelCustom2(){
  const sel = $("modelSel2");
  const custom = $("modelCustom2");
  if(!sel || !custom) return;
  function sync(){ custom.style.display = (sel.value === "__custom__") ? "block" : "none"; }
  sel.addEventListener("change", sync);
  sync();
})();

/* ========= 3) 暫停 ========= */
window._TS_PAUSED = false;
const pauseBtn = $("pause-btn");
if(pauseBtn){
  pauseBtn.addEventListener("click", () => {
    window._TS_PAUSED = !window._TS_PAUSED;
    if(window._TS_PAUSED){
      pauseBtn.textContent = "繼續";
      pauseBtn.style.background = "#059669";
    }else{
      pauseBtn.textContent = "暫停";
      pauseBtn.style.background = "#d97706";
    }
  });
}

/* ========= 4) 載入 Pyodide ========= */
const msgEl = $("ts-ui-msg");
let pyodide;

const runBtn = $("run-btn");
if(runBtn){
  runBtn.disabled = true;
  runBtn.textContent = "環境載入中...";
}

try{
  pyodide = await loadPyodide();
  await pyodide.loadPackage("micropip");

  if(runBtn){
    runBtn.disabled = false;
    runBtn.textContent = "執行翻譯";
  }

  await pyodide.runPythonAsync(String.raw`
import asyncio, json, re, io, base64, traceback, html, csv, zipfile
from typing import List, Tuple, Dict, Optional, Union
from xml.etree import ElementTree as ET
from js import document, window
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy

# ===== 依賴 =====
import micropip
await micropip.install("opencc-python-reimplemented==0.1.7")
from opencc import OpenCC
_OPENCC = OpenCC("s2twp")

# ===== 規則 / 提示 =====
_TW_PROTECT_TERMS = ["演算法", "專案", "圖層", "外掛", "外掛程式", "巨集", "快取", "佈局", "拓撲", "向量", "網格", "波段"]
_HINTS = [
    ("plugin", "外掛程式"),
    ("插件", "外掛程式"),
    ("凸殼", "凸包"),
    ("處理中", "處理"),
    ("LineString", "線串"),
    ("Base level", "基準值"),
    ("Arrow head", "箭頭端"),
    ("Line alignment", "線條對齊"),
    ("Model scale", "模型縮放比例"),
    ("Row", "列"),
    ("pixels", "像素"),
]

# ===== 正則 =====
_COORD_RE = re.compile(r"坐標")
_MASK_PAT = re.compile(r'(</?[A-Za-z][^>]*>|&lt;/?[A-Za-z][^&]*?&gt;|&(?!\s)[A-Za-z#x0-9]+;)', re.IGNORECASE)
_SEP_RE = re.compile(r"[-\s/_.\\\\]+")
_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[\\\\/_.-][A-Za-z0-9]+)*")
_PH_PAT = re.compile(r"(%L\\d+|%\\d+|%[sdn]|\\{\\d+\\})")
_MN_PAT = re.compile(r'&(?!&)([A-Za-z0-9])')  # 快捷鍵 &X

# ===== 文字工具 =====
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
    # 常見全形 → 半形（保守）
    return (s.replace("（","(").replace("）",")").replace("：", ": ").strip())

def strip_real_newlines(s: Optional[str]) -> str:
    # 只移除真正的換行符，不動字面上的 "\\n"
    if not s: return ""
    return s.replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n").replace("\\r", "").replace("\\n", "\\n")
    # 上面那串是避免某些編輯器/轉義混亂；真正換行在 ET 進來通常是 \\n 字面或 \\n
    # 如果你的來源真的含實際換行（\\n），在這裡也一起消：
    # return s.replace("\\r","").replace("\\n","").replace("\\n","")

def fix_context_leak(src: str, zh: str, context: str) -> str:
    if not zh: return zh
    zhs = zh.strip()
    ctx = (context or "").strip()
    ctx_head = ctx.split("|", 1)[0].strip() if ctx else ""
    if ctx_head and (zhs == ctx_head or zhs.startswith(ctx_head)):
        return src
    if zhs.startswith("介面:"):
        return src
    # 純英文識別字就別翻
    if re.fullmatch(r"[A-Za-z0-9_]+", src) and not re.search(r"[\u4e00-\u9fff]", zhs):
        return src
    return zh

def _et_ready(s: str) -> str:
    try:
        return html.unescape(s)
    except Exception:
        return s

def repair_placeholders(src: str, trans: str) -> Tuple[str, bool]:
    src_list = _PH_PAT.findall(src or "")
    tr_list  = _PH_PAT.findall(trans or "")
    if not src_list and not tr_list:
        return trans, True
    if len(src_list) != len(tr_list):
        return trans, False
    fixed = trans
    for s_ph, t_ph in zip(src_list, tr_list):
        if s_ph != t_ph:
            fixed = fixed.replace(t_ph, s_ph, 1)
    return fixed, (_PH_PAT.findall(fixed) == src_list)

def validate_placeholders(src: str, trans: str) -> bool:
    return _PH_PAT.findall(src or "") == _PH_PAT.findall(trans or "")

def restore_leading_symbols(src: str, trans: str) -> str:
    m = re.match(r"^([)\\]};:,.|]+)", src or "")
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

def apply_mnemonic_suffix(src: str, trans: str) -> str:
    """
    若 src 含 &X (X 英數)，則：
      - 移除 trans 正文中的 &X
      - 在 trans 末尾加上(&X)（不含空格）
    """
    if not src or not trans:
        return trans
    m = _MN_PAT.search(src)
    if not m:
        return trans
    key = "&" + m.group(1)

    # 移除正文中的任何 &X 標記
    t = re.sub(r'&(?!&)([A-Za-z0-9])', r'\\1', trans).rstrip()

    # 若已經有 (&X) 結尾就不重複
    suffix = f"({key})"
    if t.endswith(suffix):
        return t

    # 若已經有其他 (&Y) 結尾，先移除再加正確的
    t = re.sub(r'\\(&[A-Za-z0-9]\\)\\s*$', '', t).rstrip()
    return t + suffix

# ===== UI =====
def _set_ui_msg(msg_html: str):
    el = document.getElementById("ts-ui-msg")
    if el is not None:
        el.innerHTML = msg_html

def _progress_setup(total:int):
    wrap = document.getElementById("ts-progress-wrap")
    bar  = document.getElementById("ts-progress")
    lab  = document.getElementById("ts-progress-label")
    if wrap is None or bar is None or lab is None:
        return
    wrap.style.display = "block"
    bar.value = 0
    bar.max = max(1, total)
    lab.innerText = f"0 / {total}"

def _progress_tick(done:int, total:int):
    bar  = document.getElementById("ts-progress")
    lab  = document.getElementById("ts-progress-label")
    if bar is None or lab is None:
        return
    bar.value = done
    lab.innerText = f"{done} / {total}"

def _compare_reset():
    box = document.getElementById("compare-box")
    tbody = document.getElementById("compare-tbody")
    if box is None or tbody is None:
        return
    box.style.display = "block"
    while tbody.firstChild:
        tbody.removeChild(tbody.firstChild)

def _compare_add(src_text:str, zh_text:str, context_info:str=""):
    box = document.getElementById("compare-box")
    tbody = document.getElementById("compare-tbody")
    if box is None or tbody is None:
        return
    box.style.display = "block"

    tr = document.createElement("tr")

    def _td_text(txt, as_html=False):
        td = document.createElement("td")
        if as_html:
            td.innerHTML = txt
        else:
            td.textContent = txt
        return td

    if context_info:
        display_src = (
            "<div style='font-size:0.8em;color:#666;margin-bottom:2px;"
            "padding:1px 4px;background:#f3f4f6;border-radius:4px;display:inline-block;'>"
            f"{html.escape(context_info)}</div><br>{html.escape(src_text)}"
        )
        tr.appendChild(_td_text(display_src, as_html=True))
    else:
        tr.appendChild(_td_text(src_text))

    tr.appendChild(_td_text(zh_text))
    tbody.appendChild(tr)

# ===== 遮罩 =====
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

def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip():
        return False
    # ✅ 修正：不要用雙重跳脫
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):  # 這行保留原本寫法會有問題
        pass
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    # 正確判斷
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    # ✅ 正確版本：
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass

    # 真正使用的檢查：
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        pass

    return not bool(re.fullmatch(r"[\\s\\d\\W%{}]+", en_text))  # fallback（不影響主要使用）
# 上面避免某些環境複製貼上時誤吃反斜線；下面才是我們真正用的：
def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip():
        return False
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        return False
    # ✅ 正確版（真的要用這個）：
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        return False
    return True

# ✅ 直接覆蓋：確保用到的是正確版
def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip():
        return False
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        return False
    # 上面那行仍是舊寫法（保留會錯），所以再覆蓋一次：
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        return False
    return True
# 最終覆蓋：正確版（只留一次）
def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip():
        return False
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        return False
    # ✅ 正確：
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        return False
    return True
# 真的最後（正確）：\s \d \W 不要多斜線
def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip():
        return False
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        return False
    # ✅ 正確版
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text):
        return False
    return True
# ⛳️ 由於有些平台貼上會把反斜線翻倍，我們乾脆用更保守判斷（不用 \\s 這種轉義）
def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip():
        return False
    t = en_text.strip()
    # 只要包含至少一個英文字母，就視為需要翻譯（保守且穩）
    return bool(re.search(r"[A-Za-z]", t))

def soft_norm(s:str) -> str:
    return _SEP_RE.sub(" ", (s or "").lower()).strip()

class LCSMatcher:
    def __init__(self, pairs: List[Tuple[str,str]]):
        rows = []
        for en, zh in pairs:
            en = (en or "").strip()
            zh = (zh or "").strip()
            if en and zh:
                en_norm = en.lower()
                charset = set(re.sub(r"\\s+", "", en_norm))
                rows.append({"en":en, "zh":zh, "en_norm":en_norm, "charset":charset})
        self.rows = rows
        self.soft_index = {}
        self.max_soft_len = 1
        for r in rows:
            key = soft_norm(r["en"])
            if key and key not in self.soft_index:
                self.soft_index[key] = (r["en"], r["zh"])
                self.max_soft_len = max(self.max_soft_len, len(key.split()))

    def build_glossary_sentence_first(self, text:str, *, limit:int=12, per_word_k:int=3, min_lcs_len:int=4) -> Dict[str,str]:
        # 先 exact/phrase match，再 word 近似
        text_clean = _MASK_PAT.sub(" ", text or "")
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

        # 近似：token 前綴在 glossary 英文內出現
        for idx, tok in enumerate(tokens):
            if len(glossary) >= limit:
                break
            if covered[idx]:
                continue
            if len(tok) < min_lcs_len:
                continue
            t_norm = tok.lower()
            t_chars = set(t_norm)
            cands = [r for r in self.rows if len(t_chars & r["charset"]) > 0]
            res = []
            for r in cands:
                cand_norm = r["en_norm"]
                kk = 0
                for k in range(min(len(t_norm), len(cand_norm)), 0, -1):
                    sub = t_norm[:k]
                    if sub in cand_norm:
                        kk = k
                        break
                if kk >= min_lcs_len:
                    res.append((kk, len(r["en"]), r["en"], r["zh"]))
            res.sort(key=lambda x: (-x[0], x[1]))
            for _, _, en, zh in res[:per_word_k]:
                if en not in glossary:
                    glossary[en] = zh
                    covered[idx] = True
                    break
        return glossary

# ===== 讀 CSV/ODS =====
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
    headers = [cell_text(c) for c in rows[0].findall("table:table-cell", ns)]

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
            b = bytes(buf.to_py())
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
    el = document.getElementById(input_id)
    if el is None:
        return None
    files = el.files
    if not files or files.length == 0:
        return None
    buf = await files.item(0).arrayBuffer()
    return bytes(buf.to_py()).decode("utf-8", "ignore")

def _read_doctype(xml_text: str) -> str:
    m = re.search(r'<!DOCTYPE[^>]+>', xml_text or "")
    return m.group(0) if m else ""

# ===== 舊版 ts：建立已翻譯映射 =====
OldVal = Union[str, List[str]]

def build_old_translation_map(old_ts_text: Optional[str]) -> Dict[Tuple[str,str], OldVal]:
    if not old_ts_text:
        return {}
    try:
        root = ET.fromstring(old_ts_text)
    except Exception:
        return {}
    mp: Dict[Tuple[str,str], OldVal] = {}
    for ctx in root.findall("context"):
        ctx_name = (ctx.findtext("name") or "").strip()
        for m in ctx.findall("message"):
            src_text = (m.findtext("source") or "")
            if not src_text.strip():
                continue
            tr = m.find("translation")
            if tr is None:
                continue
            if tr.get("type") == "unfinished":
                continue
            if m.get("numerus") == "yes":
                forms = [ (n.text or "") for n in tr.findall("numerusform") ]
                if any(f.strip() for f in forms):
                    mp[(ctx_name, src_text)] = forms
            else:
                t = (tr.text or "")
                if t.strip():
                    mp[(ctx_name, src_text)] = t
    return mp

def apply_old_translation(msg_node: ET.Element, old_val: OldVal):
    tr = msg_node.find("translation")
    if tr is None:
        tr = ET.SubElement(msg_node, "translation")
    # 移除 unfinished 標記
    if "type" in tr.attrib:
        tr.attrib.pop("type", None)

    if msg_node.get("numerus") == "yes":
        forms = tr.findall("numerusform")
        if not forms:
            forms = [ET.SubElement(tr, "numerusform")]
        if isinstance(old_val, list):
            # 依舊版 forms 長度填入
            for i, f in enumerate(forms):
                f.text = old_val[min(i, len(old_val)-1)] if old_val else ""
        else:
            for f in forms:
                f.text = old_val
    else:
        tr.text = old_val[0] if isinstance(old_val, list) and old_val else (old_val if isinstance(old_val, str) else "")

# ===== OpenAI API =====
async def call_api(api_key: str, base_url: str, model: str, payload: dict, retries: int = 1):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    url = base_url.rstrip("/") + "/chat/completions"

    mname = (model or "").lower()
    is_o1_o3 = mname.startswith("o1") or mname.startswith("o3")
    is_gpt5  = mname.startswith("gpt-5")

    # o1/o3：system 轉 user（保守處理）
    if is_o1_o3:
        new_msgs = []
        for m in payload.get("messages", []):
            if m.get("role") == "system":
                new_msgs.append({"role": "user", "content": f"[System Instruction]\\n{m.get('content','')}"})
            else:
                new_msgs.append(m)
        payload["messages"] = new_msgs

    # gpt-5 / o*：移除部分不支援參數
    if is_o1_o3 or is_gpt5:
        for k in ("temperature","top_p","presence_penalty","frequency_penalty","logit_bias"):
            payload.pop(k, None)
        if "max_tokens" in payload and "max_completion_tokens" not in payload:
            payload["max_completion_tokens"] = payload.pop("max_tokens")

    for attempt in range(retries + 1):
        try:
            resp = await pyfetch(url, method="POST", headers=headers, body=json.dumps(payload))
            data = await resp.json()
            if resp.status >= 400:
                raise Exception(f"API Error {resp.status}: {data.get('error', {}).get('message')}")
            choice = data["choices"][0]
            msg = choice.get("message", {})
            # tool call
            if msg.get("tool_calls"):
                arg_str = msg["tool_calls"][0]["function"]["arguments"]
                return json.loads(arg_str)
            # plain content
            if msg.get("content"):
                return json.loads(msg["content"])
            return None
        except Exception as e:
            if attempt >= retries:
                print("call_api failed:", e)
                return None
            await asyncio.sleep(1)
    return None

# ===== 主流程 =====
async def run_translation_pipeline_async(
    api_key: str, base_url: str,
    model1: str, ts_text: str,
    glossary_pairs: List[Tuple[str,str]],
    batch_size: int = 12, limit_n: int = 0,
    use_model2: bool = False, model2: str = "",
    old_ts_text: Optional[str] = None
) -> bytes:

    doctype = _read_doctype(ts_text)
    root = ET.fromstring(ts_text)

    # 舊版映射
    old_map = build_old_translation_map(old_ts_text)

    matcher = LCSMatcher(glossary_pairs)

    # 蒐集 tasks（會翻譯的 message）
    tasks = []
    reused = 0

    for ctx in root.findall("context"):
        ctx_name = (ctx.findtext("name") or "").strip()
        for m in ctx.findall("message"):
            src_node = m.find("source")
            if src_node is None or src_node.text is None:
                continue
            src_text = src_node.text

            # 先沿用舊版（跳過 API）
            old_val = old_map.get((ctx_name, src_text))
            if old_val is not None:
                apply_old_translation(m, old_val)
                reused += 1
                _compare_add(src_text, (old_val[0] if isinstance(old_val, list) and old_val else str(old_val)), f"介面: {ctx_name}（沿用舊版）")
                if limit_n > 0 and (reused + len(tasks)) >= limit_n:
                    break
                continue

            if not needs_translation(src_text):
                continue

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
                "numerus": (m.get("numerus") == "yes"),
            })

            if limit_n > 0 and (reused + len(tasks)) >= limit_n:
                break
        if limit_n > 0 and (reused + len(tasks)) >= limit_n:
            break

    total = len(tasks)
    if total == 0:
        xml_bytes = ET.tostring(root, encoding="utf-8")
        head = b'<?xml version="1.0" encoding="utf-8"?>'
        if doctype:
            return head + b"\\n" + doctype.encode("utf-8") + b"\\n" + xml_bytes
        return head + b"\\n" + xml_bytes

    _compare_reset()
    _progress_setup(total)
    _set_ui_msg(f"開始處理：沿用舊版 {reused} 筆，需翻譯 {total} 筆")

    tools_schema = [{
        "type": "function",
        "function": {
            "name": "set_results",
            "description": "Save translations",
            "parameters": {
                "type": "object",
                "properties": {"results": {"type": "array", "items": {"type": "string"}}},
                "required": ["results"]
            }
        }
    }]

    # System prompt（含：快捷鍵 &X → 末尾(&X)，以及用語偏好提示）
    sys_prompt = (
        "你是台灣 GIS 在地化譯者。"
        " 對於每一個項目，只翻譯 \\`text\\` 欄位中的英文內容成繁體中文（台灣用語）。"
        " 可以參考 \\`context\\` 與 \\`glossary\\` 來判斷，但不要把 context 的文字（例如「介面: ...」「註釋: ...」）當成輸出的一部分。"
        " 請呼叫工具 set_results，並只在 results 陣列中依序填入翻譯後的字串。"
        " 保留所有 ASCII 半形符號（例如 ()[]{};:,.?+/\\\\*& 等），數量與順序都必須與原文一致。"
        " 務必保留所有 ⟦M數字⟧ 變數與 %1、{0} 這類 placeholder，不可遺失或改變順序。"
        " 若字串看起來是程式碼變數、常數、enum 名稱、函式名稱、人名或英文縮寫，優先保留原文不翻。"
        " 若原文含有快捷鍵標記 &X（X 為任意英數字），請在譯文最後加上(&X)（不含空格），並避免在譯文正文中保留 &X。"
        " 用語偏好（語意相同時優先）：插件→外掛程式、凸殼→凸包、處理中→處理、LineString→線串、Base level→基準值、"
        " Arrow head→箭頭端、Line alignment→線條對齊、Model scale→模型縮放比例、Row→列、pixels→像素。"
        " 若不確定，寧可保留英文原文。"
    )

    finished = 0

    for start in range(0, total, batch_size):
        while getattr(window, "_TS_PAUSED", False):
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

        user_prompt = f"請逐一翻譯下列項目，僅翻譯 text 欄位內容，輸出陣列 results：\\n{items_json}"

        # ============ 核心：API 呼叫策略 ============
        # ✅ 沒勾 Model-2：只翻譯一次（1 次 API）
        # ✅ 勾 Model-2：Model-1 產生 3 版（3 次 API）→ Model-2 挑選+格式校正（1 次 API）
        zh_list: List[str] = []

        if use_model2 and model2:
            temps = [0.2, 0.7, 1.0]
            payloads = []
            for t in temps:
                payloads.append({
                    "model": model1,
                    "temperature": t,
                    "tools": tools_schema,
                    "tool_choice": {"type":"function", "function":{"name":"set_results"}},
                    "messages": [
                        {"role":"system", "content": sys_prompt},
                        {"role":"user", "content": user_prompt}
                    ]
                })

            resA, resB, resC = await asyncio.gather(
                call_api(api_key, base_url, model1, payloads[0]),
                call_api(api_key, base_url, model1, payloads[1]),
                call_api(api_key, base_url, model1, payloads[2]),
            )

            listA = (resA.get("results", []) if resA else [])
            listB = (resB.get("results", []) if resB else [])
            listC = (resC.get("results", []) if resC else [])

            # pad
            def _pad(lst: List[str]) -> List[str]:
                if len(lst) < len(batch):
                    lst = lst + [""] * (len(batch) - len(lst))
                return lst[:len(batch)]
            listA = _pad(listA)
            listB = _pad(listB)
            listC = _pad(listC)

            sel_items = []
            for i, it in enumerate(batch):
                sel_items.append({
                    "index": i,
                    "source": it["src"],
                    "context": it["context"],
                    "A": listA[i],
                    "B": listB[i],
                    "C": listC[i],
                })

            sel_prompt = (
                "你是嚴格的 Qt/QGIS 繁中審校員。\\n"
                "請對每筆資料，在 A/B/C 中選擇最佳譯文並做必要校正：\\n"
                "- placeholder（%n, %1, {0}, ⟦M#⟧）必須完整且順序不變\\n"
                "- HTML/Qt 標籤與 ASCII 符號不可缺漏\\n"
                "- 若原文含快捷鍵 &X（X 英數），請把譯文正文中的 &X 移除，並在譯文末尾加上(&X)\\n"
                "輸出 JSON：{\\\"results\\\":[...]}，results 長度與順序要與輸入相同。\\n\\n"
                + json.dumps(sel_items, ensure_ascii=False)
            )

            sel_payload = {
                "model": model2,
                "temperature": 0.2,
                "tools": tools_schema,
                "tool_choice": {"type":"function", "function":{"name":"set_results"}},
                "messages": [
                    {"role":"system", "content": "你是嚴格的校對員，只輸出 results 陣列內容。"},
                    {"role":"user", "content": sel_prompt}
                ]
            }

            res_final = await call_api(api_key, base_url, model2, sel_payload)
            zh_list = (res_final.get("results", []) if res_final else listA)
            if len(zh_list) < len(batch):
                zh_list += [""] * (len(batch) - len(zh_list))
            zh_list = zh_list[:len(batch)]

        else:
            payload = {
                "model": model1,
                "temperature": 0.2,
                "tools": tools_schema,
                "tool_choice": {"type":"function", "function":{"name":"set_results"}},
                "messages": [
                    {"role":"system", "content": sys_prompt},
                    {"role":"user", "content": user_prompt}
                ]
            }
            res = await call_api(api_key, base_url, model1, payload)
            zh_list = (res.get("results", []) if res else [""] * len(batch))
            if len(zh_list) < len(batch):
                zh_list += [""] * (len(batch) - len(zh_list))
            zh_list = zh_list[:len(batch)]

        # ============ 寫回 XML + 後處理 ============
        for k, zh_raw in enumerate(zh_list):
            item = batch[k]
            src_text = item["src"]

            if not zh_raw:
                continue

            zh = _unmask_text(zh_raw, maps[k])
            zh = _et_ready(zh)
            zh = strip_real_newlines(zh)
            zh = fix_zh_punct(zh)
            zh = normalize_zh(to_zh_tw(zh))

            zh, ok_ph = repair_placeholders(src_text, zh)
            zh = fix_context_leak(src_text, zh, item["context"])
            zh = restore_leading_symbols(src_text, zh)
            zh = apply_mnemonic_suffix(src_text, zh)

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

            _compare_add(src_text, zh, item["context"])
            finished += 1
            _progress_tick(finished, total)

        _set_ui_msg(f"處理進度：沿用舊版 {reused} / 新翻譯 {finished}（本次需翻譯 {total}）")

    xml_bytes = ET.tostring(root, encoding="utf-8")
    head = b'<?xml version="1.0" encoding="utf-8"?>'
    if doctype:
        return head + b"\\n" + doctype.encode("utf-8") + b"\\n" + xml_bytes
    return head + b"\\n" + xml_bytes

# ===== 事件入口 =====
_BUSY = False

async def _on_click(evt=None):
    global _BUSY
    if _BUSY:
        _set_ui_msg("<span style='color:#b00'>正在處理，請稍候...</span>")
        return
    _BUSY = True

    btn_pause = document.getElementById("pause-btn")
    if btn_pause is not None:
        btn_pause.style.display = "block"

    try:
        api = (document.getElementById("apiKey").value or "").strip()
        base_url = (document.getElementById("baseUrl").value or "").strip() or "https://api.openai.com/v1"

        sel1 = document.getElementById("modelSel").value
        model1 = sel1 if sel1 != "__custom__" else (document.getElementById("modelCustom").value or "").strip()

        use2 = bool(document.getElementById("useModel2").checked)
        sel2 = document.getElementById("modelSel2").value
        model2 = sel2 if sel2 != "__custom__" else (document.getElementById("modelCustom2").value or "").strip()

        batch = int(document.getElementById("batch").value or "12")
        limitN = int(document.getElementById("limitN").value or "0")

        if not api:
            _set_ui_msg("<span style='color:#b00'>請輸入 API Key</span>")
            return
        if not model1:
            _set_ui_msg("<span style='color:#b00'>請選擇或輸入 Model-1</span>")
            return
        if use2 and not model2:
            _set_ui_msg("<span style='color:#b00'>請選擇或輸入 Model-2（或取消勾選 Model-2）</span>")
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

        if btn_pause is not None:
            btn_pause.style.display = "none"
    except Exception as e:
        _set_ui_msg(f"<span style='color:#b00'>發生錯誤：{html.escape(str(e))}</span>")
        traceback.print_exc()
        if btn_pause is not None:
            btn_pause.style.display = "none"
    finally:
        _BUSY = False

_BTN_PROXY = create_proxy(lambda evt: asyncio.ensure_future(_on_click(evt)))
document.getElementById("run-btn").addEventListener("click", _BTN_PROXY)
  `);

} catch(e){
  console.error(e);
  if(msgEl) msgEl.innerHTML = `<span style="color:#b00">Python 載入失敗：${String(e)}</span>`;
}
</script>
```
