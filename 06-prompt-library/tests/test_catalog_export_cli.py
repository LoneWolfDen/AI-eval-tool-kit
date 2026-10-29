import yaml

from promptlib.catalog import render_catalog
from promptlib.cli import main
from promptlib.export_suite import build_suite, dump_suite
from promptlib.model import PLACEHOLDER


def test_catalog_lists_every_prompt_with_a_link(prompts):
    text = render_catalog(prompts)
    for prompt in prompts:
        assert f"(prompts/{prompt.id}.md)" in text


def test_suite_has_one_filled_case_per_prompt(prompts):
    suite = build_suite(prompts)
    assert [case["id"] for case in suite["cases"]] == [p.id for p in prompts]
    for case in suite["cases"]:
        assert not PLACEHOLDER.search(case["prompt"])
        assert case["checks"][0]["type"] == "rubric"


def test_dumped_suite_round_trips_through_yaml(prompts):
    suite = build_suite(prompts)
    assert yaml.safe_load(dump_suite(suite)) == suite


def test_cli_list_and_show(capsys):
    assert main(["list", "--category", "risk"]) == 0
    out = capsys.readouterr().out
    assert "risk-log-entry" in out and "weekly-status-report" not in out

    assert main(["show", "escalation-message"]) == 0
    assert "Variables:" in capsys.readouterr().out


def test_cli_fill_with_example_and_overrides(capsys):
    assert main(["fill", "escalation-message", "--example", "--var", "deadline=Monday"]) == 0
    out = capsys.readouterr().out
    assert "Needed by: Monday" in out and "{{" not in out


def test_cli_fill_reads_a_value_from_a_file(tmp_path, capsys):
    notes = tmp_path / "notes.txt"
    notes.write_text("Decided to ship on Friday.", encoding="utf-8")
    assert main(["fill", "meeting-actions", "--var", "meeting_date=1 Feb", "--file", f"notes={notes}"]) == 0
    assert "Decided to ship on Friday." in capsys.readouterr().out


def test_cli_reports_errors_with_exit_code_2(capsys):
    assert main(["fill", "escalation-message"]) == 2  # required values missing
    assert "needs values" in capsys.readouterr().err
    assert main(["show", "no-such-prompt"]) == 2
    assert main(["fill", "escalation-message", "--var", "oops"]) == 2


def test_cli_writes_catalog_and_suite(tmp_path):
    assert main(["catalog", "--out", str(tmp_path / "CATALOG.md")]) == 0
    assert main(["export-suite", "--out", str(tmp_path / "suite.yaml")]) == 0
    assert (tmp_path / "CATALOG.md").stat().st_size > 0
    assert len(yaml.safe_load((tmp_path / "suite.yaml").read_text(encoding="utf-8"))["cases"]) == 12
