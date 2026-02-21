---
title: Edit
---

# TS Translation File Editor

```{raw} html
<style>
  .bd-sidebar-secondary { display: none !important; }
  .bd-content,
  .bd-article-container,
  .tex2jax_ignore.mathjax_ignore {
    max-width: 100% !important;
    width: 100% !important;
  }
  /* ===== Shared ts-ui theme (consistent with other pages) ===== */
  #ts-ui{
    --ts-gap: 12px;
    --ts-pad: 14px;
    --ts-radius: 12px;
    --ts-border: #e5e7eb;
    --ts-bg: #fff;
    --ts-surface: #fff;
    --ts-surface-2: #f9fafb;
    --ts-input-bg: #fff;
    --ts-text: #111827;
    --ts-muted: #6b7280;
    --ts-link: #2563eb;
    --ts-code-bg: #f9fafb;
    --ts-code-fg: #111827;
    --ts-accent: #2563eb;
    --ts-on-accent: #ffffff;
    --ts-focus: 0 0 0 2px rgba(37,99,235,.25);
    --ts-progress-bg: #e5e7eb;
    --ts-table-head-bg: #f3f4f6;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans", "PingFang TC", "Microsoft JhengHei", sans-serif;
    line-height: 1.35;
    margin: 8px 0 16px;
    color: var(--ts-text);
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

  #ts-ui *, #ts-ui *::before, #ts-ui *::after{ box-sizing:border-box; }

  /* Text selection color */
  #ts-ui ::selection{
    background: color-mix(in oklab, var(--ts-accent, #2563eb) 35%, transparent);
  }

  /* Card and basic layout */
  #ts-ui .ts-card{
    border:1px solid var(--ts-border);
    background:var(--ts-surface);
    border-radius:var(--ts-radius);
    padding:16px;
    box-shadow:0 1px 2px rgba(0,0,0,.04);
    color: var(--ts-text);
  }
  #ts-ui .ts-title{
    font-weight:800;
    font-size:1.1rem;
    margin:2px 0 10px;
  }
  #ts-ui .ts-grid{
    display:grid;
    grid-template-columns:1fr 1fr 1fr;
    gap:12px;
  }
  #ts-ui .ts-field{
    display:flex;
    flex-direction:column;
    gap:6px;
  }
  #ts-ui .ts-label{
    color:var(--ts-muted);
    font-size:.95rem;
  }

  #ts-ui .ts-input input{
    width:100%;
    padding:8px 10px;
    border:1px solid var(--ts-border);
    border-radius:10px;
    background:var(--ts-input-bg);
    color:var(--ts-text);
  }
  #ts-ui .ts-input input:focus{
    outline:none;
    box-shadow:var(--ts-focus);
    border-color:color-mix(in oklab, var(--ts-accent) 60%, var(--ts-border));
  }

  /* Buttons */
  #ts-ui .ts-btn{
    appearance:none;
    border:1px solid var(--ts-border);
    background:var(--ts-accent);
    color:var(--ts-on-accent);
    border-radius:10px;
    padding:8px 14px;
    font-weight:700;
    cursor:pointer;
  }
  #ts-ui .ts-btn:disabled{
    opacity:.55;
    cursor:not-allowed;
  }
  #ts-ui .ts-btn:hover{ filter:brightness(1.06); }
  #ts-ui .ts-btn:focus{
    outline:none;
    box-shadow:var(--ts-focus);
  }

  #ts-ui .toolbar{
    display:flex;
    gap:10px;
    align-items:center;
    flex-wrap:wrap;
    margin-top:8px;
  }
  #ts-ui .kpi{
    color:var(--ts-muted);
    font-variant-numeric:tabular-nums;
  }
  #ts-ui .ts-divider{
    height:1px;
    background:var(--ts-border);
    border:0;
    margin:12px 0;
  }

  /* Small toolbar */
  #ts-ui .tools{
    display:flex;
    gap:10px;
    align-items:center;
    flex-wrap:wrap;
  }
  #ts-ui .tools label{
    display:flex;
    gap:6px;
    align-items:center;
    color:var(--ts-muted);
  }

  /* Table (grid) */
  #ts-ui #table-wrap{
    border:1px solid var(--ts-border);
    border-radius:12px;
    overflow:auto;
    max-height:70vh;
    background: var(--ts-surface); /* use card bg in dark mode too */
  }

  #ts-ui table{
    width:100%;
    border-collapse:separate;
    border-spacing:0;
    table-layout: fixed;
  }

  #ts-ui thead th{
    position:sticky;
    top:0;
    z-index:3;
    background:var(--ts-table-head-bg);
    border-bottom:1px solid var(--ts-border);
    padding:10px;
    text-align:left;
    font-weight:700;
    color: var(--ts-text);
  }
  #ts-ui tbody td,
  #ts-ui tbody th{
    border-bottom:1px solid var(--ts-border);
  }
  #ts-ui th,
  #ts-ui td{
    padding:8px 10px;
    vertical-align:top;
    color: var(--ts-text);
  }

  #ts-ui .sticky-left{
    position:sticky;
    left:0;
    z-index:2;
    background:var(--ts-surface);
  }

  /* Source column */
  #ts-ui .row-label{
    width:auto;
    max-width:none;
  }
  #ts-ui .row-label .ctx{
    color:var(--ts-muted);
    font-size:.85rem;
    margin-top:2px;
  }

  /* Each translation-version cell */
  #ts-ui .pick-cell{
    min-width:0;
    max-width:none;
    border-left:1px solid var(--ts-border);
    cursor:pointer;
  }
  #ts-ui .pick-cell.missing{
    color:var(--ts-muted);
    font-style:italic;
    cursor:not-allowed;
  }
  #ts-ui .cell-box{
    display:flex;
    gap:8px;
  }
  #ts-ui .cell-index{
    color:var(--ts-muted);
    font-size:.85rem;
    min-width:1.5rem;
    text-align:right;
  }
  #ts-ui .cell-content{
    white-space:pre-wrap;
    word-break:break-word;
  }

  /* Selected cell */
  #ts-ui .pick-cell.selected{
    outline:2px solid color-mix(in oklab, var(--ts-accent) 70%, #0000);
    outline-offset:-2px;
    background:color-mix(in oklab, var(--ts-accent) 14%, var(--ts-surface));
  }

  /* Header first column (source) */
  #ts-ui .head-left{
    position:sticky;
    left:0;
    z-index:4;
    background:var(--ts-table-head-bg);
  }
  #ts-ui .head-col{
    white-space:nowrap;
  }

  @media (max-width: 860px){
    #ts-ui .cell-index{ display:none; }
  }
</style>

<div id="ts-ui">
  <div class="ts-card">
    <div class="ts-title">TS Multi-Version Merge Selection (Click to Choose)</div>
    <div class="ts-grid">
      <div class="ts-field">
        <label for="tsFiles" class="ts-label">.ts files (multiple allowed; 1st file is default)</label>
        <div class="ts-input"><input id="tsFiles" type="file" accept=".ts" multiple></div>
      </div>
      <div class="ts-field">
        <label for="searchBox" class="ts-label">Keyword Filter (source / translation)</label>
        <div class="ts-input"><input id="searchBox" type="text" placeholder="Enter keywords"></div>
      </div>
      <div class="ts-field">
        <label class="ts-label">Output</label>
        <div class="tools">
          <button class="ts-btn" id="buildBtn">Build Table</button>
          <button class="ts-btn" id="downloadBtn" disabled>Download Merged File</button>
          <label><input type="checkbox" id="onlyDiff"> Show only entries different from column 1</label>
        </div>
      </div>
    </div>

    <div class="toolbar"><span class="kpi" id="stat">Not loaded yet</span></div>

    <hr class="ts-divider"/>

    <div id="table-wrap" style="display:none;">
      <table id="grid">
        <!-- Use colgroup to control width of each column (including source column) -->
        <colgroup id="colgroup"></colgroup>
        <thead id="thead"></thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>

    <div class="ts-label" style="margin-top:10px;">
      Usage: Upload n `.ts` files → Build table. Rows (y-axis) are messages; columns (x-axis) are translations from each file.
      Click any cell to choose that file’s translation for the message; the default is column 1 for all rows.
      Click “Download Merged File” to export `merged.ts`.
    </div>
  </div>
  <div id="msg" style="margin-top:8px; color:var(--ts-muted);"></div>
</div>

<script>
(function(){
  // In Jupyter-Book, make sure the script runs after DOM is ready
  function start(){
    const root = document.getElementById('ts-ui');
    if(!root){ console.error('ts-ui DOM not found'); return; }

    const qs = (s)=>root.querySelector(s);
    const $files   = qs('#tsFiles');
    const $build   = qs('#buildBtn');
    const $dl      = qs('#downloadBtn');
    const $stat    = qs('#stat');
    const $msg     = qs('#msg');
    const $thead   = qs('#thead');
    const $tbody   = qs('#tbody');
    const $wrap    = qs('#table-wrap');
    const $search  = qs('#searchBox');
    const $onlyDiff= qs('#onlyDiff');
    const $grid    = qs('#grid');
    const $colgroup= qs('#colgroup');

    if(!$thead || !$tbody || !$wrap || !$grid || !$colgroup){
      console.error('Grid nodes not found');
      return;
    }

    // State
    let versions = [];    // [{name, doc, doctype, map, meta}]
    let base = null;      // versions[0]
    let baseKeys = [];    // key list using the first file as the base
    let picked = new Map(); // key -> vi (selected version index), default 0

    // Utility functions
    function readFileText(file){
      return new Promise((resolve,reject)=>{
        const fr = new FileReader();
        fr.onload=()=>resolve(String(fr.result||''));
        fr.onerror=()=>reject(fr.error);
        fr.readAsText(file,'utf-8');
      });
    }
    function readDoctype(xmlText){
      const m = xmlText.match(/<!DOCTYPE[^>]+>/);
      return m?m[0]:'';
    }
    function escapeHtml(s){
      return String(s||'').replace(/[&<>"']/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;' }[c]));
    }

    function parseTS(xmlText){
      const doctype = readDoctype(xmlText);
      const parser = new DOMParser();
      const xml = parser.parseFromString(xmlText, 'application/xml');
      if(xml.getElementsByTagName('parsererror').length){
        throw new Error('XML parse failed. Please check the .ts format.');
      }
      const map = new Map();
      const meta = new Map();
      const contexts = xml.getElementsByTagName('context');
      for(let i=0;i<contexts.length;i++){
        const ctx = contexts[i];
        const nameEl = ctx.getElementsByTagName('name')[0];
        const ctxName = nameEl ? (nameEl.textContent||'') : '';
        const messages = ctx.getElementsByTagName('message');
        for(let j=0;j<messages.length;j++){
          const m = messages[j];
          const srcEl = m.getElementsByTagName('source')[0];
          const src = srcEl ? (srcEl.textContent||'') : '';
          const key = ctxName + '\u241F' + src;
          map.set(key, m);
          meta.set(key, {context: ctxName, source: src});
        }
      }
      return { doc: xml, doctype, map, meta };
    }

    function getTransPreview(messageEl){
      if(!messageEl) return '';
      const trans = messageEl.getElementsByTagName('translation')[0];
      if(!trans) return '';
      const forms = trans.getElementsByTagName('numerusform');
      if(forms && forms.length){
        const parts=[]; for(let i=0;i<forms.length;i++){ parts.push(forms[i].textContent||''); }
        return parts.join(' | ');
      }
      return trans.textContent || '';
    }

    function replaceTranslation(baseDoc, baseMsg, srcMsg){
      if(!baseMsg || !srcMsg) return;
      const baseTrans = baseMsg.getElementsByTagName('translation')[0];
      const srcTrans  = srcMsg.getElementsByTagName('translation')[0];
      if(!srcTrans) return;
      const imported = baseDoc.importNode(srcTrans, true);
      if(baseTrans){ baseMsg.replaceChild(imported, baseTrans); } else { baseMsg.appendChild(imported); }
    }

    function buildHeader(files){
      $thead.innerHTML = '';
      const tr = document.createElement('tr');
      const th0 = document.createElement('th');
      th0.className = 'head-left';
      th0.textContent = 'Source (context / source)';
      tr.appendChild(th0);
      files.forEach((f, i)=>{
        const th = document.createElement('th');
        th.className = 'head-col';
        th.textContent = `${i+1}. ${f.name || `v${i+1}`}`;
        tr.appendChild(th);
      });
      $thead.appendChild(tr);
    }

    function buildRow(rowIdx, key){
      const tr = document.createElement('tr');
      tr.dataset.key = key;

      // Left row label: source + context
      const tdLabel = document.createElement('th');
      tdLabel.className = 'row-label sticky-left';
      const metaBase = base.meta.get(key) || {context:'', source:''};
      tdLabel.innerHTML = `<div style="font-weight:700;">${escapeHtml(metaBase.source)}</div><div class="ctx">${escapeHtml(metaBase.context)}</div>`;
      tr.appendChild(tdLabel);

      // Translation cell for each version
      versions.forEach((v, vi)=>{
        const td = document.createElement('td');
        td.className = 'pick-cell';
        td.tabIndex = 0; // keyboard focusable
        td.setAttribute('role','button');
        td.dataset.vi = String(vi);
        const msg = v.map.get(key);
        if(!msg){
          td.classList.add('missing');
          td.innerHTML = '<div class="cell-content">(message not found in this file)</div>';
        } else {
          const preview = escapeHtml(getTransPreview(msg)) || '<i>(empty)</i>';
          td.innerHTML = `<div class="cell-box"><div class="cell-index">${vi+1}</div><div class="cell-content">${preview}</div></div>`;
        }
        td.addEventListener('click', ()=> selectCell(tr, td));
        td.addEventListener('keydown', (e)=>{ if(e.key==='Enter' || e.key===' '){ e.preventDefault(); selectCell(tr, td);} });
        tr.appendChild(td);
      });

      // Default to column 1
      setRowPick(tr, 0);
      return tr;
    }

    function setRowPick(tr, vi){
      const key = tr.dataset.key;
      picked.set(key, vi);
      const cells = Array.from(tr.querySelectorAll('.pick-cell'));
      cells.forEach(td=> td.classList.remove('selected'));
      const target = cells[vi];
      if(target && !target.classList.contains('missing')) target.classList.add('selected');
    }

    function selectCell(tr, td){
      if(td.classList.contains('missing')) return;
      const vi = Number(td.dataset.vi||'0');
      setRowPick(tr, vi);
    }

    // Column width rules: <=4 columns share width equally; >4 columns use 25% each and scroll horizontally
    function adjustColumnWidths(){
      const totalCols = 1 + versions.length; // source + versions
      $colgroup.innerHTML = '';

      if (totalCols <= 4){
        // Evenly fill 100%
        const w = (100 / totalCols).toFixed(6) + '%';
        for(let i=0;i<totalCols;i++){
          const col = document.createElement('col');
          col.style.width = w;
          $colgroup.appendChild(col);
        }
        $grid.style.width = '100%';
      }else{
        // Each column fixed at 25%, total width exceeds container (horizontal scroll)
        for(let i=0;i<totalCols;i++){
          const col = document.createElement('col');
          col.style.width = '25%';
          $colgroup.appendChild(col);
        }
        $grid.style.width = (25 * totalCols) + '%';
      }
    }

    async function buildGrid(){
      $thead.innerHTML = ''; $tbody.innerHTML = ''; $wrap.style.display='none';
      $dl.disabled = true; $stat.textContent = 'Loading...'; $msg.textContent=''; picked = new Map();

      const files = Array.from($files.files || []);
      if(files.length < 1){ $stat.textContent = 'Please select at least 1 .ts file'; return; }

      // Read files
      const texts = await Promise.all(files.map(readFileText));
      versions = texts.map((txt, i)=>({ ...parseTS(txt), name: files[i].name || `v${i+1}` }));
      base = versions[0];
      baseKeys = Array.from(base.map.keys());

      buildHeader(files);

      const frag = document.createDocumentFragment();
      baseKeys.forEach((key, idx)=>{ frag.appendChild(buildRow(idx, key)); });
      $tbody.appendChild(frag);

      adjustColumnWidths();     // ★ adjust widths by column count
      $wrap.style.display = '';
      $dl.disabled = false;
      $stat.textContent = `Loaded ${files.length} file(s); messages: ${baseKeys.length} (file 1 is the default base)`;
      applyFilter();
    }

    function applyFilter(){
      const q = ($search.value||'').trim().toLowerCase();
      const terms = q ? q.split(/\s+/).filter(Boolean) : [];
      const onlyDiff = $onlyDiff.checked;

      Array.from($tbody.children).forEach(tr=>{
        const key = tr.dataset.key;
        let text = '';
        const metaBase = base.meta.get(key) || {context:'', source:''};
        text += (metaBase.source||'') + ' ' + (metaBase.context||'');
        versions.forEach(v=>{
          const m=v.map.get(key);
          text += ' ' + (m? getTransPreview(m):'');
        });

        const match = !terms.length || terms.every(t => text.toLowerCase().includes(t));

        let diff = true;
        if(onlyDiff){
          // Show only rows different from column 1
          const baseText = getTransPreview(versions[0].map.get(key));
          diff = versions.slice(1).some(v=> getTransPreview(v.map.get(key)) !== baseText);
        }

        tr.style.display = (match && (!onlyDiff || diff)) ? '' : 'none';
      });
    }

    function downloadMerged(){
      if(!base) return;
      const baseDoc = base.doc.cloneNode(true);

      // For each base key, replace translation using selected version
      baseKeys.forEach(key=>{
        const vi = picked.get(key) ?? 0;
        const srcMsg = (versions[vi] && versions[vi].map.get(key)) ? versions[vi].map.get(key) : base.map.get(key);

        // Locate matching message inside baseDoc
        const ctxName = base.meta.get(key)?.context || '';
        const srcText = base.meta.get(key)?.source || '';
        const ctxNodes = baseDoc.getElementsByTagName('context');
        let targetMsg = null;
        for(let i=0;i<ctxNodes.length && !targetMsg;i++){
          const n = ctxNodes[i];
          const nameEl = n.getElementsByTagName('name')[0];
          const name = nameEl ? (nameEl.textContent||'') : '';
          if(name !== ctxName) continue;
          const ms = n.getElementsByTagName('message');
          for(let j=0;j<ms.length;j++){
            const s = ms[j].getElementsByTagName('source')[0];
            const st = s ? (s.textContent||'') : '';
            if(st === srcText){ targetMsg = ms[j]; break; }
          }
        }
        if(targetMsg){ replaceTranslation(baseDoc, targetMsg, srcMsg); }
      });

      // Export XML
      const xmlDecl = '<?xml version="1.0" encoding="utf-8"?>\n';
      const ser = new XMLSerializer();
      let xmlOut = ser.serializeToString(baseDoc);
      const doctype = base.doctype;
      if(doctype){ xmlOut = xmlDecl + doctype + xmlOut; } else { xmlOut = xmlDecl + xmlOut; }

      const blob = new Blob([xmlOut], {type:'application/xml'});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'merged.ts';
      document.body.appendChild(a);
      a.click();
      setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); }, 0);
    }

    // Bind events
    $build?.addEventListener('click', async ()=>{
      try{ await buildGrid(); }
      catch(e){ $msg.textContent='Load failed: '+(e?.message||e); console.error(e); }
    });
    $dl?.addEventListener('click', downloadMerged);
    $search?.addEventListener('input', applyFilter);
    $onlyDiff?.addEventListener('change', applyFilter);
  }

  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
</script>