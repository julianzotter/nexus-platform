from copy import deepcopy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from nexus_orch.geometry import GeometryError, generate, validate_topology
from nexus_orch.geometry_run import run, load_spec
from nexus_orch import dsh, rfem5
from nexus_orch.providers import Provider, ProviderError

FIXTURE = Path(__file__).parents[1] / "examples/synthetic-frame.json"

@pytest.fixture
def spec():
    return load_spec(FIXTURE)


def test_grid_topology_and_signs(spec):
    model = generate(spec)
    assert len(model["nodes"]) == 18
    assert len(model["members"]) == len(model["lines"]) == 26
    assert {n["x_m"] for n in model["nodes"]} == {0, 4, 9}
    assert {n["z_m"] for n in model["nodes"]} == {0, -3, -6}
    assert model["nodes"][-1] == {"no": 18, "x_m": 9, "y_m": 3, "z_m": -6}
    assert generate(spec) == model


@pytest.mark.parametrize("bad", [True, 0, -1, float("nan"), float("inf"), "4", 1001, 10**1000])
def test_invalid_dimensions_rejected(spec, bad):
    spec["bays_x_m"] = [bad]
    with pytest.raises(GeometryError): generate(spec)


def test_units_and_project_evidence(spec):
    spec["units"] = "mm"
    with pytest.raises(GeometryError): generate(spec)
    spec["units"], spec["scope"] = "m", "PROJECT"
    with pytest.raises(GeometryError): generate(spec)


def test_unknown_fields_rejected(spec):
    spec["calculate"] = True
    with pytest.raises(GeometryError): generate(spec)


def test_duplicate_edge_and_bad_member(spec):
    model = generate(spec)
    model["lines"].append({**model["lines"][0], "no": 99})
    with pytest.raises(GeometryError): validate_topology(model)
    model = generate(spec)
    model["members"][0]["line"] = 999
    with pytest.raises(GeometryError): validate_topology(model)


def test_unique_runs_and_byte_hashes(spec, tmp_path):
    a, b = run(spec, tmp_path), run(spec, tmp_path)
    assert a["run_dir"] != b["run_dir"]
    folder = Path(a["run_dir"])
    for name, sha in json.loads((folder / "hashes.json").read_text()).items():
        assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == sha
    assert a["calculation"] == "NOT_RUN"


def test_failure_keeps_partial_model_identity(spec, tmp_path, monkeypatch):
    from nexus_orch import rfem6
    def fail(model, receipt, **kwargs):
        receipt.update(status="CREATED_PARTIAL_UNSAVED", model_id="test-model")
        raise RuntimeError("SECRET must not appear in receipt")
    monkeypatch.setattr(rfem6, "write_new", fail)
    r = run(spec, tmp_path, target="rfem6-new")
    assert r["status"] == "FAILED_OR_BLOCKED" and r["model_id"] == "test-model"
    assert "SECRET" not in json.dumps(r)


def test_sdk_real_roundtrip(spec):
    pytest.importorskip("dlubal.api")
    from nexus_orch.rfem6 import sdk_check
    r = sdk_check(generate(spec))
    assert r["roundtrip"] == "PASS" and r["protobuf_objects"] == 73


def test_dsh_launch_and_final_event(monkeypatch, tmp_path):
    monkeypatch.setenv("NEXUS_DSH_WORKDIR", str(tmp_path))
    monkeypatch.setattr(dsh.shutil, "which", lambda name: "/dsh")
    seen = {}
    def fake(command, **kwargs):
        seen.update(command=command, **kwargs)
        return SimpleNamespace(returncode=0, stdout=json.dumps({"type": "final", "reason": {"kind": "completed"}, "text": "{}", "sessionId": "s"}))
    monkeypatch.setattr(dsh.subprocess, "run", fake)
    result = Provider("harness", {"kind": "dsh"}).complete("Prompt")
    assert result["text"] == "{}" and result["model"] is None
    assert seen["shell"] is False and seen["input"] == "Prompt"
    assert "read-only" in seen["command"] and "never" in seen["command"]
    assert seen["command"][-1] == "-"


@pytest.mark.parametrize("event", [{"type": "final", "reason": None, "text": "bad"},
    {"type": "final", "reason": {"kind": "error"}, "text": "bad"}, {"type": "error"}])
def test_dsh_failed_terminal_rejected(monkeypatch, tmp_path, event):
    monkeypatch.setenv("NEXUS_DSH_WORKDIR", str(tmp_path))
    monkeypatch.setattr(dsh.shutil, "which", lambda _: "/dsh")
    monkeypatch.setattr(dsh.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0, stdout=json.dumps(event)))
    with pytest.raises(ProviderError): dsh.complete({}, "Prompt")


def test_no_dsh_executable_blocks(monkeypatch):
    monkeypatch.setattr(dsh.shutil, "which", lambda _: None)
    with pytest.raises(ProviderError): dsh.complete({}, "Prompt")


def test_rfem5_wrong_path_and_unlock(monkeypatch, tmp_path):
    app = Mock()
    app.GetActiveModel.return_value.GetPath.return_value = str(tmp_path / "source.rf5")
    monkeypatch.setattr(rfem5, "connect", lambda _: (app, object()))
    with pytest.raises(RuntimeError): rfem5.preflight(tmp_path / "rfem.dll", tmp_path / "copy.rf5")
    app.UnlockLicense.assert_called_once()
    app.GetActiveModel.return_value.GetModelData.assert_not_called()


