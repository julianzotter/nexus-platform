# NEXUS Sync via rclone: GitHub (nexus-platform, main) -> Google Drive per Ordner-ID
# Fuer Rechner ohne Google Drive for desktop (G:), Server/VM, Aufgabenplanung.
# Kein Push, kein Loeschen in Drive (rclone copy, niemals sync/delete).
#   .\sync_nexus_rclone.ps1               alle Jobs aus config\sync_targets.json
#   .\sync_nexus_rclone.ps1 -DryRun       nur anzeigen
#   .\sync_nexus_rclone.ps1 -Only reports nur Jobs mit src=reports
#   .\sync_nexus_rclone.ps1 -SkipTests    ohne pytest (nicht empfohlen)
param(
  [string]$Repo   = "$env:USERPROFILE\nexus-platform",
  [string]$Config = "",
  [string]$Only   = "",
  [switch]$DryRun,
  [switch]$SkipTests
)
$ErrorActionPreference = "Stop"
if (-not (Get-Command rclone -ErrorAction SilentlyContinue)) { throw "rclone fehlt -> siehe orchestrator\README.md (Abschnitt Drive-Sync rclone)" }
if (-not (Test-Path $Repo)) { git clone https://github.com/julianzotter/nexus-platform.git $Repo }
git -C $Repo checkout main; git -C $Repo pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "git pull fehlgeschlagen (lokale Aenderungen? -> git -C `"$Repo`" status)" }
if (-not $Config) { $Config = Join-Path $Repo "orchestrator\config\sync_targets.json" }
$cfg = Get-Content $Config -Raw -Encoding UTF8 | ConvertFrom-Json
$remote = $cfg.remote
rclone listremotes | Out-String | ForEach-Object { if ($_ -notmatch "(?m)^$remote`:") { throw "rclone-Remote '$remote' fehlt -> rclone config (Storage: drive)" } }

if (-not $SkipTests) {
  python -m pytest --version *> $null
  if ($LASTEXITCODE -ne 0) { throw "pytest fehlt -> python -m pip install pytest (oder -SkipTests)" }
  python -m pytest -q (Join-Path $Repo "orchestrator\tests"); if ($LASTEXITCODE -ne 0) { throw "Tests fehlgeschlagen - kein Sync" }
}
$sha = (git -C $Repo rev-parse --short HEAD)
$excl = @("--exclude", ".git/**", "--exclude", "__pycache__/**", "--exclude", ".pytest_cache/**",
          "--exclude", ".ipynb_checkpoints/**", "--exclude", "node_modules/**", "--exclude", ".venv/**",
          "--exclude", "venv/**", "--exclude", "audit/**", "--exclude", "*.pyc", "--exclude", ".env",
          "--exclude", "*.key", "--exclude", "*.pem", "--exclude", "*.secret", "--exclude", "desktop.ini")
$log = Join-Path $env:TEMP "nexus_rclone_$(Get-Date -Format yyMMdd_HHmmss).log"
$ok = 0; $fail = @()
foreach ($j in $cfg.jobs) {
  if ($Only -and $j.src -ne $Only) { continue }
  $from = Join-Path $Repo $j.src
  if (-not (Test-Path $from)) { Write-Host "[SKIP] $($j.src) fehlt im Repo"; continue }
  $id = $cfg.targets.($j.target)
  $to = "$remote,root_folder_id=$id`:$($j.dest)"
  $rcArgs = @("copy", $from, $to) + $excl + @("--log-file", $log, "--log-level", "INFO", "--stats-one-line", "-P")
  if ($DryRun) { $rcArgs += "--dry-run" }
  & rclone @rcArgs
  if ($LASTEXITCODE -ne 0) { $fail += "$($j.src)->$($j.target)"; Write-Host "[FEHLER] $($j.src) -> $($j.target)/$($j.dest)"; continue }
  if (-not $DryRun) {
    $stamp = "commit=$sha`nsynced=$(Get-Date -Format s)`nsource=github.com/julianzotter/nexus-platform/$($j.src)`nhost=$env:COMPUTERNAME"
    $stamp | rclone rcat "$to/SYNC_STAMP.txt"
  }
  $ok++; Write-Host "[OK] $($j.src) -> $($j.target)/$($j.dest) @ $sha"
}
Write-Host "Fertig: $ok ok, $($fail.Count) Fehler. Log: $log"
if ($fail.Count) { exit 1 }
