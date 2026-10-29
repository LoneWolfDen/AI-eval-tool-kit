"""Tool: save a note to disk. This one has a side effect, so it needs approval.

Two safeguards are worth copying into any tool that writes files:
  1. The name is checked against a strict pattern, so the model cannot write
     outside the output folder (no "../" tricks, no sub-folders).
  2. The tool is marked needs_approval, so a person confirms each save.
"""

from __future__ import annotations

import re
from pathlib import Path

from ..errors import ToolError
from ..types import ToolSpec

MAX_NOTE_CHARS = 5000
_SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\.md")


def make_tool(output_dir: Path) -> ToolSpec:
    """Build the save_note tool, writing only inside `output_dir`."""

    def run(filename: str, content: str) -> str:
        path = _safe_path(output_dir, filename)
        if len(content) > MAX_NOTE_CHARS:
            raise ToolError(f"The note is too long ({len(content)} characters). The limit is {MAX_NOTE_CHARS}.")

        output_dir.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Saved {path.name} ({len(content)} characters)."

    return ToolSpec(
        name="save_note",
        description="Save a Markdown note to the output folder. Needs the user's approval for each save.",
        parameters={
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "File name ending in .md, for example status-note.md. No folders."},
                "content": {"type": "string", "description": "The note text."},
            },
            "required": ["filename", "content"],
        },
        run=run,
        needs_approval=True,
    )


def _safe_path(output_dir: Path, filename: str) -> Path:
    if not isinstance(filename, str) or not _SAFE_NAME.fullmatch(filename):
        raise ToolError("filename must be a plain name ending in .md, using letters, numbers, dots, dashes or underscores.")

    path = (output_dir / filename).resolve()
    if path.parent != output_dir.resolve():  # belt and braces: never leave the output folder
        raise ToolError("filename must not point outside the output folder.")
    return path
