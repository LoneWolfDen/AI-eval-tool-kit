import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from promptlib.loader import load_prompts  # noqa: E402


@pytest.fixture(scope="session")
def prompts():
    return load_prompts(ROOT / "prompts")


@pytest.fixture
def prompt_dir() -> Path:
    return ROOT / "prompts"
