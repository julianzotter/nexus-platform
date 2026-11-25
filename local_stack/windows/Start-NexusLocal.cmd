@echo off
rem NEXUS Local Stack starten (ueber die Aufgabenplanung, nie doppelt) und Control Tower oeffnen.
setlocal
set "RT=%LOCALAPPDATA%\NEXUS\local"
set /p APPV=<"%RT%\app\CURRENT.txt"
pushd "%RT%\app\%APPV%"
where pythonw >nul 2>nul && (set "PYW=pythonw") || (set "PYW=pyw")
%PYW% -m nexus_local.supervisor --config "%RT%\nexus-local.json" --clear-stop-only
schtasks /Run /TN "NEXUS-LocalStack" >nul 2>nul
if errorlevel 1 (
  echo Aufgabe fehlt - Direktstart. Die Instanzsperre verhindert Doppelstarts.
  start "" /B %PYW% -m nexus_local.supervisor --config "%RT%\nexus-local.json"
)
popd
powershell -NoProfile -Command "for($i=0;$i -lt 20;$i++){try{Invoke-RestMethod http://127.0.0.1:8770/healthz -TimeoutSec 2|Out-Null;break}catch{Start-Sleep 1}}; $t=(Get-Content \"$env:LOCALAPPDATA\NEXUS\local\token.txt\" -Raw).Trim(); Start-Process ('http://127.0.0.1:8770/#t='+$t)"
endlocal
