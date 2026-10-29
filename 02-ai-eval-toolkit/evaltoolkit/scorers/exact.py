"""Check that the answer equals an expected string."""

from __future__ import annotations

from .base import Scorer, shorten
from ..types import CheckResult, EvalCase


class Exact(Scorer):
    """Passes if the whole answer equals `value`.

    YAML:  {type: exact, value: "READY"}

    Surrounding whitespace is ignored unless `strip: false`.
    Comparison is case-sensitive unless `case_sensitive: false`.
    """

    type_name = "exact"

    def __init__(self, value: str, strip: bool = True, case_sensitive: bool = True) -> None:
        self._expected = str(value)
        self._strip = strip
        self._case_sensitive = case_sensitive

    def score(self, case: EvalCase, output: str) -> CheckResult:
        expected, actual = self._expected, output
        if self._strip:
            expected, actual = expected.strip(), actual.strip()
        if not self._case_sensitive:
            expected, actual = expected.lower(), actual.lower()

        passed = expected == actual
        detail = "" if passed else f"expected {shorten(expected, 40)!r}, got {shorten(actual, 40)!r}"
        return self._result(passed, detail)
