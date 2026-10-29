"""evaltoolkit: a small, modular toolkit for evaluating LLM outputs.

Flow of data through the package:

    YAML suite --loader--> EvalSuite --runner--> SuiteResult --reports--> md / html / json

Each stage lives in its own module so you can swap or extend one
without touching the others.
"""

__version__ = "0.1.0"
