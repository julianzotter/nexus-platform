---
name: mp3-texta
description: Reproduce the archived local MP3 transcription workflow with deterministic preflight, source-bound execution, QA gates, and registration controls; use only for explicitly selected local audio and never imply validated transcription without review.
version: 0.1.0-candidate
status: PROPOSED_REVIEW_REQUIRED
owner_id: ID01
orchestrator_id: ID02
skill_type: local-audio-transcription
canonical_source: "gdrive:1qkXKaMfljrJJLjNVEyCdiC-DnY1UQrVT"
source_location: "AI-MP3-TEXTA/PARSER/RELEASE_2026-08-19_RECURSIVE_TRANSCRIPTION_MVP_v1_0/recursive_mp3_test_v1.0.zip"
source_record: "gdrive:1UbBJzdwz4-IHqOSgSn1EpR3R6InSWFUB"
engines: [faster-whisper, ffmpeg, ffprobe]
local_first: true
audio_external_upload: prohibited_without_ID01_approval
qa_status: STATIC_PREFLIGHT_ONLY
registration_status: REGISTRATION_PENDING
---
# MP3-TEXTA — reproduzierbarer Transkriptions-Skill (Quelle unverändert)

## Einsatz und Grenzen
Verarbeite benannte lokale/Drive-synchronisierte MP3-Dateien in einem **lokalen Windows-Python-/GPU-Lauf**, ohne Audio an Cloud-ASR zu senden. Diese Kandidatenfassung kapselt den am 19.08.2026 archivierten rekursiven MVP **unverändert**; eine Produktionsfreigabe oder abgeschlossene Transkription folgt daraus nicht. Der `AI-MP3-TEXTA`-Ordner allein ist kein autonom ausführender ChatGPT-Skill.

## Quellenhierarchie
1. NEXUS: CURRENT Manifest-MD, CURRENT Baseline-MD, `_AGBS.md` v007.1 (aktivierte Fassung separat durch Provider-Readback nachweisen) und `_TROUBLESHOOTING.md`.
2. Originalquelle: `recursive_mp3_test_v1.0.zip` (Drive-ID oben), `26_08_19_STATUSREPORT_RECURSIVE_MP3_TRANSCRIPTION_MVP_v1.0.md`.
3. Originalcode: `scripts/recursive_transcribe_v1.py`, `scripts/config.yaml` — byteidentisch aus Quell-ZIP, kein stilles Patchen.

## Preflight (P0)
- Drive-Datei-ID, Dateiname, Bytes, SHA-256, Codec, Samplingrate, Kanäle und Dauer mit `ffprobe` auf Rohdatei erfassen.
- `ffmpeg`, `ffprobe`, Python und `faster-whisper` prüfen; bei CUDA: `nvidia-smi`, Speicher, CTranslate2/CUDA/cuDNN-Kompatibilität prüfen.
- WAV-Decode eines kleinen, repräsentativen Audioausschnitts mit `ffmpeg` tatsächlich prüfen.
- Modell-/Versionsidentität und GPU-Gerät/Compute-Type aufzeichnen. Fehlende Gewichte/Tools → `BLOCKED_ASR`, keine erfundene Transkription.

## ASR (P1–P5) — unverändertes Quellverfahren
1. 240-s-Kernfenster mit ±15-s Überlappung, letzte Fensterlänge an die Gesamtaufnahmedauer anpassen.
2. `small`, `device=cuda`, `compute_type=float16`, `language=de`, `beam_size=5`, VAD und Wortzeitstempel; `condition_on_previous_text=False`.
3. Kontrollierte Fachwortliste: statische Seed-Terme + Häufigkeit ≥2, maximal 40 Begriffe. Nicht belegte Namen/Fachwörter nicht als Fakt übernehmen. **Achtung:** die Seed-Terme des Original-MVP sind Software-/LLM-Begriffe und nicht auf WIGEBA validiert; diese Einschränkung im Review ausweisen.
4. Nur bei `avg_logprob < -0.65` auf das Modell `large-v3` wechseln, maximal zwei Refinement-Runden; Änderungen in Delta-Datei protokollieren.
5. Merge mittels mindestens 50 % zeitlicher Überlappung bei Segmentduplikaten; bei abweichendem Inhalt Review-Flag statt fachlich ungerechtfertigter Korrektur.

## CLI (originalgetreu)
```powershell
python scripts/recursive_transcribe_v1.py 'G:\Meine Ablage\AI-MP3-TEXTA\26_11_22_KNEIDINGER-WIGEBA.mp3' --config scripts/config.yaml --output 'G:\Meine Ablage\AI-MP3-TEXTA\TRANSCRIPTS\KNEIDINGER-WIGEBA__SSOT_CANDIDATE'
```
Option: `RUN_KNEIDINGER_WINDOWS.ps1` prüft Vorbedingungen und startet exakt diesen Code.

## Outputs des **Originalcodes**
- `REFINED_TRANSCRIPT.md`, `KNOWLEDGE_OBJECTS.jsonl`, `KEYWORD_REGISTRY.json`, `REFINEMENT_DELTA.jsonl`, `QA_REPORT.json`, temporäre WAVs.
- Im ursprünglichen MVP **nicht implementiert**: eigenständiges `RAW_TRANSCRIPT.md`, `RUN_LOG.jsonl`, `MANIFEST.json`, unabhängige Zeitachsen-/Speech-Coverage-Prüfung, sichere Wiederaufnahme nach Abbruch und Sprecherdiarisierung. Diese Lücken stehen einer `VALIDATED`-Behauptung entgegen; sie werden nicht durch die neue Skill-Anleitung wegdefiniert.

## QA / Promotion
- Quelle/Dateiidentität verifizieren, Segmentzeiten monoton und in [0, duration] prüfen, Überlappung/Dubletten kontrollieren.
- Wortgetreue Fachbegriffe, Projektnamen, Termine, Beträge, Sprecherzuordnung und mögliche fehlende Sprache manuell gegen Audio prüfen.
- `QA_REPORT.json` enthält im Original nur begrenzte Prüfwerte. Die letzte Segmentzeit ist **kein** Beweis für vollständige Sprachabdeckung.
- Ergebnisse bleiben `SSOT_CANDIDATE`, bis unabhängige Stichproben-/Golden-Slice-Validierung und ID01-Freigabe erfolgen.

## Registrierung und Synchronisation
- Keine MP3, Transkripte, Kundendaten oder Zugangsdaten in ein womöglich öffentliches GitHub-Repo pushen.
- Skill-Definition als Kandidat auf Feature-Branch und als kanonischer Drive-Skill-Kandidat ablegen, Source-IDs und Hashes protokollieren.
- Bei fehlender atomarer Schreibfreigabe für `file-registry.jsonl` Registrierung ausschließlich als `REGISTRATION_PENDING` + append-only Delta in WORK; keine erfundene Ledgernummer.
- ChatGPT Library = Dokumentkopie; das ist **keine** Aktivierung als installierter Plugin-Skill und kein verifizierter Memory-Eintrag.
