# MP3-TEXTA · NEXUS Kandidat v0.1.0

Quelle: Original-Whisper-MVP von 2026-08-19, archiviert im AI-MP3-TEXTA/PARSER/RELEASE-Ordner, plus lokale Aufnahme vom 2026-11-22.

1. Installation auf lokalem Windows-Rechner: Python 3.11+, ffmpeg/ffprobe, `pip install faster-whisper PyYAML` und kompatibler NVIDIA-Treiber/Runtime.
2. Drive synchronisieren. Für diese Datei: `G:\Meine Ablage\AI-MP3-TEXTA\26_11_22_KNEIDINGER-WIGEBA.mp3`.
3. `powershell -ExecutionPolicy Bypass -File .\RUN_KNEIDINGER_WINDOWS.ps1` nur auf vertrauenswürdigem Rechner starten. Kein Cloud-ASR.
4. Ergebnis in `TRANSCRIPTS/KNEIDINGER-WIGEBA__SSOT_CANDIDATE` prüfen; nach manuellem Golden-Slice-Review freigeben.

Diese Kandidatenfassung erzeugt keinen automatischen `RAW_TRANSCRIPT.md` oder `RUN_LOG.jsonl`; die Lücken stehen in `SKILL.md`. Kein Abschlussnachweis der Audio-Transkription.