# Worker retry policy

`retry_policy.retry_ok` decides whether to schedule another attempt after a
failure. Its `disabled` parameter is true when the configured retry policy is
switched off. A transient failure and remaining attempt budget are also required.
`attempt_count` counts completed attempts, and `attempt_limit` sets the maximum
total attempts. Both counts are nonnegative integers.

Run this Python example from the fixture directory. The fixture test executes
the same example and checks its assertions.

```python
from retry_policy import retry_ok
from callers import next_action

assert retry_ok(
    disabled=False,
    transient_failure=True,
    attempt_count=1,
    attempt_limit=3,
) is True
assert retry_ok(
    disabled=True,
    transient_failure=True,
    attempt_count=1,
    attempt_limit=3,
) is False
assert next_action(
    retry_disabled=False,
    transient_failure=True,
    attempt_count=3,
    attempt_limit=3,
) == "stop"
```
