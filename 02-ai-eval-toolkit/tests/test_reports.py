import json

import pytest

from evaltoolkit.clients.mock import MockClient
from evaltoolkit.loader import load_suite
from evaltoolkit.reports import render_console, render_html, render_json, render_markdown, write_reports
from evaltoolkit.reports.summary import summarize
from evaltoolkit.runner import run_suite


@pytest.fixture
def results(example_suite_path):
    suite = load_suite(example_suite_path)
    judge = MockClient("judge")
    return [run_suite(suite, MockClient(name), judge) for name in ("careful", "sloppy")]


def test_summary_numbers(results):
    careful, sloppy = (summarize(r) for r in results)
    assert careful.pass_rate == 1.0
    assert sloppy.passed < sloppy.total
    assert careful.by_tag["privacy"] == (2, 2)


def test_console_report_lists_models_and_failures(results):
    text = render_console(results)
    assert "mock:careful" in text and "mock:sloppy" in text
    assert "Failures" in text
    assert "injection-system-prompt" in text


def test_markdown_report_has_expected_sections(results):
    text = render_markdown(results)
    for heading in ("## Summary", "## By tag", "## Case results", "## Failures"):
        assert heading in text


def test_html_report_escapes_model_output(results):
    results[0].cases[0].output = "<script>alert('x')</script>"
    html = render_html(results)
    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html


def test_json_report_is_valid_and_complete(results):
    data = json.loads(render_json(results))
    assert [entry["model"] for entry in data] == ["mock:careful", "mock:sloppy"]
    assert len(data[0]["cases"]) == 7


def test_write_reports_creates_three_files(results, tmp_path):
    paths = write_reports(results, tmp_path / "out")
    assert sorted(p.name for p in paths) == ["report.html", "report.md", "results.json"]
    assert all(p.stat().st_size > 0 for p in paths)
