# 06-prompt-library

Twelve reusable prompts for delivery management, kept as plain Markdown files, plus a small Python tool to fill them in and test them. See [CATALOG.md](CATALOG.md) for the full list.

| Category | Prompts |
|---|---|
| Reporting | weekly status report, steering committee brief |
| Communication | stakeholder update email, escalation message |
| Risk | risk log entry, risk log review |
| Planning | RAID items from notes, delay or change impact assessment |
| Meetings | meeting decisions and actions |
| Team | retrospective themes |
| Learning | PMP-style practice questions |
| Privacy | redaction check |

## Quick start

```bash
pip install -r requirements.txt

python -m promptlib list
python -m promptlib show weekly-status-report
python -m promptlib fill weekly-status-report --example     # fictional sample values
```

Fill one with your own text, then paste the output into the AI tool you are cleared to use:

```bash
python -m promptlib fill meeting-actions \
    --var meeting_date="21 Jan" \
    --file notes=my_notes.txt
```

`--var NAME=VALUE` sets a short value and `--file NAME=PATH` reads a long one from a text file. A typo in a name, or a missing required value, stops with a clear message instead of producing a half-filled prompt.

## What a prompt file looks like

```
---
id: escalation-message           # must match the file name
title: Escalation message
category: communication
purpose: One line on what it does.
variables:                       # values you supply
  - name: issue
    description: What is wrong.
  - name: tone
    description: Voice to use.
    required: false              # optional variables need a default
    default: calm and factual
tips: Advice for the person using it.
criteria: What a good answer looks like. Used when testing the prompt.
example:                         # fictional sample values
  issue: The vendor has not confirmed the test environment date.
---
Write an escalation about {{issue}} in a {{tone}} tone.
```

The loader checks every file: the id matches the name, every `{{placeholder}}` is declared, every declared variable is used, and the example covers all required values. `python -m pytest` runs those checks, so a bad edit is caught straight away.

## How the prompts are written

- Your input goes inside labelled tags such as `<notes>`, so the model can tell your material from the instructions.
- Each prompt names the output format and a length limit.
- Each says what to do when information is missing ("Not provided"), so the model does not invent dates, names or numbers.
- Owners are suggested by role, never by name, and the retrospective prompt asks the model not to name individuals.

## Test the prompts with your eval toolkit

`export-suite` turns every prompt into a test case for `02-ai-eval-toolkit`: its example is filled in, and its `criteria` become a rubric check for a judge model.

```bash
python -m promptlib export-suite --out prompt_suite.yaml

cd ../02-ai-eval-toolkit
python -m evaltoolkit run ../06-prompt-library/prompt_suite.yaml \
    --model anthropic:<model-id> --model ollama:llama3.1 \
    --judge anthropic:<model-id>
```

Offline, you can try the plumbing with `--model mock:careful --judge mock:judge`. The mock models know nothing about these prompts, so that run only proves the pieces connect.

## Add your own prompt

1. Copy any file in `prompts/` and change the front matter and text.
2. Run `python -m pytest` to check it.
3. Run `python -m promptlib catalog` to refresh `CATALOG.md`.

## Privacy

- Examples are fictional. A test fails if an example holds an email that does not end in `@example.com`.
- Remove names and client details from real notes before using any AI tool you have not been cleared to use. The `redaction-check` prompt helps, but run it only in a local or approved tool, because the text you give it still contains the sensitive details.

## Things to try

- Run the suite on two models and see which prompts score lowest. Rewrite one and compare.
- Add a `no_pii` check to the exported cases for prompts whose output should never contain contact details.
- Add a `--format json` option to `fill` so a prompt can feed another script.
