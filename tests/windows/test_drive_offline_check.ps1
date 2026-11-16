# Behaviour tests use child processes because the diagnostic calls exit.
$ErrorActionPreference = "Stop"
$script = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\..\tools\windows\drive_offline_check.ps1"))
$engine = (Get-Process -Id $PID).Path
$root = Join-Path ([IO.Path]::GetTempPath()) ("nexus-offline-test-" + [guid]::NewGuid())
$targets = @(
    "LLM-LOCAL-SSOT\WORK\Folder.md",
    "LLM-LOCAL-SSOT\WORK\_AGBS.md",
    "LLM-LOCAL-SSOT\00_NEXUS_MANIFEST__CURRENT__2026-09-28.md",
    "LLM-LOCAL-SSOT\00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28.md",
    "MCP-ACCESS-TOOLS\nexus_ssot_mcp.py"
)
function Assert-Equal($actual, $expected, [string]$label) {
    if ($actual -ne $expected) { throw "$label expected=$expected actual=$actual" }
}
function Run-Check([switch]$Offline) {
    $argsList = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $script, "-Root", $root, "-AsJson")
    if ($Offline) { $argsList += "-OfflineConfirmed" }
    $output = & $engine @argsList
    $exitCode = $LASTEXITCODE
    $result = ($output -join [Environment]::NewLine) | ConvertFrom-Json
    Assert-Equal $result.ExitCode $exitCode "JSON/process exit consistency"
    return $result
}
try {
    foreach ($target in $targets) {
        $path = Join-Path $root $target
        New-Item -ItemType Directory -Force (Split-Path $path) | Out-Null
        [IO.File]::WriteAllText($path, "fixture", (New-Object Text.UTF8Encoding($false)))
    }
    $r = Run-Check
    Assert-Equal $r.ExitCode 2 "Fast reads cannot prove offline access"
    Assert-Equal $r.OfflineEvidence "NOT_VERIFIED" "No offline inference"
    Assert-Equal @($r.Files).Count 5 "All required files checked"
    foreach ($row in $r.Files) {
        Assert-Equal $row.Status "READABLE" "Readable file"
        Assert-Equal $row.SHA256.Length 64 "Byte hash"
        Assert-Equal $row.SHA256 "f16d05ec6b29248d2c61adb1e9263f78e4f7bace1b955014a2d17872cfe4064d" "Exact fixture hash"
    }
    $r = Run-Check -Offline
    Assert-Equal $r.ExitCode 0 "Explicit attestation recorded"
    Assert-Equal $r.PinningEvidence "NOT_VERIFIED" "No pinning claim"
    $first = Join-Path $root $targets[0]
    [IO.File]::WriteAllBytes($first, [byte[]]@())
    $r = Run-Check -Offline
    Assert-Equal $r.ExitCode 1 "Empty fails even offline"
    Assert-Equal $r.Files[0].Status "EMPTY" "Empty detection"
    [IO.File]::WriteAllBytes($first, [byte[]]@(0xFF, 0xFE, 0xFF))
    $r = Run-Check
    Assert-Equal $r.Files[0].Status "INVALID_UTF8" "Invalid UTF8 detection"
    [IO.File]::WriteAllText($first, "fixture")
    $lock = [IO.File]::Open($first, [IO.FileMode]::Open, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
    try {
        $r = Run-Check
        Assert-Equal $r.Files[0].Status "READ_ERROR" "Locked file detection"
        Assert-Equal $r.ExitCode 1 "Read error fails closed"
        Assert-Equal @($r.Files | Where-Object Status -eq "READABLE").Count 4 "Continue after read error"
    } finally { $lock.Dispose() }
    Remove-Item -LiteralPath $first
    $r = Run-Check
    Assert-Equal $r.Files[0].Status "MISSING_OR_NOT_FILE" "Missing detection"
    Assert-Equal @($r.Files | Where-Object Status -eq "READABLE").Count 4 "Continue after failure"
    New-Item -ItemType Directory $first | Out-Null
    $r = Run-Check
    Assert-Equal $r.Files[0].Status "MISSING_OR_NOT_FILE" "Directory rejected"
    Write-Output "PASS: offline uncertainty, attestation, hash, empty, UTF8, missing, directory, continuation"
} finally {
    if (Test-Path $root) { Remove-Item -LiteralPath $root -Recurse -Force }
}
# Expected failing child processes must not become the test harness exit status.
exit 0
