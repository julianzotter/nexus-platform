<# Run in the current nexus-platform checkout; all live stages fail closed. #>
param([string]$Python = "py", [string]$ClientJson)
$ErrorActionPreference = "Stop"
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))
Push-Location $root
try {
    # Child process: successful exit from the OAuth helper must not exit this script.
    $shell = (Get-Process -Id $PID).Path
    $options = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $PSScriptRoot "repair_drive_oauth.ps1"), "-Python", $Python)
    if ($ClientJson) { $options += @("-ClientJson", $ClientJson) }
    & $shell @options
    if ($LASTEXITCODE -ne 0) { throw "OAuth renewal incomplete" }
    & $Python tools/repair_control_registers.py --apply
    if ($LASTEXITCODE -ne 0) { throw "Registry/ledger repair blocked; inspect reports/control-repair/repair-receipt.json" }
    $sourceRun = & gh run list --repo julianzotter/nexus-platform --workflow nexus-monitor.yml --branch main --status completed --limit 1 --json databaseId --jq ".[0].databaseId"
    if ($LASTEXITCODE -ne 0 -or $sourceRun -notmatch '^\d+$') { throw "No completed monitor source run found" }
    & gh workflow run nexus-delivery.yml --repo julianzotter/nexus-platform -f "source_run_id=$sourceRun"
    if ($LASTEXITCODE -ne 0) { throw "Delivery dispatch failed" }
    Write-Host "CONTROL_REGISTERS_VERIFIED; DELIVERY_DISPATCHED (completion/readback not yet confirmed)."
} finally { Pop-Location }
exit 0
