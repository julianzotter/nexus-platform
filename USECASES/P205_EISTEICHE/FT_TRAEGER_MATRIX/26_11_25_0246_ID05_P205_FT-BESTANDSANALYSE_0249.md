---
title: P205 FT-Traeger-Matrix - Bestandsanalyse Entwicklung, Tests, offene Tasks, Formellogik/Normkonformitaet
created: 2026-11-25T02:46 Europe/Vienna
author_runtime: Perplexity Computer (Claude Opus 5.5)
role_id: UNVERIFIED
artifact_number: LEDGER-PENDING
source_thread: https://www.perplexity.ai/computer/tasks/710939a9-6b3a-4982-9c75-c453cab52873
status: REPORT_ONLY
technical_release: false
human_acceptance: PENDING
---

# P205 FT-Traeger-Matrix - Bestandsanalyse

Grundlage: Repo `julianzotter/nexus-platform` (main, Stand 2026-11-25), Drive-Workbook `26_09_24_FT_Träger_Matrix_26.02_Vers-D_jz.xlsx` (Drive-ID 1Ldc8Q1zFfBCXNvaKqJp7c0i6qmf49sMe, SHA-256 3f9d64fa2135fa54fca99c34f1aca20c141a5257d9573e58264833f62fc4a795; laut Bericht 23.11. zellidentisch mit RevE), Vorversionen 26_08_20, 26_08_21, Linie A (kopie_DB).
Methode: read-only, openpyxl, gespeicherte Werte + Formeltext. Kein Excel-Rebuild. Alle Eta-Zahlen sind Screening auf Cache-Werten, kein Nachweis.

## 1. Kurzfazit

- Gesamtstatus: ROT. Kein Pilottraeger gerechnet, kein Rebuild, keine Freigabe.
- Formellogik: Grundstruktur EC2-konform (Gl. 6.8/6.9/6.13/6.14, nu1 nach 6.6N, Fuge nach 6.25 mit c/mu "rau"). Aber 4 sicherheitsrelevante Abweichungen (N1-N4), davon 3 neu.
- Architektur-Gate v0.1 (Resolver/Schema/Golden Case): nur als Entscheidungsprotokoll vorhanden, Code nicht im Repo (NICHT_IMPLEMENTIERT).
- Tests: Hilfswerkzeuge getestet (120 passed); Rechenkern/Workbook: 0 Golden Cases.

## 2. Entwicklungsschritte und Bewertung

| # | Schritt | Artefakt | Status | Qualitaet | Tests |
|---|---|---|---|---|---|
| E1 | Quelleninventar / Suchindex | SQLite 23.434 Dateien, Inventar 235 Workbooks (150 verschieden) | ERLEDIGT | gut (Hash-basiert) | Struktur-Check (PRAGMA) |
| E2 | Versionsvergleich Linie A/B, Vers-B..RevF | reports/2026-11-23_FT-Traeger-Matrix_SYNC/ | ERLEDIGT | gut, zellgenau | Zellvergleich 0 Abw. Vers-D/RevE |
| E3 | Fehleranalyse 288 Fehler | _Fehleranalyse_Datenluecken_Vers-D_jz.xlsx, Nachtrag 3 | ERLEDIGT | gut, 6 Ursachengruppen | keine (Analyse) |
| E4 | #REF!-Rekonstruktion 5 Formeln | P205_REF-Rekonstruktion_Vers-D_jz.md | VORSCHLAG | Musterbeleg 3.572/3.861 Zellen, Golden-Wert 37,310 kg reproduziert | Nachrechnung 1 Zelle |
| E5 | Peer Review v1.2 (F01-F12) | WORK/P205_FT/2026-11-23_ID02/ | ERLEDIGT | gut, evidenzklassifiziert | - |
| E6 | Native Excel-Recalc v1.2 | tools/windows/P205_FT_Excel_Native_Recalc_v1_2.ps1 | BLOCKIERT (RPC_E_CALL_REJECTED in Get-LinkSources) | solide Fehlercodes, fehlt COM-Retry | 4 statische Tests passed; kein Windows-Lauf |
| E7 | Fehler-Audit-Skript | tools/p205_error_audit.py | GELIEFERT | einfach, Grenzen dokumentiert | nur Dummy-Lauf |
| E8 | Dashboard v1.1 | USECASES/.../VersD-RevE_Dashboard_v1.1.html | ERLEDIGT | nur Anzeige | Browser 0 Skriptfehler |
| E9 | FT-CAD (DXF) | usecases/P205-EISTEICHE-BT-WEST/ft-cad-plan | PILOT | modular | 9 passed |
| E10 | AEC-Contracts (Ports/Adapters, 7 Schemas) | contracts/ | REFERENZ v0.1.0 | gut, keine Fachlogik | 96 passed (mit import-linter) |
| E11 | Bootstrap-Vertrag | tests/test_bootstrap_contract.py | ERLEDIGT | - | 8+3 passed |
| E12 | Architektur-Gate v0.1 (Katalog/Binding-Schema, Resolver, Allowlist, Golden Case, Freigabe) | nur reports/26_11_25_0010_...PROTOKOLL... | NICHT_IMPLEMENTIERT (Code verloren) | Konzept gut | 0 (damals 23 passed, nicht reproduzierbar) |
| E13 | EC2-Rechenkern / Pilottraeger | - | NICHT_GESTARTET (AP05-07) | - | 0 |
| E14 | Massen/LV/Plaene | - | NICHT_GESTARTET (AP08) | - | 0 |

