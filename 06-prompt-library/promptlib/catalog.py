"""Generate CATALOG.md, a browsable overview of every prompt."""

from __future__ import annotations

from itertools import groupby

from .model import Prompt


def render_catalog(prompts: list[Prompt]) -> str:
    parts = [
        "# Prompt catalog",
        f"{len(prompts)} prompts for delivery management. Each links to its file, which holds the full prompt, "
        "an example and tips.",
        "To fill one: `python -m promptlib fill <id> --example`, or supply your own values with `--var name=value`.",
    ]
    for category, group in groupby(prompts, key=lambda p: p.category):
        parts.append(_render_category(category, list(group)))
    return "\n\n".join(parts) + "\n"


def _render_category(category: str, prompts: list[Prompt]) -> str:
    rows = ["| Prompt | What it does | Inputs |", "|---|---|---|"]
    for prompt in prompts:
        link = f"[{prompt.title}](prompts/{prompt.id}.md)"
        rows.append(f"| {link} (`{prompt.id}`) | {prompt.purpose} | {_describe_inputs(prompt)} |")
    return f"## {category.capitalize()}\n\n" + "\n".join(rows)


def _describe_inputs(prompt: Prompt) -> str:
    names = [v.name if v.required else f"{v.name} (optional)" for v in prompt.variables]
    return ", ".join(f"`{name}`" for name in names)
