'use strict';

let state = { data: null, view: 'overview', team: null, timer: null, checked: null, error: '' };
const app = document.querySelector('#app');
const names = {
  overview: 'Übersicht', orders: 'Work Orders', p205: 'P205 · FT-Träger',
  l1: 'Eibengasse · L1', ebi: 'Eibengasse · I', system: 'Systemprüfung',
  jobs: 'Chats & Computer-Use', roles: 'Rollen & Capabilities',
  governance: 'Steuerdateien & Pfade', reports: 'Reports & Nachweise', registry: 'NEXUS-Registry', live: 'Live-Meldungen'
};
const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[char]));
const stateLabel = {
  GREEN: 'Grün · belegt', YELLOW: 'Gelb · wartet', RED: 'Rot · Problem',
  ACTIVE: 'Aktiv', PENDING: 'Wartet', UNKNOWN: 'Unbekannt', AVAILABLE: 'Verfügbar',
  UNASSIGNED: 'Nicht zugeteilt', OWNER: 'Freigabeinstanz'
};
const badge = value => `<span class="badge ${esc(String(value).toLowerCase())}">${esc(stateLabel[value] || value)}</span>`;
const link = (url, label) => `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>`;
const project = id => state.data.projects.find(item => item.id === id);
const localTime = value => {
  const date = new Date(value);
  if (!Number.isFinite(date.getTime())) return 'Zeit offen';
  return new Intl.DateTimeFormat('de-AT', {
    timeZone: state.data?.timezone || 'Europe/Vienna', day: '2-digit', month: '2-digit',
    year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit'
  }).format(date);
};

function heading(title, description, tone = '') {
  return `<div class="page-heading ${tone}"><div><span class="eyebrow">NEXUS / AEC ENGINEERING CONTROL</span>
    <h1>${esc(title)}</h1><p>${esc(description)}</p></div>
    <div class="snapshot"><i></i>Datenstand ${localTime(state.data.asOf)} · Wien</div></div>`;
}

function statusPolicy() {
  const p = state.data.policy;
  return `<section class="policy"><div>${badge('GREEN')}<p>${esc(p.green)}</p></div>
    <div>${badge('YELLOW')}<p>${esc(p.yellow)}</p></div>
    <div>${badge('RED')}<p>${esc(p.red)}</p></div></section>`;
}

function metricCards() {
  const orders = state.data.orders;
  const count = color => orders.filter(item => item[6] === color).length;
  const running = orders.filter(row => row[6] === 'YELLOW' && ['RUN','RUNNING','ACTIVE'].includes(row[7])).length;
  const percent = n => new Intl.NumberFormat('de-AT', {style:'percent', maximumFractionDigits:2}).format(orders.length ? n / orders.length : 0);
  const mix = [[running,'RUN'],[count('YELLOW')-running,'Pending'],[count('RED'),'Problem'],[count('GREEN'),'Fertig']]
    .map(([n,label]) => percent(n) + ' ' + label).join(' · ');
  const keywords = {'P205-R02':'Excel-Neuberechnung','P205-R10':'ID01-Freigabe','L1-P5':'Durchstanzen BT2C'};
  const problems = orders.filter(row => row[6] === 'RED').map(row => esc(keywords[row[0]] || row[3])).join(' · ');
  return `<section class="metrics">
    <article><small>WORK ORDERS</small><strong>${orders.length}</strong><span>${mix}</span></article>
    <article><small>ROT · STOP/PROBLEM</small><strong class="red-text">${count('RED')}</strong><span>${problems || 'Keine offenen Blocker'}</span></article>
    <article><small>GELB · WARTET</small><strong class="yellow-text">${count('YELLOW')}</strong><span>Quelle, ACK oder Gate offen</span></article>
    <article><small>GRÜN · ERLEDIGT</small><strong class="green-text">${count('GREEN')}</strong><span>Akzeptanznachweis vorhanden</span></article>
  </section>`;
}

