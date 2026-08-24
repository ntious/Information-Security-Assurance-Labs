from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, REPOSITORY_ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_restore_rules_passes_malicious_filename_as_data(tmp_path):
    helper = _load_module(
        "firewall_lab_helper", "labs/firewall_lab/basic/firewall_lab_helper.py"
    )
    source = tmp_path / "rules;touch SHOULD_NOT_RUN.backup"
    source.write_text("*filter\nCOMMIT\n", encoding="utf-8")
    calls = []

    def fake_run(args, **kwargs):
        calls.append((args, kwargs))
        return SimpleNamespace(returncode=0, stdout="", stderr=b"")

    with patch.object(helper.subprocess, "run", side_effect=fake_run):
        helper.restore_rules(str(source), dry=False)

    assert calls[0][0] == ["sudo", "tee", "/etc/ufw/user.rules"]
    assert calls[0][1]["stdin"].name == str(source.resolve())
    assert all("sh" not in args[:2] for args, _ in calls)


def test_http_server_defaults_to_loopback_and_isolated_root(tmp_path):
    toolkit = _load_module(
        "firewall_lab_toolkit", "labs/firewall_lab/firewall_lab_toolkit.py"
    )
    doc_root = tmp_path / "www"
    process = SimpleNamespace(pid=12345)

    with (
        patch.object(toolkit, "_prepare_test_content", return_value=doc_root),
        patch.object(toolkit, "_choose_bind_address", return_value="127.0.0.1"),
        patch.object(toolkit, "_write_pid"),
        patch.object(toolkit.subprocess, "Popen", return_value=process) as popen,
        patch("builtins.input", return_value="8000"),
    ):
        toolkit.start_http_server()

    args = popen.call_args.args[0]
    assert args[args.index("--bind") + 1] == "127.0.0.1"
    assert Path(args[args.index("--directory") + 1]) == doc_root
    assert toolkit.KEY_FILE.parent != doc_root


def test_external_bind_requires_exact_opt_in():
    toolkit = _load_module(
        "firewall_lab_toolkit_bind", "labs/firewall_lab/firewall_lab_toolkit.py"
    )
    with patch("builtins.input", return_value=""):
        assert toolkit._choose_bind_address() == "127.0.0.1"
    with patch("builtins.input", return_value="EXPOSE"):
        assert toolkit._choose_bind_address() == "0.0.0.0"
