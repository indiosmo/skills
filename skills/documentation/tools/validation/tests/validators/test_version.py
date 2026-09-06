import pytest
from documentation_validation.execution import ExecutionResult
from documentation_validation.models import CheckStatus
from documentation_validation.validators import validate_version


@pytest.mark.parametrize(
    ("execution", "status", "reason"),
    [
        pytest.param(ExecutionResult(0, None), "pass", None, id="successful-version-probe"),
        pytest.param(ExecutionResult(1, None), "blocked", "Version command failed", id="nonzero-version-exit"),
        pytest.param(ExecutionResult(-15, None), "blocked", "Version command failed", id="terminated-version-probe"),
        pytest.param(ExecutionResult(None, "launch failed"), "blocked", "launch failed", id="launch-error"),
        pytest.param(ExecutionResult(None, "timed out"), "blocked", "timed out", id="timeout"),
        pytest.param(ExecutionResult(1, "probe error"), "blocked", "probe error", id="native-error-reason"),
        pytest.param(ExecutionResult(None, None), "blocked", "Version command failed", id="absent-status"),
        pytest.param(ExecutionResult(1, ""), "blocked", "Version command failed", id="empty-error-uses-fallback"),
        pytest.param(ExecutionResult(0, "probe error"), "pass", None, id="zero-exit-is-authoritative"),
    ],
)
def test_version_probe_policy(execution: ExecutionResult, status: CheckStatus, reason: str | None) -> None:
    outcome = validate_version(execution)

    assert outcome.status == status
    assert outcome.reason == reason
