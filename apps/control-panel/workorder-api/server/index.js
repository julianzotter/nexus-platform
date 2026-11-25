const endpoint = '/api/v1/work-orders/WO-20261124-ID05-SYSTEMEVAL';
const panelOrigin = 'https://nexus-sync-diagnose.julianzotter.chatgpt.site';
const record = 'work-orders/WO-20261124-ID05-SYSTEMEVAL.json';
const ticket = 'WO-20261124-ID05-SYSTEMEVAL';
function validEvidence(v) {
  const sha = x => typeof x === 'string' && /^[0-9a-f]{40}$/.test(x);
  const short = x => typeof x === 'string' && x.length > 0 && x.length < 140;
  return v?.version === 1 && v.order === ticket && typeof v.checkedAt === 'string' &&
    Number.isFinite(Date.parse(v.checkedAt)) && Date.parse(v.checkedAt) <= Date.now()+60000 &&
    v.drive?.id === '1ekmdh6AIdLuOd35jpCq3kQhLlwze6CsP' && /^[0-9a-f]{64}$/.test(v.drive.hash) && short(v.drive.status) &&
    v.git?.repo === 'julianzotter/nexus-platform' && v.git.pr === 129 && v.git.branch === 'main' &&
    v.git.path === 'reports/system-evaluation/26_11_24_2351_ID05_WORKORDER_SYSTEMEVAL_LEDGER-PENDING.md' && sha(v.git.targetSha) && sha(v.git.head) &&
    short(v.git.status) && short(v.git.branchStatus) && short(v.git.prStatus) &&
    sha(v.process?.commit) && ['pr','delivery','ack','review','approval'].every(k=>short(v.process[k]));
}
function page() {
  return `<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>NEXUS · Work-Order-Datenpunkt</title><style>body{font:1rem/1.6 system-ui;max-width:65rem;margin:3rem auto;padding:0 1.5rem;color:#172036}dt{color:#536078}dd{margin:0 0 .6rem;overflow-wrap:anywhere}button,a{font:inherit}p{color:#475569}section{border-top:1px solid #cbd5e1}</style><main><h1>Work-Order-Datenpunkt</h1><p id="info" role="status">Daten werden abgerufen …</p><button id="refresh">Aktualisieren</button> <a href="${endpoint}">JSON öffnen</a><div id="facts"></div></main><script>
  const facts=document.querySelector('#facts'), info=document.querySelector('#info'), button=document.querySelector('#refresh');
  function section(title,rows){const s=document.createElement('section'), h=document.createElement('h2'), dl=document.createElement('dl');h.textContent=title;s.append(h,dl);for(const [k,v] of rows){const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=k;dd.textContent=v;dl.append(dt,dd)}return s}
  async function read(){button.disabled=true;try{const response=await fetch('${endpoint}',{cache:'no-store'});if(!response.ok)throw Error('HTTP '+response.status);const v=await response.json();info.textContent=v.order+' · Abruf '+new Date().toLocaleString('de-AT',{timeZone:'Europe/Vienna'})+' (Wien)';facts.replaceChildren(section('Anzeige',[['Quellen geprüft',v.checkedAt],['Zielrevision',v.git.targetSha]]),section('Artefakt',[['Drive',v.drive.status],['Drive-Datei',v.drive.id],['SHA-256',v.drive.hash],['GitHub · '+v.git.branch,v.git.status],['PR-Branch',v.git.branchStatus]]),section('Prozess',[['Commit',v.process.commit],['PR #'+v.git.pr,v.process.pr],['Zustellung',v.process.delivery],['Empfänger-ACK',v.process.ack],['Review',v.process.review],['Freigabe',v.process.approval]]));if(window.opener) window.opener.postMessage({type:'nexus-work-order-receipt',value:v},'${panelOrigin}')}catch(e){info.textContent='Datenpunkt nicht gelesen · '+e.message}finally{button.disabled=false}}
  button.onclick=read;read();
  </script></html>`;
}
export default {async fetch(request, env) {
  const path=new URL(request.url).pathname, origin=request.headers.get('Origin');
  const headers={'Cache-Control':'private, no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Vary':'Origin'};
  if(origin===panelOrigin){headers['Access-Control-Allow-Origin']=panelOrigin;headers['Access-Control-Allow-Credentials']='true';}
  const json=(data,status=200,extra={})=>new Response(JSON.stringify(data),{status,headers:{...headers,'Content-Type':'application/json',...extra}});
  if(path==='/') return request.method==='GET'?new Response(page(),{headers:{...headers,'Content-Type':'text/html; charset=utf-8'}}):json({error:'METHOD'},405);
  if(path!==endpoint)return json({error:'UNKNOWN_POINT'},404);
  if(request.method==='OPTIONS' && origin===panelOrigin)return new Response(null,{status:204,headers:{...headers,'Access-Control-Allow-Methods':'GET'}});
  if(!env.BUCKET)return json({error:'STORAGE_UNAVAILABLE'},503);
  if(request.method==='GET'){
    const got=await env.BUCKET.get(record);
    if(!got)return json({error:'AWAITING_FIRST_VERIFIED_SYNC'},503);
    return new Response(got.body,{headers:{...headers,'Content-Type':'application/json','ETag':got.httpEtag}});
  }
  if(request.method!=='PUT')return json({error:'METHOD'},405);
  // The owner-private Sites gate authenticates the integration; no browser-origin writes.
  if(origin || request.headers.get('X-Nexus-Sync')!=='verified-v1' || request.headers.get('Content-Type')!=='application/json')return json({error:'WRITER_ONLY'},403);
  const len=Number(request.headers.get('Content-Length'));if(!len||len>8192)return json({error:'SIZE'},413);
  let v;try{v=await request.json()}catch{return json({error:'JSON'},400)}
  if(!validEvidence(v))return json({error:'SCHEMA'},422);
  const old=await env.BUCKET.get(record);
  const serialized=JSON.stringify(v);
  if(old){const prior=await old.text();if(prior===serialized)return json({status:'UNCHANGED',etag:old.etag});if(Date.parse(JSON.parse(prior).checkedAt)>=Date.parse(v.checkedAt))return json({error:'STALE_OR_CONFLICT'},409);}
  const put=await env.BUCKET.put(record,serialized,{onlyIf:old?{etagMatches:old.etag}:{etagDoesNotMatch:'*'},httpMetadata:{contentType:'application/json'}});
  return put?json({status:'STORED',etag:put.etag}):json({error:'CONCURRENT_UPDATE'},409);
}};
