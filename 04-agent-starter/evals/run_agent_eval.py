"""Evaluate the agent end to end with 02-ai-eval-toolkit.

The toolkit tests anything that turns a prompt into an answer. Here that
"anything" is the whole agent: AgentAsClient runs the full loop and returns the
final text, so every check in agent_cases.yaml sees what a user would see.

    python evals/run_agent_eval.py --model mock:scripted --judge mock:judge
    python evals/run_agent_eval.py --model anthropic:<model-id> --judge anthropic:<model-id>

The judge is a toolkit model spec (see 02-ai-eval-toolkit). The mock judge
always says 4/5, so it only proves the pieces connect.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
AGENT_ROOT = HERE.parent
TOOLKIT_ROOT = AGENT_ROOT.parent / "02-ai-eval-toolkit"

sys.path.insert(0, str(AGENT_ROOT))
sys.path.insert(0, str(TOOLKIT_ROOT))

try:
    from evaltoolkit.clients import create_client
    from evaltoolkit.clients.base import ModelClient
    from evaltoolkit.errors import EvalToolkitError
    from evaltoolkit.loader import load_suite
    from evaltoolkit.reports import render_console, write_reports
    from evaltoolkit.runner import run_suite
except ImportError as exc:  # the toolkit lives in a sibling folder of this repo
    sys.exit(f"Could not import 02-ai-eval-toolkit from {TOOLKIT_ROOT}: {exc}")

from miniagent.errors import AgentError
from miniagent.loop import run_agent
from miniagent.models import create_model
from miniagent.prompts import SYSTEM_PROMPT
from miniagent.tools import build_tools


class AgentAsClient(ModelClient):
    """Lets the toolkit treat the whole agent as if it were a model."""

    def __init__(self, model_spec: str, data_dir: Path, max_steps: int = 8) -> None:
        self._model = create_model(model_spec)
        self._data_dir = data_dir
        self._max_steps = max_steps
        self.name = f"agent[{self._model.name}]"

    def generate(self, prompt: str, system: str | None = None) -> str:
        with tempfile.TemporaryDirectory() as scratch:  # any notes the agent saves are thrown away
            tools = build_tools(self._data_dir, Path(scratch))
            try:
                result = run_agent(
                    prompt, self._model, tools, system or SYSTEM_PROMPT,
                    max_steps=self._max_steps, approve=lambda call: True,
                )
            except AgentError as exc:
                raise EvalToolkitError(str(exc)) from exc
        return result.final_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the agent through the eval toolkit.")
    parser.add_argument("--model", required=True, help="agent model spec, e.g. mock:scripted")
    parser.add_argument("--judge", help="toolkit model spec used by rubric checks, e.g. mock:judge")
    parser.add_argument("--suite", type=Path, default=HERE / "agent_cases.yaml")
    parser.add_argument("--data-dir", type=Path, default=AGENT_ROOT / "data")
    parser.add_argument("--out", type=Path, default=HERE / "reports")
    args = parser.parse_args()

    try:
        suite = load_suite(args.suite)
        judge = create_client(args.judge) if args.judge else None
        result = run_suite(suite, AgentAsClient(args.model, args.data_dir), judge)
    except (EvalToolkitError, AgentError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(render_console([result]))
    for path in write_reports([result], args.out):
        print(f"wrote {path}")
    return 0 if all(case.passed for case in result.cases) else 1


if __name__ == "__main__":
    sys.exit(main())
