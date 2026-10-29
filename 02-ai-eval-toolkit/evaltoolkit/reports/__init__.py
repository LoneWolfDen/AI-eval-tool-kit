"""Report writers. Each `render_*` function takes results and returns text."""

from __future__ import annotations

from pathlib import Path

from ..types import SuiteResult
from .console import render_console
from .html_report import render_html
from .json_report import render_json
from .markdown import render_markdown

# file name -> function that produces its content
FILE_REPORTS = {
    "report.md": render_markdown,
    "report.html": render_html,
    "results.json": render_json,
}


def write_reports(results: list[SuiteResult], out_dir: str | Path) -> list[Path]:
    """Write every file report into `out_dir` and return the paths."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for file_name, render in FILE_REPORTS.items():
        path = out_dir / file_name
        path.write_text(render(results), encoding="utf-8")
        written.append(path)
    return written


__all__ = ["render_console", "render_markdown", "render_html", "render_json", "write_reports"]
