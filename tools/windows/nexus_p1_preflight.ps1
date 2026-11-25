# Optional section 5, read-only. From the main script:
# if ($RunP1PreflightCheck) { & "$PSScriptRoot\nexus_p1_preflight.ps1" -RepoRoot $RepoRoot }
[CmdletBinding()]
param([string]$RepoRoot = (Get-Location).Path)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$repo = 'github.com/julianzotter/nexus-platform'
$workflows = 'nexus-monitor.yml','nexus-drive-poll.yml','nexus-delivery.yml'
$rows = @()
$errorsFound = @()
try {
    $branch = git --no-optional-locks -C $RepoRoot branch --show-current
    if ($LASTEXITCODE -ne 0) { throw 'git branch failed' }
    $head = git --no-optional-locks -C $RepoRoot rev-parse HEAD
    if ($LASTEXITCODE -ne 0) { throw 'git rev-parse failed' }
    $status = @(git --no-optional-locks -C $RepoRoot status --porcelain)
    if ($LASTEXITCODE -ne 0) { throw 'git status failed' }
    $repair = Test-Path -LiteralPath (Join-Path $RepoRoot 'tools/windows/repair_nexus_sync.ps1') -PathType Leaf
    Write-Output ("branch={0} HEAD={1} dirty_entries={2} repair_script={3}" -f $branch, $head, $status.Count, $repair)
    gh workflow list --repo $repo
    if ($LASTEXITCODE -ne 0) { throw 'gh workflow list failed' }
    foreach ($name in $workflows) {
        try {
            $raw = gh run list --repo $repo --workflow $name --branch main --limit 1 --json databaseId,status,conclusion,headSha,createdAt
            if ($LASTEXITCODE -ne 0) { throw 'gh run list failed' }
            $json = ($raw -join "`n").Trim()
            if (-not $json.StartsWith('[')) { throw 'expected an array' }
            $runs = @(ConvertFrom-Json -InputObject $json)
            if ($runs.Count -ne 1 -or $null -eq $runs[0]) { throw 'no unique latest main run' }
            $r = $runs[0]
            if ($r.databaseId -le 0 -or $r.headSha -cnotmatch '^[0-9a-f]{40}$' -or
                [string]::IsNullOrWhiteSpace($r.status) -or $null -eq $r.createdAt) { throw 'invalid run data' }
            $row = [ordered]@{workflow=$name; databaseId=$r.databaseId; status=$r.status; conclusion=$r.conclusion;
                              headSha=$r.headSha; createdAt=$r.createdAt}
        } catch {
            $errorsFound += "$name - $($_.Exception.Message)"
            $row = [ordered]@{workflow=$name; databaseId=''; status='UNAVAILABLE'; conclusion=''; headSha=''; createdAt=''}
        }
        $rows += [PSCustomObject]$row
    }
    $rows | Format-Table -AutoSize | Out-String -Width 240 | Write-Output
    if ($errorsFound.Count) { throw ($errorsFound -join ', ') }
} catch {
    Write-Output "P1_PREFLIGHT_BLOCKED - $($_.Exception.Message)"
    exit 2
}
Write-Output 'P1_PREFLIGHT_READ_COMPLETE'
exit 0
