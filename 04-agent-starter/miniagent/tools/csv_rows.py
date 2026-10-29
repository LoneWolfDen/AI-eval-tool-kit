"""Shared helper for tools that read CSV files."""

from __future__ import annotations

import csv
from pathlib import Path

from ..errors import ToolError


def read_csv_rows(csv_path: Path, required_columns: tuple[str, ...]) -> list[dict]:
    """Read a CSV file into a list of dicts, checking the expected columns exist."""
    name = Path(csv_path).name
    try:
        with open(csv_path, newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            missing = [column for column in required_columns if column not in (reader.fieldnames or [])]
            if missing:
                raise ToolError(f"{name} is missing columns: {', '.join(missing)}.")
            return [dict(row) for row in reader]
    except FileNotFoundError:
        raise ToolError(f"{name} was not found.") from None