function projectCard(item) {
  const open = state.data.orders.filter(order => order[2] === item.id && order[6] !== 'GREEN').length;
  return `<a class="project-card ${item.state.toLowerCase()}" href="#${item.id}">
    <div><span class="project-id">${esc(item.id.toUpperCase())}</span>${badge(item.state)}</div>
    <h2>${esc(item.title)}</h2><p>${esc(item.summary)}</p>
    <footer><span>${open} offene/gesperrte Aufträge</span><b>${esc(item.release)} →</b></footer></a>`;
}

function compactOrders(limit = 6) {
  const rank = { RED: 0, YELLOW: 1, GREEN: 2 };
  return [...state.data.orders].sort((a, b) => rank[a[6]] - rank[b[6]]).slice(0, limit).map(order => `
    <tr><td><b>${esc(order[0])}</b><small>${esc(order[1])}</small></td><td>${esc(project(order[2])?.title || order[2])}</td>
    <td>${badge(order[6])}</td><td>${esc(order[4])} → ${esc(order[5])}</td><td><span class="ack">${esc(order[7])}</span></td></tr>`).join('');
}

function overview() {
  const green = state.data.projects.filter(item => item.state === 'GREEN').length;
  const yellow = state.data.projects.filter(item => item.state === 'YELLOW').length;
  const red = state.data.projects.filter(item => item.state === 'RED').length;
  return heading('Kontrollpanel', 'Projektsteuerung, Work Orders, Systemzustand und auditfähige Nachweise.') +
    orderEvidenceView() +
    `<section class="alert"><div><strong>Projektstand im veröffentlichten Bericht: technische Freigaben bleiben fail-closed</strong>
    <p>${red} rote, ${yellow} gelbe und ${green} grüne Projekt-/Betriebsbereiche. Ampelfarbe ist kein Ersatz für ID01-Freigabe.</p></div>
    ${badge(red ? 'RED' : yellow ? 'YELLOW' : 'GREEN')}</section>` +
    metricCards() +
    `<section class="project-grid">${state.data.projects.map(projectCard).join('')}</section>
    <section class="panel"><div class="panel-head"><div><h2>Priorisierte Work Orders</h2><p>Rot zuerst; kein ACK wird nicht als aktive Arbeit dargestellt.</p></div><a href="#orders">Alle öffnen →</a></div>
    <div class="table-wrap"><table><thead><tr><th>ID / Prio</th><th>Projekt</th><th>Status</th><th>Ersteller → Bearbeiter</th><th>ACK</th></tr></thead>
    <tbody>${compactOrders()}</tbody></table></div></section>` + statusPolicy();
}

function ordersView() {
  return heading('Work Orders', 'Nachverfolgung mit Ampel, Auftraggeber, Bearbeiter, ACK, Blocker und nächster Aktion.') +
    `<section class="panel"><div class="filters"><input id="orderSearch" type="search" placeholder="ID, Projekt, Aufgabe oder Rolle suchen …">
    <select id="orderState"><option value="ALL">Alle Ampeln</option><option>RED</option><option>YELLOW</option><option>GREEN</option></select>
    <select id="orderProject"><option value="ALL">Alle Projekte</option>${state.data.projects.map(p => `<option value="${p.id}">${esc(p.title)}</option>`).join('')}</select></div>
    <div class="table-wrap"><table class="orders"><thead><tr><th>ID / Prio</th><th>Auftrag</th><th>Projekt</th><th>Ampel</th><th>Ersteller</th><th>Bearbeiter</th><th>ACK</th><th>Nächste Aktion / Gate</th></tr></thead>
    <tbody id="orderRows"></tbody></table></div><div class="table-foot" id="orderFoot"></div></section>` + statusPolicy();
}

