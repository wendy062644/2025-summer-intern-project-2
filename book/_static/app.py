import asyncio, json, re, io, base64, traceback, os, sys, html, csv
from typing import List, Tuple, Dict, Optional
from xml.etree import ElementTree as ET
from getpass import getpass

# ---------- 環境偵測 ----------
JS_AVAILABLE = False
PYODIDE_FETCH = None
DISPLAY_HTML = None
try:
    # Pyodide 環境（可能沒有 js 模組就會失敗）
    import pyodide
    try:
        from js import document  # 若成功則可做頁面 UI
        JS_AVAILABLE = True
    except Exception:
        JS_AVAILABLE = False
    try:
        from pyodide.http import pyfetch
        PYODIDE_FETCH = pyfetch
    except Exception:
        PYODIDE_FETCH = None
    try:
        from IPython.display import display, HTML
        def _display_html(s): display(HTML(s))
        DISPLAY_HTML = _display_html
    except Exception:
        DISPLAY_HTML = None
except Exception:
    # Server Python kernel
    JS_AVAILABLE = False
    PYODIDE_FETCH = None
    try:
        from IPython.display import display, HTML
        def _display_html(s): display(HTML(s))
        DISPLAY_HTML = _display_html
    except Exception:
        DISPLAY_HTML = None

# ---------- 小工具 ----------
def _log_print(s: str):
    print(s, flush=True)

def _build_download_link(filename: str, content_bytes: bytes) -> str:
    b64 = base64.b64encode(content_bytes).decode('utf-8')
    return f'<a download="{filename}" href="data:application/octet-stream;base64,{b64}">⬇️ 下載 {filename}</a>'

def _read_doctype(xml_text: str) -> str:
    m = re.search(r'<!DOCTYPE[^>]+>', xml_text)
    return m.group(0) if m else ""

# ---------- 遮罩/還原（與你原版規則一致） ----------
_MASK_PAT = re.compile(
    r'('
    r'</?[A-Za-z][^>]*>'
    r'|&lt;/?[A-Za-z][^&]*?&gt;'
    r'|%L\d+'
    r'|%\d+'
    r'|%n'
    r'|\{\d+\}'
    r'|&(?:[A-Za-z]+|#\d+|#x[0-9A-Fa-f]+);'
    r')',
    flags=re.IGNORECASE
)
def _mask_text(s: str):
    idx = 0
    mapping: Dict[str, str] = {}
    def _repl(m):
        nonlocal idx
        key = f"⟦MASK{idx}⟧"
        mapping[key] = m.group(0)
        idx += 1
        return key
    return _MASK_PAT.sub(_repl, s), mapping

def _unmask_text(s: str, mapping: Dict[str, str]) -> str:
    for k, v in mapping.items():
        s = s.replace(k, v)
    return s

def _et_ready(s: str) -> str:
    try:
        return html.unescape(s)
    except Exception:
        return s

def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip(): return False
    if re.fullmatch(r"[\s\d\W%{}]+", en_text): return False
    return True

# ---------- 簡化版 glossary index（CSV: en,zh 或 英文名稱,中文名稱） ----------
_SEP_RE = re.compile(r'[\s/_\-.]+')
def soft_norm(s: str) -> str:
    return _SEP_RE.sub(' ', s.lower()).strip()
_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[\/_.-][A-Za-z0-9]+)*")

