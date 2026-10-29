"""Command line.

    python -m miniagent run "Draft a status note from the risk log and milestones." --model mock:scripted
    python -m miniagent run "Draft a status note and save it." --model anthropic:<model-id>
    python -m miniagent tools
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .errors import AgentError
from .loop import run_agent
from .models import SUPPORTED_PROVIDERS, create_model
from .prompts import SYSTEM_PROMPT
from .tools import build_tools
from .trace import format_step, save_trace
from .types import Step, ToolCall

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_DIR = ROOT / "output"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="miniagent", description="A tiny tool-using agent for status notes.")
    commands = parser.add_subparsers(dest="command", required=True)

    run = commands.add_parser("run", help="give the agent a task")
    run.add_argument("task", help="what you want the agent to do")
    run.add_argument("--model", required=True, metavar="PROVIDER:MODEL", help=f"providers: {', '.join(SUPPORTED_PROVIDERS)}")
    run.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="folder holding risk_log.csv and milestones.csv")
    run.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="the only folder the agent may write to")
    run.add_argument("--max-steps", type=int, default=8, help="stop after this many model turns")
    run.add_argument("--yes", action="store_true", help="approve every action without asking (use with care)")
    run.add_argument("--trace", type=Path, help="save the full run as JSON to this path")
    run.add_argument("--quiet", action="store_true", help="do not print each step")
    run.set_defaults(handler=_cmd_run)

    tools = commands.add_parser("tools", help="list the agent's tools")
    tools.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    tools.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    tools.set_defaults(handler=_cmd_tools)

    return parser


def _cmd_run(args: argparse.Namespace) -> int:
    model = create_model(args.model)
    tools = build_tools(args.data_dir, args.output_dir)
    approve = _approve_all if args.yes else _ask_person
    on_step = None if args.quiet else _print_step

    result = run_agent(args.task, model, tools, SYSTEM_PROMPT, max_steps=args.max_steps, approve=approve, on_step=on_step)

    if args.trace:
        save_trace(result, args.trace)
        print(f"trace saved to {args.trace}", file=sys.stderr)

    if result.stop_reason == "max_steps":
        print(f"Stopped: reached the limit of {args.max_steps} steps without a final answer.", file=sys.stderr)
        return 1
    print(result.final_text)
    return 0


def _cmd_tools(args: argparse.Namespace) -> int:
    for tool in build_tools(args.data_dir, args.output_dir):
        approval = "  [needs approval]" if tool.needs_approval else ""
        print(f"{tool.name}{approval}\n  {tool.description}\n")
    return 0


def _print_step(step: Step) -> None:
    print(format_step(step), file=sys.stderr)


def _approve_all(call: ToolCall) -> bool:
    return True


def _ask_person(call: ToolCall) -> bool:
    """Ask on the terminal. With no terminal input available, the answer is no."""
    print(f"\nThe agent wants to run {call.name} with: {call.arguments}", file=sys.stderr)
    try:
        answer = input("Allow this? [y/N] ")
    except EOFError:
        return False
    return answer.strip().lower() in ("y", "yes")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except AgentError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
