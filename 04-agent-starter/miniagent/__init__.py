"""miniagent: a tiny tool-using agent, written out in full so you can read every step.

The idea in one picture:

    task --> model --(asks for tools)--> your code runs the tools
                ^                                  |
                +----------(results go back)-------+
    ...repeat until the model answers without asking for a tool.

Modules: types (data), loop (the agent loop), tools/ (what the agent can do),
models/ (who does the thinking), trace (what to show and save), cli (the command line).
"""
