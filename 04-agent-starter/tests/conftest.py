import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from miniagent.tools import build_tools  # noqa: E402


@pytest.fixture
def data_dir() -> Path:
    return ROOT / "data"


@pytest.fixture
def output_dir(tmp_path) -> Path:
    return tmp_path / "output"


@pytest.fixture
def tools(data_dir, output_dir):
    return build_tools(data_dir, output_dir)


@pytest.fixture
def tool_by_name(tools):
    return {tool.name: tool for tool in tools}
