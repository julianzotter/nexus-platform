<#
.SYNOPSIS
Read-only NEXUS P2 acceptance. Run from any directory with PowerShell 5.1 or 7+.
.DESCRIPTION
The approved baseline hash must come independently from ID01. All service operations
are reads. Timestamped reports are written to a new OS temp directory.
Exit 0: every technical gate passed. Exit 2: incomplete, failed, or unavailable.
#>
[CmdletBinding()]
param(
    [string]$BaselinePath,
    [string]$BaselineSha256,
    [string]$EvidenceDirectory = '.',
    [switch]$RunP1PreflightCheck
)
$ErrorActionPreference = 'Stop'
try {
    if ($RunP1PreflightCheck) {
        $p1 = Join-Path $PSScriptRoot 'nexus_p1_preflight.ps1'
        $repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
        & (Get-Process -Id $PID).Path -NoProfile -File $p1 -RepoRoot $repoRoot
        if ($LASTEXITCODE -ne 0) { Write-Warning 'P1 preflight incomplete. P2 independently rechecks the three runs.' }
    }
    $runner = Get-Command py -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    $arguments = @()
    if ($runner) { $arguments += '-3' }
    else {
        $runner = Get-Command python3,python -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    }
    if (-not $runner) { throw 'Repository prerequisite Python 3 is unavailable.' }
    $script = Join-Path (Split-Path -Parent $PSScriptRoot) 'nexus_p2.py'
    $arguments += @('-E', '-s', '-B', $script, '--evidence-dir', $EvidenceDirectory)
    if ($BaselinePath) { $arguments += @('--baseline', $BaselinePath) }
    if ($BaselineSha256) { $arguments += @('--baseline-sha256', $BaselineSha256) }
    & $runner.Source @arguments
    if ($LASTEXITCODE -eq 0) { exit 0 }
    if ($LASTEXITCODE -eq 2) { exit 2 }
    throw 'Python verifier failed to execute.'
} catch {
    # Also emit local evidence when the process cannot start.
    $now = [DateTime]::UtcNow
    try {
        $dir = Join-Path ([IO.Path]::GetTempPath()) ('nexus-p2-' + $now.ToString('yy_MM_dd_HHmmss-') + [guid]::NewGuid().ToString('N'))
        [void][IO.Directory]::CreateDirectory($dir)
        $utf8 = New-Object System.Text.UTF8Encoding($false)
        $status = [ordered]@{ decision='P2_BLOCKED'; checked_at=$now.ToString('o'); stage='bootstrap'; detail=$_.Exception.Message }
        $jsonPath = Join-Path $dir 'status.json'
        $mdPath = Join-Path $dir 'status.md'
        [IO.File]::WriteAllText($jsonPath, ($status | ConvertTo-Json), $utf8)
        [IO.File]::WriteAllText($mdPath, ("# NEXUS P2_BLOCKED" + [Environment]::NewLine + $status.checked_at + [Environment]::NewLine + $status.detail), $utf8)
        $sums = foreach ($path in @($jsonPath,$mdPath)) {
            (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() + '  ' + [IO.Path]::GetFileName($path)
        }
        [IO.File]::WriteAllLines((Join-Path $dir 'SHA256SUMS'), [string[]]$sums, $utf8)
        Write-Output "P2_REPORT_DIR=$dir"
    } catch { Write-Warning 'Local report could not be written.' }
    Write-Output 'P2_DECISION=P2_BLOCKED'
    exit 2
}
