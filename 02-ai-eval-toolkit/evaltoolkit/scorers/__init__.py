"""Scorers (checks) and the registry that turns YAML specs into scorer objects."""

from __future__ import annotations

from .base import Scorer
from .contains import Contains, NotContains
from .exact import Exact
from .length import MaxWords, MinWords
from .pii import NoPII
from .regex import Regex
from .rubric import Rubric
from ..clients.base import ModelClient
from ..errors import ConfigError
from ..types import CheckSpec

# The word used as `type:` in YAML -> the class that implements it.
SCORER_TYPES: dict[str, type[Scorer]] = {
    cls.type_name: cls
    for cls in (Contains, NotContains, Exact, Regex, MaxWords, MinWords, NoPII, Rubric)
}


def build_scorer(spec: CheckSpec, judge: ModelClient | None = None) -> Scorer:
    """Create the scorer described by `spec`."""
    scorer_class = SCORER_TYPES.get(spec.type)
    if scorer_class is None:
        raise ConfigError(f"Unknown check type '{spec.type}'. Available: {', '.join(sorted(SCORER_TYPES))}.")

    params = dict(spec.params)
    if scorer_class.needs_judge:
        if judge is None:
            raise ConfigError(f"Check '{spec.type}' needs a judge model. Pass --judge provider:model.")
        params["judge"] = judge

    try:
        return scorer_class(**params)
    except TypeError as exc:
        raise ConfigError(f"Bad parameters for check '{spec.type}': {exc}") from exc


__all__ = ["Scorer", "SCORER_TYPES", "build_scorer"]
