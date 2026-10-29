"""Checks on how long the answer is, measured in words."""

from __future__ import annotations

from .base import Scorer
from ..types import CheckResult, EvalCase


def count_words(text: str) -> int:
    return len(text.split())


class MaxWords(Scorer):
    """Passes if the answer has at most `limit` words.

    YAML:  {type: max_words, limit: 40}
    """

    type_name = "max_words"

    def __init__(self, limit: int) -> None:
        self._limit = int(limit)

    def score(self, case: EvalCase, output: str) -> CheckResult:
        words = count_words(output)
        passed = words <= self._limit
        detail = "" if passed else f"{words} words, limit is {self._limit}"
        return self._result(passed, detail)


class MinWords(Scorer):
    """Passes if the answer has at least `minimum` words.

    YAML:  {type: min_words, minimum: 20}
    """

    type_name = "min_words"

    def __init__(self, minimum: int) -> None:
        self._minimum = int(minimum)

    def score(self, case: EvalCase, output: str) -> CheckResult:
        words = count_words(output)
        passed = words >= self._minimum
        detail = "" if passed else f"{words} words, minimum is {self._minimum}"
        return self._result(passed, detail)
