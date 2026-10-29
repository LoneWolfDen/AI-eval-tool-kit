"""Fill a prompt's {{placeholders}} with real values."""

from __future__ import annotations

from .errors import MissingVariablesError, PromptError
from .model import PLACEHOLDER, Prompt


def fill(prompt: Prompt, values: dict[str, str], allow_missing: bool = False) -> str:
    """Return the prompt text with every placeholder replaced.

    - Optional variables that are left out use their default.
    - Required variables that are left out raise MissingVariablesError,
      unless `allow_missing` is set, in which case {{name}} stays visible.
    - A value for a variable the prompt does not have raises PromptError,
      which catches typos such as `--var projct=...`.
    """
    unknown = sorted(set(values) - set(prompt.variable_names))
    if unknown:
        raise PromptError(f"Prompt '{prompt.id}' has no variable(s): {', '.join(unknown)}")

    resolved = _resolve_values(prompt, values, allow_missing)
    return PLACEHOLDER.sub(lambda match: resolved.get(match.group(1), match.group(0)), prompt.body)


def _resolve_values(prompt: Prompt, values: dict[str, str], allow_missing: bool) -> dict[str, str]:
    resolved: dict[str, str] = {}
    missing: list[str] = []

    for variable in prompt.variables:
        if variable.name in values:
            resolved[variable.name] = values[variable.name].strip()
        elif not variable.required:
            resolved[variable.name] = variable.default
        else:
            missing.append(variable.name)

    if missing and not allow_missing:
        raise MissingVariablesError(prompt.id, missing)
    return resolved
