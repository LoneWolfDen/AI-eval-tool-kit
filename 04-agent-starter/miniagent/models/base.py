"""The one interface every model adapter implements."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..types import Message, ModelTurn, ToolSpec


class AgentModel(ABC):
    """Turns the conversation so far into the model's next turn.

    To support a new provider, subclass this, translate `messages` and `tools`
    into the provider's format, call the API, and translate the reply back into
    a ModelTurn. Raise ModelError if the call fails.
    """

    #: Label shown in traces, e.g. "anthropic:<model-id>".
    name: str = "unnamed"

    @abstractmethod
    def next_turn(self, system: str, messages: list[Message], tools: list[ToolSpec]) -> ModelTurn:
        """Return the model's next turn: text, and any tool calls it wants run."""
