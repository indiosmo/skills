"""Exercise trusted rename outcomes using independent successful edits and mutants."""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

CHECKER_PATH = Path(__file__).resolve().parents[1] / "evals" / "check_rename_outcomes.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
SPECIFICATION = importlib.util.spec_from_file_location("naming_outcome_checker", CHECKER_PATH)
assert SPECIFICATION is not None and SPECIFICATION.loader is not None
checker = importlib.util.module_from_spec(SPECIFICATION)
sys.modules[SPECIFICATION.name] = checker
SPECIFICATION.loader.exec_module(checker)


def copy_fixture(tmp_path: Path, scenario: str) -> Path:
    checkout = tmp_path / scenario
    shutil.copytree(FIXTURES / scenario, checkout, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    return checkout


def replace_text(checkout: Path, filename: str, old: str, new: str) -> None:
    path = checkout / filename
    content = path.read_text()
    assert old in content, (filename, old)
    path.write_text(content.replace(old, new))


def rename_local(checkout: Path, function_name: str = "should_retry", parameter_name: str = "retry_disabled") -> None:
    for filename in ("retry_policy.py", "callers.py", "test_retry_policy.py", "usage.md"):
        path = checkout / filename
        content = path.read_text()
        content = re.sub(r"(?<!unrelated\.)\bretry_ok\b", function_name, content)
        content = re.sub(r"\bdisabled\b", parameter_name, content)
        path.write_text(content)


def rename_public(checkout: Path, field_name: str = "retry_enabled") -> None:
    for filename in ("api.py", "test_compatibility.py"):
        path = checkout / filename
        content = path.read_text().replace(".retry", f".{field_name}")
        content = content.replace("retry=", f"{field_name}=").replace("retry: bool", f"{field_name}: bool")
        path.write_text(content)
    replace_text(checkout, "README.md", "`RetryPolicy.retry`", f"`RetryPolicy.{field_name}`")


def assert_failed(report: object, status: int, check_name: str) -> None:
    assert status == 1
    assert report.status == "fail"  # pyright: ignore[reportAttributeAccessIssue]
    assert any(check.name == check_name and check.status == "fail" for check in report.checks), report  # pyright: ignore[reportAttributeAccessIssue]


@pytest.mark.parametrize(
    "function_name,parameter_name", [("should_retry", "retry_disabled"), ("retry_is_allowed", "retries_disabled")]
)
def test_accepts_distinct_local_names(tmp_path: Path, function_name: str, parameter_name: str) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout, function_name, parameter_name)
    report, status = checker.check_output("local-rename", checkout)
    assert status == 0, report
    assert report.execution["status"] == "pass"
    assert report.symbol_mapping["retry_policy.retry_ok"] == f"retry_policy.{function_name}"


@pytest.mark.parametrize("field_name", ["retry_enabled", "automatic_retries_enabled"])
def test_accepts_distinct_public_names(tmp_path: Path, field_name: str) -> None:
    checkout = copy_fixture(tmp_path, "public-contract")
    rename_public(checkout, field_name)
    report, status = checker.check_output("public-contract", checkout)
    assert status == 0, report
    assert report.symbol_mapping == {"RetryPolicy.retry": f"RetryPolicy.{field_name}"}