## 3. Formellogik und Normkonformitaet (EN 1992-1-1 + B 1992-1-1)

### 3.1 Sicherheitsrelevante Befunde

| ID | Befund | Ort | Umfang | Wirkung | Korrektur |
|---|---|---|---|---|---|
| N1 | V,Ed = (abs(VL)+abs(VR))/2 statt Maximum; 2.598 Zellen nutzen MAX, 1.338 den Mittelwert | Zeile 33 aller Traegerblaetter | 691 belastete Spalten in 92 Blaettern | unsicher: mit MAX 39 Spalten eta>1,00, 28 >1,05 (z. B. 2OG-6 BB 0,87->1,37; 2OG-B AE 0,97->1,33) | einheitlich `=MAX(ABS(@22),ABS(@23))` |
| N2 | MRd-Katalog absolut referenziert (`MRd!$H`), Querschnitt passt nicht zum Traeger | Zeilen 64/70 | 137 von 2.386 belasteten Biegenachweisen: 100 mit Katalog hoeher als Traeger (unsicher), 37 niedriger (konservativ, z. B. EG-G Traeger 40/80, Katalog MRd!AK 40/77) | unsicher in 100 Faellen (vgl. G13 "56 Spalten") | BT-Typ je Spalte per INDEX/MATCH aus Zeile 17/16 |
| N3 | Fuge: fctd = fctm/gamma_c (0,35/1,5) statt fctk,0.05/gamma_c (EC2 3.1.6(2), Tab. 3.1: C40/50 fctk,0.05 = 2,5 MPa) | VRd_Det Zeile 129-131 | 264 von 300 Katalogspalten | v_Rdi bis -13,1 %; Schubfuge hat bereits 115 Stellen >1,05 | AE129 = 0,25 kN/cm2 (fctk,0.05) |
| N4 | Durchbruch unten: Hebel `@18/200` (h1 Vergussfuge) statt `@19/200` (b,d); oben korrekt `@19` | Zeile 184 und 231 (Layout 4OG) | 26 Durchbrueche | 4 Stellen dann >1,05: 4OG-2 X 1,25; 4OG-3 X 1,21; 4OG-3 U 1,19; 4OG-2 U 1,13 | `@18` -> `@19` |

### 3.2 Modell-/Konsistenzbefunde

