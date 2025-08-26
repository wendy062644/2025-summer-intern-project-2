
<hr/>

### `translate_app.md`
```markdown
# TS Translator App

> 按上方的 **⚡️ Live Code** 啟動互動模式（Thebe）。

<hr/>

## 1) 原始碼（翻譯引擎）

```{code-cell} ipython3
:tags: [hide-output]

# -*- coding: utf-8 -*-
"""
Qt .ts 翻譯（OpenAI ChatGPT API + LCS 詞彙提示 + HTML/佔位符遮罩保留）
強化版：去重、併發多批、批次 JSON 輸出、進度條（支援 widgets 回呼）
"""
import os, re, glob, html, json, time, random, shutil
from typing import List, Tuple, Dict, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import xml.etree.ElementTree as ET

try:
    from tqdm.auto import tqdm  # CLI fallback
except Exception:
    class _NoTQDM:
        def __init__(self, total=None, desc=None, unit=None): pass
        def update(self, n=1): pass
        def close(self): pass
    def tqdm(*args, **kwargs):
        return _NoTQDM()

from openai import OpenAI

# ================== 工具：讀 DOCTYPE ==================
def _read_doctype(xml_text: str) -> str:
    m = re.search(r'<!DOCTYPE[^>]+>', xml_text)
    return m.group(0) if m else ""

# ================== 讀 ODS 詞庫（若無則空表） ==================
def load_lookup_from_ods(folder: str = "data") -> pd.DataFrame:
    paths = sorted(glob.glob(os.path.join(folder, "*.ods")))
    if not paths:
        # 線上環境常無 ODS，回傳空表即可
        print(f"[提示] 詞庫資料夾 {folder} 無 .ods；將在無 glossary 模式下運作。")
        return pd.DataFrame({"en": [], "zh": []})
    rows = []
    for p in paths:
        try:
            df = pd.read_excel(p, engine="odf")
            if "英文名稱" in df.columns and "中文名稱" in df.columns:
                sub = df[["英文名稱", "中文名稱"]].copy()
                sub.columns = ["en", "zh"]
                rows.append(sub)
            else:
                print(f"[略過] {p} 缺少『英文名稱/中文名稱』欄位")
        except Exception as e:
            print(f"[警告] 無法讀取 {p}: {e}")
    if not rows:
        print("[提示] 找不到可用的詞庫欄位，改為空表。")
        return pd.DataFrame({"en": [], "zh": []})

    tbl = pd.concat(rows, ignore_index=True)
    tbl["en"] = tbl["en"].astype(str).str.strip()
    tbl["zh"] = tbl["zh"].astype(str).str.strip()
    tbl = tbl.dropna(subset=["en", "zh"])
    tbl = tbl[(tbl["en"] != "") & (tbl["zh"] != "")]
    tbl = tbl.drop_duplicates(subset=["en"], keep="first").reset_index(drop=True)
    return tbl

# ================== LCS 比對工具 ==================
def normalize_token(s: str) -> str: return s.lower()
def normalize_cand(s: str) -> str:  return s.lower()

def anchored_prefix_sub_in(token_norm: str, cand_norm: str) -> Tuple[int, str]:
    if not token_norm or not cand_norm:
        return 0, ""
    max_k = min(len(token_norm), len(cand_norm))
    for k in range(max_k, 0, -1):
        sub = token_norm[:k]
        if sub in cand_norm:
            return k, sub
    return 0, ""

_SEP_RE = re.compile(r'[\s/_\-.]+')
def soft_norm(s: str) -> str:
    return _SEP_RE.sub(' ', s.lower()).strip()

