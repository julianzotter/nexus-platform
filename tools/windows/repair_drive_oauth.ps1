<# Local interactive repair; never accepts or prints raw token values. #>
param([string]$Python = "py", [string]$ClientJson)
$ErrorActionPreference = "Stop"
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))
Push-Location $root
try {
    & $Python -m pip install -r tools/oauth-setup-requirements.txt
    if ($LASTEXITCODE -ne 0) { throw "OAuth setup dependencies failed" }
    & gh auth status --hostname github.com
    if ($LASTEXITCODE -ne 0) {
        & gh auth login --hostname github.com --web
        if ($LASTEXITCODE -ne 0) { throw "GitHub authorization incomplete" }
    }
    $options = @("tools/configure_drive_oauth.py", "--publish")
    if (Test-Path -LiteralPath ".nexus-credentials/drive-oauth.json" -PathType Leaf) {
        $options += "--renew"
    } elseif (-not $ClientJson) {
        Add-Type -AssemblyName System.Windows.Forms
        $picker = New-Object System.Windows.Forms.OpenFileDialog
        $picker.Title = "Select original Google Desktop OAuth client JSON (local file only)"
        $picker.Filter = "Google OAuth client (*.json)|*.json"
        try {
            if ($picker.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { throw "OAuth client selection cancelled" }
            $ClientJson = $picker.FileName
        } finally { $picker.Dispose() }
    }
    if ($ClientJson) { $options += @("--client-json", $ClientJson) }
    & $Python @options
    if ($LASTEXITCODE -ne 0) { throw "OAuth renewal/preflight failed; previous credentials retained unless publication failed after local renewal" }
    & $Python tools/configure_drive_oauth.py --check --require-write
    if ($LASTEXITCODE -ne 0) { throw "Post-renewal WORK metadata check failed" }
    Write-Host "OAUTH_RENEWED_AND_PUBLISHED; WORK metadata verified. Delivery and registry readback still require their own runs."
} finally { Pop-Location }
exit 0