class GlossaryIndex:
    def __init__(self, pairs: List[Tuple[str,str]]):
        self.index: Dict[str, Tuple[str,str]] = {}
        self.max_soft_len = 1
        for en, zh in pairs:
            key = soft_norm(en)
            if key and (key not in self.index):
                self.index[key] = (en, zh)
                self.max_soft_len = max(self.max_soft_len, len(key.split()))
    def build_for_text(self, text: str, limit: int = 12) -> Dict[str,str]:
        if not self.index: return {}
        text_clean = _MASK_PAT.sub(" ", text)
        toks = [t.lower() for t in _TOKEN_RE.findall(text_clean)]
        n = len(toks); covered = [False]*n; out: Dict[str,str] = {}
        def mark(i,j):
            for k in range(i,j): covered[k]=True
        win = min(n, self.max_soft_len)
        for wlen in range(win, 0, -1):
            if len(out)>=limit: break
            for i in range(0, n-wlen+1):
                if any(covered[k] for k in range(i,i+wlen)): continue
                phrase = " ".join(toks[i:i+wlen])
                key = soft_norm(phrase)
                if key in self.index:
                    en, zh = self.index[key]
                    if en not in out:
                        out[en] = zh
                        mark(i, i+wlen)
                        if len(out)>=limit: break
        return out

def load_glossary_csv_text(csv_text: Optional[str]) -> List[Tuple[str,str]]:
    if not csv_text: return []
    rdr = csv.DictReader(io.StringIO(csv_text))
    if not rdr.fieldnames: return []
    col_en = None; col_zh = None
    for c in rdr.fieldnames:
        cc = (c or "").strip()
        if cc in ("en", "英文名稱"): col_en = c
        if cc in ("zh", "中文名稱"): col_zh = c
    if not col_en or not col_zh:
        _log_print("[glossary] 無 en/zh 欄（或 英文名稱/中文名稱），略過。")
        return []
    seen = set(); pairs=[]
    for row in rdr:
        en = (row.get(col_en) or "").strip()
        zh = (row.get(col_zh) or "").strip()
        if en and zh and en not in seen:
            pairs.append((en, zh)); seen.add(en)
    return pairs

