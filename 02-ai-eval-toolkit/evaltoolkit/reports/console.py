"""Plain-text report for the terminal."""

from __future__ import annotations

from ..types import SuiteResult
from .summary import case_ids, failure_lines, lookup, status_label, summarize


def render_console(results: list[SuiteResult]) -> str:
    sections = [
        _header(results),
        _comparison_table(results),
        _model_summaries(results),
        _failures(results),
    ]
    return "\n\n".join(section for section in sections if section) + "\n"


def _header(results: list[SuiteResult]) -> str:
    return f"Suite: {results[0].suite_name}  ({len(results[0].cases)} cases, {len(results)} model(s))"


def _comparison_table(results: list[SuiteResult]) -> str:
    models = [r.model for r in results]
    by_model = lookup(results)

    rows = [["case", *models]]
    for case_id in case_ids(results):
        rows.append([case_id, *(status_label(by_model[m][case_id]) for m in models)])
    return _format_table(rows)


def _format_table(rows: list[list[str]]) -> str:
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    lines = []
    for index, row in enumerate(rows):
        lines.append("  ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip())
        if index == 0:
            lines.append("  ".join("-" * width for width in widths))
    return "\n".join(lines)


def _model_summaries(results: list[SuiteResult]) -> str:
    lines = ["Summary"]
    for result in results:
        s = summarize(result)
        lines.append(
            f"  {s.model}: {s.passed}/{s.total} passed ({s.pass_rate:.0%}), "
            f"avg score {s.avg_score:.2f}, avg latency {s.avg_latency_s:.2f}s"
        )
    return "\n".join(lines)


def _failures(results: list[SuiteResult]) -> str:
    lines = []
    for result in results:
        for case_result in result.cases:
            reasons = failure_lines(case_result)
            if reasons:
                lines.append(f"  [{result.model}] {case_result.case.id}")
                lines.extend(f"      - {reason}" for reason in reasons)
    return "Failures\n" + "\n".join(lines) if lines else ""
