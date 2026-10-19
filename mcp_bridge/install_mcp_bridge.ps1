# NEXUS MCP-Bridge: lokale Installation (Windows, Google Drive for desktop auf G:)
#   .\install_mcp_bridge.ps1                 venv + mcp installieren, Selbsttest, Config ausgeben
#   .\install_mcp_bridge.ps1 -ClaudeDesktop  zusaetzlich in %APPDATA%\Claude\claude_desktop_config.json eintragen (Backup)
param([string]$Work = "G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\WORK", [string]$AgentId = "ID03", [switch]$ClaudeDesktop, [switch]$Verifier)
$ErrorActionPreference = "Stop"
$here = $PSScriptRoot; $repo = Split-Path $here
if (-not (Test-Path $Work)) { throw "WORK-Mount fehlt: $Work (Google Drive for desktop gestartet?)" }
python -m venv "$here\.venv"
& "$here\.venv\Scripts\python.exe" -m pip install -q -r "$here\requirements.txt"
$py = "$here\.venv\Scripts\python.exe"
$env:NEXUS_WORK_ROOT = $Work; $env:NEXUS_REPO_ROOT = $repo
& $py -c "import sys; sys.path.insert(0, r'$here'); from nexus_mcp_server import NexusBridge as B; import json; print(json.dumps(B(r'$Work', r'$repo').status()))"
$entry = [ordered]@{ command = $py; args = @("$here\nexus_mcp_server.py")
  env = [ordered]@{ NEXUS_WORK_ROOT = $Work; NEXUS_REPO_ROOT = $repo; NEXUS_MCP_WRITE = "0"; NEXUS_AGENT_ID = $AgentId } }
if ($ClaudeDesktop) {
  $cfg = Join-Path $env:APPDATA "Claude\claude_desktop_config.json"
  $obj = if (Test-Path $cfg) { Copy-Item $cfg "$cfg.bak" -Force; Get-Content $cfg -Raw | ConvertFrom-Json } else { [pscustomobject]@{} }
  if (-not $obj.mcpServers) { $obj | Add-Member mcpServers ([pscustomobject]@{}) }
  $obj.mcpServers | Add-Member "nexus-bridge" $entry -Force
  New-Item -ItemType Directory -Force (Split-Path $cfg) | Out-Null
  $obj | ConvertTo-Json -Depth 8 | Set-Content $cfg -Encoding UTF8
  Write-Host "[OK] Claude Desktop konfiguriert (Backup: $cfg.bak) - Claude neu starten"
} else {
  Write-Host "[OK] MCP-Eintrag fuer deinen Client:"; @{ mcpServers = @{ "nexus-bridge" = $entry } } | ConvertTo-Json -Depth 8
}
if ($Verifier) {  # deterministischer Verifier alle 15 min (lokal, 0 Tokens): TIMEOUT/VERIFIED + STATUS.md/_FRONT_LOG.md
  $arg = "`"$repo\tools\nexus_ledger.py`" --work `"$Work`" --agent SYS-VERIFY verify"
  $act = New-ScheduledTaskAction -Execute $py -Argument $arg -WorkingDirectory $repo
  $trg = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 15)
  Register-ScheduledTask -TaskName "NEXUS-Ledger-Verify" -Action $act -Trigger $trg -Force | Out-Null
  Write-Host "[OK] Aufgabe NEXUS-Ledger-Verify alle 15 min"
}
Write-Host "Schreiben (submit_result) aktivieren: NEXUS_MCP_WRITE = 1 im Client-Eintrag."
