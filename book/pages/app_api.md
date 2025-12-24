<title>API</title>

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
    color: var(--ts-text);
  }
  #ts-ui .wrap{ padding: 16px; background: var(--ts-bg); border: 1px solid var(--ts-border); border-radius: 14px; }
  #ts-ui .grid{ display:grid; grid-template-columns: 1fr 1fr; gap: var(--ts-gap); }
  #ts-ui .card{
    border: 1px solid var(--ts-border);
    border-radius: var(--ts-radius);
    background: #fff;
    padding: var(--ts-pad);
    box-shadow: 0 1px 2px rgba(0,0,0,.04);
  }
  #ts-ui h2{ font-size: 18px; margin: 0 0 10px; }
  #ts-ui label{ display:block; font-size: 13px; color: var(--ts-muted); margin-bottom: 6px; }
  #ts-ui input[type="text"], #ts-ui input[type="password"], #ts-ui select{
    width: 100%;
    padding: 10px 12px;
    border: 1px solid var(--ts-border);
    border-radius: 10px;
    outline: none;
    background: #fff;
  }
  #ts-ui .row{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
  #ts-ui .btn{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid var(--ts-border);
    background: #fff;
    cursor:pointer;
    user-select:none;
    transition: .15s;
    font-size: 14px;
  }
  #ts-ui .btn.primary{
    background: var(--ts-accent);
    color: var(--ts-on-accent);
    border-color: var(--ts-accent);
  }
  #ts-ui .btn:hover{ transform: translateY(-1px); box-shadow: 0 2px 6px rgba(0,0,0,.08); }
  #ts-ui .btn:disabled{ opacity:.55; cursor:not-allowed; transform:none; box-shadow:none; }
  #ts-ui .hint{ font-size: 12px; color: var(--ts-muted); margin-top: 8px; line-height:1.5; }
  #ts-ui .progress{
    width: 100%;
    height: 14px;
    border-radius: 999px;
    background: var(--ts-progress-bg);
    overflow:hidden;
  }
  #ts-ui progress{ width:100%; height: 14px; }
  #ts-ui .kvs{ font-size: 13px; color: var(--ts-muted); margin-top: 8px; }
  #ts-ui .filebox{
    border: 1px dashed var(--ts-border);
    border-radius: 12px;
    padding: 12px;
    background: #fafafa;
  }
  #ts-ui .filebox input{ width:100%; }
  #ts-ui table{
    width:100%;
    border-collapse: collapse;
    margin-top: 10px;
    font-size: 13px;
  }
  #ts-ui th, #ts-ui td{
    border: 1px solid var(--ts-border);
    padding: 8px;
    vertical-align: top;
  }
  #ts-ui th{
    background: var(--ts-table-head-bg);
    text-align:left;
    position: sticky;
    top: 0;
    z-index: 1;
  }
  #ts-ui .compare-box{
    max-height: 320px;
    overflow:auto;
    border: 1px solid var(--ts-border);
    border-radius: 12px;
    margin-top: 10px;
    display:none;
  }
  #ts-ui .mono{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }
</style>

