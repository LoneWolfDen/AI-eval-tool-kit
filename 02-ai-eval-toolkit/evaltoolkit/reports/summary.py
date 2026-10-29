"""Numbers derived from results. Every report format reuses these helpers."""

from __future__ import annotations

from dataclasses import dataclass

from ..types import CaseResult, SuiteResult


@dataclass(frozen=True)
class ModelSummary:
    """Headline numbers for one model on one suite."""

    model: str
    total: int
    passed: int
    errors: int
    avg_score: float
    avg_latency_s: float
    by_tag: dict[str, tuple[int, int]]  # tag -> (passed, total)

    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total else 0.0


def summarize(result: SuiteResult) -> ModelSummary:
    cases = result.cases
    total = len(cases)
    return ModelSummary(
        model=result.model,
        total=total,
        passed=sum(1 for c in cases if c.passed),
        errors=sum(1 for c in cases if c.error),
        avg_score=_mean([c.score for c in cases]),
        avg_latency_s=_mean([c.latency_s for c in cases]),
        by_tag=_tally_by_tag(cases),
    )


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _tally_by_tag(cases: list[CaseResult]) -> dict[str, tuple[int, int]]:
    tally: dict[str, list[int]] = {}
    for case in cases:
        for tag in case.case.tags:
            passed_total = tally.setdefault(tag, [0, 0])
            passed_total[0] += int(case.passed)
            passed_total[1] += 1
    return {tag: (p, t) for tag, (p, t) in sorted(tally.items())}


def case_ids(results: list[SuiteResult]) -> list[str]:
    """Case ids in suite order, taken from the first result."""
    return [c.case.id for c in results[0].cases] if results else []


def lookup(results: list[SuiteResult]) -> dict[str, dict[str, CaseResult]]:
    """model name -> case id -> CaseResult, for building comparison tables."""
    return {r.model: {c.case.id: c for c in r.cases} for r in results}


def status_label(case_result: CaseResult) -> str:
    """One word describing a case outcome: PASS, FAIL or ERROR."""
    if case_result.error:
        return "ERROR"
    return "PASS" if case_result.passed else "FAIL"


def failure_lines(case_result: CaseResult) -> list[str]:
    """Human-readable reasons a case did not pass (empty if it passed)."""
    if case_result.error:
        return [f"model call failed: {case_result.error}"]
    return [f"{c.check}: {c.detail or 'failed'}" for c in case_result.checks if not c.passed]
