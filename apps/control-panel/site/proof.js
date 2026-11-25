'use strict';
// The private PR supplies the receipt in the URL fragment. Its contents never go in a network request.
const receiptKey = 'nexus.reviewReceipt';
const receiptDigest = '9bf85d2cd073d88defe2952aca3e6a8eb07de25b71b655830dfc933dfac27fc5';
let orderReceipt = null;
let receiptError = '';
async function digestBytes(bytes) {
  const hash = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(hash), byte => byte.toString(16).padStart(2, '0')).join('');
}
async function openReviewReceipt() {
  const fragment = location.hash.startsWith('#proof=') ? location.hash.slice(7) : null;
  if (fragment !== null) history.replaceState(null, '', location.pathname + location.search + '#overview');
  try {
    let encoded = fragment;
    if (!encoded) { try { encoded = sessionStorage.getItem(receiptKey); } catch {} }
    if (!encoded) return;
    if (encoded.length > 6000) throw new Error();
    const raw = Uint8Array.from(atob(encoded.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0));
    if (await digestBytes(raw) !== receiptDigest) throw new Error();
    orderReceipt = JSON.parse(new TextDecoder().decode(raw));
    try { sessionStorage.setItem(receiptKey, encoded); } catch {}
  } catch { receiptError = 'Dieser Beleg passt nicht zur geprüften Revision.'; }
}
function orderEvidenceView() {
  const r = orderReceipt;
  const row = (k,v) => '<dt>'+esc(k)+'</dt><dd>'+esc(v)+'</dd>';
  const box = (title,body) => '<article><h3>'+title+'</h3><dl>'+body+'</dl></article>';
  const dash = 'Ungeprüft';
  const drive = r ? 'https://drive.google.com/file/d/'+r.drive.id+'/view' : '';
  const pr = r ? 'https://github.com/'+r.git.repo+'/pull/'+r.git.pr : '';
  return '<section class="panel proof"><div class="panel-head"><div><h2>Quellenprüfung und Work Order</h2><p>'+
    (r ? esc(r.order)+' · Beleg vom '+localTime(r.checkedAt) : esc(receiptError || 'Kein persönlicher Prüfbeleg im Browser geladen.'))+
    '</p></div><button id="connectPoint" class="btn">Privaten Datenpunkt öffnen</button></div><div class="proof-grid">'+
    box('Anzeige',row('Seitenabruf',state.panelRead ? localTime(state.panelRead) : dash)+row('Datenstand',localTime(state.data.asOf))+row('Panel-JSON · SHA-256',state.panelHash || dash)+row('Datenpunkt abgerufen',pointRead ? localTime(pointRead) : 'Ausstehend')+row('Drive/GitHub geprüft',r ? localTime(r.checkedAt) : dash))+
    box('Artefakt',row('Drive',r?.drive.status || dash)+row('Zielbranch',r ? r.git.branch+' · '+r.git.status : dash)+row('Zielrevision',r?.git.targetSha || dash)+row('PR-Branch',r?.git.branchStatus || dash)+row('Datei · SHA-256',r?.drive.hash || dash))+
    box('Prozess',row('Commit',r?.process.commit || dash)+row('Pull Request',r ? '#'+r.git.pr+' · '+r.process.pr : dash)+row('Zustellung',r?.process.delivery || dash)+row('Empfänger-ACK',r?.process.ack || dash)+row('Review',r?.process.review || dash)+row('Freigabe',r?.process.approval || dash))+
    '</div>'+(pointError ? '<p class="warn">'+esc(pointError)+'</p>' : '')+(r ? '<p class="proof-links">'+link(drive,'Drive-Datei')+' · '+link(pr,'Aktueller PR')+'</p>' : '')+'</section>';
}
