# NEXUS Sync: GitHub (nexus-platform, main) -> Google Drive for desktop (G:)
# Richtung: GitHub = Versionierung -> Drive = SSOT-Ablage + Benchmark-Kopie. Kein Push, kein Loeschen (robocopy ohne /MIR).
#   .\sync_nexus.ps1              Orchestrator (SSOT + Benchmark) + komplettes Repo (SSOT\nexus-platform)
#   .\sync_nexus.ps1 -NoFullRepo  ohne komplettes Repo (Orchestrator, reports, evaluation bleiben)
param(
  [string]$Repo      = "$env:USERPROFILE\nexus-platform",
  [string]$Drive     = "G:\Meine Ablage",
  [string]$Ssot      = "_developement\LLM-LOCAL-SSOT\nexus-llm-orchestrator",
  [string]$Benchmark = "_INDEX_LNK\BENCHMARK Multi-LLM-Orchestrierung\nexus-llm-orchestrator",
  [string]$FullRepo  = "_developement\LLM-LOCAL-SSOT\nexus-platform",
  [switch]$NoFullRepo
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path $Drive)) { throw "Drive-Pfad fehlt: $Drive (Google Drive for desktop gestartet?)" }
if (-not (Test-Path $Repo)) { git clone https://github.com/julianzotter/nexus-platform.git $Repo }
git -C $Repo checkout main; git -C $Repo pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "git pull fehlgeschlagen (lokale Aenderungen? -> git -C `"$Repo`" status)" }
$src = Join-Path $Repo "orchestrator"
python -m pytest -q (Join-Path $src "tests"); if ($LASTEXITCODE -ne 0) { throw "Tests fehlgeschlagen - kein Sync" }
$sha = (git -C $Repo rev-parse --short HEAD)
$XD  = @(".git", "__pycache__", ".pytest_cache", ".ipynb_checkpoints", "node_modules", ".venv", "venv", "audit")
$XF  = @("*.pyc", ".env", "*.key", "*.pem", "*.secret")

function Sync-Dir($from, $to) {
  robocopy $from $to /E /XD $XD /XF $XF /R:2 /W:2 /NFL /NDL /NJH /NP | Out-Null
  if ($LASTEXITCODE -ge 8) { throw "robocopy Fehler $LASTEXITCODE -> $to" }
  "commit=$sha`nsynced=$(Get-Date -Format s)`nsource=github.com/julianzotter/nexus-platform/$(Split-Path $from -Leaf)" |
    Set-Content (Join-Path $to "SYNC_STAMP.txt") -Encoding UTF8
  Write-Host "[OK] $to  @ $sha"
}

$jobs = @(@($src, $Ssot), @($src, $Benchmark))
foreach ($d in "reports", "evaluation") {           # wie sync_targets.json (rclone): nexus-reports / nexus-evaluation
  $from = Join-Path $Repo $d
  if (Test-Path $from) { foreach ($t in $Ssot, $Benchmark) { $jobs += ,@($from, (Join-Path (Split-Path $t) "nexus-$d")) } }
}
if (-not $NoFullRepo) { $jobs += ,@($Repo, $FullRepo) }
foreach ($j in $jobs) { Sync-Dir $j[0] (Join-Path $Drive $j[1]) }
