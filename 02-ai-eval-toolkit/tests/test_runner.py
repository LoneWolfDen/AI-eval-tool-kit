import pytest

from evaltoolkit.clients.base import ModelClient
from evaltoolkit.clients.mock import MockClient
from evaltoolkit.errors import ClientError, ConfigError
from evaltoolkit.loader import load_suite
from evaltoolkit.runner import run_suite


class BrokenClient(ModelClient):
    name = "broken"

    def generate(self, prompt, system=None):
        raise ClientError("connection refused")


def test_careful_mock_passes_everything(example_suite_path):
    suite = load_suite(example_suite_path)
    result = run_suite(suite, MockClient("careful"), judge=MockClient("judge"))
    assert all(case.passed for case in result.cases)


def test_sloppy_mock_fails_the_cases_it_was_designed_to_fail(example_suite_path):
    suite = load_suite(example_suite_path)
    result = run_suite(suite, MockClient("sloppy"), judge=MockClient("judge"))
    failed = {case.case.id for case in result.cases if not case.passed}
    assert {"fact-pmp", "format-one-word", "brevity-raid", "privacy-contact-details", "injection-system-prompt"} <= failed


def test_model_errors_are_recorded_not_raised(example_suite_path):
    suite = load_suite(example_suite_path)
    result = run_suite(suite, BrokenClient(), judge=MockClient("judge"))
    assert all(case.error == "connection refused" for case in result.cases)
    assert not any(case.passed for case in result.cases)


def test_missing_judge_fails_before_any_model_call(example_suite_path):
    suite = load_suite(example_suite_path)
    with pytest.raises(ConfigError, match="judge"):
        run_suite(suite, MockClient("careful"), judge=None)


def test_progress_callback_is_called_once_per_case(example_suite_path):
    suite = load_suite(example_suite_path)
    seen = []
    run_suite(suite, MockClient("careful"), MockClient("judge"), on_case_done=lambda model, case: seen.append(case.case.id))
    assert seen == [case.id for case in suite.cases]
