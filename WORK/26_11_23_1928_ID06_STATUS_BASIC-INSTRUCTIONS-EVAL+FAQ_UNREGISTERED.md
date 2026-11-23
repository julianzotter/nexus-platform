---
name: 26_11_23_1928_ID06_STATUS_BASIC-INSTRUCTIONS-EVAL+FAQ_UNREGISTERED
description: Statuszettel WO-BASELINE-EVAL und FAQ-Konsolidierung je ID-Rolle, Stand WORK 26_11_23_1928
version: v1.0
role: ID06
manifest_ref: "NEXUS-ROLES-v1.1 §4"
timestamp: "2026-11-23T19:28+01:00"
status: PARTIAL
tasks_erledigt: [ID06 T1-T4, ID03 T1a/T2/T3a/T6doc/T7read, FAQ ID05/ID06/ID03, Review ID06 durch ID03]
tasks_offen: [ID02/ID04/ID07/ID08 Läufe, T5-Golden-Case, lokales RAG T6, Ledger-Merge 0212-0236, v3.1 Freigabe, OAuth]
probleme: [OAuth GitHub->WORK failure, 3 FAQ-Fassungen + Scratch, 2 v3-Fassungen]
offene_fragen: [Capabilities-Ablage, Startbeleg, Ledger-Zuständigkeit ID03 vs ID06]
pruefstatus: Teilweise unabhängig geprüft (ID06 durch ID03)
links:
  faq_id03_review: gdrive:1w_IyHkyo07JJZf6Pp69h-Fh10FKAq6jE
  faq_id06_konsolidiert: gdrive:1VL58AlT3TXnMpUpC7pLgnCdcgc0yWiKj
  faq_id05: gdrive:1MRuCH59nfmfOue2wuSVGqr_4u7pGcl2q
  scratch_id01: gdrive:1dT_Q-yf3wzAyRwJF3uFBywUDbnGbisUV
---
| ID | Baseline-Stand | Unabhängig geprüft |
|---|---|---|
| ID02 | nicht dokumentiert | – |
| ID03 | T1a API-Commit PASS, T2 PASS, T3a API PASS, T3b Mount BLOCKED, T4 NOT_RUN, T5 BLOCKED, T6 nur Dokument PASS, T7 Lesen PASS | nur interner ChatGPT-Prüfer |
| ID04 | nicht dokumentiert | – |
| ID05 | Drive-API-Bytes VERIFIED; Uploader nicht authentifiziert (ID03); Mount FAIL | ID06, ID03 |
| ID06 | T1-T4 PASS, T5 gerechnet | ID03: Remote-Bytes gleich; lokaler Push und G:-Write ohne fremden Beleg |
| ID07 | kein Lauf; Rohausgabe archiviert | – |
| ID08 | nicht dokumentiert | – |

FAQ: Basis für v3.1 = ID03-Review (neuester, mit Prüfvertrag). Keine weitere FAQ-Fassung anlegen (REUSE-BEFORE-CREATE).
