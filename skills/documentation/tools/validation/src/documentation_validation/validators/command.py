"""Classify a native validation command's execution result."""

from collections.abc import Collection

from ..execution import ExecutionResult
from ..models import ValidationOutcome


def validate_command(execution: ExecutionResult, blocked_exit_codes: Collection[int]) -> ValidationOutcome:
    """Apply execution failures and configured blocked codes before success."""
    if execution.error or execution.exit_status in blocked_exit_codes:
        return ValidationOutcome(status="blocked", reason=execution.error)
    if execution.exit_status == 0:
        return ValidationOutcome(status="pass", reason=execution.error)
    return ValidationOutcome(status="fail", reason=execution.error)
