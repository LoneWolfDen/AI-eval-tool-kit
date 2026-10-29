"""Check the answer against a regular expression."""

from __future__ import annotations

import re

from .base import Scorer
from ..errors import ConfigError
from ..types import CheckResult, EvalCase


class Regex(Scorer):
    """Passes if the pattern is found (or, with `must_match: false`, NOT found).

    YAML:  {type: regex, pattern: '^\\d+$'}
           {type: regex, pattern: 'password', must_match: false, ignore_case: true}

    Uses `re.search`, so anchor the pattern with ^ and $ for a whole-answer match.
    """

    type_name = "regex"

    def __init__(self, pattern: str, must_match: bool = True, ignore_case: bool = False) -> None:
        flags = re.IGNORECASE if ignore_case else 0
        try:
            self._pattern = re.compile(pattern, flags)
        except re.error as exc:
            raise ConfigError(f"regex: invalid pattern {pattern!r}: {exc}") from exc
        self._must_match = must_match

    def score(self, case: EvalCase, output: str) -> CheckResult:
        found = self._pattern.search(output.strip()) is not None
        passed = found == self._must_match

        if passed:
            return self._result(True)
        verdict = "did not match" if self._must_match else "matched but should not have"
        return self._result(False, f"pattern {self._pattern.pattern!r} {verdict}")
