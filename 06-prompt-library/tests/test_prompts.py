"""Checks on the real prompt files, so a bad edit is caught straight away."""

import re

from promptlib.filler import fill
from promptlib.model import PLACEHOLDER


def test_all_twelve_prompts_load(prompts):
    assert len(prompts) == 12


def test_every_example_fills_the_prompt_completely(prompts):
    for prompt in prompts:
        filled = fill(prompt, prompt.example)
        assert not PLACEHOLDER.search(filled), prompt.id


def test_examples_use_only_fictional_contact_details(prompts):
    """Prompts are committed to a repo, so examples must never hold real contact details."""
    for prompt in prompts:
        text = " ".join(prompt.example.values())
        for email in re.findall(r"[\w.+-]+@[\w.-]+", text):
            assert email.endswith("@example.com"), f"{prompt.id}: {email}"
        for phone in re.findall(r"\b0\d{4} \d{6}\b", text):
            assert phone.startswith("07700 900"), f"{prompt.id}: {phone}"  # Ofcom drama range


def test_every_prompt_has_criteria_and_tips(prompts):
    for prompt in prompts:
        assert len(prompt.criteria) > 40, prompt.id
        assert len(prompt.tips) > 20, prompt.id


def test_categories_are_the_expected_set(prompts):
    categories = {p.category for p in prompts}
    assert categories == {"communication", "learning", "meetings", "planning", "privacy", "reporting", "risk", "team"}
