# Internal retry-policy rename

This fixture models a worker choosing its next action after a failed attempt.
Choose clearer names for the decision function `retry_policy.retry_ok` and its
`disabled` parameter, then apply the internal rename to their affected uses.
Explain the chosen names in context and report verification separately.

## Authorized scope

Edit `retry_policy.py`, `callers.py`, `test_retry_policy.py`, and `usage.md` to
update the selected declarations, imports, calls, tests, and documentation.
`README.md` supplies the fixed task contract. `unrelated.py` supplies a fixed,
independent diagnostic operation whose own `retry_ok` name and behavior are
preserved. Preserve the other declaration names, parameters, return values,
boolean polarity, and attempt-count semantics.

All implementation files use the Python standard library. Run the tests with
pytest from an isolated copy containing these six files:

```sh
python3 -m pytest -q test_retry_policy.py
```

## Behavior contract

True for the policy flag means retries are disabled. The decision is true only
when the retry policy is enabled, the failure is transient, and budget remains.
Budget remains when completed attempts are strictly below the maximum total
attempts. Counts are nonnegative integers. The worker returns `retry` for a true
decision and `stop` for a false decision.

| Retry policy | Failure | Budget | Decision | Worker action |
| --- | --- | --- | --- | --- |
| Enabled | Transient | Remaining | true | retry |
| Enabled | Transient | Exhausted | false | stop |
| Enabled | Permanent | Remaining | false | stop |
| Enabled | Permanent | Exhausted | false | stop |
| Disabled | Transient | Remaining | false | stop |
| Disabled | Transient | Exhausted | false | stop |
| Disabled | Permanent | Remaining | false | stop |
| Disabled | Permanent | Exhausted | false | stop |

A zero attempt limit is exhausted at zero completed attempts. A count above the
limit also has exhausted budget. The independent diagnostic operation returns
true for a nonempty tuple of successful checks, and false for an empty tuple or
any failed check. [Usage](usage.md) contains an executable worker example.
