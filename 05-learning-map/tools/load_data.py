"""Load resources.json and check it, so mistakes show up at build time."""

from __future__ import annotations

import json
from pathlib import Path

RESOURCE_TYPES = {"course", "read", "repo", "guidance"}
TIERS = {"start", "deeper"}

_MAP_KEYS = ("title", "subtitle", "checked", "stages")
_STAGE_KEYS = ("id", "short", "title", "goal", "color", "color_dark", "gate", "resources")
_RESOURCE_KEYS = ("id", "title", "url", "type", "tier", "note", "cost")


class MapDataError(ValueError):
    """resources.json is missing something or contains a bad value."""


def load_map(path: str | Path) -> dict:
    """Read the JSON file, validate it and return it as a dict."""
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MapDataError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise MapDataError(f"{path} is not valid JSON: {exc}") from exc

    validate_map(data)
    return data


def validate_map(data: dict) -> None:
    _require_keys(data, _MAP_KEYS, "map")
    if not data["stages"]:
        raise MapDataError("map needs at least one stage")

    seen_ids: set[str] = set()
    for stage in data["stages"]:
        _validate_stage(stage, seen_ids)


def _validate_stage(stage: dict, seen_ids: set[str]) -> None:
    _require_keys(stage, _STAGE_KEYS, "stage")
    label = f"stage '{stage['id']}'"
    _require_keys(stage["gate"], ("build", "check"), f"{label} gate")
    if not stage["resources"]:
        raise MapDataError(f"{label} has no resources")

    _claim_id(f"{stage['id']}:gate", seen_ids)
    for resource in stage["resources"]:
        _validate_resource(resource, label, seen_ids)


def _validate_resource(resource: dict, stage_label: str, seen_ids: set[str]) -> None:
    _require_keys(resource, _RESOURCE_KEYS, f"{stage_label} resource")
    label = f"resource '{resource['id']}'"

    if resource["type"] not in RESOURCE_TYPES:
        raise MapDataError(f"{label}: type must be one of {sorted(RESOURCE_TYPES)}")
    if resource["tier"] not in TIERS:
        raise MapDataError(f"{label}: tier must be one of {sorted(TIERS)}")
    if not resource.get("internal") and not resource["url"].startswith("https://"):
        raise MapDataError(f"{label}: external links must start with https://")

    _claim_id(resource["id"], seen_ids)


def _claim_id(identifier: str, seen_ids: set[str]) -> None:
    """Ids double as progress-tracking keys, so each must be unique."""
    if identifier in seen_ids:
        raise MapDataError(f"duplicate id '{identifier}'")
    seen_ids.add(identifier)


def _require_keys(item: dict, keys: tuple[str, ...], label: str) -> None:
    missing = [key for key in keys if key not in item]
    if missing:
        raise MapDataError(f"{label} is missing: {', '.join(missing)}")
