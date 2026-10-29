"""Exception types, so callers can catch toolkit problems specifically."""


class EvalToolkitError(Exception):
    """Base class for every error this package raises on purpose."""


class SuiteError(EvalToolkitError):
    """The YAML suite file is missing, malformed or inconsistent."""


class ConfigError(EvalToolkitError):
    """The run is configured wrongly (unknown scorer, missing judge, ...)."""


class ClientError(EvalToolkitError):
    """A model client could not be created or a model call failed."""
