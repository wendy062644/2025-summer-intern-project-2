---
title: App
thebe: false
---

# App

<!-- ===== 外層 UI（你原本的結構） ===== -->
<div id="ts-ui" style="font-family: system-ui; line-height:1.35; margin: 8px 0 16px;">
  <div style="margin-bottom:.5rem;">
    <label>API Key：
      <input type="password" id="apiKey" placeholder="sk-..." style="width:320px">
    </label>
    <label style="margin-left:12px;">Base URL：
      <input type="text" id="baseUrl" value="https://api.openai.com/v1" style="width:360px">
    </label>
    <label style="margin-left:12px;">Model：
      <select id="modelSel" style="width:220px">
        <option value="gpt-4.1-mini" selected>gpt-4.1-mini（便宜）</option>
        <option value="gpt-4.1">gpt-4.1</option>
        <option value="gpt-4o-mini">gpt-4o-mini</option>
        <option value="gpt-4o">gpt-4o</option>
        <option value="o4-mini">o4-mini（推理）</option>
      </select>
    </label>
  </div>
  <div style="margin-bottom:.5rem;">
    <label>Batch：
      <input type="number" id="batch" value="32" min="1" max="64">
    </label>
    <label style="margin-left:12px;">處理筆數上限：
      <input type="number" id="limitN" value="200" min="1">
    </label>
  </div>
  <div style="margin-bottom:.5rem;">
    <label>.ts 檔（上傳）：
      <input type="file" id="tsFile" accept=".ts">
    </label>
    <label style="margin-left:12px;">glossary（CSV/ODS；欄：en,zh 或 英文名稱,中文名稱）：
      <input type="file" id="glsFile" accept=".csv,.ods" multiple>
    </label>
    <button id="run-btn" style="margin-left:12px;">執行翻譯</button>
  </div>
  <div id="ts-ui-msg" style="color:#555; font-size: 0.95rem;"></div>
</div>

<!-- ===== Pyodide ===== -->
<script type="module">
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.mjs";
const pyodide = await loadPyodide();

const $msg = document.getElementById("ts-ui-msg");
try {
  await pyodide.runPythonAsync(String.raw`
import asyncio, json, re, io, base64, traceback, html, csv, zipfile
from typing import List, Tuple, Dict, Optional
from xml.etree import ElementTree as ET
from js import document
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy

# ===== UI 訊息列 =====
def _set_ui_msg(msg_html: str):
    document.getElementById("ts-ui-msg").innerHTML = msg_html

# ===== 讀取上傳檔 =====
async def read_glossaries_from_file_input(input_id: str) -> List[Tuple[str,str]]:
    """
    從 <input type="file" multiple> 讀取多個 CSV/ODS，合併去重（以英文為 key）。
    """
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

    # 依英文去重（保留第一筆）
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
    if not en_text or not en_text.strip(): return False
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text): return False
    return True

# ===== LCS 詞庫匹配（改為不依賴 pandas）=====
_SEP_RE = re.compile(r"[\s/_\-.]+")
def soft_norm(s:str)->str: return _SEP_RE.sub(" ", s.lower()).strip()
_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[\\/_.-][A-Za-z0-9]+)*")

class LCSMatcher:
    def __init__(self, pairs: List[Tuple[str,str]], min_token_len:int=4, min_lcs_len:int=4):
        # 預處理
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
        # 句子優先：soft 索引
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

# ===== 讀 CSV / ODS（瀏覽器版）=====
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
            pairs.append((en, zh))
            seen.add(en)
    return pairs

def load_glossary_ods_bytes(ods_bytes: bytes)->List[Tuple[str,str]]:
    # 輕量解析 ODS/content.xml
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
            pairs.append((en, zh)); seen.add(en)
    return pairs

# ===== OpenAI Chat Completions（pyfetch；批次）=====
async def call_chat_completions_batch_pyfetch(api_key:str, base_url:str, model:str,
                                              masked_texts:List[str], glossaries:List[Dict[str,str]]):
    # 準備 items
    items=[]
    for i,(t,g) in enumerate(zip(masked_texts, glossaries)):
        items.append({"id": i, "text": t, "glossary": [f"{en} -> {zh}" for en, zh in g.items()]})

    system_prompt = """你是台灣 GIS 在地化譯者，將多個獨立英文片段翻為自然專業的繁體中文（台灣）。
    規則：
    • 保留所有 ⟦MASK數字⟧；
    • 不要解釋；
    • 不要改動任何 HTML 標籤或 HTML 實體；
    • 只輸出與輸入等長、同序的結果。"""
    user_prompt = "請逐一翻譯 items。只需回傳 function 參數，不要輸出其他文字。\n" + \
              "items = " + json.dumps(items, ensure_ascii=False)

    # 用 tools 定義明確 schema：必須回傳 translations: string[]
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

    # 讀取 tool call 的 arguments（是純 JSON）
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

# ===== 主流程（與你原本的一致，只是改成瀏覽器 I/O）=====
async def run_translation_pipeline_async(api_key:str, base_url:str, model:str,
                                         ts_text:str, glossary_pairs:List[Tuple[str,str]],
                                         batch_size:int=32, limit_n:int=200) -> bytes:
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
            # 退回逐筆（簡化：逐筆仍用同一 API 端點，但一次送一筆）
            zh_list=[]
            for masked, g in zip(masked_texts, glossaries):
                one = await call_chat_completions_batch_pyfetch(api_key, base_url, model, [masked], [g])
                zh_list.append(one[0])

        for (m, src_text, is_num), zh_raw, mp in zip(batch, zh_list, maps):
            trans = m.find("translation")
            if trans is None:
                trans = ET.SubElement(m, "translation")
            zh = _et_ready(_unmask_text(zh_raw, mp))
            if is_num:
                forms = trans.findall("numerusform")
                if not forms:
                    forms=[ET.SubElement(trans, "numerusform")]
                for f in forms:
                    f.text = zh
            else:
                trans.text = zh
            if "type" in trans.attrib: trans.attrib.pop("type", None)
            finished += 1

        _set_ui_msg(f"處理進度：{finished}/{total}")

    xml_bytes = ET.tostring(root, encoding="utf-8")
    head = b'<?xml version="1.0" encoding="utf-8"?>'
    if doctype: xml_bytes = head + ("\\n"+doctype+"\\n").encode("utf-8") + xml_bytes
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

        # 讀 glossary（CSV/ODS 皆可）
        pairs=[]
        pairs = await read_glossaries_from_file_input("glsFile")

        _set_ui_msg("⏳ 連線中…")
        xml_bytes = await run_translation_pipeline_async(
            api_key=api, base_url=base_url, model=model,
            ts_text=ts_text, glossary_pairs=pairs,
            batch_size=batch, limit_n=limitN
        )

        # 輸出檔名
        out_name = "qgis_zh-Hant.ts"
        ts_files = document.getElementById("tsFile").files
        if ts_files and ts_files.length>0:
            nm = ts_files.item(0).name
            if nm.lower().endswith(".ts"):
                out_name = re.sub(r"\\.ts$", "", nm) + "_zh-Hant.ts"

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