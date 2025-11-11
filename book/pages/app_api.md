<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>QGIS .ts 兩階段翻譯（含格式修補）</title>
  <style>
  /* —— 全部樣式只限制在 #ts-ui，並且用 --ts-* 變數，避免和主題衝突 —— */
  #ts-ui{
    --ts-gap: 12px; --ts-pad: 14px; --ts-radius: 12px; --ts-border: #e5e7eb;
    --ts-bg: #fff; --ts-muted: #6b7280; --ts-text: #111827;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans", "PingFang TC", "Microsoft JhengHei", sans-serif;
    line-height: 1.35; margin: 8px 0 16px; color: var(--ts-text);
  }
  @media (prefers-color-scheme: dark){
    #ts-ui{ --ts-border: #2b2f36; --ts-bg: #111418; --ts-muted: #9aa3af; --ts-text: #e5e7eb; }
  }
  #ts-ui *, #ts-ui *::before, #ts-ui *::after{ box-sizing: border-box; }
  #ts-ui .ts-card{ border:1px solid var(--ts-border); background:var(--ts-bg); border-radius: var(--ts-radius); padding:16px; box-shadow:0 1px 2px rgba(0,0,0,.04); }
  #ts-ui .ts-title{ font-size:1.05rem; font-weight:600; margin:2px 0 10px; }
  #ts-ui .ts-grid{ display:grid; grid-template-columns: 160px 1fr; gap:10px 14px; align-items:center; }
  #ts-ui .ts-label{ color:var(--ts-muted); font-size:.95rem; white-space:nowrap; }
  #ts-ui .ts-input input, #ts-ui .ts-input select{ width:100%; padding:8px 10px; border:1px solid var(--ts-border); border-radius:10px; background:transparent; font-size:.95rem; }
  #ts-ui .ts-input select{ appearance:none; -webkit-appearance:none; -moz-appearance:none; }
  #ts-ui .ts-input input[type="file"]{ padding:6px; }
  #ts-ui .ts-inline{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
  #ts-ui .ts-hint{ color:var(--ts-muted); font-size:.9rem; }
  #ts-ui .ts-toolbar{ margin-top:10px; display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
  #ts-ui .ts-btn-primary{ appearance:none; border:1px solid var(--ts-border); background:#111827; color:#fff; border-radius:10px; padding:8px 14px; font-weight:600; cursor:pointer; }
  @media (prefers-color-scheme: dark){ #ts-ui .ts-btn-primary{ background:#e5e7eb; color:#111418; } }
  #ts-ui .ts-btn-primary:hover{ filter:brightness(0.95); }
  #ts-ui .ts-divider{ height:1px; background:var(--ts-border); margin:12px 0; border:0; }

  /* 附屬區塊（ID 不變，但樣式仍只在 #ts-ui 作用） */
  #ts-ui #ts-progress-wrap{ margin:12px 0; }
  #ts-ui #compare-box{ border:1px solid var(--ts-border); border-radius:12px; padding:8px 12px; margin-top:8px; background:var(--ts-bg); }
  #ts-ui #compare-box table{ width:100%; border-collapse:collapse; font-size:.95rem; }
  #ts-ui #compare-box th, #ts-ui #compare-box td{ padding:6px 6px; border-bottom:1px solid var(--ts-border); text-align:left; }
  #ts-ui #compare-box thead th{ font-weight:600; }
  #ts-ui #ts-ui-msg{ color:var(--ts-muted); font-size:.95rem; margin-top:8px; }

  /* 手機版：單欄 */
  @media (max-width: 640px){
    #ts-ui .ts-grid{ grid-template-columns: 1fr; }
    #ts-ui .ts-label{ margin-top:6px; }
  }

  #ts-ui .ts-row-2{ display: grid; grid-template-columns: var(--ts-col1, 1fr) var(--ts-col2, 1fr); gap: 10px 14px; align-items: center; }
  #ts-ui .ts-6-4{ --ts-col1: 6fr; --ts-col2: 4fr; }
  #ts-ui .ts-4-6{ --ts-col1: 4fr; --ts-col2: 6fr; }
  #ts-ui .ts-row-3{ display: grid; grid-template-columns: var(--ts-col1, 1fr) var(--ts-col2, 1fr) var(--ts-col3, 1fr); gap: 10px 14px; align-items: center; }
  #ts-ui .ts-3-4-3{ --ts-col1: 3fr; --ts-col2: 4fr; --ts-col3: 3fr; }
  #ts-ui .ts-field{ display: flex; flex-direction: column; gap: 6px; }
  #ts-ui .ts-field .ts-label{ margin: 0; }
  #ts-ui .left-col{ grid-column: 1 / 3; }
  @media (max-width: 640px){ #ts-ui .ts-row-2, #ts-ui .ts-row-3{ grid-template-columns: 1fr; } }

  /* 深色主題 tokens */
  @media (prefers-color-scheme: dark){
    #ts-ui{ --ts-bg: #0f1115; --ts-surface: #111418; --ts-surface-2: #0b0f14; --ts-input-bg: #0b0f14; --ts-border: #2b2f36; --ts-text: #e7eaf0; --ts-muted: #a6afbd; --ts-link: #8ab4ff; --ts-code-bg: #0b0f14; --ts-code-fg: #e7eaf0; --ts-accent: #3b82f6; --ts-on-accent: #0b0f14; --ts-focus: 0 0 0 2px rgba(59,130,246,.35); --ts-progress-bg: #1a1f29; --ts-table-head-bg: #121621; }
  }
  html[data-theme="dark"] #ts-ui{
    --ts-bg: #0f1115; --ts-surface: #111418; --ts-surface-2: #0b0f14; --ts-input-bg: #0b0f14; --ts-border: #2b2f36; --ts-text: #e7eaf0; --ts-muted: #a6afbd; --ts-link: #8ab4ff; --ts-code-bg: #0b0f14; --ts-code-fg: #e7eaf0; --ts-accent: #3b82f6; --ts-on-accent: #0b0f14; --ts-focus: 0 0 0 2px rgba(59,130,246,.35); --ts-progress-bg: #1a1f29; --ts-table-head-bg: #121621;
  }
  #ts-ui .ts-card{ background: var(--ts-surface); border-color: var(--ts-border); color: var(--ts-text); }
  #ts-ui .ts-label, #ts-ui .ts-hint{ color: var(--ts-muted); }
  #ts-ui .ts-input input, #ts-ui .ts-input select{ background: var(--ts-input-bg); color: var(--ts-text); border-color: var(--ts-border); }
  #ts-ui .ts-input input:focus, #ts-ui .ts-input select:focus{ outline: none; box-shadow: var(--ts-focus); border-color: color-mix(in oklab, var(--ts-accent) 60%, var(--ts-border)); }
  #ts-ui .ts-btn-primary{ background: var(--ts-accent); color: var(--ts-on-accent); border: 1px solid var(--ts-border); }
  #ts-ui .ts-btn-primary:hover{ filter: brightness(1.06); } #ts-ui .ts-btn-primary:focus{ outline: none; box-shadow: var(--ts-focus); }
  #ts-ui #compare-box{ background: var(--ts-surface); border-color: var(--ts-border); }
  #ts-ui #compare-box thead th{ background: var(--ts-table-head-bg); color: var(--ts-text); }
  #ts-ui #compare-box td, #ts-ui #compare-box th{ border-bottom: 1px solid var(--ts-border); }
  #ts-ui progress{ width:100%; height: 14px; background: var(--ts-progress-bg); border-radius: 8px; overflow: hidden; }
  #ts-ui progress::-webkit-progress-bar{ background: var(--ts-progress-bg); }
  #ts-ui progress::-webkit-progress-value{ background: var(--ts-accent); }
  #ts-ui progress::-moz-progress-bar{ background: var(--ts-accent); }
  #ts-ui code{ background: var(--ts-code-bg); color: var(--ts-code-fg); padding: .1em .35em; border-radius: .35em; border: 1px solid var(--ts-border); }
  #ts-ui a{ color: var(--ts-link); text-underline-offset: 2px; }
  #ts-ui ::selection{ background: color-mix(in oklab, var(--ts-accent) 35%, transparent); }
  </style>
</head>
<body>
  <div id="ts-ui">
    <!-- Stage 1: API 設定 -->
    <div class="ts-card">
      <div class="ts-title">第一階段：API 設定（翻譯）</div>
      <div class="ts-field" style="margin-bottom:10px;">
        <label class="ts-label" for="apiKey">API Key</label>
        <div class="ts-input"><input type="password" id="apiKey" placeholder="sk-..." autocomplete="off"></div>
      </div>
      <div class="ts-row-2 ts-6-4" style="margin-top:10px;">
        <div class="ts-field">
          <label class="ts-label" for="baseUrl">Base URL</label>
          <div class="ts-input"><input type="text" id="baseUrl" value="https://api.openai.com/v1"></div>
        </div>
        <div class="ts-field">
          <label class="ts-label" for="modelSel">Model</label>
          <div class="ts-input">
            <div class="ts-inline" style="width:100%;">
              <select id="modelSel" style="flex:1;min-width:220px;">
                <optgroup label="GPT-5"><option value="gpt-5">gpt-5</option><option value="gpt-5-mini">gpt-5-mini</option><option value="gpt-5-nano">gpt-5-nano</option></optgroup>
                <optgroup label="GPT-4.1"><option value="gpt-4.1">gpt-4.1</option><option value="gpt-4.1-mini" selected>gpt-4.1-mini</option><option value="gpt-4.1-nano">gpt-4.1-nano</option></optgroup>
                <optgroup label="GPT-4o"><option value="gpt-4o">gpt-4o</option><option value="gpt-4o-mini">gpt-4o-mini</option></optgroup>
                <optgroup label="Reasoning"><option value="o4-mini">o4-mini</option><option value="o3-mini">o3-mini</option></optgroup>
                <optgroup label="Legacy"><option value="gpt-4-turbo">gpt-4-turbo</option><option value="gpt-3.5-turbo">gpt-3.5-turbo</option></optgroup>
                <optgroup label="自訂"><option value="__custom__">其他</option></optgroup>
              </select>
              <input id="modelCustom" type="text" placeholder="例如：my-org/gpt-xy-2025-10-15" style="display:none;flex:1;">
            </div>
          </div>
        </div>
      </div>

      <hr class="ts-divider">
      <div class="ts-title">第二階段：API 設定（格式修補 / 後編輯）</div>
      <div class="ts-grid" style="margin-bottom:6px;">
        <label class="ts-label" for="stage2Enabled">啟用第二階段</label>
        <div class="ts-input"><input type="checkbox" id="stage2Enabled" checked></div>
      </div>
      <div class="ts-field" style="margin-bottom:10px;">
        <label class="ts-label" for="apiKey2">API Key（第二階段）</label>
        <div class="ts-input"><input type="password" id="apiKey2" placeholder="若空白則沿用第一階段" autocomplete="off"></div>
      </div>
      <div class="ts-row-2 ts-6-4">
        <div class="ts-field">
          <label class="ts-label" for="baseUrl2">Base URL（第二階段）</label>
          <div class="ts-input"><input type="text" id="baseUrl2" placeholder="留空沿用第一階段"></div>
        </div>
        <div class="ts-field">
          <label class="ts-label" for="modelSel2">Model（第二階段）</label>
          <div class="ts-input">
            <div class="ts-inline" style="width:100%;">
              <select id="modelSel2" style="flex:1;min-width:220px;">
                <optgroup label="GPT-5"><option value="gpt-5">gpt-5</option><option value="gpt-5-mini">gpt-5-mini</option><option value="gpt-5-nano">gpt-5-nano</option></optgroup>
                <optgroup label="GPT-4.1"><option value="gpt-4.1">gpt-4.1</option><option value="gpt-4.1-mini">gpt-4.1-mini</option><option value="gpt-4.1-nano">gpt-4.1-nano</option></optgroup>
                <optgroup label="GPT-4o"><option value="gpt-4o">gpt-4o</option><option value="gpt-4o-mini">gpt-4o-mini</option></optgroup>
                <optgroup label="Reasoning"><option value="o4-mini">o4-mini</option><option value="o3-mini">o3-mini</option></optgroup>
                <optgroup label="Legacy"><option value="gpt-4-turbo">gpt-4-turbo</option><option value="gpt-3.5-turbo">gpt-3.5-turbo</option></optgroup>
                <optgroup label="自訂"><option value="__custom2__">其他</option></optgroup>
              </select>
              <input id="modelCustom2" type="text" placeholder="例如：my-org/gpt-xy-2025-10-15" style="display:none;flex:1;">
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="ts-card" style="margin-top:12px;">
      <div class="ts-title">處理參數</div>
      <div class="ts-row-3 ts-3-4-3">
        <div class="ts-field">
          <label class="ts-label" for="batch">Batch</label>
          <div class="ts-input"><input type="number" id="batch" value="32" min="1" max="64"></div>
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
          <div class="ts-input"><input type="file" id="tsFile" accept=".ts"></div>
        </div>
      </div>

      <hr class="ts-divider">
      <div class="ts-title">輸入檔案</div>
      <div class="ts-row-2" style="--ts-col1: 7fr; --ts-col2: 3fr;">
        <div class="ts-field">
          <label class="ts-label" for="glsFile">glossary（CSV / ODS）</label>
          <div class="ts-input"><input type="file" id="glsFile" accept=".csv,.ods" multiple></div>
        </div>
        <div class="ts-field">
          <label class="ts-label" style="visibility:hidden;">執行翻譯</label>
          <div class="ts-input"><button id="run-btn" class="ts-btn-primary" style="width:100%;">執行翻譯</button></div>
        </div>
        <div class="ts-hint left-col" style="margin-top:6px;">欄位：<code>en, zh</code> 或 <code>英文名稱, 中文名稱</code></div>
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
            <thead><tr><th style="width:50%;">原文</th><th style="width:50%;">譯文</th></tr></thead>
            <tbody id="compare-tbody"></tbody>
          </table>
        </div>
      </div>

      <div id="ts-ui-msg"></div>
    </div>
  </div>

  <!-- Pyodide + pipeline -->
  <script type="module">
  import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.mjs";

  // --- small DOM helpers ---
  const $ = (id) => document.getElementById(id);

  // --- counters from .ts file ---
  (function setupTsCounter(){
    const tsFile = $('tsFile');
    const limitN = $('limitN');
    const countInfo = $('countInfo');
    countInfo.textContent = ' / 0';

    function needsTranslationJS(text){
      if (!text) return false;
      const t = String(text).trim();
      if (!t) return false;
      if (/^[\s\d\W%{}]+$/u.test(t)) return false; // 只有符號/數字/空白 -> 跳過
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
          limitN.max = String(total);
          if (Number(limitN.value) <= 0) limitN.value = total;
          countInfo.textContent = ' / ' + total;
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
      if (max){ if (v > max) v = max; if (v < 0) v = 0; limitN.value = v; }
      else if (v < 0){ limitN.value = 0; }
    }
    tsFile.addEventListener('change', handleTsChange);
    limitN.addEventListener('input', clampLimit);
  })();

  // --- show "custom" model input boxes ---
  (function setupModelCustom(){
    const sel1 = $('modelSel'); const custom1 = $('modelCustom');
    const sel2 = $('modelSel2'); const custom2 = $('modelCustom2');
    function sync1(){ custom1.style.display = (sel1.value === '__custom__') ? 'block' : 'none'; }
    function sync2(){ custom2.style.display = (sel2.value === '__custom2__') ? 'block' : 'none'; }
    sel1.addEventListener('change', sync1); sel2.addEventListener('change', sync2);
    sync1(); sync2();
  })();

  const pyodide = await loadPyodide();
  await pyodide.loadPackage('micropip');
  const $msg = $('ts-ui-msg');

  try{
    await pyodide.runPythonAsync(`
import asyncio, json, re, io, base64, traceback, html, csv, zipfile
from typing import List, Tuple, Dict, Optional
from xml.etree import ElementTree as ET
from js import document
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy

# ---- OpenCC (s2twp) for TW terms ----
try:
    from opencc import OpenCC
except ModuleNotFoundError:
    import micropip
    await micropip.install('opencc-python-reimplemented==0.1.7')
    from opencc import OpenCC
_OPENCC = OpenCC('s2twp')
_TW_PROTECT_TERMS = ['演算法']

# ---- zh normalization ----
def to_zh_tw(s: Optional[str]) -> str:
    if not s: return ''
    text = s
    placeholders = {}
    for i, term in enumerate(_TW_PROTECT_TERMS):
        key = f'⟦TWTERM{i}⟧'
        placeholders[key] = term
        text = text.replace(term, key)
    try:
        text = _OPENCC.convert(text)
    except Exception:
        pass
    for k,v in placeholders.items():
        text = text.replace(k, v)
    return text

_COORD_RE = re.compile(r'坐標')
def normalize_zh(s: Optional[str]) -> str:
    if not s: return ''
    try:
        return _COORD_RE.sub('座標', s)
    except Exception:
        return s

# ---- UI helpers ----
def _set_ui_msg(msg_html: str):
    document.getElementById('ts-ui-msg').innerHTML = msg_html

def _progress_setup(total:int):
    wrap = document.getElementById('ts-progress-wrap')
    bar = document.getElementById('ts-progress')
    lab = document.getElementById('ts-progress-label')
    wrap.style.display = 'block'
    bar.value = 0
    bar.max = max(1, total)
    lab.innerText = f'0 / {total}'

def _progress_tick(done:int, total:int):
    bar = document.getElementById('ts-progress')
    lab = document.getElementById('ts-progress-label')
    bar.value = done
    lab.innerText = f'{done} / {total}'

def _compare_reset():
    box = document.getElementById('compare-box')
    box.style.display = 'block'
    tbody = document.getElementById('compare-tbody')
    while tbody.firstChild:
        tbody.removeChild(tbody.firstChild)

def _compare_add(src_text:str, zh_text:str):
    box = document.getElementById('compare-box')
    box.style.display = 'block'
    tbody = document.getElementById('compare-tbody')
    tr = document.createElement('tr')
    def _td(txt):
        td = document.createElement('td')
        td.style.padding = '4px'
        td.style.borderBottom = '1px solid #eee'
        td.textContent = txt
        return td
    tr.appendChild(_td(src_text or ''))
    tr.appendChild(_td(zh_text or ''))
    tbody.appendChild(tr)
    try:
        scroller = box.children.item(1)
        if scroller:
            scroller.scrollTop = scroller.scrollHeight
    except Exception:
        pass

# ---- file helpers ----
async def read_glossaries_from_file_input(input_id: str) -> List[Tuple[str,str]]:
    files = document.getElementById(input_id).files
    if not files or files.length == 0:
        return []
    pairs_all: List[Tuple[str,str]] = []
    for i in range(files.length):
        f = files.item(i)
        name = (f.name or '').lower()
        try:
            buf = await f.arrayBuffer()
            raw = buf.to_py()
            b = raw if isinstance(raw, (bytes, bytearray)) else bytes(raw)
            if name.endswith('.ods'):
                pairs_all.extend(load_glossary_ods_bytes(b))
            elif name.endswith('.csv'):
                txt = b.decode('utf-8', 'ignore')
                pairs_all.extend(load_glossary_csv_text(txt))
        except Exception as e:
            print(f'[glossary] 讀取 {f.name} 失敗：{e}')
    seen, dedup = set(), []
    for en, zh in pairs_all:
        if en not in seen:
            dedup.append((en, zh))
            seen.add(en)
    return dedup

async def _read_file_text(input_id: str) -> Optional[str]:
    files = document.getElementById(input_id).files
    if not files or files.length==0: return None
    buf = await files.item(0).arrayBuffer()
    return bytes(buf.to_py()).decode('utf-8', 'ignore')

# ---- data: URL builder ----
def _build_download_link(filename: str, content_bytes: bytes) -> str:
    b64 = base64.b64encode(content_bytes).decode('utf-8')
    return f'<a download="{filename}" href="data:application/octet-stream;base64,{b64}">⬇️ 下載 {filename}</a>'

# ---- XML helpers ----
_DOCTYPE_RE = re.compile(r'<!DOCTYPE[^>]+>')

def _read_doctype(xml_text: str) -> str:
    m = _DOCTYPE_RE.search(xml_text)
    return m.group(0) if m else ''

_MASK_PAT = re.compile(r'(</?[A-Za-z][^>]*>|&lt;/?[A-Za-z][^&]*?&gt;|%L\\d+|%\\d+|%n|\\{\\d+\\}|&(?:[A-Za-z]+|#\\d+|#x[0-9A-Fa-f]+);)', re.IGNORECASE)

def _mask_text(s:str):
    idx=0; mapping={}
    def _repl(m):
        nonlocal idx
        k=f'⟦MASK{idx}⟧'; mapping[k]=m.group(0); idx+=1; return k
    return _MASK_PAT.sub(_repl, s), mapping

def _unmask_text(s:str, mapping:Dict[str,str])->str:
    for k,v in mapping.items():
        s = s.replace(k,v)
    return s

def _et_ready(s:str)->str:
    try:
        return html.unescape(s)
    except Exception:
        return s

def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip(): return False
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text): return False
    return True

# ---- soft glossary matching (LCS-ish) ----
import csv as _csv
_SEP_RE = re.compile(r'[-\\s/_.\\\\]+')
_TOKEN_RE = re.compile(r'[A-Za-z0-9]+(?:[\\\\/_.-][A-Za-z0-9]+)*')

def soft_norm(s:str)->str:
    return _SEP_RE.sub(' ', s.lower()).strip()

class LCSMatcher:
    def __init__(self, pairs: List[Tuple[str,str]], min_token_len:int=4, min_lcs_len:int=4):
        rows = []
        for en, zh in pairs:
            en = (en or '').strip(); zh = (zh or '').strip()
            if en and zh:
                en_norm = en.lower()
                charset = set(re.sub(r'\\s+', '', en_norm))
                rows.append({'en':en, 'zh':zh, 'en_norm':en_norm, 'charset':charset})
        self.rows = rows
        self.min_token_len = min_token_len
        self.min_lcs_len = min_lcs_len
        self.soft_index = {}
        self.max_soft_len = 1
        for r in rows:
            key = soft_norm(r['en'])
            if key and key not in self.soft_index:
                self.soft_index[key] = (r['en'], r['zh'])
                self.max_soft_len = max(self.max_soft_len, len(key.split()))

    def _topk_for_word(self, token:str, k:int=3)->List[Dict]:
        t_norm = token.lower()
        if len(t_norm) < self.min_token_len: return []
        t_chars = set(t_norm)
        cand = [r for r in self.rows if len(t_chars & r['charset'])>0]
        res=[]
        def anchored_prefix_sub_in(token_norm:str, cand_norm:str):
            if not token_norm or not cand_norm: return 0,''
            max_k = min(len(token_norm), len(cand_norm))
            for kk in range(max_k,0,-1):
                sub = token_norm[:kk]
                if sub in cand_norm: return kk, sub
            return 0,''
        for r in cand:
            kk, sub = anchored_prefix_sub_in(t_norm, r['en_norm'])
            if kk >= self.min_lcs_len:
                res.append({'token':token,'en':r['en'],'zh':r['zh'],'lcs_len':kk})
        res.sort(key=lambda d: (-d['lcs_len'], len(d['en'])))
        return res[:k]

    def build_glossary_sentence_first(self, text:str, *, limit:int=12, per_word_k:int=3, min_lcs_len:int=4)->Dict[str,str]:
        text_clean = _MASK_PAT.sub(' ', text)
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
                phrase=' '.join(toks_lc[i:i+w]); key=soft_norm(phrase)
                if key in self.soft_index:
                    en, zh = self.soft_index[key]
                    if en not in glossary:
                        glossary[en]=zh; _mark(i,i+w)
                if len(glossary)>=limit: break
        for idx, tok in enumerate(tokens):
            if len(glossary)>=limit: break
            if covered[idx]: continue
            if len(tok) < min_lcs_len: continue
            for r in self._topk_for_word(tok, k=per_word_k):
                if r['lcs_len']>=min_lcs_len and r['en'] not in glossary:
                    glossary[r['en']] = r['zh']; covered[idx]=True
                if len(glossary)>=limit: break
        return glossary

# ---- glossary loaders ----
def load_glossary_csv_text(csv_text: Optional[str]) -> List[Tuple[str,str]]:
    if not csv_text: return []
    rdr = _csv.DictReader(io.StringIO(csv_text))
    if not rdr.fieldnames: return []
    col_en = col_zh = None
    for c in rdr.fieldnames or []:
        cc = (c or '').strip()
        if cc in ('en', '英文名稱'): col_en = c
        if cc in ('zh', '中文名稱'): col_zh = c
    if not col_en or not col_zh: return []
    pairs, seen = [], set()
    for row in rdr:
        en = (row.get(col_en) or '').strip()
        zh = (row.get(col_zh) or '').strip()
        if en and zh and en not in seen:
            zh = normalize_zh(to_zh_tw(zh))
            pairs.append((en, zh))
            seen.add(en)
    return pairs

def load_glossary_ods_bytes(ods_bytes: bytes)->List[Tuple[str,str]]:
    with zipfile.ZipFile(io.BytesIO(ods_bytes)) as z:
        xml = z.read('content.xml')
        ns = {
            'office':'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
            'table':'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
            'text':'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        }
        root = ET.fromstring(xml)
        table = root.find('.//table:table', ns)
        if table is None: return []
        rows = table.findall('table:table-row', ns)
        def cell_text(cell):
            parts=[]
            for p in cell.findall('.//text:p', ns):
                parts.append(''.join(p.itertext()))
            return (parts[0] if parts else '').strip()
        if not rows: return []
        header_cells = rows[0].findall('table:table-cell', ns)
        headers = [cell_text(c) for c in header_cells]
        def _find_idx(names:set):
            for i,h in enumerate(headers):
                if (h or '').strip().lower() in names: return i
            return -1
        idx_en = _find_idx({'英文名稱','en'})
        idx_zh = _find_idx({'中文名稱','zh'})
        if idx_en<0 or idx_zh<0: return []
        pairs=[]; seen=set()
        for r in rows[1:]:
            cells = r.findall('table:table-cell', ns)
            if idx_en>=len(cells) or idx_zh>=len(cells): continue
            en = cell_text(cells[idx_en]).strip()
            zh = cell_text(cells[idx_zh]).strip()
            if en and zh and en not in seen:
                zh = normalize_zh(to_zh_tw(zh))
                pairs.append((en, zh)); seen.add(en)
        return pairs

# ---- OpenAI-compatible calls ----
def _mk_items_stage1(masked_texts:List[str], glossaries:List[Dict[str,str]]):
    return [
        {
            'id': i,
            'text': t,
            'glossary': [f"{en} -> {zh}" for en, zh in g.items()],
        } for i,(t,g) in enumerate(zip(masked_texts, glossaries))
    ]

async def _post_json(base_url:str, path:str, body:dict, api_key:str):
    resp = await pyfetch(base_url.rstrip('/') + path, method='POST', headers={'Authorization': f'Bearer {api_key}', 'Content-Type':'application/json'}, body=json.dumps(body))
    data = await resp.json()
    return resp.status, data

async def _try_family(endpoints:List[str], build_body, base_url:str, api_key:str):
    tried = []
    for ep in endpoints:
        body = build_body(ep)
        status, data = await _post_json(base_url, ep, body, api_key)
        tried.append((ep, status, data))
        if status < 400:
            return status, data
        # lite compatibility tweaks
        if status == 400:
            msg = (data.get('error',{}) or {}).get('message','')
            if ep == '/responses':
                # key shuffle
                if 'max_output_tokens' in msg and 'Unsupported' in msg:
                    body = build_body(ep, force_tokens_key='max_completion_tokens')
                    status2, data2 = await _post_json(base_url, ep, body, api_key)
                    tried.append((ep+'*', status2, data2))
                    if status2 < 400:
                        return status2, data2
                if 'reasoning' in msg.lower():
                    body = build_body(ep, drop_reasoning=True)
                    status2, data2 = await _post_json(base_url, ep, body, api_key)
                    tried.append((ep+'*', status2, data2))
                    if status2 < 400:
                        return status2, data2
            if ep == '/chat/completions':
                if 'max_tokens' in msg and 'Unsupported' in msg:
                    body = build_body(ep, swap_chat_tokens=True)
                    status2, data2 = await _post_json(base_url, ep, body, api_key)
                    tried.append((ep+'*', status2, data2))
                    if status2 < 400:
                        return status2, data2
                if 'not compatible with the chat.completions' in msg.lower():
                    # try responses
                    continue
    raise RuntimeError('API Error', tried)

# ---- Stage 1: translation ----
async def call_stage1(api_key:str, base_url:str, model:str, masked_texts:List[str], glossaries:List[Dict[str,str]]):
    items = _mk_items_stage1(masked_texts, glossaries)
    system_prompt = (
        '你是台灣 GIS 在地化譯者，將多個獨立英文片段翻為自然專業的繁體中文（台灣）。\\n'
        '規則：\\n'
        '• 保留所有 ⟦MASK數字⟧；\\n'
        '• 不要解釋；\\n'
        '• 不要改動任何 HTML 標籤或 HTML 實體；\\n'
        '• 只輸出與輸入等長、同序的結果。'
    )
    user_prompt = '請逐一翻譯 items。只需回傳 function 參數，不要輸出其他文字。\\n' + 'items = ' + json.dumps(items, ensure_ascii=False)

    def build_body(path:str, force_tokens_key:str=None, drop_reasoning:bool=False, swap_chat_tokens:bool=False):
        m = (model or '').lower()
        new_family = m.startswith(('gpt-5','gpt-4.1','o4','o3'))
        tokens = min(4000, 220 * max(4, len(masked_texts)))
        chat_tokens_key = 'max_completion_tokens'
        if not new_family: chat_tokens_key = 'max_tokens'
        if force_tokens_key: chat_tokens_key = force_tokens_key
        if path == '/chat/completions':
            body = {
                'model': model,
                'messages': [
                    {'role':'system','content': system_prompt},
                    {'role':'user','content': user_prompt}
                ],
                'tools': [{
                    'type':'function',
                    'function':{
                        'name':'return_translations',
                        'description':'回傳與輸入 items 等長、同序的繁中翻譯陣列',
                        'parameters':{
                            'type':'object',
                            'properties':{'translations':{'type':'array','items':{'type':'string'}}},
                            'required':['translations'],
                            'additionalProperties': False
                        }
                    }
                }],
                'tool_choice':{'type':'function','function':{'name':'return_translations'}},
            }
            body[chat_tokens_key] = tokens
            return body
        else: # '/responses'
            body = {
                'model': model,
                'input': [
                    {'role':'system','content':[{'type':'input_text','text': system_prompt}]},
                    {'role':'user','content':[{'type':'input_text','text': user_prompt}]}
                ],
                'tools':[{
                    'type':'function',
                    'function':{
                        'name':'return_translations',
                        'description':'回傳與輸入 items 等長、同序的繁中翻譯陣列',
                        'parameters':{
                            'type':'object',
                            'properties':{'translations':{'type':'array','items':{'type':'string'}}},
                            'required':['translations'],
                            'additionalProperties': False
                        }
                    }
                }],
            }
            if not drop_reasoning and m.startswith(('gpt-5','o4','o3')):
                body['reasoning'] = {'effort':'medium'}
            body['max_output_tokens'] = tokens
            if force_tokens_key == 'max_completion_tokens':
                body.pop('max_output_tokens', None)
                body['max_completion_tokens'] = tokens
            return body

    # prefer responses for new family, else chat
    m = (model or '').lower()
    endpoints = ['/responses','/chat/completions'] if m.startswith(('gpt-5','gpt-4.1','o4','o3')) else ['/chat/completions','/responses']
    status, data = await _try_family(endpoints, build_body, base_url, api_key)

    def _extract_tool_args_from_chat(obj:dict)->Optional[str]:
        try:
            msg = obj['choices'][0]['message']
            tcalls = msg.get('tool_calls') or []
            if not tcalls: return None
            return tcalls[0]['function']['arguments']
        except Exception:
            return None

    def _deep_find_arguments(o):
        if isinstance(o, dict):
            if 'arguments' in o and isinstance(o['arguments'], str): return o['arguments']
            for v in o.values():
                r = _deep_find_arguments(v)
                if r is not None: return r
        elif isinstance(o, list):
            for v in o:
                r = _deep_find_arguments(v)
                if r is not None: return r
        return None

    args_raw = _extract_tool_args_from_chat(data)
    if args_raw is None and 'output' in data:
        args_raw = _deep_find_arguments(data['output'])
    if args_raw is None and 'response' in data:
        args_raw = _deep_find_arguments(data['response'])
    if not args_raw:
        raise ValueError('模型未呼叫 function（找不到結構化輸出）。')
    parsed = json.loads(args_raw)
    arr = parsed.get('translations')
    if not (isinstance(arr, list) and all(isinstance(x, str) for x in arr)):
        raise ValueError('function 參數不符合 {translations: string[]} 格式')
    return arr

# ---- Stage 2: post-edit/format-fix ----
async def call_stage2(api_key:str, base_url:str, model:str, masked_src:List[str], masked_zh:List[str]):
    items = [
        {
            'id': i,
            'src': s,
            'zh': z,
        } for i,(s,z) in enumerate(zip(masked_src, masked_zh))
    ]
    system_prompt = (
        '你是嚴格的「格式修補器」。\\n'
        '任務：在保持中文意思不變的前提下，讓中文譯文的「格式」與 src 完全等價。\\n'
        '要求：\\n'
        '• 絕對保留所有 ⟦MASK數字⟧ 與所有 placeholder：%n、%1、%L1、{0} 等（字面不變）。\\n'
        '• 括號/大括號/冒號/分號/引號/斜線/逗號/點號等標點與半形全形，需與 src 對齊；例如：作者：｛０｝ → 作者: {0}。\\n'
        '• HTML 標籤與 HTML 實體必須原樣保留。\\n'
        '• 不要新增或刪除任何額外字元，只修改不匹配的標點與空白。\\n'
        '• 僅輸出與 items 等長、同序的結果。'
    )
    user_prompt = '請逐一修補 items.zh 以對齊 items.src 的格式。只需回傳 function 參數。\\n' + 'items = ' + json.dumps(items, ensure_ascii=False)

    def build_body(path:str, force_tokens_key:str=None, drop_reasoning:bool=False, swap_chat_tokens:bool=False):
        m = (model or '').lower()
        new_family = m.startswith(('gpt-5','gpt-4.1','o4','o3'))
        tokens = min(4000, 220 * max(4, len(masked_src)))
        chat_tokens_key = 'max_completion_tokens' if new_family else 'max_tokens'
        if force_tokens_key: chat_tokens_key = force_tokens_key
        if path == '/chat/completions':
            body = {
                'model': model,
                'messages': [
                    {'role':'system','content': system_prompt},
                    {'role':'user','content': user_prompt}
                ],
                'tools': [{
                    'type':'function',
                    'function':{
                        'name':'return_post_edits',
                        'description':'回傳與輸入 items 等長、同序的格式修補後中文陣列',
                        'parameters':{
                            'type':'object',
                            'properties':{'edits':{'type':'array','items':{'type':'string'}}},
                            'required':['edits'],
                            'additionalProperties': False
                        }
                    }
                }],
                'tool_choice':{'type':'function','function':{'name':'return_post_edits'}},
            }
            body[chat_tokens_key] = tokens
            return body
        else:
            body = {
                'model': model,
                'input': [
                    {'role':'system','content':[{'type':'input_text','text': system_prompt}]},
                    {'role':'user','content':[{'type':'input_text','text': user_prompt}]}
                ],
                'tools':[{
                    'type':'function',
                    'function':{
                        'name':'return_post_edits',
                        'description':'回傳與輸入 items 等長、同序的格式修補後中文陣列',
                        'parameters':{
                            'type':'object',
                            'properties':{'edits':{'type':'array','items':{'type':'string'}}},
                            'required':['edits'],
                            'additionalProperties': False
                        }
                    }
                }],
            }
            if not drop_reasoning and m.startswith(('gpt-5','o4','o3')):
                body['reasoning'] = {'effort':'medium'}
            body['max_output_tokens'] = tokens
            if force_tokens_key == 'max_completion_tokens':
                body.pop('max_output_tokens', None)
                body['max_completion_tokens'] = tokens
            return body

    m = (model or '').lower()
    endpoints = ['/responses','/chat/completions'] if m.startswith(('gpt-5','gpt-4.1','o4','o3')) else ['/chat/completions','/responses']
    status, data = await _try_family(endpoints, build_body, base_url, api_key)

    def _extract_tool_args_from_chat(obj:dict)->Optional[str]:
        try:
            msg = obj['choices'][0]['message']
            tcalls = msg.get('tool_calls') or []
            if not tcalls: return None
            return tcalls[0]['function']['arguments']
        except Exception:
            return None

    def _deep_find_arguments(o):
        if isinstance(o, dict):
            if 'arguments' in o and isinstance(o['arguments'], str): return o['arguments']
            for v in o.values():
                r = _deep_find_arguments(v)
                if r is not None: return r
        elif isinstance(o, list):
            for v in o:
                r = _deep_find_arguments(v)
                if r is not None: return r
        return None

    args_raw = _extract_tool_args_from_chat(data)
    if args_raw is None and 'output' in data:
        args_raw = _deep_find_arguments(data['output'])
    if args_raw is None and 'response' in data:
        args_raw = _deep_find_arguments(data['response'])
    if not args_raw:
        raise ValueError('模型未呼叫 function（找不到結構化輸出）。')
    parsed = json.loads(args_raw)
    arr = parsed.get('edits')
    if not (isinstance(arr, list) and all(isinstance(x, str) for x in arr)):
        raise ValueError('function 參數不符合 {edits: string[]} 格式')
    return arr

# ---- main pipeline ----
async def run_translation_pipeline_async(api_key:str, base_url:str, model:str, *,
                                         api_key2:str=None, base_url2:str=None, model2:str=None, stage2_enabled:bool=True,
                                         ts_text:str, glossary_pairs:List[Tuple[str,str]], batch_size:int=32, limit_n:int=0) -> bytes:
    doctype = _read_doctype(ts_text)
    root = ET.fromstring(ts_text)
    messages = root.findall('.//message')
    matcher = LCSMatcher(glossary_pairs, min_token_len=4, min_lcs_len=4)

    tasks=[]
    for m in messages:
        src=m.find('source')
        if src is None or src.text is None: continue
        if needs_translation(src.text):
            tasks.append((m, src.text, m.get('numerus')=='yes'))
        if limit_n > 0 and len(tasks) >= limit_n: break

    finished=0; total=len(tasks)
    if total==0:
        return ET.tostring(root, encoding='utf-8')

    _compare_reset(); _progress_setup(total)

    for start in range(0, total, batch_size):
        batch = tasks[start:start+batch_size]
        glossaries=[]; masked_texts=[]; maps=[]
        for _, src_text, _ in batch:
            g = matcher.build_glossary_sentence_first(src_text, limit=12, per_word_k=3, min_lcs_len=4)
            glossaries.append(g)
            masked, mp = _mask_text(src_text)
            masked_texts.append(masked); maps.append(mp)

        # Stage 1
        try:
            zh_list = await call_stage1(api_key, base_url, model, masked_texts, glossaries)
        except Exception:
            # fallback one-by-one
            zh_list=[]
            for masked, g in zip(masked_texts, glossaries):
                one = await call_stage1(api_key, base_url, model, [masked], [g])
                zh_list.append(one[0])

        # Stage 2 (optional)
        if stage2_enabled and model2:
            masked_src2 = masked_texts
            masked_zh2 = zh_list
            try:
                zh_list = await call_stage2(api_key2 or api_key, base_url2 or base_url, model2, masked_src2, masked_zh2)
            except Exception:
                # best-effort per item
                fixed=[]
                for s,z in zip(masked_src2, masked_zh2):
                    one = await call_stage2(api_key2 or api_key, base_url2 or base_url, model2, [s], [z])
                    fixed.append(one[0])
                zh_list = fixed

        # write back & UI
        for (m, src_text, is_num), zh_raw, mp in zip(batch, zh_list, maps):
            trans = m.find('translation')
            if trans is None: trans = ET.SubElement(m, 'translation')
            zh = _et_ready(_unmask_text(zh_raw, mp))
            zh = normalize_zh(to_zh_tw(zh))
            if is_num:
                forms = trans.findall('numerusform')
                if not forms:
                    forms=[ET.SubElement(trans, 'numerusform')]
                for f in forms:
                    f.text = zh
            else:
                trans.text = zh
            if 'type' in trans.attrib:
                trans.attrib.pop('type', None)

            _compare_add(src_text, zh)
            finished += 1
            _progress_tick(finished, total)
            _set_ui_msg(f'處理進度：{finished}/{total}')

    xml_bytes = ET.tostring(root, encoding='utf-8')
    head = b'<?xml version="1.0" encoding="utf-8"?>'
    if doctype:
        xml_bytes = head + doctype.encode('utf-8') + xml_bytes
    else:
        xml_bytes = head + b'\n' + xml_bytes
    return xml_bytes

# ---- on click ----
_BUSY=False
async def _on_click(evt=None):
    global _BUSY
    if _BUSY:
        _set_ui_msg('<span style="color:#b00">正在處理，請稍候…</span>'); return
    _BUSY=True; _set_ui_msg('')
    try:
        api = document.getElementById('apiKey').value.strip()
        base_url = document.getElementById('baseUrl').value.strip() or 'https://api.openai.com/v1'
        sel = document.getElementById('modelSel')
        model = sel.value
        if model == '__custom__':
            model = document.getElementById('modelCustom').value.strip()
        if not model:
            _set_ui_msg('<span style="color:#b00">請選擇或輸入第一階段 model id</span>'); return
        batch = int(document.getElementById('batch').value or '32')
        limitN = int(document.getElementById('limitN').value or '0')
        if not api:
            _set_ui_msg('<span style="color:#b00">請輸入 API Key（第一階段）</span>'); return
        ts_text = await _read_file_text('tsFile')
        if not ts_text:
            _set_ui_msg('<span style="color:#b00">請上傳 .ts 檔</span>'); return
        pairs = await read_glossaries_from_file_input('glsFile')

        # stage 2 config
        stage2_enabled = bool(document.getElementById('stage2Enabled').checked)
        api2 = document.getElementById('apiKey2').value.strip() or None
        base2 = document.getElementById('baseUrl2').value.strip() or None
        sel2 = document.getElementById('modelSel2')
        model2 = sel2.value
        if (model2 == '__custom2__'):
            model2 = document.getElementById('modelCustom2').value.strip()
        if not stage2_enabled:
            model2 = None

        _set_ui_msg('⏳ 連線中…')
        xml_bytes = await run_translation_pipeline_async(
            api_key=api, base_url=base_url, model=model,
            api_key2=api2 or api, base_url2=base2 or base_url, model2=model2, stage2_enabled=bool(stage2_enabled),
            ts_text=ts_text, glossary_pairs=pairs, batch_size=batch, limit_n=limitN
        )
        out_name = 'qgis_zh-Hant.ts'
        link = _build_download_link(out_name, xml_bytes)
        _set_ui_msg(link + '　<span style="color:#0a0">完成！</span>')
    except Exception as e:
        _set_ui_msg(f"<span style='color:#b00'>發生錯誤：{html.escape(str(e))}</span>")
        traceback.print_exc()
    finally:
        _BUSY=False

_BTN_PROXY = create_proxy(lambda evt: asyncio.ensure_future(_on_click(evt)))
document.getElementById('run-btn').addEventListener('click', _BTN_PROXY)
    `);
  } catch (e) {
    console.error(e);
    $msg.innerHTML = `<span style="color:#b00">Python 載入失敗：${String(e)}</span>`;
  }
  </script>
</body>
</html>
