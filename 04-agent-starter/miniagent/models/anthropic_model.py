"""Adapter for Claude models through Anthropic's Messages API (needs `pip install anthropic`).

Tool use in this API works like this:
  - You send `tools`: name, description and an `input_schema` (JSON Schema).
  - The model replies with content blocks. A `tool_use` block carries an id, a name and `input`.
  - You run the tool, then send a user message holding a `tool_result` block per call,
    each pointing back at its `tool_use_id`. Failed tools set `is_error: true`.
Docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use
"""

from __future__ import annotations

from ..errors import ModelError
from ..types import Message, ModelTurn, ToolCall, ToolSpec
from .base import AgentModel


class AnthropicModel(AgentModel):
    """Reads ANTHROPIC_API_KEY from the environment."""

    def __init__(self, model: str, max_tokens: int = 1500) -> None:
        try:
            import anthropic
        except ImportError as exc:
            raise ModelError("The anthropic package is missing. Run: pip install anthropic") from exc

        self._sdk = anthropic.Anthropic()
        self._model = model
        self._max_tokens = max_tokens
        self.name = f"anthropic:{model}"

    def next_turn(self, system: str, messages: list[Message], tools: list[ToolSpec]) -> ModelTurn:
        try:
            response = self._sdk.messages.create(
                model=self._model,
                max_tokens=self._max_tokens,
                system=system,
                tools=to_anthropic_tools(tools),
                messages=to_anthropic_messages(messages),
            )
        except Exception as exc:  # the SDK raises several error types; report them uniformly
            raise ModelError(f"Anthropic call failed: {exc}") from exc

        return parse_anthropic_content(response.content)


# ---- translation helpers: plain functions, so they can be tested without the SDK ----


def to_anthropic_tools(tools: list[ToolSpec]) -> list[dict]:
    return [{"name": t.name, "description": t.description, "input_schema": t.parameters} for t in tools]


def to_anthropic_messages(messages: list[Message]) -> list[dict]:
    """Convert our neutral messages. Consecutive tool results share one user message."""
    converted: list[dict] = []
    for message in messages:
        if message.role == "user":
            converted.append({"role": "user", "content": message.content})
        elif message.role == "assistant":
            converted.append({"role": "assistant", "content": _assistant_blocks(message)})
        elif message.role == "tool":
            block = {"type": "tool_result", "tool_use_id": message.tool_call_id, "content": message.content}
            if message.is_error:
                block["is_error"] = True
            if converted and _is_tool_result_message(converted[-1]):
                converted[-1]["content"].append(block)
            else:
                converted.append({"role": "user", "content": [block]})
    return converted


def parse_anthropic_content(content_blocks: list) -> ModelTurn:
    text = "".join(block.text for block in content_blocks if block.type == "text")
    calls = tuple(
        ToolCall(id=block.id, name=block.name, arguments=dict(block.input))
        for block in content_blocks
        if block.type == "tool_use"
    )
    return ModelTurn(text=text, tool_calls=calls)


def _assistant_blocks(message: Message) -> list[dict]:
    blocks: list[dict] = []
    if message.content.strip():  # the API rejects empty text blocks
        blocks.append({"type": "text", "text": message.content})
    blocks += [{"type": "tool_use", "id": c.id, "name": c.name, "input": c.arguments} for c in message.tool_calls]
    return blocks


def _is_tool_result_message(entry: dict) -> bool:
    content = entry["content"]
    return entry["role"] == "user" and isinstance(content, list) and bool(content) and content[0].get("type") == "tool_result"
