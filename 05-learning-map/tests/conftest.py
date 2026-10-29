import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.load_data import load_map  # noqa: E402


@pytest.fixture
def map_data():
    return load_map(ROOT / "resources.json")
