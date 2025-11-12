---
title: merge
---

# 檔案合併(將已翻譯內容覆蓋原文)

> 功能：上傳 2 個 .ts 檔（目標檔 與 來源檔）。僅當 **`<source>` 完全相同** 時，將來源檔對應訊息的 `<translation>` 覆蓋到目標檔。

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

  #table-wrap{ border:1px solid var(--ts-border); border-radius:12px; overflow:auto; max-height:70vh; }
  #ts-ui table{
    width:100%;
    border-collapse:separate; border-spacing:0;
    table-layout: fixed;
  }
  thead th{ position:sticky; top:0; z-index:3; background:var(--ts-head-bg); border-bottom:1px solid var(--ts-border); padding:10px; text-align:left; font-weight:700; }
  tbody td, tbody th{ border-bottom:1px solid var(--ts-border); }
  th, td{ padding:8px 10px; vertical-align:top; }
  /* 取消固定 34% 寬，交給 colgroup 控制比例 */
  .row-label{ width:auto; max-width:none; }
  .cell-content{ white-space:pre-wrap; word-break:break-word; }
  .will{ font-weight:700; }
  .ok { color:#059669; }
  .skip{ color:#ef4444; }
</style>

<div id="ts-ui">
  <div class="ts-card">
    <div class="ts-grid">
      <div class="ts-field">
        <label class="ts-label">目標檔（被覆蓋）</label>
        <div class="ts-input"><input id="fileTarget" type="file" accept=".ts"></div>
      </div>
      <div class="ts-field">
        <label class="ts-label">來源檔（提供譯文）</label>
        <div class="ts-input"><input id="fileSource" type="file" accept=".ts"></div>
      </div>
      <div class="ts-field">
        <label class="ts-label">動作</label>
        <div class="toolbar">
          <button class="ts-btn" id="previewBtn">產生預覽</button>
          <button class="ts-btn" id="downloadBtn" disabled>下載覆蓋後檔</button>
        </div>
      </div>
    </div>

    <div class="toolbar" style="margin-top:6px; gap:16px;">
      <label><input type="checkbox" id="optNonEmptyOnly" checked> 只覆蓋來源「非空」譯文</label>
      <label><input type="checkbox" id="optFillEmptyOnly"> 只填補目標「空白」譯文（目標非空則跳過）</label>
      <label><input type="checkbox" id="optShowUpdatesOnly"> 只顯示將被覆蓋的項目</label>
      <label style="margin-left:auto;display:flex;align-items:center;gap:6px;">
        <span class="ts-label">關鍵字過濾</span>
        <div class="ts-input" style="min-width:220px;"><input id="searchBox" type="text" placeholder="搜尋 source / 目前譯文 / 來源譯文"></div>
      </label>
    </div>
    <div class="toolbar"><span class="kpi" id="stat">尚未載入</span></div>
    <hr class="ts-divider"/>

    <div id="table-wrap" style="display:none;">
      <table id="grid">
        <colgroup>
          <!-- 前三欄等分「扣掉動作欄 150px」後的剩餘寬度 -->
          <col style="width: calc((100% - 150px) / 3 - 0.5px)">
          <col style="width: calc((100% - 150px) / 3 - 0.5px)">
          <col style="width: calc((100% - 150px) / 3 - 0.5px)">
          <col style="width: 150px">
        </colgroup>
        <thead>
          <tr>
            <th>原文（source）</th>
            <th>目標檔目前譯文</th>
            <th>來源檔擬覆蓋譯文</th>
            <th>動作</th>
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

    let target = null;  // {doc, doctype, name, messages: [{ctx,src,msgEl}], mapByKey}
    let source = null;  // {doc, doctype, name, mapBySource: Map<string, Element[]>, dupSources: string[]}
    let previewRows = []; // [{key, src, tgtText, srcText, will, reason, ctx}]

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

    function parseXML(text){
      const parser = new DOMParser();
      const xml = parser.parseFromString(text, 'application/xml');
      if(xml.getElementsByTagName('parsererror').length){
        throw new Error('XML 解析失敗，請確認 .ts 格式');
      }
      return xml;
    }

    function getTranslationPreview(messageEl){
      if(!messageEl) return '';
      const trans = messageEl.getElementsByTagName('translation')[0];
      if(!trans) return '';
      const forms = trans.getElementsByTagName('numerusform');
      if(forms && forms.length){
        const arr=[]; for(let i=0;i<forms.length;i++){ arr.push(forms[i].textContent||''); }
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
          if((forms[i].textContent||'').trim()!== '') return true;
        }
        return false;
      }
      return (t.textContent||'').trim() !== '';
    }

    function parseTarget(text, name){
      const doctype = readDoctype(text);
      const doc = parseXML(text);
      const messages=[];
      const mapByKey = new Map();
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
          const key = ctxName + '\\u241F' + src;
          const rec = {ctx: ctxName, src, msgEl: m, key};
          messages.push(rec);
          mapByKey.set(key, m);
        }
      }
      return {doc, doctype, name, messages, mapByKey};
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
          else { map.get(src).push(m); if(map.get(src).length===2) dups.push(src); }
        }
      }
      return {doc, doctype, name, mapBySource: map, dupSources: dups};
    }

    function buildPreview(){
      previewRows = [];
      const nonEmptyOnly = $nonEmpty.checked;
      const fillEmptyOnly = $fillEmpty.checked;

      for(const rec of target.messages){
        const srcList = source.mapBySource.get(rec.src);
        const srcMsg = srcList && srcList.length ? srcList[0] : null; // 取第一筆
        const tgtText = getTranslationPreview(rec.msgEl);
        const srcText = getTranslationPreview(srcMsg);
        let will=false, reason='';
        if(!srcMsg){ will=false; reason='來源無此 source'; }
        else if(nonEmptyOnly && !hasNonEmptyTranslation(srcMsg)){ will=false; reason='來源譯文為空'; }
        else if(fillEmptyOnly && hasNonEmptyTranslation(rec.msgEl)){ will=false; reason='目標已有非空譯文'; }
        else { will=true; reason='覆蓋'; }
        previewRows.push({key:rec.key, ctx:rec.ctx, src:rec.src, tgtText, srcText, will, reason});
      }
    }

    function renderPreview(){
      const q = ($search.value||'').trim().toLowerCase();
      const showUpdOnly = $onlyUpd.checked;
      $tbody.innerHTML = '';
      let shown=0, totalWill=0;
      const frag = document.createDocumentFragment();
      for(const r of previewRows){
        if(showUpdOnly && !r.will) continue;
        const hay = (r.src + ' ' + (r.tgtText||'') + ' ' + (r.srcText||'')).toLowerCase();
        if(q && !hay.includes(q)) continue;
        const tr = document.createElement('tr');
        const td0 = document.createElement('th'); td0.className='row-label';
        td0.innerHTML = '<div style="font-weight:700;">'+escapeHtml(r.src)+'</div>'+
                        '<div class="ts-label">'+escapeHtml(r.ctx)+'</div>';
        const td1 = document.createElement('td'); td1.innerHTML = '<div class="cell-content">'+escapeHtml(r.tgtText||'')+'</div>';
        const td2 = document.createElement('td'); td2.innerHTML = '<div class="cell-content">'+escapeHtml(r.srcText||'')+'</div>';
        const td3 = document.createElement('td');
        td3.className = 'will ' + (r.will? 'ok':'skip');
        td3.textContent = r.will ? '覆蓋' : ('跳過：'+r.reason);
        tr.appendChild(td0); tr.appendChild(td1); tr.appendChild(td2); tr.appendChild(td3);
        frag.appendChild(tr);
        shown++; if(r.will) totalWill++;
      }
      $tbody.appendChild(frag);
      $wrap.style.display = shown? '' : 'none';
      $download.disabled = !shown || !previewRows.some(r=>r.will);

      const total = previewRows.length;
      const dupN = source.dupSources.length;
      $stat.textContent = `匹配源文字：${total}；預計覆蓋：${totalWill}；來源重複 source：${dupN}${dupN? '（取第一筆）':''}`;
      if(dupN){ $msg.textContent = '注意：來源檔出現重複 source 共 '+dupN+' 筆（僅採第一筆）。'; }
      else { $msg.textContent=''; }
    }

    function escapeHtml(s){
      return String(s||'').replace(/[&<>\"']/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;','\'':'&#39;' }[c]));
    }

    function applyAndDownload(){
      // 準備 target 複本與快速索引（ctx+\u241F+src）
      const outDoc = target.doc.cloneNode(true);
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
          keyMap.set(ctxName + '\\u241F' + s, m);
        }
      }

      const nonEmptyOnly = $nonEmpty.checked;
      const fillEmptyOnly = $fillEmpty.checked;

      let applied=0;
      for(const r of previewRows){
        if(!r.will) continue;
        const targetMsg = keyMap.get(r.key);
        const srcList = source.mapBySource.get(r.src);
        const srcMsg = srcList && srcList.length ? srcList[0] : null;
        if(!targetMsg || !srcMsg) continue;
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
      if(doctype){ xmlOut = xmlDecl + doctype + xmlOut; } else { xmlOut = xmlDecl + xmlOut; }

      const blob = new Blob([xmlOut], {type:'application/xml'});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      const baseName = (target.name||'target').replace(/\.ts$/i,'');
      a.download = baseName + '.overlay.ts';
      document.body.appendChild(a);
      a.click();
      setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); }, 0);

      $msg.textContent = '已套用覆蓋並匯出（實際覆蓋 '+applied+' 筆）。';
    }

    async function doPreview(){
      try{
        $tbody.innerHTML=''; $wrap.style.display='none'; $download.disabled = true;
        $stat.textContent='載入中…'; $msg.textContent='';
        const fT = $fileTarget.files && $fileTarget.files[0];
        const fS = $fileSource.files && $fileSource.files[0];
        if(!fT || !fS){ $stat.textContent='請選擇 2 個 .ts 檔（目標與來源）'; return; }
        const [tText, sText] = await Promise.all([readFileText(fT), readFileText(fS)]);
        target = parseTarget(tText, fT.name);
        source = parseSource(sText, fS.name);
        buildPreview();
        renderPreview();
      }catch(e){
        console.error(e); $stat.textContent='載入失敗'; $msg.textContent='錯誤：'+(e?.message||e);
      }
    }

    $preview?.addEventListener('click', doPreview);
    $download?.addEventListener('click', applyAndDownload);
    $search?.addEventListener('input', renderPreview);
    $onlyUpd?.addEventListener('change', renderPreview);
    $nonEmpty?.addEventListener('change', ()=>{ buildPreview(); renderPreview(); });
    $fillEmpty?.addEventListener('change', ()=>{ buildPreview(); renderPreview(); });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
</script>