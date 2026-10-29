"""Plain data containers shared by every module.

The conversation is kept in one neutral format (Message). Each model adapter
translates it to and from its provider's format, so the loop never needs to
know which provider is in use.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

# If a model sends tool arguments that are not valid JSON, the adapter stores the
# raw text under this key, and the loop reports the problem back to the model.
INVALID_ARGUMENTS_KEY = "__invalid_arguments__"


@dataclass(frozen=True)
class ToolCall:
    """The model asking for one tool to be run."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class Message:
    """One entry in the conversation. role is "user", "assistant" or "tool"."""

    role: str
    content: str = ""
    tool_calls: tuple[ToolCall, ...] = ()  # only on assistant messages
    tool_call_id: str = ""  # only on tool messages: which call this answers
    is_error: bool = False  # only on tool messages: the tool failed


@dataclass(frozen=True)
class ModelTurn:
    """What a model returns for one turn: some text, and maybe tool requests."""

    text: str
    tool_calls: tuple[ToolCall, ...] = ()


@dataclass(frozen=True)
class ToolSpec:
    """A tool the agent may use.

    `parameters` is a JSON Schema describing the arguments. `run` receives those
    arguments as keyword arguments and returns text. If `needs_approval` is set,
    a person must approve each call before it runs.
    """

    name: str
    description: str
    parameters: dict[str, Any]
    run: Callable[..., str]
    needs_approval: bool = False


# ---- what a run produces ---------------------------------------------------


@dataclass(frozen=True)
class ToolResult:
    call: ToolCall
    output: str
    is_error: bool = False


@dataclass(frozen=True)
class Step:
    """One trip round the loop: the model's words and the tools it triggered."""

    number: int
    text: str
    results: tuple[ToolResult, ...] = ()


@dataclass
class AgentResult:
    final_text: str
    steps: list[Step] = field(default_factory=list)
    stop_reason: str = "finished"  # "finished" or "max_steps"

    @property
    def tools_called(self) -> list[str]:
        """Names of every tool the model asked for, in order."""
        return [result.call.name for step in self.steps for result in step.results]
