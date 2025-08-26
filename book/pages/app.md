---
title: App
---

# App

```{replite}
:kernel: python
:height: 680px
import asyncio, json, re, io, base64, traceback
from typing import List, Tuple, Dict, Optional
from xml.etree import ElementTree as ET
from IPython.display import display, HTML
from js import document
from pyodide.ffi import to_py, create_proxy
from pyodide.http import pyfetch

# ---------------- UI ----------------
html_ui = """
<div id="tsapp" style="font-family: system-ui; line-height:1.35">
  <div style="margin-bottom:.5rem;">
    <label>API Key：
      <input type="password" id="apiKey" placeholder="sk-..." style="width:320px">
    </label>
    <label style="margin-left:12px;">Base URL：
      <input type="text" id="baseUrl" value="https://api.openai.com/v1" style="width:360px">
    </label>
    <label style="margin-left:12px;">Model：
      <input type="text" id="model" value="gpt-4.1-mini" style="width:200px">
    </label>
  </div>
  <div style="margin-bottom:.5rem;">
    <label>Batch：
      <input type="number" id="batch" value="16" min="1" max="64">
    </label>
    <label style="margin-left:12px;">處理筆數上限：
      <input type="number" id="limitN" value="50" min="1">
    </label>
  </div>
  <div style="margin-bottom:.5rem;">
    <label>.ts 檔：
      <input type="file" id="tsFile" accept=".ts">
    </label>
    <label style="margin-left:12px;">glossary（CSV：en,zh 或 英文名稱,中文名稱）：
      <input type="file" id="glsFile" accept=".csv,.ods">
    </label>
    <button id="run-btn" style="margin-left:12px;">Run</button>
  </div>
  <div id="dl"></div>
  <pre id="log" style="background:#111;color:#eee;padding:8px;max-height:280px;overflow:auto;border-radius:6px;"></pre>
</div>
"""
display(HTML(html_ui))

def log(msg: str):
    el = document.getElementById("log")
    el.textContent += str(msg) + "\n"
    el.scrollTop = el.scrollHeight

def set_download(filename: str, content_bytes: bytes):
    b64 = base64.b64encode(content_bytes).decode("utf-8")
    href = f'data:application/octet-stream;base64,{b64}'
    document.getElementById("dl").innerHTML = (
        f'<a download="{filename}" href="{href}">⬇️ 下載 {filename}</a>'
    )

async def read_file_text(input_id: str) -> Optional[str]:
    files = document.getElementById(input_id).files
    if not files or files.length == 0:
        return None
    f = files.item(0)
    buf = await f.arrayBuffer()
    data = to_py(buf)
    return bytes(data).decode("utf-8", errors="ignore")

# -------------- Glossary（CSV） --------------
def load_glossary_csv(csv_text: Optional[str]) -> List[Tuple[str, str]]:
    if not csv_text:
        return []
    import csv
    rows: List[Tuple[str,str]] = []
    rdr = csv.DictReader(io.StringIO(csv_text))
    if not rdr.fieldnames:
        return []
    # 欄位對應
    col_en = None; col_zh = None
    for c in rdr.fieldnames:
        cc = (c or "").strip()
        if cc in ("en", "英文名稱"): col_en = c
        if cc in ("zh", "中文名稱"): col_zh = c
    if not col_en or not col_zh:
        log("[glossary] 找不到 en/zh 欄位（或 英文名稱/中文名稱），已略過。")
        return []
    seen = set()
    for row in rdr:
        en = (row.get(col_en) or "").strip()
        zh = (row.get(col_zh) or "").strip()
        if en and zh and en not in seen:
            rows.append((en, zh))
            seen.add(en)
    return rows

# -------------- 遮罩/還原（與你原版一致） --------------
_MASK_PAT = re.compile(
    r'('
    r'</?[A-Za-z][^>]*>'
    r'|&lt;/?[A-Za-z][^&]*?&gt;'
    r'|%L\\d+'
    r'|%\\d+'
    r'|%n'
    r'|\\{\\d+\\}'
    r'|&(?:[A-Za-z]+|#\\d+|#x[0-9A-Fa-f]+);'
    r')',
    flags=re.IGNORECASE
)

def _mask_text(s: str) -> Tuple[str, Dict[str, str]]:
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
    import html as _html
    try: return _html.unescape(s)
    except Exception: return s

def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip(): return False
    if re.fullmatch(r"[\\s\\d\\W%{}]+", en_text): return False
    return True

# -------------- LCS-ish glossary（無 pandas 版） --------------
_SEP_RE = re.compile(r"[\\s/_\\-.]+")
def soft_norm(s: str) -> str:
    return _SEP_RE.sub(" ", s.lower()).strip()

_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[\\/_.-][A-Za-z0-9]+)*")

class GlossaryIndex:
    def __init__(self, pairs: List[Tuple[str,str]]):
        self.index: Dict[str, Tuple[str,str]] = {}
        self.max_soft_len = 1
        for en, zh in pairs:
            key = soft_norm(en)
            self.index[key] = (en, zh)
            self.max_soft_len = max(self.max_soft_len, len(key.split()))
    def build_for_text(self, text: str, limit: int = 12) -> Dict[str,str]:
        if not self.index: return {}
        text_clean = _MASK_PAT.sub(" ", text)
        toks = [t.lower() for t in _TOKEN_RE.findall(text_clean)]
        n = len(toks)
        covered = [False]*n
        out: Dict[str,str] = {}
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

# -------------- Chat Completions（批次，一次回傳 JSON 陣列） --------------
async def call_chat_completions_batch(masked_texts: List[str], glossaries: List[Dict[str,str]]):
    assert len(masked_texts)==len(glossaries)
    items = []
    for i,(t,g) in enumerate(zip(masked_texts, glossaries)):
        hints = [f"{en} -> {zh}" for en,zh in g.items()]
        items.append({"id": i, "text": t, "glossary": hints})

    system_prompt = (
        "你是台灣 GIS 在地化譯者，將多個獨立英文片段翻為自然專業的繁體中文（台灣）。\\n"
        "必守規則：\\n"
        "• 保留並原樣輸出所有 ⟦MASK數字⟧ 片段；不可增刪或改動。\\n"
        "• 不得輸出任何解釋、標題、程式碼框或多餘文字。\\n"
        "• 請『只輸出』一個 JSON 陣列（字串陣列），長度必須與輸入 items 相同，且依原順序對應。\\n"
        "• Glossary 僅供參考；若不自然可忽略。\\n"
        "• 不要改動任何 HTML 標籤或 HTML 實體。"
    )
    user_prompt = (
        "請逐一翻譯下列 items。每個 item：{\\\"id\\\":<序號>,\\\"text\\\":\\\"<含遮罩的英文>\\\",\\\"glossary\\\":[\\\"en -> zh\\\",...]}\\n\\n"
        "請『只輸出』一個 JSON 陣列，例如：[\\\"譯文0\\\",\\\"譯文1\\\",...]\\n\\n"
        f"items = {json.dumps(items, ensure_ascii=False)}"
    )

    headers = {
        "Authorization": f"Bearer {document.getElementById('apiKey').value}",
        "Content-Type": "application/json",
    }
    body = {
        "model": document.getElementById("model").value,
        "messages": [
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": max(512, 200*max(4, len(masked_texts))),
    }
    url = document.getElementById("baseUrl").value.rstrip("/") + "/chat/completions"
    resp = await pyfetch(url, method="POST", headers=headers, body=json.dumps(body))
    data = await resp.json()
    if resp.status >= 400:
        raise RuntimeError(f"API Error {resp.status}: {data}")
    raw = (data["choices"][0]["message"]["content"] or "").strip()

    # 嚴格 JSON 解析
    def _parse_json_list(s: str):
        try:
            arr = json.loads(s)
            if isinstance(arr, list) and all(isinstance(x, str) for x in arr): return arr
        except Exception:
            pass
        lb = s.find('['); rb = s.rfind(']')
        if 0 <= lb < rb:
            chunk = s[lb:rb+1]
            arr = json.loads(chunk)
            if isinstance(arr, list) and all(isinstance(x, str) for x in arr): return arr
        raise ValueError("模型輸出非純 JSON 字串陣列")
    return _parse_json_list(raw)

# -------------- 主流程 --------------
def _read_doctype(xml_text: str) -> str:
    m = re.search(r'<!DOCTYPE[^>]+>', xml_text)
    return m.group(0) if m else ""

async def run_pipeline(evt=None):
    try:
        document.getElementById("dl").innerHTML = ""
        document.getElementById("log").textContent = ""

        api = document.getElementById("apiKey").value.strip()
        if not api:
            log("請先輸入 API Key"); return
        ts_text = await read_file_text("tsFile")
        if not ts_text:
            log("請先上傳 .ts 檔"); return

        gls_text = None
        files = document.getElementById("glsFile").files
        if files and files.length>0:
            name = files.item(0).name.lower()
            if name.endswith(".csv"):
                gls_text = await read_file_text("glsFile")
            elif name.endswith(".ods"):
                log("[glossary] 目前環境無 odfpy（ODS 解析），請先轉成 CSV。")

        pairs = load_glossary_csv(gls_text)
        gindex = GlossaryIndex(pairs)
        if pairs:
            log(f"📘 glossary 條目：{len(pairs)}")
        else:
            log("📘 無 glossary（可上傳 CSV）")

        doctype = _read_doctype(ts_text)
        root = ET.fromstring(ts_text)
        messages = root.findall(".//message")

        limitN = int(document.getElementById("limitN").value or "50")
        to_do = []
        for m in messages:
            src = m.find("source")
            if src is None or src.text is None: continue
            if needs_translation(src.text):
                to_do.append((m, src.text, m.get("numerus") == "yes"))
            if len(to_do) >= limitN: break

        log(f"🔎 共 {len(messages)} 則 message，將處理 {len(to_do)} 則；Batch={document.getElementById('batch').value}")

        B = max(1, int(document.getElementById("batch").value or "16"))
        finished = 0
        total = len(to_do)

        for start in range(0, total, B):
            batch = to_do[start:start+B]
            glossaries, masked_texts, maps = [], [], []
            for _, src_text, _ in batch:
                g = gindex.build_for_text(src_text, limit=12)
                glossaries.append(g)
                masked, mp = _mask_text(src_text)
                masked_texts.append(masked); maps.append(mp)

            try:
                zh_list = await call_chat_completions_batch(masked_texts, glossaries)
            except Exception as e:
                log(f"[{start+1}..{start+len(batch)}] 批次失敗，改逐筆：{e}")
                zh_list = []
                for masked, g in zip(masked_texts, glossaries):
                    try:
                        single = await call_chat_completions_batch([masked],[g])
                        zh_list.append(single[0])
                    except Exception as ee:
                        # 回原文
                        idx = len(zh_list)
                        zh_list.append(batch[idx][1])
                        log(f"  └ 逐筆失敗，回原文：{ee}")

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
                log(f"[{finished}/{total}] {repr(src_text[:60])} -> {repr(zh[:60])}")
            await asyncio.sleep(0)

        xml_bytes = ET.tostring(root, encoding="utf-8")
        header = b'<?xml version="1.0" encoding="utf-8"?>'
        if doctype:
            xml_bytes = header + ("\n"+doctype+"\n").encode("utf-8") + xml_bytes
        else:
            xml_bytes = header + b"\n" + xml_bytes

        # 檔名：原名加 _zh-Hant
        ts_files = document.getElementById("tsFile").files
        out_name = "translated_zh-Hant.ts"
        if ts_files and ts_files.length>0:
            name = ts_files.item(0).name
            out_name = re.sub(r"\\.ts$", "", name) + "_zh-Hant.ts"

        set_download(out_name, xml_bytes)
        log("✅ 完成，已產生下載連結。")

    except Exception as e:
        log("發生錯誤： " + str(e))
        traceback.print_exc()

# 綁定按鈕
document.getElementById("run-btn").addEventListener("click", create_proxy(lambda evt: asyncio.ensure_future(run_pipeline(evt))))
```
