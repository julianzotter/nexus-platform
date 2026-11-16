@echo off
rem NEXUS Control Tower lokal starten (ID06, v0.2.0). Liest nur, schreibt nichts.
setlocal
set "WORK=G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\WORK"
set "PORT=8765"
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (set "PY=py -3") else (set "PY=python")
echo Starte NEXUS Control Tower auf http://localhost:%PORT%
%PY% "%~dp0nexus_tower.py" --work "%WORK%" --port %PORT% --open
if errorlevel 1 echo Start fehlgeschlagen. Ist Python installiert und der WORK-Pfad richtig?
pause
