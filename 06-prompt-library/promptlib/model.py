"""Plain data containers for prompts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# {{name}} with optional spaces inside the braces. Names are lowercase snake_case.
PLACEHOLDER = re.compile(r"\{\{\s*([a-z_][a-z0-9_]*)\s*\}\}")


@dataclass(frozen=True)
class Variable:
    """One value the user supplies when using a prompt."""

    name: str
    description: str
    required: bool = True
    default: str = ""  # used when the variable is optional and left out


@dataclass(frozen=True)
class Prompt:
    """A reusable prompt and everything we know about it."""

    id: str
    title: str
    category: str
    purpose: str
    variables: tuple[Variable, ...]
    body: str  # the prompt text, containing {{placeholders}}
    tips: str  # advice for the person using it
    criteria: str  # what a good answer looks like; used when exporting an eval suite
    example: dict[str, str]  # sample values, all fictional
    path: Path | None = None

    @property
    def variable_names(self) -> list[str]:
        return [variable.name for variable in self.variables]

    @property
    def placeholders_in_body(self) -> list[str]:
        """Placeholder names in order of first appearance, without repeats."""
        names = PLACEHOLDER.findall(self.body)
        return list(dict.fromkeys(names))
