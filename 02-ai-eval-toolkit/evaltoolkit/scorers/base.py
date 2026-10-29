"""The interface every scorer (check) implements."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..types import CheckResult, EvalCase


class Scorer(ABC):
    """Judges one model answer and returns a CheckResult.

    To add a new check: subclass this, set `type_name`, implement `score`,
    then register the class in `scorers/__init__.py`.
    """

    #: The word used for `type:` in the YAML suite.
    type_name: str = ""

    #: Set to True if the scorer calls a second model (an LLM judge).
    needs_judge: bool = False

    @abstractmethod
    def score(self, case: EvalCase, output: str) -> CheckResult:
        """Check `output` (the model's answer to `case.prompt`)."""

    def _result(self, passed: bool, detail: str = "", score: float | None = None) -> CheckResult:
        """Build a CheckResult. Pass/fail checks get a score of 1.0 or 0.0."""
        if score is None:
            score = 1.0 if passed else 0.0
        return CheckResult(check=self.type_name, passed=passed, score=score, detail=detail)


def shorten(text: str, limit: int = 80) -> str:
    """Trim long text for use in one-line detail messages."""
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[: limit - 1] + "…"
