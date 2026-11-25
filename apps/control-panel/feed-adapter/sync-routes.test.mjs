import test from 'node:test';
import assert from 'node:assert/strict';
import {makeSyncRoutes} from './sync-routes.mjs';

const ORIGIN='https://nexus-work-sync.julianzotter.chatgpt.site';
const SHA='a'.repeat(64);
const request=(path,method='GET',headers={},body)=>new Request(ORIGIN+path,{method,headers,body});
function fixture(flags={}){
  let count=0;
  const handler=makeSyncRoutes({
    origin:ORIGIN,
    authorize:async()=>flags.unauth?null:{id:flags.other?'other':'owner',allowed:!flags.forbidden},
    verifyCsrf:async()=>!flags.badCsrf,
    runner:{enqueueCoalesced:async()=>{count++;return {id:'run_12345678',status:'QUEUED'};}},
    runs:{get:async()=>({id:'run_12345678',ownerId:'owner',status:'SUCCEEDED',snapshotRevision:SHA})},
    snapshots:{currentFor:async()=>flags.noSnapshot?null:{verified:!flags.unverified,revision:SHA,provenance:'CLOUD',body:{observedAt:'2026-11-25T17:00:00Z',workOrders:[],reports:[]}}}
  });
  return {handler,count:()=>count};
}
test('does not intercept existing routes',async()=>assert.equal(await fixture().handler(request('/feed')),null));
test('anonymous access denied to all routes',async()=>{
  const h=fixture({unauth:true}).handler;
  for(const [path,method,headers,body] of [
    ['/api/v1/sync-runs','POST',{'Origin':ORIGIN,'Content-Type':'application/json'},'{}'],
    ['/api/v1/sync-runs/run_12345678','GET',{},undefined],
    ['/api/v1/snapshots/current','GET',{},undefined]])
    assert.equal((await h(request(path,method,headers,body))).status,401);
});
test('POST requires identity scope, same-origin and CSRF',async()=>{
  const headers={'Origin':ORIGIN,'Content-Type':'application/json'};
  for(const [flags,h,body] of [
    [{forbidden:true},headers,'{}'],[{badCsrf:true},headers,'{}'],
    [{},{'Content-Type':'application/json'},'{}']])
    assert.equal((await fixture(flags).handler(request('/api/v1/sync-runs','POST',h,body))).status,403);
  assert.equal((await fixture().handler(request('/api/v1/sync-runs','POST',headers,'{"drive":"arbitrary"}'))).status,422);
});
test('POST reuses injected shared runner; GET has no sync side effect',async()=>{
  const f=fixture(), h={'Origin':ORIGIN,'Content-Type':'application/json'};
  const start=await f.handler(request('/api/v1/sync-runs','POST',h,'{}'));
  assert.equal(start.status,202);
  assert.equal((await start.json()).runId,'run_12345678');
  const check=await f.handler(request('/api/v1/sync-runs/run_12345678'));
  assert.equal((await check.json()).snapshotRevision,SHA);
  const snap=await f.handler(request('/api/v1/snapshots/current'));
  assert.equal((await snap.json()).revision,SHA);
  assert.equal(f.count(),1);
});
test('owner separation; unverified snapshot cannot pass',async()=>{
  assert.equal((await fixture({other:true}).handler(request('/api/v1/sync-runs/run_12345678'))).status,404);
  assert.equal((await fixture({unverified:true}).handler(request('/api/v1/snapshots/current'))).status,503);
  assert.equal((await fixture({noSnapshot:true}).handler(request('/api/v1/snapshots/current'))).status,404);
});
