const teamStateLabel = {
  ACTIVE: 'Arbeitet', BLOCKED: 'Blockiert', AVAILABLE: 'Verfügbar gemeldet',
  COMPLETE: 'Abgeschlossen', UNKNOWN: 'Ohne Nachweis', REPORTED: 'Bericht liegt vor'
};
const team = {
  snapshot: null, checked: null, problem: '', handle: null, timer: null,
  clock: null, epoch: 0, busy: false, signature: ''
};
const teamTime = new Intl.DateTimeFormat('de-AT', {
  timeZone:'Europe/Vienna',day:'2-digit',month:'2-digit',year:'numeric',
  hour:'2-digit',minute:'2-digit',second:'2-digit'
});
function teamTimestamp(value) {
  return Number.isFinite(Date.parse(value)) ? teamTime.format(Date.parse(value)) : 'Zeitpunkt offen';
}
function teamStatus(entry, now, failed) {
  if (entry.state !== 'ACTIVE') return entry.state;
  const age = now - Date.parse(entry.observedAt);
  return !failed && age >= 0 && age <= 30000 ? 'ACTIVE' : 'STALE';
}
function validateTeamSnapshot(raw) {
  if (!raw || !Number.isFinite(Date.parse(raw.asOf)) || !Array.isArray(raw.entries)) {
    throw new Error('Ungültiger Datenstand oder fehlende Meldungsliste.');
  }
  for (const entry of raw.entries) {
    if (!entry || typeof entry.actor !== 'string' || !entry.actor.trim()
        || !Object.hasOwn(teamStateLabel, entry.state) || !Array.isArray(entry.files)
        || entry.files.some(file => typeof file !== 'string')) {
      throw new Error('Eine Meldung enthält ungültige Felder.');
    }
  }
  return raw;
}
function teamPanel() {
  return `<div class="page-heading"><div><h1>Kontrollpanel</h1><p>Arbeitsaufträge, Dateinachweise und Entscheidungen im NEXUS-Team</p></div></div>
  <section class="panel team-panel"><div class="team-bar"><div><h2>Meldequelle</h2><p id="team-source"></p></div><div class="team-actions">
  ${typeof window.showOpenFilePicker === 'function' ? '<button class="btn" id="team-connect">Lokale Statusdatei verbinden</button>' : ''}
  <a class="btn" target="_blank" rel="noopener noreferrer" href="https://drive.google.com/file/d/1hUswc3CCUlXR8s0r0a3r7kOEF45ZlEcU/view">Aktuellen Drive-Stand öffnen</a><button class="btn" id="team-default" hidden>Site-Daten anzeigen</button><button class="btn" id="team-now">Jetzt abrufen</button></div></div>
  <p id="team-check" class="team-timing"></p><p id="team-problem" role="status" class="team-warn" hidden></p></section>
  <section class="panel team-panel"><div class="team-bar"><h2>Arbeitsmeldungen</h2><label>Anzeige <select id="team-filter"><option value="all">Alle Meldungen</option><option value="BLOCKED">Blockiert</option><option value="ACTIVE">Arbeitet</option><option value="STALE">Lebenszeichen abgelaufen</option><option value="COMPLETE">Abgeschlossen</option><option value="UNKNOWN">Ohne Nachweis</option></select></label></div>
  <div id="team-list"></div></section>`;
}
function teamSourceLink(source) {
  if (!source) return '';
  try {
    const url = new URL(source);
    if (url.protocol === 'https:') return ext(url.href,'Quelle öffnen');
  } catch { /* A local source can be shown as text. */ }
  return esc(source);
}
function teamRow(entry, state) {
  const label = state === 'STALE' ? 'Lebenszeichen abgelaufen' : teamStateLabel[state];
  const files = entry.files.length ? entry.files.map(file => `<li>${esc(file)}</li>`).join('') : '';
  return `<article class="team-row"><div class="team-actor"><h3>${esc(entry.actor)}</h3><small>${esc(entry.role || 'Rolle offen')}</small></div>
    <div class="team-task"><strong>${esc(entry.task || 'Kein Auftrag dokumentiert')}</strong>
    <dl><dt>Ordner</dt><dd>${esc(entry.folder || 'Kein Ordner gemeldet')}</dd><dt>Dateien</dt><dd>${files ? '<ul>'+files+'</ul>' : 'Keine Schreibmeldung'}</dd>
    <dt>${state==='BLOCKED'?'Klärung':'Nächster Schritt'}</dt><dd>${esc(entry.next || 'Offen')}</dd></dl></div>
    <div class="team-state"><span class="team-pill" data-state="${state}">${esc(label)}</span><small>${teamTimestamp(entry.observedAt)}</small>${teamSourceLink(entry.source)}</div></article>`;
}
function paintTeam() {
  const list = document.querySelector('#team-list');
  if (!list) return;
  const now = Date.now();
  const filter = document.querySelector('#team-filter').value;
  document.querySelector('#team-source').textContent = team.handle ? 'Lokale Datei · '+team.handle.name : 'Gespeicherter Stand bei Veröffentlichung · laufender Drive-Stand über die verlinkte Datei';
  document.querySelector('#team-default').hidden = !team.handle;
  const time = team.checked ? teamTimestamp(team.checked) : 'ausstehend';
  const asOf = team.snapshot ? teamTimestamp(team.snapshot.asOf) : 'ausstehend';
  document.querySelector('#team-check').textContent = 'Datenstand '+asOf+' · Letzter Abruf '+time+' · Intervall 10 s · Aktivmeldung gültig für 30 s · Zeit in Wien';
  const warning = document.querySelector('#team-problem');
  warning.hidden = !team.problem;
  warning.textContent = team.problem;
  const rows = (team.snapshot?.entries || []).map(entry => ({entry,state:teamStatus(entry,now,!!team.problem)}))
    .filter(({state}) => filter==='all' || filter===state);
  const signature = JSON.stringify([rows,!!team.snapshot,team.problem]);
  if (signature === team.signature) return;
  team.signature = signature;
  list.innerHTML = rows.map(({entry,state})=>teamRow(entry,state)).join('') ||
    `<p class="mon-foot">${team.snapshot?'Keine passenden Meldungen.':team.problem?'Kein verifizierter Datenstand verfügbar.':'Meldungen werden abgerufen …'}</p>`;
}
async function readTeam() {
  if (team.busy || !document.querySelector('#team-list')) return;
  team.busy = true;
  const epoch = team.epoch;
  try {
    let raw;
    if (team.handle) raw = JSON.parse(await (await team.handle.getFile()).text());
    else {
      const response = await fetch('team-status.json', {cache:'no-store',signal:AbortSignal.timeout(8000)});
      if (!response.ok) throw new Error('Statusdatei nicht erreichbar.');
      raw = await response.json();
    }
    if (epoch !== team.epoch) return;
    team.snapshot = validateTeamSnapshot(raw);
    team.checked = new Date().toISOString();
    team.problem = '';
  } catch {
    if (epoch !== team.epoch) return;
    team.problem = 'Abruf fehlgeschlagen oder Daten unlesbar.' + (team.snapshot ? ' Angezeigt wird der letzte erfolgreiche Abruf.' : '');
  } finally {
    if (epoch === team.epoch) {team.busy=false;paintTeam();}
  }
}
function stopTeamPanel() {
  clearInterval(team.timer); clearInterval(team.clock);
  team.epoch++; team.busy=false; team.signature='';
}
function setTeamSource(handle) {
  team.epoch++; team.busy=false; team.handle=handle; team.snapshot=null; team.checked=null; team.problem=''; team.signature='';
  paintTeam(); void readTeam();
}
function startTeamPanel() {
  stopTeamPanel();
  document.querySelector('#team-filter').addEventListener('change',paintTeam);
  document.querySelector('#team-now').addEventListener('click',readTeam);
  document.querySelector('#team-default').addEventListener('click',()=>setTeamSource(null));
  document.querySelector('#team-connect')?.addEventListener('click',async()=>{
    try {
      const [handle] = await window.showOpenFilePicker({multiple:false,types:[{description:'NEXUS-Status',accept:{'application/json':['.json']}}]});
      setTeamSource(handle);
    } catch (error) { if (error.name!=='AbortError') {team.problem='Lokale Dateiauswahl nicht verfügbar.';paintTeam();} }
  });
  paintTeam(); void readTeam();
  team.timer=setInterval(readTeam,10000); team.clock=setInterval(paintTeam,1000);
}
