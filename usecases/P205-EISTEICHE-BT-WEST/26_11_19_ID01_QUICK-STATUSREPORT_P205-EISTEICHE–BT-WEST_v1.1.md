# QUICK-STATUSREPORT — P205 Campus Eisteiche BIG (Statik BT West)

> **ID:** 26_11_19_ID01 · **Version:** v1.1 · **Datum:** 2026-11-19
> **Projekt:** An den Eisteichen, A-1120 Wien · **Bauteil:** WEST (Schule, Brücke, Trafo, Retentionsbecken, Baugrube, Baulogistik/Kran)
> **Rolle:** Statik / Tragwerksplanung (Zotter–Litschauer)

---

## 1 · Ziel
Baumeister-LV „An den Eisteichen“ (BT West) **gewerkeweise/Bauablauf in Pakete gliedern**, je Paket die
**Standard-Textblöcke aus dem LV extrahieren** und um **kostenrelevante „Besondere Herstellanweisungen seitens Statik“**
ergänzen (Geltung: LV vor Plan; Grundriss/Schnitt/Ansicht vor Detail) — als Arbeitsgrundlage für den
**Technischen Bericht zur Statik**. Zwischenschritt: **Suchindex** für Massen-LV + Ausschreibungs-Statikunterlagen.

## 2 · Was wurde erstellt
| Artefakt | Ort (Google Drive, Projektordner) |
|---|---|
| Strukturierte Analyse (LV-Prüfung LG 03/07/16/36) | `01_E-MAIL-IN\26_07_16_LV\EIS BAUMEISTER-LV 20260619_Analyse_Statik_BT-WEST.docx` |
| Statikbericht-Paketstruktur (11 Pakete, A/B/C-Blöcke) | `01_E-MAIL-IN\26_07_16_LV\EIS BAUMEISTER-LV 20260619_Statikbericht_Pakete_BT-WEST.docx` |
| SQLite-Suchindex (20.301 Dateien, FTS5) | `99_SUCHINDEX\suchindex.sqlite` |
| SUCHINDEX.md (Übersicht) | `99_SUCHINDEX\SUCHINDEX.md` |
| Statistik-JSON | `99_SUCHINDEX\suchindex_stats.json` |