def test_accepts_bound_import_aliases(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    for filename in ("callers.py", "test_retry_policy.py", "usage.md"):
        replace_text(
            checkout,
            filename,
            "from retry_policy import should_retry",
            "from retry_policy import should_retry as retry_ok",
        )
        replace_text(checkout, filename, "should_retry(", "retry_ok(")
    report, status = checker.check_output("local-rename", checkout)
    assert status == 0, report


@pytest.mark.parametrize("scenario", ["local-rename", "public-contract"])
def test_unchanged_baseline_is_not_a_completed_rename(tmp_path: Path, scenario: str) -> None:
    checkout = copy_fixture(tmp_path, scenario)
    report, status = checker.check_output(scenario, checkout)
    assert_failed(report, status, "rename_applied")


@pytest.mark.parametrize(
    "filename,old,new,check_name",
    [
        ("callers.py", "import should_retry", "import retry_ok", "import_binding"),
        ("callers.py", "retry_disabled=retry_disabled", "disabled=retry_disabled", "keyword_binding"),
        ("test_retry_policy.py", "retry_disabled=retry_disabled", "disabled=retry_disabled", "keyword_binding"),
        ("usage.md", "`retry_policy.should_retry`", "`retry_policy.retry_ok`", "documentation_binding"),
        ("usage.md", "`retry_disabled`", "`disabled`", "documentation_binding"),
        ("usage.md", "retry_disabled=False", "disabled=False", "keyword_binding"),
        ("retry_policy.py", "retry_disabled is true", "disabled is true", "parameter_documentation"),
        ("retry_policy.py", "return not retry_disabled", "return retry_disabled", "trusted_behavior"),
        ("retry_policy.py", "attempt_count < attempt_limit", "attempt_count <= attempt_limit", "trusted_behavior"),
        ("unrelated.py", "def retry_ok(", "def diagnostic_retry_passed(", "immutable_file"),
        ("callers.py", 'return "retry"', 'return "again"', "trusted_behavior"),
    ],
)
def test_local_mutations_are_observed(tmp_path: Path, filename: str, old: str, new: str, check_name: str) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    replace_text(checkout, filename, old, new)
    report, status = checker.check_output("local-rename", checkout)
    assert_failed(report, status, check_name)


@pytest.mark.parametrize(
    "filename,old,new,check_name",
    [
        ("api.py", '{"retry": policy.retry_enabled}', '{"retry_enabled": policy.retry_enabled}', "trusted_behavior"),
        ("api.py", "retry_enabled: bool = False", "retry_enabled: bool = True", "trusted_behavior"),
        ("api.py", 'configuration.get("retry", False)', 'configuration.get("retry", True)', "trusted_behavior"),
        (
            "api.py",
            "type(self.retry_enabled) is not bool",
            "not isinstance(self.retry_enabled, (bool, int))",
            "trusted_behavior",
        ),
        ("api.py", 'raise ValueError("unknown retry configuration field")', "pass", "trusted_behavior"),
        ("README.md", "`RetryPolicy.retry_enabled`", "`RetryPolicy.retry`", "documentation_binding"),
        ("test_compatibility.py", "RetryPolicy().retry_enabled", "RetryPolicy().retry", "test_bindings"),
        ("schema.json", '"default": false', '"default": true', "immutable_file"),
        (
            "client.py",
            'configuration.get("retry", False)',
            'configuration.get("retry_enabled", False)',
            "immutable_file",
        ),
    ],
)
def test_public_mutations_are_observed(tmp_path: Path, filename: str, old: str, new: str, check_name: str) -> None:
    checkout = copy_fixture(tmp_path, "public-contract")
    rename_public(checkout)
    replace_text(checkout, filename, old, new)
    report, status = checker.check_output("public-contract", checkout)
    assert_failed(report, status, check_name)


def test_changed_output_tests_cannot_establish_wire_compatibility(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "public-contract")
    rename_public(checkout)
    replace_text(checkout, "api.py", '{"retry": policy.retry_enabled}', '{"retry_enabled": policy.retry_enabled}')
    (checkout / "test_compatibility.py").write_text("assert True\n")
    report, status = checker.check_output("public-contract", checkout)
    assert_failed(report, status, "trusted_behavior")
    assert "wire field/value" in report.execution["stderr"]


@pytest.mark.parametrize("scenario", ["local-rename", "public-contract"])
def test_rejects_added_source(tmp_path: Path, scenario: str) -> None:
    checkout = copy_fixture(tmp_path, scenario)
    (rename_local if scenario == "local-rename" else rename_public)(checkout)
    (checkout / "additional.py").write_text("value = 1\n")
    report, status = checker.check_output(scenario, checkout)
    assert_failed(report, status, "scope")


@pytest.mark.parametrize("scenario", ["local-rename", "public-contract"])
def test_missing_outputs_are_incomplete(tmp_path: Path, scenario: str) -> None:
    checkout = copy_fixture(tmp_path, scenario)
    (checkout / "README.md").unlink()
    report, status = checker.check_output(scenario, checkout)
    assert status == 2 and report.status == "incomplete"
    assert "README.md" in report.checks[-1].detail


def test_missing_checkout_is_incomplete(tmp_path: Path) -> None:
    report, status = checker.check_output("local-rename", tmp_path / "missing")
    assert status == 2 and report.status == "incomplete"


def test_ambiguous_declarations_are_incomplete(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    with (checkout / "retry_policy.py").open("a") as stream:
        stream.write("\ndef other_policy():\n    return False\n")
    report, status = checker.check_output("local-rename", checkout)
    assert status == 2 and "one top-level" in report.checks[-1].detail


@pytest.mark.parametrize(
    "addition,check_name",
    [
        ("\ninvalid syntax !\n", "source_parse"),
        ("\nraise RuntimeError('worker failed')\n", "trusted_behavior"),
        ("\nimport unavailable_fixture_module\n", "trusted_behavior"),
    ],
)
def test_parse_and_execution_failures_retain_diagnostics(tmp_path: Path, addition: str, check_name: str) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    with (checkout / "retry_policy.py").open("a") as stream:
        stream.write(addition)
    report, status = checker.check_output("local-rename", checkout)
    assert_failed(report, status, check_name)
    assert report.checks[-1].detail if check_name == "source_parse" else report.execution["stderr"]


def test_worker_timeout_is_blocked(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    with (checkout / "retry_policy.py").open("a") as stream:
        stream.write("\nwhile True:\n    pass\n")
    report, status = checker.check_output("local-rename", checkout, timeout=0.2)
    assert status == 3 and report.status == "blocked"
    assert report.execution["status"] == "blocked"


def test_unavailable_trusted_resource_is_blocked(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    report, status = checker.check_output("local-rename", checkout, fixture_directory=tmp_path / "missing")
    assert status == 3 and report.status == "blocked"
    assert "Trusted baseline" in report.checks[-1].detail


@pytest.mark.parametrize("entry", ["checkout", "retry_policy.py"])
def test_symlink_output_is_incomplete(tmp_path: Path, entry: str) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    if entry == "checkout":
        alias = tmp_path / "linked-checkout"
        alias.symlink_to(checkout, target_is_directory=True)
        checkout = alias
    else:
        (checkout / entry).unlink()
        (checkout / entry).symlink_to(FIXTURES / "local-rename" / entry)
    report, status = checker.check_output("local-rename", checkout)
    assert status == 2 and report.status == "incomplete"


def test_cli_emits_machine_readable_evidence(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    process = subprocess.run(
        [sys.executable, str(CHECKER_PATH), "--scenario", "local-rename", "--output-checkout", str(checkout)],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    report = json.loads(process.stdout)
    assert process.returncode == 0, report
    assert report["status"] == "pass" and report["checks"] and report["changed_files"]
    assert report["execution"]["returncode"] == 0


def test_invalid_cli_invocation_is_json() -> None:
    process = subprocess.run(
        [sys.executable, str(CHECKER_PATH), "--scenario", "unknown"],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert process.returncode == 2
    assert json.loads(process.stdout)["checks"][0]["name"] == "invocation"


def test_preserves_independent_diagnostic_binding_in_tests(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    replace_text(checkout, "test_retry_policy.py", "unrelated.retry_ok", "unrelated.should_retry")
    report, status = checker.check_output("local-rename", checkout)
    assert_failed(report, status, "implementation_scope")


def test_accepts_native_verification_caches_and_preserves_inputs(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    for directory in ("__pycache__", ".pytest_cache"):
        (checkout / directory).mkdir()
        (checkout / directory / "cached").write_text("cache")
    before = {path.name: path.read_bytes() for path in checkout.iterdir() if path.is_file()}
    report, status = checker.check_output("local-rename", checkout)
    assert status == 0, report
    assert before == {path.name: path.read_bytes() for path in checkout.iterdir() if path.is_file()}


def test_refuses_to_evaluate_packaged_baseline_as_output() -> None:
    report, status = checker.check_output("local-rename", FIXTURES / "local-rename")
    assert status == 2 and "separate" in report.checks[-1].detail


def test_module_qualified_aliases_require_manual_binding_review(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    replace_text(checkout, "callers.py", "from retry_policy import should_retry", "import retry_policy as policy")
    replace_text(checkout, "callers.py", "if should_retry(", "if policy.should_retry(")
    report, status = checker.check_output("local-rename", checkout)
    assert status == 2 and report.status == "incomplete"
    assert "manual binding review" in report.checks[-1].detail


@pytest.mark.parametrize("timeout", [0, -1, float("inf"), float("nan")])
def test_invalid_timeout_is_incomplete(tmp_path: Path, timeout: float) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    report, status = checker.check_output("local-rename", checkout, timeout=timeout)
    assert status == 2 and report.status == "incomplete"


@pytest.mark.parametrize(
    "scenario,filename", [("local-rename", "test_retry_policy.py"), ("public-contract", "test_compatibility.py")]
)
def test_deleted_output_assertions_fail_scope(tmp_path: Path, scenario: str, filename: str) -> None:
    checkout = copy_fixture(tmp_path, scenario)
    (rename_local if scenario == "local-rename" else rename_public)(checkout)
    (checkout / filename).write_text("")
    report, status = checker.check_output(scenario, checkout)
    assert_failed(report, status, "implementation_scope")


def test_widened_output_assertion_fails_scope(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    replace_text(checkout, "test_retry_policy.py", "is decision", "in (True, False)")
    report, status = checker.check_output("local-rename", checkout)
    assert_failed(report, status, "implementation_scope")


def test_usage_keeps_meaningful_assertions(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    replace_text(checkout, "usage.md", ") is True", ") in (True, False)")
    report, status = checker.check_output("local-rename", checkout)
    assert_failed(report, status, "usage_scope")
    assert report.execution["status"] == "pass"


def test_executable_case_identifiers_fail_scope(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    path = checkout / "test_retry_policy.py"
    source, replacements = re.subn(
        r"    ids=\[.*?    \],", "    ids=make_ids(),", path.read_text(), count=1, flags=re.DOTALL
    )
    assert replacements == 1
    path.write_text(source)
    report, status = checker.check_output("local-rename", checkout)
    assert_failed(report, status, "implementation_scope")


def test_empty_case_table_fails_scope(tmp_path: Path) -> None:
    checkout = copy_fixture(tmp_path, "local-rename")
    rename_local(checkout)
    path = checkout / "test_retry_policy.py"
    source, replacements = re.subn(
        r"    \[\n.*?    \],\n    ids=", "    [],\n    ids=", path.read_text(), count=1, flags=re.DOTALL
    )
    assert replacements == 1
    path.write_text(source)
    report, status = checker.check_output("local-rename", checkout)
    assert_failed(report, status, "implementation_scope")
