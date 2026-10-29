"""Render index.html: one self-contained file (CSS, JavaScript and data inlined)."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"


def render_html(data: dict, src_dir: Path = SRC_DIR) -> str:
    template = (src_dir / "template.html").read_text(encoding="utf-8")
    replacements = {
        "{{TITLE}}": escape(data["title"]),
        "{{SUBTITLE}}": escape(data["subtitle"]),
        "{{CHECKED}}": escape(data["checked"]),
        "{{STYLE}}": (src_dir / "style.css").read_text(encoding="utf-8"),
        "{{SCRIPT}}": (src_dir / "app.js").read_text(encoding="utf-8"),
        "{{DATA_JSON}}": _json_for_script_tag(data),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


def _json_for_script_tag(data: dict) -> str:
    """Serialise data so that nothing inside it can close the <script> tag early."""
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
