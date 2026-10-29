"""Run a suite against a model and score every answer."""

from __future__ import annotations

import time
from typing import Callable

from .clients.base import ModelClient
from .errors import EvalToolkitError
from .scorers import Scorer, build_scorer
from .types import CaseResult, CheckResult, EvalCase, EvalSuite, SuiteResult

ProgressCallback = Callable[[str, CaseResult], None]


def prepare_scorers(suite: EvalSuite, judge: ModelClient | None) -> dict[str, list[Scorer]]:
    """Build every scorer up front, so config mistakes fail before any model call."""
    return {case.id: [build_scorer(spec, judge) for spec in case.checks] for case in suite.cases}


def run_suite(
    suite: EvalSuite,
    client: ModelClient,
    judge: ModelClient | None = None,
    on_case_done: ProgressCallback | None = None,
) -> SuiteResult:
    """Ask `client` every question in `suite` and score the answers.

    `on_case_done(model_name, case_result)` is called after each case,
    which the CLI uses to print progress.
    """
    scorers_by_case = prepare_scorers(suite, judge)
    result = SuiteResult(suite_name=suite.name, model=client.name)

    for case in suite.cases:
        case_result = _run_case(case, client, scorers_by_case[case.id])
        result.cases.append(case_result)
        if on_case_done:
            on_case_done(client.name, case_result)

    return result


def _run_case(case: EvalCase, client: ModelClient, scorers: list[Scorer]) -> CaseResult:
    started = time.perf_counter()
    try:
        output = client.generate(case.prompt, case.system)
    except EvalToolkitError as exc:
        return CaseResult(case=case, output="", latency_s=time.perf_counter() - started, error=str(exc))
    latency = time.perf_counter() - started

    checks = [_run_check(scorer, case, output) for scorer in scorers]
    return CaseResult(case=case, output=output, latency_s=latency, checks=checks)


def _run_check(scorer: Scorer, case: EvalCase, output: str) -> CheckResult:
    """Run one scorer; a crashing scorer becomes a failed check, not a crashed run."""
    try:
        return scorer.score(case, output)
    except EvalToolkitError as exc:
        return CheckResult(check=scorer.type_name, passed=False, score=0.0, detail=f"scorer error: {exc}")
