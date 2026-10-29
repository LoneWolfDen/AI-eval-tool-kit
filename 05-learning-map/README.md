# 05-learning-map

A route map for learning AI evaluation, agents, privacy and team guidance using free resources. Open `index.html` in any browser, or read `RESOURCES.md` on GitHub.

The page is drawn like a transit map. Each stage is a coloured line, each resource is a stop you tick, and each stage ends in a square gate stop where you build something and answer one question. Progress is saved in your browser only.

## The five stages

| Stage | You will be able to |
|---|---|
| Prompting basics | Write clear prompts and explain why they work |
| AI evaluation | Test whether answers are good, with repeatable suites |
| Agents | Explain how tool-using agents work and when a workflow is better |
| Privacy and security | Spot where personal data can leak, and what the guidance expects |
| Governance and team guidance | Write rules your team can follow without asking you |

Each stage has "Start here" stops and a collapsed "Go deeper" list. The start stops are 16 resources plus 5 gates, 21 in all. The deeper lists add 19 more resources.

A suggested pace is two or three hours a week, about two weeks per stage. That is a suggestion, so adjust it to your own schedule.

## Update the map

Everything lives in `resources.json`. Edit it, then rebuild:

```bash
python build.py
python -m pytest        # optional: checks the data and the rendered page
```

`build.py` validates the data, then writes `index.html` (one self-contained file, no external requests) and `RESOURCES.md`.

## Files

```
resources.json        the single source of truth: stages, resources, gates
build.py              entry point: validate, then write both outputs
tools/load_data.py    loads and validates resources.json
tools/render_html.py  fills src/template.html with CSS, JavaScript and data
tools/render_markdown.py  writes RESOURCES.md
src/template.html     page skeleton
src/style.css         transit-map styling (light and dark)
src/app.js            builds the map, ticks, filters and progress
tests/                data validation and render checks
index.html            generated
RESOURCES.md          generated
```

## Things to try

- Add your own stops: a book, a course at work, a talk. Pick a type (`course`, `read`, `repo`, `guidance`) and a tier (`start`, `deeper`).
- Add a sixth stage for a topic you care about, and give it a colour pair (`color` for light mode, `color_dark` for dark mode).
- Change a gate to match a real task at work, so ticking it means you shipped something.

## About the links

Links were checked on 29 October 2026 using search results, and each course's cost was read from its own page at the time. The DeepLearning.AI course was free to enrol during its platform beta, with the certificate behind a paid plan. Prices and availability change, so check before you start.
