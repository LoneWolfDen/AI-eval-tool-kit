"""Exception types."""


class AgentError(Exception):
    """Base class for errors this package raises on purpose."""


class ToolError(AgentError):
    """A tool could not do what the model asked.

    The message is sent back to the model, so write it as advice the model can
    act on, for example "status must be one of: active, open, closed".
    """


class ModelError(AgentError):
    """The model could not be created or called."""
