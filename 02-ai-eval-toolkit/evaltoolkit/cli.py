"""Command-line interface.

    python -m evaltoolkit run examples/suite_basic.yaml --model mock:careful --model mock:sloppy --judge mock:judge
    python -m evaltoolkit checks
"""

from __future__ import annotations

import argparse
import sys

from .clients import SUPPORTED_PROVIDERS, create_client
from .errors import EvalToolkitError
from .loader import load_suite
from .reports import render_console, write_reports
from .reports.summary import status_label, summarize
from .runner import run_suite
from .scorers import SCORER_TYPES
from .types import CaseResult


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evaltoolkit", description="Evaluate LLM answers against a YAML suite.")
    commands = parser.add_subparsers(dest="command", required=True)

    run = commands.add_parser("run", help="run a suite against one or more models")
    run.add_argument("suite", help="path to a YAML suite file")
    run.add_argument(
        "--model",
        action="append",
        required=True,
        metavar="PROVIDER:MODEL",
        help=f"model to test; repeat to compare several. Providers: {', '.join(SUPPORTED_PROVIDERS)}",
    )
    run.add_argument("--judge", metavar="PROVIDER:MODEL", help="model used by 'rubric' checks")
    run.add_argument("--out", default="reports", help="folder for report files (default: reports)")
    run.add_argument("--fail-under", type=float, metavar="PCT", help="exit with code 1 if any model's pass rate is below PCT")
    run.set_defaults(handler=_cmd_run)

    checks = commands.add_parser("checks", help="list the available check types")
    checks.set_defaults(handler=_cmd_checks)

    return parser


def _cmd_run(args: argparse.Namespace) -> int:
    suite = load_suite(args.suite)
    judge = create_client(args.judge) if args.judge else None
    clients = [create_client(spec) for spec in args.model]

    results = []
    for client in clients:
        print(f"Running '{suite.name}' on {client.name} ...", file=sys.stderr)
        results.append(run_suite(suite, client, judge, on_case_done=_print_progress))

    print()
    print(render_console(results))
    for path in write_reports(results, args.out):
        print(f"wrote {path}")

    return _exit_code(results, args.fail_under)


def _print_progress(model: str, case_result: CaseResult) -> None:
    print(f"  {case_result.case.id:<28} {status_label(case_result)}", file=sys.stderr)


def _exit_code(results, fail_under: float | None) -> int:
    if fail_under is None:
        return 0
    below = [summarize(r).model for r in results if summarize(r).pass_rate * 100 < fail_under]
    if below:
        print(f"Pass rate below {fail_under}% for: {', '.join(below)}", file=sys.stderr)
        return 1
    return 0


def _cmd_checks(args: argparse.Namespace) -> int:
    for name in sorted(SCORER_TYPES):
        summary = (SCORER_TYPES[name].__doc__ or "").strip().splitlines()[0]
        print(f"{name:<14} {summary}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except EvalToolkitError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