# ---------- OpenAI-compatible Chat Completions ----------
async def call_chat_completions_batch_pyfetch(api_key: str, base_url: str, model: str,
                                              masked_texts: List[str], glossaries: List[Dict[str,str]]):
    items = []
    for i, (t, g) in enumerate(zip(masked_texts, glossaries)):
        items.append({"id": i, "text": t, "glossary": [f"{en} -> {zh}" for en, zh in g.items()]})
    system_prompt = (
        "你是台灣 GIS 在地化譯者，將多個獨立英文片段翻為自然專業的繁體中文（台灣）。\n"
        "必守規則：\n"
        "• 保留並原樣輸出所有 ⟦MASK數字⟧ 片段；不可增刪或改動。\n"
        "• 不得輸出任何解釋、標題、程式碼框或多餘文字。\n"
        "• 請『只輸出』一個 JSON 陣列（字串陣列），長度必須與輸入 items 相同，且依原順序對應。\n"
        "• Glossary 僅供參考；若不自然可忽略。\n"
        "• 不要改動任何 HTML 標籤或 HTML 實體。"
    )
    user_prompt = (
        "請逐一翻譯下列 items。每個 item：{\"id\":<序號>,\"text\":\"<含遮罩>\",\"glossary\":[\"en -> zh\",...]}\n\n"
        "請『只輸出』一個 JSON 陣列，例如：[\"譯文0\",\"譯文1\",...]\n\n"
        f"items = {json.dumps(items, ensure_ascii=False)}"
    )
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {
        "model": model,
        "messages": [{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],
        "temperature": 0.2,
        "max_tokens": max(512, 200*max(4, len(masked_texts))),
    }
    resp = await PYODIDE_FETCH(base_url.rstrip('/') + "/chat/completions",
                               method="POST", headers=headers, body=json.dumps(body))
    data = await resp.json()
    if resp.status >= 400:
        raise RuntimeError(f"API Error {resp.status}: {data}")
    raw = (data["choices"][0]["message"]["content"] or "").strip()
    return _parse_json_list_strict(raw)

def _parse_json_list_strict(s: str) -> List[str]:
    try:
        arr = json.loads(s)
        if isinstance(arr, list) and all(isinstance(x, str) for x in arr):
            return arr
    except Exception:
        pass
    lb = s.find('['); rb = s.rfind(']')
    if 0 <= lb < rb:
        chunk = s[lb:rb+1]
        arr = json.loads(chunk)
        if isinstance(arr, list) and all(isinstance(x, str) for x in arr):
            return arr
    raise ValueError("模型輸出非純 JSON 字串陣列")

def http_post_requests(url: str, headers: Dict[str,str], body: Dict) -> Dict:
    try:
        import requests
        r = requests.post(url, headers=headers, json=body, timeout=120)
        r.raise_for_status()
        return r.json()
    except Exception:
        # urllib fallback
        import urllib.request, urllib.error
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'),
                                     headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=120) as f:
                return json.loads(f.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTPError {e.code}: {e.read().decode('utf-8', 'ignore')}")

def call_chat_completions_batch_requests(api_key: str, base_url: str, model: str,
                                         masked_texts: List[str], glossaries: List[Dict[str,str]]) -> List[str]:
    items = []
    for i, (t, g) in enumerate(zip(masked_texts, glossaries)):
        items.append({"id": i, "text": t, "glossary": [f"{en} -> {zh}" for en, zh in g.items()]})
    system_prompt = (
        "你是台灣 GIS 在地化譯者，將多個獨立英文片段翻為自然專業的繁體中文（台灣）。\n"
        "必守規則：\n"
        "• 保留並原樣輸出所有 ⟦MASK數字⟧ 片段；不可增刪或改動。\n"
        "• 不得輸出任何解釋、標題、程式碼框或多餘文字。\n"
        "• 請『只輸出』一個 JSON 陣列（字串陣列），長度必須與輸入 items 相同，且依原順序對應。\n"
        "• Glossary 僅供參考；若不自然可忽略。\n"
        "• 不要改動任何 HTML 標籤或 HTML 實體。"
    )
    user_prompt = (
        "請逐一翻譯下列 items。每個 item：{\"id\":<序號>,\"text\":\"<含遮罩>\",\"glossary\":[\"en -> zh\",...]}\n\n"
        "請『只輸出』一個 JSON 陣列，例如：[\"譯文0\",\"譯文1\",...]\n\n"
        f"items = {json.dumps(items, ensure_ascii=False)}"
    )
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {
        "model": model,
        "messages": [{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],
        "temperature": 0.2,
        "max_tokens": max(512, 200*max(4, len(masked_texts))),
    }
    data = http_post_requests(base_url.rstrip('/') + "/chat/completions", headers, body)
    raw = (data["choices"][0]["message"]["content"] or "").strip()
    return _parse_json_list_strict(raw)

# ---------- 主流程（共用） ----------
def run_translation_pipeline(api_key: str, base_url: str, model: str,
                             ts_text: str, glossary_csv_text: Optional[str],
                             batch_size: int = 16, limit_n: int = 50) -> bytes:
    doctype = _read_doctype(ts_text)
    root = ET.fromstring(ts_text)
    messages = root.findall(".//message")
    pairs = load_glossary_csv_text(glossary_csv_text)
    gindex = GlossaryIndex(pairs)
    print(f"🔎 message 總數：{len(messages)}；將處理：{limit_n}；batch={batch_size}")
    if pairs:
        print(f"📘 glossary 條目：{len(pairs)}")
    else:
        print("📘 無 glossary（可提供 CSV）")

    tasks = []
    for m in messages:
        src_el = m.find("source")
        if src_el is None or src_el.text is None: continue
        if needs_translation(src_el.text):
            tasks.append((m, src_el.text, m.get("numerus")=="yes"))
        if len(tasks) >= limit_n: break

    finished = 0
    total = len(tasks)
    for start in range(0, total, batch_size):
        batch = tasks[start:start+batch_size]
        glossaries, masked_texts, maps = [], [], []
        for _, src_text, _ in batch:
            glossaries.append(gindex.build_for_text(src_text, limit=12))
            masked, mp = _mask_text(src_text)
            masked_texts.append(masked); maps.append(mp)

        try:
            if PYODIDE_FETCH is not None:
                zh_list = asyncio.get_event_loop().run_until_complete(
                    call_chat_completions_batch_pyfetch(api_key, base_url, model, masked_texts, glossaries)
                )
            else:
                zh_list = call_chat_completions_batch_requests(api_key, base_url, model, masked_texts, glossaries)
        except Exception as e:
            print(f"[{start+1}..{start+len(batch)}] 批次失敗，改逐筆：{e}")
            zh_list = []
            for masked, g in zip(masked_texts, glossaries):
                try:
                    if PYODIDE_FETCH is not None:
                        single = asyncio.get_event_loop().run_until_complete(
                            call_chat_completions_batch_pyfetch(api_key, base_url, model, [masked], [g])
                        )
                    else:
                        single = call_chat_completions_batch_requests(api_key, base_url, model, [masked], [g])
                    zh_list.append(single[0])
                except Exception as ee:
                    idx = len(zh_list)
                    zh_list.append(batch[idx][1])  # 回原文
                    print(f"  └ 逐筆失敗，回原文：{ee}")

        for (m, src_text, is_num), zh_raw, mp in zip(batch, zh_list, maps):
            trans_el = m.find("translation")
            if trans_el is None:
                trans_el = ET.SubElement(m, "translation")
            zh = _unmask_text(zh_raw, mp)
            zh = _et_ready(zh)
            if is_num:
                forms = trans_el.findall("numerusform")
                if not forms:
                    forms = [ET.SubElement(trans_el, "numerusform")]
                for f in forms: f.text = zh
            else:
                trans_el.text = zh
            if "type" in trans_el.attrib:
                trans_el.attrib.pop("type", None)
            finished += 1
            print(f"[{finished}/{total}] {repr(src_text[:60])} -> {repr(zh[:60])}")

    xml_bytes = ET.tostring(root, encoding="utf-8")
    header = b'<?xml version="1.0" encoding="utf-8"?>'
    if doctype:
        xml_bytes = header + ("\n"+doctype+"\n").encode("utf-8") + xml_bytes
    else:
        xml_bytes = header + b"\n" + xml_bytes
    return xml_bytes

# ---------- JS 版（頁面 UI） ----------
async def _run_with_js_ui():
    from js import document
    # 產生簡單 UI
    html_ui = """
    <div id="tsapp" style="font-family: system-ui; line-height:1.35">
      <div style="margin-bottom:.5rem;">
        <label>API Key：<input type="password" id="apiKey" placeholder="sk-..." style="width:320px"></label>
        <label style="margin-left:12px;">Base URL：<input type="text" id="baseUrl" value="https://api.openai.com/v1" style="width:360px"></label>
        <label style="margin-left:12px;">Model：<input type="text" id="model" value="gpt-4.1-mini" style="width:200px"></label>
      </div>
      <div style="margin-bottom:.5rem;">
        <label>Batch：<input type="number" id="batch" value="16" min="1" max="64"></label>
        <label style="margin-left:12px;">處理筆數上限：<input type="number" id="limitN" value="50" min="1"></label>
      </div>
      <div style="margin-bottom:.5rem;">
        <label>.ts 檔：<input type="file" id="tsFile" accept=".ts"></label>
        <label style="margin-left:12px;">glossary（CSV：en,zh 或 英文名稱,中文名稱）：<input type="file" id="glsFile" accept=".csv"></label>
        <button id="run-btn" style="margin-left:12px;">Run</button>
      </div>
      <div id="dl"></div>
      <pre id="log" style="background:#111;color:#eee;padding:8px;max-height:280px;overflow:auto;border-radius:6px;"></pre>
    </div>
    """
    if DISPLAY_HTML: DISPLAY_HTML(html_ui)
    else: print("(HTML 顯示不可用)")

    # 綁定事件
    from pyodide.ffi import to_py, create_proxy
    from pyodide.http import pyfetch

    async def read_file_text(input_id: str) -> Optional[str]:
        files = document.getElementById(input_id).files
        if not files or files.length == 0:
            return None
        f = files.item(0)
        buf = await f.arrayBuffer()
        data = to_py(buf)
        return bytes(data).decode("utf-8", errors="ignore")

    async def handle_run(evt=None):
        try:
            document.getElementById("dl").innerHTML = ""
            document.getElementById("log").textContent = ""
            def log(s): 
                el = document.getElementById("log")
                el.textContent += str(s) + "\n"
                el.scrollTop = el.scrollHeight
            api = document.getElementById("apiKey").value.strip()
            if not api: 
                log("請先輸入 API Key"); return
            ts_text = await read_file_text("tsFile")
            if not ts_text: 
                log("請先上傳 .ts 檔"); return
            gls_text = await read_file_text("glsFile")

            B = int(document.getElementById("batch").value or "16")
            N = int(document.getElementById("limitN").value or "50")
            xml_bytes = run_translation_pipeline(
                api_key=api,
                base_url=document.getElementById("baseUrl").value,
                model=document.getElementById("model").value,
                ts_text=ts_text,
                glossary_csv_text=gls_text,
                batch_size=B,
                limit_n=N
            )
            # 下載連結
            out_name = "translated_zh-Hant.ts"
            files = document.getElementById("tsFile").files
            if files and files.length>0:
                nm = files.item(0).name
                if nm.lower().endswith(".ts"):
                    out_name = re.sub(r"\.ts$", "", nm) + "_zh-Hant.ts"
            link = _build_download_link(out_name, xml_bytes)
            document.getElementById("dl").innerHTML = link
            log("✅ 完成，已產生下載連結。")
        except Exception as e:
            traceback.print_exc()
            print(e)

    document.getElementById("run-btn").addEventListener("click", create_proxy(lambda evt: asyncio.ensure_future(handle_run(evt))))

# ---------- Console 版（無 js） ----------
def _run_with_console():
    print("（偵測不到瀏覽器 js；改用主控台互動）")
    api = getpass("API Key: ").strip()
    base_url = input("Base URL [https://api.openai.com/v1]: ").strip() or "https://api.openai.com/v1"
    model = input("Model [gpt-4.1-mini]: ").strip() or "gpt-4.1-mini"
    batch = input("Batch size [16]: ").strip() or "16"
    limitN = input("處理筆數上限 [50]: ").strip() or "50"
    src = input("來源 .ts 檔路徑（必填）: ").strip()
    gls = input("glossary CSV 路徑（可留白）: ").strip()

    if not os.path.exists(src):
        print(f"找不到檔案：{src}")
        return
    ts_text = open(src, "r", encoding="utf-8", errors="ignore").read()
    gls_text = open(gls, "r", encoding="utf-8", errors="ignore").read() if gls and os.path.exists(gls) else None

    xml_bytes = run_translation_pipeline(
        api_key=api,
        base_url=base_url,
        model=model,
        ts_text=ts_text,
        glossary_csv_text=gls_text,
        batch_size=int(batch),
        limit_n=int(limitN)
    )
    out_name = re.sub(r"\.ts$", "", os.path.basename(src)) + "_zh-Hant.ts"
    with open(out_name, "wb") as f:
        f.write(xml_bytes)
    print(f"✅ 完成，輸出：{out_name}")
    if DISPLAY_HTML:
        DISPLAY_HTML("<hr/>" + _build_download_link(out_name, xml_bytes))

# ---------- 執行 ----------
try:
    if JS_AVAILABLE and PYODIDE_FETCH is not None:
        asyncio.get_event_loop().run_until_complete(_run_with_js_ui())
    else:
        _run_with_console()
except Exception as e:
    traceback.print_exc()
    print("初始化失敗：", e)