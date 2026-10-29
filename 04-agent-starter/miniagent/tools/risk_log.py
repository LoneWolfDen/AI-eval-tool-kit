"""Tool: read the risk log (a CSV file) and return risks ranked by score."""

from __future__ import annotations

import json
from pathlib import Path

from ..errors import ToolError
from ..types import ToolSpec
from .csv_rows import read_csv_rows

STATUS_CHOICES = ("active", "open", "mitigating", "closed", "any")
_ACTIVE = {"open", "mitigating"}
_COLUMNS = ("id", "title", "likelihood", "impact", "status", "owner", "mitigation", "due")


def make_tool(csv_path: Path) -> ToolSpec:
    """Build the read_risk_log tool, reading from `csv_path`."""

    def run(status: str = "active", min_score: int = 1) -> str:
        if status not in STATUS_CHOICES:
            raise ToolError(f"status must be one of: {', '.join(STATUS_CHOICES)}.")
        min_score = _as_whole_number(min_score, "min_score")
        if not 1 <= min_score <= 25:
            raise ToolError("min_score must be between 1 and 25.")

        risks = [r for r in read_risks(csv_path) if _status_matches(r["status"], status) and r["score"] >= min_score]
        risks.sort(key=lambda r: (-r["score"], r["id"]))
        return json.dumps(risks)

    return ToolSpec(
        name="read_risk_log",
        description=(
            "Read the project risk log. Returns a JSON list of risks, highest score first. "
            "Each risk has id, title, likelihood (1-5), impact (1-5), score (likelihood x impact), "
            "status, owner, mitigation and due date."
        ),
        parameters={
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": list(STATUS_CHOICES),
                    "description": "Which risks to return. 'active' means open or mitigating. Default 'active'.",
                },
                "min_score": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 25,
                    "description": "Only return risks with at least this score. Default 1.",
                },
            },
        },
        run=run,
    )


def read_risks(csv_path: Path) -> list[dict]:
    """Load every risk from the CSV file, adding the calculated score."""
    risks = []
    for row in read_csv_rows(csv_path, _COLUMNS):
        likelihood = _as_whole_number(row["likelihood"], f"likelihood for {row['id']}")
        impact = _as_whole_number(row["impact"], f"impact for {row['id']}")
        risks.append({**row, "likelihood": likelihood, "impact": impact, "score": likelihood * impact})
    return risks


def _status_matches(risk_status: str, wanted: str) -> bool:
    if wanted == "any":
        return True
    if wanted == "active":
        return risk_status in _ACTIVE
    return risk_status == wanted


def _as_whole_number(value: object, label: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ToolError(f"{label} must be a whole number, got {value!r}.") from None

