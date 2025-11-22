---
title: Local
thebe: false
---

# Local LLM 翻譯

```{raw} html
<style>
  /* 讓內容拉滿、隱藏右側 sidebar（和其它頁一致） */
  .bd-sidebar-secondary { display: none !important; }
  .bd-content,
  .bd-article-container,
  .tex2jax_ignore.mathjax_ignore {
    max-width: 100% !important;
    width: 100% !important;
  }

  /* #ts-ui 主題變數（整體色系 / 字體） */
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

    --ts-accent: #2563eb;
    --ts-on-accent: #ffffff;
    --ts-focus: 0 0 0 2px rgba(37,99,235,.25);

    --ts-progress-bg: #e5e7eb;
    --ts-table-head-bg: #f3f4f6;
    --ts-head-bg: var(--ts-table-head-bg);

    font-family: system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans",
                 "PingFang TC", "Microsoft JhengHei", sans-serif;
    line-height: 1.35;
    margin: 8px 0 16px;
    color: var(--ts-text);
  }

  /* 依系統偏好自動 dark（備用） */
  @media (prefers-color-scheme: dark){
    #ts-ui{
      --ts-border: #2b2f36;

      --ts-bg: #0f1115;
      --ts-surface: #111418;
      --ts-input-bg: #0b0f14;

      --ts-text: #e5e7eb;
      --ts-muted: #9aa3af;

      --ts-progress-bg: #1a1f29;
      --ts-table-head-bg: #121621;
      --ts-head-bg: var(--ts-table-head-bg);
    }
  }

  /* Jupyter Book 主題切到 dark 時，強制使用暗色變數 */
  html[data-theme="dark"] #ts-ui{
    --ts-border: #2b2f36;

    --ts-bg: #0f1115;
    --ts-surface: #111418;
    --ts-input-bg: #0b0f14;

    --ts-text: #e5e7eb;
    --ts-muted: #9aa3af;

    --ts-progress-bg: #1a1f29;
    --ts-table-head-bg: #121621;
    --ts-head-bg: var(--ts-table-head-bg);
  }

  #ts-ui ::selection{
    background: color-mix(in oklab, var(--ts-accent, #2563eb) 35%, transparent);
  }
  #ts-ui *, #ts-ui *::before, #ts-ui *::after{
    box-sizing: border-box;
  }

  /* ===== Local LLM 設定 UI（.nbui） ===== */
  .nbui{
    font-family: inherit;
    line-height: 1.45;
    color: var(--ts-text);
  }
  .nbui *{
    box-sizing: border-box;
  }
  .nbui h2{
    margin: .5rem 0 0.25rem;
  }

  .nbui .card{
    border: 1px solid var(--ts-border);
    border-radius: var(--ts-radius);
    padding: var(--ts-pad);
    background: var(--ts-surface);
    margin: 12px 0;
    box-shadow: 0 1px 2px rgba(0,0,0,.04);
    color: var(--ts-text);
  }

  .nbui .muted{
    color: var(--ts-muted);
    font-size: 13px;
  }

  .nbui .grid{
    display: grid;
    gap: 12px;
  }
  .nbui .grid-2{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 12px;
  }
  .nbui .grid-3{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
  }
  /* 固定三欄：1:1:1 並排 */
  .nbui .grid-3-fixed{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12px;
  }
  @media (max-width: 900px){
    .nbui .grid-3-fixed{ grid-template-columns: 1fr 1fr; }
  }
  @media (max-width: 640px){
    .nbui .grid-3-fixed{ grid-template-columns: 1fr; }
  }

  .nbui label{
    font-size: 14px;
    color: var(--ts-text);
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .nbui input[type="text"],
  .nbui input[type="number"],
  .nbui select{
    padding: 10px 12px;
    border: 1px solid var(--ts-border);
    border-radius: 10px;
    min-width: 200px;
    background: var(--ts-input-bg);
    color: var(--ts-text);
  }
  .nbui input[type="text"]:focus,
  .nbui input[type="number"]:focus,
  .nbui select:focus{
    outline: none;
    border-color: color-mix(in oklab, var(--ts-accent) 60%, var(--ts-border));
    box-shadow: var(--ts-focus);
  }

  .nbui button{
    padding: 10px 14px;
    border: 1px solid var(--ts-border);
    border-radius: 10px;
    background: var(--ts-surface);
    cursor: pointer;
    color: var(--ts-text);
    transition: background .15s ease, transform .1s ease;
  }
  .nbui button:hover{
    background: color-mix(in oklab, var(--ts-accent) 8%, var(--ts-surface));
  }
  .nbui button:active{
    transform: translateY(1px);
  }

  /* 如果之後有主要動作按鈕，可以額外加這個 */
  .nbui .btn-primary{
    background: var(--ts-accent);
    color: var(--ts-on-accent);
  }
  .nbui .btn-primary:hover{
    background: color-mix(in oklab, var(--ts-accent) 110%, #0000);
  }

  .nbui pre.preview{
    white-space: pre-wrap;
    background: var(--ts-input-bg);
    border: 1px solid var(--ts-border);
    padding: 10px;
    border-radius: 10px;
    margin-top: 10px;
    display: none;
    color: var(--ts-text);
  }

  .nbui .section{
    display: block;
    margin: 6px 0 2px;
  }
  .nbui .section h3{
    margin: .25rem 0 .25rem;
    font-size: 15px;
    color: var(--ts-text);
    font-weight: 600;
  }

  .nbui .btn-row{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
  }
</style>

<div id="ts-ui">
  <div class="nbui" id="nbui">
    <div class="card">
      <!-- 檔案 / 輸入輸出 -->
      <div class="section">
        <h3>檔案與輸入 / 輸出</h3>
        <div class="grid-3-fixed">
          <label>輸入檔名
            <input id="inputFile" type="text" placeholder="qgis_en.ts">
          </label>
          <label>輸出檔名（不需副檔名）
            <input id="fname" type="text" value="qgis_zh-Hant">
          </label>
          <label>字典資料夾位置（ODS_DIR）
            <input id="odsDir" type="text" value="data" placeholder="data">
          </label>
        </div>
      </div>

      <!-- 模型設定 與 API -->
      <div class="section">
        <h3>模型設定</h3>
        <div class="grid-2">
          <label>模型（Model）
            <select id="model">
              <option value="taide/Gemma-3-TAIDE-12B-Chat" selected>taide/Gemma-3-TAIDE-12B-Chat</option>
              <option value="taide/Llama-3.1-TAIDE-LX-8B-Chat">taide/Llama-3.1-TAIDE-LX-8B-Chat</option>
              <option value="taide/TAIDE-Gemma-2-9B-Chat">taide/TAIDE-Gemma-2-9B-Chat</option>
              <option value="Qwen/Qwen3-7B-Instruct">Qwen/Qwen3-7B-Instruct</option>
              <option value="Qwen/Qwen2.5-7B-Instruct">Qwen/Qwen2.5-7B-Instruct</option>
              <option value="Qwen/Qwen2.5-14B-Instruct">Qwen/Qwen2.5-14B-Instruct</option>
              <option value="THUDM/glm-4-9b-chat">THUDM/glm-4-9b-chat</option>
              <option value="google/gemma-2-9b-it">google/gemma-2-9b-it</option>
              <option value="meta-llama/Meta-Llama-3.1-8B-Instruct">meta-llama/Meta-Llama-3.1-8B-Instruct</option>
            </select>
          </label>
          <label>備用模型（FALLBACK_MODEL）
            <input id="fallbackModel" type="text" placeholder="可留空，主要模型失敗時改用（例如 Qwen/Qwen2.5-7B-Instruct）">
          </label>
          <label>API Key or Token（可留空）
            <input id="apiKey" type="text" placeholder="sk-...">
          </label>
          <label>API Base URL
            <input id="apiBase" type="text" value="https://api.openai.com/v1">
          </label>
        </div>
        <div class="muted" style="margin-top:6px">提醒：若不希望把 API Key 寫進 notebook，留空即可；也可在執行環境用環境變數配置。</div>
      </div>

      <!-- 參數設定 -->
      <div class="section">
        <h3>參數設定</h3>
        <div class="grid-3">
          <label>Batch
            <input id="batch" type="number" min="1" value="4">
          </label>
          <label>Max Tokens
            <input id="maxTokens" type="number" min="1" value="1024">
          </label>
          <label>Min Tokens
            <input id="minTokens" type="number" min="1" value="4">
          </label>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="btn-row">
        <button id="btn-download">下載 .ipynb 檔</button>
        <button id="btn-preview">預覽 Config cell</button>
      </div>
      <pre id="preview" class="preview muted"></pre>
    </div>
  </div>
</div>

<script>
(async function(){
  async function loadBaseNotebook(){
    const candidates = [
      '../sites/Untitled11.ipynb',
    ];
    for (const u of candidates){
      try{
        const r = await fetch(u);
        if (r.ok) return await r.json();
      }catch(e){}
    }
    throw new Error('找不到 Untitled11.ipynb，請把檔案放在與此頁同資料夾或 assets/sites/ 下，或修改程式中的 candidates 路徑。');
  }

  // 小工具
  function toSourceLines(text){ return text.replace(/\r\n/g, "\n").split("\n").map(l => l+"\n"); }

  function buildInstallCell(){
    const src = `import os, sys, platform, subprocess, shutil\n\n`+
`def run(cmd):\n`+
`    print('[pip]', ' '.join(cmd))\n`+
`    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)\n`+
`    print(r.stdout)\n`+
`    if r.returncode != 0:\n`+
`        raise RuntimeError('Command failed: ' + ' '.join(cmd))\n\n`+
`def pip_install(args, index_url=None):\n`+
`    cmd = [sys.executable, '-m', 'pip', 'install', '-q'] + list(args)\n`+
`    if index_url: cmd += ['--index-url', index_url]\n`+
`    run(cmd)\n\n`+
`# 升級\n`+
`pip_install(['--upgrade', 'pip', 'setuptools', 'wheel'])\n\n`+
`# 判斷 CUDA\n`+
`def cuda_available():\n`+
`    try:\n`+
`        out = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)\n`+
`        return out.returncode == 0\n`+
`    except Exception:\n`+
`        return False\n\n`+
`cuda = cuda_available()\n`+
`# 先嘗試 CUDA 12.1 的 PyTorch\n`+
`tried_gpu = False\n`+
`if cuda:\n`+
`    try:\n`+
`        pip_install(['torch', 'torchvision', 'torchaudio'], index_url='https://download.pytorch.org/whl/cu121')\n`+
`        tried_gpu = True\n`+
`        print('Installed PyTorch (CUDA 12.1)')\n`+
`    except Exception as e:\n`+
`        print('CUDA 安裝失敗，改裝 CPU。', e)\n\n`+
`if not tried_gpu:\n`+
`    pip_install(['torch', 'torchvision', 'torchaudio'], index_url='https://download.pytorch.org/whl/cpu')\n`+
`    print('Installed PyTorch (CPU)')\n\n`+
`common = [\n`+
`  'transformers', 'accelerate', 'safetensors', 'sentencepiece', 'tokenizers',\n`+
`  'datasets', 'huggingface_hub', 'peft', 'einops', 'tiktoken',\n`+
`  'protobuf>=3.20,<5', 'numpy', 'scipy', 'tqdm', 'pyyaml', 'requests', 'orjson', 'psutil',\n`+
`  'gradio', 'uvicorn', 'fastapi', 'odfpy>=1.4.1'\n`+
`]\n`+
`pip_install(common)\n\n`+
`if cuda and platform.system() == 'Linux':\n`+
`    try:\n`+
`        pip_install(['bitsandbytes'])\n`+
`        print('Installed bitsandbytes')\n`+
`    except Exception as e:\n`+
`        print('安裝 bitsandbytes 失敗，略過。', e)\n\n`+
`print('基礎套件安裝完成。')\n`;

    return {
      cell_type: 'code',
      execution_count: null,
      metadata: {"name":"auto_install"},
      outputs: [],
      source: toSourceLines(src)
    };
  }

  function buildConfigCell(){
    const outputFile    = document.getElementById('fname').value;
    const apiKey        = document.getElementById('apiKey').value;
    const apiBase       = document.getElementById('apiBase').value;
    const model         = document.getElementById('model').value;
    const batch         = parseInt(document.getElementById('batch').value)||1;
    const inputFile     = document.getElementById('inputFile').value;
    const maxTokens     = parseInt(document.getElementById('maxTokens').value)||0;
    const minTokens     = parseInt(document.getElementById('minTokens').value)||0;
    const fallbackModel = document.getElementById('fallbackModel').value;
    const odsDir        = document.getElementById('odsDir').value;

    const lines = [
      `API_KEY = ${apiKey ? JSON.stringify(apiKey) : "None"}`,
      `API_BASE = ${JSON.stringify(apiBase)}`,
      `MODEL = ${JSON.stringify(model)}`,
      `INPUT_FILENAME = ${JSON.stringify(inputFile)}`,
      `BATCH = ${batch}`,
      `MAX_TOKENS = ${maxTokens}`,
      `MIN_TOKENS = ${minTokens}`,
      `FALLBACK_MODEL = ${fallbackModel ? JSON.stringify(fallbackModel) : "None"}`,
      `OUTPUT_FILENAME = ${JSON.stringify(outputFile || "")}`,
      `ODS_DIR = ${JSON.stringify(odsDir || "")}`,
    ].join("\n");

    return {
      cell_type: "code",
      execution_count: null,
      metadata: {"name":"auto_config"},
      outputs: [],
      source: toSourceLines(lines)
    };
  }

  function buildNotebook(BASE_NB){
    const nb = JSON.parse(JSON.stringify(BASE_NB));
    if (!nb.cells) nb.cells = [];
    const installCell = buildInstallCell();
    const cfgCell = buildConfigCell();
    nb.cells = [installCell, cfgCell, ...nb.cells];
    nb.nbformat = nb.nbformat || 4;
    nb.nbformat_minor = nb.nbformat_minor || 5;
    nb.metadata = nb.metadata || {};
    nb.metadata.kernelspec = nb.metadata.kernelspec || {"name":"python3","display_name":"Python 3","language":"python"};
    nb.metadata.language_info = nb.metadata.language_info || {"name":"python"};
    return nb;
  }

  // 綁定按鈕
  const BASE_NB = await loadBaseNotebook();

  const previewBtn = document.getElementById('btn-preview');
  const previewEl  = document.getElementById('preview');
  let previewOpen  = false;

  function buildPreviewText(){
    const install = buildInstallCell().source.join("");
    const cfg = buildConfigCell().source.join("");
    return `# === Install Cell ===\n${install}\n\n# === Config Cell ===\n${cfg}`;
  }

  function togglePreview(){
    if (previewOpen){
      // 收起
      previewEl.style.display = 'none';
      previewBtn.textContent = '預覽 Install + Config cell';
      previewEl.setAttribute('aria-hidden', 'true');
      previewBtn.setAttribute('aria-expanded', 'false');
    } else {
      // 展開
      previewEl.textContent = buildPreviewText();
      previewEl.style.display = 'block';
      previewBtn.textContent = '收起預覽';
      previewEl.setAttribute('aria-hidden', 'false');
      previewBtn.setAttribute('aria-expanded', 'true');
    }
    previewOpen = !previewOpen;
  }

  previewBtn.addEventListener('click', togglePreview);

  document.getElementById('btn-download').addEventListener('click', ()=>{
    const nb = buildNotebook(BASE_NB);
    const blob = new Blob([JSON.stringify(nb, null, 2)], {type:"application/json"});
    const a = document.createElement('a');
    const url = URL.createObjectURL(blob);
    a.href = url;
    a.download = "Local_LLM.ipynb";
    a.click();
    URL.revokeObjectURL(url);
  });
})();
</script>
