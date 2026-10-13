---
title: "NEXUS-AI Kurz-Manual"
subtitle: "Die zwei Perplexity-Aufgaben"
date: "2026-10-13"
---

# NEXUS-AI Kurz-Manual: Die zwei Perplexity-Aufgaben

Stand: 2026-10-13. Grundlage: `orchestrator/README.md`, `orchestrator/config/routing.json`, `reports/2026-10-13_parsing-pipeline/NEXUS_PARSE_REPORT_v1.0.md`. Nicht mit echten API-Zugängen und nicht auf einem Anwender-Rechner getestet.

## 1. Zweck

Nexus bietet einen gemeinsamen Einstiegspunkt für mehrere KI-Modelle: Aufgabentyp und Anfrage angeben, Nexus wählt den vorgesehenen Anbieter, ruft ihn auf und gibt das Ergebnis zurück.

| Aufgabe | Was sie macht | In einem Satz |
|---|---|---|
| **1. Integrate Perplexity Into Nexus-AI** | Recherche-Anbindung | Nexus stellt Perplexity eine Frage und gibt Antwort und Quellen zurück |
| **2. Build Nexus-AI Multi-LLM System** | Multi-Modell-Steuerung | Nexus wählt je Aufgabentyp das passende Modell |

Die erste Aufgabe liefert den Perplexity-Baustein, die zweite die Steuerung, in der er eine Route unter mehreren ist.

## 2. Aufgabe 1: Perplexity-Anbindung

**Was sie tut**

- Eine Recherchefrage geht über die Sonar-API (`sonar-pro`) an Perplexity.
- Die Antwort wird mit Zitaten ausgegeben.
- Bei einem Fehler greift die Fallback-Kette: zuerst Gemini, dann GPT.

**Nutzen:** belegbare Quellen, z. B. zu Normen oder Fachliteratur.

**Bedienung**

```powershell
python -m nexus_orch.cli run research "Recherchiere Thema X und nenne die Quellen."
```

**Status:** Anbindung im Code vorhanden. Die Funktion mit eigenen API-Zugängen ist nicht bestätigt.

## 3. Aufgabe 2: Multi-LLM-System

**Was sie tut:** Verteilt Aufgaben nach `config/routing.json`.

| Aufgabentyp | Vorrangiger Anbieter |
|---|---|
| Recherche (`research`) | Perplexity |
| Code, Review (`code`, `review`) | Claude |
| Textentwurf (`draft`) | GPT |
| Langer Kontext (`long_context`) | Gemini |
| Vertraulich (`private`) | Lokales Modell (Ollama) |
| OCR (`ocr`) | Google Cloud Vision, Ersatz Gemini |

**Zusatzfunktionen**

- **Fallback:** Fällt der Hauptanbieter aus, wird der nächste genutzt; der Fehler wird protokolliert.
- **Privacy Hard Gate:** Anfragen mit `VERTRAULICH`, `CONFIDENTIAL` oder `[P3]` laufen nur lokal, ohne Cloud-Fallback.
- **Model Council:** Mehrere Modelle beantworten dieselbe Frage; bei Abweichungen entsteht eine Synthese (Konsens / Abweichungen / Empfehlung).
- **Lessons:** Erfahrungsregeln werden gespeichert (Status PROPOSED) und können gesucht werden.
- **Audit:** Das Protokoll enthält nur den Prompt-Hash, keinen Klartext.

**Bedienung**

```powershell
python -m nexus_orch.cli council engineering_decision "Vergleiche Variante A und B: ..."
python -m nexus_orch.cli lesson --agent claude --context EC5 --condition "wenn NKL fehlt" --pattern "NKL vor kmod abfragen" --evidence "Session 2026-10-13"
python -m nexus_orch.cli lessons kmod
python -m nexus_orch.cli registry
```

## 4. Erste Schritte

1. PowerShell im Ordner `orchestrator` öffnen.
2. `.\setup.ps1` ausführen (fragt API-Schlüssel ab, startet Tests). Danach ein neues Fenster öffnen.
3. `python -m nexus_orch.cli status` zeigt, welche Schlüssel hinterlegt sind.
4. Eine kleine echte Recherche mit `run research` starten, um die Anbindung zu prüfen.

## 5. Aktueller Status

- Vorhanden: Anbieter-Anbindungen, Routing, Fallback, Model Council, Audit, Lessons.
- Tests laufen überwiegend mit simulierten Anbietern und belegen keine Verbindung zu echten KI-Zugängen.
- Nicht bestätigt: lokale Installation, gültige API-Schlüssel, laufendes Ollama, erfolgreiche echte Anfragen.

## 6. Wichtige Grenzen

- Die Anbindung ist eine API-Anbindung; bestehende Perplexity-Computer-Chats werden nicht synchronisiert.
- `status` prüft nur, ob Schlüssel vorhanden sind, nicht ihre Gültigkeit und nicht, ob Ollama läuft.
- Der Aufgabentyp muss selbst angegeben werden.
- Lessons werden nicht automatisch an jede Anfrage angehängt.
- Das Council-Ergebnis ist eine KI-Zusammenfassung, keine fachliche Freigabe.
- Eine Suche in eigenen Dokumenten ist nicht angebunden: Das Inventar (858 Objekte, inkl. Ordner) listet nur Dateien; OCR, Chunking und Vektorindex stehen laut Bericht noch aus.

## PDF-Export

```bash
pandoc docs/NEXUS-AI-Kurz-Manual.md -o NEXUS-AI-Kurz-Manual.pdf
```

Alternativ in einem Markdown-Editor (z. B. VS Code mit „Markdown PDF“) öffnen und als PDF exportieren.
