"""Assert policy decisions, worker actions, documentation, and diagnostic checks."""

import re
from pathlib import Path

import pytest
import unrelated
from callers import next_action
from retry_policy import retry_ok


@pytest.mark.parametrize(
    ("retry_disabled", "transient_failure", "attempt_count", "attempt_limit", "decision", "action"),
    [
        (False, True, 1, 3, True, "retry"),
        (False, True, 3, 3, False, "stop"),
        (False, False, 1, 3, False, "stop"),
        (False, False, 3, 3, False, "stop"),
        (True, True, 1, 3, False, "stop"),
        (True, True, 3, 3, False, "stop"),
        (True, False, 1, 3, False, "stop"),
        (True, False, 3, 3, False, "stop"),
        (False, True, 0, 0, False, "stop"),
        (False, True, 4, 3, False, "stop"),
        (False, True, 2, 3, True, "retry"),
    ],
    ids=[
        "enabled-transient-budget",
        "enabled-transient-exhausted",
        "enabled-permanent-budget",
        "enabled-permanent-exhausted",
        "disabled-transient-budget",
        "disabled-transient-exhausted",
        "disabled-permanent-budget",
        "disabled-permanent-exhausted",
        "zero-attempt-limit",
        "above-attempt-limit",
        "one-attempt-remaining",
    ],
)
def test_policy_and_worker_contract(
    retry_disabled: bool,
    transient_failure: bool,
    attempt_count: int,
    attempt_limit: int,
    decision: bool,
    action: str,
) -> None:
    assert (
        retry_ok(
            disabled=retry_disabled,
            transient_failure=transient_failure,
            attempt_count=attempt_count,
            attempt_limit=attempt_limit,
        )
        is decision
    )
    assert (
        next_action(
            retry_disabled=retry_disabled,
            transient_failure=transient_failure,
            attempt_count=attempt_count,
            attempt_limit=attempt_limit,
        )
        == action
    )


def test_usage_example() -> None:
    usage = Path(__file__).with_name("usage.md").read_text(encoding="utf-8")
    examples = re.findall(r"^```python\n(.*?)^```", usage, flags=re.MULTILINE | re.DOTALL)
    assert len(examples) == 1
    exec(compile(examples[0], "usage.md", "exec"), {})


@pytest.mark.parametrize(
    ("check_results", "expected"),
    [((), False), ((True, True), True), ((True, False), False)],
    ids=["no-checks", "all-checks-passed", "failed-check"],
)
def test_independent_diagnostic_operation(check_results: tuple[bool, ...], expected: bool) -> None:
    assert unrelated.retry_ok(check_results) is expected
