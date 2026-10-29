"""Command line for the prompt library.

    python -m promptlib list
    python -m promptlib show weekly-status-report
    python -m promptlib fill weekly-status-report --example
    python -m promptlib fill risk-log-entry --var concern="Vendor may miss the March date" --file project_context=context.txt
    python -m promptlib catalog
    python -m promptlib export-suite --out suite.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .catalog import render_catalog
from .errors import PromptError
from .export_suite import build_suite, dump_suite
from .filler import fill
from .loader import load_prompts
from .model import Prompt

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPT_DIR = ROOT / "prompts"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="promptlib", description="Keep, fill and test reusable prompts.")
    parser.add_argument("--dir", type=Path, default=DEFAULT_PROMPT_DIR, help="folder of prompt files")
    commands = parser.add_subparsers(dest="command", required=True)

    listing = commands.add_parser("list", help="list prompts")
    listing.add_argument("--category", help="show only this category")
    listing.set_defaults(handler=_cmd_list)

    show = commands.add_parser("show", help="show one prompt with its variables, example and tips")
    show.add_argument("id")
    show.set_defaults(handler=_cmd_show)

    fill_cmd = commands.add_parser("fill", help="print a prompt with its placeholders filled")
    fill_cmd.add_argument("id")
    fill_cmd.add_argument("--var", action="append", default=[], metavar="NAME=VALUE", help="set a value; repeatable")
    fill_cmd.add_argument("--file", action="append", default=[], metavar="NAME=PATH", help="set a value from a text file; repeatable")
    fill_cmd.add_argument("--example", action="store_true", help="start from the prompt's example values")
    fill_cmd.add_argument("--allow-missing", action="store_true", help="leave unfilled {{placeholders}} in place")
    fill_cmd.set_defaults(handler=_cmd_fill)

    catalog = commands.add_parser("catalog", help="write CATALOG.md")
    catalog.add_argument("--out", type=Path, default=ROOT / "CATALOG.md")
    catalog.set_defaults(handler=_cmd_catalog)

    export = commands.add_parser("export-suite", help="write an eval-toolkit suite built from the examples")
    export.add_argument("--out", type=Path, default=Path("prompt_suite.yaml"))
    export.set_defaults(handler=_cmd_export)

    return parser


# ---- commands ----------------------------------------------------------------


def _cmd_list(args: argparse.Namespace) -> int:
    for prompt in load_prompts(args.dir):
        if args.category and prompt.category != args.category:
            continue
        print(f"{prompt.id:<28} {prompt.category:<14} {prompt.title}")
    return 0


def _cmd_show(args: argparse.Namespace) -> int:
    prompt = _find(load_prompts(args.dir), args.id)
    print(f"{prompt.title}  ({prompt.category})\n{prompt.purpose}\n")
    print("Variables:")
    for variable in prompt.variables:
        marker = "required" if variable.required else f"optional, default {variable.default!r}"
        print(f"  {variable.name} ({marker}): {variable.description}")
    print(f"\nTips: {prompt.tips}\n\n--- prompt ---\n{prompt.body}")
    return 0


def _cmd_fill(args: argparse.Namespace) -> int:
    prompt = _find(load_prompts(args.dir), args.id)
    values = dict(prompt.example) if args.example else {}
    values.update(_parse_pairs(args.var))
    values.update({name: Path(path).read_text(encoding="utf-8") for name, path in _parse_pairs(args.file).items()})
    print(fill(prompt, values, allow_missing=args.allow_missing), end="")
    return 0


def _cmd_catalog(args: argparse.Namespace) -> int:
    args.out.write_text(render_catalog(load_prompts(args.dir)), encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    args.out.write_text(dump_suite(build_suite(load_prompts(args.dir))), encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


# ---- helpers -------------------------------------------------------------------


def _find(prompts: list[Prompt], prompt_id: str) -> Prompt:
    for prompt in prompts:
        if prompt.id == prompt_id:
            return prompt
    known = ", ".join(p.id for p in prompts)
    raise PromptError(f"No prompt called '{prompt_id}'. Available: {known}")


def _parse_pairs(items: list[str]) -> dict[str, str]:
    pairs = {}
    for item in items:
        name, separator, value = item.partition("=")
        if not separator or not name:
            raise PromptError(f"Expected NAME=VALUE, got '{item}'")
        pairs[name] = value
    return pairs


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except (PromptError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
