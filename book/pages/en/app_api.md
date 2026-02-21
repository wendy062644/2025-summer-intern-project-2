---
title: API
thebe: false
---

# ChatGPT API Translation

```{raw} html
<style>
  .bd-sidebar-secondary { display: none !important; }
  .bd-content,
  .bd-article-container,
  .tex2jax_ignore.mathjax_ignore {
    max-width: 100% !important;
    width: 100% !important;
  }
  /* —— Scope all styles inside #ts-ui only —— */
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
  #ts-ui .ts-input input,
  #ts-ui .ts-input select,
  #ts-ui .ts-input textarea{
    width:100%;
    padding:8px 10px;
    border:1px solid var(--ts-border);
    border-radius:10px;
    background:transparent;
    font-size:.95rem;
  }
  #ts-ui .ts-input select{
    appearance:none; -webkit-appearance:none; -moz-appearance:none;
  }
  #ts-ui .ts-input textarea{
    resize: vertical;
    min-height: 140px;
    line-height: 1.35;
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

  /* Secondary blocks */
  #ts-ui #ts-progress-wrap{ margin:12px 0; }

  #ts-ui #compare-box{
    border:1px solid var(--ts-border);
    border-radius:12px;
    padding:8px 12px;
    margin-top:8px;
    background:var(--ts-bg);
  }

  #ts-ui #compare-box table{
    width:100%;
    border-collapse:collapse;
    font-size:.95rem;
    table-layout: fixed;
  }

  #ts-ui #compare-box th,
  #ts-ui #compare-box td{
    padding:6px 6px;
    border-bottom:1px solid var(--ts-border);
    text-align:left;
    word-break: break-word;
    overflow-wrap: anywhere;
    white-space: normal;
  }

  #ts-ui #compare-box thead th{ font-weight:600; }

  #ts-ui #ts-ui-msg{
    color:var(--ts-muted);
    font-size:.95rem;
    margin-top:8px;
  }

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

  #ts-ui .ts-field{
    display: flex; flex-direction: column; gap: 6px;
  }
  #ts-ui .ts-field .ts-label{ margin: 0; }

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

  @media (max-width: 640px){
    #ts-ui .ts-row-3{ grid-template-columns: 1fr; }
  }
  #ts-ui .left-col{ grid-column: 1 / 3; }

  @media (max-width:640px){
    #ts-ui{ grid-template-columns: 1fr; }
    #ts-ui .left-col,
    #ts-ui .right-col{ grid-column: 1 / -1; }
  }

  @media (prefers-color-scheme: dark){
    #ts-ui{
      --ts-bg: #0f1115;
      --ts-surface: #111418;
      --ts-surface-2: #0b0f14;
      --ts-input-bg: #0b0f14;
      --ts-border: #2b2f36;
      --ts-text: #e7eaf0;
      --ts-muted: #a6afbd;
      --ts-link: #8ab4ff;
      --ts-code-bg: #0b0f14;
      --ts-code-fg: #e7eaf0;
      --ts-accent: #3b82f6;
      --ts-on-accent: #0b0f14;
      --ts-focus: 0 0 0 2px rgba(59,130,246,.35);
      --ts-progress-bg: #1a1f29;
      --ts-table-head-bg: #121621;
    }
  }
  html[data-theme="dark"] #ts-ui{
    --ts-bg: #0f1115;
    --ts-surface: #111418;
    --ts-surface-2: #0b0f14;
    --ts-input-bg: #0b0f14;
    --ts-border: #2b2f36;
    --ts-text: #e7eaf0;
    --ts-muted: #a6afbd;
    --ts-link: #8ab4ff;
    --ts-code-bg: #0b0f14;
    --ts-code-fg: #e7eaf0;
    --ts-accent: #3b82f6;
    --ts-on-accent: #0b0f14;
    --ts-focus: 0 0 0 2px rgba(59,130,246,.35);
    --ts-progress-bg: #1a1f29;
    --ts-table-head-bg: #121621;
  }

  #ts-ui .ts-card{
    background: var(--ts-surface);
    border-color: var(--ts-border);
    color: var(--ts-text);
  }

  #ts-ui .ts-label{ color: var(--ts-muted); }
  #ts-ui .ts-hint{ color: var(--ts-muted); }

  #ts-ui .ts-input input,
  #ts-ui .ts-input select,
  #ts-ui .ts-input textarea{
    background: var(--ts-input-bg);
    color: var(--ts-text);
    border-color: var(--ts-border);
  }

  #ts-ui .ts-input input:focus,
  #ts-ui .ts-input select:focus,
  #ts-ui .ts-input textarea:focus{
    outline: none;
    box-shadow: var(--ts-focus);
    border-color: color-mix(in oklab, var(--ts-accent) 60%, var(--ts-border));
  }

  #ts-ui .ts-btn-primary{
    background: var(--ts-accent);
    color: var(--ts-on-accent);
    border: 1px solid var(--ts-border);
  }
  #ts-ui .ts-btn-primary:hover{ filter: brightness(1.06); }
  #ts-ui .ts-btn-primary:focus{ outline: none; box-shadow: var(--ts-focus); }

  /* Pause button */
  #ts-ui .ts-btn-warning{
    background: #d97706; /* Amber 600 */
    color: #fff;
    border: 1px solid var(--ts-border);
  }
  #ts-ui .ts-btn-warning:hover{ filter: brightness(1.1); }

  #ts-ui #compare-box{
    background: var(--ts-surface);
    border-color: var(--ts-border);
  }
  #ts-ui #compare-box thead th{
    background: var(--ts-table-head-bg);
    color: var(--ts-text);
  }
  #ts-ui #compare-box td,
  #ts-ui #compare-box th{
    border-bottom: 1px solid var(--ts-border);
  }

  #ts-ui progress{ width:100%; height: 14px; background: var(--ts-progress-bg); border-radius: 8px; overflow: hidden; }
  #ts-ui progress::-webkit-progress-bar{ background: var(--ts-progress-bg); }
  #ts-ui progress::-webkit-progress-value{ background: var(--ts-accent); }
  #ts-ui progress::-moz-progress-bar{ background: var(--ts-accent); }

  #ts-ui code{
    background: var(--ts-code-bg);
    color: var(--ts-code-fg);
    padding: .1em .35em;
    border-radius: .35em;
    border: 1px solid var(--ts-border);
  }
  #ts-ui a{ color: var(--ts-link); text-underline-offset: 2px; }
  #ts-ui ::selection{
    background: color-mix(in oklab, var(--ts-accent) 35%, transparent);
  }

  @media (max-width:640px){
    html[data-theme="dark"] #ts-ui .ts-card,
    #ts-ui .ts-card{
      background: var(--ts-surface);
    }
  }
  #ts-ui .ts-field:has(#useModel2){
    flex-direction: row;
    align-items: center;
    gap: 10px;
  }
  #ts-ui .ts-field:has(#useModel2) .ts-label{ margin: 0 6px 0 0; }
  #ts-ui .ts-field:has(#useModel2) .ts-input{
    display: flex;
    align-items: center;
    gap: 10px;
  }
  #ts-ui #useModel2{
    width: 16px; height: 16px; margin: 0; vertical-align: middle;
  }
  @media (max-width:640px){
    #ts-ui .ts-field:has(#useModel2){
      flex-direction: column;
      align-items: stretch;
    }
  }

  /* Prompt accordion */
  #ts-ui details.ts-accordion{
    border: 1px solid var(--ts-border);
    border-radius: var(--ts-radius);
    background: var(--ts-surface, var(--ts-bg));
    overflow: hidden;
    margin-top: 10px;
  }

  #ts-ui details.ts-accordion > summary{
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    padding: 10px 12px;
    user-select: none;
    background: var(--ts-table-head-bg, var(--ts-bg));
    color: var(--ts-text);
  }

  #ts-ui details.ts-accordion > summary::-webkit-details-marker{ display:none; }

  #ts-ui details.ts-accordion > summary::after{
    content: "▸";
    margin-left: 10px;
    transform-origin: center;
    transition: transform .15s ease;
  }

  #ts-ui details.ts-accordion[open] > summary::after{
    transform: rotate(90deg);
  }

  #ts-ui details.ts-accordion[open] > summary{
    border-bottom: 1px solid var(--ts-border);
  }

  #ts-ui .ts-accordion-body{
    padding: 10px 12px 12px;
  }

  #ts-ui details.ts-accordion .ts-hint{
    margin-left: auto;
  }
</style>

<div id="ts-ui">
  <div class="ts-card">
    <div class="ts-title">API Settings</div>

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
        <label class="ts-label" for="modelSel">Model-1 (Translation)</label>
        <div class="ts-input">
          <div class="ts-inline" style="width:100%;">
            <select id="modelSel" style="flex:1;min-width:220px;">
              <optgroup label="GPT-5">
                <option value="gpt-5">gpt-5</option>
                <option value="gpt-5-mini">gpt-5-mini</option>
                <option value="gpt-5-nano">gpt-5-nano</option>
              </optgroup>
              <optgroup label="GPT-4.1">
                <option value="gpt-4.1">gpt-4.1</option>
                <option value="gpt-4.1-mini">gpt-4.1-mini</option>
                <option value="gpt-4.1-nano">gpt-4.1-nano</option>
              </optgroup>
              <optgroup label="GPT-4o">
                <option value="gpt-4o">gpt-4o</option>
                <option value="gpt-4o-mini" selected>gpt-4o-mini</option>
              </optgroup>
              <optgroup label="Reasoning">
                <option value="o1-mini">o1-mini</option>
                <option value="o3-mini">o3-mini</option>
              </optgroup>
              <optgroup label="Legacy">
                <option value="gpt-4-turbo">gpt-4-turbo</option>
                <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
              </optgroup>
              <optgroup label="Custom">
                <option value="__custom__">Other</option>
              </optgroup>
            </select>
            <input id="modelCustom" type="text" placeholder="e.g., my-org/gpt-xy" style="display:none;flex:1;">
          </div>
        </div>
      </div>
    </div>

    <div class="ts-row-2 ts-6-4" style="margin-top:10px;">
      <div class="ts-field">
        <div class="ts-input ts-inline">
          <label for="useModel2" class="ts-inline" style="gap:8px; align-items:center; white-space:nowrap;">
            <input type="checkbox" id="useModel2" checked>
            <span class="ts-label" style="margin:0;">Second model (selection + format fix)</span>
          </label>
          <span class="ts-hint" style="margin-left:8px; font-size: 12px">Choose the best candidate and fix formatting</span>
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" for="modelSel2">Model-2 (Selection / Review)</label>
        <div class="ts-input">
          <div class="ts-inline" style="width:100%;">
            <select id="modelSel2" style="flex:1;min-width:220px;">
              <optgroup label="GPT-5">
                <option value="gpt-5">gpt-5</option>
                <option value="gpt-5-mini">gpt-5-mini</option>
                <option value="gpt-5-nano">gpt-5-nano</option>
              </optgroup>
              <optgroup label="GPT-4.1">
                <option value="gpt-4.1">gpt-4.1</option>
                <option value="gpt-4.1-mini" selected>gpt-4.1-mini</option>
                <option value="gpt-4.1-nano">gpt-4.1-nano</option>
              </optgroup>
              <optgroup label="GPT-4o">
                <option value="gpt-4o">gpt-4o</option>
                <option value="gpt-4o-mini">gpt-4o-mini</option>
              </optgroup>
              <optgroup label="Reasoning">
                <option value="o1-mini">o1-mini</option>
                <option value="o3-mini">o3-mini</option>
              </optgroup>
              <optgroup label="Legacy">
                <option value="gpt-4-turbo">gpt-4-turbo</option>
                <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
              </optgroup>
              <optgroup label="Custom">
                <option value="__custom__">Other</option>
              </optgroup>
            </select>
            <input id="modelCustom2" type="text" placeholder="e.g., my-org/gpt-xy" style="display:none;flex:1;">
          </div>
        </div>
      </div>
    </div>

    <details class="ts-accordion" id="prompt-accordion">
      <summary>
        <span style="font-weight:600;">Prompt (System / Translation Rules)</span>
        <span class="ts-hint">Click to expand/collapse</span>
      </summary>

      <div class="ts-accordion-body">
        <div class="ts-field">
          <label class="ts-label" for="sysPrompt">Content</label>
          <div class="ts-input">
            <textarea id="sysPrompt" rows="10">You are a Taiwan GIS localization translator.
For each item, translate only the English content in the text field into Traditional Chinese (Taiwan usage).
You may use context and glossary for reference, but do not include context text (e.g., "UI: ." or "Note: .") in the output.
Please call the tool set_results and fill only the translated strings in order in the results array.
Preserve all ASCII half-width symbols (e.g., ()[]{};:,.?+/\*& etc.), and keep both count and order exactly the same as the source.
You must preserve all variables like ⟦M<number>⟧ and placeholders such as %1 and {0}; do not remove them or change their order.
If a string looks like a code variable, constant, enum name, function name, person name, or English acronym, prefer keeping it unchanged.
If the source contains a shortcut marker &X (X is a letter or number), do not output &X inside the translation; append (&X) at the end of the translation (no spaces), and X must match the source.
If no suitable or reliable Chinese translation is available, prefer keeping the original English instead of inventing terms.</textarea>
          </div>
          <div class="ts-hint">You can edit this. If left empty, the built-in default prompt will be used.</div>
        </div>
      </div>
    </details>

    <hr class="ts-divider">

    <div class="ts-title">Processing Parameters</div>
    <div class="ts-row-3 ts-3-4-3">
      <div class="ts-field">
        <label class="ts-label" for="batch">Batch</label>
        <div class="ts-input">
          <input type="number" id="batch" value="12" min="1" max="64">
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" for="limitN">Max items to process</label>
        <div class="ts-input ts-inline">
          <input type="number" id="limitN" value="0" style="max-width:220px;">
          <span id="countInfo" class="ts-hint"> / 0</span>
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" for="tsFile">.ts file (upload)</label>
        <div class="ts-input">
          <input type="file" id="tsFile" accept=".ts">
        </div>
      </div>
    </div>

    <div class="ts-row-2" style="--ts-col1: 7fr; --ts-col2: 3fr; margin-top:10px;">
      <div class="ts-field">
        <label class="ts-label" for="oldTsFile">Old .ts file</label>
        <div class="ts-input">
          <input type="file" id="oldTsFile" accept=".ts">
        </div>
      </div>
      <div class="ts-hint right-col" style="margin-top:26px;">
        Same <code>&lt;source&gt;</code> → reuse directly (no API call)
      </div>
    </div>

    <hr class="ts-divider">

    <div class="ts-title">Input Files</div>
    <div class="ts-row-2" style="--ts-col1: 7fr; --ts-col2: 3fr;">
      <div class="ts-field">
        <label class="ts-label" for="glsFile">Glossary (CSV / ODS)</label>
        <div class="ts-input">
          <input type="file" id="glsFile" accept=".csv,.ods" multiple>
        </div>
      </div>
      <div class="ts-field">
        <label class="ts-label" style="visibility:hidden;">Run Translation</label>
        <div class="ts-input ts-inline" style="gap:6px;">
          <button id="run-btn" class="ts-btn-primary" style="flex:2;">Run Translation</button>
          <button id="pause-btn" class="ts-btn-primary ts-btn-warning" style="flex:1; display:none;">Pause</button>
        </div>
      </div>
      <div class="ts-hint right-col" style="margin-top:6px;">
        Columns: <code>en, zh</code> or <code>英文名稱, 中文名稱</code>
      </div>
    </div>

    <div id="ts-progress-wrap" style="display:none;">
      <div class="ts-inline">
        <progress id="ts-progress" value="0" max="100" style="width:100%;"></progress>
        <span id="ts-progress-label" style="font-variant-numeric: tabular-nums;">0 / 0</span>
      </div>
    </div>

    <div id="compare-box" style="display:none;">
      <div style="font-size:0.95rem;color:var(--ts-text);margin-bottom:4px;">Translation comparison (live updates)</div>
      <div style="max-height: 360px; overflow:auto;">
        <table>
          <thead>
            <tr>
              <th style="width:50%;">Source (Context)</th>
              <th style="width:50%;">Translation</th>
            </tr>
          </thead>
          <tbody id="compare-tbody"></tbody>
        </table>
      </div>
    </div>

    <div id="ts-ui-msg"></div>
  </div>
</div>

<script>
async function __tsui_init(){
  const __root = document.getElementById("ts-ui");
  if (!__root) return;

  if (__root.dataset.inited === "1") return;

  const $ = (id) => document.getElementById(id);

  const tsFile = $("tsFile");
  const oldTsFile = $("oldTsFile");
  const limitN = $("limitN");
  const countInfo = $("countInfo");
  const runBtn = $("run-btn");
  const pauseBtn = $("pause-btn");
  const $msg = $("ts-ui-msg");

  if (!tsFile || !oldTsFile || !limitN || !countInfo || !runBtn || !pauseBtn || !$msg) {
    console.warn("[ts-ui] DOM not ready / missing nodes");
    return;
  }

  window.__TSUI_INITED__ = true;
  __root.dataset.inited = "1";

  // ---------- 1) Bind UI events first (without waiting for pyodide) ----------
  function needsTranslationJS(text){
    const t = (text ?? "").toString().trim();
    if (!t) return false;
    if (/^[\s\p{N}\p{P}\p{S}_]+$/u.test(t)) return false;
    return true;
  }

  function isTranslationFilledJS(msg){
    const tr = msg.getElementsByTagName("translation")[0];
    if (!tr) return false;
    if (tr.getAttribute("type") === "unfinished") return false;

    const numerus = (msg.getAttribute("numerus") === "yes");
    if (numerus){
      const forms = tr.getElementsByTagName("numerusform");
      if (forms && forms.length){
        for (const f of forms){
          if (!((f.textContent || "").trim())) return false;
        }
        return true;
      }
    }
    return !!((tr.textContent || "").trim());
  }

  function buildOldIndexJS(oldDoc){
    // source -> (ctx_name -> valKey)
    const idx = new Map();
    if (!oldDoc) return idx;

    for (const ctx of oldDoc.getElementsByTagName("context")){
      const nameNode = ctx.getElementsByTagName("name")[0];
      const ctxName = ((nameNode?.textContent) || "").trim();

      for (const m of ctx.getElementsByTagName("message")){
        const srcNode = m.getElementsByTagName("source")[0];
        const srcText = srcNode?.textContent;
        if (!srcText || !srcText.trim()) continue;

        const tr = m.getElementsByTagName("translation")[0];
        if (!tr) continue;
        if (tr.getAttribute("type") === "unfinished") continue;

        const numerus = (m.getAttribute("numerus") === "yes");
        let val;
        if (numerus){
          const forms = tr.getElementsByTagName("numerusform");
          if (forms && forms.length){
            const vals = Array.from(forms).map(f => (f.textContent || "").trim());
            if (!vals.every(v => v)) continue;
            val = "A:" + vals.join("\u0001");
          } else {
            const t = (tr.textContent || "").trim();
            if (!t) continue;
            val = "S:" + t;
          }
        } else {
          const t = (tr.textContent || "").trim();
          if (!t) continue;
          val = "S:" + t;
        }

        if (!idx.has(srcText)) idx.set(srcText, new Map());
        idx.get(srcText).set(ctxName, val);
      }
    }
    return idx;
  }

  function canReuseOldJS(oldMap, srcText, ctxName){
    if (!oldMap || !srcText) return false;
    const perCtx = oldMap.get(srcText);
    if (!perCtx) return false;
    if (perCtx.has(ctxName)) return true;

    const uniq = new Set(perCtx.values());
    return uniq.size === 1;
  }

  async function readFileTextById(inputId){
    const el = document.getElementById(inputId);
    if (!el?.files || el.files.length === 0) return null;
    const buf = await el.files.item(0).arrayBuffer();
    return new TextDecoder("utf-8").decode(buf);
  }

  tsFile.addEventListener("change", handleTsChange);
  oldTsFile.addEventListener("change", handleTsChange);

  async function handleTsChange(){
    if (window._TS_RUNNING){
      window._TS_ABORT = true;
      window._TS_PAUSED = false; // avoid getting stuck in paused state
      pauseBtn.textContent = "Pause";
      pauseBtn.style.background = "#d97706";
      $msg.innerHTML = "<span style='color:#b00'>File change detected: cancelling current task. Please run again shortly.</span>";
    }

    const file = tsFile.files && tsFile.files[0];
    if (!file){ countInfo.textContent = " / 0"; limitN.removeAttribute("max"); return; }

    try{
      const txt = await file.text();
      let total = 0;

      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(txt, "application/xml");
      const hasErr = xmlDoc.getElementsByTagName("parsererror").length > 0;

      if (!hasErr){
        const contexts = xmlDoc.getElementsByTagName("context");
        for (let c = 0; c < contexts.length; c++){
          const ctx = contexts[c];
          const messages = ctx.getElementsByTagName("message");
          for (let i = 0; i < messages.length; i++){
            const m = messages[i];
            const src = m.getElementsByTagName("source")[0];
            if (!src) continue;
            const s = src.textContent || "";
            if (!needsTranslationJS(s)) continue;
            total++;
          }
        }
      } else {
        const srcMatches = txt.match(/<message[\s\S]*?<\/message>/g) || [];
        for (const block of srcMatches){
          const msrc = block.match(/<source>([\s\S]*?)<\/source>/);
          if (!msrc) continue;
          const s = msrc[1].replace(/<[^>]+>/g, "");
          if (!needsTranslationJS(s)) continue;
          total++;
        }
      }

      if (total > 0){
        limitN.value = String(total);
        limitN.max = String(total);
        countInfo.textContent = ` / ${total}`;
      } else {
        countInfo.textContent = " / 0";
        limitN.removeAttribute("max");
      }
    } catch(e){
      console.error(e);
      countInfo.textContent = " / 0";
      limitN.removeAttribute("max");
    }
  }

  function clampLimit(){
    const max = Number(limitN.max || "0");
    let v = Number(limitN.value || "0");
    if (max){
      if (v > max) v = max;
      if (v < 0) v = 0;
      limitN.value = v;
    } else if (v < 0){
      limitN.value = 0;
    }
  }

  limitN.addEventListener("input", clampLimit);

  try { await handleTsChange(); } catch(e){ console.warn(e); }

  (function setupModelCustom(){
    const sel = $("modelSel");
    const custom = $("modelCustom");
    function sync(){ custom.style.display = (sel.value === "__custom__") ? "block" : "none"; }
    sel.addEventListener("change", sync);
    sync();
  })();

  (function setupModelCustom2(){
    const sel = $("modelSel2");
    const custom = $("modelCustom2");
    function sync(){ custom.style.display = (sel.value === "__custom__") ? "block" : "none"; }
    sel.addEventListener("change", sync);
    sync();
  })();

  // Pause logic
  window._TS_PAUSED = false;
  pauseBtn.addEventListener("click", () => {
    window._TS_PAUSED = !window._TS_PAUSED;
    if (window._TS_PAUSED){
      pauseBtn.textContent = "Resume";
      pauseBtn.style.background = "#059669";
    } else {
      pauseBtn.textContent = "Pause";
      pauseBtn.style.background = "#d97706";
    }
  });

  // ---------- 2) Load Pyodide (dynamic import to avoid Jupyter Book module/reflow issues) ----------
  runBtn.disabled = true;
  runBtn.textContent = "Loading environment...";

  let pyodide;
  try{
    const mod = await import("https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.mjs");
    pyodide = await mod.loadPyodide();
    await pyodide.loadPackage("micropip");

    runBtn.disabled = true;
    runBtn.textContent = "Initializing translator...";
  } catch(e){
    console.error(e);
    $msg.innerHTML = `<span style="color:#b00">Failed to load Python: ${String(e)}</span>`;
    // (Optional) allow retry initialization later
    __root.dataset.inited = "";
    window.__TSUI_INITED__ = false;
    return;
  }

  try{
    await pyodide.runPythonAsync(String.raw`
