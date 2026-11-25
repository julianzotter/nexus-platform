# NEXUS Local Stack - Installer (Benutzerebene, kein Admin). v0.1.0
#   powershell -ExecutionPolicy Bypass -File .\Install-NexusLocal.ps1            Installieren + starten + testen
#   ... -SkipModels      ohne Modell-Setup (Ollama)
#   ... -SetupMirror     privaten Git-Klon fuer review/* anlegen (Login im Vordergrund)
#   ... -Uninstall       Aufgabe abmelden, Stopp-Absicht setzen (nichts wird geloescht)
param([switch]$SkipModels, [switch]$SetupMirror, [switch]$Uninstall, [string]$TaskName = "NEXUS-LocalStack")
$ErrorActionPreference = "Stop"
$Here    = Split-Path -Parent $MyInvocation.MyCommand.Path
$Stack   = Split-Path -Parent $Here                          # ...\local_stack
$Runtime = Join-Path $env:LOCALAPPDATA "NEXUS\local"
$Cfg     = Join-Path $Runtime "nexus-local.json"
$ts      = Get-Date -Format "yyyyMMdd_HHmmss"
New-Item -ItemType Directory -Force -Path (Join-Path $Runtime "logs"), (Join-Path $Runtime "state"), (Join-Path $Runtime "app"), (Join-Path $Runtime "tests") | Out-Null
Start-Transcript -Path (Join-Path $Runtime "logs\install_$ts.log") | Out-Null

function Step($t) { Write-Host "`n=== $t ===" -ForegroundColor Cyan }

# ---------------------------------------------------------------- Python
Step "1 Python"
$py = $null
foreach ($c in @(@("py","-3.12"), @("py","-3"), @("python"))) {
  try { $exe = & $c[0] $c[1..9] -c "import sys;print(sys.executable)" 2>$null; if ($LASTEXITCODE -eq 0 -and $exe) { $py = $exe.Trim(); break } } catch {}
}
if (-not $py) { throw "Python 3.10+ nicht gefunden (https://www.python.org/downloads/windows/)" }
$ver = & $py -c "import sys;print('%d.%d'%sys.version_info[:2])"
if ([version]$ver -lt [version]"3.10") { throw "Python $ver zu alt (>=3.10 noetig)" }
$pyw = Join-Path (Split-Path $py) "pythonw.exe"
if (-not (Test-Path $pyw)) { throw "pythonw.exe fehlt neben $py" }
& $py -c "import zoneinfo; zoneinfo.ZoneInfo('Europe/Vienna')" 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "Hinweis: tzdata fehlt -> eingebaute CET/CEST-Regel wird genutzt (optional: $py -m pip install --user tzdata)" }
Write-Host "Python $ver : $py"

# ---------------------------------------------------------------- Uninstall
if ($Uninstall) {
  Step "Deinstallation (nichts wird geloescht)"
  & $py -c "import json,pathlib;p=pathlib.Path(r'$Runtime\state\desired.json');d=json.loads(p.read_text()) if p.exists() else {};d['_supervisor']='stopped';p.write_text(json.dumps(d))"
  try { Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue; Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false; Write-Host "[OK] Aufgabe $TaskName abgemeldet" } catch { Write-Host "Aufgabe nicht vorhanden" }
  Stop-Transcript | Out-Null; return
}

# ---------------------------------------------------------------- Deployment (versioniert, unveraenderlich)
Step "2 Versioniertes Deployment"
$repoRoot = Split-Path -Parent $Stack
$commit = "nogit"
try { $commit = (git -C $repoRoot rev-parse --short=12 HEAD).Trim() } catch {}
$dirty = ""
try { if (git -C $repoRoot status --porcelain -- local_stack) { $dirty = "-dirty-$ts" } } catch {}
$App = Join-Path $Runtime "app\$commit$dirty"
if (-not (Test-Path $App)) {
  robocopy (Join-Path $Stack "nexus_local") (Join-Path $App "nexus_local") /E /XD __pycache__ /NFL /NDL /NJH /NJS /NP | Out-Null
  if ($LASTEXITCODE -ge 8) { throw "robocopy Fehler $LASTEXITCODE" }
}
Set-Content -Path (Join-Path $Runtime "app\CURRENT.txt") -Value "$commit$dirty`n$App`ninstalled=$(Get-Date -Format s)" -Encoding ascii
Write-Host "App: $App"

