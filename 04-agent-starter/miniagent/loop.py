"""The agent loop: ask the model, run the tools it requests, repeat.

This file is the heart of the project. Frameworks wrap this same idea in more
features; reading it once makes them much easier to understand.
"""

from __future__ import annotations

from typing import Callable

from .errors import ToolError
from .models.base import AgentModel
from .types import (
    INVALID_ARGUMENTS_KEY,
    AgentResult,
    Message,
    Step,
    ToolCall,
    ToolResult,
    ToolSpec,
)

MAX_TOOL_OUTPUT_CHARS = 4000  # long results are cut so they cannot flood the model's context

Approver = Callable[[ToolCall], bool]
StepCallback = Callable[[Step], None]


def run_agent(
    task: str,
    model: AgentModel,
    tools: list[ToolSpec],
    system: str,
    max_steps: int = 8,
    approve: Approver | None = None,
    on_step: StepCallback | None = None,
) -> AgentResult:
    """Run the agent on `task` and return what happened.

    - `max_steps` stops a model that keeps asking for tools forever.
    - `approve(call)` decides whether a tool marked needs_approval may run.
      With no approver, those tools are refused.
    - `on_step(step)` is called after every step, e.g. to print progress.
    """
    tools_by_name = {tool.name: tool for tool in tools}
    messages = [Message(role="user", content=task)]
    steps: list[Step] = []

    for number in range(1, max_steps + 1):
        turn = model.next_turn(system, messages, tools)
        messages.append(Message(role="assistant", content=turn.text, tool_calls=turn.tool_calls))

        results = tuple(_execute(call, tools_by_name, approve) for call in turn.tool_calls)
        for result in results:
            messages.append(
                Message(role="tool", content=result.output, tool_call_id=result.call.id, is_error=result.is_error)
            )

        step = Step(number=number, text=turn.text, results=results)
        steps.append(step)
        if on_step:
            on_step(step)

        if not turn.tool_calls:  # the model answered instead of asking for a tool
            return AgentResult(final_text=turn.text, steps=steps, stop_reason="finished")

    return AgentResult(final_text="", steps=steps, stop_reason="max_steps")


def _execute(call: ToolCall, tools_by_name: dict[str, ToolSpec], approve: Approver | None) -> ToolResult:
    """Run one requested tool. Problems become error text for the model, not crashes."""
    tool = tools_by_name.get(call.name)
    if tool is None:
        known = ", ".join(sorted(tools_by_name))
        return _error(call, f"Unknown tool '{call.name}'. Available tools: {known}.")

    if INVALID_ARGUMENTS_KEY in call.arguments:
        return _error(call, "The arguments were not valid JSON. Send a JSON object that matches the tool's schema.")

    if tool.needs_approval and not (approve and approve(call)):
        return _error(call, "The user did not approve this action, so it was not done. Do not retry. Tell the user.")

    try:
        output = tool.run(**call.arguments)
    except ToolError as exc:
        return _error(call, str(exc))
    except TypeError as exc:  # wrong or missing argument names
        return _error(call, f"Bad arguments for '{call.name}': {exc}")
    except Exception as exc:  # keep the agent alive; the model gets to see what went wrong
        return _error(call, f"'{call.name}' failed unexpectedly: {exc}")

    return ToolResult(call=call, output=_truncate(output))


def _error(call: ToolCall, message: str) -> ToolResult:
    return ToolResult(call=call, output=message, is_error=True)


def _truncate(text: str) -> str:
    if len(text) <= MAX_TOOL_OUTPUT_CHARS:
        return text
    return text[:MAX_TOOL_OUTPUT_CHARS] + "\n[output cut: too long]"
