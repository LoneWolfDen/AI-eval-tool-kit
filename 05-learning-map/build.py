"""Regenerate index.html and RESOURCES.md from resources.json.

    python build.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from tools.load_data import MapDataError, load_map
from tools.render_html import render_html
from tools.render_markdown import render_markdown

ROOT = Path(__file__).resolve().parent


def main() -> int:
    try:
        data = load_map(ROOT / "resources.json")
    except MapDataError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    outputs = {
        ROOT / "index.html": render_html(data),
        ROOT / "RESOURCES.md": render_markdown(data),
    }
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
