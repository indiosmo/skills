"""Translate the retry policy decision into a worker action."""

from retry_policy import retry_ok


def next_action(
    *,
    retry_disabled: bool,
    transient_failure: bool,
    attempt_count: int,
    attempt_limit: int,
) -> str:
    """Return the action following a classified failed attempt."""
    if retry_ok(
        disabled=retry_disabled,
        transient_failure=transient_failure,
        attempt_count=attempt_count,
        attempt_limit=attempt_limit,
    ):
        return "retry"
    return "stop"
