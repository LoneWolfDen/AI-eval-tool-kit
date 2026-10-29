# ai-eval-toolkit

A small, modular Python toolkit for evaluating LLM answers. You write test cases in YAML, run them against one or more models, and get a console summary plus Markdown, HTML and JSON reports.

It is built for learning. Every file does one job, uses the standard library wherever possible, and is short enough to read in a few minutes.

## Quick start (no API key needed)

```bash
pip install -r requirements.txt
python -m evaltoolkit run examples/suite_basic.yaml \
    --model mock:careful --model mock:sloppy --judge mock:judge
```

This runs two fake models against the example suite. Open `reports/report.html` in a browser to see the comparison. A sample is in `examples/sample-output/`.

Run the tests with `python -m pytest`.

## Using real models

| Provider | Example flag | Needs |
|---|---|---|
| Anthropic | `--model anthropic:<model-id>` | `pip install anthropic`, `ANTHROPIC_API_KEY` |
| Ollama (local) | `--model ollama:llama3.1` | Ollama running on port 11434 |
| LM Studio (local) | `--model lmstudio:<name>` | Local server on port 1234 |
| OpenAI | `--model openai:<model-id>` | `OPENAI_API_KEY` |

Repeat `--model` to compare several models side by side. Use `--judge provider:model` for `rubric` checks. A stronger model than the one under test is the usual choice.

```bash
python -m evaltoolkit run my_suite.yaml --model ollama:llama3.1 --model anthropic:<model-id> --judge anthropic:<model-id>
```

Use `--fail-under 90` to exit with code 1 when any model scores below 90% (handy in CI).

## Writing a suite

```yaml
name: my-suite
cases:
  - id: fact-pmp
    tags: [accuracy]
    system: "Optional system prompt"
    prompt: "What does PMP stand for?"
    checks:
      - type: contains
        value: Project Management Professional
```

Run `python -m evaltoolkit checks` to list check types. All of them:

| Type | Passes when | Key options |
|---|---|---|
| `contains` | answer includes the text | `value` (string or list), `match: all/any`, `case_sensitive` |
| `not_contains` | answer includes none of the text | `value`, `case_sensitive` |
| `exact` | answer equals the text | `value`, `strip`, `case_sensitive` |
| `regex` | pattern is found (or not, with `must_match: false`) | `pattern`, `ignore_case` |
| `max_words` / `min_words` | word count within limit | `limit` / `minimum` |
| `no_pii` | no email, phone, UK NI number or card number found | `kinds` |
| `rubric` | a judge model scores it at or above `min_score` (1-5) | `criteria`, `min_score` |

A case passes only when all of its checks pass.

## How it fits together

```
evaltoolkit/
  types.py        data containers (EvalCase, CheckResult, SuiteResult, ...)
  loader.py       YAML file  -> validated EvalSuite
  clients/        one file per provider; all implement ModelClient.generate()
  scorers/        one file per check type; all implement Scorer.score()
  runner.py       suite + client + judge -> SuiteResult
  reports/        SuiteResult -> console / markdown / html / json
  cli.py          argparse wiring only
```

Data flows one way: `loader -> runner -> reports`. The runner never prints and the reports never call models, which makes each stage easy to test and swap.

## Extending it

**New check**: create `scorers/my_check.py` with a `Scorer` subclass (set `type_name`, implement `score`), then add the class to the tuple in `scorers/__init__.py`. It is immediately usable as `type: my_check` in YAML.

**New provider**: create `clients/my_provider.py` with a `ModelClient` subclass, then add a branch in `create_client` in `clients/__init__.py`.

**New report**: write a `render_xxx(results) -> str` function in `reports/` and add it to `FILE_REPORTS`.

## Things to try yourself

1. Write a 10-case suite from your real work (status summaries, risk wording, stakeholder replies) and run it on two models.
2. Add a `json_valid` check, then a `starts_with` check. Each should take under 20 lines.
3. Test your judge: run the same `rubric` check with two different judge models and compare where they disagree.
4. Add a `--repeats N` option to the runner and measure how often a model's answer flips between runs.
5. Build a privacy red-team suite: prompts that try to extract personal data or hidden instructions, checked with `no_pii` and `not_contains`.
6. Probe judge bias: give the judge a long but vague answer and a short precise one. Which scores higher?

## Similar tools to compare with

These are established open-source evaluation projects. Check each README for current features.

- [promptfoo](https://github.com/promptfoo/promptfoo): YAML-driven prompt and model testing, including red-teaming.
- [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai): evaluation framework from the UK AI Security Institute.
- [DeepEval](https://github.com/confident-ai/deepeval): pytest-style LLM tests with many built-in metrics.
- [Ragas](https://github.com/explodinggradients/ragas): metrics for retrieval-augmented generation.
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness): standard academic benchmarks.
- [OpenAI Evals](https://github.com/openai/evals): eval registry and framework.

## Limits to keep in mind

- The `no_pii` detectors are simple heuristics for catching obvious leaks. They are not a compliance tool.
- LLM judges can be inconsistent or biased. Spot-check their verdicts against your own reading.
- Checks like `contains` are brittle for open-ended answers. Pair them with a `rubric` where wording varies.
- Mock models exist only to demo and test the toolkit. Their results say nothing about real models.
