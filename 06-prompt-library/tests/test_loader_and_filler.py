import pytest

from promptlib.errors import MissingVariablesError, PromptError
from promptlib.filler import fill
from promptlib.loader import load_prompts, parse_prompt

VALID = """---
id: demo
title: Demo
category: testing
purpose: A demo.
variables:
  - name: topic
    description: What to talk about.
  - name: tone
    description: Voice.
    required: false
    default: plain
tips: Use it for tests only.
criteria: The answer is about the topic and is written in the requested tone.
example:
  topic: tea
---
Write about {{topic}} in a {{ tone }} tone.
"""


def make(**changes):
    """VALID with one piece of text replaced, to test one kind of mistake at a time."""
    text = VALID
    for old, new in changes.items():
        text = text.replace(old.replace("__", " "), new)
    return text


def test_valid_prompt_parses():
    prompt = parse_prompt(VALID)
    assert prompt.id == "demo"
    assert prompt.placeholders_in_body == ["topic", "tone"]


def test_fill_uses_defaults_for_optional_variables():
    assert fill(parse_prompt(VALID), {"topic": "tea"}).strip() == "Write about tea in a plain tone."


def test_fill_raises_for_missing_required_values():
    with pytest.raises(MissingVariablesError, match="topic"):
        fill(parse_prompt(VALID), {})


def test_allow_missing_leaves_placeholder_visible():
    assert "{{topic}}" in fill(parse_prompt(VALID), {}, allow_missing=True)


def test_fill_rejects_unknown_variable_names():
    with pytest.raises(PromptError, match="no variable"):
        fill(parse_prompt(VALID), {"topic": "tea", "topik": "oops"})


@pytest.mark.parametrize(
    "bad_text, message",
    [
        ("no front matter at all", "front matter"),
        (VALID.replace("title: Demo\n", ""), "missing: title"),
        (VALID.replace("{{topic}}", "{{subject}}"), "not declared"),
        (VALID.replace("{{ tone }}", "calm"), "never used"),
        (VALID.replace("example:\n  topic: tea", "example:\n  tone: calm"), "example is missing"),
        (VALID.replace("  topic: tea", "  topic: tea\n  colour: red"), "unknown variables"),
    ],
)
def test_mistakes_in_prompt_files_are_caught(bad_text, message):
    with pytest.raises(PromptError, match=message):
        parse_prompt(bad_text)


def test_file_name_must_match_id(tmp_path):
    (tmp_path / "other-name.md").write_text(VALID, encoding="utf-8")
    with pytest.raises(PromptError, match="must match the file name"):
        load_prompts(tmp_path)


def test_missing_folder_is_a_prompt_error(tmp_path):
    with pytest.raises(PromptError, match="not found"):
        load_prompts(tmp_path / "nope")
