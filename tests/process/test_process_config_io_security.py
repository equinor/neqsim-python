import json

import pytest


def test_resolve_path_rejects_absolute(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    from neqsim.process import processTools

    with pytest.raises(ValueError):
        processTools._resolve_path_in_cwd(str(tmp_path / "x.yaml"), must_exist=False)


def test_resolve_path_rejects_traversal(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    from neqsim.process import processTools

    with pytest.raises(ValueError):
        processTools._resolve_path_in_cwd("../secrets.yaml", must_exist=False)


def test_processbuilder_from_json_reads_local_file(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    from neqsim.process.processTools import ProcessBuilder

    cfg = {"name": "Test", "equipment": []}
    (tmp_path / "process_config.json").write_text(json.dumps(cfg), encoding="utf-8")

    builder = ProcessBuilder.from_json("process_config.json")
    assert builder.get_process() is not None
