<!DOCTYPE html>
<html lang="zh-TW" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 翻譯工具 (專業版)</title>
<style>
  :root {
    --bg: #f9fafb; --surface: #ffffff; --border: #e5e7eb;
    --text: #111827; --muted: #6b7280; --accent: #2563eb; --on-accent: #ffffff;
    --err: #dc2626; --ok: #059669;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #0f1115; --surface: #1a1d21; --border: #2b2f36;
      --text: #e7eaf0; --muted: #9ca3af; --accent: #3b82f6;
    }
  }
  body {
    background: var(--bg); color: var(--text); margin: 0; padding: 20px;
    font-family: system-ui, -apple-system, sans-serif; line-height: 1.5; font-size: 14px;
  }
  .container { max-width: 900px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px; }
  .card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 20px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  }
  h1, h2 { margin: 0 0 12px; font-weight: 600; letter-spacing: -0.01em; }
  h1 { font-size: 1.25rem; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
  h2 { font-size: 1rem; color: var(--text); }
  
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .full { grid-column: 1 / -1; }
  @media (max-width: 600px) { .grid { grid-template-columns: 1fr; } }

  label { display: block; color: var(--muted); font-size: 0.85rem; margin-bottom: 4px; font-weight: 500; }
  input, select {
    width: 100%; padding: 8px 10px; border-radius: 6px;
    border: 1px solid var(--border); background: var(--bg); color: var(--text);
    font-size: 0.9rem; outline: none; box-sizing: border-box;
  }
  input:focus, select:focus { border-color: var(--accent); box-shadow: 0 0 0 2px rgba(37,99,235,0.1); }
  
  button {
    background: var(--text); color: var(--bg); border: 1px solid var(--text);
    padding: 10px 16px; border-radius: 6px; font-weight: 600; cursor: pointer;
    transition: opacity 0.2s; width: 100%; font-size: 0.9rem;
  }
  button.primary { background: var(--accent); color: var(--on-accent); border: 1px solid var(--accent); }
  button:hover { opacity: 0.9; }
  button:disabled { opacity: 0.5; cursor: not-allowed; }

  .hint { font-size: 0.8rem; color: var(--muted); margin-top: 4px; }
  
  /* Checkbox Styling */
  .chk-group { display: flex; align-items: center; gap: 8px; cursor: pointer; user-select: none; border: 1px solid var(--border); padding: 10px; border-radius: 6px; }
  .chk-group input { width: auto; margin: 0; }
  .chk-desc { display: flex; flex-direction: column; }
  .chk-desc strong { font-size: 0.9rem; }
  .chk-desc small { font-size: 0.75rem; color: var(--muted); }

  /* Progress & Logs */
  #progress-wrap { margin-top: 16px; display: none; }
  progress { width: 100%; height: 6px; border-radius: 3px; overflow: hidden; appearance: none; }
  progress::-webkit-progress-bar { background: var(--border); }
  progress::-webkit-progress-value { background: var(--accent); }
  
  #compare-box { margin-top: 16px; overflow: auto; max-height: 500px; border: 1px solid var(--border); border-radius: 6px; display: none; }
  table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
  th { background: var(--bg); position: sticky; top: 0; text-align: left; padding: 8px; border-bottom: 1px solid var(--border); font-weight: 600; z-index: 10; }
  td { padding: 8px; border-bottom: 1px solid var(--border); vertical-align: top; line-height: 1.4; }
  
  .tag {
    display: inline-block; font-size: 0.7rem; padding: 1px 4px;
    border-radius: 3px; margin-bottom: 2px; margin-right: 4px; font-family: monospace;
  }
  .tag-ctx { background: var(--bg); border: 1px solid var(--border); color: var(--muted); }
  .tag-err { background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; font-weight: bold; }
  
  #msg { margin-top: 12px; font-size: 0.9rem; }
  .status-ok { color: var(--ok); font-weight: 500; }
  .status-err { color: var(--err); font-weight: 500; }
  a.dl-link { color: var(--accent); text-decoration: underline; font-weight: bold; cursor: pointer; }
</style>
</head>
<body>

<div class="container">
  <div class="card">
    <h1>AI 翻譯工具 (Qt .ts)</h1>
    
    <div class="grid">
      <div class="full">
        <label>OpenAI API Key</label>
        <input type="password" id="apiKey" placeholder="sk-..." autocomplete="off">
      </div>
      
      <div>
        <label>API Base URL</label>
        <input type="text" id="baseUrl" value="https://api.openai.com/v1">
      </div>
      
      <div>
        <label>Model 1 (翻譯)</label>
        <select id="modelSel">
          <option value="gpt-4o-mini" selected>gpt-4o-mini (推薦)</option>
          <option value="gpt-4o">gpt-4o</option>
          <option value="o1-mini">o1-mini</option>
          <option value="__custom__">自訂...</option>
        </select>
        <input id="modelCustom" type="text" placeholder="輸入模型名稱" style="display:none; margin-top:4px;">
      </div>
    </div>

    <div style="margin: 16px 0; border-top: 1px solid var(--border);"></div>

    <div class="grid">
      <div class="full">
        <label class="chk-group">
          <input type="checkbox" id="useModel2" checked>
          <div class="chk-desc">
            <strong>啟用雙重校對 (Parallel A/B Check)</strong>
            <small>同時生成兩版譯文並進行平行比對，修正格式錯誤與幻覺 (推薦)</small>
          </div>
        </label>
      </div>
      
      <div>
        <label>Model 2 (校對)</label>
        <select id="modelSel2">
          <option value="gpt-4o-mini" selected>gpt-4o-mini (推薦)</option>
          <option value="gpt-4o">gpt-4o</option>
          <option value="__custom__">自訂...</option>
        </select>
        <input id="modelCustom2" type="text" placeholder="輸入模型名稱" style="display:none; margin-top:4px;">
      </div>
      
      <div>
        <label>Batch Size</label>
        <input type="number" id="batch" value="32" min="1" max="100">
      </div>
    </div>
  </div>

  <div class="card">
    <h2>檔案處理</h2>
    <div class="grid">
      <div>
        <label>.ts 來源檔 (Qt Linguist)</label>
        <input type="file" id="tsFile" accept=".ts">
        <div class="hint" id="tsInfo">尚未選擇</div>
      </div>
      <div>
        <label>術語表 (CSV/ODS)</label>
        <input type="file" id="glsFile" accept=".csv,.ods" multiple>
        <div class="hint">格式: en, zh (第一列為標題)</div>
      </div>
      <div class="full">
        <label>處理筆數限制 (0 = 全部)</label>
        <input type="number" id="limitN" value="0" placeholder="例如: 100">
      </div>
    </div>
    
    <div style="margin-top: 20px;">
      <button id="run-btn" class="primary">開始翻譯</button>
    </div>

    <div id="progress-wrap">
      <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.8rem; color:var(--muted);">
        <span>處理進度</span>
        <span id="progress-txt">0 / 0</span>
      </div>
      <progress id="p-bar" value="0" max="100"></progress>
    </div>
    
    <div id="msg"></div>
  </div>

  <div id="compare-box">
    <table>
      <thead><tr><th style="width:45%">Context & Source</th><th>Translation</th></tr></thead>
      <tbody id="compare-body"></tbody>
    </table>
  </div>
</div>

<script type="module">
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.mjs";

const $ = id => document.getElementById(id);
let pyodide = null;

async function initPyodide() {
  $('msg').innerHTML = '<span style="color:var(--muted)">正在載入 Python 引擎...</span>';
  try {
    pyodide = await loadPyodide();
    await pyodide.loadPackage("micropip");
    $('msg').innerHTML = '';
  } catch(e) {
    $('msg').innerHTML = '<span class="status-err">Python 載入失敗，請重新整理頁面。</span>';
  }

  // File info listener
  $('tsFile').addEventListener('change', async (e) => {
    const f = e.target.files[0];
    if(!f) { $('tsInfo').textContent="尚未選擇"; return; }
    const txt = await f.text();
    // Simple rough count
    const matches = txt.match(/<source>/g);
    const count = matches ? matches.length : 0;
    $('tsInfo').textContent = `檔案: ${f.name} (約 ${count} 筆)`;
    if(count > 0) $('limitN').placeholder = `最大 ${count}`;
  });

  // Custom model toggle
  const toggleCustom = (selId, inpId) => {
    const sel = $(selId), inp = $(inpId);
    sel.addEventListener('change', () => inp.style.display = sel.value === '__custom__' ? 'block' : 'none');
  };
  toggleCustom('modelSel', 'modelCustom');
  toggleCustom('modelSel2', 'modelCustom2');
}

initPyodide();

$('run-btn').addEventListener('click', async () => {
  if (!pyodide) return alert("Python 尚未載入完成，請稍候。");
  const apiKey = $('apiKey').value;
  const tsFile = $('tsFile').files[0];
  
  if (!apiKey) return alert("請輸入 API Key");
  if (!tsFile) return alert("請選擇 .ts 檔案");

  const getVal = (sel, inp) => $(sel).value === '__custom__' ? $(inp).value : $(sel).value;
  
  // UI Reset
  $('run-btn').disabled = true;
  $('run-btn').textContent = "處理中...";
  $('msg').innerHTML = "";
  $('compare-box').style.display = "none";
  $('compare-body').innerHTML = "";
  $('progress-wrap').style.display = "block";

  try {
    await pyodide.runPythonAsync(PYTHON_SCRIPT);
    
    // Bind JS functions for Python to call
    self.py_update_progress = (done, total) => {
        $('p-bar').max = total; $('p-bar').value = done;
        $('progress-txt').textContent = `${done} / ${total}`;
    };
    self.py_add_row = (src, trans, ctx, isErr) => {
        $('compare-box').style.display = "block";
        const row = $('compare-body').insertRow();
        
        const c1 = row.insertCell();
        if(ctx) c1.innerHTML += `<span class="tag tag-ctx">${ctx}</span><br>`;
        c1.appendChild(document.createTextNode(src));
        
        const c2 = row.insertCell();
        if(isErr) c2.innerHTML += `<span class="tag tag-err">Var Error</span>`;
        c2.appendChild(document.createTextNode(trans));
        
        // Auto scroll
        const box = $('compare-box');
        if(box.scrollHeight - box.scrollTop < box.clientHeight + 100) {
             box.scrollTop = box.scrollHeight;
        }
    };
    self.py_log = (html) => $('msg').innerHTML = html;

    // Execute Python Main Process
    await pyodide.globals.get('main_process')(
      apiKey,
      $('baseUrl').value,
      getVal('modelSel', 'modelCustom'),
      getVal('modelSel2', 'modelCustom2'),
      $('useModel2').checked,
      parseInt($('batch').value),
      parseInt($('limitN').value)
    );

  } catch (e) {
    console.error(e);
    $('msg').innerHTML = `<span class="status-err">系統錯誤: ${e.message}</span>`;
  } finally {
    $('run-btn').disabled = false;
    $('run-btn').textContent = "開始翻譯";
  }
});

const PYTHON_SCRIPT = String.raw`
import asyncio, json, re, io, base64, html, zipfile, csv
from xml.etree import ElementTree as ET
from js import document, self, Uint8Array, File
from pyodide.http import pyfetch

# Install Dependencies
try:
    from opencc import OpenCC
except ImportError:
    import micropip
    await micropip.install("opencc-python-reimplemented==0.1.7")
    from opencc import OpenCC

_OPENCC = OpenCC("s2twp")
# Terms protected from OpenCC conversion (GIS specifics)
_TW_PROTECT = ["演算法", "專案", "圖層", "外掛", "巨集", "快取", "佈局", "拓撲", "向量", "網格", "波段"]
_MASK_PAT = re.compile(r'(</?[A-Za-z][^>]*>|&lt;/?[A-Za-z][^&]*?&gt;|%L\d+|%\d+|%[sdn]|\{\d+\}|&(?!\s)[A-Za-z#x0-9]+;)', re.IGNORECASE)
_SEP_RE = re.compile(r"[-\s/_.\\]+")

# ================= LCS & Glossary Logic =================

def soft_norm(s): 
    return _SEP_RE.sub(" ", s.lower()).strip()

class LCSMatcher:
    def __init__(self, pairs, min_len=4):
        self.rows = []
        for en, zh in pairs:
            e = (en or "").strip(); z = (zh or "").strip()
            if e and z: 
                self.rows.append({"e":e, "z":z, "norm": soft_norm(e)})
        
    def build_glossary(self, text, limit=5):
        # Find terms in source text that match glossary entries
        g = {}
        norm_text = soft_norm(text)
        count = 0
        # Sort by length desc to match longest terms first
        sorted_rows = sorted(self.rows, key=lambda x: len(x["norm"]), reverse=True)
        
        for r in sorted_rows:
            if count >= limit: break
            if r["norm"] in norm_text:
                # Avoid sub-string matching for very short words if possible
                if len(r["norm"]) < 4 and f" {r['norm']} " not in f" {norm_text} ":
                    continue
                if r["e"] not in g:
                    g[r["e"]] = r["z"]
                    count += 1
        return g

def load_glossary_csv(text):
    try:
        r = csv.DictReader(io.StringIO(text))
        if not r.fieldnames: return []
        # Flexible column matching
        headers = [h.strip().lower() for h in r.fieldnames]
        en_key = next((r.fieldnames[i] for i,h in enumerate(headers) if h in ("en", "英文", "source")), None)
        zh_key = next((r.fieldnames[i] for i,h in enumerate(headers) if h in ("zh", "中文", "target", "zh-tw")), None)
        
        if not en_key or not zh_key: return []
        return [(row[en_key], row[zh_key]) for row in r if row.get(en_key) and row.get(zh_key)]
    except: return []

def load_glossary_ods(data):
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z: xml = z.read("content.xml")
        ns = {"text":"urn:oasis:names:tc:opendocument:xmlns:text:1.0", "table":"urn:oasis:names:tc:opendocument:xmlns:table:1.0"}
        root = ET.fromstring(xml)
        rows = root.findall(".//table:table-row", ns)
        pairs = []
        if not rows: return []
        
        def get_txt(cell):
            return "".join("".join(p.itertext()) for p in cell.findall(".//text:p", ns)).strip()
            
        headers = [get_txt(c).lower() for c in rows[0].findall("table:table-cell", ns)]
        try:
            ei = next(i for i,h in enumerate(headers) if h in ("en", "英文", "source"))
            zi = next(i for i,h in enumerate(headers) if h in ("zh", "中文", "target", "zh-tw"))
        except: return []
        
        for r in rows[1:]:
            cells = r.findall("table:table-cell", ns)
            if len(cells) > max(ei, zi):
                en = get_txt(cells[ei]); zh = get_txt(cells[zi])
                if en and zh: pairs.append((en, zh))
        return pairs
    except: return []

# ================= Helper Functions =================

def to_zh_tw(text):
    if not text: return ""
    ph = {}
    # Protect special terms
    for i, t in enumerate(_TW_PROTECT):
        k = f"⟦TP{i}⟧"; ph[k] = t; text = text.replace(t, k)
    
    try: text = _OPENCC.convert(text)
    except: pass
    
    for k, v in ph.items(): text = text.replace(k, v)
    # Manual fixes
    return text.replace("坐標", "座標").replace("軟件", "軟體").replace("通過", "透過").replace("文件", "檔案").replace("項目", "專案")

def fix_punct(text):
    if not text: return ""
    # Convert full-width parens to half-width used in UI
    return text.replace("（", "(").replace("）", ")").replace("：", ": ").strip()

def validate_vars(src, trans):
    # Regex to find variables like %s, %1, {0}
    pat = re.compile(r"(%\d|%[sdn]|{\d+})")
    src_vars = sorted(pat.findall(src))
    trans_vars = sorted(pat.findall(trans))
    return src_vars == trans_vars

def mask_text(s):
    m = {}; i = 0
    def r(x): nonlocal i; k=f"⟦M{i}⟧"; m[k]=x.group(0); i+=1; return k
    return _MASK_PAT.sub(r, s), m

def unmask_text(s, m):
    for k, v in m.items(): s = s.replace(k, v)
    return s

# ================= API Logic =================

async def call_api(api_key, base_url, model, payload, retries=1):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    url = base_url.rstrip("/") + "/chat/completions"
    
    # O1/O3 model compatibility
    if model.lower().startswith(("o1", "o3")):
        new_msgs = []
        for m in payload.get("messages", []):
            if m["role"] == "system":
                new_msgs.append({"role": "user", "content": f"System Instruction:\n{m['content']}"})
            else: new_msgs.append(m)
        payload["messages"] = new_msgs
        payload.pop("temperature", None)
        payload["max_completion_tokens"] = payload.pop("max_tokens", 4000)
    
    for _ in range(retries + 1):
        try:
            r = await pyfetch(url, method="POST", headers=headers, body=json.dumps(payload))
            d = await r.json()
            if r.status >= 400: raise Exception(d.get("error", {}).get("message"))
            
            ch = d["choices"][0]["message"]
            # Return Tool Calls or Content
            if ch.get("tool_calls"): return json.loads(ch["tool_calls"][0]["function"]["arguments"])
            if ch.get("content"): return json.loads(ch["content"])
        except Exception as e:
            if _ == retries: return None
            await asyncio.sleep(1)
    return None

# ================= Main Process =================

async def main_process(api_key, base_url, m1, m2, use_m2, batch_size, limit_n):
    # 1. Read TS File
    ts_input = document.getElementById("tsFile")
    if not ts_input.files.length: return
    ts_text = (await ts_input.files.item(0).arrayBuffer()).decode("utf-8")
    
    # 2. Read Glossaries
    gl_input = document.getElementById("glsFile")
    gl_pairs = []
    if gl_input.files.length:
        self.py_log("讀取術語表中...")
        for i in range(gl_input.files.length):
            f = gl_input.files.item(i)
            b = await f.arrayBuffer()
            if f.name.endswith(".csv"): gl_pairs += load_glossary_csv(b.decode("utf-8","ignore"))
            elif f.name.endswith(".ods"): gl_pairs += load_glossary_ods(b)
    
    matcher = LCSMatcher(gl_pairs) if gl_pairs else None
    
    # 3. Parse XML with Context Extraction
    self.py_log("解析 XML 結構與 Context...")
    # Keep DOCTYPE if exists
    doctype = ""
    dt_match = re.search(r'<!DOCTYPE[^>]+>', ts_text)
    if dt_match: doctype = dt_match.group(0)

    root = ET.fromstring(ts_text)
    tasks = []
    
    for ctx in root.findall("context"):
        c_name = ctx.find("name").text or ""
        
        for msg in ctx.findall("message"):
            src = msg.find("source")
            # Skip empty or technical-only strings
            if src is None or not src.text or not src.text.strip(): continue
            if re.match(r'^[0-9\W]+$', src.text): continue
            
            # Build Context String
            info = []
            if c_name: info.append(f"UI: {c_name}")
            if msg.find("comment") is not None: info.append(f"Note: {msg.find('comment').text}")
            if msg.find("extracomment") is not None: info.append(f"Extra: {msg.find('extracomment').text}")
            
            ctx_str = " | ".join(info)
            
            tasks.append({"node": msg, "src": src.text, "ctx": ctx_str})
            
            if limit_n > 0 and len(tasks) >= limit_n: break
        if limit_n > 0 and len(tasks) >= limit_n: break
        
    total = len(tasks)
    self.py_update_progress(0, total)
    self.py_log(f"準備翻譯 {total} 筆資料 (含術語 {len(gl_pairs)} 筆)")
    
    finished = 0
    
    # Define Tools for structured output
    tools = [{
        "type": "function",
        "function": {
            "name": "save_translations",
            "description": "Save the list of translations",
            "parameters": {
                "type": "object",
                "properties": {
                    "results": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["results"]
            }
        }
    }]

    # 4. Batch Processing
    for i in range(0, total, batch_size):
        batch = tasks[i : i + batch_size]
        
        masked_list = []
        maps_list = []
        items_payload = []
        
        # Prepare items for LLM
        for k, t in enumerate(batch):
            m, mp = mask_text(t["src"])
            masked_list.append(m)
            maps_list.append(mp)
            
            # Get glossary matches
            g = matcher.build_glossary(t["src"]) if matcher else {}
            gls_str = ", ".join([f"{k}->{v}" for k,v in g.items()])
            
            items_payload.append({
                "id": k,
                "text": m,
                "context": t["ctx"],
                "glossary": gls_str
            })

        sys_prompt = "You are a professional translator for GIS software (English to Traditional Chinese Taiwan). Use the provided Context and Glossary to resolve ambiguities (e.g. 'Open' -> '開啟', 'Band' -> '波段'). Keep variables (⟦M0⟧, %s) intact."
        user_prompt = f"Translate the following items:\n{json.dumps(items_payload, ensure_ascii=False)}"
        
        res_final = []
        
        try:
            if use_m2:
                # Parallel Call A (Temp 0.2) & B (Temp 0.8)
                payload_a = {
                    "model": m1, "temperature": 0.2, "tools": tools,
                    "tool_choice": {"type":"function", "function":{"name":"save_translations"}},
                    "messages": [{"role":"system","content":sys_prompt},{"role":"user","content":user_prompt}]
                }
                payload_b = {**payload_a, "temperature": 0.8}
                
                res_a, res_b = await asyncio.gather(
                    call_api(api_key, base_url, m1, payload_a),
                    call_api(api_key, base_url, m1, payload_b)
                )
                
                list_a = res_a.get("results", []) if res_a else [""]*len(batch)
                list_b = res_b.get("results", []) if res_b else [""]*len(batch)
                
                # Normalize lengths
                list_a += [""] * (len(batch) - len(list_a))
                list_b += [""] * (len(batch) - len(list_b))
                
                # Selection Phase (Model 2)
                sel_items = []
                for idx, (orig, a, b) in enumerate(zip(batch, list_a, list_b)):
                    sel_items.append({"src": orig["src"], "ctx": orig["ctx"], "Option_A": a, "Option_B": b})
                
                sel_sys = "Select the best translation for Taiwan GIS software. Ensure variables (%s, {0}) match the source. If both are bad, provide a corrected version."
                sel_payload = {
                    "model": m2, "temperature": 0.1, "tools": tools,
                    "tool_choice": {"type":"function", "function":{"name":"save_translations"}},
                    "messages": [
                        {"role":"system","content":sel_sys},
                        {"role":"user","content":json.dumps(sel_items, ensure_ascii=False)}
                    ]
                }
                
                rf = await call_api(api_key, base_url, m2, sel_payload)
                res_final = rf.get("results", []) if rf else list_a
                
            else:
                # Single Model Mode
                payload = {
                    "model": m1, "temperature": 0.2, "tools": tools,
                    "tool_choice": {"type":"function", "function":{"name":"save_translations"}},
                    "messages": [{"role":"system","content":sys_prompt},{"role":"user","content":user_prompt}]
                }
                r = await call_api(api_key, base_url, m1, payload)
                res_final = r.get("results", []) if r else [""]*len(batch)

        except Exception as e:
            print(f"Batch error: {e}")
            res_final = [""] * len(batch)
            
        # Process Results & Write XML
        for k, raw_trans in enumerate(res_final):
            if k >= len(batch): break
            task = batch[k]
            
            # Post-processing pipeline
            # 1. Unmask -> 2. Unescape HTML -> 3. OpenCC/Fixes -> 4. Punctuation
            processed = unmask_text(raw_trans, maps_list[k])
            processed = html.unescape(processed)
            processed = to_zh_tw(fix_punct(processed))
            
            # Variable Validation
            is_err = not validate_vars(task["src"], processed)
            if is_err:
                processed = f"[Var Error] {processed}"
            
            # Write to XML Node
            tr_node = task["node"].find("translation")
            if tr_node is None:
                tr_node = ET.SubElement(task["node"], "translation")
            
            # Handle plurals (numerus) if necessary, simplify for now
            tr_node.text = processed
            # Remove "unfinished" type if present
            if "type" in tr_node.attrib: del tr_node.attrib["type"]
            
            self.py_add_row(task["src"], processed, task["ctx"], is_err)
            
        finished += len(batch)
        self.py_update_progress(finished, total)
        
    # 5. Export
    out_xml = ET.tostring(root, encoding="utf-8")
    if doctype: out_xml = doctype.encode("utf-8") + b"\n" + out_xml
    else: out_xml = b"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" + out_xml
    
    b64 = base64.b64encode(out_xml).decode("ascii")
    self.py_log(f'<span class="status-ok">翻譯完成！</span> <a class="dl-link" href="data:application/xml;base64,{b64}" download="qgis_zh-Hant.ts">點此下載翻譯結果</a>')
`;
</script>
</body>
</html>