_GLOSSARY_FILTER_PAT = re.compile(
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
def _clean_for_glossary(text: str) -> str:
    return _GLOSSARY_FILTER_PAT.sub(' ', text)

class LCSMatcher:
    _TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[\/_.-][A-Za-z0-9]+)*")

    def __init__(self, lookup_df: pd.DataFrame, min_token_len: int = 4, min_lcs_len: int = 4):
        self.lookup = lookup_df.copy()
        self.lookup["en_norm"] = self.lookup["en"].apply(normalize_cand) if len(self.lookup) else []
        if len(self.lookup):
            self.lookup = self.lookup[self.lookup["en_norm"].str.len() >= 1].reset_index(drop=True)
            self.lookup["charset"] = self.lookup["en_norm"].apply(lambda s: set(re.sub(r"\s+", "", s)))
            self.lookup["en_soft"] = self.lookup["en"].apply(soft_norm)
            self.soft_index: Dict[str, Tuple[str, str]] = {}
            for _, row in self.lookup.iterrows():
                key = row["en_soft"]
                if key not in self.soft_index:
                    self.soft_index[key] = (row["en"], row["zh"])
            self.max_soft_len = max((len(x.split()) for x in self.lookup["en_soft"]), default=1)
        else:
            self.lookup = pd.DataFrame({"en": [], "zh": [], "en_norm": []})
            self.soft_index = {}
            self.max_soft_len = 1
        self.min_token_len = min_token_len
        self.min_lcs_len = min_lcs_len

    def _topk_for_word(self, token: str, k: int = 3) -> List[Dict]:
        if len(self.lookup) == 0:
            return []
        t_norm = normalize_token(token)
        if len(t_norm) < self.min_token_len:
            return []
        t_chars = set(t_norm)
        candidates = self.lookup[self.lookup["charset"].apply(lambda s: len(s & t_chars) > 0)]
        results = []
        for _, row in candidates.iterrows():
            kk, sub = anchored_prefix_sub_in(t_norm, row["en_norm"])
            if kk >= self.min_lcs_len:
                results.append({
                    "token": token, "en": row["en"], "zh": row["zh"],
                    "lcs_len": kk, "lcs": sub
                })
        results.sort(key=lambda d: (-d["lcs_len"], len(d["en"])))
        return results[:k]

    def build_glossary_sentence_first(
        self, text: str, *, limit: int = 8, per_word_k: int = 2, min_lcs_len: int = 4,
    ) -> Dict[str, str]:
        if len(self.lookup) == 0:
            return {}
        text_clean = _clean_for_glossary(text)
        tokens = self._TOKEN_RE.findall(text_clean)
        toks_lc = [t.lower() for t in tokens]
        n = len(toks_lc)
        covered = [False] * n
        glossary: Dict[str, str] = {}

        def _mark(i: int, j: int):
            for k in range(i, j): covered[k] = True

        win_max = min(n, getattr(self, "max_soft_len", n))
        for w in range(win_max, 0, -1):
            if len(glossary) >= limit: break
            for i in range(0, n - w + 1):
                if any(covered[k] for k in range(i, i + w)): continue
                phrase = " ".join(toks_lc[i:i + w])
                key = soft_norm(phrase)
                if key in self.soft_index:
                    en, zh = self.soft_index[key]
                    if en not in glossary:
                        glossary[en] = zh
                        _mark(i, i + w)
                        if len(glossary) >= limit: break

        for idx, tok in enumerate(tokens):
            if len(glossary) >= limit: break
            if covered[idx]: continue
            if len(tok) < min_lcs_len: continue
            hits = self._topk_for_word(tok, k=per_word_k)
            for r in hits:
                if r["lcs_len"] >= min_lcs_len and r["en"] not in glossary:
                    glossary[r["en"]] = r["zh"]
                    covered[idx] = True
                    if len(glossary) >= limit: break
        return glossary

# ================== 遮罩/還原 ==================
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

# ================== 判斷是否需要翻譯 ==================
def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip():
        return False
    if re.fullmatch(r"[\s\d\W%{}]+", en_text):
        return False
    return True

# ================== OpenAI 呼叫（含重試） ==================
def _with_retry(fn, *, tries=4, base=0.6, cap=4.0):
    last = None
    for t in range(tries):
        try:
            return fn()
        except Exception as e:
            last = e
            if t == tries - 1:
                break
            sleep = min(cap, base * (2 ** t)) * (0.8 + 0.4 * random.random())
            time.sleep(sleep)
    raise last if last else RuntimeError("未知錯誤")

def chatgpt_translate(masked_text: str, glossary: Dict[str, str], *, model: str, client: OpenAI) -> str:
    glossary_str = "\n".join([f"- {en} -> {zh}" for en, zh in glossary.items()]) or "（無）"
    system_prompt = (
        "你是台灣 GIS 軟體在地化譯者，請將英文翻為自然專業的繁體中文（台灣）。\n"
        "嚴格規則：\n"
        "1) ⟦MASKi⟧ 原樣保留且不可增刪；\n"
        "2) 不得輸出任何解釋或前後綴；只輸出譯文；\n"
        "3) Glossary 僅供參考，若不自然可忽略；\n"
        "4) 不要改動任何 HTML 標籤或 HTML 實體；"
    )
    user_prompt = (
        f"詞彙對照（僅供參考）：\n{glossary_str}\n\n"
        f"英文句子（含遮罩）：\n{masked_text}\n\n"
        "請直接輸出最終中文譯文："
    )
    def _call():
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
            temperature=0.2,
            max_tokens=100,
        )
        return (resp.choices[0].message.content or "").strip()
    zh = _with_retry(_call)
    for line in zh.splitlines():
        s = line.strip().strip("「」\"'")
        if s:
            return s
    return ""

