"""Client for Anthropic's Messages API (needs `pip install anthropic`)."""

from __future__ import annotations

from .base import ModelClient
from ..errors import ClientError


class AnthropicClient(ModelClient):
    """Calls Claude models. Reads ANTHROPIC_API_KEY from the environment."""

    def __init__(self, model: str, max_tokens: int = 1024) -> None:
        try:
            import anthropic
        except ImportError as exc:
            raise ClientError("The anthropic package is missing. Run: pip install anthropic") from exc

        self._sdk = anthropic.Anthropic()
        self._model = model
        self._max_tokens = max_tokens
        self.name = f"anthropic:{model}"

    def generate(self, prompt: str, system: str | None = None) -> str:
        request = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            request["system"] = system

        try:
            message = self._sdk.messages.create(**request)
        except Exception as exc:  # the SDK raises several error types; report them uniformly
            raise ClientError(f"Anthropic call failed: {exc}") from exc

        return "".join(block.text for block in message.content if block.type == "text")
