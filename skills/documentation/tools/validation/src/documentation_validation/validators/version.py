"""Classify a tool version probe's execution result."""

from ..execution import ExecutionResult
from ..models import ValidationOutcome


def validate_version(execution: ExecutionResult) -> ValidationOutcome:
    """Require a successful version probe before running the native check."""
    if execution.exit_status != 0:
        return ValidationOutcome(status="blocked", reason=execution.error or "Version command failed")
    return ValidationOutcome(status="pass")
