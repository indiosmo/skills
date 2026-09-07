# Rename an internal field while preserving the JSON contract

The [public-contract fixture](../tests/fixtures/public-contract/README.md) stores
a retry configuration in `RetryPolicy.retry`. True means configuration enables
automatic retries after failures. The
[adapter](../tests/fixtures/public-contract/api.py) accepts and emits JSON key
`retry`; an [existing client](../tests/fixtures/public-contract/client.py) and
[schema](../tests/fixtures/public-contract/schema.json) use that spelling.
The authorized task improves the internal field and its bound uses.

The available evidence distinguishes a policy setting from the eventual retry
decision. `retry_enabled` describes the stored setting explicitly.
`should_retry` would imply a decision requiring failure classification and budget;
`can_retry` would imply capability requiring further evidence. The current
`retry` is serviceable in the published configuration context, but the internal
field benefits from making its boolean meaning explicit.

**Decision: rename `RetryPolicy.retry` to `RetryPolicy.retry_enabled`, keeping
JSON `retry`.** The fixture's stable-wire requirement and explicit adapter make
this a clear choice. The internal binding map is:

| Surface | Applied mapping |
| --- | --- |
| Dataclass field in `api.py` | `retry: bool = False` becomes `retry_enabled: bool = False` |
| Bound attribute reads | `self.retry` and `policy.retry` become `self.retry_enabled` and `policy.retry_enabled` |
| Constructor keyword | `RetryPolicy(retry=...)` becomes `RetryPolicy(retry_enabled=...)` |
| Internal assertions and README reference | Use `retry_enabled` for the internal field |
| JSON keys, schema, client, error behavior | Preserve the established `retry` contract |

These excerpts are from the executed renamed adapter; surrounding parsing and
validation appear in the complete fixture:

```python
return RetryPolicy(retry_enabled=configuration.get("retry", False))
```

```python
return json.dumps({"retry": policy.retry_enabled}, sort_keys=True)
```

The distinct contextual review checks the proposed name against each boundary:
the dataclass stores an enabled policy flag, the constructor requires a real
boolean, parsing supplies false on omission, and serialization writes the flag
under the established key. **Name assessment: internal `retry_enabled` is supported.**
The receiver `policy` gives the setting its context, and the adapter makes the
internal-to-public mapping visible. The
[retention example](retaining-an-existing-name.md) assesses the public spelling
separately.

The demonstration edited `api.py`, `test_compatibility.py`, and the internal-field
reference in `README.md` in an isolated five-file copy. To repeat it, copy the
packet into `{public_copy}`, apply the bound mappings above, and run this command
from that directory before and after editing:

```sh
python3 -m unittest -v test_compatibility
```

**Applied-change checks, 2026-09-06:** baseline **Ran 8 tests; OK**; renamed copy
**Ran 8 tests; OK**. The executed suite covers omitted/false/true settings,
internal construction, strict boolean rejection, non-object roots, malformed
JSON, unknown fields, round trips, exact emitted keys, schema properties, and
the existing client. Byte comparisons establish that `client.py` and
`schema.json` are unchanged and all packaged fixture sources are unchanged.
Diff inspection confirms that edited tests update only internal field bindings
and retain the public-key expectations and input cases.

The final review follows `from_json` through the renamed value into `to_json`:
`{"retry": true}` still reaches the supplied client as true, while `{}` resolves
to false and serializes explicitly as `{"retry": false}`. The adapter's unknown
field rejection and client's extra-field behavior remain covered by the original
cases. These checks support the applied rename independently of whether a reader
prefers the new spelling.

Recovery for this demonstration is discarding the isolated copy. In a project,
the equivalent recovery would reverse the focused internal diff and rerun the
same contract checks. Coverage is bounded to the supplied adapter and client;
the suite inspects schema properties rather than running a full schema validator.
External Python consumers would require their own binding inventory before a
real internal rename. Human review remains pending; independent evaluation-checker
execution is outside this demonstration. See
[renaming](../references/renaming.md) and the
[validation report](../templates/validation-report.md#applied-change-checks).