function renderOrderRows() {
  const target = document.querySelector('#orderRows');
  if (!target) return;
  const query = document.querySelector('#orderSearch').value.toLowerCase().trim();
  const color = document.querySelector('#orderState').value;
  const projectId = document.querySelector('#orderProject').value;
  const rows = state.data.orders.filter(order => {
    const haystack = order.join(' ').toLowerCase();
    return (!query || haystack.includes(query)) && (color === 'ALL' || order[6] === color)
      && (projectId === 'ALL' || order[2] === projectId);
  });
  target.innerHTML = rows.map(order => `<tr><td><b>${esc(order[0])}</b><small>${esc(order[1])}</small></td>
    <td>${esc(order[3])}</td><td>${esc(project(order[2])?.title || order[2])}</td><td>${badge(order[6])}</td>
    <td>${esc(order[4])}</td><td>${esc(order[5])}</td><td><span class="ack">${esc(order[7])}</span></td><td>${esc(order[8])}</td></tr>`).join('');
  document.querySelector('#orderFoot').textContent = `${rows.length} von ${state.data.orders.length} Aufträgen`;
}

function projectView(id) {
  const item = project(id);
  const orders = state.data.orders.filter(order => order[2] === id);
  return heading(item.title, item.subtitle, item.state.toLowerCase()) +
    `<section class="project-hero"><div><span>STATUS / RELEASE</span><h2>${badge(item.state)} <b>${esc(item.release)}</b></h2>
    <p>${esc(item.summary)}</p></div><dl><dt>Owner</dt><dd>${esc(item.owner)}</dd><dt>Lead</dt><dd>${esc(item.lead)}</dd>
    <dt>Offene Aufträge</dt><dd>${orders.filter(order => order[6] !== 'GREEN').length}</dd></dl></section>
    <div class="two-col"><section class="panel"><div class="panel-head"><h2>Quellengebundene Befunde</h2></div><ul class="findings">${item.facts.map(fact => `<li>${esc(fact)}</li>`).join('')}</ul></section>
    <section class="panel"><div class="panel-head"><h2>Quellen</h2></div><div class="source-list">${item.sources.map(source => `<div>${link(source[1], source[0])}</div>`).join('')}</div></section></div>
    <section class="panel"><div class="panel-head"><h2>Freigabe-Gates</h2><span>${item.gates.length} Prüfpfade</span></div>
    <div class="gate-list">${item.gates.map(gate => `<article><b>${esc(gate[0])}</b><div><strong>${esc(gate[1])}</strong><p>${esc(gate[3])}</p></div>${badge(gate[2])}</article>`).join('')}</div></section>
    <section class="panel"><div class="panel-head"><h2>Work Orders</h2><a href="#orders">Gesamtregister →</a></div>
    <div class="table-wrap"><table><thead><tr><th>ID</th><th>Auftrag</th><th>Status</th><th>Bearbeiter</th><th>ACK</th><th>Gate</th></tr></thead><tbody>
    ${orders.map(order => `<tr><td><b>${esc(order[0])}</b></td><td>${esc(order[3])}</td><td>${badge(order[6])}</td><td>${esc(order[5])}</td><td><span class="ack">${esc(order[7])}</span></td><td>${esc(order[8])}</td></tr>`).join('')}
    </tbody></table></div></section>` + statusPolicy();
}

