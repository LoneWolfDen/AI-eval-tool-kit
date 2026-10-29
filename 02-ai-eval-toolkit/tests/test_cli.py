from evaltoolkit.cli import main


def run_cli(example_suite_path, tmp_path, *extra):
    return main(["run", str(example_suite_path), "--out", str(tmp_path), *extra])


def test_run_writes_reports(example_suite_path, tmp_path, capsys):
    code = run_cli(example_suite_path, tmp_path, "--model", "mock:careful", "--judge", "mock:judge")
    assert code == 0
    assert (tmp_path / "report.html").exists()
    assert "7/7 passed" in capsys.readouterr().out


def test_fail_under_sets_exit_code(example_suite_path, tmp_path):
    code = run_cli(example_suite_path, tmp_path, "--model", "mock:sloppy", "--judge", "mock:judge", "--fail-under", "90")
    assert code == 1


def test_config_problems_return_exit_code_2(example_suite_path, tmp_path, capsys):
    code = run_cli(example_suite_path, tmp_path, "--model", "mock:careful")  # rubric check but no judge
    assert code == 2
    assert "judge" in capsys.readouterr().err


def test_bad_model_spec_returns_exit_code_2(example_suite_path, tmp_path, capsys):
    code = run_cli(example_suite_path, tmp_path, "--model", "nonsense")
    assert code == 2
    assert "provider:model" in capsys.readouterr().err


def test_checks_command_lists_scorers(capsys):
    assert main(["checks"]) == 0
    assert "no_pii" in capsys.readouterr().out