| ID | Befund | Bewertung |
|---|---|---|
| N5 | Durchbruch: zwei Querkraftaufteilungen OG/UG (Zeile 174/175 Rechteck, Zeile 247/248 mit Aufbeton); 177 nimmt MAX, 182 nutzt 174, 230 nutzt 247 | inkonsistent, ein Modell festlegen |
| N6 | V,Rd,s = Buegel Traeger + Buegel Rost addiert (VRd_Det Z. 25); V,Rd,max als gewichtete Summe dreier Mechanismen (Z. 29-33) | kein EC2-Standardmodell; Verankerung beider Buegellagen in Druck- und Zugzone nachweisen oder V,Rd,max je Steg einzeln |
| N7 | theta = 35 Grad (cot 1,43), alpha = 90 | im EC2-Bereich; gegen ÖNORM B 1992-1-1 zu 6.2.3(2) pruefen (AT-NA regelt dort den Grenzwinkel, laut [SCIA NA-Uebersicht](https://help.scia.net/24.0/en/national_annexes/en1992/austria.htm?TocPath=Design%20and%20check%7CComposite%7CGreece%7CNational%20Annexes%20to%20EN%201992%7C%7CEN%201992-1-1%7C_____1)) |
| N8 | fcd = fck/1,5 (alpha_cc = 1,0), fyd = 550/1,15 | konform: AT nutzt EN-Empfehlung zu 3.1.6(1) ([SCIA](https://help.scia.net/24.0/en/national_annexes/en1992/austria.htm?TocPath=Design%20and%20check%7CComposite%7CGreece%7CNational%20Annexes%20to%20EN%201992%7C%7CEN%201992-1-1%7C_____1), [NÖ Planungsgrundlagen](https://www.noe.gv.at/noe/Ausschreibungen-Liegenschaften/NOe_Planungsgrundlagen_Teil_B2_Plattenfoermige_Stahlbetonfer.pdf): alpha_cc = 1,000); Design-Guide-Kopf nennt aber DIN/NA-D (G12) |
| N9 | Materialwerte hart in Formeln (40/1.5, 550/1.15, 26.7, 478.3) | Wartungsrisiko; zentrale Parameterzellen |
| N10 | M,Ed = MIN(Nachbar,eigen) / MAX(Nachbar,eigen) (Z. 65/71) | Absicht (gemeinsamer Schnitt?) durch ID01 bestaetigen |
| N11 | Kriterium 105 % | nicht normativ; EC2 verlangt eta <= 1,00 |
| N12 | "GESAMTAUSLASTUNG" Z. 252 = nur Durchbruch-Positionen, ohne V/M/Fuge | Bezeichnung irrefuehrend |
| N13 | z: Label "0,8*d", Formel 0,9*d (VRd_Det Z. 135) | Doku-Fehler, Wert EC2-zulaessig |

### 3.3 LV-/Massenbefunde

| ID | Befund | Wirkung |
|---|---|---|
| M1 | 5 #REF!-Formeln (2OG-3/2OG-4 BC110/114, 2OG-BC Z114) + Begleitfehler (BD-Querbezug, Eingabespalte BD, Z110 m3 statt kg) | GESAMT-Massen Uebersicht = #REF! |
| M2 | Spaltenversatz Durchbruch in EG-G, EG-B, 2OG-G, 3OG-2, 3OG-E (+RO-Kopien) | Masse beim Nachbartraeger, Betonabzug fehlt |
| M3 | Uebersicht O9/P9 = SUM(16:23), N9 = SUM(16:470) | Q9 [kg/m3] falsch; U9 korrekt |

### 3.4 Eta-Screening (Cache, belastete Nachweise)

| Gruppe | Zeile | n | >1,00 | >1,05 |
|---|---|---|---|---|
| Querkraft | 34 | 1.985 | 2 | 1 |
| Schubfuge | 57 | 1.918 | 148 | 115 |
| M- | 66 | 2.010 | 43 | 19 |
| M+ | 72 | 2.018 | 42 | 16 |

Deckt sich mit Peer Review F01 (19/15/1/115). Vor N1-N4-Korrektur und Rebuild nicht belastbar.

## 4. Fehleranalyse 288 (Status)

- 145 #DIV/0!, 109 #VALUE!, 34 #REF!; 170 Wurzeln in 6 Gruppen (Bericht 23.11., Nachtrag 3).
- Datenluecken: Kopierzeilen 37/42/47 = 0 (ca. 85 Wurzeln), `?`-Platzhalter (172 Zellen, ca. 48 Wurzeln), `--`-Division (14), leere Spalte BD 4OG-D/I (10), EG-3 AE (3), #REF! Uebersicht (13).
- #REF!: Rekonstruktion liegt vor (E4).

## 5. Offene Tasks (konsolidiert, priorisiert)

| Prio | Task | Wer | Abhaengigkeit |
|---|---|---|---|
| P0 | Recalc v1.2: COM-Retry (RPC_E_CALL_REJECTED) einbauen, RUN-01 auf Kopie | Perplexity/ID02 + ID01 Windows | - |
| P0 | N1-N4 + M1 auf Arbeitskopie korrigieren | ID01-Entscheid, dann Agent | Freigabe ID01 |
| P0 | E1.1-E1.4 entscheiden (Toleranz, alpha 4OG-2 AK, Lage 4OG-2 BD, I1-Top-4) | ID01 | - |
| P0 | RFEM-Schnittkraefte fuer 32 `?` (1OG-J/2OG-J, Eingabe_RFEM_765) | ID01 | RFEM-Ordner |
| P1 | Kopierzeilen 37/42/47 befuellen (81 Spalten) | Agent | N3-Fix |
| P1 | Pilottraeger 4OG-2 unabhaengig (Python) gegenrechnen = Golden Case | Agent | Rebuild |
| P1 | Normprofil AT festschreiben (cot theta, NDP-Liste) | ID01 | - |
| P1 | Architektur-Gate v0.1 neu implementieren + Tests ins Repo | Agent | - |
| P2 | M2/M3 Massenkorrektur, LV-Abgleich LG07/16/36 | Agent + ID01 | P1 |
| P2 | Exporter + SQLite 12.11. in WORK, RUNLOG.md, Ledger-/Rollen-ID | ID01 | - |
| P3 | Dashboard neu exportieren, DXF, Peer Review, ZT-Freigabe | alle | P2 |

## 6. Empfehlung

1. Rechenkern nicht weiter in Excel reparieren als noetig: Excel = Eingabe/Ausgabe; Pilot 4OG-2 als deterministischer Python-Solver mit Golden Case gegen Excel-Rebuild.
2. Reihenfolge: COM-Fix -> RUN-01 -> N1-N4/M1 -> Rebuild -> Golden Case 4OG-2 -> Rollout.
3. COM-Retry fuer v1.2 (Muster):

```powershell
function Invoke-ComRetry([scriptblock]$Call,[int]$Max=20){
  for($i=1;$i -le $Max;$i++){
    try { return & $Call }
    catch [System.Runtime.InteropServices.COMException] {
      if($_.Exception.HResult -ne -2147418111){ throw }   # 0x80010001 RPC_E_CALL_REJECTED
      Start-Sleep -Milliseconds (250*$i)
    }
  }
  throw 'E_COM_CALL_REJECTED_RETRY_EXHAUSTED'
}
# Aufruf: $links = Invoke-ComRetry { $Workbook.LinkSources(1) }
# Vorher: $Excel.DisplayAlerts=$false; $Excel.AskToUpdateLinks=$false; Workbooks.Open($p, 0) (UpdateLinks=0)
```

## 7. Tests (ausgefuehrt 2026-11-25)

| Suite | Ergebnis |
|---|---|
| tests/test_p205_excel_native_recalc_script.py | 4 passed (statisch, kein Windows) |
| tests/test_bootstrap_contract.py + test_context_bootstrap.py | 11 passed |
| ft-cad-plan/tests | 9 passed |
| contracts/ | 96 passed (7 failed ohne import-linter, Umgebungsabhaengigkeit) |
| Workbook / EC2-Kern | keine Tests, keine Golden Cases |
