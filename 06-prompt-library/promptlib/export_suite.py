"""Turn the prompts into a test suite for the eval toolkit (02-ai-eval-toolkit).

Each prompt becomes one case: its example values are filled in, and a
'rubric' check carries the prompt's quality criteria. Run the suite on a real
model with a judge to see how well each prompt performs.
"""

from __future__ import annotations

import yaml

from .filler import fill
from .model import Prompt

DEFAULT_MIN_SCORE = 4


def build_suite(prompts: list[Prompt], name: str = "prompt-library") -> dict:
    """Build the suite as plain data, in the toolkit's YAML shape."""
    return {
        "name": name,
        "description": "One case per prompt, filled with its example values and graded against its quality criteria.",
        "cases": [_build_case(prompt) for prompt in prompts],
    }


def _build_case(prompt: Prompt) -> dict:
    return {
        "id": prompt.id,
        "tags": [prompt.category],
        "prompt": fill(prompt, prompt.example).strip(),
        "checks": [{"type": "rubric", "criteria": prompt.criteria, "min_score": DEFAULT_MIN_SCORE}],
    }


def dump_suite(suite: dict) -> str:
    """Write the suite as YAML, keeping multi-line text readable."""
    return yaml.dump(suite, Dumper=_ReadableDumper, sort_keys=False, allow_unicode=True, width=100)


class _ReadableDumper(yaml.SafeDumper):
    """Writes multi-line strings as '|' blocks instead of one escaped line."""


def _represent_string(dumper: yaml.SafeDumper, value: str) -> yaml.ScalarNode:
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_ReadableDumper.add_representer(str, _represent_string)
