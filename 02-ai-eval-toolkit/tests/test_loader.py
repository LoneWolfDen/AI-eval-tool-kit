import pytest

from evaltoolkit.errors import SuiteError
from evaltoolkit.loader import load_suite, parse_suite


def test_example_suite_loads(example_suite_path):
    suite = load_suite(example_suite_path)
    assert suite.name == "delivery-assistant-basics"
    assert len(suite.cases) == 7
    assert suite.cases[0].checks[0].type == "contains"


def test_check_params_exclude_the_type_key():
    suite = parse_suite({"cases": [{"id": "a", "prompt": "p", "checks": [{"type": "exact", "value": "x"}]}]})
    assert suite.cases[0].checks[0].params == {"value": "x"}


def test_missing_file_is_a_suite_error(tmp_path):
    with pytest.raises(SuiteError, match="not found"):
        load_suite(tmp_path / "nope.yaml")


@pytest.mark.parametrize(
    "raw, message",
    [
        ("just text", "mapping"),
        ({"cases": []}, "non-empty 'cases'"),
        ({"cases": [{"prompt": "p", "checks": [{"type": "exact"}]}]}, "missing an 'id'"),
        ({"cases": [{"id": "a", "checks": [{"type": "exact"}]}]}, "missing a 'prompt'"),
        ({"cases": [{"id": "a", "prompt": "p"}]}, "non-empty 'checks'"),
        ({"cases": [{"id": "a", "prompt": "p", "checks": [{"value": "x"}]}]}, "needs a 'type'"),
    ],
)
def test_invalid_suites_give_readable_errors(raw, message):
    with pytest.raises(SuiteError, match=message):
        parse_suite(raw)


def test_duplicate_ids_are_rejected():
    case = {"id": "same", "prompt": "p", "checks": [{"type": "exact", "value": "x"}]}
    with pytest.raises(SuiteError, match="Duplicate case id"):
        parse_suite({"cases": [case, case]})
