"""Adapter for local servers that speak the OpenAI chat format (Ollama, LM Studio).

Uses only the standard library. Tool calling works like this in this format:
  - You send `tools`: [{"type": "function", "function": {name, description, parameters}}].
  - The reply message may hold `tool_calls`, each with an id and `function.arguments`
    (a JSON *string*, which small models sometimes get wrong).
  - You answer each call with a message of role "tool" and the matching `tool_call_id`.
Not every local model supports tool calling. Pick one that advertises it.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from ..errors import ModelError
from ..types import INVALID_ARGUMENTS_KEY, Message, ModelTurn, ToolCall, ToolSpec
from .base import AgentModel

BASE_URLS = {
    "ollama": "http://localhost:11434/v1",
    "lmstudio": "http://localhost:1234/v1",
}


class OpenAICompatModel(AgentModel):
    def __init__(self, provider: str, model: str, timeout_s: float = 180.0) -> None:
        self._base_url = BASE_URLS[provider]
        self._model = model
        self._timeout_s = timeout_s
        self.name = f"{provider}:{model}"

    def next_turn(self, system: str, messages: list[Message], tools: list[ToolSpec]) -> ModelTurn:
        payload = {
            "model": self._model,
            "messages": to_openai_messages(system, messages),
            "tools": to_openai_tools(tools),
            "temperature": 0,
        }
        reply = self._post("/chat/completions", payload)
        try:
            return parse_openai_message(reply["choices"][0]["message"])
        except (KeyError, IndexError, TypeError) as exc:
            raise ModelError(f"Unexpected response shape: {reply!r}") from exc

    def _post(self, path: str, payload: dict) -> dict:
        request = urllib.request.Request(
            self._base_url + path,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout_s) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:300]
            raise ModelError(f"HTTP {exc.code} from {self._base_url}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ModelError(f"Could not reach {self._base_url}: {exc}") from exc


# ---- translation helpers: plain functions, so they can be tested without a server ----


def to_openai_tools(tools: list[ToolSpec]) -> list[dict]:
    return [
        {"type": "function", "function": {"name": t.name, "description": t.description, "parameters": t.parameters}}
        for t in tools
    ]


def to_openai_messages(system: str, messages: list[Message]) -> list[dict]:
    converted: list[dict] = [{"role": "system", "content": system}]
    for message in messages:
        if message.role == "user":
            converted.append({"role": "user", "content": message.content})
        elif message.role == "assistant":
            entry: dict = {"role": "assistant", "content": message.content or None}
            if message.tool_calls:
                entry["tool_calls"] = [
                    {"id": c.id, "type": "function", "function": {"name": c.name, "arguments": json.dumps(c.arguments)}}
                    for c in message.tool_calls
                ]
            converted.append(entry)
        elif message.role == "tool":
            converted.append({"role": "tool", "tool_call_id": message.tool_call_id, "content": message.content})
    return converted


def parse_openai_message(message: dict) -> ModelTurn:
    calls = tuple(_parse_call(raw, index) for index, raw in enumerate(message.get("tool_calls") or []))
    return ModelTurn(text=message.get("content") or "", tool_calls=calls)


def _parse_call(raw: dict, index: int) -> ToolCall:
    function = raw["function"]
    arguments_text = function.get("arguments") or "{}"
    try:
        arguments = json.loads(arguments_text)
        if not isinstance(arguments, dict):
            raise ValueError("arguments must be a JSON object")
    except ValueError:
        arguments = {INVALID_ARGUMENTS_KEY: arguments_text}
    return ToolCall(id=raw.get("id") or f"call_{index + 1}", name=function["name"], arguments=arguments)
