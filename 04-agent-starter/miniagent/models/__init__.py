"""Model adapters, plus `create_model` to build one from a "provider:model" string."""

from __future__ import annotations

from ..errors import ModelError
from .anthropic_model import AnthropicModel
from .base import AgentModel
from .mock import ScriptedModel
from .openai_compat_model import BASE_URLS, OpenAICompatModel

SUPPORTED_PROVIDERS = ("mock", "anthropic", *BASE_URLS)


def create_model(spec: str) -> AgentModel:
    """Build a model from text like "mock:scripted", "anthropic:<model-id>" or "ollama:llama3.1"."""
    provider, separator, name = spec.partition(":")
    if not separator or not name:
        raise ModelError(f"Model spec '{spec}' must look like provider:model (for example mock:scripted).")

    if provider == "mock":
        if name != "scripted":
            raise ModelError("The only mock model is mock:scripted.")
        return ScriptedModel()
    if provider == "anthropic":
        return AnthropicModel(name)
    if provider in BASE_URLS:
        return OpenAICompatModel(provider, name)

    raise ModelError(f"Unknown provider '{provider}'. Choose from: {', '.join(SUPPORTED_PROVIDERS)}.")


__all__ = ["AgentModel", "create_model", "SUPPORTED_PROVIDERS"]
