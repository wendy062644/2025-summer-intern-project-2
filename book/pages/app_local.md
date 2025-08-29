---
title: Local
thebe: false
---

# Local LLM 翻譯

```{raw} html
<style>
  .nbui *{box-sizing:border-box}
  .nbui{font-family:system-ui,-apple-system,Segoe UI,Roboto,"Noto Sans","PingFang TC","Microsoft JhengHei",sans-serif;line-height:1.45}
  .nbui h2{margin:.5rem 0 0.25rem}
  .nbui .card{border:1px solid #e5e7eb;border-radius:12px;padding:14px;background:#fff;margin:12px 0}
  .nbui .muted{color:#6b7280;font-size:13px}
  .nbui .grid{display:grid;gap:12px}
  .nbui .grid-2{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
  .nbui .grid-3{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
  /* 固定三欄：1:1:1 並排 */
  .nbui .grid-3-fixed{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
  @media (max-width:900px){ .nbui .grid-3-fixed{grid-template-columns:1fr 1fr} }
  @media (max-width:640px){ .nbui .grid-3-fixed{grid-template-columns:1fr} }

  .nbui label{font-size:14px;color:#374151;display:flex;flex-direction:column;gap:6px}
  .nbui input[type="text"], .nbui input[type="number"], .nbui select{
    padding:10px 12px;border:1px solid #d1d5db;border-radius:10px;min-width:200px
  }
  .nbui button{padding:10px 14px;border:1px solid #d1d5db;border-radius:10px;background:#fff;cursor:pointer}
  .nbui button:hover{background:#f3f4f6}
  .nbui pre.preview{white-space:pre-wrap;background:#f9fafb;border:1px solid #e5e7eb;padding:10px;border-radius:10px;margin-top:10px;display:none}
  .nbui .section{display:block;margin:6px 0 2px}
  .nbui .section h3{margin:.25rem 0 .25rem;font-size:15px;color:#374151;font-weight:600}
  .nbui .btn-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center}

  .nbui button{ color:#111827; }

  @media (prefers-color-scheme: dark){
    .nbui label{ color:#f0f1f3; }
    .nbui .section h3{ color:#f5f6f7; }
    .nbui .muted{ color:#c7ced8; }
    .nbui .card{ background:#111418; border-color:#2b2f36; color:#e5e7eb; }
    .nbui button{ background:#111418; border-color:#2b2f36; color:#e5e7eb; }
    .nbui button:hover{ background:#0b0f14; }
    .nbui pre.preview{ background:#0b0f14; border-color:#2b2f36; color:#e5e7eb; }
    .nbui input[type="text"], .nbui input[type="number"], .nbui select{
      background:#0b0f14; border-color:#2b2f36; color:#e5e7eb;
    }
  }
  html[data-theme="dark"] .nbui label{ color:#f0f1f3; }
  html[data-theme="dark"] .nbui .section h3{ color:#f5f6f7; }
  html[data-theme="dark"] .nbui .muted{ color:#c7ced8; }
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
            <option value="THUDM/glm-4-9b-chat" selected>THUDM/glm-4-9b-chat</option>
            <option value="taide/Llama-3.1-TAIDE-LX-8B-Chat">taide/Llama-3.1-TAIDE-LX-8B-Chat</option>
            <option value="Qwen/Qwen2.5-7B-Instruct">Qwen/Qwen2.5-7B-Instruct</option>
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
          <input id="maxTokens" type="number" min="1" value="8192">
        </label>
        <label>Min Tokens
          <input id="minTokens" type="number" min="1" value="256">
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
    nb.cells = [buildConfigCell(), ...nb.cells];
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

  function togglePreview(){
    if (previewOpen){
      // 收起
      previewEl.style.display = 'none';
      previewBtn.textContent = '預覽 Config cell';
      previewEl.setAttribute('aria-hidden', 'true');
      previewBtn.setAttribute('aria-expanded', 'false');
    } else {
      // 展開
      const cfg = buildConfigCell();
      previewEl.textContent = cfg.source.join("");
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