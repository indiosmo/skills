# Apply and verify a rename

A rename changes how a program refers to an established concept. Start with a
name justified by [contextual validation](contextual-validation.md), then map the
affected declarations, uses, and contracts before editing. This page helps
you carry out an authorized change and show that its behavior and compatibility
match the intended scope.

Fowler's refactoring definition supplies the behavior-preservation criterion;
the procedure here is local verification policy. See
[COMP-001](evidence.md#comp-001), [COMP-014](evidence.md#comp-014), and
[LOCAL-006](evidence.md#local-006). A clearer name can accompany a behavioral
redesign, but that redesign needs its own explicit decision and verification.

## Establish the change boundary

Record the declaration's location, current and selected spellings, meaning,
authorized edit scope, and observable behavior. Determine what the request
authorizes: a recommendation, a local edit, a compatibility migration, or a
deployment. Continue work already authorized by the request and prior decisions.
Seek missing intent only where it changes the concrete action's scope.

For a small local rename, a sentence and a reviewed diff may be enough. A public
change benefits from the [rename plan](../templates/rename-plan.md), whose fields
capture consumers, compatibility decisions, verification, and recovery.

Establish a baseline using the relevant behavior checks before editing. Include
the values that distinguish the concept from tempting alternative meanings:
policy enabled versus disabled, an exhausted retry budget, a missing value,
different units, or the state a proposed modifier would exclude. Tests express
the intended observable contract independently of the proposed spelling.

### Trace bindings and representations

Inspect the declaration and actual references with the language's symbol tools
when available. Supplement that evidence with scoped text searches. Begin in
the known module and its consumers, then expand through discovered dependencies.
Search both old and proposed spellings to expose collisions and existing aliases.

Apply the edit with a language-aware rename tool when available, using its preview
to check the selected declaration and affected bindings. Inspect the resulting
diff even when the tool reports success. When editing manually, use the binding
map to update references in small groups and run the affected calls; scoped text
searches supplement that map.

| Surface found in the project | Evidence to inspect |
| --- | --- |
| Ordinary bindings | Declarations, imports/exports, overloads, positional and keyword calls, receiver types |
| Runtime-selected names | String attribute lookup, plugin registries, entry points, reflection, configured import paths |
| Generated code | Schema or generator inputs, generated bindings, and the supported regeneration command |
| Persisted representations | Serialized keys and enum strings, stored qualified names, database queries, and historical messages |
| Operational interfaces | Configuration keys, command options, environment mappings, telemetry fields, and saved queries |
| Reader-facing contracts | Documentation, glossary, examples, tests, public schema, and existing client code |

Classify every relevant search hit by its referent and contract. The same spelling
can belong to an unrelated local symbol, a compatibility alias, or a wire field
that should retain its spelling. A global replacement cannot make that distinction.
Inspect text-search results as candidate references rather than treating their
count as proof of a complete binding map.

Python illustrates two extra surfaces: `getattr` can select an attribute through
a string, and pickle locates functions/classes through qualified importable
names. Their consequences are specific to those mechanisms; inspect the runtime
features actually present. See [COMP-006](evidence.md#comp-006) and
[COMP-007](evidence.md#comp-007).

## Preserve predicates and effects

Consider an original retry scenario whose policy allows a further attempt only
when retries are enabled, the failure is transient, and the attempt count is
below the limit. The abbreviated `retry_ok` could become `should_retry` when
those facts establish a policy decision. A capability name would need evidence
about the capability it promises. This illustrative Python use site exposes the
policy inputs and result:

```python
retry_decision = should_retry(
    retry_enabled=True,
    transient_failure=True,
    attempt_count=1,
    attempt_limit=3,
)
```

Under the stipulated contract, this call returns true. The following contract
table defines the required combinations independently of the chosen spelling:

| Retries enabled | Transient failure | Budget remaining | Decision |
| --- | --- | --- | --- |
| false | false | false | false |
| false | false | true | false |
| false | true | false | false |
| false | true | true | false |
| true | false | false | false |
| true | false | true | false |
| true | true | false | false |
| true | true | true | true |

After editing, check the complete truth table through the renamed function and
its callers. Include boundary counts at and below the limit. Update keyword
arguments with the parameter they bind, imports with the declaration they expose,
and examples with the operation they demonstrate. Preserve an unrelated symbol
whose existing name describes its own behavior.

Keep return values, exceptions, mutation, defaults, units, and state transitions
fixed unless the task separately authorizes changes to them. For example,
renaming a negative flag to a positive flag can require a value inversion;
that is a representation change with affected callers and serialized values to
inspect. It deserves an explicit mapping rather than a spelling-only edit.
See [variables and state](variables-and-state.md) for polarity and
[functions and methods](functions-and-methods.md) for effects.

## Choose compatibility deliberately

Public spellings have consumers. Google's AIP-180 distinguishes source, wire,
and semantic compatibility within its API policy; this is a useful way to
identify separate checks in another project. Determine that project's actual
support promise before applying a migration rule. See
[COMP-002](evidence.md#comp-002) and
[API, schema, and configuration naming](apis-schemas-and-configuration.md).

An original adapter might expose the JSON field `retry` while storing an
internal value named `retry_enabled`. Its public contract can continue to accept
and emit `retry`; a serialization mapping makes the relationship explicit.
Changing the internal name then needs internal caller checks plus existing-client
and wire checks. Changing the JSON field as well expands the compatibility task.

| Approach | When it fits | Tradeoff and required evidence |
| --- | --- | --- |
| Retain the current name | Contextual review finds it accurate and useful | Explain the retained meaning and avoid a migration with little benefit |
| Rename internally, retain public spelling | A stable mapping separates internal vocabulary from the external representation | Test mapping, internal uses, defaults, accepted inputs, and exact emitted keys |
| Add an alias | The interface supports equivalent alternate spellings | Define conflicts, precedence, canonical output and support duration; test both spellings and conflicting input |
| Stage a public migration | Consumers, release policy, and persisted data permit a coordinated transition | Verify supported old/new reader-writer combinations, deployment order, stored data, and the retirement gate |
| Rename directly | Binding and consumer evidence establish a coordinated change boundary | Review the complete affected scope and run representative old-contract behavior checks |

These are conditional approaches. For a concrete choice with several viable
options, apply [selection](selection.md): use grounded scores for the actual
complexity, compatibility, blast radius, maintenance, coupling, and reversibility.
Record the rationale directly when the established constraints make one approach
a clear winner.

Different encodings need different evidence. A protobuf field number can remain
stable while its JSON spelling changes. ProtoJSON's enum-alias migration sequence
depends on compatible readers preceding changed writers, serializer ordering,
persisted data, and rollback support. Apply those rules within that format;
an arbitrary JSON adapter needs its own alias semantics. See
[COMP-004](evidence.md#comp-004) and [COMP-005](evidence.md#comp-005).

A database may support a direct column rename, as PostgreSQL does
([COMP-010](evidence.md#comp-010)). Evaluate its
locks, dependencies, and external SQL. An add/backfill/cutover migration is useful
when mixed versions need both representations. In that case, establish the
source of truth, dual-write failure handling, resumable backfill, and a retirement
gate. The naming task supplies a proposal when execution lies outside its
authorized scope. This migration checklist is local engineering policy
([LOCAL-010](evidence.md#local-010)).

## Verify the edited result

Review the resulting diff by declaration and contract. Run fresh checks that
cover the boundaries discovered above, and preserve their native diagnostics.

1. Inspect changed declarations, imports, calls, documentation, and generated
   outputs. Reclassify remaining old spellings and collisions with the new name.
2. Run affected behavior and caller tests that exercise keyword calls and boundary
   cases. Compare with the independently established baseline contract.
3. Exercise retained clients, schema validation, serialization, and deserialization
   when those surfaces exist. Check omitted values, false, null, defaults and
   round trips according to the actual accepted-input policy.
4. Verify examples through their documented commands. Check unrelated symbols
   and intentionally retained public spellings directly.
5. Reassess the selected name against the final use sites. Record any mismatch,
   correct the name or revisit the concept, then rerun affected checks.

An edited test suite alone can conceal an accidental behavior change. Evaluation
of rename outputs therefore uses trusted contract assertions outside the edited
checkout, alongside diff and affected-use inspection. In everyday work, the same
principle means deriving expectations from the established contract and comparing
the tests with it. See the [fixture checks](../tests/README.md).

## Record evidence and recovery

Report the name and rationale, edited scope, commands and observed results,
preserved compatibility policy, and remaining uncertainty. Separate the naming
assessment from applied-change checks in the
[validation report](../templates/validation-report.md). Passing checks establish
their exercised paths; dynamic or inaccessible consumers remain explicitly
unverified. A description-only migration recommendation identifies the concrete
checks needed when an implementation becomes available.

For a local edit, recovery can be a focused reversal of that diff while preserving
other work. For a deployed representation change, check that the previous code
can read values written after cutover or that a tested conversion exists.
Stored messages, backups, offline consumers and dormant clients can extend the
compatibility window. Zero observed use in logs needs instrumentation and support
context before it can support retirement. These recovery and retirement questions
are local engineering policy: [LOCAL-010](evidence.md#local-010).
