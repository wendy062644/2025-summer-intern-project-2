<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>TS 多版本合併選擇介面</title>
  <style>
    /* —— 全部樣式只限制在 #ts-ui（延續你原本的 design tokens）—— */
    #ts-ui{
      --ts-gap: 12px; --ts-pad: 14px; --ts-radius: 12px;
      --ts-border: #e5e7eb; --ts-bg: #fff; --ts-muted: #6b7280; --ts-text: #111827;
      --ts-surface: #fff; --ts-surface-2: #f9fafb; --ts-accent: #3b82f6; --ts-on-accent: #fff;
      --ts-link: #2563eb; --ts-progress-bg:#eef2f7; --ts-table-head-bg:#f8fafc; --ts-focus: 0 0 0 2px rgba(59,130,246,.35);
      font-family: system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans", "PingFang TC", "Microsoft JhengHei", sans-serif;
      line-height: 1.35; color: var(--ts-text); margin: 18px auto; max-width: 1100px; padding: 0 10px;
    }
    @media (prefers-color-scheme: dark){
      #ts-ui{ --ts-border:#2b2f36; --ts-bg:#0f1115; --ts-surface:#111418; --ts-surface-2:#0b0f14; --ts-text:#e7eaf0; --ts-muted:#a6afbd; --ts-link:#8ab4ff; --ts-progress-bg:#1a1f29; --ts-table-head-bg:#121621; --ts-on-accent:#0b0f14; }
    }
    #ts-ui *, #ts-ui *::before, #ts-ui *::after{ box-sizing: border-box; }
    #ts-ui .ts-card{ border:1px solid var(--ts-border); background:var(--ts-surface); border-radius: var(--ts-radius); padding:16px; box-shadow:0 1px 2px rgba(0,0,0,.04); }
    #ts-ui .ts-title{ font-size:1.05rem; font-weight:700; margin:2px 0 10px; }
    #ts-ui .ts-grid{ display:grid; grid-template-columns: 1fr 1fr; gap:10px 14px; align-items:center; }
    #ts-ui .ts-field{ display:flex; flex-direction:column; gap:6px; }
    #ts-ui .ts-label{ color:var(--ts-muted); font-size:.95rem; }
    #ts-ui .ts-hint{ color:var(--ts-muted); font-size:.9rem; }
    #ts-ui .ts-input input{ width:100%; padding:8px 10px; border:1px solid var(--ts-border); border-radius:10px; background:transparent; font-size:.95rem; color:var(--ts-text); }
    #ts-ui .ts-input input:focus{ outline:none; box-shadow: var(--ts-focus); border-color: color-mix(in oklab, var(--ts-accent) 60%, var(--ts-border)); }
    #ts-ui .ts-btn{ appearance:none; border:1px solid var(--ts-border); background:var(--ts-accent); color:var(--ts-on-accent); border-radius:10px; padding:8px 14px; font-weight:600; cursor:pointer; }
    #ts-ui .ts-btn:hover{ filter:brightness(1.06); }
    #ts-ui .ts-btn:disabled{ opacity: .55; cursor:not-allowed; }
    #ts-ui .ts-inline{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
    #ts-ui .ts-divider{ height:1px; background:var(--ts-border); margin:12px 0; border:0; }

    /* 表格 */
    #table-wrap{ border:1px solid var(--ts-border); border-radius:12px; overflow:hidden; background:var(--ts-surface); }
    #merge-table{ width:100%; border-collapse:collapse; font-size:.95rem; }
    #merge-table thead th{ background:var(--ts-table-head-bg); position:sticky; top:0; z-index:1; }
    #merge-table th, #merge-table td{ padding:8px 10px; border-bottom:1px solid var(--ts-border); text-align:left; vertical-align:top; }
    .src-cell{ width:40%; }

    /* 選項清單（條列） */
    .choice-list{ display:flex; flex-direction:column; gap:8px; }
    .choice-item{ display:flex; align-items:flex-start; gap:10px; padding:8px; border:1px solid var(--ts-border); border-radius:10px; background:var(--ts-surface-2); }
    .choice-item[disabled]{ opacity:.6; }
    .choice-item label{ display:block; cursor:pointer; }
    .filename{ font-size:.85rem; color:var(--ts-muted); }
    .trans-snippet{ white-space:pre-wrap; word-break:break-word; }

    /* 工具列 */
    .toolbar{ display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-top:8px; }
    .kpi{ font-variant-numeric: tabular-nums; color:var(--ts-muted); }

    @media (max-width: 720px){ .src-cell{ width:auto; } }
  </style>
