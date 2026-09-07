# Preserving boolean polarity during a local rename

The [local-rename fixture](../tests/fixtures/local-rename/README.md) models a
worker selecting `retry` or `stop` after a failed attempt. Its function
`retry_policy.retry_ok` receives a `disabled` flag, failure classification,
completed-attempt count, and total-attempt limit. True for `disabled` means the
configured retry policy is switched off. The authorized task improves the
function and parameter names while preserving those meanings.

Reading the declaration alone leaves "ok" ambiguous between a decision and an
observed successful retry. The [caller](../tests/fixtures/local-rename/callers.py)
uses the result to choose its next action. The
[usage](../tests/fixtures/local-rename/usage.md) confirms the scheduling decision.
The independent `unrelated.retry_ok` instead summarizes checks after a diagnostic
retry. These bindings give the same spelling two different referents.

Candidates for the decision are `should_retry`, `can_retry`, and
`retry_succeeded`. The action branch supports `should_retry`; `can_retry` would
suggest operational capability beyond the supplied inputs, and
`retry_succeeded` fits an observation after execution. For the parameter,
`retry_disabled` supplies the missing policy context while preserving its true
proposition. `retry_enabled` would require inverted values and a representation
change. These constraints make `should_retry` and `retry_disabled` clear winners.

| Declaration identity | Original spelling | Selected spelling | Preserved meaning |
| --- | --- | --- | --- |
| Function in `retry_policy.py` | `retry_ok` | `should_retry` | Decision to schedule another attempt |
| Keyword-only parameter of that function | `disabled` | `retry_disabled` | True means retry policy switched off |

The resulting body and representative keyword call are excerpts from the
executed edited copy:

```python
return not retry_disabled and transient_failure and attempt_count < attempt_limit
```

```python
should_retry(
    retry_disabled=False,
    transient_failure=True,
    attempt_count=1,
    attempt_limit=3,
)
```

The body is a function excerpt; the call requires its import from the renamed
module. The complete runnable example is the edited `usage.md` in the copy.

The distinct name review traces the chosen names through the decision and the
worker branch, then checks the true proposition against the fixture contract:

| retry_disabled | transient_failure | Budget remaining | should_retry |
| --- | --- | --- | --- |
| false | true | true | true |
| false | true | false | false |
| false | false | true | false |
| false | false | false | false |
| true | true | true | false |
| true | true | false | false |
| true | false | true | false |
| true | false | false | false |

**Name assessment: supported.** The negation reads correctly with `retry_disabled`,
and `should_retry` describes the policy decision consumed by `next_action`.
Budget means `attempt_count < attempt_limit`; a limit counts total attempts.

The authorized demonstration changed only `retry_policy.py`, `callers.py`,
`test_retry_policy.py`, and `usage.md` in an isolated six-file copy. Imports and
calls bound to the decision became `should_retry`; bound `disabled=` keywords,
the declaration, expression, and descriptive prose became `retry_disabled`.
The caller's existing `retry_disabled` parameter and every other parameter name
remain established bindings. `unrelated.retry_ok` retains its independent
diagnostic meaning and its qualified test calls.

To repeat the demonstration, copy the packet into `{local_copy}`, apply the
mapping above to its bound uses, and run this command from that directory before
and after editing:

```sh
python3 -m pytest -q test_retry_policy.py
```

**Applied-change checks, 2026-09-06:** baseline **15 passed**; renamed copy
**15 passed**. The suite exercises all eight rows through both function and
worker, zero limit, above-limit and one-attempt-remaining boundaries, the
executable usage example, and three diagnostic cases. Diff inspection verified
the changed bindings and preserved test expectations. Byte comparisons verified
unchanged `README.md`, `unrelated.py`, and all packaged fixture source files.

The final review reread the renamed import, keyword calls, body, and usage; they
agree on a disabled policy input and a scheduling decision. Recovery for this
local demonstration is discarding the isolated copy. These checks cover the
supplied packet; dynamic consumers outside it remain unexamined, and human review
is pending. Native tests plus inspected diffs support this record; independent
evaluation-checker execution is outside this demonstration. See
[boolean guidance](../references/variables-and-state.md#boolean-meaning-and-polarity)
and the [rename plan](../templates/rename-plan.md).
