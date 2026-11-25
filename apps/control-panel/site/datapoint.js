const pointOrigin = 'https://nexus-work-sync.julianzotter.chatgpt.site';
const pointPath = '/api/v1/work-orders/WO-20261124-ID05-SYSTEMEVAL';
let pointRead = null, pointError = '', pointPending = null, pointWindow = null;
function isReceipt(v) {
  return v?.version === 1 && v.order === 'WO-20261124-ID05-SYSTEMEVAL' && Number.isFinite(Date.parse(v.checkedAt))
    && v.git?.repo === 'julianzotter/nexus-platform' && v.git?.pr === 129 && v.drive?.id === '1ekmdh6AIdLuOd35jpCq3kQhLlwze6CsP'
    && /^[a-f0-9]{40}$/.test(v.git.head) && /^[a-f0-9]{40}$/.test(v.git.targetSha) && /^[a-f0-9]{64}$/.test(v.drive.hash)
    && v.process && ['pr','commit','delivery','ack','review','approval'].every(k=>typeof v.process[k]==='string');
}
function repaintPoint() { const view=document.querySelector('.proof'); if(view && state.data) view.outerHTML=orderEvidenceView(); }
function applyPoint(v) {
  if(!isReceipt(v)) throw new Error('Ungültiger Datenbeleg');
  if(orderReceipt && Date.parse(v.checkedAt)<Date.parse(orderReceipt.checkedAt)) throw new Error('Älterer Beleg empfangen');
  orderReceipt=v; pointRead=new Date().toISOString(); pointError=''; repaintPoint();
}
function refreshPoint() {
  if(pointPending) return pointPending;
  pointPending=(async()=>{
    try {const res=await fetch(pointOrigin+pointPath,{credentials:'include',cache:'no-store',signal:AbortSignal.timeout(7500)});
      if(!res.ok || !res.headers.get('Content-Type')?.includes('application/json'))throw new Error('Geschützten Datenpunkt öffnen');
      await Promise.resolve(applyPoint(await res.json())); return true;
    } catch {pointError='Privaten Datenpunkt öffnen und anmelden. Ein vorhandener Beleg behält seinen Prüfzeitpunkt.';repaintPoint();return false;}
  })().finally(()=>{pointPending=null});
  return pointPending;
}
document.addEventListener('click',event=>{if(event.target.closest?.('#connectPoint')) pointWindow=window.open(pointOrigin+'/','nexusPrivatePoint');});
window.addEventListener('message',event=>{if(event.origin!==pointOrigin || !pointWindow || event.source!==pointWindow || event.data?.type!=='nexus-work-order-receipt')return;
  try{applyPoint(event.data.value)}catch{pointError='Ungültiger Datenpunktbeleg';repaintPoint();}
});
