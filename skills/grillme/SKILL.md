---
name: grillme
description: Falsifizierungs-Gate (Popper) fuer Arbeitsplaene im regelbasierten Eurocode-System. Vor Ausfuehrung laden, jede Frage binaer beantworten (JA/NEIN + Beleg). Danach lessonslearned.
version: 0.1
status: PROPOSED (Issue #148/#149, ID01-Entscheid 2026-11-27)
timestamp: 2026-11-27T01:10+01:00
rolle: CLA (Voice)
regel: ein NEIN = Plan nicht freigegeben; Beleg = Fundstelle (Norm §, Drive-ID, Issue)
---
## Grundlagen
G1 Fragestellung exakt gelesen, Auftrag = nur das Bestellte?
G2 Normausgabe + NA aus Normenregister, gleiche Generation?
G3 Fehlende Angaben als Annahme gekennzeichnet?
## Widerlegungsversuche
W1 Gibt es eine Ausnahme/Sonderregel, die das Ergebnis umdreht? Gesucht + geladen?
W2 Liegt die massgebende Fundstelle am Kontext-Anfang (nicht in der Mitte)?
W3 Gilt das Modell im Anwendungsbereich (Systemgrenzen, NKL, Lastdauer)?
## Mechanik
M1 Einheiten-Check durchgefuehrt?
M2 Gleichgewicht SigmaV=0, SigmaM=0 geprueft?
M3 Plausibilitaet: Groessenordnung, Delta zu Bestand/Referenz?
## Holzbau/HBV (falls zutreffend)
H1 gammaM, kmod, kdef, kh, ksys, NKL geprueft?
H2 HBV: gamma-Methode im Gueltigkeitsbereich bzw. Kerve diskret?
## Abschluss
A1 Rechnung durch deterministischen Solver, nicht durch LLM?
A2 Artefakt archiviert + Log + Statuszettel (3 Ebenen)?
