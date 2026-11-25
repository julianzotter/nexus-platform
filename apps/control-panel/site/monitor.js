function monitoringHeading(title, description) {
  return `<div class="page-heading"><div><h1>${title}</h1><p>${description}</p></div><button class="btn" data-action="export">Evidenz exportieren</button></div>`;
}
function monitoring() {
  const m = data.monitoring;
  const receipts = m.receipts.map(([name,time,trigger,detail,id]) =>
    `<tr><th scope="row">${name}</th><td>${time} MEZ<br><small>${trigger}</small></td><td>${detail}</td><td>${ext(repo+'/actions/runs/'+id,'#'+id)}</td></tr>`).join('');
  const gates = m.gates.map(([id,name,status,detail]) =>
    `<details class="gate" data-status="${status}"><summary><span class="gate-id">${id}</span><strong>${name}</strong><span class="pill" data-tone="${status}">${status}</span></summary><p>${detail}</p></details>`).join('');
  return monitoringHeading('NEXUS Betriebsübersicht','Berichtsstand vom 20. November 2026 · Manuell zusammengestellte Momentaufnahme') +
    `<section class="monitor-summary"><div><small>Sync-Nachweis · 08:27 MEZ</small><h2>Ende-zu-Ende-Prüfung offen</h2><p>Der Drive-Poller scheiterte beim OAuth-Refresh. Im Gegenpfad stoppte die Zustellung bereits im Preflight.</p>${ext(m.sources.gates,'Critical-Gates-Bericht')}</div><div class="proof-count"><strong>0 / 3</strong><span>erfolgreiche Zeitplanläufe in Folge</span></div></section>
    <section class="panel mon"><div class="panel-header"><h2>Letzte im Bericht belegte Läufe</h2><span>20.11.2026</span></div><div class="table-wrap"><table><thead><tr><th>Pfad</th><th>Start / Auslöser</th><th>Befund</th><th>GitHub-Lauf</th></tr></thead><tbody>${receipts}</tbody></table></div></section>
    <section class="panel mon"><div class="panel-header"><h2>Critical Gates</h2><label>Anzeige <select id="gate-filter"><option>Alle</option><option>Abweichung</option><option>Ungeprüft</option><option>OK</option></select></label></div>${gates}<div class="mon-foot">${ext(m.sources.gates,'Befunde P1–P7 · 08:27 MEZ')} · ${ext(repo+'/issues/73','Auftrag #73')}</div></section>
    <section class="panel mon"><div class="panel-header"><h2>WORK-Watch</h2><span>08:39 MEZ</span></div><div class="mon-foot">14 Dateien im Änderungsfenster. Der Watch meldet keinen neu autorisierten Fachauftrag. Zwei Entwürfe gingen zur Einordnung ein. ${ext(m.sources.watch,'Watch-Bericht')}</div></section>
    <a class="btn" href="#roadmap">Arbeitspakete und Abnahmekriterien</a> <a class="btn" href="#overview">Laufarchiv vom 17. November</a>`;
}
function roadmap() {
  const m = data.monitoring;
  const items = m.packages.map(([id,title,work,criterion]) =>
    `<details class="gate"><summary><span class="gate-id">${id}</span><strong>${title}</strong></summary><p>${work}</p><p><b>Abnahmekriterium</b><br>${criterion}</p></details>`).join('');
  return monitoringHeading('Knowledge System','Implementierungsplan v0.1.0 · Vorschlag vom 20. November 2026, 08:56 MEZ') +
    `<section class="panel mon"><div class="panel-header"><h2>Arbeitspakete & Abnahme</h2><span>Planungsstand</span></div>${items}<div class="mon-foot">${ext(m.sources.plan,'Implementierungsplan · Abschnitt 5')}</div></section>`;
}
document.addEventListener('change', event => {
  if (event.target.id !== 'gate-filter') return;
  const filter = event.target.value;
  document.querySelectorAll('.gate[data-status]').forEach(row => {
    row.hidden = filter !== 'Alle' && row.dataset.status !== filter;
  });
});
