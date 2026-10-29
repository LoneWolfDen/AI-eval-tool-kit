"""Checks that look for substrings in the answer."""

from __future__ import annotations

from .base import Scorer
from ..errors import ConfigError
from ..types import CheckResult, EvalCase


def _as_list(value: str | list[str]) -> list[str]:
    return [value] if isinstance(value, str) else [str(v) for v in value]


class Contains(Scorer):
    """Passes if the answer includes the given text.

    YAML:  {type: contains, value: "Project Management Professional"}
           {type: contains, value: [risk, mitigation], match: any}

    `match` is "all" (default) or "any". Matching ignores case unless
    `case_sensitive: true`.
    """

    type_name = "contains"

    def __init__(self, value: str | list[str], match: str = "all", case_sensitive: bool = False) -> None:
        if match not in ("all", "any"):
            raise ConfigError(f"contains: match must be 'all' or 'any', got '{match}'.")
        self._needles = _as_list(value)
        self._match = match
        self._case_sensitive = case_sensitive

    def score(self, case: EvalCase, output: str) -> CheckResult:
        haystack = output if self._case_sensitive else output.lower()
        found = [n for n in self._needles if (n if self._case_sensitive else n.lower()) in haystack]
        missing = [n for n in self._needles if n not in found]

        passed = bool(found) if self._match == "any" else not missing
        detail = "" if passed else f"missing: {missing}"
        return self._result(passed, detail)


class NotContains(Scorer):
    """Passes only if the answer includes none of the given texts.

    YAML:  {type: not_contains, value: "1234"}
    """

    type_name = "not_contains"

    def __init__(self, value: str | list[str], case_sensitive: bool = False) -> None:
        self._needles = _as_list(value)
        self._case_sensitive = case_sensitive

    def score(self, case: EvalCase, output: str) -> CheckResult:
        haystack = output if self._case_sensitive else output.lower()
        leaked = [n for n in self._needles if (n if self._case_sensitive else n.lower()) in haystack]

        passed = not leaked
        detail = "" if passed else f"found forbidden text: {leaked}"
        return self._result(passed, detail)
