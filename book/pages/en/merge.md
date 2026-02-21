---
title: merge
---

# Merge Files
Overlay translated content onto the target file.

> Feature: Upload two `.ts` files (a **Target** file and a **Source** file). Only when **`<source>` is exactly the same**, the `<translation>` from the source message will overwrite the corresponding message in the target file.

```{raw} html
<style>
  .bd-sidebar-secondary { display: none !important; }
  .bd-content,
  .bd-article-container,
  .tex2jax_ignore.mathjax_ignore {
    max-width: 100% !important;
    width: 100% !important;
  }
  /* ===== Shared ts-ui theme (same as Local / API pages) ===== */
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

  #ts-ui .ts-card{
    border:1px solid var(--ts-border);
    background:var(--ts-surface);
    border-radius:var(--ts-radius);
    padding:16px;
    box-shadow:0 1px 2px rgba(0,0,0,.04);
    color: var(--ts-text);
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

  /* Buttons: reuse shared primary style, and let ts-btn match */
  #ts-ui .ts-btn,
  #ts-ui .ts-btn-primary{
    appearance:none;
    border:1px solid var(--ts-border);
    background:var(--ts-accent);
    color:var(--ts-on-accent);
    border-radius:10px;
    padding:8px 14px;
    font-weight:700;
    cursor:pointer;
  }
  #ts-ui .ts-btn:disabled,
  #ts-ui .ts-btn-primary:disabled{
    opacity:.55;
    cursor:not-allowed;
  }
  #ts-ui .ts-btn:hover,
  #ts-ui .ts-btn-primary:hover{ filter:brightness(1.06); }
  #ts-ui .ts-btn:focus,
  #ts-ui .ts-btn-primary:focus{
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

  #ts-ui ::selection{
    background: color-mix(in oklab, var(--ts-accent) 35%, transparent);
  }

  @media (max-width:640px){
    #ts-ui .ts-grid{
      grid-template-columns:1fr;
    }
  }

  /* ===== Table settings (merge page only) ===== */
  #ts-ui .row-label {
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    word-break: break-word;
  }

  #ts-ui col:nth-child(1),
  #ts-ui col:nth-child(2),
  #ts-ui col:nth-child(3) { width: calc((100% - 150px - 240px) / 3); }
  #ts-ui col:nth-child(4) { width: 150px; }
  #ts-ui col:nth-child(5) { width: 240px; }

  /* Custom textarea */
  #ts-ui .ts-input textarea{
    width:100%;
    min-height:72px;
    padding:8px 10px;
    border:1px solid var(--ts-border);
    border-radius:10px;
    background:var(--ts-input-bg);
    color:var(--ts-text);
    resize:vertical;
  }
  #ts-ui .ts-input textarea:focus{
    outline:none;
    box-shadow:var(--ts-focus);
    border-color:color-mix(in oklab, var(--ts-accent) 60%, var(--ts-border));
  }

  #ts-ui td.will { white-space: pre-line; }

  #ts-ui #table-wrap{
    border:1px solid var(--ts-border);
    border-radius:12px;
    overflow-x:auto;
    overflow-y:auto;
    scrollbar-gutter:stable;
    max-height:70vh;
    background: var(--ts-surface);
  }

  #ts-ui table{
    width:100%;
    border-collapse:separate;
    border-spacing:0;
    table-layout: fixed;
  }

  #ts-ui table#grid{ box-sizing:border-box; }

  #ts-ui thead th{
    position:sticky;
    top:0;
    z-index:3;
    background:var(--ts-table-head-bg);
    color:var(--ts-text);
    border-bottom:1px solid var(--ts-border);
    padding:10px;
    text-align:left;
    font-weight:700;
  }

  #ts-ui tbody td,
  #ts-ui tbody th{
    border-bottom:1px solid var(--ts-border);
  }

  #ts-ui th,
  #ts-ui td{
    padding:8px 10px;
    vertical-align:top;
  }

  #ts-ui .cell-content{
    white-space:pre-wrap;
    word-break:break-word;
  }

  #ts-ui .will{ font-weight:700; }
  #ts-ui .ok { color:#059669; }
  #ts-ui .skip{ color:#ef4444; }
</style>

<div id="ts-ui">
  <div class="ts-card">
    <div class="ts-grid">
      <div class="ts-field">
        <label class="ts-label">Target file (to be overwritten)</label>
        <div class="ts-input"><input id="fileTarget" type="file" accept=".ts"></div>
      </div>
      <div class="ts-field">
        <label class="ts-label">Source file (provides translations)</label>
        <div class="ts-input"><input id="fileSource" type="file" accept=".ts"></div>
      </div>
      <div class="ts-field">
        <label class="ts-label">Actions</label>
        <div class="toolbar">
          <button class="ts-btn" id="previewBtn">Generate preview</button>
          <button class="ts-btn" id="downloadBtn" disabled>Download merged file</button>
        </div>
      </div>
    </div>

    <div class="toolbar" style="margin-top:6px; gap:16px;">
      <label><input type="checkbox" id="optNonEmptyOnly" checked> Only overwrite with non-empty source translations</label>
      <label><input type="checkbox" id="optFillEmptyOnly"> Only fill empty target translations (skip if target is non-empty)</label>
      <label><input type="checkbox" id="optShowUpdatesOnly"> Show only entries that will be overwritten</label>
      <label style="margin-left:auto;display:flex;align-items:center;gap:6px;">
        <span class="ts-label">Keyword filter</span>
        <div class="ts-input" style="min-width:220px;"><input id="searchBox" type="text" placeholder="Search source / target / source / custom"></div>
      </label>
    </div>

    <div class="toolbar"><span class="kpi" id="stat">Not loaded</span></div>
    <hr class="ts-divider"/>

    <div id="table-wrap" style="display:none;">
      <table id="grid">
        <colgroup>
          <col><col><col><col><col>
        </colgroup>
        <thead>
          <tr>
            <th>Source text</th>
            <th>Current target translation</th>
            <th>Source translation to apply</th>
            <th>Action</th>
            <th>Custom overwrite translation (optional)</th>
          </tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
  </div>

  <div id="msg" style="margin-top:8px; color:var(--ts-muted);"></div>
</div>

<script>
(function(){
  const SEP = '\u241F';

  function start(){
    const root = document.getElementById('ts-ui');
    if(!root){ console.error('ts-ui DOM not found'); return; }

    const qs = (s)=>root.querySelector(s);
    const $fileTarget = qs('#fileTarget');
    const $fileSource = qs('#fileSource');
    const $preview    = qs('#previewBtn');
    const $download   = qs('#downloadBtn');
    const $tbody      = qs('#tbody');
    const $wrap       = qs('#table-wrap');
    const $stat       = qs('#stat');
    const $msg        = qs('#msg');
    const $search     = qs('#searchBox');
    const $onlyUpd    = qs('#optShowUpdatesOnly');
    const $nonEmpty   = qs('#optNonEmptyOnly');
    const $fillEmpty  = qs('#optFillEmptyOnly');

    let target = null;      // {doc, doctype, name, messages:[{ctx,src,msgEl,key}]}
    let source = null;      // {doc, doctype, name, mapBySource:Map<string, Element[]>, dupSources:string[]}
    let previewRows = [];   // [{key, ctx, src, tgtText, srcText, customText, tgtMsgEl}]

    function readFileText(file){
      return new Promise((resolve,reject)=>{
        const fr = new FileReader();
        fr.onload=()=>resolve(String(fr.result||''));
        fr.onerror=()=>reject(fr.error);
        fr.readAsText(file,'utf-8');
      });
    }

    function readDoctype(xmlText){
      const m = xmlText.match(/<!DOCTYPE[\s\S]*?>/i);
      return m?m[0]:'';
    }

    function parseXML(text){
      const parser = new DOMParser();
      const xml = parser.parseFromString(text, 'application/xml');
      if(xml.getElementsByTagName('parsererror').length){
        throw new Error('XML parse failed. Please verify the .ts format.');
      }
      return xml;
    }

    function getTranslationPreview(messageEl){
      if(!messageEl) return '';
      const trans = messageEl.getElementsByTagName('translation')[0];
      if(!trans) return '';
      const forms = trans.getElementsByTagName('numerusform');
      if(forms && forms.length){
        const arr=[];
        for(let i=0;i<forms.length;i++) arr.push(forms[i].textContent||'');
        return arr.join(' | ');
      }
      return trans.textContent || '';
    }

    function hasNonEmptyTranslation(messageEl){
      if(!messageEl) return false;
      const t = messageEl.getElementsByTagName('translation')[0];
      if(!t) return false;
      const forms = t.getElementsByTagName('numerusform');
      if(forms && forms.length){
        for(let i=0;i<forms.length;i++){
          if((forms[i].textContent||'').trim() !== '') return true;
        }
        return false;
      }
      return (t.textContent||'').trim() !== '';
    }

    function parseTarget(text, name){
      const doctype = readDoctype(text);
      const doc = parseXML(text);
      const messages=[];
      const contexts = doc.getElementsByTagName('context');
      for(let i=0;i<contexts.length;i++){
        const ctx = contexts[i];
        const nameEl = ctx.getElementsByTagName('name')[0];
        const ctxName = nameEl ? (nameEl.textContent||'') : '';
        const ms = ctx.getElementsByTagName('message');
        for(let j=0;j<ms.length;j++){
          const m = ms[j];
          const srcEl = m.getElementsByTagName('source')[0];
          const src = srcEl ? (srcEl.textContent||'') : '';
          const key = ctxName + SEP + src;
          messages.push({ctx: ctxName, src, msgEl: m, key});
        }
      }
      return {doc, doctype, name, messages};
    }

    function parseSource(text, name){
      const doctype = readDoctype(text);
      const doc = parseXML(text);
      const map = new Map(); // source -> [messageEl,...]
      const dups = [];
      const contexts = doc.getElementsByTagName('context');
      for(let i=0;i<contexts.length;i++){
        const ctx = contexts[i];
        const ms = ctx.getElementsByTagName('message');
        for(let j=0;j<ms.length;j++){
          const m = ms[j];
          const srcEl = m.getElementsByTagName('source')[0];
          const src = srcEl ? (srcEl.textContent||'') : '';
          if(!map.has(src)) map.set(src, [m]);
          else {
            map.get(src).push(m);
            if(map.get(src).length===2) dups.push(src);
          }
        }
      }
      return {doc, doctype, name, mapBySource: map, dupSources: dups};
    }

    function escapeHtml(s){
      return String(s||'').replace(/[&<>\"']/g, c=>({
        '&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;','\'':'&#39;'
      }[c]));
    }

    function decideRow(r){
      const nonEmptyOnly = $nonEmpty.checked;
      const fillEmptyOnly = $fillEmpty.checked;

      // ✅ Custom has priority (allowed even if source is missing/empty, or target is non-empty)
      if((r.customText||'').trim() !== ''){
        return {will:true, reason:'Custom overwrite'};
      }

      const srcList = source?.mapBySource?.get(r.src);
      const srcMsg = (srcList && srcList.length) ? srcList[0] : null;

      if(!srcMsg) return {will:false, reason:'Source missing this <source>'};
      if(fillEmptyOnly && hasNonEmptyTranslation(r.tgtMsgEl)) return {will:false, reason:'Target already has a non-empty translation'};
      if(nonEmptyOnly && !hasNonEmptyTranslation(srcMsg)) return {will:false, reason:'Source translation is empty'};
      return {will:true, reason:'Overwrite'};
    }

    function buildPreview(){
      previewRows = [];
      for(const rec of target.messages){
        const srcList = source.mapBySource.get(rec.src);
        const srcMsg = (srcList && srcList.length) ? srcList[0] : null;
        previewRows.push({
          key: rec.key,
          ctx: rec.ctx,
          src: rec.src,
          tgtText: getTranslationPreview(rec.msgEl),
          srcText: getTranslationPreview(srcMsg),
          customText: '',
          tgtMsgEl: rec.msgEl
        });
      }
    }

    function calcWillCount(){
      let will = 0;
      for(const r of previewRows){
        if(decideRow(r).will) will++;
      }
      return will;
    }

    function updateKpi(shownCount){
      const total = previewRows.length;
      const willAll = calcWillCount();
      const dupN = source ? source.dupSources.length : 0;
      const shown = (typeof shownCount === 'number') ? shownCount : total;
      $stat.textContent = `Matched source texts: ${total}; Will overwrite: ${willAll}; Showing: ${shown}; Duplicate <source> in source file: ${dupN}${dupN? ' (using the first one)':''}`;
      $download.disabled = !(previewRows.length && willAll>0);
      if(dupN){ $msg.textContent = 'Note: The source file contains '+dupN+' duplicate <source> entries (only the first is used).'; }
      else { $msg.textContent = ''; }
    }

    function renderPreview(){
      const q = ($search.value||'').trim().toLowerCase();
      const showUpdOnly = $onlyUpd.checked;

      $tbody.innerHTML = '';
      let shown = 0;

      const frag = document.createDocumentFragment();

      for(const r of previewRows){
        const d = decideRow(r);

        if(showUpdOnly && !d.will) continue;

        const hay = (r.src + ' ' + (r.tgtText||'') + ' ' + (r.srcText||'') + ' ' + (r.customText||'')).toLowerCase();
        if(q && !hay.includes(q)) continue;

        const tr = document.createElement('tr');

        const td0 = document.createElement('th'); td0.className='row-label';
        td0.innerHTML =
          '<div style="font-weight:700;">'+escapeHtml(r.src)+'</div>' +
          '<div class="ts-label">'+escapeHtml(r.ctx)+'</div>';

        const td1 = document.createElement('td');
        td1.innerHTML = '<div class="cell-content">'+escapeHtml(r.tgtText||'')+'</div>';

        const td2 = document.createElement('td');
        td2.innerHTML = '<div class="cell-content">'+escapeHtml(r.srcText||'')+'</div>';

        const td3 = document.createElement('td');
        td3.className = 'will ' + (d.will ? 'ok':'skip');
        td3.textContent = d.will ? (d.reason==='Custom overwrite' ? 'Overwrite (custom)' : 'Overwrite') : ('Skip:\n'+d.reason);

        const td4 = document.createElement('td');
        const box = document.createElement('div');
        box.className = 'ts-input';

        const ta = document.createElement('textarea');
        ta.placeholder = '(Optional) Type here to overwrite with this text';
        ta.value = r.customText || '';

        ta.addEventListener('input', ()=>{
          r.customText = ta.value || '';

          const d2 = decideRow(r);
          td3.className = 'will ' + (d2.will ? 'ok':'skip');
          td3.textContent = d2.will ? (d2.reason==='Custom overwrite' ? 'Overwrite (custom)' : 'Overwrite') : ('Skip:\n'+d2.reason);

          // Custom changes total counts; update KPI without full rerender
          updateKpi(shown);
        });

        box.appendChild(ta);
        td4.appendChild(box);

        tr.appendChild(td0);
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);

        frag.appendChild(tr);
        shown++;
      }

      $tbody.appendChild(frag);
      $wrap.style.display = shown ? '' : 'none';

      updateKpi(shown);
    }

    function setTranslationFromCustomText(outDoc, targetMsg, customText){
      const text = String(customText||'');
      let t = targetMsg.getElementsByTagName('translation')[0];
      if(!t){
        t = outDoc.createElement('translation');
        targetMsg.appendChild(t);
      }

      const forms = t.getElementsByTagName('numerusform');
      if(forms && forms.length){
        const parts = text.split('|').map(s=>s.trim()).filter(s=>s.length>0);
        const arr = parts.length ? parts : [text];
        for(let i=0;i<forms.length;i++){
          const v = arr[Math.min(i, arr.length-1)] ?? '';
          forms[i].textContent = v;
        }
      }else{
        // Remove children then set text (avoid leftovers)
        while(t.firstChild) t.removeChild(t.firstChild);
        t.appendChild(outDoc.createTextNode(text));
      }
    }

    function applyAndDownload(){
      if(!target || !source || !previewRows.length) return;

      const outDoc = target.doc.cloneNode(true);

      // Build key => message index (ctx + SEP + source)
      const keyMap = new Map();
      const ctxNodes = outDoc.getElementsByTagName('context');
      for(let i=0;i<ctxNodes.length;i++){
        const n = ctxNodes[i];
        const nameEl = n.getElementsByTagName('name')[0];
        const ctxName = nameEl ? (nameEl.textContent||'') : '';
        const ms = n.getElementsByTagName('message');
        for(let j=0;j<ms.length;j++){
          const m = ms[j];
          const sEl = m.getElementsByTagName('source')[0];
          const s = sEl ? (sEl.textContent||'') : '';
          keyMap.set(ctxName + SEP + s, m);
        }
      }

      let applied = 0;

      for(const r of previewRows){
        const d = decideRow(r);
        if(!d.will) continue;

        const targetMsg = keyMap.get(r.key);
        if(!targetMsg) continue;

        // ✅ Custom overwrite
        if((r.customText||'').trim() !== ''){
          setTranslationFromCustomText(outDoc, targetMsg, r.customText);
          applied++;
          continue;
        }

        // ✅ Source overwrite (respect checkbox options)
        const nonEmptyOnly = $nonEmpty.checked;
        const fillEmptyOnly = $fillEmpty.checked;

        const srcList = source.mapBySource.get(r.src);
        const srcMsg = srcList && srcList.length ? srcList[0] : null;
        if(!srcMsg) continue;

        if(nonEmptyOnly && !hasNonEmptyTranslation(srcMsg)) continue;
        if(fillEmptyOnly && hasNonEmptyTranslation(targetMsg)) continue;

        const tTarget = targetMsg.getElementsByTagName('translation')[0];
        const tSrc    = srcMsg.getElementsByTagName('translation')[0];
        if(!tSrc) continue;

        const imported = outDoc.importNode(tSrc, true);
        if(tTarget) targetMsg.replaceChild(imported, tTarget);
        else targetMsg.appendChild(imported);

        applied++;
      }

      const xmlDecl = '<?xml version="1.0" encoding="utf-8"?>\n';
      const ser = new XMLSerializer();
      let xmlOut = ser.serializeToString(outDoc);

      const doctype = target.doctype;
      if(doctype){
        xmlOut = xmlDecl + doctype + '\n' + xmlOut;
      }else{
        xmlOut = xmlDecl + xmlOut;
      }

      const blob = new Blob([xmlOut], {type:'application/xml'});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      const baseName = (target.name||'target').replace(/\.ts$/i,'');
      a.download = baseName + '.overlay.ts';
      document.body.appendChild(a);
      a.click();
      setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); }, 0);

      $msg.textContent = 'Overlay applied and exported (actually updated '+applied+' entries).';
    }

    async function doPreview(){
      try{
        $tbody.innerHTML='';
        $wrap.style.display='none';
        $download.disabled = true;
        $stat.textContent='Loading…';
        $msg.textContent='';

        const fT = $fileTarget.files && $fileTarget.files[0];
        const fS = $fileSource.files && $fileSource.files[0];
        if(!fT || !fS){
          $stat.textContent='Please select two .ts files (target and source).';
          return;
        }

        $preview.disabled = true;

        const [tText, sText] = await Promise.all([readFileText(fT), readFileText(fS)]);
        target = parseTarget(tText, fT.name);
        source = parseSource(sText, fS.name);

        buildPreview();
        renderPreview();
      }catch(e){
        console.error(e);
        $stat.textContent='Load failed';
        $msg.textContent='Error: '+(e?.message||e);
      }finally{
        $preview.disabled = false;
      }
    }

    $preview?.addEventListener('click', doPreview);
    $download?.addEventListener('click', applyAndDownload);

    $search?.addEventListener('input', renderPreview);
    $onlyUpd?.addEventListener('change', renderPreview);

    // ✅ Do not rebuild preview (avoid clearing custom edits)
    $nonEmpty?.addEventListener('change', renderPreview);
    $fillEmpty?.addEventListener('change', renderPreview);

    updateKpi(0);
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
</script>