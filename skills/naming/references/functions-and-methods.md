# Naming functions and methods

An operation name sets expectations about what happens when a reader calls it.
Establish its inputs, result, effects and failure paths, then test the complete
call against those facts. The practical review below is local engineering
judgment grounded in the scoped conventions in the
[evidence register](evidence.md#lang-02).

## Start with the operation's contract

Read the implementation, callers, tests, and public documentation. Write one
sentence describing the successful path, followed by material alternatives such
as missing input, rejection or deferred completion. Include state mutation,
storage writes, network requests and published messages when they affect callers.
A verb alone cannot establish these effects.

The following are original hypothetical contracts and candidate names. Each
recommendation depends on the behavior in its row.

| Observed behavior | Candidate use site | Why it fits |
| --- | --- | --- |
| Calculate buffer duration from frame count and rate | `buffer_duration(buffer_size_frames, sample_rate)` | Names a derived value; units belong in types or the verified numeric contract |
| Look up one shipment, returning absence if missing | `find_shipment(shipment_identifier)` | Singular result and optional lookup, where the project uses `find` this way |
| Return a stored shipment or create and store one when absent | `get_or_create_shipment(shipment_identifier)` | Exposes both retrieval and creation |
| Check a specimen identifier and return violations | `validate_specimen_identifier(specimen_identifier)` | Describes checking under a stated identifier contract |
| Produce a canonical spelling of a specimen identifier | `normalize_specimen_identifier(specimen_identifier)` | Describes transformation under a stated normalization rule |
| Persist a receipt record and return its identifier | `record_specimen_receipt(specimen_identifier, received_at)` | Makes the recording action visible |

These are illustrative calls rather than runnable implementations. Specimen
terminology is supported by [FHIR's material-sample concept](sources.md#con-fhir-specimen);
the identifier rules and receipt operation are stipulated software behavior.
They establish no clinical conclusion. The audio quantities follow
[CON-011](evidence.md#con-011).

A validation operation may legitimately normalize under an existing API contract.
Inspect that behavior and callers before retaining or changing its name. If
checking, transformation and persistence form a coherent domain operation, choose
that domain action and document its contract. If the concept remains unclear,
return to [elicitation](elicitation.md). A proposal to split the operation changes
its design and deserves a separate decision.

## Actions, queries and predicates

Use grammar that fits the ecosystem and the whole expression. Swift distinguishes
imperative effectful methods from value-oriented queries, including mutation and
derived-value pairs such as `sort` and `sorted`. This is a scoped convention:
other languages and established libraries use other pairs
([LANG-02](evidence.md#lang-02)). A calculation can read naturally as a noun
phrase. A predicate can read as an assertion such as `overlaps(interval)` without
an `is` prefix.

For mutation, inspect both the receiver and aliased arguments. An operation
returning a value may also modify shared state. In an original use-site sketch,
`normalized_identifier = normalize_specimen_identifier(specimen_identifier)`
suggests a derived identifier under the stipulated contract. If it instead edits
a stored specimen record, a recording or update action may better describe its
observable work. The assignment syntax supplies evidence about reader
expectations; the implementation establishes the actual effects.

For boolean results, preserve policy versus capability and the precise predicate.
`retry_policy.should_retry(...)` can describe a policy decision when the
implementation evaluates that policy. `connection.is_available()` describes an
observed state under its measurement contract. Review false as well as true
cases using [boolean meaning and polarity](variables-and-state.md#boolean-meaning-and-polarity).

## Lookups, conversions and failure

Treat verbs such as `get`, `find`, `load`, `fetch`, `parse`, `convert` and `try`
as candidates governed by project conventions and actual contracts. To choose
among them, inspect whether the operation reads memory, performs I/O, creates an
object, returns absence, raises an error, or returns an error value. Check how
callers distinguish an empty result from an unavailable service. Encode the
most useful distinction in the name, and make the full contract accessible in
types and documentation.

Rust has specific ownership and cost conventions: API Guidelines C-CONV associates
`as_` with free borrowed views, `to_` with conversions involving work or
copied/borrowed inputs, and `into_` with consuming owned non-Copy inputs. Consuming
can be cheap or costly. Its getter and iterator rules also have category-specific
exceptions ([LANG-05](evidence.md#lang-05)). Consult
[language conventions](language-conventions.md) before applying those spellings.
The Rust recommendations provide no basis for renaming every conversion in
another ecosystem.

For parsing, state the accepted representation and failure behavior. An original
contract might give `parse_shipment_identifier(text)` a validated identifier or
an error result; `format_shipment_identifier(shipment_identifier)` might produce
a display representation. Check whether formatting round-trips before claiming
that relationship. A `try_` prefix only communicates a particular error strategy
when the project gives it that meaning. Examine exceptions, error values and
caller branches independently of the prefix.

## Parameters, cardinality and complete calls

A parameter names its role in the operation. Compare its declaration with actual
positional and keyword calls. Two timestamps might be an observation time and a
deadline; two prices might be a resting price and an aggressor limit. Shared
primitive types make those role words particularly useful.

In this original pseudocode, receipt persistence uses the specimen's identifier
and the supplied recording instant:

```text
receipt_identifier = record_specimen_receipt(
    specimen_identifier = specimen.identifier,
    received_at = clock.instant()
)
```

`receipt_identifier` identifies the resulting receipt record. Naming the result
`specimen` would suggest a different entity. If the actual return is an acceptance
ticket for queued work, name it for that ticket and review the operation against
its deferred contract. Similarly, compare `find_shipment` returning one optional
record with `find_shipments` returning a collection; inspect filtering and
pagination before promising all matching records.

Receiver context and labels can make a concise name clear. Read the complete
call aloud, then examine a realistic caller where context is less convenient.
Swift explicitly includes argument labels in this assessment
([LANG-02](evidence.md#lang-02)); other ecosystems can apply the review question
without copying Swift syntax. Public keyword names also need
[compatibility review](renaming.md).

## Async work and completion boundaries

Determine what completion means: dispatch accepted, job queued, remote response
received, state persisted, or a transaction committed. A future, promise, or task
type may expose asynchronous execution; some frameworks use a spelling suffix.
Follow the verified project convention rather than imposing a universal `Async`
rule. Inspect cancellation and failure paths along with the successful result.

For an original queued-operation contract, `request_specimen_receipt_recording`
returns an acceptance ticket after enqueueing. `record_specimen_receipt` could
fit an operation that returns after the recording contract completes. Choose
from the actual boundary, and document what awaiting the result establishes.
Event publication has its own boundary, discussed in
[types and messages](types-and-messages.md#commands-events-and-lifecycle).

## Verify a recommendation

Select the name using its contract and representative calls. Then make a distinct
pass through callers, side effects, return cardinality, error handling, and async
completion. Compare it with neighboring operations and public documentation.
Record concrete evidence and any missing path inspection. A successful syntax
check establishes syntax; a behavior test establishes its exercised path; neither
alone proves that the name communicates the intended operation.

See [contextual validation](contextual-validation.md) for the review procedure,
[APIs, schemas and configuration](apis-schemas-and-configuration.md) for public
operation contracts, and [types and messages](types-and-messages.md) for results,
errors and command/event distinctions.