function systemView() {
  const moe = state.data.moe;
  return heading('Systemprüfung + Architektur-Matrix', 'Daten, Programme, Monitoring und Multi-Agent-Workflow – Befund, Risiko und Gate getrennt.') +
    `<section class="panel"><div class="panel-head"><div><h2>Kritisches Architektur-Audit</h2><p>Cloud-Stream und lokale Schreibzentrale werden logisch und betrieblich getrennt.</p></div>${badge('YELLOW')}</div>
    <div class="table-wrap"><table class="matrix"><thead><tr><th>Prüfbereich</th><th>Befund aus dem Verlauf</th><th>Kritische Bewertung & Risiko</th><th>Korrekturmaßnahme (Gate)</th></tr></thead><tbody>
    ${state.data.architecture.map(row => `<tr><td><strong>${esc(row[0])}</strong>${badge(row[2])}</td><td>${esc(row[1])}</td><td>${esc(row[3])}</td><td>${esc(row[4])}</td></tr>`).join('')}
    </tbody></table></div></section>
    <section class="rule-card"><span>BETRIEBSREGEL</span><p>Drive-Projektdaten sind standardmäßig Input. Die aktive SQLite-Datei und temporäre Rechenartefakte liegen auf einer echten lokalen Platte; nach geschlossenem Writer werden konsistente, gehashte Snapshots exportiert.</p></section>
    <div class="two-col"><section class="panel"><div class="panel-head"><div><h2>MoE Router</h2><p>Expertenzuordnung, keine Mehrheitsentscheidung.</p></div></div>
    <div class="table-wrap"><table><thead><tr><th>Modul</th><th>Aufgabe</th><th>Primärrolle</th><th>Kontrolle</th></tr></thead><tbody>
    ${moe.routes.map(row => `<tr><td><b>${esc(row[0])}</b></td><td>${esc(row[1])}</td><td>${esc(row[2])}</td><td>${esc(row[3])}</td></tr>`).join('')}</tbody></table></div></section>
    <section class="panel"><div class="panel-head"><div><h2>Signal Energy</h2><p>${esc(moe.formula)} ${esc(moe.bands)}</p></div></div>
    <div class="table-wrap"><table><thead><tr><th>Signal</th><th>C/U/D/X</th><th>E</th><th>Route</th><th>Gate</th></tr></thead><tbody>
    ${moe.signals.map(row => `<tr><td><b>${esc(row[0])}</b><small>${esc(row[1])}</small></td><td>${esc(row[2])}</td><td><strong>${row[3]} · ${esc(row[4])}</strong></td><td>${esc(row[5])}</td><td>${badge(row[6] === 'STOP' ? 'RED' : 'YELLOW')}</td></tr>`).join('')}</tbody></table></div></section></div>
    <section class="notice"><b>Grenze:</b> Ein Energy-Score priorisiert nur. Er ersetzt weder Fachsoftware noch unabhängigen Readback noch ID01-Freigabe.</section>`;
}

function rolesView() {
  return heading('Rollen & Capabilities', 'LLM-Name, Rollen-ID, Aufgabe, Grenze und tatsächlich beobachteter Status.') +
    `<section class="panel"><div class="table-wrap"><table><thead><tr><th>ID</th><th>Actor / Modell</th><th>Capability</th><th>Grenze / nächstes Gate</th><th>Status</th></tr></thead><tbody>
    ${state.data.roles.map(role => `<tr><td><b>${esc(role[0])}</b></td><td>${esc(role[1])}</td><td>${esc(role[2])}</td><td>${esc(role[3])}</td><td>${badge(role[4])}</td></tr>`).join('')}
    </tbody></table></div></section><section class="notice"><b>ACK-Regel:</b> Eine Modellbezeichnung oder Auftragszeile beweist keine Annahme. ACTIVE erfordert eine signierte Meldung ≤30 s; der lokale Watchdog darf nur PROCESS_ALIVE melden.</section>`;
}