import asyncio, json, re, io, base64, traceback, html, csv, zipfile
from typing import List, Tuple, Dict, Optional, Any
from xml.etree import ElementTree as ET
from js import document, window
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy

# Install opencc (first time may take longer)
import micropip
await micropip.install("opencc-python-reimplemented==0.1.7")
from opencc import OpenCC

_OPENCC = OpenCC("s2twp")

_TW_PROTECT_TERMS = ["演算法", "專案", "圖層", "外掛", "外掛程式", "巨集", "快取", "佈局", "拓撲", "向量", "網格", "波段"]
_COORD_RE = re.compile(r"坐標")

_MASK_PAT = re.compile(
    r'(</?[A-Za-z][^>]*>|&lt;/?[A-Za-z][^&]*?&gt;|&(?!\s)[A-Za-z#x0-9]+;)',
    re.IGNORECASE
)
_SEP_RE = re.compile(r"[-\s/_.\\]+")
_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[\\/_.-][A-Za-z0-9]+)*")

# Shortcut key: &X (ignore &&)
_MNEMONIC_RE = re.compile(r"(?<!&)&([A-Za-z0-9])")

# Preferred terms: post-processing force replacement
_TERM_REPL: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"插件"), "外掛程式"),
    (re.compile(r"凸殼"), "凸包"),
    (re.compile(r"處理中"), "處理"),
    (re.compile(r"\bLineString\b", re.IGNORECASE), "線串"),
    (re.compile(r"\bBase\s+level\b", re.IGNORECASE), "基準值"),
    (re.compile(r"\bArrow\s+head\b", re.IGNORECASE), "箭頭端"),
    (re.compile(r"\bLine\s+alignment\b", re.IGNORECASE), "線條對齊"),
    (re.compile(r"\bModel\s+scale\b", re.IGNORECASE), "模型縮放比例"),
    (re.compile(r"\bRow\b", re.IGNORECASE), "列"),
    (re.compile(r"\bpixels\b", re.IGNORECASE), "像素"),
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

    # Remove any existing trailing shortcut marker
    t = re.sub(r"\s*\(&[A-Za-z0-9]\)\s*$", "", t).strip()
    # Remove in-text same-key & marker
    t = t.replace(f"&{key}", "")
    # Append correct suffix
    return (t + suffix)

