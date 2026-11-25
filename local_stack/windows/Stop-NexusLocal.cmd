@echo off
rem NEXUS Local Stack geordnet stoppen. Die Stopp-Absicht bleibt gespeichert (kein Neustart durch den Watchdog),
rem bis Start-NexusLocal.cmd ausgefuehrt wird. Ollama wird nicht angefasst.
powershell -NoProfile -Command "$t=(Get-Content \"$env:LOCALAPPDATA\NEXUS\local\token.txt\" -Raw).Trim(); try { Invoke-RestMethod http://127.0.0.1:8770/api/supervisor/stop -Method Post -Headers @{Authorization=('Bearer '+$t)} -ContentType 'application/json' -Body '{}' | Out-Null; 'NEXUS Local Stack gestoppt.' } catch { 'Supervisor nicht erreichbar: ' + $_.Exception.Message }"
