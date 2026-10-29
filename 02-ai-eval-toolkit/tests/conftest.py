"""Shared test setup: make the package importable and offer reusable fixtures."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evaltoolkit.types import CheckSpec, EvalCase  # noqa: E402


@pytest.fixture
def make_case():
    """Build an EvalCase quickly: make_case("prompt text", system="...")."""

    def _make(prompt: str = "Question?", system: str | None = None, tags: tuple[str, ...] = ()) -> EvalCase:
        return EvalCase(id="case-1", prompt=prompt, checks=(CheckSpec("exact", {"value": "x"}),), system=system, tags=tags)

    return _make


@pytest.fixture
def example_suite_path() -> Path:
    return Path(__file__).resolve().parent.parent / "examples" / "suite_basic.yaml"
