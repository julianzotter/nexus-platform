# NEXUS Sync: GitHub (nexus-platform, main) -> Google Drive for desktop (G:)
# Richtung: GitHub = Versionierung -> Drive = SSOT-Ablage + Benchmark-Kopie. Kein Push, kein Loeschen (robocopy ohne /MIR).
param(
  [string]$Repo      = "$env:USERPROFILE\nexus-platform",
  [string]$Drive     = "G:\Meine Ablage",
  [string]$Ssot      = "_developement\LLM-LOCAL-SSOT\nexus-llm-orchestrator",
  [string]$Benchmark = "_INDEX_LNK\BENCHMARK Multi-LLM-Orchestrierung\nexus-llm-orchestrator"
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path $Repo)) { git clone https://github.com/julianzotter/nexus-platform.git $Repo }
git -C $Repo checkout main; git -C $Repo pull --ff-only
$src = Join-Path $Repo "orchestrator"
python -m pytest -q (Join-Path $src "tests"); if ($LASTEXITCODE -ne 0) { throw "Tests fehlgeschlagen - kein Sync" }
$sha = (git -C $Repo rev-parse --short HEAD)
foreach ($t in $Ssot, $Benchmark) {
  $dst = Join-Path $Drive $t
  robocopy $src $dst /E /XD __pycache__ .pytest_cache audit /XF *.pyc /NFL /NDL /NJH /NP | Out-Null
  if ($LASTEXITCODE -ge 8) { throw "robocopy Fehler $LASTEXITCODE -> $dst" }
  "commit=$sha`nsynced=$(Get-Date -Format s)`nsource=github.com/julianzotter/nexus-platform/orchestrator" | Set-Content (Join-Path $dst "SYNC_STAMP.txt") -Encoding UTF8
  Write-Host "[OK] $dst  @ $sha"
}
