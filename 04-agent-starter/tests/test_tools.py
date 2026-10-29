import json

import pytest

from miniagent.errors import ToolError


def run(tool_by_name, name, **arguments):
    return tool_by_name[name].run(**arguments)


# ---- read_risk_log ---------------------------------------------------------------


def test_risks_come_back_highest_score_first(tool_by_name):
    risks = json.loads(run(tool_by_name, "read_risk_log"))
    scores = [risk["score"] for risk in risks]
    assert scores == sorted(scores, reverse=True)
    assert risks[0]["id"] == "R-001" and risks[0]["score"] == 20  # likelihood 4 x impact 5


def test_default_returns_only_active_risks(tool_by_name):
    ids = {risk["id"] for risk in json.loads(run(tool_by_name, "read_risk_log"))}
    assert "R-006" not in ids  # closed
    assert "R-002" in ids  # mitigating still counts as active


def test_status_and_min_score_filters(tool_by_name):
    closed = json.loads(run(tool_by_name, "read_risk_log", status="closed"))
    assert [risk["id"] for risk in closed] == ["R-006"]

    serious = json.loads(run(tool_by_name, "read_risk_log", min_score=15))
    assert {risk["id"] for risk in serious} == {"R-001", "R-002"}


def test_min_score_given_as_text_is_accepted(tool_by_name):
    assert json.loads(run(tool_by_name, "read_risk_log", min_score="15"))  # small models often send "15"


@pytest.mark.parametrize(
    "arguments, message",
    [
        ({"status": "stale"}, "status must be one of"),
        ({"min_score": 99}, "between 1 and 25"),
        ({"min_score": "high"}, "whole number"),
    ],
)
def test_bad_arguments_give_advice_the_model_can_act_on(tool_by_name, arguments, message):
    with pytest.raises(ToolError, match=message):
        run(tool_by_name, "read_risk_log", **arguments)


# ---- read_milestones -----------------------------------------------------------------


def test_milestones_are_in_date_order(tool_by_name):
    dates = [m["due"] for m in json.loads(run(tool_by_name, "read_milestones"))]
    assert dates == sorted(dates)


def test_attention_filter_returns_late_and_at_risk(tool_by_name):
    names = {m["name"] for m in json.loads(run(tool_by_name, "read_milestones", status="attention"))}
    assert names == {"Test environment ready", "Data migration dry run 2"}


# ---- save_note --------------------------------------------------------------------------


def test_save_note_writes_inside_the_output_folder(tool_by_name, output_dir):
    message = run(tool_by_name, "save_note", filename="status-note.md", content="hello")
    assert (output_dir / "status-note.md").read_text(encoding="utf-8") == "hello"
    assert "status-note.md" in message


@pytest.mark.parametrize(
    "filename",
    ["../escape.md", "sub/dir.md", "/etc/passwd.md", "notes.txt", ".hidden.md", "", "a\\b.md"],
)
def test_save_note_refuses_unsafe_names(tool_by_name, output_dir, filename):
    with pytest.raises(ToolError, match="filename"):
        run(tool_by_name, "save_note", filename=filename, content="x")
    assert not output_dir.exists() or not any(output_dir.iterdir())


def test_save_note_refuses_very_long_notes(tool_by_name):
    with pytest.raises(ToolError, match="too long"):
        run(tool_by_name, "save_note", filename="big.md", content="x" * 6000)


def test_only_save_note_needs_approval(tools):
    assert {tool.name for tool in tools if tool.needs_approval} == {"save_note"}


def test_missing_data_file_is_a_clear_tool_error(tmp_path, output_dir):
    from miniagent.tools import build_tools

    empty_tools = {t.name: t for t in build_tools(tmp_path, output_dir)}
    with pytest.raises(ToolError, match="not found"):
        empty_tools["read_risk_log"].run()
