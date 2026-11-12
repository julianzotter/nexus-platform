---
name: reuse-cot-workflow
description: Deterministisches Chain-of-Thought-Arbeitsprotokoll für ReUse / Baustoff-Kreislauf entlang der Phasen FIND→INVENTORY→TRACE→TEST→LCA/GWP→SCORE→RECERTIFY→REUSE, mit expliziten Reasoning- und Freigabe-Gates pro Phase. Use when the user wants a CoT workflow, reasoning protocol, or step-by-step ReUse/Materialpass pipeline for structural-element reuse.
---

Deterministisches Chain-of-Thought-Arbeitsprotokoll für die Wiederverwendung (ReUse) von Bauteilen / Baustoffströmen. Jede Phase erzwingt explizites Reasoning, eine Validierung und ein Gate, bevor die nächste Phase startet.

## When to use
- Der Nutzer fragt nach einem CoT-Workflow, Reasoning-Protokoll, Arbeitsprotokoll oder Schritt-für-Schritt-Pipeline für ReUse / Materialpass / Bauteil-Wiederverwendung.
- Ein neues Bauteil/Projekt (z. B. FT-Träger, Gusseisen, Hybriddecke) soll von Fund bis Wiederverwendung durchgeschleust werden.

## Architektur-Kontext (aus dem Master-Index)
Hierarchie: `L1 KB (RAG) → L2 Orchestrator → L3 PythonModule → L4 Rechenkern`.
Harte Gates (gelten in JEDER Phase):
- **Ohne Quelle keine Antwort** — jede Aussage braucht eine zitierbare Quelle (Norm/ETA/Prüfbericht/Projektdoku).
- **4-Augen-Prinzip** — ValidatorAgent + HumanVeto/FreigabeGate vor Phasenwechsel.
- **η ≤ 1.0** bei Nachweisen; Rekursion (Self-Refine) bei Abweichung > 10 %.
- **Compliance:** GDPR, ÖNORM, Eurocodes, OIB; vollständiger AuditTrail.

## Reasoning-Gate-Schema (pro Phase identisch anwenden)
Für jede Phase strukturiere die Antwort als:
1. **Ziel** — was diese Phase liefern muss.
2. **Inputs** — welche Daten/Quellen vorliegen (mit Verweis).
3. **CoT-Reasoning** — explizite Gedankenkette: Annahmen → Ableitung → Zwischenergebnis. Annahmen ohne Quelle als `⚠ UNGESICHERT` markieren.
4. **Validation** — ValidatorAgent-Check (Einheiten, Grenzwerte, η≤1.0, Plausibilität).
5. **Gate** — `PASS` nur wenn Validation grün UND Quelle vorhanden UND (falls kritisch) HumanVeto-Freigabe. Sonst `BLOCK` mit benannter offener Frage.
6. **Output** — strukturiertes Ergebnis (JSON/Excel/Materialpass-Feld) für die nächste Phase.

## Die 8 Phasen
**FIND** — Bauteil/Projekt identifizieren. Quelle: Drive/Gmail/Outlook-Treffer. Gate: eindeutige Bauteil-Referenz + Herkunftsnachweis vorhanden.
**INVENTORY** — Geometrie & Menge erfassen (IFC/BricsCAD → QTO, Holz/Beton/Stahl). Gate: QTO mit Toleranzprüfung, PlausibilitätsFlags gesetzt.
**TRACE** — Herkunft/Lebenslauf (Herkunftsstatik, EPCIS, DPP). Gate: lückenlose Provenienz; Bauteil-ID/GUID/QR definiert.
**TEST** — Material-/Tragfähigkeitsprüfung (Prüfbericht, ETA). Gate: η≤1.0 nachgewiesen, Prüfberichte priorisiert zitiert.
**LCA/GWP** — Ökobilanz/CO₂. Gate: GWP berechnet, Datengrundlage zitiert, Vergleich Neubau vs. ReUse.
**SCORE** — Eignungs-/Risiko-Score (SWOT, RED-FLAG, Safety-Serviceability-Durability). Gate: Score reproduzierbar, Schwellwerte dokumentiert.
**RECERTIFY** — Re-Zertifizierung/Freigabe (4-Augen, OIB/ÖNORM-Konformität). Gate: HumanVeto-Freigabe + AuditTrail-Eintrag.
**REUSE** — Wiedereinbau/Materialpass final. Gate: Materialpass vollständig, Downstream-Export (JSON/Excel) erzeugt.

## Self-Refine-Loop
Nach SCORE: wenn ein Gate `BLOCK` oder Abweichung > 10 %, springe rekursiv zur frühesten betroffenen Phase zurück (max. 3 Iterationen), protokolliere den Grund im AuditTrail, dann erneut vorwärts.

## Done when:
- Alle 8 Phasen mit dem 6-Punkte-Schema durchlaufen sind.
- Jedes Gate explizit `PASS`/`BLOCK` ausweist (kein implizites Überspringen).
- Offene `BLOCK`-Punkte als nummerierte Liste am Ende stehen.
- Der finale Materialpass-Output (Felder + Quelle je Feld) ausgegeben ist.
