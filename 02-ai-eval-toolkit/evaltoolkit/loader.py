"""Load and validate a YAML suite file into an EvalSuite.

Validation lives here, in one place, so that a typo in a suite produces a
readable error message before any model is called.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .errors import SuiteError
from .types import CheckSpec, EvalCase, EvalSuite


def load_suite(path: str | Path) -> EvalSuite:
    """Read `path` and return a validated EvalSuite."""
    path = Path(path)
    if not path.is_file():
        raise SuiteError(f"Suite file not found: {path}")

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise SuiteError(f"{path} is not valid YAML: {exc}") from exc

    return parse_suite(raw, default_name=path.stem)


def parse_suite(raw: Any, default_name: str = "suite") -> EvalSuite:
    """Turn already-parsed YAML data (a dict) into an EvalSuite."""
    if not isinstance(raw, dict):
        raise SuiteError("Suite must be a mapping with a 'cases' list.")

    raw_cases = raw.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise SuiteError("Suite needs a non-empty 'cases' list.")

    cases = tuple(_parse_case(item, position) for position, item in enumerate(raw_cases, 1))
    _ensure_unique_ids(cases)

    return EvalSuite(
        name=str(raw.get("name", default_name)),
        description=str(raw.get("description", "")),
        cases=cases,
    )


def _parse_case(item: Any, position: int) -> EvalCase:
    label = f"case #{position}"
    if not isinstance(item, dict):
        raise SuiteError(f"{label} must be a mapping.")

    case_id = item.get("id")
    if not case_id:
        raise SuiteError(f"{label} is missing an 'id'.")
    label = f"case '{case_id}'"

    prompt = item.get("prompt")
    if not prompt:
        raise SuiteError(f"{label} is missing a 'prompt'.")

    raw_checks = item.get("checks")
    if not isinstance(raw_checks, list) or not raw_checks:
        raise SuiteError(f"{label} needs a non-empty 'checks' list.")

    return EvalCase(
        id=str(case_id),
        prompt=str(prompt),
        checks=tuple(_parse_check(c, label) for c in raw_checks),
        system=item.get("system"),
        tags=tuple(str(t) for t in item.get("tags", [])),
    )


def _parse_check(item: Any, case_label: str) -> CheckSpec:
    if not isinstance(item, dict) or "type" not in item:
        raise SuiteError(f"{case_label}: every check needs a 'type'.")
    params = {key: value for key, value in item.items() if key != "type"}
    return CheckSpec(type=str(item["type"]), params=params)


def _ensure_unique_ids(cases: tuple[EvalCase, ...]) -> None:
    seen: set[str] = set()
    for case in cases:
        if case.id in seen:
            raise SuiteError(f"Duplicate case id: '{case.id}'.")
        seen.add(case.id)
