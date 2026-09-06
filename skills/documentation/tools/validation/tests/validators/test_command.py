from collections.abc import Collection

import pytest
from documentation_validation.execution import ExecutionResult
from documentation_validation.models import CheckStatus
from documentation_validation.validators import validate_command


@pytest.mark.parametrize(
    ("execution", "blocked_exit_codes", "status", "reason"),
    [
        pytest.param(ExecutionResult(0, None), [], "pass", None, id="successful-command"),
        pytest.param(ExecutionResult(1, None), [], "fail", None, id="validation-failure"),
        pytest.param(ExecutionResult(-15, None), [], "fail", None, id="terminated-command"),
        pytest.param(ExecutionResult(2, None), [2], "blocked", None, id="declared-blocked-exit"),
        pytest.param(ExecutionResult(0, None), [0], "blocked", None, id="blocked-exit-precedes-success"),
        pytest.param(ExecutionResult(2, None), {2}, "blocked", None, id="blocked-code-collection"),
        pytest.param(ExecutionResult(None, "launch failed"), [], "blocked", "launch failed", id="launch-error"),
        pytest.param(ExecutionResult(None, "timed out"), [], "blocked", "timed out", id="timeout"),
        pytest.param(
            ExecutionResult(0, "execution error"), [], "blocked", "execution error", id="error-precedes-success"
        ),
        pytest.param(
            ExecutionResult(1, "execution error"), [], "blocked", "execution error", id="error-precedes-failure"
        ),
        pytest.param(ExecutionResult(None, None), [], "fail", None, id="absent-status-without-error"),
        pytest.param(ExecutionResult(0, ""), [], "pass", "", id="empty-error-is-preserved"),
    ],
)
def test_native_command_policy(
    execution: ExecutionResult,
    blocked_exit_codes: Collection[int],
    status: CheckStatus,
    reason: str | None,
) -> None:
    outcome = validate_command(execution, blocked_exit_codes)

    assert outcome.status == status
    assert outcome.reason == reason
