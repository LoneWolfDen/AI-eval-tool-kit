"""Show a run on screen and save it to a file, so you can see how the agent behaved."""

from __future__ import annotations

import json
from pathlib import Path

from .types import AgentResult, Step

_PREVIEW_CHARS = 160


def format_step(step: Step) -> str:
    """A short readable view of one step, for the terminal."""
    lines = [f"step {step.number}"]
    if step.text.strip():
        lines.append(f"  model: {_preview(step.text)}")
    for result in step.results:
        marker = "ERROR" if result.is_error else "ok"
        lines.append(f"  tool:  {result.call.name}({_format_arguments(result.call.arguments)}) -> [{marker}] {_preview(result.output)}")
    return "\n".join(lines)


def save_trace(result: AgentResult, path: str | Path) -> None:
    """Write the full run as JSON: nothing is shortened, so it can be reviewed or tested later."""
    data = {
        "stop_reason": result.stop_reason,
        "final_text": result.final_text,
        "steps": [
            {
                "number": step.number,
                "text": step.text,
                "tool_results": [
                    {
                        "tool": r.call.name,
                        "arguments": r.call.arguments,
                        "output": r.output,
                        "is_error": r.is_error,
                    }
                    for r in step.results
                ],
            }
            for step in result.steps
        ],
    }
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _format_arguments(arguments: dict) -> str:
    return ", ".join(f"{key}={_preview(json.dumps(value, ensure_ascii=False), 40)}" for key, value in arguments.items())


def _preview(text: str, limit: int = _PREVIEW_CHARS) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[: limit - 1] + "…"
