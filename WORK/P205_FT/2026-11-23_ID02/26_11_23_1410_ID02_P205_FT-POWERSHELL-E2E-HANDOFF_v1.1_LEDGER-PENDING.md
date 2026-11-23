# P205 FT – Windows Excel Desktop E2E Handoff v1.1

Status: `READY_FOR_WINDOWS_EXECUTION / ENGINEERING_RELEASE_BLOCKED`

## Ursache und Korrektur

- Der vorherige Abbruch trat vor Excel auf, weil ein blockweise eingefügter Lauf `Workbooks.Open($source, …)` erreichte, ohne `$source` zu initialisieren.
- Die Korrektur ist eine vollständige `.ps1`-Datei mit Pflichtparametern. Es gibt keine freie `$source`-Variable; `InputXlsx` wird sofort zu `$sourcePath` kanonisiert.
- Der Quell-Hash wird vor dem Öffnen geprüft und nach dem Lauf erneut verifiziert. Die Quelle wird read-only geöffnet; gespeichert wird ausschließlich eine neue Ausgabekopie.

## Ausführung am Windows-Rechner

```powershell
$script = "C:\NEXUS\tools\windows\P205_FT_Excel_Native_Recalc_v1_2.ps1"
$input  = "<ABSOLUTER_PFAD_ZUR_VERIFIZIERTEN_ARBEITSMAPPE>"
$out    = "C:\NEXUS_RUNS\P205_FT\EXCEL_E2E"
$sha256 = "<ERWARTETER_SHA256_DER_QUELLE>"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File $script `
  -InputXlsx $input `
  -OutputDirectory $out `
  -ExpectedSha256 $sha256
```

## PASS-Kriterien

1. Prozess beendet mit Exitcode `0`.
2. JSON-Report enthält `status=COMPLETE`, `source_unchanged=true` und `calculation=FULL_REBUILD_SAVE_CLOSE_COMPLETE`.
3. Quell-SHA-256 ist unverändert; Ausgabe-SHA-256 und Excel-Version/Build sind protokolliert.
4. Erzeugte Arbeitsmappe wird per OOXML-Readback und anschließend unabhängig geprüft.
5. Erst danach dürfen ID03/ID07 Peer Review und ID01-Freigabe erfolgen.

## Grenzen

- Der bereitgestellte Cloud-Executor besitzt weder Windows PowerShell noch Excel COM. Hier wurde deshalb nur der deterministische Skriptvertrag statisch getestet.
- Ein erfolgreicher Excel-Lauf schließt Plan-/RFEM-Zuordnung, unabhängige Prüfung und technische Freigabe nicht automatisch.