# ---------------------------------------------------------------- Config + Token + Ordner
Step "3 Konfiguration, Token, Ordner"
if (-not (Test-Path $Cfg)) { Copy-Item (Join-Path $Stack "config\nexus-local.example.json") $Cfg; Write-Host "[NEU] $Cfg" }
else { Write-Host "[BLEIBT] $Cfg (wird nie ueberschrieben; Vorlage: config\nexus-local.example.json)" }
$tok = Join-Path $Runtime "token.txt"
if (-not (Test-Path $tok)) {
  $b = New-Object byte[] 32; [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($b)
  [IO.File]::WriteAllText($tok, (($b | ForEach-Object { $_.ToString("x2") }) -join ""))
}
icacls $tok /inheritance:r /grant:r "${env:USERNAME}:(R,W)" | Out-Null
if ($env:OneDrive) {
  foreach ($d in "NEXUS", "NEXUS\INBOX", "NEXUS\EXPORT-APPROVED") { New-Item -ItemType Directory -Force -Path (Join-Path $env:OneDrive $d) | Out-Null }
  Write-Host "OneDrive: $env:OneDrive\NEXUS\{INBOX,EXPORT-APPROVED}"
} else { Write-Host "WARNUNG: %OneDrive% nicht gesetzt -> OneDrive-Bruecken bleiben BLOCKED" -ForegroundColor Yellow }
foreach ($d in "gpt-exports", "skills-staging") { New-Item -ItemType Directory -Force -Path (Join-Path $Runtime $d) | Out-Null }
if (-not (Test-Path "G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\WORK")) { Write-Host "WARNUNG: WORK auf G: nicht gefunden (Drive for desktop gestartet?)" -ForegroundColor Yellow }

# ---------------------------------------------------------------- Bestand pruefen (nur lesen)
Step "4 Bestehende NEXUS-Aufgaben (nur Inventar, keine Aenderung)"
Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object { $_.TaskName -like "NEXUS*" -and $_.TaskName -ne $TaskName } |
  ForEach-Object { Write-Host (" - {0}  [{1}]  {2}" -f $_.TaskName, $_.State, (($_.Actions | ForEach-Object { $_.Arguments }) -join " ")) }

# ---------------------------------------------------------------- Git-Spiegel (optional)
if ($SetupMirror) {
  Step "5 Privater Git-Klon fuer review/* (Anmeldung ggf. im Browser)"
  $clone = Join-Path $Runtime "mirror-clone"
  if (-not (Test-Path (Join-Path $clone ".git"))) { git clone --no-tags https://github.com/julianzotter/nexus-platform.git $clone }
  git -C $clone config core.autocrlf false
  git -C $clone fetch origin main
  Write-Host "Klon bereit. In nexus-local.json git_mirror.enabled=true setzen (ID01-Entscheidung)."
}

# ---------------------------------------------------------------- Aufgabenplanung
Step "6 Aufgabenplanung $TaskName (AtLogOn + 15-min-Watchdog, RestartCount 5)"
$user = "$env:USERDOMAIN\$env:USERNAME"
$arg  = "-m nexus_local.supervisor --config `"$Cfg`""
$action   = New-ScheduledTaskAction -Execute $pyw -Argument $arg -WorkingDirectory $App
$tLogon   = New-ScheduledTaskTrigger -AtLogOn -User $user
$tLogon.Delay = "PT1M"                                   # Drive/OneDrive mounten lassen
$tWatch   = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable `
            -ExecutionTimeLimit ([TimeSpan]::Zero) -RestartCount 5 -RestartInterval (New-TimeSpan -Minutes 1) -MultipleInstances IgnoreNew
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
$registered = $false
try {
  Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger @($tLogon, $tWatch) -Settings $settings -Principal $principal `
    -Description "NEXUS Local Stack Supervisor (Control Tower 8770, MCP 8766, Bruecken, Reporter)" -Force | Out-Null
  [xml]$x = Export-ScheduledTask -TaskName $TaskName
  $rc = $x.Task.Settings.RestartOnFailure.Count
  Write-Host "[OK] Aufgabe registriert. Readback: RestartCount=$rc Interval=$($x.Task.Settings.RestartOnFailure.Interval) ExecutionTimeLimit=$($x.Task.Settings.ExecutionTimeLimit) MultipleInstances=$($x.Task.Settings.MultipleInstancesPolicy)"
  $registered = $true
} catch {
  Write-Host "Aufgabenplanung fehlgeschlagen: $($_.Exception.Message)" -ForegroundColor Yellow
  $startup = Join-Path ([Environment]::GetFolderPath("Startup")) "NEXUS-LocalStack.cmd"
  "@echo off`r`nstart `"`" /D `"$App`" `"$pyw`" $arg" | Set-Content -Path $startup -Encoding ascii
  Write-Host "[FALLBACK] Autostart-Datei: $startup (kein automatischer Neustart nach Absturz)"
}

# ---------------------------------------------------------------- Modelle
if (-not $SkipModels) { Step "7 Ollama-Modelle"; & (Join-Path $Here "Setup-NexusModels.ps1") -ConfigPath $Cfg }

# ---------------------------------------------------------------- Start + Test
Step "8 Start + Abnahmetest"
& $pyw -m nexus_local.supervisor --config $Cfg --clear-stop-only
if ($registered) { Start-ScheduledTask -TaskName $TaskName } else { Start-Process -FilePath $pyw -ArgumentList $arg -WorkingDirectory $App -WindowStyle Hidden }
$ok = $false
for ($i = 0; $i -lt 30; $i++) { try { $h = Invoke-RestMethod "http://127.0.0.1:8770/healthz" -TimeoutSec 2; if ($h.service -eq "nexus-control-tower") { $ok = $true; break } } catch { Start-Sleep 1 } }
if (-not $ok) { Write-Host "Control Tower antwortet nicht. Log: $Runtime\logs" -ForegroundColor Red }
& (Join-Path $Here "Test-NexusLocal.ps1") -TaskName $TaskName
$t = (Get-Content $tok -Raw).Trim()
Start-Process "http://127.0.0.1:8770/#t=$t"
Stop-Transcript | Out-Null
