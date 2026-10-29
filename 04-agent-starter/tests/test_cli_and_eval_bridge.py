import json
import subprocess
import sys
from pathlib import Path

import pytest

from miniagent.cli import main

ROOT = Path(__file__).resolve().parent.parent
TASK = "Draft a short status note from the risk log and milestones."


def test_run_prints_the_note_and_the_steps(capsys, tmp_path):
    code = main(["run", TASK, "--model", "mock:scripted", "--output-dir", str(tmp_path)])
    captured = capsys.readouterr()
    assert code == 0
    assert "R-001" in captured.out
    assert "step 1" in captured.err and "read_risk_log" in captured.err


def test_quiet_hides_the_steps(capsys, tmp_path):
    main(["run", TASK, "--model", "mock:scripted", "--output-dir", str(tmp_path), "--quiet"])
    assert "step 1" not in capsys.readouterr().err


def test_yes_flag_approves_saving(tmp_path):
    code = main(["run", TASK + " Save it.", "--model", "mock:scripted", "--output-dir", str(tmp_path), "--yes", "--quiet"])
    assert code == 0 and (tmp_path / "status-note.md").exists()


def test_without_yes_and_no_terminal_saving_is_refused(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": (_ for _ in ()).throw(EOFError()))
    main(["run", TASK + " Save it.", "--model", "mock:scripted", "--output-dir", str(tmp_path), "--quiet"])
    assert not (tmp_path / "status-note.md").exists()
    assert "could not save" in capsys.readouterr().out.lower()


def test_typing_y_approves_saving(tmp_path, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "y")
    main(["run", TASK + " Save it.", "--model", "mock:scripted", "--output-dir", str(tmp_path), "--quiet"])
    assert (tmp_path / "status-note.md").exists()


def test_trace_file_holds_the_full_run(tmp_path):
    trace_path = tmp_path / "trace.json"
    main(["run", TASK, "--model", "mock:scripted", "--output-dir", str(tmp_path), "--trace", str(trace_path), "--quiet"])
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    assert trace["stop_reason"] == "finished"
    assert [r["tool"] for r in trace["steps"][0]["tool_results"]] == ["read_risk_log", "read_milestones"]


def test_max_steps_limit_returns_exit_code_1(tmp_path, capsys):
    assert main(["run", TASK, "--model", "mock:scripted", "--output-dir", str(tmp_path), "--max-steps", "1", "--quiet"]) == 1
    assert "limit" in capsys.readouterr().err


def test_bad_model_spec_returns_exit_code_2(capsys):
    assert main(["run", TASK, "--model", "nonsense"]) == 2
    assert "provider:model" in capsys.readouterr().err


def test_tools_command_lists_all_three(capsys):
    assert main(["tools"]) == 0
    out = capsys.readouterr().out
    assert "read_risk_log" in out and "save_note  [needs approval]" in out


# ---- the bridge to 02-ai-eval-toolkit -----------------------------------------------------------------


@pytest.mark.skipif(not (ROOT.parent / "02-ai-eval-toolkit").is_dir(), reason="02-ai-eval-toolkit is not next to this folder")
def test_eval_bridge_runs_the_agent_through_the_toolkit(tmp_path):
    pytest.importorskip("yaml")
    completed = subprocess.run(
        [sys.executable, str(ROOT / "evals" / "run_agent_eval.py"), "--model", "mock:scripted", "--judge", "mock:judge", "--out", str(tmp_path)],
        capture_output=True, text=True, timeout=120,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "note-uses-the-data" in completed.stdout
    assert (tmp_path / "report.html").exists()
