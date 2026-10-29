"""Client for any server that speaks the OpenAI chat-completions format.

That covers Ollama, LM Studio, vLLM and OpenAI itself. It uses only the
standard library (urllib), so no extra package is needed.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from .base import ModelClient
from ..errors import ClientError

# provider name -> connection settings
PRESETS = {
    "ollama": {"base_url": "http://localhost:11434/v1", "api_key_env": None, "temperature": 0.0},
    "lmstudio": {"base_url": "http://localhost:1234/v1", "api_key_env": None, "temperature": 0.0},
    "openai": {"base_url": "https://api.openai.com/v1", "api_key_env": "OPENAI_API_KEY", "temperature": None},
}


class OpenAICompatClient(ModelClient):
    def __init__(
        self,
        provider: str,
        model: str,
        base_url: str | None = None,
        timeout_s: float = 120.0,
    ) -> None:
        preset = PRESETS[provider]
        self._base_url = (base_url or preset["base_url"]).rstrip("/")
        self._model = model
        self._temperature = preset["temperature"]
        self._timeout_s = timeout_s
        self._api_key = self._read_api_key(preset["api_key_env"])
        self.name = f"{provider}:{model}"

    @staticmethod
    def _read_api_key(env_var: str | None) -> str | None:
        if env_var is None:
            return None
        key = os.environ.get(env_var)
        if not key:
            raise ClientError(f"Set the {env_var} environment variable first.")
        return key

    def generate(self, prompt: str, system: str | None = None) -> str:
        payload = {"model": self._model, "messages": self._build_messages(prompt, system)}
        if self._temperature is not None:
            payload["temperature"] = self._temperature

        reply = self._post("/chat/completions", payload)

        try:
            return reply["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError) as exc:
            raise ClientError(f"Unexpected response shape: {reply!r}") from exc

    @staticmethod
    def _build_messages(prompt: str, system: str | None) -> list[dict[str, str]]:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return messages

    def _post(self, path: str, payload: dict) -> dict:
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        request = urllib.request.Request(
            self._base_url + path,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout_s) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:300]
            raise ClientError(f"HTTP {exc.code} from {self._base_url}: {body}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ClientError(f"Could not reach {self._base_url}: {exc}") from exc