def test_rfem5_nonempty_never_writes(spec, monkeypatch, tmp_path):
    app, model = Mock(), Mock()
    monkeypatch.setattr(rfem5, "connect", lambda _: (app, object()))
    monkeypatch.setattr(rfem5, "inspect", lambda *a: (model, {"counts": {"Node": 1}}))
    with pytest.raises(RuntimeError): rfem5.write_empty(tmp_path / "lib", tmp_path / "copy", generate(spec), {})
    model.GetModelData.assert_not_called()
    app.UnlockLicense.assert_called_once()


def test_duplicate_json_keys(tmp_path):
    p = tmp_path / "input.json"
    p.write_text('{"units":"m","units":"mm"}')
    with pytest.raises(ValueError): load_spec(p)


def test_cli_defaults_dry_run(tmp_path, capsys):
    from nexus_orch.cli import main
    assert main(["geometry", "--spec", str(FIXTURE), "--out", str(tmp_path)]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "DRY_RUN_PASS"


def test_dsh_available_requires_binary_and_workdir(monkeypatch):
    monkeypatch.setattr(dsh.shutil, "which", lambda _: None)
    assert not Provider("dsh", {"kind": "dsh", "env_key": None}).available()


def test_partial_checkpoint_written_before_adapter_mutation(spec, tmp_path, monkeypatch):
    from nexus_orch import rfem6
    def fake(model, receipt, *, checkpoint, **kwargs):
        receipt.update(status="CREATE_REQUESTED", model_name="unique-name")
        checkpoint()
        folder = next(tmp_path.iterdir())
        events = [json.loads(v) for v in (folder / "progress.jsonl").read_text().splitlines()]
        assert events[-1]["model_name"] == "unique-name"
        raise RuntimeError("network failure")
    monkeypatch.setattr(rfem6, "write_new", fake)
    result = run(spec, tmp_path, target="rfem6-new")
    assert result["previous_status"] == "CREATE_REQUESTED"


def test_prompt_plan_stays_dry(spec, tmp_path):
    from nexus_orch.geometry_plan import plan
    p = tmp_path / "prompt.txt"
    p.write_text("synthetic test request")
    orch = Mock()
    orch.run.return_value = {"text": json.dumps(spec), "provider": "mock", "model": "mock"}
    result = plan(p, tmp_path / "runs", orch)
    assert result["target"] == "dry-run" and result["calculation"] == "NOT_RUN"
    assert (Path(result["run_dir"]) / "proposal-origin.json").exists()
    assert orch.run.call_args[0][0] == "rfem_plan"


def test_prompt_code_is_rejected(tmp_path):
    from nexus_orch.geometry_plan import plan
    p = tmp_path / "prompt.txt"
    p.write_text("request")
    orch = Mock()
    orch.run.return_value = {"text": "import os; os.system('never execute')"}
    with pytest.raises(ValueError): plan(p, tmp_path / "out", orch)
    assert not (tmp_path / "out").exists()


def test_input_hash_domains_explicit(spec, tmp_path):
    spec["bays_x_m"] = [4, 5]
    result = run(spec, tmp_path)
    file_hash = hashlib.sha256((Path(result["run_dir"]) / "input.json").read_bytes()).hexdigest()
    assert result["input_file_sha256"] == file_hash
    assert result["normalized_spec_sha256"] != file_hash
    assert generate(spec)["normalized_spec_sha256"] == generate({**spec, "bays_x_m": [4.0, 5.0]})["normalized_spec_sha256"]


def test_rfem6_new_model_binds_every_call(spec, monkeypatch):
    pytest.importorskip("dlubal.api")
    from dlubal.api import rfem
    from nexus_orch import rfem6
    app = Mock()
    app.get_application_info.return_value = SimpleNamespace(version="6.16", full_version="6.16.test")
    app.get_model_list.return_value = SimpleNamespace(model_info=[])
    app.create_model.return_value = "new-guid"
    planned = generate(spec)
    typed = rfem6.objects(planned)
    app.get_object_list.side_effect = lambda *, objs, model_id: [o for o in typed if type(o) is type(objs[0])]
    context = Mock()
    context.__enter__ = Mock(return_value=app)
    context.__exit__ = Mock(return_value=False)
    monkeypatch.setattr(rfem, "Application", lambda **kw: context)
    receipt, events = {}, []
    rfem6.write_new(planned, receipt, checkpoint=lambda: events.append(dict(receipt)))
    assert receipt["status"] == "GEOMETRY_READBACK_PASS_UNSAVED"
    assert events[0]["status"] == "CREATE_REQUESTED" and events[1]["model_id"] == "new-guid"
    assert app.create_object_list.call_args.kwargs["model_id"] == "new-guid"
    assert app.create_object_list.call_args.kwargs["skip_invalid_attributes"] is False
    for call in app.get_object_list.call_args_list: assert call.kwargs["model_id"] == "new-guid"
    app.calculate_all.assert_not_called()
    app.save_model.assert_not_called()


def test_preflight_missing_com_inputs_clean_error(capsys):
    from nexus_orch.cli import main
    assert main(["rfem-preflight", "--target", "rfem5"]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "PREFLIGHT_BLOCKED"