# ====== Basic utilities ======
def to_zh_tw(s: Optional[str]) -> str:
    if not s: return ""
    text = s
    placeholders = {}
    for i, term in enumerate(_TW_PROTECT_TERMS):
        key = f"⟦TP{i}⟧"
        placeholders[key] = term
        text = text.replace(term, key)
    try:
        text = _OPENCC.convert(text)
    except Exception:
        pass
    for key, term in placeholders.items():
        text = text.replace(key, term)
    return text

def normalize_zh(s: Optional[str]) -> str:
    if not s: return ""
    try:
        return _COORD_RE.sub("座標", s)
    except Exception:
        return s

def fix_zh_punct(s: Optional[str]) -> str:
    if not s:
        return ""
    return s.replace("（", "(").replace("）", ")").replace("：", ":").strip()

def strip_all_newlines(s: Optional[str]) -> str:
    if not s: return ""
    return s.replace("\\n", "").replace("\\r", "").replace("\n", "").replace("\r", "")

# Prevent leaking Context into translation; protect enum/code-like identifiers
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

# ====== Placeholder handling (KEEP ONLY ONE VERSION) ======
_PLACEHOLDER_PAT = re.compile(r"(%L\d+|%\d+|%[sdn]|\{\d+\})")

def _ph_list(s: str) -> List[str]:
    return _PLACEHOLDER_PAT.findall(s or "")

