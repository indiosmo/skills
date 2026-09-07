# Retaining an adequate public name

An engineer reviewing the retry configuration suggests changing the JSON key
`retry` to `retry_enabled` for more explicit boolean wording. The original
[public-contract fixture](../tests/fixtures/public-contract/README.md) supplies
the adapter, an existing client, a schema, and compatibility tests. The request
here is a naming assessment of the published key.

The concept is a configuration setting: true enables automatic retries after
failures. Execution uses that setting alongside failure classification and an
attempt budget. The JSON object is explicitly a retry configuration, and its
schema describes `retry` as a boolean with an effective false default when
omitted. That surrounding contract contributes meaning to the short key.

Candidate spellings are `retry`, `retry_enabled`, and `should_retry`.
`retry_enabled` spells out the policy state and is useful internally.
`should_retry` suggests a decision for a particular failed attempt; the stored
setting alone supplies only one input to that decision. The public use is:

```json
{"retry": true}
```

**Decision: retain the public key `retry`.** It is adequate in the inspected
configuration context, and an existing consumer reads precisely that key.
The explicit stable-wire requirement makes retention the clear winner for this
assessment. A more descriptive internal field can coexist with it through the
adapter, as the [internal rename example](public-contract-rename.md) demonstrates.

The distinct contextual review checks the candidate independently of its brevity:

| Inspected context | Finding | Outcome |
| --- | --- | --- |
| [Schema](../tests/fixtures/public-contract/schema.json) | Defines `retry` as the boolean configuration field | Meaning is explicit at the public boundary |
| [Adapter](../tests/fixtures/public-contract/api.py) | Reads omission as false and emits exactly `retry` | Reader and writer agree on spelling and default |
| [Existing client](../tests/fixtures/public-contract/client.py) | Reads `configuration.get("retry", False)` | Changing the emitted key could silently yield false |
| [Tests](../tests/fixtures/public-contract/test_compatibility.py) | Assert exact keys, false/true, omission, errors, and existing-client results | Contract checks distinguish compatibility from stylistic preference |

**Review outcome: retain.** The accurate policy interpretation and concrete
consumer coupling support the recommendation. This review recommends no edits.

Verification used an unchanged isolated copy of all five files on 2026-09-06:
`python3 -m unittest -v test_compatibility` reported **Ran 8 tests; OK**. The suite
checks schema properties directly; it does not constitute full JSON Schema
validator conformance. The execution establishes behavior for the supplied
consumer and cases. It cannot establish compatibility with unprovided deployed
clients or stored documents.

Reopen this decision if the object acquires several retry-related settings and
the current key becomes ambiguous, or if an authorized public migration supplies
consumer and support-policy evidence. Human review remains pending. The
[decision template](../templates/naming-decision.md) and
[compatibility guidance](../references/renaming.md#choose-compatibility-deliberately)
capture the same retention rationale for a real project.
