"""Markdown report, handy for pasting into docs, wikis or pull requests."""

from __future__ import annotations

from ..types import SuiteResult
from .summary import case_ids, failure_lines, lookup, status_label, summarize

_ICONS = {"PASS": "✅ PASS", "FAIL": "❌ FAIL", "ERROR": "⚠️ ERROR"}


def render_markdown(results: list[SuiteResult]) -> str:
    parts = [
        f"# Evaluation report: {results[0].suite_name}",
        _summary_table(results),
        _tag_table(results),
        _matrix(results),
        _failure_details(results),
    ]
    return "\n\n".join(part for part in parts if part) + "\n"


def _table(header: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def _summary_table(results: list[SuiteResult]) -> str:
    rows = []
    for result in results:
        s = summarize(result)
        rows.append(
            [s.model, f"{s.passed}/{s.total} ({s.pass_rate:.0%})", f"{s.avg_score:.2f}", f"{s.avg_latency_s:.2f}s", str(s.errors)]
        )
    header = ["Model", "Passed", "Avg score", "Avg latency", "Errors"]
    return "## Summary\n\n" + _table(header, rows)


def _tag_table(results: list[SuiteResult]) -> str:
    summaries = [summarize(r) for r in results]
    tags = sorted({tag for s in summaries for tag in s.by_tag})
    if not tags:
        return ""

    rows = []
    for tag in tags:
        cells = []
        for s in summaries:
            passed, total = s.by_tag.get(tag, (0, 0))
            cells.append(f"{passed}/{total}" if total else "-")
        rows.append([tag, *cells])
    return "## By tag\n\n" + _table(["Tag", *[s.model for s in summaries]], rows)


def _matrix(results: list[SuiteResult]) -> str:
    models = [r.model for r in results]
    by_model = lookup(results)
    rows = [
        [f"`{case_id}`", *(_ICONS[status_label(by_model[m][case_id])] for m in models)]
        for case_id in case_ids(results)
    ]
    return "## Case results\n\n" + _table(["Case", *models], rows)


def _failure_details(results: list[SuiteResult]) -> str:
    lines = []
    for result in results:
        for case_result in result.cases:
            reasons = failure_lines(case_result)
            if reasons:
                lines.append(f"**{result.model}** · `{case_result.case.id}`")
                lines.extend(f"- {reason}" for reason in reasons)
                lines.append("")
    return "## Failures\n\n" + "\n".join(lines).rstrip() if lines else ""
