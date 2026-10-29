"""Plain data containers shared by every other module.

They hold data and a few tiny derived properties, and contain no I/O.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# --------------------------------------------------------------------------
# Input side: what the YAML suite describes
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CheckSpec:
    """One check to run on a model's answer, as written in the YAML.

    Example YAML:  {type: contains, value: "PMP"}
    becomes        CheckSpec(type="contains", params={"value": "PMP"})
    """

    type: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvalCase:
    """A single prompt plus the checks its answer must satisfy."""

    id: str
    prompt: str
    checks: tuple[CheckSpec, ...]
    system: str | None = None
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class EvalSuite:
    """A named collection of cases."""

    name: str
    description: str
    cases: tuple[EvalCase, ...]


# --------------------------------------------------------------------------
# Output side: what running a suite produces
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CheckResult:
    """Outcome of one check. `score` is always between 0.0 and 1.0."""

    check: str
    passed: bool
    score: float
    detail: str = ""


@dataclass
class CaseResult:
    """Everything we know about one case after running it on one model."""

    case: EvalCase
    output: str
    latency_s: float
    error: str | None = None
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """A case passes only if the model answered and every check passed."""
        return self.error is None and all(c.passed for c in self.checks)

    @property
    def score(self) -> float:
        """Average of the check scores (0.0 if the model call failed)."""
        if self.error is not None or not self.checks:
            return 0.0
        return sum(c.score for c in self.checks) / len(self.checks)


@dataclass
class SuiteResult:
    """All case results for one suite run against one model."""

    suite_name: str
    model: str
    cases: list[CaseResult] = field(default_factory=list)
