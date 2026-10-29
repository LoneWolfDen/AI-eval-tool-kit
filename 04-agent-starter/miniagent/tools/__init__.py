"""The tools the agent can use. To add one: write a make_tool() in a new file and list it here."""

from __future__ import annotations

from pathlib import Path

from ..types import ToolSpec
from . import milestones, notes, risk_log


def build_tools(data_dir: Path, output_dir: Path) -> list[ToolSpec]:
    """Create the agent's tool set: two read-only tools and one that writes."""
    return [
        risk_log.make_tool(Path(data_dir) / "risk_log.csv"),
        milestones.make_tool(Path(data_dir) / "milestones.csv"),
        notes.make_tool(Path(output_dir)),
    ]