def chatgpt_translate_batch(masked_texts: List[str], glossaries: List[Dict[str, str]], *, model: str, client: OpenAI) -> List[str]:
    assert len(masked_texts) == len(glossaries), "masked_texts / glossaries 長度不一致"

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

    def _call():
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
            temperature=0.2,
            max_tokens=min(4096, 160 * max(4, len(masked_texts))),
        )
        return (resp.choices[0].message.content or "").strip()

    raw = _with_retry(_call)

    def _parse_json_list(s: str) -> List[str]:
        import json as _json
        try:
            arr = _json.loads(s)
            if isinstance(arr, list) and all(isinstance(x, str) for x in arr):
                return arr
        except Exception:
            pass
        lb = s.find('[')
        rb = s.rfind(']')
        if 0 <= lb < rb:
            chunk = s[lb:rb+1]
            arr = _json.loads(chunk)
            if isinstance(arr, list) and all(isinstance(x, str) for x in arr):
                return arr
        raise ValueError("模型輸出非純 JSON 字串陣列")

    arr = _parse_json_list(raw)
    if len(arr) != len(masked_texts):
        raise ValueError(f"JSON 陣列長度不符，期待 {len(masked_texts)}，得到 {len(arr)}")
    return arr

# ================== 翻譯輔助 ==================
def translate_one(src_text: str, matcher: LCSMatcher, *, model: str, client: OpenAI) -> str:
    glossary = matcher.build_glossary_sentence_first(src_text, limit=8, per_word_k=2, min_lcs_len=4)
    masked, mapping = _mask_text(src_text)
    zh_raw = chatgpt_translate(masked, glossary, model=model, client=client)
    if not zh_raw:
        return src_text
    zh = _unmask_text(zh_raw, mapping)
    if src_text.endswith("\n") and not zh.endswith("\n"):
        zh += "\n"
    return zh

def translate_chunk(chunk_srcs: List[str], matcher: LCSMatcher, *, model: str, client: OpenAI) -> List[str]:
    glossaries, masked_texts, mappings = [], [], []
    for s in chunk_srcs:
        g = matcher.build_glossary_sentence_first(s, limit=8, per_word_k=2, min_lcs_len=4)
        glossaries.append(g)
        masked, mp = _mask_text(s)
        masked_texts.append(masked)
        mappings.append(mp)
    try:
        zh_list = chatgpt_translate_batch(masked_texts, glossaries, model=model, client=client)
    except Exception:
        zh_list = []
        for s in chunk_srcs:
            try:
                zh_list.append(translate_one(s, matcher, model=model, client=client))
            except Exception:
                zh_list.append(s)
    return [_et_ready(_unmask_text(z, mp)) for z, mp in zip(zh_list, mappings)]