<div id="ts-ui">
  <div class="wrap">
    <div class="grid">
      <div class="card">
        <h2>1) 來源檔案</h2>
        <div class="filebox">
          <label>上傳待翻譯 .ts（目標檔）</label>
          <input id="ts-file" type="file" accept=".ts"/>
          <div class="hint">只會翻譯尚未有 translation 或 unfinished 的訊息。</div>
        </div>

        <div style="height:10px"></div>

        <div class="filebox">
          <label>（可選）上傳舊版 .ts 以沿用既有翻譯</label>
          <input id="old-ts-file" type="file" accept=".ts"/>
          <div class="hint">若 source 完全相同，會直接沿用舊版翻譯，減少 API 次數。</div>
        </div>

        <div style="height:10px"></div>

        <div class="filebox">
          <label>（可選）上傳 glossary（CSV/ODS/TSV 文字）</label>
          <input id="glossary-file" type="file"/>
          <div class="hint">格式：每行「英文,中文」或 ODS 表格含「英文名稱/中文名稱」。</div>
        </div>
      </div>

      <div class="card">
        <h2>2) API 設定</h2>

        <label>Base URL（可留空，使用 OpenAI 預設）</label>
        <input id="base-url" type="text" placeholder="https://api.openai.com/v1"/>

        <div style="height:10px"></div>

        <label>API Key</label>
        <input id="api-key" type="password" placeholder="sk-..."/>

        <div style="height:10px"></div>

        <div class="row">
          <div style="flex:1; min-width: 220px;">
            <label>Model-1（翻譯）</label>
            <input id="model-1" type="text" value="gpt-4.1-mini"/>
          </div>
          <div style="flex:1; min-width: 220px;">
            <label>Model-2（挑選/校正，可選）</label>
            <input id="model-2" type="text" value="gpt-4.1-mini"/>
          </div>
        </div>

        <div style="height:10px"></div>

        <div class="row">
          <label style="margin:0; display:flex; gap:8px; align-items:center;">
            <input id="use-model-2" type="checkbox" checked/>
            使用 Model-2 挑選 A/B/C 並做格式校正（較慢、較貴，但一致性更好）
          </label>
        </div>

        <div style="height:10px"></div>

        <div class="row">
          <button id="run-btn" class="btn primary">開始翻譯</button>
          <button id="pause-btn" class="btn">暫停</button>
          <button id="resume-btn" class="btn">繼續</button>
          <button id="download-btn" class="btn" disabled>下載翻譯後 .ts</button>
        </div>

        <div class="kvs">
          <div id="status-line" class="mono"></div>
        </div>

        <div style="height:10px"></div>
        <label>進度</label>
        <progress id="ts-progress" value="0" max="100"></progress>
        <div id="ts-progress-label" class="kvs mono"></div>

        <div class="compare-box" id="compare-box">
          <table>
            <thead>
              <tr>
                <th style="width:38%">SOURCE</th>
                <th style="width:38%">TRANSLATION</th>
                <th style="width:24%">CONTEXT</th>
              </tr>
            </thead>
            <tbody id="compare-tbody"></tbody>
          </table>
        </div>

        <div class="hint">
          若勾選 Model-2：每批會先用 Model-1 產生 A/B/C，再由 Model-2 決定最終譯文。<br/>
          若不勾 Model-2：只會用 Model-1 翻譯一次（不做 A/B/C）。<br/>
          會保留 placeholders（如 %1、{0}、⟦M0⟧）與 ASCII 半形符號順序。
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  // ====== 介面狀態 ======
  const UI = {
    tsFile: document.getElementById("ts-file"),
    oldTsFile: document.getElementById("old-ts-file"),
    glossaryFile: document.getElementById("glossary-file"),
    baseUrl: document.getElementById("base-url"),
    apiKey: document.getElementById("api-key"),
    model1: document.getElementById("model-1"),
    model2: document.getElementById("model-2"),
    useModel2: document.getElementById("use-model-2"),
    runBtn: document.getElementById("run-btn"),
    pauseBtn: document.getElementById("pause-btn"),
    resumeBtn: document.getElementById("resume-btn"),
    downloadBtn: document.getElementById("download-btn"),
    statusLine: document.getElementById("status-line"),
    progress: document.getElementById("ts-progress"),
    progressLabel: document.getElementById("ts-progress-label"),
    compareBox: document.getElementById("compare-box"),
    compareTbody: document.getElementById("compare-tbody"),
  };

  function setStatus(html){
    UI.statusLine.innerHTML = html || "";
  }

  // ====== 讀檔工具 ======
  function readFileAsArrayBuffer(file){
    return new Promise((resolve,reject)=>{
      const fr = new FileReader();
      fr.onload = () => resolve(fr.result);
      fr.onerror = reject;
      fr.readAsArrayBuffer(file);
    });
  }
  function readFileAsText(file){
    return new Promise((resolve,reject)=>{
      const fr = new FileReader();
      fr.onload = () => resolve(fr.result);
      fr.onerror = reject;
      fr.readAsText(file, "utf-8");
    });
  }

  // ====== 暫停/繼續 ======
  window._TS_PAUSED = false;
  UI.pauseBtn.onclick = () => {
    window._TS_PAUSED = true;
    setStatus("<span style='color:#b00'>已暫停（可按「繼續」）</span>");
  };
  UI.resumeBtn.onclick = () => {
    window._TS_PAUSED = false;
    setStatus("<span style='color:#0a0'>已繼續</span>");
  };

  // ====== Pyodide 載入 ======
  let pyodideReadyPromise = null;
  async function ensurePyodide(){
    if(pyodideReadyPromise) return pyodideReadyPromise;
    pyodideReadyPromise = (async ()=>{
      // 使用 JupyterLite/pyodide 的全域 loadPyodide
      if(typeof loadPyodide === "undefined"){
        throw new Error("找不到 loadPyodide，請確認本頁已載入 pyodide");
      }
      const pyodide = await loadPyodide();
      await pyodide.loadPackage(["micropip"]);
      // 這裡不安裝重型依賴，避免卡住；我們用純標準庫 + opencc-lite 自己做
      return pyodide;
    })();
    return pyodideReadyPromise;
  }

  // ====== 把檔案傳給 Python ======
  function bytesFromArrayBuffer(ab){
    return new Uint8Array(ab);
  }

  // ====== Python 程式碼（只改這段） ======
  const PY_CODE = String.raw`
import asyncio, json, re, html, io, zipfile
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple
from js import window, document

# ===== JS 互動 =====
def _set_ui_msg(html_str: str):
    document.getElementById("status-line").innerHTML = html_str or ""

def _progress_init(total:int):
    bar = document.getElementById("ts-progress")
    lab = document.getElementById("ts-progress-label")
    bar.max = total if total>0 else 100
    bar.value = 0
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

def _compare_add(src:str, zh:str, ctx:str):
    tbody = document.getElementById("compare-tbody")
    tr = document.createElement("tr")
    td1 = document.createElement("td"); td1.innerText = src
    td2 = document.createElement("td"); td2.innerText = zh
    td3 = document.createElement("td"); td3.innerText = ctx
    tr.appendChild(td1); tr.appendChild(td2); tr.appendChild(td3)
    tbody.appendChild(tr)

# ====== HTTP 呼叫（OpenAI 相容） ======
async def call_api(api_key:str, base_url:str, model:str, payload:Dict[str,Any]) -> Dict[str,Any]:
    import js
    if not base_url:
        base_url = "https://api.openai.com/v1"
    url = base_url.rstrip("/") + "/chat/completions"
    headers = js.Object.fromEntries([["Content-Type","application/json"],["Authorization", f"Bearer {api_key}"]])
    resp = await js.fetch(url, method="POST", headers=headers, body=json.dumps(payload))
    if not resp.ok:
        txt = await resp.text()
        raise RuntimeError(f"HTTP {resp.status}: {txt}")
    data = await resp.json()
    # 解析 tool call
    try:
        choice = data["choices"][0]
        msg = choice["message"]
        if "tool_calls" in msg and msg["tool_calls"]:
            args = msg["tool_calls"][0]["function"]["arguments"]
            return json.loads(args)
        # fallback：直接 content
        content = msg.get("content","")
        return {"results":[content]}
    except Exception:
        return {"results":[]}

# ====== TS 解析/讀寫 ======
def parse_ts_bytes(ts_bytes: bytes) -> Tuple[ET.ElementTree, ET.Element, Optional[str]]:
    # 保留 doctype（若有）
    text = ts_bytes.decode("utf-8", errors="ignore")
    m = re.search(r"(<!DOCTYPE[^>]+>)", text)
    doctype = m.group(1) if m else None

    # ElementTree 解析
    root = ET.fromstring(text)
    return ET.ElementTree(root), root, doctype

def get_source_text(msg: ET.Element) -> str:
    s = msg.find("source")
    return (s.text or "") if s is not None else ""

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
    t = msg.find("translation")
    if t is None:
        t = ET.SubElement(msg, "translation")
    # 清掉 unfinished
    if "type" in t.attrib:
        if t.attrib.get("type") == "unfinished":
            del t.attrib["type"]

    # numerus
    if isinstance(text_or_list, list):
        # 確保 numerus 子節點存在
        cur = t.findall("numerusform")
        # 對齊數量
        need = len(text_or_list)
        while len(cur) < need:
            ET.SubElement(t, "numerusform")
            cur = t.findall("numerusform")
        for i, val in enumerate(text_or_list):
            cur[i].text = val
        return

    t.text = text_or_list

def build_old_index(old_ts_text: str) -> Dict[str, Dict[str, Any]]:
    m: Dict[str, Dict[str, Any]] = {}
    try:
        root = ET.fromstring(old_ts_text)
    except Exception:
        return m
    for ctx in root.findall("context"):
        name = ctx.find("name")
        ctxname = (name.text or "") if name is not None else ""
        for msg in ctx.findall("message"):
            src = get_source_text(msg)
            if not src.strip():
                continue
            tr = msg.find("translation")
            numerus = (msg.get("numerus") == "yes")
            if tr is None:
                continue
            if tr.get("type") == "unfinished":
                continue
            if numerus:
                forms = tr.findall("numerusform")
                if forms:
                    vals = [(f.text or "") for f in forms]
                    if all(v.strip() for v in vals):
                        m[src] = {"trans": vals, "ctx": ctxname}
                else:
                    val = (tr.text or "")
                    if val.strip():
                        m[src] = {"trans": val, "ctx": ctxname}
            else:
                val = (tr.text or "")
                if val.strip():
                    m[src] = {"trans": val, "ctx": ctxname}
    return m

# ====== placeholder / & mnemonic / 符號修復 ======
_MASK_PAT = re.compile(r"(%L\d+|%\d+|%[sdn]|\{\d+\})|(&[A-Za-z0-9])")
_COORD_RE = re.compile(r"\bcoordinate(s)?\b", re.I)
_MNEMONIC_RE = re.compile(r"&([A-Za-z0-9])")
_SEP_RE = re.compile(r"[\s\-_]+")

# 用語偏好
_TERM_REPL = [
    (re.compile(r"插件"), "外掛程式"),
    (re.compile(r"凸殼"), "凸包"),
    (re.compile(r"處理中"), "處理"),
    (re.compile(r"\bLineString\b"), "線串"),
    (re.compile(r"\bBase level\b", re.I), "基準值"),
    (re.compile(r"\bArrow head\b", re.I), "箭頭端"),
    (re.compile(r"\bLine alignment\b", re.I), "線條對齊"),
    (re.compile(r"\bModel scale\b", re.I), "模型縮放比例"),
    (re.compile(r"\bRow\b", re.I), "列"),
    (re.compile(r"\bpixels\b", re.I), "像素"),
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

def to_zh_tw(s: Optional[str]) -> str:
    # 簡易：用幾個常見替換，避免引入 heavy 套件
    if not s: return ""
    # 你若有 OpenCC 可以加強，這裡先保守
    return s.replace("坐标","座標").replace("图层","圖層").replace("矢量","向量")

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

def repair_placeholders(src: str, trans: str) -> tuple[str, bool]:
    pat = re.compile(r"(%L\d+|%\d+|%[sdn]|\{\d+\})")
    src_list = pat.findall(src or "")
    tr_list  = pat.findall(trans or "")

    if not src_list and not tr_list:
        return trans, True
    if len(src_list) != len(tr_list):
        return trans, False

    fixed = trans
    for s_ph, t_ph in zip(src_list, tr_list):
        if s_ph != t_ph:
            fixed = fixed.replace(t_ph, s_ph, 1)

    return fixed, (pat.findall(fixed) == src_list)

def validate_placeholders(src: str, trans: str) -> bool:
    pat = re.compile(r"(%\d|%[sdn]|\{\d+\})")
    src_set = sorted(pat.findall(src or ""))
    trans_set = sorted(pat.findall(trans or ""))
    return src_set == trans_set

def restore_leading_symbols(src: str, trans: str) -> str:
    m = re.match(r"^([)\]};:,.|]+)", src or "")
    if not m:
        return trans
    head = m.group(1)
    if trans.startswith(head):
        return trans
    # 嘗試把 head 插回去
    return head + trans

def _et_ready(s:str) -> str:
    try:
        return html.unescape(s)
    except Exception:
        return s

def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip():
        return False
    if re.fullmatch(r"[\s\d\W%{}]+", en_text):
        return False
    return True

def soft_norm(s:str) -> str:
    return _SEP_RE.sub(" ", s.lower()).strip()

# ====== glossary：LCS-ish ======
class LCSMatcher:
    def __init__(self, pairs: List[Tuple[str,str]]):
        self.pairs = [(a.strip(), b.strip()) for a,b in pairs if a and b]

    def build_glossary_sentence_first(self, src: str, topk:int=12) -> Dict[str,str]:
        # 簡單：找出出現的英文片段
        out = {}
        src_low = src.lower()
        for en, zh in self.pairs:
            if not en: continue
            if en.lower() in src_low:
                out[en] = zh
        # 限制數量
        items = list(out.items())[:topk]
        return dict(items)

def load_glossary_csv_text(text: str) -> List[Tuple[str,str]]:
    pairs = []
    for line in (text or "").splitlines():
        line=line.strip()
        if not line or line.startswith("#"): 
            continue
        # 支援 tab / comma
        if "\t" in line:
            a,b = line.split("\t",1)
        elif "," in line:
            a,b = line.split(",",1)
        else:
            continue
        a=a.strip(); b=b.strip()
        if a and b:
            pairs.append((a,b))
    return pairs

def load_glossary_ods_bytes(b: bytes) -> List[Tuple[str,str]]:
    # 只做最基本 ODS 解析（content.xml）找「英文名稱/中文名稱」
    pairs = []
    try:
        zf = zipfile.ZipFile(io.BytesIO(b))
        content = zf.read("content.xml").decode("utf-8", errors="ignore")
        # 很粗略：抓 table:table-row 內的 text:p
        rows = re.findall(r"<table:table-row[^>]*>(.*?)</table:table-row>", content, flags=re.S)
        if not rows:
            return pairs
        # 取前幾列 header 來定位欄位
        parsed = []
        for r in rows[:2000]:
            cells = re.findall(r"<text:p[^>]*>(.*?)</text:p>", r, flags=re.S)
            cells = [re.sub(r"<[^>]+>","",c).strip() for c in cells]
            parsed.append(cells)
        if not parsed:
            return pairs
        header = parsed[0]
        # 找欄位 index
        def find_idx(keys):
            for i, h in enumerate(header):
                for k in keys:
                    if k in h:
                        return i
            return None
        i_en = find_idx(["英文名稱","en","English"])
        i_zh = find_idx(["中文名稱","zh","Chinese"])
        if i_en is None or i_zh is None:
            return pairs
        for row in parsed[1:]:
            if len(row) <= max(i_en, i_zh):
                continue
            en = (row[i_en] or "").strip()
            zh = (row[i_zh] or "").strip()
            if en and zh:
                pairs.append((en, zh))
    except Exception:
        return pairs
    return pairs

async def read_glossaries_from_file_input(glossary_bytes: Optional[bytes], glossary_name: str) -> List[Tuple[str,str]]:
    if not glossary_bytes:
        return []
    name = (glossary_name or "").lower()
    if name.endswith(".ods"):
        return load_glossary_ods_bytes(glossary_bytes)
    # default: text
    try:
        text = glossary_bytes.decode("utf-8", errors="ignore")
    except Exception:
        text = ""
    return load_glossary_csv_text(text)

# ====== 主流程 ======
async def run_translation_pipeline_async(
    ts_bytes: bytes,
    old_ts_text: Optional[str],
    glossary_bytes: Optional[bytes],
    glossary_name: str,
    api_key: str,
    base_url: str,
    model1: str,
    model2: str,
    use_model2: bool,
    batch_size: int = 25
) -> bytes:
    tree, root, doctype = parse_ts_bytes(ts_bytes)

    # glossary
    pairs = await read_glossaries_from_file_input(glossary_bytes, glossary_name)
    matcher = LCSMatcher(pairs)

    # old index
    old_map = build_old_index(old_ts_text or "") if old_ts_text else {}

    # collect tasks
    tasks = []
    reused = 0
    for ctx in root.findall("context"):
        cname_el = ctx.find("name")
        ctxname = (cname_el.text or "") if cname_el is not None else ""
        for msg in ctx.findall("message"):
            src = get_source_text(msg)
            if not needs_translation(src):
                continue
            # 已有翻譯就跳過
            if is_translation_filled(msg):
                continue
            # 沿用舊版
            if src in old_map:
                set_translation(msg, old_map[src]["trans"])
                reused += 1
                continue
            # 需要翻譯
            comment = msg.find("comment")
            note = (comment.text or "") if comment is not None else ""
            context = f"{ctxname}"
            if note.strip():
                context += f" | 註釋: {note.strip()}"
            tasks.append({
                "src": src,
                "context": context,
                "node": msg,
                "numerus": (msg.get("numerus") == "yes"),
            })

    total = len(tasks)
    _compare_reset()
    _progress_init(total)
    _set_ui_msg(f"待翻譯：{total} 筆；已沿用舊版：{reused} 筆")

    # tool schema
    tools_schema = [{
        "type":"function",
        "function":{
            "name":"set_results",
            "description":"Return translations list in same order.",
            "parameters":{
                "type":"object",
                "properties":{
                    "results":{"type":"array","items":{"type":"string"}}
                },
                "required":["results"]
            }
        }
    }]

    sys_prompt = (
        "你是台灣 GIS 在地化譯者。"
        " 對於每一個項目，只翻譯 `text` 欄位中的英文內容成繁體中文（台灣用語）。"
        " 可以參考 `context` 與 `glossary` 來判斷，但不要把 context 的文字（例如「介面: ...」「註釋: ...」）當成輸出的一部分。"
        " 請呼叫工具 set_results，並只在 results 陣列中依序填入翻譯後的字串。"
        " 保留所有 ASCII 半形符號（例如 ()[]{};:,.?+/\\\\*& 等），數量與順序都必須與原文完全一致。"
        " 務必保留所有 ⟦M數字⟧ 變數與 %1、{0} 這類 placeholder，不可遺失或改變順序。"
        " 若字串看起來是程式碼變數、常數、enum 名稱、函式名稱、人名或英文縮寫，優先保留原文不翻。"
        " 若原文字串含有快捷鍵標記 &X（X 為字母或數字），譯文中不要出現 &X；請在譯文最後加上 ( &X )（不含空格），且 X 必須與原文一致。"
        " 用語偏好（若語意相同，優先使用）：插件→外掛程式、凸殼→凸包、處理中→處理、LineString→線串、Base level→基準值、"
        " Arrow head→箭頭端、Line alignment→線條對齊、Model scale→模型縮放比例、Row→列、pixels→像素。"
        " 若沒有合適或確定的中文翻譯，寧可保留英文原文，不要亂造詞。"
    )

    # Model-2 回傳異常時：本地挑選 A/B/C（以 placeholder 完整度與格式一致為主）
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
                sc += 10
            # 長度接近原文（避免跑出一堆 context）加分
            sc -= abs(len(cand) - len(src))
            if sc > best_score:
                best_score = sc
                best = cand
        return best

    # 3次翻譯溫度（gpt-5/o1/o3 會被移除，但仍照流程）
    temps = [0.2, 0.7, 1.0]

    finished = 0
    for start in range(0, total, batch_size):
        while window._TS_PAUSED:
            await asyncio.sleep(0.2)

        batch = tasks[start:start+batch_size]

        # 建 glossary + mask placeholders
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

        if use_model2 and model2:
            # ① Model-1：A/B/C 三次（僅在需要 Model-2 仲裁時才做）
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
            def _pad(lst):
                if len(lst) < len(batch):
                    lst += [""] * (len(batch) - len(lst))
                return lst[:len(batch)]
            listA, listB, listC = _pad(listA), _pad(listB), _pad(listC)

            # ② Model-2：挑選 + 格式校正（一次）
            sel_items = [
                {
                    "id": i,
                    "src": it["src"],
                    "context": it["context"],
                    "glossary": gls_list[i],
                    "A": listA[i],
                    "B": listB[i],
                    "C": listC[i],
                }
                for i, it in enumerate(batch)
            ]

            sel_payload = {
                "model": model2,
                "temperature": 0.0,
                "tools": tools_schema,
                "tool_choice": {"type":"function", "function":{"name":"set_results"}},
                "messages": [
                    {
                        "role":"system",
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
                    {"role":"user", "content": "請處理下列項目：\\n" + json.dumps(sel_items, ensure_ascii=False)}
                ]
            }

            res_final = await call_api(api_key, base_url, model2, sel_payload)
            zh_list = res_final.get("results", []) if res_final else [""] * len(batch)
            if len(zh_list) < len(batch):
                zh_list += [""] * (len(batch) - len(zh_list))
            zh_list = zh_list[:len(batch)]

            # Model-2 偶發回空：fallback 本地挑選 A/B/C（不再額外翻譯）
            for j in range(len(zh_list)):
                if not zh_list[j]:
                    zh_list[j] = local_pick_best(batch[j]["src"], [listA[j], listB[j], listC[j]])

        else:
            # ① Model-1：只翻譯一次（未勾 Model-2 時，避免重複翻譯）
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
            res1 = await call_api(api_key, base_url, model1, payload)
            zh_list = res1.get("results", []) if res1 else [""] * len(batch)
            if len(zh_list) < len(batch):
                zh_list += [""] * (len(batch) - len(zh_list))
            zh_list = zh_list[:len(batch)]

        # ③ 寫回 XML（含快捷鍵規則、用語偏好、placeholder 修復）
        for i in range(len(batch)):
            item = batch[i]
            zh_raw = zh_list[i] if i < len(zh_list) else ""
            if not zh_raw:
                zh_raw = item["src"]  # API 回傳空時：保留原文，避免進度卡住

            zh = _unmask_text(zh_raw, maps[i])
            zh = _et_ready(zh)
            zh = strip_all_newlines(zh)
            zh = fix_zh_punct(zh)
            zh = normalize_zh(to_zh_tw(zh))

            # 用語偏好後處理（含 插件/凸殼/處理中…）
            zh = apply_term_preferences(zh)

            # placeholder 修復
            zh, ok_ph = repair_placeholders(item["src"], zh)

            # context leak 防呆
            zh = fix_context_leak(item["src"], zh, item["context"])

            # 頭部符號修復
            zh = restore_leading_symbols(item["src"], zh)

            # 快捷鍵規則：&X → 末尾 (&X)
            zh = apply_mnemonic_rule(item["src"], zh)

            if not ok_ph:
                zh = f"[變數錯誤] {zh}"

            # numerus：寫入每個 plural form（Qt TS 以 <numerusform> 為主）
            if item.get("numerus"):
                tr = item["node"].find("translation")
                forms = tr.findall("numerusform") if tr is not None else []
                nforms = len(forms) if forms else 2
                set_translation(item["node"], [zh] * nforms)
            else:
                set_translation(item["node"], zh)

            _compare_add(item["src"], zh, item["context"])
            finished += 1
            _progress_tick(finished, total)

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
    document.getElementById("pause-btn").style.display = "inline-flex"
    document.getElementById("resume-btn").style.display = "inline-flex"

    # 讀取 UI 值
    api_key = document.getElementById("api-key").value.strip()
    base_url = document.getElementById("base-url").value.strip()
    model1 = document.getElementById("model-1").value.strip()
    model2 = document.getElementById("model-2").value.strip()
    use_model2 = bool(document.getElementById("use-model-2").checked)

    if not api_key:
        _set_ui_msg("<span style='color:#b00'>請先輸入 API Key</span>")
        _BUSY = False
        return

    # 取檔案 bytes
    if not window._TS_BYTES:
        _set_ui_msg("<span style='color:#b00'>請先上傳待翻譯 .ts</span>")
        _BUSY = False
        return

    old_text = window._OLD_TS_TEXT if hasattr(window, "_OLD_TS_TEXT") else None
    gls_bytes = window._GLOSSARY_BYTES if hasattr(window, "_GLOSSARY_BYTES") else None
    gls_name  = window._GLOSSARY_NAME if hasattr(window, "_GLOSSARY_NAME") else ""

    try:
        out_bytes = await run_translation_pipeline_async(
            window._TS_BYTES.to_py(),
            old_text,
            gls_bytes.to_py() if gls_bytes else None,
            gls_name,
            api_key, base_url, model1, model2, use_model2
        )
        window._OUT_TS_BYTES = out_bytes
        document.getElementById("download-btn").disabled = False
        _set_ui_msg("<span style='color:#0a0'>完成！可下載翻譯後 .ts</span>")
    except Exception as e:
        _set_ui_msg(f"<span style='color:#b00'>錯誤：{html.escape(str(e))}</span>")
    finally:
        _BUSY = False

def setup_py_handlers():
    # 綁定 run button
    btn = document.getElementById("run-btn")
    btn.onclick = lambda evt: asyncio.ensure_future(_on_click(evt))

setup_py_handlers()
`;

  // ====== 下載結果 ======
  UI.downloadBtn.onclick = () => {
    const b = window._OUT_TS_BYTES;
    if(!b) return;
    const blob = new Blob([b], {type:"application/xml"});
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "translated.ts";
    a.click();
    URL.revokeObjectURL(a.href);
  };

  // ====== 檔案上傳：存到 window 供 Python 讀 ======
  UI.tsFile.onchange = async () => {
    const f = UI.tsFile.files?.[0];
    if(!f) return;
    const ab = await readFileAsArrayBuffer(f);
    window._TS_BYTES = bytesFromArrayBuffer(ab);
    setStatus(`<span style="color:#0a0">已載入：${f.name}</span>`);
    UI.downloadBtn.disabled = true;
  };

  UI.oldTsFile.onchange = async () => {
    const f = UI.oldTsFile.files?.[0];
    if(!f) { window._OLD_TS_TEXT = null; return; }
    const txt = await readFileAsText(f);
    window._OLD_TS_TEXT = txt;
    setStatus(`<span style="color:#0a0">已載入舊版：${f.name}</span>`);
  };

  UI.glossaryFile.onchange = async () => {
    const f = UI.glossaryFile.files?.[0];
    if(!f) { window._GLOSSARY_BYTES = null; window._GLOSSARY_NAME=""; return; }
    const ab = await readFileAsArrayBuffer(f);
    window._GLOSSARY_BYTES = bytesFromArrayBuffer(ab);
    window._GLOSSARY_NAME = f.name;
    setStatus(`<span style="color:#0a0">已載入 glossary：${f.name}</span>`);
  };

  // ====== RUN：載入 pyodide + 執行 python ======
  UI.runBtn.onclick = async () => {
    try{
      setStatus("初始化中…");
      const pyodide = await ensurePyodide();
      setStatus("載入 Python 程式…");
      await pyodide.runPythonAsync(PY_CODE);
      setStatus("<span style='color:#0a0'>已啟動（按一次「開始翻譯」即可）</span>");
      // Python 內 setup_py_handlers 會綁 run 按鈕；這裡不重綁
    }catch(e){
      console.error(e);
      setStatus(`<span style='color:#b00'>Pyodide 錯誤：${String(e)}</span>`);
    }
  };
</script>