function jobsView() {
  return heading('Chats, Tasks & Computer-Use', 'Fachliche Chat-Aufträge und ausführende Rechnerjobs werden getrennt bewertet.') +
    `<div class="two-col"><section class="panel"><div class="panel-head"><div><h2>Chats & Tasks</h2><p>Ergebnisstatus des Auftrags, nicht bloß Aktivität.</p></div></div>
    <div class="job-list">${state.data.chatTasks.map(row => `<article><div><b>${esc(row[0])}</b><small>${esc(row[2])}</small></div>
    <div><strong>${esc(row[1])}</strong><p>${esc(row[4])}</p></div>${badge(row[3])}</article>`).join('')}</div></section>
    <section class="panel"><div class="panel-head"><div><h2>Computer-Use Jobs</h2><p>Host/Engine, Aktion, Receipt und Owner separat.</p></div></div>
    <div class="job-list">${state.data.computerJobs.map(row => `<article><div><b>${esc(row[0])}</b><small>${esc(row[1])}</small></div>
    <div><strong>${esc(row[2])}</strong><p><span class="ack">${esc(row[4])}</span> · ${esc(row[5])}</p></div>${badge(row[3])}</article>`).join('')}</div></section></div>
    <section class="notice"><b>Trennregel:</b> Ein LLM-Task darf Quellen klassifizieren und einen Lauf spezifizieren. Nur die ausgewiesene lokale Engine darf Excel/RFEM/Python-Berechnungen ausführen; ein Receipt ist noch keine technische Freigabe.</section>`;
}

function governanceView() {
  const groups = [...new Set(state.data.navigation.map(row => row[0]))];
  return heading('Steuerdateien, Ordner & Kommunikation', 'Verifizierte Webziele werden geöffnet; lokale Pfade werden kopiert und müssen am Windows-Rechner aufgelöst werden.') +
    `<section class="nav-grid">${groups.map(group => `<article><h2>${esc(group)}</h2>
    ${state.data.navigation.filter(row => row[0] === group).map(row => row[4] === 'PATH'
      ? `<div class="nav-item"><div><strong>${esc(row[1])}</strong><p>${esc(row[2])}</p><code>${esc(row[3])}</code></div><button class="btn copy-path" data-copy="${esc(row[3])}">Pfad kopieren</button></div>`
      : `<div class="nav-item"><div><strong>${esc(row[1])}</strong><p>${esc(row[2])}</p></div>${link(row[3], row[4])}</div>`).join('')}
    </article>`).join('')}</section>
    <section class="notice"><b>Browsergrenze:</b> Die gehostete Site öffnet absichtlich keine <code>file://</code>-Ziele. Vor lokaler Ausführung: Pfad, Mount, Schreibmodus, Git-Commit und Script-Hash prüfen.</section>`;
}

function reportsView() {
  return heading('Reports & Nachweise', 'Verlinkte Berichte, Datenbanken, Statusfeeds und GitHub-Receipts.') +
    `<section class="report-grid">${state.data.reports.map(report => `<article><span>${esc(report[1])}</span><h2>${esc(report[0])}</h2>${link(report[2], 'Öffnen')}</article>`).join('')}</section>
    <section class="panel"><div class="panel-head"><h2>Integritätsangaben</h2></div><dl class="integrity">
    <dt>P205 Audit-DB SHA-256</dt><dd><code>5b8d1bd3d919acfe790362a23c7d4ac27f49acb944bf4334e40812f5bd5710f6</code></dd>
    <dt>SQLite-Prüfung</dt><dd>integrity_check = ok · 0 Foreign-Key-Verletzungen</dd>
    <dt>GitHub PR</dt><dd>#116 · ${esc(state.data.reports.find(row => row[0] === 'GitHub PR #116')?.[1] || 'Unbekannt')} · Quelle: veröffentlichter GitHub-Abgleich</dd>
    </dl></section>`;
}