def validate_placeholders(src: str, trans: str) -> bool:
    # Must match in exact order (avoid swapping %1 / %2)
    return _ph_list(src) == _ph_list(trans)

def repair_placeholders(src: str, trans: str) -> tuple[str, bool]:
    src_ph = _ph_list(src)
    tr_ph  = _ph_list(trans)

    if not src_ph and not tr_ph:
        return trans, True
    if len(src_ph) != len(tr_ph):
        return trans, False

    out: List[str] = []
    last = 0
    for i, m in enumerate(_PLACEHOLDER_PAT.finditer(trans or "")):
        out.append((trans or "")[last:m.start()])
        out.append(src_ph[i])
        last = m.end()
    out.append((trans or "")[last:])

    fixed = "".join(out)
    return fixed, (_ph_list(fixed) == src_ph)

def restore_leading_symbols(src: str, trans: str) -> str:
    m = re.match(r"^([)\]};:,.|]+)", src or "")
    if not m:
        return trans
    head = m.group(1)
    if trans.startswith(head):
        return trans
    for i in range(len(head)):
        suffix = head[i:]
        if trans.startswith(suffix):
            return head[:i] + trans
    return head + trans

# ====== UI Functions ======
def _set_ui_msg(msg_html: str):
    document.getElementById("ts-ui-msg").innerHTML = msg_html

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
    while tbody.firstChild:
        tbody.removeChild(tbody.firstChild)

