import json
from pathlib import Path
from tempfile import TemporaryDirectory
from tools.artifact_registry_gate import validate_record, validate_registry

VALID = {"artifact_id": "gdrive:abc", "provider_file_id": "abc",
         "name": "a.md", "canonical_uri": "https://drive.google.com/file/d/abc/view",
         "version": "v004", "provenance": {"source": "test"},
         "verification_status": "REVIEW_PENDING", "registration_status": "REGISTERED",
         "registered_at": "2026-11-01T08:00:00+01:00", "owner": "ID01",
         "ticket_id": None}

def test_valid_record():
    assert validate_record(VALID) == []

def test_missing_required_fields():
    assert validate_record({})

def test_bad_url():
    assert validate_record({**VALID, "canonical_uri": "http://example.org"})

def test_wrong_provider_id():
    assert validate_record({**VALID, "provider_file_id": "wrong"})

def test_registered():
    with TemporaryDirectory() as d:
        path = Path(d) / "registry.jsonl"
        path.write_text(json.dumps(VALID) + "\n", encoding="utf-8")
        assert validate_registry(path, "gdrive:abc") == []

def test_unknown_artifact_blocked():
    with TemporaryDirectory() as d:
        path = Path(d) / "registry.jsonl"
        path.write_text(json.dumps(VALID) + "\n", encoding="utf-8")
        assert validate_registry(path, "gdrive:missing")

def test_invalid_json_blocked():
    with TemporaryDirectory() as d:
        path = Path(d) / "registry.jsonl"
        path.write_text("{bad json\n", encoding="utf-8")
        assert validate_registry(path, "gdrive:abc")

def test_unregistered_latest_version_blocked():
    with TemporaryDirectory() as d:
        path = Path(d) / "registry.jsonl"
        path.write_text(json.dumps(VALID) + "\n" +
                        json.dumps({**VALID, "registration_status": "PENDING"}) + "\n",
                        encoding="utf-8")
        assert validate_registry(path, "gdrive:abc")

def test_missing_registry_blocked():
    assert validate_registry(Path("/nonexistent/nexus-registry.jsonl"), "gdrive:abc")
