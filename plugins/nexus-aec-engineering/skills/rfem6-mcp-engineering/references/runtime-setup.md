# Version-aware local RFEM setup
Verified 2026-10-19 against official sources:
- https://apidocs.dlubal.com/installation_mcp.html
- https://apidocs.dlubal.com/access_control.html

The current guide applies to MCP 1.0.17 and newer: client-launched local STDIO;
no MCP HTTP port or bearer token in this transport. Dlubal API authentication
still requires an API key. Python 3.11–3.13 is documented; 3.14 is unsupported.
Match API minor to application minor, e.g. RFEM 6.15 and dlubal.api 2.15.*.
Record exact installed versions; 1.0.17 is a guide boundary, not a latest-version claim.

Windows cmd example ONLY after checking installed RFEM minor:
```bat
py -3.12 -m venv %USERPROFILE%\dlubal-mcp
%USERPROFILE%\dlubal-mcp\Scripts\python.exe -m pip install dlubal-mcp "dlubal.api==2.15.*"
%USERPROFILE%\dlubal-mcp\Scripts\python.exe -m pip check
%USERPROFILE%\dlubal-mcp\Scripts\python.exe -m dlubal_mcp --help
```
Configure the client command to the actual environment Python and arguments
`-m dlubal_mcp --transport stdio`. Set `DLUBAL_MCP_ALLOW_SCRIPTS=false` for
only typed tools. This removes free-form script tools, NOT all mutating tools.
Discover/limit actual typed write tools separately.

RFEM gRPC documented default: 127.0.0.1:9000. Verify the active setting.
Overrides: RFEM_URL / RFEM_API_PORT. Key store:
%LOCALAPPDATA%\Dlubal\api\config.ini, section [api_keys], documented default
entry `default`, not `default_key`. Prefer named key references; never print keys.

HTTP 7130/bearer instructions in project text are legacy version-specific
claims. For an existing HTTP deployment verify its installed CLI/auth before
use. Do not disable auth or expose it externally. A cloud skill cannot reach a
private Windows STDIO process without a separately authorized bridge/connector.
Dlubal API requests, including local MCP, count toward subscription usage.
