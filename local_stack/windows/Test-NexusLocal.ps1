# NEXUS Local Stack - Abnahmetest auf der Workstation. v0.1.0
# Ergebnis: PASS / FAIL / NOT_RUN je Test + JSON in %LOCALAPPDATA%\NEXUS\local\tests
param([string]$TaskName = "NEXUS-LocalStack", [switch]$SkipLlm)
$ErrorActionPreference = "Continue"
$Runtime = Join-Path $env:LOCALAPPDATA "NEXUS\local"
$tok = (Get-Content (Join-Path $Runtime "token.txt") -Raw).Trim()
$cfg = Get-Content (Join-Path $Runtime "nexus-local.json") -Raw | ConvertFrom-Json
$T = [ordered]@{}
$H = @{ Authorization = "Bearer $tok" }

function Raw-Http([int]$port, [string]$req) {
  $c = New-Object Net.Sockets.TcpClient("127.0.0.1", $port); $s = $c.GetStream()
  $b = [Text.Encoding]::ASCII.GetBytes($req); $s.Write($b, 0, $b.Length)
  $s.ReadTimeout = 5000; $buf = New-Object byte[] 4096; $n = $s.Read($buf, 0, 4096); $c.Close()
  [Text.Encoding]::ASCII.GetString($buf, 0, $n)
}
function Mcp([string]$method, $params, [string]$name) {
  $params["_meta"] = @{ "io.modelcontextprotocol/protocolVersion" = "2026-07-28"; "io.modelcontextprotocol/clientInfo" = @{ name = "Test-NexusLocal"; version = "0.1.0" }; "io.modelcontextprotocol/clientCapabilities" = @{} }
  $body = @{ jsonrpc = "2.0"; id = 1; method = $method; params = $params } | ConvertTo-Json -Depth 8
  $h = @{ Authorization = "Bearer $tok"; "MCP-Protocol-Version" = "2026-07-28"; "Mcp-Method" = $method; Accept = "application/json, text/event-stream" }
  if ($name) { $h["Mcp-Name"] = $name }
  Invoke-RestMethod "http://127.0.0.1:8766/mcp" -Method Post -Headers $h -Body ([Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json" -TimeoutSec 600
}

# T1 Aufgabe registriert mit erwarteten Einstellungen
try { [xml]$x = Export-ScheduledTask -TaskName $TaskName -ErrorAction Stop
  $T["T1 Aufgabe RestartCount=5, kein Zeitlimit"] = if ($x.Task.Settings.RestartOnFailure.Count -eq "5" -and $x.Task.Settings.ExecutionTimeLimit -eq "PT0S") { "PASS" } else { "FAIL" }
} catch { $T["T1 Aufgabe RestartCount=5, kein Zeitlimit"] = "FAIL (nicht registriert)" }

# T2 Control Tower erreichbar (Health-Schema)
try { $h = Invoke-RestMethod "http://127.0.0.1:8770/healthz" -TimeoutSec 3; $T["T2 Control Tower /healthz"] = if ($h.service -eq "nexus-control-tower") { "PASS" } else { "FAIL" } } catch { $T["T2 Control Tower /healthz"] = "FAIL" }

# T3 Authentifizierung
try { Invoke-RestMethod "http://127.0.0.1:8770/api/status" -TimeoutSec 3 | Out-Null; $T["T3a /api/status ohne Token = 401"] = "FAIL" } catch { $T["T3a /api/status ohne Token = 401"] = if ($_.Exception.Response.StatusCode.value__ -eq 401) { "PASS" } else { "FAIL" } }
try { $st = Invoke-RestMethod "http://127.0.0.1:8770/api/status" -Headers $H -TimeoutSec 5; $T["T3b /api/status mit Token"] = if ($st.tasks.Count -ge 4) { "PASS" } else { "FAIL" } } catch { $T["T3b /api/status mit Token"] = "FAIL" }

# T4 DNS-Rebinding / fremde Origin
try { $r = Raw-Http 8770 "GET /api/status HTTP/1.1`r`nHost: evil.example:8770`r`nAuthorization: Bearer $tok`r`nConnection: close`r`n`r`n"; $T["T4a fremder Host = 421"] = if ($r -match "^HTTP/1.1 421") { "PASS" } else { "FAIL" } } catch { $T["T4a fremder Host = 421"] = "FAIL" }
try { $r = Raw-Http 8770 "POST /api/task HTTP/1.1`r`nHost: 127.0.0.1:8770`r`nOrigin: http://evil.example`r`nAuthorization: Bearer $tok`r`nContent-Type: application/json`r`nContent-Length: 2`r`nConnection: close`r`n`r`n{}"; $T["T4b fremde Origin = 403"] = if ($r -match "^HTTP/1.1 403") { "PASS" } else { "FAIL" } } catch { $T["T4b fremde Origin = 403"] = "FAIL" }

# T5 MCP 2026-07-28: discover + tools/list
try { $d = Mcp "server/discover" @{} $null; $l = Mcp "tools/list" @{} $null
  $T["T5 MCP discover + tools/list"] = if ($d.result.supportedVersions -contains "2026-07-28" -and $l.result.tools.Count -ge 5) { "PASS ($($l.result.tools.Count) Tools)" } else { "FAIL" } } catch { $T["T5 MCP discover + tools/list"] = "FAIL $($_.Exception.Message)" }

# T6 MCP work_list (WORK gemountet)
try { $w = Mcp "tools/call" @{ name = "work_list"; arguments = @{ limit = 3 } } "work_list"
  $T["T6 MCP work_list WORK"] = if (-not $w.result.isError) { "PASS ($($w.result.structuredContent.count) Eintraege)" } else { "FAIL $($w.result.content[0].text)" } } catch { $T["T6 MCP work_list WORK"] = "FAIL" }

# T7 lokales Modell ueber MCP + GPU-Residenz
if ($SkipLlm) { $T["T7 local_llm + 100% GPU"] = "NOT_RUN" } else {
  try { $sw = [Diagnostics.Stopwatch]::StartNew(); $r = Mcp "tools/call" @{ name = "local_llm"; arguments = @{ prompt = "Antworte nur mit: OK"; max_tokens = 20 } } "local_llm"; $sw.Stop()
    $ps = (Invoke-RestMethod "http://127.0.0.1:11434/api/ps").models | Select-Object -First 1
    $gpu = if ($ps.size) { [math]::Round(100 * $ps.size_vram / $ps.size) } else { 0 }
    $T["T7 local_llm + 100% GPU"] = if (-not $r.result.isError -and $gpu -ge 100) { "PASS ($([math]::Round($sw.Elapsed.TotalSeconds,1)) s, $($ps.name), ctx $($ps.context_length))" } elseif (-not $r.result.isError) { "FAIL (GPU $gpu %)" } else { "FAIL $($r.result.content[0].text)" }
  } catch { $T["T7 local_llm + 100% GPU"] = "FAIL $($_.Exception.Message)" } }

# T8 Bruecken nicht blockiert (Probelauf)
try { $b = $st.bridges.rules | ForEach-Object { "$($_.name)=$(if ($_.last.blocked) { $_.last.blocked } else { 'OK' })" }
  $T["T8 Bruecken"] = if (($st.bridges.rules | Where-Object { $_.last.blocked }).Count -eq 0) { "PASS ($($b -join ', '))" } else { "FAIL ($($b -join ', '))" } } catch { $T["T8 Bruecken"] = "NOT_RUN" }

# T9 Heartbeat im LLM-HISTORY-LOG
$hb = Join-Path $cfg.paths.history_log "_HEARTBEAT_$($cfg.agent_id)_NEXUS-LOCALSTACK.md"
$T["T9 Heartbeat LLM-HISTORY-LOG"] = if ((Test-Path $hb) -and ((Get-Date) - (Get-Item $hb).LastWriteTime).TotalMinutes -lt 15) { "PASS" } else { "NOT_RUN/FAIL (noch kein Lauf oder G: fehlt)" }

"`n=== NEXUS Local Stack Abnahme ==="
$T.GetEnumerator() | ForEach-Object { "{0,-42} {1}" -f $_.Key, $_.Value }
$f = Join-Path $Runtime ("tests\acceptance_{0}.json" -f (Get-Date -Format "yyyyMMdd_HHmmss"))
[pscustomobject]@{ at = (Get-Date).ToString("o"); user = "$env:USERDOMAIN\$env:USERNAME"; results = $T } | ConvertTo-Json -Depth 4 | Set-Content -Encoding utf8 $f
"Ergebnis: $f"
