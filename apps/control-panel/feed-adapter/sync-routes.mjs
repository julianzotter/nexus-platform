/** Authorized routes to MOUNT inside the EXISTING private feed Worker.
 * Dependencies must be backed by the deployed authenticated worker, never by the browser.
 * runs, snapshots and runner lock must be SHARED across workers and durable.
 */
const STATUSES = new Set(['QUEUED','RUNNING','SUCCEEDED','FAILED']);
const HEADERS = {'Content-Type':'application/json; charset=utf-8','Cache-Control':'private, no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Vary':'Cookie, Authorization'};
const json=(status,body)=>new Response(JSON.stringify(body),{status,headers:HEADERS});
const error=(status,code)=>json(status,{error:code});
const RUN=/^\/api\/v1\/sync-runs\/([A-Za-z0-9_-]{8,100})$/;

export function makeSyncRoutes({authorize,verifyCsrf,runs,runner,snapshots,origin}) {
  if(![authorize,verifyCsrf,runs,runner,snapshots].every(Boolean)||!origin) throw Error('MISSING_WORKER_DEPENDENCY');
  return async request=>{
    const u=new URL(request.url), path=u.pathname;
    const start=path==='/api/v1/sync-runs', current=path==='/api/v1/snapshots/current', match=path.match(RUN);
    if(!start&&!current&&!match)return null; // preserve existing Feed routes
    if(request.method!==(start?'POST':'GET'))return error(405,'METHOD_NOT_ALLOWED');
    if(u.search||u.hash)return error(400,'UNSUPPORTED_QUERY');
    let user;
    try{user=await authorize(request,start?'nexus:sync':'nexus:read');}
    catch{return error(503,'IDENTITY_BACKEND_UNAVAILABLE');}
    if(!user?.id)return error(401,'UNAUTHENTICATED');
    if(user.allowed!==true)return error(403,'FORBIDDEN');
    if(start){
      if(request.headers.get('Origin')!==origin)return error(403,'ORIGIN_DENIED');
      if(request.headers.get('Content-Type')?.split(';')[0].trim()!=='application/json')return error(415,'CONTENT_TYPE_REQUIRED');
      if(Number(request.headers.get('Content-Length')||0)>1024)return error(413,'REQUEST_TOO_LARGE');
      try{if(!await verifyCsrf(request,user))return error(403,'CSRF_DENIED');}
      catch{return error(503,'CSRF_CHECK_UNAVAILABLE');}
      const bytes=await request.arrayBuffer();
      if(bytes.byteLength>1024)return error(413,'REQUEST_TOO_LARGE');
      // Fixed server configuration. No browser-provided Drive paths, Git refs or credentials.
      if(new TextDecoder().decode(bytes).trim()!=='{}')return error(422,'BODY_MUST_BE_EMPTY_OBJECT');
      try{
        // Existing runner must atomically deduplicate work using a durable shared lock.
        const run=await runner.enqueueCoalesced({principalId:user.id});
        if(!run?.id||!/^[A-Za-z0-9_-]{8,100}$/.test(run.id))return error(503,'INVALID_RUN_RECEIPT');
        return json(202,{runId:run.id,status:run.status||'QUEUED'});
      }catch{return error(503,'SYNC_RUNNER_UNAVAILABLE');}
    }
    if(match){
      try{
        const run=await runs.get(match[1]);
        if(!run||run.ownerId!==user.id)return error(404,'RUN_NOT_FOUND');
        if(!STATUSES.has(run.status))return error(503,'INVALID_RUN_STATE');
        const body={runId:run.id,status:run.status};
        if(run.status==='SUCCEEDED')body.snapshotRevision=run.snapshotRevision;
        if(run.status==='FAILED')body.errorCode=String(run.errorCode||'SYNC_FAILED').replace(/[^A-Z0-9_]/g,'').slice(0,64);
        return json(200,body);
      }catch{return error(503,'RUN_STORE_UNAVAILABLE');}
    }
    try{
      const snapshot=await snapshots.currentFor(user);
      if(!snapshot)return error(404,'NO_VALID_SNAPSHOT');
      const body=snapshot.body;
      if(!body||!Number.isFinite(Date.parse(body.observedAt))||
         !Array.isArray(body.workOrders)||!Array.isArray(body.reports)||
         !/^[0-9a-f]{64}$/.test(snapshot.revision||'')||snapshot.verified!==true)
        return error(503,'SNAPSHOT_UNVERIFIED');
      // Immutable readback and SHA-256 verification belong to the shared backend snapshot store.
      return json(200,{...body,revision:snapshot.revision,provenance:snapshot.provenance});
    }catch{return error(503,'SNAPSHOT_STORE_UNAVAILABLE');}
  };
}
