"""The adapters translate between our neutral messages and each provider's format.
These tests check the translation as plain data, so they need no SDK, server or key."""

import json
from types import SimpleNamespace

import pytest

from miniagent.errors import ModelError
from miniagent.models import create_model
from miniagent.models.anthropic_model import parse_anthropic_content, to_anthropic_messages, to_anthropic_tools
from miniagent.models.openai_compat_model import parse_openai_message, to_openai_messages, to_openai_tools
from miniagent.types import INVALID_ARGUMENTS_KEY, Message, ToolCall

CALLS = (ToolCall("a1", "read_risk_log", {"status": "active"}), ToolCall("a2", "read_milestones", {}))
CONVERSATION = [
    Message(role="user", content="Draft a note."),
    Message(role="assistant", content="Reading.", tool_calls=CALLS),
    Message(role="tool", content="[risks]", tool_call_id="a1"),
    Message(role="tool", content="boom", tool_call_id="a2", is_error=True),
]


# ---- Anthropic ----------------------------------------------------------------------


def test_anthropic_tools_use_input_schema(tools):
    converted = to_anthropic_tools(tools)
    assert converted[0].keys() == {"name", "description", "input_schema"}
    assert converted[0]["input_schema"]["type"] == "object"


def test_anthropic_messages_group_tool_results_into_one_user_message():
    converted = to_anthropic_messages(CONVERSATION)
    assert [m["role"] for m in converted] == ["user", "assistant", "user"]

    assistant_blocks = converted[1]["content"]
    assert [b["type"] for b in assistant_blocks] == ["text", "tool_use", "tool_use"]
    assert assistant_blocks[1] == {"type": "tool_use", "id": "a1", "name": "read_risk_log", "input": {"status": "active"}}

    results = converted[2]["content"]
    assert [b["tool_use_id"] for b in results] == ["a1", "a2"]
    assert "is_error" not in results[0] and results[1]["is_error"] is True


def test_anthropic_assistant_message_without_text_has_no_empty_text_block():
    converted = to_anthropic_messages([Message(role="user", content="hi"), Message(role="assistant", content="", tool_calls=CALLS[:1])])
    assert [b["type"] for b in converted[1]["content"]] == ["tool_use"]


def test_anthropic_response_parsing():
    blocks = [
        SimpleNamespace(type="text", text="Let me look."),
        SimpleNamespace(type="tool_use", id="t1", name="read_milestones", input={"status": "attention"}),
    ]
    turn = parse_anthropic_content(blocks)
    assert turn.text == "Let me look."
    assert turn.tool_calls == (ToolCall("t1", "read_milestones", {"status": "attention"}),)


# ---- OpenAI-style (Ollama, LM Studio) ------------------------------------------------------


def test_openai_tools_are_wrapped_as_functions(tools):
    assert to_openai_tools(tools)[0]["type"] == "function"
    assert to_openai_tools(tools)[0]["function"]["parameters"]["type"] == "object"


def test_openai_messages_put_the_system_prompt_first_and_serialise_arguments():
    converted = to_openai_messages("be brief", CONVERSATION)
    assert converted[0] == {"role": "system", "content": "be brief"}
    assert [m["role"] for m in converted] == ["system", "user", "assistant", "tool", "tool"]

    first_call = converted[2]["tool_calls"][0]
    assert first_call["function"]["arguments"] == json.dumps({"status": "active"})  # a JSON string, not a dict
    assert converted[3] == {"role": "tool", "tool_call_id": "a1", "content": "[risks]"}


def test_openai_response_parsing():
    turn = parse_openai_message(
        {"content": None, "tool_calls": [{"id": "x1", "type": "function", "function": {"name": "read_risk_log", "arguments": '{"min_score": 10}'}}]}
    )
    assert turn.text == "" and turn.tool_calls == (ToolCall("x1", "read_risk_log", {"min_score": 10}),)


def test_openai_invalid_json_arguments_are_flagged_not_fatal():
    turn = parse_openai_message({"content": "", "tool_calls": [{"function": {"name": "read_risk_log", "arguments": "{min_score: 10"}}]})
    assert turn.tool_calls[0].arguments == {INVALID_ARGUMENTS_KEY: "{min_score: 10"}
    assert turn.tool_calls[0].id == "call_1"  # a missing id is filled in


def test_openai_plain_answer_has_no_tool_calls():
    assert parse_openai_message({"content": "All done."}).tool_calls == ()


# ---- choosing a model ---------------------------------------------------------------------------


def test_create_model_accepts_the_mock_and_local_providers():
    assert create_model("mock:scripted").name == "mock:scripted"
    assert create_model("ollama:llama3.1").name == "ollama:llama3.1"


@pytest.mark.parametrize("spec", ["nonsense", "mock:smart", "gizmo:x"])
def test_create_model_rejects_bad_specs(spec):
    with pytest.raises(ModelError):
        create_model(spec)
