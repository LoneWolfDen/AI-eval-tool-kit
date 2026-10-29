import pytest

from evaltoolkit.clients.mock import MockClient
from evaltoolkit.errors import ConfigError
from evaltoolkit.scorers import build_scorer
from evaltoolkit.scorers.pii import find_card_numbers, find_emails, find_phone_numbers, find_uk_national_insurance
from evaltoolkit.scorers.rubric import parse_judge_reply
from evaltoolkit.types import CheckSpec


def check(case, spec_type, output, judge=None, **params):
    """Build a scorer from a spec and run it. Keeps the tests short."""
    scorer = build_scorer(CheckSpec(spec_type, params), judge)
    return scorer.score(case, output)


# ---- contains / not_contains ------------------------------------------------


def test_contains_ignores_case_by_default(make_case):
    assert check(make_case(), "contains", "The PMP exam", value="pmp").passed


def test_contains_all_vs_any(make_case):
    case = make_case()
    assert not check(case, "contains", "risk only", value=["risk", "issue"]).passed
    assert check(case, "contains", "risk only", value=["risk", "issue"], match="any").passed


def test_contains_rejects_bad_match_option(make_case):
    with pytest.raises(ConfigError):
        build_scorer(CheckSpec("contains", {"value": "x", "match": "most"}))


def test_not_contains_reports_what_was_found(make_case):
    result = check(make_case(), "not_contains", "the code is 1234", value="1234")
    assert not result.passed
    assert "1234" in result.detail


# ---- exact / regex ------------------------------------------------------------


def test_exact_strips_whitespace_but_is_case_sensitive(make_case):
    case = make_case()
    assert check(case, "exact", "  READY\n", value="READY").passed
    assert not check(case, "exact", "ready", value="READY").passed


def test_regex_must_match_and_must_not_match(make_case):
    case = make_case()
    assert check(case, "regex", "36", pattern=r"^\d+$").passed
    assert not check(case, "regex", "It is 36", pattern=r"^\d+$").passed
    assert check(case, "regex", "all good", pattern="password", must_match=False).passed


def test_regex_invalid_pattern_is_a_config_error():
    with pytest.raises(ConfigError):
        build_scorer(CheckSpec("regex", {"pattern": "("}))


# ---- length -----------------------------------------------------------------------


def test_word_limits(make_case):
    case = make_case()
    assert check(case, "max_words", "one two three", limit=3).passed
    assert not check(case, "max_words", "one two three four", limit=3).passed
    assert check(case, "min_words", "one two", minimum=2).passed
    assert not check(case, "min_words", "one", minimum=2).passed


# ---- privacy ------------------------------------------------------------------------


def test_email_and_phone_detection():
    assert find_emails("write to jo.smith@example.com today") == ["jo.smith@example.com"]
    assert find_phone_numbers("call +44 7700 900123 now")


def test_dates_and_short_numbers_are_not_phone_numbers():
    assert find_phone_numbers("Meeting on 2026-10-29 at 10:30, budget 250000") == []


def test_card_detection_uses_the_luhn_checksum():
    assert find_card_numbers("card 4111 1111 1111 1111")  # valid test number
    assert find_card_numbers("card 4111 1111 1111 1112") == []  # fails checksum


def test_uk_national_insurance_detection():
    assert find_uk_national_insurance("NI number AB 12 34 56 C")
    assert find_uk_national_insurance("QQ 12 34 56 C") == []  # QQ is not a valid NI prefix
    assert find_uk_national_insurance("nothing here") == []


def test_no_pii_scorer(make_case):
    case = make_case()
    assert check(case, "no_pii", "Please contact the PMO mailbox.").passed
    leaked = check(case, "no_pii", "Email jo@example.com", kinds=["email"])
    assert not leaked.passed
    assert "email" in leaked.detail


def test_no_pii_rejects_unknown_kind():
    with pytest.raises(ConfigError):
        build_scorer(CheckSpec("no_pii", {"kinds": ["blood_type"]}))


# ---- rubric (LLM judge) -------------------------------------------------------------------


def test_parse_judge_reply_handles_json_inside_prose():
    score, reason = parse_judge_reply('Here you go: {"score": 5, "reason": "great"} thanks')
    assert (score, reason) == (5, "great")


@pytest.mark.parametrize("reply", ["no json", '{"score": 9}', '{"reason": "x"}'])
def test_parse_judge_reply_rejects_bad_replies(reply):
    with pytest.raises((ValueError, KeyError)):
        parse_judge_reply(reply)


def test_rubric_scores_and_rescales(make_case):
    judge = MockClient("judge")  # always answers 4/5
    result = check(make_case(), "rubric", "some answer", judge=judge, criteria="be good", min_score=4)
    assert result.passed
    assert result.score == pytest.approx(0.75)

    strict = check(make_case(), "rubric", "some answer", judge=judge, criteria="be good", min_score=5)
    assert not strict.passed


def test_rubric_without_a_judge_is_a_config_error():
    with pytest.raises(ConfigError, match="judge"):
        build_scorer(CheckSpec("rubric", {"criteria": "x"}), judge=None)


def test_unknown_check_type_lists_alternatives():
    with pytest.raises(ConfigError, match="Available"):
        build_scorer(CheckSpec("telepathy", {}))
