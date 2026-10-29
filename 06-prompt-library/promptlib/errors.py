"""Exception types for the prompt library."""


class PromptError(Exception):
    """A prompt file is malformed, or a request for one cannot be met."""


class MissingVariablesError(PromptError):
    """Filling a prompt failed because required values were not supplied."""

    def __init__(self, prompt_id: str, names: list[str]) -> None:
        self.names = names
        super().__init__(f"Prompt '{prompt_id}' needs values for: {', '.join(names)}")