## 3 · Was lokal gesichert ist
- **Google Drive (G:)** — dauerhaft: die 5 Artefakte oben.
- **Nur temporär** (`C:\Users\julia\AppData\Local\Temp\`): Extraktions-/Build-Skripte (`dsh_p205_*.py`),
  Zwischentexte (`p205_lv_text.txt`, `p205_og02_structure.txt`, …) — bei Temp-Bereinigung verloren.

## 4 · Statusreport im WORK-Ordner?
**Kein „WORK“-Ordner vorhanden** (dieser Report legt ihn an). Frühere Statusberichte liegen unter
`51_SEED-CONTEXT\` (`26_07_05_Statusbericht_EISTEICHE_CONTEXT_LIST.txt` [UTF-16], `…_LV-Beilagenliste_…pdf`,
`AUTOMATION\P205_STATUS.gdoc`, `AUTOMATION\09_LOGS\26_07_06_CLAUDE_STATUS-REPORT.md`) sowie `_DSH_ANALYSE\`.

## 5 · GitHub-Backup + Sync
**Status:** wird mit diesem Arbeitsschritt eingerichtet. Ziel-Repo: **`julianzotter/nexus-platform`** (NEXUS Platform Hub),
eigener Unterordner **`usecases/`** für den Usecase **P205-EISTEICHE-BT-WEST**.
- Git 2.42.0 · GitHub CLI (gh) 2.103.3 · Konto `julianzotter` (keyring), Token-Scopes: gist, read:org, repo, workflow.
- Kein lokales `.git`-Repository im Projektordner (kein bisheriges Backup).

## 6 · Workflow-Automatisierung
**Bestehender Ansatz** (aus früheren Sessions, noch nicht mit dieser Arbeit verbunden):
`51_SEED-CONTEXT\AUTOMATION\` → `blackboard.py` (Blackboard-Architektur, Hayes-Roth/Corkill, append-only JSONL +
SHA-256), `reconcile.py`, Register (`P205_SOURCE_REGISTRY.csv`, `PROJECT_REGISTER.csv`, `FINANCE_REGISTER.csv`,
`MAIL_SIGNAL_FILTER.csv`, `OUTPUT_MANIFEST.json`, `AGENT_ENVELOPES.json`), `P205_SSOT_DUPLICATE_RULE.md`.
**Verknüpfung mit der neuen SQLite-DB / Paket-Doku steht aus.**

## 7 · Arbeitsschritte & Status
| Schritt | Status |
|---|---|
| PDF-Extraktion (549 S., OG 02, 1.122 Positionen / 18 LG) | erledigt |
| Strukturanalyse + Prüfbericht (DOCX) | erledigt |
| Paketstruktur + Herstellanweisungen Statik (DOCX) | erledigt |
| Suchindex (SQLite + SUCHINDEX.md) | erledigt |
| Paketweise Vertiefung (volle Positionstexte + Mengen) | offen |
| Abgleich mit Statikbericht `EIS-ST-AS-WT-STATIKBERICHT-251127` | offen |
| Zuordnung Bekament-Schalungs-/Bewehrungspläne zu Paketen | offen |
| Integration in P205-Register/Blackboard + GitHub-Sync | in Arbeit |

## 8 · Datenbankmigration
`suchindex.sqlite` **frisch** angelegt (Tabellen `files`, `folders`, `files_fts` FTS5 + Indizes).
Überführung der bestehenden P205-Register (CSV/JSON) in SQLite **möglich, noch nicht erfolgt**.

## 9 · Workflow-Implementierung / Arbeitspakete
Blackboard-Pattern (`blackboard.py`) + Register vorhanden. Konkrete Implementierung der Anbindung
(SQLite ↔ Register ↔ Paket-Doku ↔ GitHub) **offen** — siehe „Nächste Schritte“.

## 10 · Google-Drive-Ablage-Orte
- Root: `G:\…\P205_Campus_Eisteiche_BIG`
- **Outputs**: `01_E-MAIL-IN\26_07_16_LV\` (DOCX) · `99_SUCHINDEX\` (DB/MD) · `WORK\` (dieser Report)
- **Quellen**: `06_BERICHTE` · `13_AUSSCHREIBUNG_LV-HB` · `30_HOLZHYBRID-LV-STRUKTUR` · `05_STATIK` ·
  `11_GEOTECHNIK` · `51_SEED-CONTEXT` · `01/02_E-MAIL-IN/OUT(_Bekament)` · `18_DSL3_Prüfstatik` · `17_ÖBA+IL3-Überwachung`

## 11 · Relevante GitHub-Repositories
- `julianzotter/nexus-platform` — NEXUS Platform Hub (Ziel für USECASES)
- `julianzotter/nexus-ai-operation-system` — NEXUS AI operating system
- `julianzotter/nexus-skills-factory` · `julianzotter/NEXUS-AI-ENGINEERING-APPS` · `julianzotter/NEXUS-AI-AEC-ENGINEERIN-KNOWLEDGE-GRAPH`

## 12 · Integration in SQLite-DB
Erledigt: Datei-Inventar + Kategorien + FTS5.
Offen: LV-Positionen, TWP-Planliste, Bekament-Planregister, Statikbericht-Referenzen, Merge der P205-Register.

## 13 · Zusätzlich nutzbare Quellen / Patterns / Scripts / Wissensdaten / Normen
- **Scripts/Patterns:** `51_SEED-CONTEXT\AUTOMATION\blackboard.py`, `reconcile.py`, `P205_SSOT_DUPLICATE_RULE.md`
- **Index/Register:** `51_SEED-CONTEXT\INDEXLISTEN+DASHBOARDS\MASTER_INDEX_P205.md` (Planlistenabgleich),
  `P205_REGISTRY.jsonl`, `REGISTRY_STORAGE_TOPOLOGY_P205.md`, `26_10_07_P205_Quelleninventar.csv`, Dashboards (HTML)
- **Prompts/Wissen:** `51_SEED-CONTEXT\AI-EISTEICHE-ABGABE_WORKSPACE-STUDIO\SYSTEM-MASTER-PROMPTS\`
- **Frühere DSH-Analysen:** `_DSH_ANALYSE\`
- **Normenbasis:** LB-HB **022 (2021-12)**; ÖNORM EN 1990/1991/1992/1995, EN 13670; ÖNORM B 3664 (FBV „Gelbe Wanne“),
  B 2204, B 2061, B 3692; EN 15497/14080 (Holz); Klassifizierung **CC3/RC2/DSL3/IL3, Prüfstatiker Ja, R90/REI90**

## 14 · Kritische Punkte & Problemlösungen
- **G: = Google Drive** → Sandbox-Schreibfreigabe schlägt fehl (`Win32 87`). Lösung: Lese-Tools normal, Schreiben über vollen Zugriff.
- **Kein Git/GitHub-Backup** (bis jetzt) → lokales Single-Point-of-Failure → wird mit diesem Schritt behoben.
- **Zwei parallele Indizes** (neu `99_SUCHINDEX\suchindex.sqlite` vs. alt `P205_REGISTRY.jsonl`/MASTER_INDEX) → SSOT-/Doppelpflege-Risiko.
- **Aus MASTER_INDEX:** „81 t Zusatzbewehrung“ historisch nicht neu freigegeben; Nachweislücken Schalung (16/20) / Bewehrung (21/44).
- Rauschen: 2.576 `desktop.ini` (bereits als „SONSTIGES“ gefiltert).

## 15 · Prüfung & Freigabe
- Strukturprüfung beider DOCX (`check_office.py`) = **pass**.
- Inhaltliche **Freigabe durch den Statiker** steht aus (insb. „B“-Herstellanweisungen und „C“-Reviewpunkte).
- Projektseitig gefordert: **DSL3-Prüfstatiker** + **IL3-Fremdüberwachung**.

## 16 · Nächste Schritte
1. GitHub-Backup/Sync einrichten (nexus-platform → `usecases/P205-EISTEICHE-BT-WEST`), Report + Artefakte pushen.
2. Indizes zusammenführen: SQLite als SSOT, alte Register (CSV/JSON) migrieren/integrieren.
3. Paketweise Vertiefung (Paket 2 Baugrube/Tiefgründung, Paket 3 UG/FBV) mit vollen Positionstexten + Mengen.
4. Abgleich mit `EIS-ST-AS-WT-STATIKBERICHT-251127`; Zuordnung der Bekament-Schalungs-/Bewehrungspläne zu Paketen.
5. Blackboard/Register-Anbindung an die neue SQLite-DB implementieren.

---

*Erstellt am 2026-11-19 · Quelle: strukturierte Textextraktion `AN DEN EISTEICHEN BAUMEISTER-LV 20260619.pdf` (549 S., OG 02).*