// Generated by tools/build_control_data.py (schema 4.2.0): workflows, skills, ID ledger, monitor snapshot.
function registryTable(head, rows) {
  return `<div class="table-wrap"><table><thead><tr>${head.map(h => `<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>
    ${rows.map(row => `<tr>${row.map((cell, i) => `<td>${i === 0 ? '<b>' + esc(cell) + '</b>' : esc(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}
function registryView() {
  const n = state.data.nexus;
  if (!n) return heading('NEXUS-Registry', 'Keine generierten Registry-Daten (schemaVersion 4.1.0, manuell gepflegt).', 'YELLOW');
  const m = n.monitor, l = n.ledger, s = n.skills, w = n.workflows, r = n.reportFiles;
  const monitorTone = m.status === 'PASS' ? 'GREEN' : (m.status === 'ATTENTION' ? 'RED' : 'YELLOW');
  const checks = m.checks ? Object.entries(m.checks).map(([k, v]) => `${k}: ${v}`).join(' · ') : (m.detail || '');
  return heading('NEXUS-Registry', 'Aus dem Repository generiert · Commit ' + n.sourceCommit.slice(0, 12) + ' · keine Freigabe, nur Bestand.') +
    `<section class="panel"><div class="panel-head"><div><h2>Monitor-Snapshot</h2><p>${esc(checks)}</p></div>${badge(monitorTone)}</div>
      <p>Status <b>${esc(m.status)}</b>${m.observedAt ? ' · beobachtet ' + esc(localTime(m.observedAt)) + ' · Lauf #' + esc(m.runId) + ' · Knoten ' + esc(m.nodes) : ''}</p></section>
    <section class="panel"><div class="panel-head"><div><h2>Workflow-Registry v${esc(w.version)} · ${w.items.length} WF</h2><p>Pipeline: ${esc(w.pipeline.join(' → '))}</p></div></div>
      ${registryTable(['ID', 'Workflow', 'Route', 'Quelle'], w.items)}</section>
    <section class="panel"><div class="panel-head"><div><h2>Skills · ${s.items.length} Pakete</h2><p>${esc(Object.entries(s.counts).map(([k, v]) => k + ' ' + v).join(' · '))} · Prüfumfang: ${esc(s.scope)}</p></div></div>
      ${registryTable(['ID', 'Art', 'Status', 'Version', 'Pfad'], s.items)}</section>
    <section class="panel"><div class="panel-head"><div><h2>ID-Ledger · ${l.entries} Einträge</h2><p>Nächste freie ID ${esc(l.nextFreeId)} · letzter Eintrag ${esc(l.lastDate)} · ${esc(Object.entries(l.byValidity).map(([k, v]) => k + ' ' + v).join(' · '))}</p></div></div>
      ${registryTable(['ID', 'Datum', 'Typ', 'Titel', 'Akteur', 'Reife'], l.latest)}</section>
    ${r ? `<section class="panel"><div class="panel-head"><div><h2>Report-Dateien · ${r.entries}</h2><p>Regel ${esc(r.rule)} · ${esc(Object.entries(r.byState).map(([k, v]) => k + ' ' + v).join(' · '))}</p></div>${badge(r.byState.REGISTERED === r.entries ? 'GREEN' : 'YELLOW')}</div>
      ${registryTable(['Datei', 'Datum', 'Rolle', 'Ledger-Status', 'Pfad'], r.items)}</section>` : ''}
    ${n.surfaces ? `<section class="panel"><div class="panel-head"><div><h2>Oberflächen · ${n.surfaces.items.length} (Registry v${esc(n.surfaces.version)})</h2><p>${esc(n.surfaces.rule)} · ${esc(Object.entries(n.surfaces.byRole).map(([k, v]) => k + ' ' + v).join(' · '))}</p></div>${badge((n.surfaces.byRole.PROTOTYPE || 0) === 0 ? 'GREEN' : 'YELLOW')}</div>
      ${registryTable(['ID', 'Rolle', 'Titel', 'Owner', 'Status', 'Konsolidierungsziel', 'Pfad'], n.surfaces.items)}</section>` : ''}
    <section class="notice"><b>Quellen (SHA-256):</b> ${n.inputs.map(([p, h]) => esc(p) + ' ' + esc(h.slice(0, 12))).join(' · ')}</section>`;
}

function liveStatus(entry) {
  if (entry.state !== 'ACTIVE') return entry.state;
  const age = Date.now() - Date.parse(entry.observedAt);
  return age >= 0 && age <= 30000 ? 'ACTIVE' : 'STALE';
}

function liveView() {
  return heading('Live-Meldungen', '10-s-Abruf des veröffentlichten Status-Snapshots; Aktivmeldung verfällt nach 30 s.') +
    `<section class="panel"><div class="panel-head"><div><h2>Statusquelle</h2><p id="liveMeta">Abruf läuft …</p></div><div class="actions">
    ${link(state.data.links.teamFeed, 'Drive-Feed')}<button class="btn" id="liveRefresh">Jetzt abrufen</button></div></div>
    <p id="liveError" class="warn" hidden></p><div id="liveRows" class="live-rows"></div></section>
    <section class="notice"><b>Interpretation:</b> Die Site kann keinen Agenten zu 10-s-Meldungen zwingen. Ohne neuen Agenten-ACK wird ACTIVE nach 30 s als STALE dargestellt; der veröffentlichte Snapshot selbst kann älter sein.</section>`;
}

function paintLive() {
  const target = document.querySelector('#liveRows');
  if (!target) return;
  const meta = document.querySelector('#liveMeta');
  meta.textContent = state.team ? `Datenstand ${localTime(state.team.asOf)} · letzter Abruf ${localTime(state.checked)}` : 'Noch kein gültiger Snapshot.';
  const warning = document.querySelector('#liveError');
  warning.hidden = !state.error;
  warning.textContent = state.error;
  target.innerHTML = (state.team?.entries || []).map(entry => {
    const status = liveStatus(entry);
    const tone = status === 'COMPLETE' || status === 'REPORTED' ? 'GREEN'
      : status === 'BLOCKED' ? 'RED' : 'YELLOW';
    return `<article><div><h3>${esc(entry.actor)}</h3><small>${esc(entry.role || 'Rolle offen')}</small></div>
      <div><strong>${esc(entry.task || 'Kein Auftrag')}</strong><p>${esc(entry.folder || 'Kein Ordner')}</p>
      <p>${esc(entry.next || 'Nächster Schritt offen')}</p></div><div>${badge(tone)}<small>${esc(status)} · ${localTime(entry.observedAt)}</small></div></article>`;
  }).join('') || '<p class="empty">Keine Meldungen verfügbar.</p>';
}

async function fetchLive() {
  try {
    const response = await fetch('team-status.json', { cache: 'no-store', signal: AbortSignal.timeout(8000) });
    if (!response.ok) throw new Error('HTTP ' + response.status);
    const raw = await response.json();
    if (!raw || !Array.isArray(raw.entries) || !Number.isFinite(Date.parse(raw.asOf))) throw new Error('Schema ungültig');
    state.team = raw; state.checked = new Date().toISOString(); state.error = '';
  } catch (error) {
    state.error = 'Abruf fehlgeschlagen; letzter gültiger Snapshot bleibt sichtbar.';
  }
  paintLive();
}

function render() {
  clearInterval(state.timer);
  const requested = location.hash.slice(1) || 'overview';
  state.view = Object.hasOwn(names, requested) ? requested : 'overview';
  document.querySelector('#crumb').textContent = names[state.view];
  document.querySelectorAll('nav a').forEach(item => item.classList.toggle('active', item.dataset.view === state.view));
  if (state.view === 'overview') app.innerHTML = overview();
  else if (state.view === 'orders') app.innerHTML = ordersView();
  else if (['p205', 'l1', 'ebi'].includes(state.view)) app.innerHTML = projectView(state.view);
  else if (state.view === 'system') app.innerHTML = systemView();
  else if (state.view === 'jobs') app.innerHTML = jobsView();
  else if (state.view === 'roles') app.innerHTML = rolesView();
  else if (state.view === 'governance') app.innerHTML = governanceView();
  else if (state.view === 'reports') app.innerHTML = reportsView();
  else if (state.view === 'registry') app.innerHTML = registryView();
  else if (state.view === 'live') {
    app.innerHTML = liveView(); void fetchLive(); state.timer = setInterval(fetchLive, 10000);
    document.querySelector('#liveRefresh').addEventListener('click', fetchLive);
  }
  if (state.view === 'orders') {
    ['orderSearch', 'orderState', 'orderProject'].forEach(id => document.querySelector('#' + id).addEventListener(id === 'orderSearch' ? 'input' : 'change', renderOrderRows));
    renderOrderRows();
  }
  document.querySelectorAll('.copy-path').forEach(button => button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      button.textContent = 'Kopiert';
      setTimeout(() => { button.textContent = 'Pfad kopieren'; }, 1400);
    } catch {
      button.textContent = 'Kopieren blockiert';
    }
  }));
}

let pendingRead = null;
function loadData() {
  if (pendingRead) return pendingRead;
  const button = document.querySelector('#refresh');
  const publication = document.querySelector('#publication');
  button.disabled = true;
  pendingRead = (async () => {
    try {
      const response = await fetch('control-data.json', {cache:'no-store', signal:AbortSignal.timeout(8000)});
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const bytes = await response.arrayBuffer();
      const raw = JSON.parse(new TextDecoder().decode(bytes));
      if (!['4.1.0', '4.2.0'].includes(raw.schemaVersion) || !Array.isArray(raw.projects) || !Array.isArray(raw.orders) || !Number.isFinite(Date.parse(raw.asOf))) throw new Error('Datenformat ungültig');
      const revision = await digestBytes(bytes);
      const hadData = Boolean(state.data);
      const changed = revision !== state.panelHash;
      state.panelRead = new Date().toISOString();
      state.panelHash = revision;
      if (changed) {
        state.data = raw;
        document.querySelector('#orderCount').textContent = raw.orders.length;
        render();
      } else {
        const proof = document.querySelector('.proof');
        if (proof) proof.outerHTML = orderEvidenceView();
      }
      const result = hadData ? (changed ? 'Neue Panelrevision' : 'Panelrevision unverändert') : 'Panelrevision geladen';
      publication.textContent = result + ' · Seitenabruf ' + localTime(state.panelRead) + ' · Datenstand ' + localTime(raw.asOf) + ' (Wien) · SHA-256 ' + revision.slice(0,12) + ' · Work-Order-Beleg separat im Datenpunkt';
      return result;
    } catch (error) {
      publication.textContent = 'Abruf fehlgeschlagen · ' + (state.panelRead ? 'letzter erfolgreicher Abruf ' + localTime(state.panelRead) : 'kein bestätigter Abruf');
      if (!state.data) app.innerHTML = '<section class="fatal"><h1>Kontrolldaten nicht verfügbar</h1><p>'+esc(error.message)+'</p></section>';
      return 'Abruf fehlgeschlagen';
    } finally { button.disabled = false; }
  })().finally(() => { pendingRead = null; });
  return pendingRead;
}

function downloadEvidence() {
  if (!state.data) return;
  const blob = new Blob([JSON.stringify(state.data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const anchor = Object.assign(document.createElement('a'), { href: url, download: 'NEXUS_CONTROL_PANEL_EVIDENCE.json' });
  anchor.click(); URL.revokeObjectURL(url);
}

window.addEventListener('hashchange', () => state.data && render());
document.querySelector('#refresh').addEventListener('click', async () => {
  const [result, connected] = await Promise.all([loadData(), refreshPoint()]);
  const toast = document.querySelector('#toast');
  toast.textContent = result + (connected ? ' · Datenpunkt gelesen' : ' · Datenpunktzugriff offen'); toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 1800);
});
document.addEventListener('keydown', event => {
  if (event.key.toLowerCase() === 'e' && (event.ctrlKey || event.metaKey)) {
    event.preventDefault(); downloadEvidence();
  }
});
void openReviewReceipt().then(() => Promise.all([loadData(), refreshPoint()]));
setInterval(() => { if (!document.hidden) void loadData(); }, 10000);
