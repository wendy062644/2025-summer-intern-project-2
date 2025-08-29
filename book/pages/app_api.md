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
  #ts-ui .ts-input > input,
  #ts-ui .ts-input > select{
    width:100%; padding:8px 10px; border:1px solid var(--ts-border);
    border-radius:10px; background:transparent; font-size:.95rem;
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
    .nbui .card{ background:#111418; border-color:#2b2f36; color:#e5e7eb; }
    .nbui button{ background:#111418; border-color:#2b2f36; color:#e5e7eb; }
    .nbui button:hover{ background:#0b0f14; }
    .nbui pre.preview{ background:#0b0f14; border-color:#2b2f36; color:#e5e7eb; }
    .nbui input[type="text"], .nbui input[type="number"], .nbui select{
      background:#0b0f14; border-color:#2b2f36; color:#e5e7eb;
    }
  }
  html[data-theme="dark"] .nbui .card{ background:#111418; border-color:#2b2f36; color:#e5e7eb; }
  html[data-theme="dark"] .nbui button{ background:#111418; border-color:#2b2f36; color:#e5e7eb; }
  html[data-theme="dark"] .nbui button:hover{ background:#0b0f14; }
  html[data-theme="dark"] .nbui pre.preview{ background:#0b0f14; border-color:#2b2f36; color:#e5e7eb; }
  html[data-theme="dark"] .nbui input[type="text"],
  html[data-theme="dark"] .nbui input[type="number"],
  html[data-theme="dark"] .nbui select{
    background:#0b0f14; border-color:#2b2f36; color:#e5e7eb;
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
        <label class="ts-label" for="modelSel">Model</label>
        <div class="ts-input">
          <select id="modelSel">
            <option value="gpt-4.1-mini" selected>gpt-4.1-mini（便宜）</option>
            <option value="gpt-4.1">gpt-4.1</option>
            <option value="gpt-4o-mini">gpt-4o-mini</option>
            <option value="gpt-4o">gpt-4o</option>
            <option value="o4-mini">o4-mini（推理）</option>
          </select>
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
        <input type="number" id="limitN" value="0" min="1" style="max-width:220px;">
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
            <th style="width:50%;">原文</th>
            <th style="width:50%;">譯文</th>
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
    // 近似 Python: 僅有空白/數字/非字元/%/{} 視為不需翻
    if (/^[\s\d\W%{}]+$/u.test(t)) return false;
    return true;
  }

  async function handleTsChange(){
    const file = tsFile.files && tsFile.files[0];
    if (!file){ countInfo.textContent = ' / 0'; limitN.removeAttribute('max'); return; }
    try{
      const txt = await file.text();
      let total = 0;

      // 優先用 DOMParser 解析 XML
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
        // 後備：正規表達抓 <source>…</source>
        const matches = txt.match(/<source>([\s\S]*?)<\/source>/g) || [];
        for (const m of matches){
          const inner = m.replace(/^<source>|<\/source>$/g, '');
          if (needsTranslationJS(inner)) total++;
        }
      }

      // 更新 UI
      if (total > 0){
        limitN.value = total;          // 將處理筆數上限設為總數
        limitN.max   = String(total);  // 避免超過
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

  // 若使用者手動改數字，限制不超過總數 & 不小於 1
  function clampLimit(){
    const max = Number(limitN.max || '0');
    let v = Number(limitN.value || '0');
    if (max){
      if (v > max) v = max;
      if (v < 1) v = 1;
      limitN.value = v;
    } else if (v < 1){
      limitN.value = 1;
    }
  }

  tsFile.addEventListener('change', handleTsChange);
  limitN.addEventListener('input', clampLimit);
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

from typing import Optional

try:
    from opencc import OpenCC
except ModuleNotFoundError:
    import micropip
    # 指定版本較穩
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
        key = f"⟦TWTERM{i}⟧"  # 不與你原本 ⟦MASKn⟧ 衝突
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
    # 清空舊列
    while tbody.firstChild:
        tbody.removeChild(tbody.firstChild)

def _compare_add(src_text:str, zh_text:str):
    box = document.getElementById("compare-box")
    box.style.display = "block"
    tbody = document.getElementById("compare-tbody")
    tr = document.createElement("tr")

    def _td(txt):
        td = document.createElement("td")
        td.style.padding = "4px"
        td.style.borderBottom = "1px solid #eee"
        td.textContent = txt  # 用 textContent 避免 HTML 注入
        return td

    tr.appendChild(_td(src_text or ""))
    tr.appendChild(_td(zh_text or ""))
    tbody.appendChild(tr)

    # 自動滾動到表格底部
    try:
        # compare-box 的第 2 個子元素是帶滾動的 div
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

async def _read_file_bytes(input_id: str)->Optional[bytes]:
    files = document.getElementById(input_id).files
    if not files or files.length==0: return None
    buf = await files.item(0).arrayBuffer()
    return bytes(buf.to_py())

def _build_download_link(filename: str, content_bytes: bytes) -> str:
    b64 = base64.b64encode(content_bytes).decode("utf-8")
    return f'<a download="{filename}" href="data:application/octet-stream;base64,{b64}">⬇️ 下載 {filename}</a>'

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

# ===== LCS 詞庫匹配（不依賴 pandas）=====
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

    def _topk_for_word(self, token:str, k:int=3)->List[Dict]:
        t_norm = token.lower()
        if len(t_norm) < self.min_token_len: return []
        t_chars = set(t_norm)
        cand = [r for r in self.rows if len(t_chars & r["charset"])>0]
        res=[]
        def anchored_prefix_sub_in(token_norm:str, cand_norm:str):
            if not token_norm or not cand_norm: return 0,""
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
        res.sort(key=lambda d: (-d["lcs_len"], len(d["en"])))
        return res[:k]

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
        for idx, tok in enumerate(tokens):
            if len(glossary)>=limit: break
            if covered[idx]: continue
            if len(tok) < min_lcs_len: continue
            for r in self._topk_for_word(tok, k=per_word_k):
                if r["lcs_len"]>=min_lcs_len and r["en"] not in glossary:
                    glossary[r["en"]] = r["zh"]; covered[idx]=True
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

# ===== OpenAI Chat Completions（批次）=====
async def call_chat_completions_batch_pyfetch(api_key:str, base_url:str, model:str,
                                              masked_texts:List[str], glossaries:List[Dict[str,str]]):
    items=[]
    for i,(t,g) in enumerate(zip(masked_texts, glossaries)):
        items.append({"id": i, "text": t, "glossary": [f"{en} -> {zh}" for en, zh in g.items()]})

    system_prompt = """你是台灣 GIS 在地化譯者，將多個獨立英文片段翻為自然專業的繁體中文（台灣）。
    規則：
    • 保留所有 ⟦MASK數字⟧；
    • 不要解釋；
    • 不要改動任何 HTML 標籤或 HTML 實體；
    • 只輸出與輸入等長、同序的結果。"""
    user_prompt = "請逐一翻譯 items。只需回傳 function 參數，不要輸出其他文字。\\n" + \
              "items = " + json.dumps(items, ensure_ascii=False)

    tools = [{
      "type": "function",
      "function": {
        "name": "return_translations",
        "description": "回傳與輸入 items 等長、同序的繁中翻譯陣列",
        "parameters": {
          "type": "object",
          "properties": {
            "translations": {
              "type": "array",
              "items": {"type": "string"}
            }
          },
          "required": ["translations"],
          "additionalProperties": False
        }
      }
    }]

    body = {
      "model": model,
      "messages": [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_prompt}
      ],
      "tools": tools,
      "tool_choice": {"type": "function", "function": {"name": "return_translations"}},
      "temperature": 0.2,
      "max_tokens": min(4000, 220 * max(4, len(masked_texts))),
    }

    resp = await pyfetch(base_url.rstrip("/") + "/chat/completions",
                         method="POST",
                         headers={"Authorization": f"Bearer {api_key}", "Content-Type":"application/json"},
                         body=json.dumps(body))
    data = await resp.json()
    if resp.status >= 400:
        raise RuntimeError(f"API Error {resp.status}: {data}")

    msg = data["choices"][0]["message"]
    tcalls = msg.get("tool_calls") or []
    if not tcalls:
        raise ValueError("模型未呼叫 function（無法取得結構化輸出）")

    args_raw = tcalls[0]["function"]["arguments"] or "{}"
    parsed = json.loads(args_raw)
    arr = parsed.get("translations")
    if not (isinstance(arr, list) and all(isinstance(x, str) for x in arr)):
        raise ValueError("function 參數不符合 {translations: string[]} 格式")

    if len(arr) != len(masked_texts):
        raise ValueError(f"JSON 陣列長度不符，期待 {len(masked_texts)}，得到 {len(arr)}")

    return arr

# ===== 主流程（加入即時對照與進度）=====
async def run_translation_pipeline_async(api_key:str, base_url:str, model:str,
                                         ts_text:str, glossary_pairs:List[Tuple[str,str]],
                                         batch_size:int=32, limit_n:int=0) -> bytes:
    doctype = _read_doctype(ts_text)
    root = ET.fromstring(ts_text)
    messages = root.findall(".//message")
    matcher = LCSMatcher(glossary_pairs, min_token_len=4, min_lcs_len=4)

    # 收集任務
    tasks=[]
    for m in messages:
        src=m.find("source")
        if src is None or src.text is None: continue
        if needs_translation(src.text):
            tasks.append((m, src.text, m.get("numerus")=="yes"))
        if len(tasks)>=limit_n: break

    finished=0; total=len(tasks)
    if total==0:
        return ET.tostring(root, encoding="utf-8")

    # 初始化 UI
    _compare_reset()
    _progress_setup(total)

    for start in range(0, total, batch_size):
        batch = tasks[start:start+batch_size]
        glossaries=[]; masked_texts=[]; maps=[]
        for _, src_text, _ in batch:
            g = matcher.build_glossary_sentence_first(src_text, limit=12, per_word_k=3, min_lcs_len=4)
            glossaries.append(g)
            masked, mp = _mask_text(src_text)
            masked_texts.append(masked); maps.append(mp)

        try:
            zh_list = await call_chat_completions_batch_pyfetch(api_key, base_url, model, masked_texts, glossaries)
        except Exception as e:
            zh_list=[]
            for masked, g in zip(masked_texts, glossaries):
                one = await call_chat_completions_batch_pyfetch(api_key, base_url, model, [masked], [g])
                zh_list.append(one[0])

        # 寫回 XML，並即時輸出「原文／譯文」對照與進度
        for (m, src_text, is_num), zh_raw, mp in zip(batch, zh_list, maps):
            trans = m.find("translation")
            if trans is None:
                trans = ET.SubElement(m, "translation")
            zh = _et_ready(_unmask_text(zh_raw, mp))
            zh = normalize_zh(to_zh_tw(zh))
            if is_num:
                forms = trans.findall("numerusform")
                if not forms:
                    forms=[ET.SubElement(trans, "numerusform")]
                for f in forms:
                    f.text = zh
            else:
                trans.text = zh
            if "type" in trans.attrib: trans.attrib.pop("type", None)

            # 即時對照（翻譯前 / 翻譯後）
            _compare_add(src_text, zh)

            finished += 1
            _progress_tick(finished, total)

        _set_ui_msg(f"處理進度：{finished}/{total}")

    xml_bytes = ET.tostring(root, encoding="utf-8")
    head = b'<?xml version="1.0" encoding="utf-8"?>'
    if doctype: xml_bytes = head + (doctype).encode("utf-8") + xml_bytes
    else: xml_bytes = head + b"\\n" + xml_bytes
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
        model = document.getElementById("modelSel").value
        batch = int(document.getElementById("batch").value or "32")
        limitN = int(document.getElementById("limitN").value or "200")
        if not api:
            _set_ui_msg("<span style='color:#b00'>請輸入 API Key</span>"); return
        ts_text = await _read_file_text("tsFile")
        if not ts_text:
            _set_ui_msg("<span style='color:#b00'>請上傳 .ts 檔</span>"); return

        pairs = await read_glossaries_from_file_input("glsFile")

        _set_ui_msg("⏳ 連線中…")
        xml_bytes = await run_translation_pipeline_async(
            api_key=api, base_url=base_url, model=model,
            ts_text=ts_text, glossary_pairs=pairs,
            batch_size=batch, limit_n=limitN
        )

        out_name = "qgis_zh-Hant.ts"
        ts_files = document.getElementById("tsFile").files

        link = _build_download_link(out_name, xml_bytes)
        _set_ui_msg(link + "　<span style='color:#0a0'>完成！</span>")
    except Exception as e:
        _set_ui_msg(f"<span style='color:#b00'>發生錯誤：{html.escape(str(e))}</span>")
        traceback.print_exc()
    finally:
        _BUSY=False

_BTN_PROXY = create_proxy(lambda evt: asyncio.ensure_future(_on_click(evt)))
document.getElementById("run-btn").addEventListener("click", _BTN_PROXY)
`);
} catch (e) {
  console.error(e);
  $msg.innerHTML = `<span style="color:#b00">Python 載入失敗：${String(e)}</span>`;
}
</script>