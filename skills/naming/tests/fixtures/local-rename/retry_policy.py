"""Decide whether a failed attempt qualifies for another attempt."""


def retry_ok(
    *,
    disabled: bool,
    transient_failure: bool,
    attempt_count: int,
    attempt_limit: int,
) -> bool:
    """Return true when policy, failure classification, and budget allow retry.

    disabled is true when the retry policy is switched off. attempt_count counts
    completed attempts; attempt_limit is the maximum total number of attempts.
    Precondition: counts are nonnegative integers.
    """
    return not disabled and transient_failure and attempt_count < attempt_limit