def _compare_add(src_text:str, zh_text:str, context_info:str="", tag:str=""):
    box = document.getElementById("compare-box")
    box.style.display = "block"
    tbody = document.getElementById("compare-tbody")
    tr = document.createElement("tr")

    def _td(txt, is_html=False):
        td = document.createElement("td")
        td.style.padding = "4px"
        td.style.borderBottom = "1px solid #eee"
        if is_html:
            td.innerHTML = txt
        else:
            td.textContent = txt
        return td

    display_src = src_text
    meta = []
    if tag:
        meta.append(tag)
    if context_info:
        meta.append(context_info)

    if meta:
        header = " | ".join(meta)
        display_src = (
            "<div style='font-size:0.8em; color:#666; margin-bottom:2px; "
            "padding:1px 4px; background:#f3f4f6; border-radius:4px; display:inline-block;'>"
            f"{html.escape(header)}</div><br>{html.escape(src_text)}"
        )
        tr.appendChild(_td(display_src, is_html=True))
    else:
        tr.appendChild(_td(src_text))

    tr.appendChild(_td(zh_text))
    tbody.appendChild(tr)

# ====== Masking ======
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

def _et_ready(s:str) -> str:
    try:
        return html.unescape(s)
    except Exception:
        return s

def needs_translation(en_text: Optional[str]) -> bool:
    if not en_text or not en_text.strip():
        return False
    # If only whitespace / digits / symbols, no translation needed
    if re.fullmatch(r"[\s\W\d_]+", en_text):
        return False
    return True

def soft_norm(s:str) -> str:
    return _SEP_RE.sub(" ", s.lower()).strip()

# ====== glossary: LCS-ish ======
class LCSMatcher:
    def __init__(self, pairs: List[Tuple[str,str]], min_token_len:int=4, min_lcs_len:int=4):
        rows = []
        for en, zh in pairs:
            en = (en or "").strip()
            zh = (zh or "").strip()
            if en and zh:
                en_norm = en.lower()
                charset = set(re.sub(r"\s+", "", en_norm))
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

    def build_glossary_sentence_first(self, text:str, *, limit:int=12, per_word_k:int=3, min_lcs_len:int=4) -> Dict[str,str]:
        text_clean = _MASK_PAT.sub(" ", text)
        tokens = _TOKEN_RE.findall(text_clean)
        toks_lc = [t.lower() for t in tokens]
        n = len(toks_lc)
        covered = [False]*n
        glossary = {}
        def _mark(i,j):
            for k in range(i,j):
                covered[k] = True
        win_max = min(n, self.max_soft_len)
        for w in range(win_max, 0, -1):
            if len(glossary) >= limit:
                break
            for i in range(0, n-w+1):
                if any(covered[k] for k in range(i,i+w)):
                    continue
                phrase = " ".join(toks_lc[i:i+w])
                key = soft_norm(phrase)
                if key in self.soft_index:
                    en, zh = self.soft_index[key]
                    if en not in glossary:
                        glossary[en] = zh
                        _mark(i,i+w)
                        if len(glossary) >= limit:
                            break
        for idx, tok in enumerate(tokens):
            if len(glossary) >= limit:
                break
            if covered[idx]:
                continue
            if len(tok) < min_lcs_len:
                continue
            for r in self._topk_for_word(tok, k=per_word_k):
                if r["lcs_len"] >= min_lcs_len and r["en"] not in glossary:
                    glossary[r["en"]] = r["zh"]
                    covered[idx] = True
                    if len(glossary) >= limit:
                        break
        return glossary

    def _topk_for_word(self, token:str, k:int=3) -> List[Dict]:
        t_norm = token.lower()
        if len(t_norm) < self.min_token_len:
            return []
        t_chars = set(t_norm)
        cand = [r for r in self.rows if len(t_chars & r["charset"]) > 0]
        res = []
        def anchored_prefix_sub_in(token_norm:str, cand_norm:str):
            if not token_norm or not cand_norm:
                return 0,""
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
        res.sort(key=lambda d: (-d["lcs_len"], len(d["en"])) )
        return res[:k]

# ===== Read CSV / ODS =====
def load_glossary_csv_text(csv_text: Optional[str]) -> List[Tuple[str,str]]:
    if not csv_text:
        return []
    rdr = csv.DictReader(io.StringIO(csv_text))
    if not rdr.fieldnames:
        return []
    col_en = col_zh = None
    for c in rdr.fieldnames or []:
        cc = (c or "").strip().lower()
        if cc in ("en", "英文名稱"):
            col_en = c
        if cc in ("zh", "中文名稱"):
            col_zh = c
    if not col_en or not col_zh:
        return []
    pairs = []
    seen = set()
    for row in rdr:
        en = (row.get(col_en) or "").strip()
        zh = (row.get(col_zh) or "").strip()
        if en and zh and en not in seen:
            zh = normalize_zh(to_zh_tw(zh))
            pairs.append((en, zh))
            seen.add(en)
    return pairs

