"""JSON report: raw results for further analysis in pandas, notebooks, etc."""

from __future__ import annotations

import json

from ..types import SuiteResult
from .summary import summarize


def render_json(results: list[SuiteResult]) -> str:
    payload = [_result_to_dict(result) for result in results]
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def _result_to_dict(result: SuiteResult) -> dict:
    s = summarize(result)
    return {
        "suite": result.suite_name,
        "model": result.model,
        "summary": {
            "total": s.total,
            "passed": s.passed,
            "pass_rate": round(s.pass_rate, 4),
            "avg_score": round(s.avg_score, 4),
            "avg_latency_s": round(s.avg_latency_s, 4),
            "errors": s.errors,
        },
        "cases": [
            {
                "id": c.case.id,
                "tags": list(c.case.tags),
                "passed": c.passed,
                "score": round(c.score, 4),
                "latency_s": round(c.latency_s, 4),
                "error": c.error,
                "output": c.output,
                "checks": [
                    {"check": k.check, "passed": k.passed, "score": round(k.score, 4), "detail": k.detail}
                    for k in c.checks
                ],
            }
            for c in result.cases
        ],
    }
