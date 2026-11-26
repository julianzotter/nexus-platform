# Exercise the actual Windows process exit code, serializer and detached hashes.
$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot '..\..\tools\windows\verify_nexus_sync_p2.ps1'
$engine = (Get-Process -Id $PID).Path
$output = & $engine -NoProfile -File $script
if ($LASTEXITCODE -ne 2) { throw 'Missing ID01 baseline must exit 2.' }
$matchesDir = @($output | Where-Object { $_ -like 'P2_REPORT_DIR=*' })
if ($matchesDir.Count -ne 1) { throw 'Expected a single local report directory.' }
$dir = $matchesDir[0].Substring('P2_REPORT_DIR='.Length)
$report = Get-Content -LiteralPath (Join-Path $dir 'status.json') -Encoding UTF8 -Raw | ConvertFrom-Json
if ($report.report.decision -ne 'P2_BLOCKED' -or $report.report.gates.BASELINE.status -ne 'BLOCKED') {
    throw 'Missing baseline was not reported by the actual check engine.'
}
foreach ($row in (Get-Content -LiteralPath (Join-Path $dir 'SHA256SUMS'))) {
    if ($row -notmatch '^([a-f0-9]{64})  (status\.(json|md))$') { throw 'Invalid digest row.' }
    $expected = $Matches[1]
    $file = Join-Path $dir $Matches[2]
    if ((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash -ne $expected) { throw 'Bad report hash.' }
}
Write-Output ('PASS: blocked exit and verified report checksums on PowerShell ' + $PSVersionTable.PSVersion)
exit 0
