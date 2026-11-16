param(
    [string]$PythonExe = "python",
    [string]$OutputDir = ".\rfem_gate_results",
    [switch]$DeepSeekAuth,
    [switch]$RFEM5Attach,
    [string]$RFEM6ModelName,
    [string]$ApprovedSpecJson,
    [string]$RFEM6NewCandidate
)
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Test-Path -LiteralPath $OutputDir) {
    throw "OutputDir exists: choose a NEW directory to protect previous evidence."
}
New-Item -ItemType Directory -Path $OutputDir -ErrorAction Stop | Out-Null
$outputAbs = (Resolve-Path -LiteralPath $OutputDir).Path
& $PythonExe (Join-Path $scriptDir "preflight.py") --out (Join-Path $outputAbs "preflight.json")
if ($LASTEXITCODE -ne 0) { throw "Preflight failed" }
& $PythonExe -m unittest discover -s $scriptDir -p "test_*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Offline tests failed" }
if ($DeepSeekAuth) {
    & $PythonExe (Join-Path $scriptDir "deepseek_auth.py") |
        Out-File -FilePath (Join-Path $outputAbs "deepseek_auth.json") -Encoding ascii -NoClobber
    if ($LASTEXITCODE -ne 0) { throw "DeepSeek authentication probe failed" }
}
if ($RFEM5Attach) {
    & $PythonExe (Join-Path $scriptDir "rfem5_probe.py") |
        Out-File -FilePath (Join-Path $outputAbs "rfem5_probe.json") -Encoding ascii -NoClobber
    if ($LASTEXITCODE -ne 0) { throw "RFEM5 probe failed" }
}
if ($RFEM6ModelName) {
    if (-not $ApprovedSpecJson) { throw "ApprovedSpecJson required for RFEM6 readback" }
    & $PythonExe (Join-Path $scriptDir "rfem6_readback.py") $ApprovedSpecJson `
        --model-name $RFEM6ModelName --out (Join-Path $outputAbs "rfem6_readback.json")
    if ($LASTEXITCODE -ne 0) { throw "RFEM6 readback command failed" }
}
if ($RFEM6NewCandidate) {
    & $PythonExe (Join-Path $scriptDir "rfem6_collision.py") `
        --candidate $RFEM6NewCandidate --out (Join-Path $outputAbs "rfem6_collision.json")
    if ($LASTEXITCODE -ne 0) { throw "RFEM6 collision check failed" }
}
Write-Host "Gate reports: $outputAbs"
