"""Self-contained HTML report: open the file in any browser, no server needed."""

from __future__ import annotations

from datetime import datetime
from html import escape

from ..types import CaseResult, SuiteResult
from .summary import ModelSummary, case_ids, failure_lines, lookup, status_label, summarize

_STYLE = """
:root { --bg:#ffffff; --fg:#1f2328; --muted:#656d76; --card:#f6f8fa; --line:#d0d7de;
        --pass:#1a7f37; --fail:#cf222e; --warn:#9a6700; --bar:#2da44e; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#0d1117; --fg:#e6edf3; --muted:#8d96a0; --card:#161b22; --line:#30363d;
          --pass:#3fb950; --fail:#f85149; --warn:#d29922; --bar:#3fb950; }
}
body { font: 15px/1.5 system-ui, sans-serif; background: var(--bg); color: var(--fg);
       max-width: 960px; margin: 0 auto; padding: 24px 16px; }
h1 { margin-bottom: 0; } h2 { margin-top: 32px; }
.sub { color: var(--muted); margin-top: 4px; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 14px; }
.card h3 { margin: 0 0 6px; font-size: 14px; word-break: break-all; }
.big { font-size: 32px; font-weight: 600; }
.bar { height: 8px; background: var(--line); border-radius: 4px; overflow: hidden; margin: 8px 0; }
.bar > span { display: block; height: 100%; background: var(--bar); }
.meta { color: var(--muted); font-size: 13px; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid var(--line); padding: 6px 10px; text-align: left; }
th { background: var(--card); }
.PASS { color: var(--pass); font-weight: 600; }
.FAIL { color: var(--fail); font-weight: 600; }
.ERROR { color: var(--warn); font-weight: 600; }
details { border: 1px solid var(--line); border-radius: 8px; margin: 8px 0; padding: 8px 12px; }
summary { cursor: pointer; font-weight: 600; }
pre { background: var(--card); padding: 8px; border-radius: 6px; white-space: pre-wrap; margin: 4px 0; }
ul { margin: 4px 0 10px; padding-left: 20px; }
"""


def render_html(results: list[SuiteResult]) -> str:
    summaries = [summarize(r) for r in results]
    title = f"Evaluation report: {results[0].suite_name}"
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    body = "\n".join(
        [
            f"<h1>{escape(title)}</h1>",
            f'<p class="sub">Generated {stamp} · {len(results[0].cases)} cases · {len(results)} model(s)</p>',
            _cards(summaries),
            "<h2>Case results</h2>",
            _matrix(results),
            _tag_section(summaries),
            "<h2>Details</h2>",
            _details(results),
        ]
    )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{escape(title)}</title><style>{_STYLE}</style></head><body>{body}</body></html>\n"
    )


def _cards(summaries: list[ModelSummary]) -> str:
    cards = []
    for s in summaries:
        cards.append(
            '<div class="card">'
            f"<h3>{escape(s.model)}</h3>"
            f'<div class="big">{s.pass_rate:.0%}</div>'
            f'<div class="bar"><span style="width:{s.pass_rate * 100:.0f}%"></span></div>'
            f'<div class="meta">{s.passed}/{s.total} passed · avg score {s.avg_score:.2f}<br>'
            f"avg latency {s.avg_latency_s:.2f}s · {s.errors} error(s)</div>"
            "</div>"
        )
    return f'<div class="cards">{"".join(cards)}</div>'


def _status_cell(case_result: CaseResult) -> str:
    label = status_label(case_result)
    return f'<td class="{label}">{label}</td>'


def _matrix(results: list[SuiteResult]) -> str:
    by_model = lookup(results)
    head = "".join(f"<th>{escape(r.model)}</th>" for r in results)
    rows = []
    for case_id in case_ids(results):
        cells = "".join(_status_cell(by_model[r.model][case_id]) for r in results)
        rows.append(f"<tr><td><code>{escape(case_id)}</code></td>{cells}</tr>")
    return f"<table><tr><th>Case</th>{head}</tr>{''.join(rows)}</table>"


def _tag_section(summaries: list[ModelSummary]) -> str:
    tags = sorted({tag for s in summaries for tag in s.by_tag})
    if not tags:
        return ""
    head = "".join(f"<th>{escape(s.model)}</th>" for s in summaries)
    rows = []
    for tag in tags:
        cells = []
        for s in summaries:
            passed, total = s.by_tag.get(tag, (0, 0))
            cells.append(f"<td>{passed}/{total}</td>" if total else "<td>-</td>")
        rows.append(f"<tr><td>{escape(tag)}</td>{''.join(cells)}</tr>")
    return f"<h2>By tag</h2><table><tr><th>Tag</th>{head}</tr>{''.join(rows)}</table>"


def _details(results: list[SuiteResult]) -> str:
    by_model = lookup(results)
    blocks = []
    for case_id in case_ids(results):
        first = by_model[results[0].model][case_id]
        per_model = "".join(_model_detail(r.model, by_model[r.model][case_id]) for r in results)
        blocks.append(
            f"<details><summary>{escape(case_id)}</summary>"
            f"<p><strong>Prompt</strong></p><pre>{escape(first.case.prompt)}</pre>{per_model}</details>"
        )
    return "".join(blocks)


def _model_detail(model: str, case_result: CaseResult) -> str:
    label = status_label(case_result)
    reasons = failure_lines(case_result)
    reason_html = "".join(f"<li>{escape(r)}</li>" for r in reasons)
    reason_block = f"<ul>{reason_html}</ul>" if reasons else ""
    return (
        f'<p><strong>{escape(model)}</strong> <span class="{label}">{label}</span></p>'
        f"<pre>{escape(case_result.output or '(no output)')}</pre>{reason_block}"
    )
