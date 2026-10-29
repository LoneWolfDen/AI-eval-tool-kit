"""Read prompt files from disk and check them.

Checking happens here, once, so a mistake in a prompt file (a typo in a
placeholder, a missing example) is caught by the tests instead of in use.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from .errors import PromptError
from .model import Prompt, Variable

# A prompt file is: front matter between two "---" lines, then the prompt text.
_FILE_SHAPE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)
_REQUIRED_KEYS = ("id", "title", "category", "purpose", "variables", "tips", "criteria", "example")


def load_prompts(directory: str | Path) -> list[Prompt]:
    """Load every *.md file in `directory`, sorted by category then id."""
    directory = Path(directory)
    if not directory.is_dir():
        raise PromptError(f"Prompt folder not found: {directory}")

    prompts = [parse_prompt(path.read_text(encoding="utf-8"), path) for path in sorted(directory.glob("*.md"))]
    _ensure_unique_ids(prompts)
    return sorted(prompts, key=lambda p: (p.category, p.id))


def parse_prompt(text: str, path: Path | None = None) -> Prompt:
    """Turn the text of one prompt file into a validated Prompt."""
    label = path.name if path else "prompt"

    shape = _FILE_SHAPE.match(text)
    if shape is None:
        raise PromptError(f"{label}: must start with front matter between two '---' lines.")

    try:
        meta = yaml.safe_load(shape.group(1))
    except yaml.YAMLError as exc:
        raise PromptError(f"{label}: front matter is not valid YAML: {exc}") from exc

    missing = [key for key in _REQUIRED_KEYS if not isinstance(meta, dict) or key not in meta]
    if missing:
        raise PromptError(f"{label}: front matter is missing: {', '.join(missing)}")

    prompt = Prompt(
        id=str(meta["id"]),
        title=str(meta["title"]),
        category=str(meta["category"]),
        purpose=str(meta["purpose"]).strip(),
        variables=tuple(_parse_variable(item, label) for item in meta["variables"]),
        body=shape.group(2).strip() + "\n",
        tips=str(meta["tips"]).strip(),
        criteria=str(meta["criteria"]).strip(),
        example={str(k): str(v).strip() for k, v in dict(meta["example"]).items()},
        path=path,
    )
    _check_prompt(prompt, path, label)
    return prompt


def _parse_variable(item: object, label: str) -> Variable:
    if not isinstance(item, dict) or "name" not in item or "description" not in item:
        raise PromptError(f"{label}: each variable needs a name and a description.")
    return Variable(
        name=str(item["name"]),
        description=str(item["description"]).strip(),
        required=bool(item.get("required", True)),
        default=str(item.get("default", "")),
    )


def _check_prompt(prompt: Prompt, path: Path | None, label: str) -> None:
    if path is not None and path.stem != prompt.id:
        raise PromptError(f"{label}: id '{prompt.id}' must match the file name.")

    declared = set(prompt.variable_names)
    used = set(prompt.placeholders_in_body)

    if undeclared := sorted(used - declared):
        raise PromptError(f"{label}: placeholders not declared as variables: {', '.join(undeclared)}")
    if unused := sorted(declared - used):
        raise PromptError(f"{label}: variables never used in the prompt text: {', '.join(unused)}")

    required = {v.name for v in prompt.variables if v.required}
    if lacking := sorted(required - set(prompt.example)):
        raise PromptError(f"{label}: example is missing values for: {', '.join(lacking)}")
    if stray := sorted(set(prompt.example) - declared):
        raise PromptError(f"{label}: example has values for unknown variables: {', '.join(stray)}")


def _ensure_unique_ids(prompts: list[Prompt]) -> None:
    seen: set[str] = set()
    for prompt in prompts:
        if prompt.id in seen:
            raise PromptError(f"Duplicate prompt id: '{prompt.id}'")
        seen.add(prompt.id)
