"""Model clients, plus `create_client` to build one from a "provider:model" string."""

from __future__ import annotations

from .anthropic_client import AnthropicClient
from .base import ModelClient
from .mock import MockClient
from .openai_compat import PRESETS, OpenAICompatClient
from ..errors import ClientError

SUPPORTED_PROVIDERS = ("mock", "anthropic", *PRESETS)


def create_client(spec: str) -> ModelClient:
    """Build a client from text like "anthropic:claude-sonnet-5-5" or "ollama:llama3.1"."""
    provider, separator, model = spec.partition(":")
    if not separator or not model:
        raise ClientError(f"Model spec '{spec}' must look like provider:model (e.g. ollama:llama3.1).")

    if provider == "mock":
        return MockClient(model)
    if provider == "anthropic":
        return AnthropicClient(model)
    if provider in PRESETS:
        return OpenAICompatClient(provider, model)

    raise ClientError(f"Unknown provider '{provider}'. Choose from: {', '.join(SUPPORTED_PROVIDERS)}.")


__all__ = ["ModelClient", "create_client", "SUPPORTED_PROVIDERS"]