</head>
<body>
<div id="ts-ui">
  <div class="ts-card">
    <div class="ts-title">TS 多版本合併選擇</div>
    <div class="ts-grid">
      <div class="ts-field">
        <label for="tsFiles" class="ts-label">.ts 檔（可多選；第一個為「底稿／預設」）</label>
        <div class="ts-input"><input id="tsFiles" type="file" accept=".ts" multiple></div>
      </div>
      <div class="ts-field">
        <label class="ts-label" for="searchBox">關鍵字過濾（原文/譯文）</label>
        <div class="ts-input"><input id="searchBox" type="text" placeholder="輸入關鍵字以過濾條目"></div>
      </div>
    </div>

    <div class="toolbar">
      <button class="ts-btn" id="buildBtn">生成表格</button>
      <button class="ts-btn" id="downloadBtn" disabled>下載合併檔</button>
      <span class="kpi" id="stat">尚未載入</span>
    </div>

    <hr class="ts-divider"/>

    <div id="table-wrap" style="display:none; max-height: 65vh; overflow:auto;">
      <table id="merge-table" aria-label="多版本合併表">
        <thead>
          <tr>
            <th class="src-cell">原文（context / source）</th>
            <th>選擇版本（顯示各版譯文；預設選第一個檔案）</th>
          </tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>

    <div class="ts-hint" style="margin-top:8px;">
      使用說明：選擇多個 .ts 檔後按「生成表格」，每一列為一個訊息。預設選第一個檔案的譯文；可改勾其他版本。按「下載合併檔」輸出 .ts，內容以被勾選版本的 &lt;translation&gt; 為主（未勾選仍採第一個檔案）。
    </div>
  </div>

  <div id="msg" style="margin-top:10px; color:var(--ts-muted);"></div>
</div>

