"""Render the map as RESOURCES.md, readable on GitHub with no JavaScript."""

from __future__ import annotations


def render_markdown(data: dict) -> str:
    parts = [
        f"# {data['title']}",
        data["subtitle"],
        f"Links were checked on {data['checked']}. Pages move, so edit `resources.json` and run `python build.py` to refresh this file.",
    ]
    parts.extend(_render_stage(stage) for stage in data["stages"])
    return "\n\n".join(parts) + "\n"


def _render_stage(stage: dict) -> str:
    start = [r for r in stage["resources"] if r["tier"] == "start"]
    deeper = [r for r in stage["resources"] if r["tier"] == "deeper"]

    lines = [f"## {stage['title']}", "", stage["goal"], ""]
    lines += ["**Start here**", ""] + [_render_resource(r) for r in start] + [""]
    if deeper:
        lines += ["**Go deeper**", ""] + [_render_resource(r) for r in deeper] + [""]
    lines += [
        f"**Stage gate: build it.** {stage['gate']['build']}",
        "",
        f"**Check yourself.** {stage['gate']['check']}",
    ]
    return "\n".join(lines)


def _render_resource(resource: dict) -> str:
    return f"- [{resource['title']}]({resource['url']}) ({resource['type']}, {resource['cost']}): {resource['note']}"