# ================== 主流程（支援 widgets 進度） ==================
def process_ts_openai(input_ts: str, output_ts: str, matcher: LCSMatcher, *, 
                      openai_api_key: str, openai_model: str = "gpt-4.1-mini",
                      batch_size: int = 16, concurrency: int = 4,
                      on_total: Optional[Callable[[int], None]] = None,
                      on_progress: Optional[Callable[[int], None]] = None,
                      on_log: Optional[Callable[[str], None]] = None):
    """
    on_total(total)   ：回報 unique 原文數
    on_progress(delta)：每完成 delta 筆 unique 原文時呼叫
    on_log(msg)       ：即時訊息輸出
    """
    if on_log: on_log(f"開始處理：{input_ts}")
    client = OpenAI(api_key=openai_api_key)
    # 備份
    shutil.copyfile(input_ts, f"{input_ts}.bak")
    raw_xml = open(input_ts, "r", encoding="utf-8").read()
    doctype = _read_doctype(raw_xml)

    tree = ET.ElementTree(ET.fromstring(raw_xml))
    root = tree.getroot()

    messages = root.findall(".//message")
    tasks = []
    for m in messages:
        src_el = m.find("source")
        if src_el is None or src_el.text is None:
            continue
        if needs_translation(src_el.text):
            tasks.append((m, src_el.text, m.get("numerus") == "yes"))

    total_msg = len(messages)
    need_cnt = len(tasks)
    if on_log: on_log(f"🔍 原始檔共 {total_msg} 筆 message，需翻譯 {need_cnt} 筆")

    if not tasks:
        xml_bytes = ET.tostring(root, encoding="utf-8")
        with open(output_ts, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="utf-8"?>')
            if doctype:
                f.write(("\n" + doctype + "\n").encode("utf-8"))
            f.write(xml_bytes)
        if on_log: on_log(f"✅ 無需翻譯，輸出 -> {output_ts}")
        return

    # 去重
    idx_map: Dict[str, int] = {}
    uniq_srcs: List[str] = []
    task_uid: List[int] = []
    for _m, src, _num in tasks:
        if src not in idx_map:
            idx_map[src] = len(uniq_srcs)
            uniq_srcs.append(src)
        task_uid.append(idx_map[src])

    if on_total: on_total(len(uniq_srcs))

    uniq_zh = [""] * len(uniq_srcs)
    chunks = [uniq_srcs[i:i+batch_size] for i in range(0, len(uniq_srcs), batch_size)]

    pbar = tqdm(total=len(uniq_srcs), desc="翻譯唯一字串", unit="筆")
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = {ex.submit(translate_chunk, ch, matcher, model=openai_model, client=client): (idx, ch) 
                   for idx, ch in enumerate(chunks)}
        for fut in as_completed(futures):
            idx, ch = futures[fut]
            base = idx * batch_size
            try:
                result = fut.result()
            except Exception as e:
                if on_log: on_log(f"[警告] 批次失敗（降級逐筆）：{e}")
                result = [translate_one(s, matcher, model=openai_model, client=client) for s in ch]
            for j, zh in enumerate(result):
                if base + j < len(uniq_zh):
                    uniq_zh[base + j] = zh
            pbar.update(len(ch))
            if on_progress: on_progress(len(ch))
    pbar.close()

    # 回填
    for (m, _src_text, is_numerus), uid in zip(tasks, task_uid):
        trans_el = m.find("translation")
        if trans_el is None:
            trans_el = ET.SubElement(m, "translation")
        zh = uniq_zh[uid] or _src_text
        if is_numerus:
            forms = trans_el.findall("numerusform")
            if not forms:
                forms = [ET.SubElement(trans_el, "numerusform")]
            for f in forms:
                f.text = zh
        else:
            trans_el.text = zh
        trans_el.attrib.pop("type", None)

    xml_bytes = ET.tostring(root, encoding="utf-8")
    with open(output_ts, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="utf-8"?>')
        if doctype:
            f.write(("\n" + doctype + "\n").encode("utf-8"))
        f.write(xml_bytes)

    if on_log: on_log(f"✅ 完成翻譯 {len(tasks)} 筆（唯一 {len(uniq_srcs)} 筆），輸出 -> {output_ts}")

import io, os, pathlib
import ipywidgets as W
from IPython.display import display, FileLink

# --- Widgets ---
api_box   = W.Password(description="API Key", placeholder="sk-...")
model_box = W.Text(value="gpt-4.1-mini", description="Model")
batch_box = W.BoundedIntText(value=16, min=1, max=64, step=1, description="Batch")
conc_box  = W.BoundedIntText(value=4, min=1, max=16, step=1, description="Concurrency")

upload_ts = W.FileUpload(accept=".ts", multiple=False, description="上傳 .ts")
start_btn = W.Button(description="開始", button_style="success")
progress  = W.IntProgress(value=0, min=0, max=1, description="進度")
log_out   = W.Output(layout={"border":"1px solid #ddd"})

controls = W.VBox([api_box, model_box, W.HBox([batch_box, conc_box]), upload_ts, start_btn, progress, log_out])
display(controls)

workdir = pathlib.Path("./work")
workdir.mkdir(exist_ok=True)

def _log(msg):
    with log_out:
        print(msg)

def _on_total(total):
    progress.max = max(1, int(total))
    progress.value = 0
    progress.description = f"進度 (共 {total})"

def _on_progress(delta):
    progress.value = min(progress.max, progress.value + int(delta))

def _save_upload(uploader: W.FileUpload, dst_path: pathlib.Path) -> bool:
    if not uploader.value:
        _log("請先上傳 .ts 檔")
        return False
    item = list(uploader.value.values())[0]
    data = item["content"]
    dst_path.write_bytes(data)
    _log(f"已儲存：{dst_path}")
    return True

def _on_start(_btn):
    log_out.clear_output()
    if not api_box.value.strip():
        _log("請輸入 OpenAI API Key")
        return
    src = workdir / "input.ts"
    out = workdir / "output_zh-Hant.ts"
    if not _save_upload(upload_ts, src):
        return
    try:
        df_lookup = load_lookup_from_ods("data")  # 若無 ODS 也會正常回傳空表
        matcher = LCSMatcher(df_lookup, min_token_len=4, min_lcs_len=4)
        process_ts_openai(
            str(src), str(out), matcher,
            openai_api_key=api_box.value.strip(),
            openai_model=model_box.value.strip() or "gpt-4.1-mini",
            batch_size=int(batch_box.value),
            concurrency=int(conc_box.value),
            on_total=_on_total,
            on_progress=_on_progress,
            on_log=_log,
        )
        _log("完成。")
        display(FileLink(out, result_html_prefix="下載結果："))
    except Exception as e:
        _log(f"[錯誤] {e}")

start_btn.on_click(_on_start)