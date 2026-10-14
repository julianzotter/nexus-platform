# NEXUS Auto-Sync: Windows-Aufgabenplanung fuer sync_nexus.ps1 (GitHub main -> Google Drive, testgated, ohne Loeschen)
#   .\install_autosync.ps1                  taeglich 07:00 + bei Anmeldung
#   .\install_autosync.ps1 -Time 18:30      andere Uhrzeit
#   .\install_autosync.ps1 -Rclone          sync_nexus_rclone.ps1 statt Laufwerk G:
#   .\install_autosync.ps1 -Remove          Aufgabe entfernen
param([string]$Time = "07:00", [switch]$Rclone, [switch]$Remove, [string]$Name = "NEXUS-AutoSync")
$ErrorActionPreference = "Stop"
if ($Remove) { Unregister-ScheduledTask -TaskName $Name -Confirm:$false; Write-Host "[OK] Aufgabe $Name entfernt"; return }
$script = Join-Path $PSScriptRoot ($(if ($Rclone) { "sync_nexus_rclone.ps1" } else { "sync_nexus.ps1" }))
if (-not (Test-Path $script)) { throw "Skript fehlt: $script" }
$log = Join-Path $env:LOCALAPPDATA "NEXUS\autosync.log"
New-Item -ItemType Directory -Force (Split-Path $log) | Out-Null
$cmd = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command `"& '$script' *>> '$log'`""
$action   = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $cmd -WorkingDirectory $PSScriptRoot
$triggers = @((New-ScheduledTaskTrigger -Daily -At $Time), (New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME))
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30)
Register-ScheduledTask -TaskName $Name -Action $action -Trigger $triggers -Settings $settings -Description "NEXUS GitHub->Drive Sync" -Force | Out-Null
Write-Host "[OK] Aufgabe $Name: taeglich $Time + bei Anmeldung -> $script"
Write-Host "     Log: $log  ·  Sofort testen: Start-ScheduledTask -TaskName $Name"
