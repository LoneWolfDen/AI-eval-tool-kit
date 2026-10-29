from miniagent.loop import MAX_TOOL_OUTPUT_CHARS, run_agent
from miniagent.models.base import AgentModel
from miniagent.models.mock import ScriptedModel
from miniagent.prompts import SYSTEM_PROMPT
from miniagent.types import INVALID_ARGUMENTS_KEY, ModelTurn, ToolCall, ToolSpec

TASK = "Draft a short status note from the risk log and milestones."


class FixedModel(AgentModel):
    """Plays back a list of turns, then repeats the last one. Lets tests control the 'model'."""

    name = "fixed"

    def __init__(self, *turns: ModelTurn) -> None:
        self._turns = list(turns)
        self.seen_messages = []

    def next_turn(self, system, messages, tools):
        self.seen_messages.append(list(messages))
        return self._turns.pop(0) if len(self._turns) > 1 else self._turns[0]


def calls(*pairs):
    return ModelTurn("", tuple(ToolCall(f"c{i}", name, args) for i, (name, args) in enumerate(pairs, 1)))


# ---- the basic loop -----------------------------------------------------------------


def test_agent_reads_data_then_answers(tools):
    result = run_agent(TASK, ScriptedModel(), tools, SYSTEM_PROMPT)
    assert result.stop_reason == "finished"
    assert result.tools_called == ["read_risk_log", "read_milestones"]
    assert "R-001" in result.final_text
    assert "R-006" not in result.final_text  # closed risk stays out


def test_every_tool_result_is_sent_back_to_the_model(tools):
    model = FixedModel(calls(("read_risk_log", {})), ModelTurn("done"))
    run_agent(TASK, model, tools, SYSTEM_PROMPT)
    second_turn_messages = model.seen_messages[1]
    assert [m.role for m in second_turn_messages] == ["user", "assistant", "tool"]
    assert second_turn_messages[2].tool_call_id == "c1"


def test_on_step_is_called_for_each_step(tools):
    seen = []
    run_agent(TASK, ScriptedModel(), tools, SYSTEM_PROMPT, on_step=seen.append)
    assert [step.number for step in seen] == [1, 2]


def test_max_steps_stops_a_model_that_never_finishes(tools):
    endless = FixedModel(calls(("read_milestones", {})))
    result = run_agent(TASK, endless, tools, SYSTEM_PROMPT, max_steps=3)
    assert result.stop_reason == "max_steps"
    assert len(result.steps) == 3


# ---- approval ------------------------------------------------------------------------


def test_saving_is_refused_when_nobody_approves(tools, output_dir):
    result = run_agent(TASK + " Save it.", ScriptedModel(), tools, SYSTEM_PROMPT)
    assert not (output_dir / "status-note.md").exists()
    assert "could not save" in result.final_text.lower()


def test_saving_works_when_approved(tools, output_dir):
    approved = []
    result = run_agent(TASK + " Save it.", ScriptedModel(), tools, SYSTEM_PROMPT, approve=lambda c: approved.append(c.name) or True)
    assert approved == ["save_note"]
    assert (output_dir / "status-note.md").exists()
    assert result.final_text.startswith("Saved the note.")


def test_read_only_tools_never_ask_for_approval(tools):
    asked = []
    run_agent(TASK, ScriptedModel(), tools, SYSTEM_PROMPT, approve=lambda c: asked.append(c) or True)
    assert asked == []


# ---- when the model makes mistakes: errors go back to it, nothing crashes ---------------------


def error_text_seen_by_model(tools, bad_turn):
    model = FixedModel(bad_turn, ModelTurn("ok"))
    run_agent(TASK, model, tools, SYSTEM_PROMPT)
    return model.seen_messages[1][-1]


def test_unknown_tool_lists_the_available_ones(tools):
    message = error_text_seen_by_model(tools, calls(("send_email", {})))
    assert message.is_error and "read_risk_log" in message.content


def test_bad_argument_value_is_reported_back(tools):
    message = error_text_seen_by_model(tools, calls(("read_risk_log", {"status": "stale"})))
    assert message.is_error and "status must be one of" in message.content


def test_wrong_argument_name_is_reported_back(tools):
    message = error_text_seen_by_model(tools, calls(("read_risk_log", {"colour": "red"})))
    assert message.is_error and "Bad arguments" in message.content


def test_invalid_json_arguments_are_reported_back(tools):
    message = error_text_seen_by_model(tools, calls(("read_risk_log", {INVALID_ARGUMENTS_KEY: "{oops"})))
    assert message.is_error and "not valid JSON" in message.content


def test_unexpected_crash_inside_a_tool_does_not_stop_the_agent():
    def explode() -> str:
        raise RuntimeError("disk on fire")

    broken = ToolSpec("explode", "always fails", {"type": "object", "properties": {}}, run=explode)
    model = FixedModel(calls(("explode", {})), ModelTurn("recovered"))
    result = run_agent(TASK, model, [broken], SYSTEM_PROMPT)
    assert result.final_text == "recovered"
    assert result.steps[0].results[0].is_error


def test_very_long_tool_output_is_cut():
    long_tool = ToolSpec("long", "returns a lot", {"type": "object", "properties": {}}, run=lambda: "x" * 50_000)
    model = FixedModel(calls(("long", {})), ModelTurn("done"))
    result = run_agent(TASK, model, [long_tool], SYSTEM_PROMPT)
    output = result.steps[0].results[0].output
    assert len(output) < MAX_TOOL_OUTPUT_CHARS + 100 and "cut" in output
