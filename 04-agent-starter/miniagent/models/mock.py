"""A scripted stand-in for a model, so the loop runs offline with no API key.

It is NOT intelligent. It follows a fixed routine that shows the loop working:
read both data tools, optionally save a note, then answer with a status note
built from what the tools returned. Use a real model to see real behaviour.
"""

from __future__ import annotations

import json

from ..types import Message, ModelTurn, ToolCall, ToolSpec
from .base import AgentModel

_ATTENTION_STATUSES = {"at_risk": "at risk", "late": "late"}
TOP_RISK_COUNT = 3


class ScriptedModel(AgentModel):
    name = "mock:scripted"

    def next_turn(self, system: str, messages: list[Message], tools: list[ToolSpec]) -> ModelTurn:
        outcomes = _latest_outcomes(messages)

        if "read_risk_log" not in outcomes:
            return ModelTurn(
                "I'll read the risk log and the milestones first.",
                (
                    ToolCall("call_1", "read_risk_log", {"status": "active"}),
                    ToolCall("call_2", "read_milestones", {}),
                ),
            )

        risks_text, risks_failed = outcomes["read_risk_log"]
        milestones_text, milestones_failed = outcomes.get("read_milestones", ("", True))
        if risks_failed or milestones_failed:
            return ModelTurn(f"I could not read the project data. {risks_text if risks_failed else milestones_text}")

        note = compose_note(json.loads(risks_text), json.loads(milestones_text))

        wants_save = "save" in _first_user_text(messages).lower()
        if wants_save and "save_note" not in outcomes:
            return ModelTurn("Now I'll save the note.", (ToolCall("call_3", "save_note", {"filename": "status-note.md", "content": note}),))

        return ModelTurn(_describe_save(outcomes) + note)


def compose_note(risks: list[dict], milestones: list[dict]) -> str:
    """Build a short status note from tool results. Pure text work, no model involved."""
    attention = [m for m in milestones if m["status"] in _ATTENTION_STATUSES]
    top_risks = risks[:TOP_RISK_COUNT]

    lines = [f"Status note: {len(attention)} of {len(milestones)} milestones need attention.", "", "Milestones needing attention:"]
    lines += [f"- {m['name']} (due {m['due']}): {_ATTENTION_STATUSES[m['status']]}" for m in attention] or ["- None"]
    lines += ["", "Top risks:"]
    lines += [
        f"- {r['id']} {r['title']} (score {r['score']}), owner {r['owner']}. Next: {r['mitigation']}."
        for r in top_risks
    ]
    if top_risks:
        lines += ["", f"Ask: agree how we unblock {top_risks[0]['id']} ({top_risks[0]['title']})."]
    return "\n".join(lines)


def _latest_outcomes(messages: list[Message]) -> dict[str, tuple[str, bool]]:
    """Map tool name -> (output, is_error) for the most recent result of each tool."""
    names_by_call_id = {call.id: call.name for m in messages for call in m.tool_calls}
    return {names_by_call_id[m.tool_call_id]: (m.content, m.is_error) for m in messages if m.role == "tool"}


def _first_user_text(messages: list[Message]) -> str:
    return next((m.content for m in messages if m.role == "user"), "")


def _describe_save(outcomes: dict[str, tuple[str, bool]]) -> str:
    if "save_note" not in outcomes:
        return ""
    text, failed = outcomes["save_note"]
    return f"I could not save the note: {text}\n\n" if failed else "Saved the note.\n\n"
