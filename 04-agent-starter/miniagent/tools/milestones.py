"""Tool: read the milestone plan (a CSV file), earliest due date first."""

from __future__ import annotations

import json
from pathlib import Path

from ..errors import ToolError
from ..types import ToolSpec
from .csv_rows import read_csv_rows

STATUS_CHOICES = ("any", "attention", "done", "on_track", "at_risk", "late")
_ATTENTION = {"at_risk", "late"}
_COLUMNS = ("id", "name", "due", "status")


def make_tool(csv_path: Path) -> ToolSpec:
    """Build the read_milestones tool, reading from `csv_path`."""

    def run(status: str = "any") -> str:
        if status not in STATUS_CHOICES:
            raise ToolError(f"status must be one of: {', '.join(STATUS_CHOICES)}.")

        milestones = [m for m in read_csv_rows(csv_path, _COLUMNS) if _status_matches(m["status"], status)]
        milestones.sort(key=lambda m: (m["due"], m["id"]))
        return json.dumps(milestones)

    return ToolSpec(
        name="read_milestones",
        description=(
            "Read the milestone plan. Returns a JSON list with id, name, due date (YYYY-MM-DD) and status "
            "(done, on_track, at_risk or late), earliest due date first."
        ),
        parameters={
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": list(STATUS_CHOICES),
                    "description": "Which milestones to return. 'attention' means at_risk or late. Default 'any'.",
                }
            },
        },
        run=run,
    )


def _status_matches(milestone_status: str, wanted: str) -> bool:
    if wanted == "any":
        return True
    if wanted == "attention":
        return milestone_status in _ATTENTION
    return milestone_status == wanted