def load_glossary_ods_bytes(ods_bytes: bytes) -> List[Tuple[str,str]]:
    with zipfile.ZipFile(io.BytesIO(ods_bytes)) as z:
        xml = z.read("content.xml")
    ns = {
        "office":"urn:oasis:names:tc:opendocument:xmlns:office:1.0",
        "table":"urn:oasis:names:tc:opendocument:xmlns:table:1.0",
        "text":"urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    }
    root = ET.fromstring(xml)
    table = root.find(".//table:table", ns)
    if table is None:
        return []
    rows = table.findall("table:table-row", ns)
    def cell_text(cell):
        parts = []
        for p in cell.findall(".//text:p", ns):
            parts.append("".join(p.itertext()))
        return (parts[0] if parts else "").strip()
    if not rows:
        return []
    header_cells = rows[0].findall("table:table-cell", ns)
    headers = [cell_text(c) for c in header_cells]
    def _find_idx(names:set):
        for i,h in enumerate(headers):
            if (h or "").strip().lower() in names:
                return i
        return -1
    idx_en = _find_idx({"英文名稱","en"})
    idx_zh = _find_idx({"中文名稱","zh"})
    if idx_en < 0 or idx_zh < 0:
        return []
    pairs = []
    seen = set()
    for r in rows[1:]:
        cells = r.findall("table:table-cell", ns)
        if idx_en >= len(cells) or idx_zh >= len(cells):
            continue
        en = cell_text(cells[idx_en]).strip()
        zh = cell_text(cells[idx_zh]).strip()
        if en and zh and en not in seen:
            zh = normalize_zh(to_zh_tw(zh))
            pairs.append((en, zh))
            seen.add(en)
    return pairs

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
                pairs_all.extend(load_glossary_csv_text(b.decode("utf-8","ignore")))
        except Exception as e:
            print(f"Glossary error: {e}")
    seen = set()
    dedup = []
    for en, zh in pairs_all:
        if en not in seen:
            dedup.append((en, zh))
            seen.add(en)
    return dedup

# ===== OpenAI API call =====
async def call_api(api_key, base_url, model, payload, retries=1):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    url = base_url.rstrip("/") + "/chat/completions"

    mname = (model or "").lower()
    is_o1_o3 = mname.startswith("o1") or mname.startswith("o3")
    is_gpt5  = mname.startswith("gpt-5")

    if is_o1_o3:
        new_msgs = []
        for m in payload.get("messages", []):
            if m["role"] == "system":
                new_msgs.append({"role": "user", "content": f"[System Instruction]\\n{m['content']}"} )
            else:
                new_msgs.append(m)
        payload["messages"] = new_msgs

    if is_o1_o3 or is_gpt5:
        payload.pop("temperature", None)
        payload.pop("top_p", None)
        payload.pop("presence_penalty", None)
        payload.pop("frequency_penalty", None)
        payload.pop("logit_bias", None)
        if "max_tokens" in payload and "max_completion_tokens" not in payload:
            payload["max_completion_tokens"] = payload.pop("max_tokens")

    for _ in range(retries + 1):
        try:
            resp = await pyfetch(url, method="POST", headers=headers, body=json.dumps(payload))
            data = await resp.json()
            if resp.status >= 400:
                raise Exception(f"API Error {resp.status}: {data.get('error', {}).get('message')}")

            choice = data["choices"][0]
            if choice["message"].get("tool_calls"):
                arg_str = choice["message"]["tool_calls"][0]["function"]["arguments"]
                return json.loads(arg_str)
            if choice["message"].get("content"):
                return json.loads(choice["message"]["content"])
        except Exception as e:
            if _ == retries:
                return None
            await asyncio.sleep(1)
    return None

# ===== TS utilities =====
def _read_doctype(xml_text: str) -> str:
    m = re.search(r'<!DOCTYPE[^>]+>', xml_text or "")
    return m.group(0) if m else ""

def _strip_doctype(xml_text: str) -> str:
    return re.sub(r'<!DOCTYPE[^>]+>', '', xml_text or '')

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
    tr = msg.find("translation")
    if tr is None:
        tr = ET.SubElement(msg, "translation")
    # Remove unfinished
    tr.attrib.pop("type", None)

    numerus = (msg.get("numerus") == "yes")
    if numerus:
        forms = tr.findall("numerusform")
        if not forms:
            # Create at least one
            forms = [ET.SubElement(tr, "numerusform")]
        if isinstance(text_or_list, list):
            # Align count (pad with last value if needed)
            vals = text_or_list[:]
            if len(vals) < len(forms):
                vals += [vals[-1] if vals else ""] * (len(forms) - len(vals))
            for f, v in zip(forms, vals):
                f.text = v
        else:
            # Single string: apply to all forms
            for f in forms:
                f.text = str(text_or_list)
    else:
        tr.text = str(text_or_list)

def build_old_index(old_ts_text: str) -> Dict[str, Dict[str, Any]]:
    # source -> ctx_name -> translation (str or list)
    idx: Dict[str, Dict[str, Any]] = {}
    if not old_ts_text:
        return idx

    s = _strip_doctype(old_ts_text)
    try:
        root = ET.fromstring(s)
    except Exception:
        return idx

    for ctx in root.findall("context"):
        ctx_name_node = ctx.find("name")
        ctx_name = (ctx_name_node.text if (ctx_name_node is not None and ctx_name_node.text) else "").strip()

        for m in ctx.findall("message"):
            src_node = m.find("source")
            if src_node is None or src_node.text is None:
                continue
            src_text = src_node.text
            if not (src_text and src_text.strip()):
                continue

            tr = m.find("translation")
            if tr is None:
                continue
            if tr.get("type") == "unfinished":
                continue

            numerus = (m.get("numerus") == "yes")
            if numerus:
                forms = tr.findall("numerusform")
                if forms:
                    vals = [(f.text or "").strip() for f in forms]
                    if not all(vals):
                        continue
                    val: Any = vals
                else:
                    val = (tr.text or "").strip()
                    if not val:
                        continue
            else:
                val = (tr.text or "").strip()
                if not val:
                    continue

            idx.setdefault(src_text, {})[ctx_name] = val

    return idx

def pick_old_translation(old_map: Dict[str, Dict[str, Any]], src: str, ctx_name: str) -> Optional[Any]:
    if not old_map or not src:
        return None
    per_ctx = old_map.get(src)
    if not per_ctx:
        return None
    if ctx_name in per_ctx:
        return per_ctx[ctx_name]

    # If same source has a single unique translation across contexts, reuse safely
    uniq = []
    for _, v in per_ctx.items():
        if v not in uniq:
            uniq.append(v)
    if len(uniq) == 1:
        return uniq[0]
    return None

# ====== Main pipeline ======
async def _read_file_text(input_id: str) -> Optional[str]:
    files = document.getElementById(input_id).files
    if not files or files.length == 0:
        return None
    buf = await files.item(0).arrayBuffer()
    return bytes(buf.to_py()).decode("utf-8", "ignore")

async def run_translation_pipeline_async(
    api_key:str, base_url:str, model1:str,
    ts_text:str,
    glossary_pairs:List[Tuple[str,str]],
    batch_size:int=32,
    limit_n:int=0,
    use_model2:bool=False,
    model2:str="",
    old_ts_text: Optional[str]=None,
    sys_prompt_override: Optional[str]=None
) -> bytes:
    doctype = _read_doctype(ts_text)
    ts_no_dt = _strip_doctype(ts_text)
    root = ET.fromstring(ts_no_dt)

    old_map = build_old_index(old_ts_text or "")

    matcher = LCSMatcher(glossary_pairs, min_token_len=4, min_lcs_len=4)

    tasks = []
    reused = 0

    # Scan first: reuse old translations where possible, queue the rest
    for ctx in root.findall("context"):
        ctx_name_node = ctx.find("name")
        ctx_name = (ctx_name_node.text if (ctx_name_node is not None and ctx_name_node.text) else "").strip()

        for m in ctx.findall("message"):
            src_node = m.find("source")
            if src_node is None or src_node.text is None:
                continue
            src_text = src_node.text

            if not needs_translation(src_text):
                continue

            # Reuse old translation
            old_val = pick_old_translation(old_map, src_text, ctx_name)
            if old_val is not None:
                set_translation(m, old_val)
                reused += 1
                _compare_add(
                    src_text,
                    str(old_val[0] if isinstance(old_val, list) and old_val else old_val),
                    f"UI: {ctx_name}",
                    tag="Reused old"
                )
                continue

            # Needs translation
            extras = []
            if ctx_name:
                extras.append(f"UI: {ctx_name}")
            cmt = m.find("comment")
            if cmt is not None and cmt.text:
                extras.append(f"Comment: {cmt.text}")
            ext = m.find("extracomment")
            if ext is not None and ext.text:
                extras.append(f"Note: {ext.text}")
            ctx_str = " | ".join(extras)

            tasks.append({
                "node": m,
                "src": src_text,
                "context": ctx_str,
                "ctx_name": ctx_name,
                "numerus": (m.get("numerus") == "yes"),
            })

            if limit_n > 0 and len(tasks) >= limit_n:
                break
        if limit_n > 0 and len(tasks) >= limit_n:
            break

    total = len(tasks)
    finished = 0

    if total == 0:
        xml_bytes = ET.tostring(root, encoding="utf-8")
        head = b'<?xml version="1.0" encoding="utf-8"?>'
        if doctype:
            xml_bytes = head + b"\n" + doctype.encode("utf-8") + b"\n" + xml_bytes
        else:
            xml_bytes = head + b"\n" + xml_bytes
        return xml_bytes

    _compare_reset()
    _progress_setup(total)

    tools_schema = [{
        "type": "function",
        "function": {
            "name": "set_results",
            "description": "Save translations",
            "parameters": {
                "type": "object",
                "properties": {
                    "results": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["results"]
            }
        }
    }]

    # Translation system prompt: includes shortcut key rule and term preferences
    DEFAULT_SYS_PROMPT  = (
"You are a Taiwan GIS localization translator."
" For each item, translate only the English content in the text field into Traditional Chinese (Taiwan usage)."
" You may use context and glossary for reference, but do not include context text (e.g., 'UI: .' or 'Comment: .') in the output."
" Please call the tool set_results and put only translated strings in the results array in order."
" Preserve all ASCII half-width symbols (e.g., ()[]{};:,.?+/\\\\*& etc.), with exactly the same count and order as the source."
" You must preserve all variables like ⟦M<number>⟧ and placeholders such as %1 and {0}; do not remove or reorder them."
" If a string looks like a code variable, constant, enum name, function name, person name, or English acronym, prefer leaving it unchanged."
" If the source contains a shortcut marker &X, append (&X) to the end of the translation, and do not leave any other &X inside the translation."
" If uncertain, prefer outputting the original text."
    )
    sys_prompt = (sys_prompt_override or "").strip() or DEFAULT_SYS_PROMPT

    # If Model-2 is disabled: local A/B/C selection (focus on placeholder/format integrity)
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
            # Rough bonus for fewer full-width punctuation marks
            if "（" not in cand and "）" not in cand and "：" not in cand:
                sc += 30
            # Slight penalty for overly long output
            sc -= max(0, len(cand) - len(src)) // 10
            if sc > best_score:
                best_score = sc
                best = cand
        return best

    def _postprocess_one(src_text: str, raw_zh: str, mp: Dict[str, str], ctx_str: str) -> str:
        zh = (raw_zh or "").strip()
        zh = _et_ready(zh)
        zh = strip_all_newlines(zh)

        zh = _unmask_text(zh, mp)

        zh = to_zh_tw(zh)
        zh = normalize_zh(zh)
        zh = apply_term_preferences(zh)
        zh = fix_zh_punct(zh)

        zh = apply_mnemonic_rule(src_text, zh)

        zh = fix_context_leak(src_text, zh, ctx_str)

        zh = restore_leading_symbols(src_text, zh)
        fixed, ok = repair_placeholders(src_text, zh)
        if ok:
            zh = fixed

        if not validate_placeholders(src_text, zh):
            zh = src_text

        return zh

    for start in range(0, total, batch_size):
        while window._TS_PAUSED:
            await asyncio.sleep(0.2)

        batch = tasks[start:start + batch_size]
        masked_inputs: List[str] = []
        maps: List[Dict[str, str]] = []
        context_list: List[str] = []
        gls_list: List[List[str]] = []

        for item in batch:
            src_text = item["src"]
            g = matcher.build_glossary_sentence_first(src_text)
            gls_list.append([f"{k}->{v}" for k, v in g.items()])

            m_txt, mp = _mask_text(src_text)
            masked_inputs.append(m_txt)
            maps.append(mp)

            context_list.append(item["context"])

        items_json = json.dumps(
            [{"id": k, "text": txt, "context": ctx, "glossary": gls}
             for k, (txt, ctx, gls) in enumerate(zip(masked_inputs, context_list, gls_list))],
            ensure_ascii=False
        )
        user_prompt = f"Translate the following items one by one. Translate only the text field and output array results:\\n{items_json}"

        # =========================================================
        # Get raw zh_list
        # =========================================================
        zh_list: List[str] = []

        if use_model2 and model2:
            # --- Model-1: A/B/C (three passes) ---
            temps = [0.2, 0.7, 1.0]
            payloads = [{
                "model": model1,
                "temperature": t,
                "tools": tools_schema,
                "tool_choice": {"type": "function", "function": {"name": "set_results"}},
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            } for t in temps]

            resA, resB, resC = await asyncio.gather(
                call_api(api_key, base_url, model1, payloads[0]),
                call_api(api_key, base_url, model1, payloads[1]),
                call_api(api_key, base_url, model1, payloads[2]),
            )

            listA = (resA.get("results", []) if resA else [])
            listB = (resB.get("results", []) if resB else [])
            listC = (resC.get("results", []) if resC else [])

            def _pad(lst: List[str]) -> List[str]:
                if len(lst) < len(batch):
                    lst = lst + [""] * (len(batch) - len(lst))
                return lst[:len(batch)]

            listA, listB, listC = _pad(listA), _pad(listB), _pad(listC)

            # --- Model-2: arbitration + format correction (one pass) ---
            sel_items = [{
                "id": i,
                "src": it["src"],
                "context": it["context"],
                "glossary": gls_list[i],
                "A": listA[i],
                "B": listB[i],
                "C": listC[i],
            } for i, it in enumerate(batch)]

            sel_payload = {
                "model": model2,
                "temperature": 0.1,
                "tools": tools_schema,
                "tool_choice": {"type": "function", "function": {"name": "set_results"}},
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a strict reviewer and arbiter."
                            " For each item, choose the best translation from A/B/C; if needed, combine strengths and fix formatting."
                            " Must preserve placeholders and ASCII symbol order/count. Do not output context text."
                            " If source contains &X, append (&X) at the end and do not leave other &X inside."
                            " Preferred terms: 插件→外掛程式, 凸殼→凸包, 處理中→處理, LineString→線串, Base level→基準值, "
                            "Arrow head→箭頭端, Line alignment→線條對齊, Model scale→模型縮放比例, Row→列, pixels→像素."
                            " If unsure, output the source text."
                            " Call set_results and output results array only (strings)."
                        )
                    },
                    {"role": "user", "content": json.dumps(sel_items, ensure_ascii=False)}
                ]
            }

            res_final = await call_api(api_key, base_url, model2, sel_payload)
            zh_list = (res_final.get("results", []) if res_final else [])

            # Fallback: if Model-2 fails, choose locally from A/B/C
            if not zh_list:
                zh_list = [local_pick_best(it["src"], [listA[i], listB[i], listC[i]]) for i, it in enumerate(batch)]

        else:
            # --- No second model: Model-1 translates once ---
            payload = {
                "model": model1,
                "temperature": 0.2,
                "tools": tools_schema,
                "tool_choice": {"type": "function", "function": {"name": "set_results"}},
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            res1 = await call_api(api_key, base_url, model1, payload)
            zh_list = (res1.get("results", []) if res1 else [])

        # Align length
        if len(zh_list) < len(batch):
            zh_list = zh_list + [""] * (len(batch) - len(zh_list))
        zh_list = zh_list[:len(batch)]

        # =========================================================
        # Write back to XML + update UI/progress
        # =========================================================
        for i, item in enumerate(batch):
            src_text = item["src"]
            ctx_str = item["context"]
            ctx_name = item.get("ctx_name", "") or ""

            zh_raw = zh_list[i]
            zh_final = _postprocess_one(src_text, zh_raw, maps[i], ctx_str)

            set_translation(item["node"], zh_final)
            finished += 1
            _progress_tick(finished, total)

            show_zh = " / ".join(zh_final) if isinstance(zh_final, list) else (zh_final or "")
            tag = "Model-2" if use_model2 else "Model-1"

            _compare_add(
                src_text,
                show_zh,
                ctx_str,
                tag=tag
            )

        _set_ui_msg(f"Progress: {finished}/{total} (reused from old file: {reused})")

    xml_bytes = ET.tostring(root, encoding="utf-8")
    head = b'<?xml version="1.0" encoding="utf-8"?>'
    if doctype:
        xml_bytes = head + b"\n" + doctype.encode("utf-8") + b"\n" + xml_bytes
    else:
        xml_bytes = head + b"\n" + xml_bytes
    return xml_bytes

# ===== Event entry =====
_BUSY = False

async def _on_click(evt=None):
    global _BUSY
    if _BUSY:
        _set_ui_msg("<span style='color:#b00'>Processing in progress. Please wait.</span>")
        return

    _BUSY = True
    run_btn = document.getElementById("run-btn")
    pause_btn = document.getElementById("pause-btn")

    _set_ui_msg("")
    run_btn.disabled = True
    run_btn.textContent = "Translating..."
    pause_btn.style.display = "block"

    try:
        api = document.getElementById("apiKey").value.strip()
        base_url = document.getElementById("baseUrl").value.strip() or "https://api.openai.com/v1"

        sel1 = document.getElementById("modelSel")
        model1 = sel1.value
        if model1 == "__custom__":
            model1 = document.getElementById("modelCustom").value.strip()

        use2 = bool(document.getElementById("useModel2").checked)
        sel2 = document.getElementById("modelSel2")
        model2 = sel2.value
        if model2 == "__custom__":
            model2 = document.getElementById("modelCustom2").value.strip()

        batch = int(document.getElementById("batch").value or "32")
        limitN = int(document.getElementById("limitN").value or "0")

        if not api:
            _set_ui_msg("<span style='color:#b00'>Please enter API Key</span>")
            return
        if not model1:
            _set_ui_msg("<span style='color:#b00'>Please select or enter Model-1</span>")
            return
        if use2 and not model2:
            _set_ui_msg("<span style='color:#b00'>Please select or enter Model-2</span>")
            return

        ts_text = await _read_file_text("tsFile")
        if not ts_text:
            _set_ui_msg("<span style='color:#b00'>Please upload a .ts file</span>")
            return

        old_text = await _read_file_text("oldTsFile")

        pairs = await read_glossaries_from_file_input("glsFile")

        _set_ui_msg("Connecting...")
        sys_prompt_ui = (document.getElementById("sysPrompt").value or "").strip()

        xml_bytes = await run_translation_pipeline_async(
            api_key=api,
            base_url=base_url,
            model1=model1,
            ts_text=ts_text,
            glossary_pairs=pairs,
            batch_size=batch,
            limit_n=limitN,
            use_model2=use2,
            model2=model2,
            old_ts_text=old_text,
            sys_prompt_override=(sys_prompt_ui or None)
        )

        out_name = "qgis_zh-Hant.ts"
        b64 = base64.b64encode(xml_bytes).decode("ascii")
        link = f'<a download="{out_name}" href="data:application/octet-stream;base64,{b64}">Download {out_name}</a>'
        _set_ui_msg(link + "　<span style='color:#0a0'>Done!</span>")
        document.getElementById("pause-btn").style.display = "none"
    except Exception as e:
        _set_ui_msg(f"<span style='color:#b00'>Error: {html.escape(str(e))}</span>")
        traceback.print_exc()
        document.getElementById("pause-btn").style.display = "none"
    finally:
        pause_btn.style.display = "none"
        run_btn.disabled = False
        run_btn.textContent = "Run Translation"
        _BUSY = False

try:
    prev = getattr(window, "__TSUI_BTN_PROXY__", None)
    if prev:
        document.getElementById("run-btn").removeEventListener("click", prev)
except Exception:
    pass

_BTN_PROXY = create_proxy(lambda evt: asyncio.ensure_future(_on_click(evt)))
window.__TSUI_BTN_PROXY__ = _BTN_PROXY
document.getElementById("run-btn").addEventListener("click", _BTN_PROXY)
  `);

    runBtn.disabled = false;
    runBtn.textContent = "Run Translation";
  } catch(e){
    console.error(e);
    $msg.innerHTML = `<span style="color:#b00">Translator initialization failed: ${String(e)}</span>`;
    runBtn.disabled = true;
    runBtn.textContent = "Initialization failed";
    __root.dataset.inited = "";
    window.__TSUI_INITED__ = false;
    return;
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  await __tsui_init();
});

if (document.readyState !== "loading") {
  __tsui_init();
}

document.addEventListener("turbo:load", () => { __tsui_init(); });
document.addEventListener("pjax:complete", () => { __tsui_init(); });

</script>