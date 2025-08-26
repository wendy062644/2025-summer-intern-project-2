---
title: App
---

# App

```{replite}
import piplite
await piplite.install("ipywidgets")

:kernel: python
:height: 580px
import asyncio, json, re, os, html, glob, io, base64, traceback
from typing import List, Tuple, Dict, Optional

import ipywidgets as w
from IPython.display import display

# 試著載入可用套件（Pyodide 環境通常有 pandas，但 .ods 需要 odfpy；若沒有就支援 .csv）
try:
    import pandas as pd
except Exception:
    pd = None

import xml.etree.ElementTree as ET

# =========================
# UI
# =========================
api_key = w.Password(description='API Key:', placeholder='sk-...')
base_url = w.Text(value='https://api.openai.com/v1', description='Base URL:')
model    = w.Text(value='gpt-4.1-mini', description='Model:')
batchsz  = w.IntSlider(value=16, min=1, max=64, step=1, description='Batch:')
limit_n  = w.IntText(value=50, description='處理筆數上限:')

ts_upl   = w.FileUpload(accept='.ts', multiple=False, description='上傳 .ts')
gls_upl  = w.FileUpload(accept='.ods,.csv', multiple=False, description='glossary(選用)')

run_btn  = w.Button(description='Run', button_style='primary')
out      = w.Output()

display(
    w.VBox([
        w.HBox([api_key, base_url, model]),
        w.HBox([batchsz, limit_n]),
        w.HBox([ts_upl, gls_upl]),
        run_btn,
        out
    ])
)

# =========================
# 工具與流程（依你的原始邏輯精簡調整為瀏覽器可跑）
# =========================
# 遮罩/還原（HTML/placeholder/實體保護）
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
def _mask_text(s: str) -> Tuple[str, Dict[str, str]]:
    idx = 0
    mapping: Dict[str, str] = {}
    def _repl(m):
        nonlocal idx
        key = f"⟦MASK{idx}⟧"
        mapping[key] = m.group(0)
        idx += 1
        return key
    masked = _MASK_PAT.sub(_repl, s)
    return masked, mapping

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
    if not en_text or not en_text.strip():
        return False
    if re.fullmatch(r"[\s\d\W%{}]+", en_text):
        return False
    return True

# LCS/glossary（句子優先 + 單字前綴），用較輕量寫法
_SEP_RE = re.compile(r'[\s/_\-.]+')
def soft_norm(s: str) -> str:
    return _SEP_RE.sub(' ', s.lower()).strip()

class LCSMatcher:
    _TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[\/_.-][A-Za-z0-9]+)*")
    def __init__(self, df):
        # df: 需有 'en','zh'
        if df is None or df.empty:
            self.lookup = None
            self.soft_index = {}
            self.max_soft_len = 1
            return
        self.lookup = df.copy()
        self.lookup["en_soft"] = self.lookup["en"].map(soft_norm)
        self.soft_index = {}
        for _, row in self.lookup.iterrows():
            key = row["en_soft"]
            if key not in self.soft_index:
                self.soft_index[key] = (row["en"], row["zh"])
        self.max_soft_len = max((len(x.split()) for x in self.lookup["en_soft"]), default=1)

    def build_glossary_sentence_first(self, text: str, limit: int = 12) -> Dict[str, str]:
        if not self.lookup is not None:
            return {}
        text_clean = re.sub(_MASK_PAT, " ", text)
        tokens = self._TOKEN_RE.findall(text_clean)
        toks_lc = [t.lower() for t in tokens]
        n = len(toks_lc)
        covered = [False] * n
        glossary: Dict[str, str] = {}
        def _mark(i: int, j: int):
            for k in range(i, j): covered[k] = True
        win_max = min(n, getattr(self, "max_soft_len", n))
        for wlen in range(win_max, 0, -1):
            if len(glossary) >= limit: break
            for i in range(0, n - wlen + 1):
                if any(covered[k] for k in range(i, i + wlen)): continue
                phrase = " ".join(toks_lc[i:i + wlen])
                key = soft_norm(phrase)
                if key in self.soft_index:
                    en, zh = self.soft_index[key]
                    if en not in glossary:
                        glossary[en] = zh
                        _mark(i, i + wlen)
                        if len(glossary) >= limit: break
        return glossary

def _read_doctype(xml_text: str) -> str:
    m = re.search(r'<!DOCTYPE[^>]+>', xml_text)
    return m.group(0) if m else ""

def load_glossary_from_upload(upl: w.FileUpload):
    if (pd is None) or (upl is None) or (len(upl.value)==0):
        return None
    # 僅取第一個檔
    meta = list(upl.value.values())[0]
    name = meta['metadata']['name']
    content = meta['content']  # bytes
    bio = io.BytesIO(content)

    if name.lower().endswith('.csv'):
        try:
            df = pd.read_csv(bio)
            df = df.rename(columns={c: c.strip() for c in df.columns})
            if 'en' in df.columns and 'zh' in df.columns:
                df = df[['en','zh']].dropna().drop_duplicates(subset=['en'])
                return df
        except Exception as e:
            with out:
                print(f"[glossary] CSV 讀取失敗：{e}")
        return None

    if name.lower().endswith('.ods'):
        try:
            # 需要 odfpy 引擎；若環境沒有會丟例外
            df = pd.read_excel(bio, engine='odf')
            df = df.rename(columns={c: c.strip() for c in df.columns})
            if "英文名稱" in df.columns and "中文名稱" in df.columns:
                sub = df[["英文名稱", "中文名稱"]].copy()
                sub.columns = ["en", "zh"]
                sub = sub.dropna().drop_duplicates(subset=['en'])
                return sub
            elif 'en' in df.columns and 'zh' in df.columns:
                sub = df[['en','zh']].dropna().drop_duplicates(subset=['en'])
                return sub
            else:
                with out:
                    print("[glossary] ODS 缺少必要欄位（需「英文名稱」「中文名稱」或 en/zh）")
        except Exception as e:
            with out:
                print(f"[glossary] ODS 讀取失敗（可能缺 odfpy）：{e}")
        return None

    with out:
        print("[glossary] 僅支援 .ods 或 .csv")
    return None

async def call_chat_completions_batch(masked_texts: List[str], glossaries: List[Dict[str,str]]):
    """
    單次呼叫模型，要求回傳等長的 JSON 陣列（字串），與你的原版邏輯一致。
    """
    assert len(masked_texts) == len(glossaries)
    items = []
    for i, (t, g) in enumerate(zip(masked_texts, glossaries)):
        hints = [f"{en} -> {zh}" for en, zh in g.items()]
        items.append({"id": i, "text": t, "glossary": hints})

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
        "請逐一翻譯下列 items。每個 item 格式如下：\n"
        "{ \"id\": <序號>, \"text\": \"<含遮罩的英文>\", \"glossary\": [\"en -> zh\", ...] }\n\n"
        "請『只輸出』一個 JSON 陣列，例如：\n"
        "[\"譯文0\", \"譯文1\", ...]\n\n"
        f"items = {json.dumps(items, ensure_ascii=False)}"
    )

    headers = {
        "Authorization": f"Bearer {api_key.value}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model.value,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        # 預留較大 max_tokens，避免長輸出被截斷
        "max_tokens": max(512, 200*max(4, len(masked_texts)))
    }

    # 用 pyodide 的 pyfetch（瀏覽器 fetch）。注意：可能受 CORS 影響。
    from pyodide.http import pyfetch
    resp = await pyfetch(
        f"{base_url.value.rstrip('/')}/chat/completions",
        method="POST",
        headers=headers,
        body=json.dumps(body),
    )
    data = await resp.json()
    if resp.status >= 400:
        raise RuntimeError(f"API Error {resp.status}: {data}")
    raw = (data["choices"][0]["message"]["content"] or "").strip()

    # 嚴格解析成 list[str]
    def _parse_json_list(s: str):
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
    return _parse_json_list(raw)

def build_download_link(filename: str, content_bytes: bytes) -> str:
    b64 = base64.b64encode(content_bytes).decode('utf-8')
    return f'<a download="{filename}" href="data:application/octet-stream;base64,{b64}">⬇️ 下載 {filename}</a>'

async def run_pipeline(_):
    out.clear_output()
    try:
        if not api_key.value.strip():
            with out:
                print("請先輸入 API Key")
            return
        if len(ts_upl.value) == 0:
            with out:
                print("請先上傳 .ts 檔")
            return

        # 讀取 TS
        ts_meta = list(ts_upl.value.values())[0]
        ts_name = ts_meta['metadata']['name']
        ts_text = ts_meta['content'].decode('utf-8', errors='ignore')
        doctype = _read_doctype(ts_text)
        root = ET.fromstring(ts_text)
        messages = root.findall(".//message")

        # glossary
        df_gls = load_glossary_from_upload(gls_upl) if pd is not None else None
        matcher = LCSMatcher(df_gls)

        with out:
            print(f"🔎 共 {len(messages)} 則 <message>，將處理前 {limit_n.value} 則（可調整『處理筆數上限』）。")
            if df_gls is not None:
                print(f"📘 glossary 條目數：{len(df_gls)}")
            else:
                print("📘 無 glossary（可上傳 .csv 或 .ods）")

        # 擷取需翻譯任務
        tasks = []
        for m in messages:
            src_el = m.find("source")
            if src_el is None or src_el.text is None:
                continue
            if needs_translation(src_el.text):
                tasks.append((m, src_el.text, m.get("numerus") == "yes"))
            if len(tasks) >= limit_n.value:
                break

        finished = 0
        total = len(tasks)

        # 批次處理
        for start in range(0, total, batchsz.value):
            batch = tasks[start:start+batchsz.value]
            glossaries, masked_texts, maps = [], [], []
            for _, src_text, _ in batch:
                g = matcher.build_glossary_sentence_first(src_text, limit=12) if matcher.lookup is not None else {}
                glossaries.append(g)
                masked, mp = _mask_text(src_text)
                masked_texts.append(masked)
                maps.append(mp)

            try:
                zh_list = await call_chat_completions_batch(masked_texts, glossaries)
            except Exception as e:
                with out:
                    print(f"[{start+1}..{start+len(batch)}] 批次失敗：{e}")
                # 改逐筆（保守）
                zh_list = []
                for (m, src_text, _), masked, g in zip(batch, masked_texts, glossaries):
                    try:
                        one = await call_chat_completions_batch([masked],[g])
                        zh_list.append(one[0])
                    except Exception as ee:
                        with out:
                            print(f"  └ 逐筆失敗，回原文：{ee}")
                        zh_list.append(src_text)

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
                    for f in forms:
                        f.text = zh
                else:
                    trans_el.text = zh
                if "type" in trans_el.attrib:
                    trans_el.attrib.pop("type", None)
                finished += 1
                with out:
                    print(f"[{finished}/{total}] {repr(src_text[:60])} -> {repr(zh[:60])}")

        # 寫回（保留宣告與 DOCTYPE）
        xml_bytes = ET.tostring(root, encoding="utf-8")
        header = b'<?xml version="1.0" encoding="utf-8"?>'
        if doctype:
            xml_bytes = header + ("\n"+doctype+"\n").encode("utf-8") + xml_bytes
        else:
            xml_bytes = header + b"\n" + xml_bytes

        # 檔名
        out_name = re.sub(r'\.ts$', '', ts_name) + "_zh-Hant.ts"
        link_html = build_download_link(out_name, xml_bytes)
        with out:
            from IPython.display import HTML
            display(HTML(f"<hr/>{link_html}"))
            print("✅ 完成（上面連結可下載結果）")

    except Exception as e:
        with out:
            print("發生錯誤：", e)
            traceback.print_exc()

run_btn.on_click(lambda _: asyncio.ensure_future(run_pipeline(_)))
```
