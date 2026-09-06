"""Exercise check sequencing through the explicit execution dependency."""

from pathlib import Path

from documentation_validation import Check, Manifest, validate
from documentation_validation.execution import ExecutionResult


def make_check(name: str, **overrides: object) -> Check:
    return Check.model_validate(
        {
            "name": name,
            "scope": "selected files",
            "command": [name],
            "version_command": [name, "--version"],
            **overrides,
        }
    )


class RecordingExecutor:
    def __init__(self, results: dict[tuple[str, ...], ExecutionResult]) -> None:
        self.results = results
        self.calls: list[tuple[list[str], Path, int, str | None, Path]] = []

    def __call__(
        self, command: list[str], directory: Path, timeout: int, stdin: str | None, log: Path
    ) -> ExecutionResult:
        self.calls.append((command, directory, timeout, stdin, log))
        log.write_bytes(b"  native version\xff\n")
        return self.results.get(tuple(command), ExecutionResult(0, None))


def test_version_failure_prevents_command_and_skips_transitive_dependents(tmp_path: Path) -> None:
    executor = RecordingExecutor({("first", "--version"): ExecutionResult(7, None)})
    report = validate(
        Manifest(
            checks=[
                make_check("first"),
                make_check("second", depends_on=["first"]),
                make_check("third", depends_on=["second"]),
                make_check("independent"),
            ]
        ),
        tmp_path,
        tmp_path,
        tmp_path / "report",
        executor=executor,
    )
    assert [call[0] for call in executor.calls] == [
        ["first", "--version"],
        ["independent", "--version"],
        ["independent"],
    ]
    assert [result["status"] for result in report["checks"]] == ["blocked", "skipped", "skipped", "pass"]
    assert report["checks"][0]["version"] == "native version\ufffd"
    assert report["checks"][0]["reason"] == "Version command failed"
    assert report["checks"][0]["exit_status"] == 7
    assert report["checks"][0]["log"] == str(tmp_path / "report/first.version.log")
    assert report["checks"][2]["reason"] == "Prerequisite checks did not pass: second"


def test_explicit_skip_wins_and_failed_prerequisites_keep_declared_order(tmp_path: Path) -> None:
    executor = RecordingExecutor({("first",): ExecutionResult(1, None), ("second",): ExecutionResult(2, None)})
    report = validate(
        Manifest(
            checks=[
                make_check("first"),
                make_check("second", blocked_exit_codes=[2]),
                make_check("manual", depends_on=["first"], skip_reason="Review pending."),
                make_check("dependent", depends_on=["second", "first"]),
            ]
        ),
        tmp_path,
        tmp_path,
        tmp_path / "report",
        executor=executor,
    )
    assert len(executor.calls) == 4
    assert report["exit_status"] == 2
    assert not report["complete"]
    manual = report["checks"][2]
    assert manual["reason"] == "Review pending."
    assert manual["status"] == "skipped"
    assert manual["version"] is manual["exit_status"] is manual["log"] is None
    assert report["checks"][3]["reason"] == "Prerequisite checks did not pass: second, first"


def test_execution_receives_resolved_inputs_and_separate_timeout_budgets(tmp_path: Path) -> None:
    executor = RecordingExecutor({})
    output = tmp_path / "report"
    report = validate(
        Manifest(
            checks=[
                make_check(
                    "native",
                    command=["{skill}/tool", "{output}"],
                    version_command=["{skill}/tool", "--version"],
                    working_directory="docs",
                    stdin="{project}",
                    timeout_seconds=9,
                )
            ]
        ),
        tmp_path,
        tmp_path / "skill",
        output,
        executor=executor,
    )
    assert executor.calls == [
        ([str(tmp_path / "skill/tool"), "--version"], tmp_path / "docs", 9, None, output / "native.version.log"),
        ([str(tmp_path / "skill/tool"), str(output)], tmp_path / "docs", 9, str(tmp_path), output / "native.log"),
    ]
    assert report["complete"]
