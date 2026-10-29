"""The one interface every model client implements."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ModelClient(ABC):
    """Anything that can turn a prompt into a text answer.

    To support a new provider, subclass this, implement `generate`,
    and register it in `clients/__init__.py`.
    """

    #: Label shown in reports, e.g. "anthropic:claude-sonnet-5-5".
    name: str = "unnamed"

    @abstractmethod
    def generate(self, prompt: str, system: str | None = None) -> str:
        """Return the model's text reply. Raise ClientError on failure."""
