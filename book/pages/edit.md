---
title: Edit
---

# ts 翻譯檔編輯

```{raw} html
<style>
  .bd-sidebar-secondary { display: none !important; }
  .bd-content,
  .bd-article-container,
  .tex2jax_ignore.mathjax_ignore {
    max-width: 100% !important;
    width: 100% !important;
  }
</style>

<style>
  /* —— 全部樣式限制在 #ts-ui —— */
  #ts-ui{
    --ts-gap: 12px; --ts-pad: 14px; --ts-radius: 12px;
    --ts-border:#e5e7eb; --ts-bg:#fff; --ts-surface:#fff; --ts-surface-2:#f9fafb;
    --ts-text:#111827; --ts-muted:#6b7280; --ts-accent:#3b82f6; --ts-on-accent:#fff;
    --ts-head-bg:#f8fafc; --ts-focus:0 0 0 2px rgba(59,130,246,.35);
    font-family: system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans", "PingFang TC", "Microsoft JhengHei", sans-serif;
    line-height:1.35; color:var(--ts-text);
    margin:18px auto; max-width:100%; width:100%; padding:0 10px;
  }
  @media (prefers-color-scheme: dark){
    #ts-ui{ --ts-border:#2b2f36; --ts-bg:#0f1115; --ts-surface:#111418; --ts-surface-2:#0b0f14; --ts-text:#e7eaf0; --ts-muted:#a6afbd; --ts-accent:#8ab4ff; --ts-on-accent:#0b0f14; --ts-head-bg:#121621; }
  }
  #ts-ui *, #ts-ui *::before, #ts-ui *::after{ box-sizing:border-box; }
  .ts-card{ border:1px solid var(--ts-border); background:var(--ts-surface); border-radius:var(--ts-radius); padding:16px; box-shadow:0 1px 2px rgba(0,0,0,.04); }
  .ts-title{ font-weight:800; font-size:1.1rem; margin:2px 0 10px; }
  .ts-grid{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; }
  .ts-field{ display:flex; flex-direction:column; gap:6px; }
  .ts-label{ color:var(--ts-muted); font-size:.95rem; }
  .ts-input input{ width:100%; padding:8px 10px; border:1px solid var(--ts-border); border-radius:10px; background:transparent; color:var(--ts-text); }
  .ts-input input:focus{ outline:none; box-shadow:var(--ts-focus); border-color:color-mix(in oklab, var(--ts-accent) 60%, var(--ts-border)); }
  .ts-btn{ appearance:none; border:1px solid var(--ts-border); background:var(--ts-accent); color:var(--ts-on-accent); border-radius:10px; padding:8px 14px; font-weight:700; cursor:pointer; }
  .ts-btn:disabled{ opacity:.55; cursor:not-allowed; }
  .toolbar{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin-top:8px; }
  .kpi{ color:var(--ts-muted); font-variant-numeric:tabular-nums; }
  .ts-divider{ height:1px; background:var(--ts-border); border:0; margin:12px 0; }

  /* 表格（網格）*/
  #table-wrap{ border:1px solid var(--ts-border); border-radius:12px; overflow:auto; max-height:70vh; }
  #ts-ui table{
    width:100%;                     /* JS 會在 >4 欄時改為 25%×欄數 */
    border-collapse:separate; border-spacing:0;
    table-layout: fixed;            /* 讓 colgroup 寬度生效、平均分配 */
  }
  thead th{ position:sticky; top:0; z-index:3; background:var(--ts-head-bg); border-bottom:1px solid var(--ts-border); padding:10px; text-align:left; font-weight:700; }
  tbody td, tbody th{ border-bottom:1px solid var(--ts-border); }
  th, td{ padding:8px 10px; vertical-align:top; }
  .sticky-left{ position:sticky; left:0; z-index:2; background:var(--ts-surface); }

  /* 取消固定寬，交給 colgroup 控制；讓「原文」也能等比參與 */
  .row-label{ width:auto; max-width:none; }
  .row-label .ctx{ color:var(--ts-muted); font-size:.85rem; margin-top:2px; }

  /* 取消欄寬上限，否則等比不會生效 */
  .pick-cell{ min-width:0; max-width:none; border-left:1px solid var(--ts-border); cursor:pointer; }
  .pick-cell.missing{ color:var(--ts-muted); font-style:italic; cursor:not-allowed; }
  .cell-box{ display:flex; gap:8px; }
  .cell-index{ color:var(--ts-muted); font-size:.85rem; min-width:1.5rem; text-align:right; }
  .cell-content{ white-space:pre-wrap; word-break:break-word; }

  /* 被選取的格子 */
  .pick-cell.selected{ outline:2px solid color-mix(in oklab, var(--ts-accent) 70%, #0000); outline-offset:-2px; background:color-mix(in oklab, var(--ts-accent) 14%, var(--ts-surface)); }

  /* 表頭第一欄（原文）*/
  .head-left{ position:sticky; left:0; z-index:4; background:var(--ts-head-bg); }
  .head-col{ white-space:nowrap; }

  /* 小工具列 */
  .tools{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
  .tools label{ display:flex; gap:6px; align-items:center; color:var(--ts-muted); }

  @media (max-width: 860px){
    .cell-index{ display:none; }
  }
</style>

<div id="ts-ui">
  <div class="ts-card">
    <div class="ts-title">TS 多版本合併選擇（點格選取）</div>
    <div class="ts-grid">
      <div class="ts-field">
        <label for="tsFiles" class="ts-label">.ts 檔（可多選；第 1 檔為預設）</label>
        <div class="ts-input"><input id="tsFiles" type="file" accept=".ts" multiple></div>
      </div>
      <div class="ts-field">
        <label for="searchBox" class="ts-label">關鍵字過濾（原文/譯文）</label>
        <div class="ts-input"><input id="searchBox" type="text" placeholder="輸入關鍵字"></div>
      </div>
      <div class="ts-field">
        <label class="ts-label">輸出</label>
        <div class="tools">
          <button class="ts-btn" id="buildBtn">生成表格</button>
          <button class="ts-btn" id="downloadBtn" disabled>下載合併檔</button>
          <label><input type="checkbox" id="onlyDiff"> 只顯示與第 1 欄不同</label>
        </div>
      </div>
    </div>

    <div class="toolbar"><span class="kpi" id="stat">尚未載入</span></div>

    <hr class="ts-divider"/>

    <div id="table-wrap" style="display:none;">
      <table id="grid">
        <!-- 用 colgroup 控制每一欄的寬度（包含原文欄） -->
        <colgroup id="colgroup"></colgroup>
        <thead id="thead"></thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>

    <div class="ts-label" style="margin-top:10px;">
      使用說明：上傳 n 個 .ts → 生成表格。行（y 軸）是一個訊息；列（x 軸）是各檔的譯文。點選任一「格」即表示此訊息採用該檔的翻譯；預設全為第 1 欄。按「下載合併檔」輸出 merged.ts。
    </div>
  </div>
  <div id="msg" style="margin-top:8px; color:var(--ts-muted);"></div>
</div>

<script>
(function(){
  // 在 Jupyter-Book 中，確保 DOM ready 後再執行
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

    // 狀態
    let versions = [];    // [{name, doc, doctype, map, meta}]
    let base = null;      // versions[0]
    let baseKeys = [];    // 以第一檔為底稿的 key 列表
    let picked = new Map(); // key -> vi（選中的版本 index），預設 0

    // 工具函數
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
        throw new Error('XML 解析失敗，請確認 .ts 格式');
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
      th0.textContent = '原文（context / source）';
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

      // 左側 row label：原文 + context
      const tdLabel = document.createElement('th');
      tdLabel.className = 'row-label sticky-left';
      const metaBase = base.meta.get(key) || {context:'', source:''};
      tdLabel.innerHTML = `<div style="font-weight:700;">${escapeHtml(metaBase.source)}</div><div class="ctx">${escapeHtml(metaBase.context)}</div>`;
      tr.appendChild(tdLabel);

      // 每個版本的翻譯 cell
      versions.forEach((v, vi)=>{
        const td = document.createElement('td');
        td.className = 'pick-cell';
        td.tabIndex = 0; // 可鍵盤聚焦
        td.setAttribute('role','button');
        td.dataset.vi = String(vi);
        const msg = v.map.get(key);
        if(!msg){
          td.classList.add('missing');
          td.innerHTML = '<div class="cell-content">（此檔無此訊息）</div>';
        } else {
          const preview = escapeHtml(getTransPreview(msg)) || '<i>（空白）</i>';
          td.innerHTML = `<div class="cell-box"><div class="cell-index">${vi+1}</div><div class="cell-content">${preview}</div></div>`;
        }
        td.addEventListener('click', ()=> selectCell(tr, td));
        td.addEventListener('keydown', (e)=>{ if(e.key==='Enter' || e.key===' '){ e.preventDefault(); selectCell(tr, td);} });
        tr.appendChild(td);
      });

      // 預設選第 1 欄
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

    // 依規則調整欄寬：<=4 欄平均分配；>4 欄每欄 25%，總寬 25%×欄數
    function adjustColumnWidths(){
      const totalCols = 1 + versions.length; // 原文 + 版本數
      $colgroup.innerHTML = '';

      if (totalCols <= 4){
        // 平均分配填滿 100%
        const w = (100 / totalCols).toFixed(6) + '%';
        for(let i=0;i<totalCols;i++){
          const col = document.createElement('col');
          col.style.width = w;
          $colgroup.appendChild(col);
        }
        $grid.style.width = '100%';
      }else{
        // 每欄固定 25%，表格總寬超過容器，水平可捲動
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
      $dl.disabled = true; $stat.textContent = '載入中…'; $msg.textContent=''; picked = new Map();

      const files = Array.from($files.files || []);
      if(files.length < 1){ $stat.textContent = '請選擇至少 1 個 .ts 檔'; return; }

      // 讀檔
      const texts = await Promise.all(files.map(readFileText));
      versions = texts.map((txt, i)=>({ ...parseTS(txt), name: files[i].name || `v${i+1}` }));
      base = versions[0];
      baseKeys = Array.from(base.map.keys());

      buildHeader(files);

      const frag = document.createDocumentFragment();
      baseKeys.forEach((key, idx)=>{ frag.appendChild(buildRow(idx, key)); });
      $tbody.appendChild(frag);

      adjustColumnWidths();     // ★ 依欄數調整欄寬
      $wrap.style.display = '';
      $dl.disabled = false;
      $stat.textContent = `已載入 ${files.length} 檔；訊息 ${baseKeys.length}（第 1 檔為預設）`;
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
          // 與第 1 欄不同才顯示
          const baseText = getTransPreview(versions[0].map.get(key));
          diff = versions.slice(1).some(v=> getTransPreview(v.map.get(key)) !== baseText);
        }

        tr.style.display = (match && (!onlyDiff || diff)) ? '' : 'none';
      });
    }

    function downloadMerged(){
      if(!base) return;
      const baseDoc = base.doc.cloneNode(true);

      // 對每個 base key，依 picked 選取，替換 translation
      baseKeys.forEach(key=>{
        const vi = picked.get(key) ?? 0;
        const srcMsg = (versions[vi] && versions[vi].map.get(key)) ? versions[vi].map.get(key) : base.map.get(key);

        // 定位 baseDoc 內對應 message
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

      // 輸出 XML
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

    // 綁定事件
    $build?.addEventListener('click', async ()=>{
      try{ await buildGrid(); }
      catch(e){ $msg.textContent='載入失敗：'+(e?.message||e); console.error(e); }
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