<script>
(function(){
  const $ = (s) => document.querySelector(s);
  const $tbody = $('#tbody');
  const $wrap  = $('#table-wrap');
  const $build = $('#buildBtn');
  const $dl    = $('#downloadBtn');
  const $stat  = $('#stat');
  const $msg   = $('#msg');
  const $files = $('#tsFiles');
  const $search= $('#searchBox');

  /**
   * Util: 讀取檔案文字
   */
  function readFileText(file){
    return new Promise((resolve,reject)=>{ const fr = new FileReader(); fr.onload=()=>resolve(String(fr.result||'')); fr.onerror=()=>reject(fr.error); fr.readAsText(file, 'utf-8'); });
  }

  /**
   * Util: 取 DOCTYPE（保留原檔資訊）
   */
  function readDoctype(xmlText){
    const m = xmlText.match(/<!DOCTYPE[^>]+>/);
    return m ? m[0] : '';
  }

  /**
   * 解析 .ts：回傳 {doc, doctype, map: key->message, meta: key->{context, source}}
   * key = contextName + "\u241F" + sourceText
   */
  function parseTS(xmlText){
    const doctype = readDoctype(xmlText);
    const parser = new DOMParser();
    const xml = parser.parseFromString(xmlText, 'application/xml');
    if(xml.getElementsByTagName('parsererror').length){ throw new Error('XML 解析失敗，請確認 .ts 格式'); }
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

  /**
   * 取得顯示用譯文摘要（含 numerus）
   */
  function getTranslationPreview(messageEl){
    if(!messageEl) return '(無此訊息)';
    const trans = messageEl.getElementsByTagName('translation')[0];
    if(!trans) return '(無 translation)';
    const forms = trans.getElementsByTagName('numerusform');
    if(forms && forms.length){
      const parts = [];
      for(let i=0;i<forms.length;i++){ parts.push(forms[i].textContent || ''); }
      return parts.join(' | ');
    }
    return trans.textContent || '';
  }

  /**
   * 將 baseDoc 中對應訊息的 <translation> 以 srcDoc 的同節點取代（深拷貝）
   */
  function replaceTranslation(baseDoc, baseMsg, srcMsg){
    if(!baseMsg || !srcMsg) return;
    const baseTrans = baseMsg.getElementsByTagName('translation')[0];
    const srcTrans  = srcMsg.getElementsByTagName('translation')[0];
    if(!srcTrans) return; // 沒有就不動
    const imported = baseDoc.importNode(srcTrans, true);
    if(baseTrans){ baseMsg.replaceChild(imported, baseTrans); }
    else{ baseMsg.appendChild(imported); }
  }

  /**
   * 建立一列（條列型選單）
   */
  function buildRow(rowIdx, key, metaBase, versions){
    const tr = document.createElement('tr');

    const tdSrc = document.createElement('td');
    tdSrc.className = 'src-cell';
    const ctxName = metaBase.context || '(no-context)';
    const src = metaBase.source || '';
    tdSrc.innerHTML = `<div style="font-weight:600;">${escapeHtml(src)}</div><div class="ts-hint">${escapeHtml(ctxName)}</div>`;

    const tdPick = document.createElement('td');
    const list = document.createElement('div');
    list.className = 'choice-list';

    versions.forEach((v, vi)=>{
      const wrap = document.createElement('div');
      wrap.className = 'choice-item';

      const labelId = `pick-${rowIdx}-${vi}`;
      const radio = document.createElement('input');
      radio.type = 'radio';
      radio.name = `pick-${rowIdx}`; // 每列互斥
      radio.id = labelId;
      radio.value = String(vi);
      if(vi === 0) radio.checked = true; // 預設第一個

      const msg = v.map.get(key);
      const has = !!msg;
      if(!has){
        radio.disabled = true;
        wrap.setAttribute('disabled','');
      }

      const label = document.createElement('label');
      label.htmlFor = labelId;
      const fname = escapeHtml(v.name || `v${vi+1}`);
      const snippet = has ? escapeHtml(getTranslationPreview(msg)) : '（此檔無此訊息）';
      label.innerHTML = `<div class="filename">${vi+1}. ${fname}</div><div class="trans-snippet">${snippet || '<i>（空白）</i>'}</div>`;

      wrap.appendChild(radio);
      wrap.appendChild(label);
      list.appendChild(wrap);
    });

    tdPick.appendChild(list);

    tr.appendChild(tdSrc);
    tr.appendChild(tdPick);
    tr.dataset.key = key;
    return tr;
  }

  function escapeHtml(s){
    return String(s||'').replace(/[&<>"']/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;' }[c]));
  }

  /**
   * 狀態
   */
  let versions = []; // [{name, doc, doctype, map, meta}]
  let base = null;   // versions[0]
  let baseKeys = []; // 只用第一個檔案作為底稿的 key 列表

  /**
   * 生成表格
   */
  async function buildTable(){
    $tbody.innerHTML = '';
    $wrap.style.display = 'none';
    $dl.disabled = true; $stat.textContent = '載入中…'; $msg.textContent='';

    const files = Array.from($files.files || []);
    if(files.length < 1){ $stat.textContent = '請選擇至少 1 個 .ts 檔'; return; }

    // 讀所有檔
    const texts = await Promise.all(files.map(readFileText));
    versions = texts.map((txt, i)=>({ ...parseTS(txt), name: files[i].name || `v${i+1}` }));

    base = versions[0];
    // 以第一個檔案的訊息作為輸出底稿
    baseKeys = Array.from(base.map.keys());

    // 建表
    baseKeys.forEach((key, idx)=>{
      const metaBase = base.meta.get(key) || {context:'', source:''};
      const tr = buildRow(idx, key, metaBase, versions);
      $tbody.appendChild(tr);
    });

    $wrap.style.display = '';
    $dl.disabled = false;
    $stat.textContent = `已載入 ${files.length} 檔；條目數 ${baseKeys.length}（以第 1 檔為底稿）`;
    applyFilter();
  }

  /**
   * 依關鍵字過濾（原文/譯文）
   */
  function applyFilter(){
    const q = ($search.value || '').trim().toLowerCase();
    if(!q){ Array.from($tbody.children).forEach(tr=>tr.style.display=''); return; }
    const terms = q.split(/\s+/).filter(Boolean);

    Array.from($tbody.children).forEach(tr=>{
      const key = tr.dataset.key;
      let text = '';
      const metaBase = base.meta.get(key) || {context:'',source:''};
      text += (metaBase.source||'') + ' ' + (metaBase.context||'');
      // 各版譯文也檢索
      versions.forEach(v=>{
        const m = v.map.get(key);
        text += ' ' + (m ? getTranslationPreview(m) : '');
      });
      const lc = text.toLowerCase();
      const hit = terms.every(t=> lc.includes(t));
      tr.style.display = hit ? '' : 'none';
    });
  }

  /**
   * 下載合併檔（以第一個檔案為基礎，逐列取用選中的 <translation>）
   */
  function downloadMerged(){
    if(!base){ return; }
    const baseDoc = base.doc.cloneNode(true);

    Array.from($tbody.children).forEach((tr, idx)=>{
      if(tr.style.display==='none') return; // 過濾不影響輸出，但可視需求忽略隱藏列
      const key = tr.dataset.key;
      const baseMsg = base.map.get(key); // in original
      // 找到 baseDoc 中對應的 message（需重新尋找，不能用原節點引用）
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
      if(!targetMsg) return;

      // 取選到的版本 index
      const picked = tr.querySelector(`input[name="pick-${idx}"]:checked`);
      const vi = picked ? Number(picked.value) : 0;
      const srcMsg = versions[vi] && versions[vi].map.get(key) ? versions[vi].map.get(key) : baseMsg;
      replaceTranslation(baseDoc, targetMsg, srcMsg);
    });

    // 序列化
    const xmlDecl = '<?xml version="1.0" encoding="utf-8"?>\n';
    const ser = new XMLSerializer();
    let xmlOut = ser.serializeToString(baseDoc);
    const doctype = base.doctype;
    if(doctype){ xmlOut = xmlDecl + doctype + xmlOut; }
    else{ xmlOut = xmlDecl + xmlOut; }

    const blob = new Blob([xmlOut], {type:'application/xml'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'merged.ts';
    document.body.appendChild(a);
    a.click();
    setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); }, 0);
  }

  $build.addEventListener('click', async ()=>{
    try{ await buildTable(); }catch(e){ $msg.textContent = '載入失敗：' + (e?.message || e); console.error(e); }
  });
  $dl.addEventListener('click', downloadMerged);
  $search.addEventListener('input', applyFilter);
})();
</script>
</body>
</html>
