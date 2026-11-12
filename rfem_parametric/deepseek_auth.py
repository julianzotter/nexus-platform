"""DeepSeek bearer authentication check: GET /models, no paid inference."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


def check_models() -> dict[str, object]:
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        return {"status": "BLOCKED_NO_PROCESS_KEY", "endpoint": "/models"}
    req = urllib.request.Request(
        "https://api.deepseek.com/models",
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            payload = json.load(response)
            return {"status": "AUTH_OK" if response.status == 200 else "UNEXPECTED_STATUS",
                    "http_status": response.status,
                    "model_ids": sorted(str(m.get("id")) for m in payload.get("data", []) if m.get("id"))}
    except urllib.error.HTTPError as exc:
        return {"status": "AUTH_FAILED" if exc.code == 401 else "HTTP_FAILURE",
                "http_status": exc.code}
    except (urllib.error.URLError, TimeoutError, ValueError):
        return {"status": "NETWORK_OR_RESPONSE_FAILURE"}


if __name__ == "__main__":
    print(json.dumps(check_models(), indent=2, ensure_ascii=False))
