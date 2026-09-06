"""Exercise process execution and diagnostic retention at the native boundary."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from documentation_validation.execution import ExecutionResult, execute


def test_combines_native_output_and_preserves_failure_exit(tmp_path: Path) -> None:
    log = tmp_path / "check.log"
    log.write_text("stale evidence", encoding="utf-8")
    result = execute(
        [
            sys.executable,
            "-c",
            "import sys; print('stdout', flush=True); print('stderr', file=sys.stderr, flush=True); sys.exit(7)",
        ],
        tmp_path,
        10,
        None,
        log,
    )
    assert result == ExecutionResult(exit_status=7, error=None)
    assert log.read_text(encoding="utf-8") == "stdout\nstderr\n"


def test_passes_literal_arguments_stdin_and_working_directory(tmp_path: Path) -> None:
    directory = tmp_path / "project with spaces"
    directory.mkdir()
    log = tmp_path / "check.log"
    arguments = ["two words", "$HOME", "$(touch injected)", "*.md", "; exit 4"]
    program = (
        "import json, os, sys; "
        "print(json.dumps({'arguments': sys.argv[1:], 'stdin': sys.stdin.read(), 'directory': os.getcwd()}))"
    )
    result = execute([sys.executable, "-c", program, *arguments], directory, 10, "input\nsecond line", log)
    assert result == ExecutionResult(0, None)
    assert json.loads(log.read_text(encoding="utf-8")) == {
        "arguments": arguments,
        "stdin": "input\nsecond line",
        "directory": str(directory),
    }
    assert not (directory / "injected").exists()


@pytest.mark.parametrize("missing", ["executable", "directory"])
def test_missing_execution_resource_is_recorded(tmp_path: Path, missing: str) -> None:
    command = [str(tmp_path / "missing-tool")] if missing == "executable" else [sys.executable, "--version"]
    directory = tmp_path / "missing-project" if missing == "directory" else tmp_path
    log = tmp_path / "check.log"
    result = execute(command, directory, 10, None, log)
    assert result.exit_status is None
    assert result.error is not None
    assert "No such file or directory" in result.error
    assert log.read_text(encoding="utf-8") == f"\nFileNotFoundError: {result.error}\n"


def test_execution_permission_error_is_recorded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def deny_execution(*arguments: object, **options: object) -> subprocess.CompletedProcess[str]:
        raise PermissionError("execution denied")

    monkeypatch.setattr(subprocess, "run", deny_execution)
    log = tmp_path / "check.log"
    result = execute(["restricted-tool"], tmp_path, 10, None, log)
    assert result == ExecutionResult(None, "execution denied")
    assert log.read_text(encoding="utf-8") == "\nPermissionError: execution denied\n"


def test_timeout_retains_partial_output(tmp_path: Path) -> None:
    log = tmp_path / "check.log"
    command = [sys.executable, "-c", "import time; print('partial evidence', flush=True); time.sleep(30)"]
    result = execute(command, tmp_path, 1, None, log)
    assert result.exit_status is None
    assert result.error is not None
    assert "timed out after" in result.error
    assert log.read_text(encoding="utf-8") == f"partial evidence\n\nTimeoutExpired: {result.error}\n"


def test_unwritable_log_propagates_without_executing_command(tmp_path: Path) -> None:
    marker = tmp_path / "executed"
    command = [sys.executable, "-c", "from pathlib import Path; Path('executed').touch()"]
    with pytest.raises(IsADirectoryError):
        execute(command, tmp_path, 10, None, tmp_path)
    assert not marker.exists()
