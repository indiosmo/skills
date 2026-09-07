"""Summarize checks observed after a diagnostic retry has completed."""


def retry_ok(check_results: tuple[bool, ...]) -> bool:
    """Return true when a diagnostic retry has checks and every check passed."""
    return bool(check_results) and all(check_results)
