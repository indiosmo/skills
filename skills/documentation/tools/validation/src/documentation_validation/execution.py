"""Execute one native command and retain its combined diagnostic output."""

import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple


class ExecutionResult(NamedTuple):
    """Native exit status, or an execution error recorded in the command log."""

    exit_status: int | None
    error: str | None


Executor = Callable[[list[str], Path, int, str | None, Path], ExecutionResult]


def execute(command: list[str], directory: Path, timeout: int, stdin: str | None, log: Path) -> ExecutionResult:
    """Run an argv with its own timeout; log-write failures propagate as OSError."""
    try:
        with log.open("w", encoding="utf-8") as output:
            completed = subprocess.run(
                command,
                cwd=directory,
                input=stdin,
                text=True,
                stdout=output,
                stderr=subprocess.STDOUT,
                timeout=timeout,
                check=False,
            )
        return ExecutionResult(completed.returncode, None)
    except (OSError, subprocess.TimeoutExpired) as error:
        with log.open("a", encoding="utf-8") as output:
            output.write(f"\n{type(error).__name__}: {error}\n")
        return ExecutionResult(None, str(error))
