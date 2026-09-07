# Name APIs, schemas, and configuration

Names crossing a process, storage, or operator boundary participate in a
contract. Choose them by identifying the operation or value, its consumers, and
the convention that governs that surface. Review source names, serialized
spellings and behavior separately: a name can improve source readability while
an established wire spelling remains necessary for compatibility.

The design procedures here are local engineering judgment informed by the
[language claims](evidence.md#lang-09) and
[compatibility claims](evidence.md#compatibility-claims). Those registers name the
scope and strength of each source. [Renaming](renaming.md) owns decisions about
aliases, rollout, retirement and recovery when changing an existing contract.

## Match operation names to the API paradigm

Begin with the effect and response: what does the request ask for, when does the
effect occur, and what does a successful response establish? Then choose the
API's grammar. A command-oriented interface may use an imperative operation;
a resource-oriented interface may combine an HTTP method and a resource path;
a library query may use a noun phrase when its language favors that usage.
Inspect an existing API specification and neighboring calls before transferring
one style to another.

In Google's resource-oriented APIs, prefer standard methods when their semantics
fit. [AIP-136](https://google.aip.dev/136#guidance) gives custom methods verb/noun
names and permits a custom verb after a colon in the URI. Thus a rule requiring
all URLs to be verb-free would reject a supported convention. Swift's
[fluent usage guidance](https://www.swift.org/documentation/api-design-guidelines/#strive-for-fluent-usage)
also distinguishes effectful operations from value-oriented queries. Neither
convention determines an arbitrary API's behavior.

Original pseudocode use sites for a stipulated export service:

```text
RPC command: StartExport(report_identifier) returns operation_identifier
Resource custom method: POST /reports/report-42:startExport
Query: export_operation(operation_identifier) returns current operation state
Event: ExportCompleted(operation_identifier, artifact_identifier)
```

Here starting an export accepts asynchronous work; completion means the artifact
has been produced. `StartExport` preserves that distinction, whereas a command
named `ExportCompleted` would describe the later occurrence. The resource form
illustrates an AIP-style custom operation; the other forms illustrate a local
contract. The sketches are unexecuted pseudocode, with no live service implied.
Check the response, operation state machine, and event publication point before
adopting the names. See [types and messages](types-and-messages.md) for commands,
events and errors, and [functions and methods](functions-and-methods.md) for
operation expectations.

HTTP verbs have protocol meanings that need an application contract for further
interpretation. In particular, [RFC 9110 section 9.3.5](https://www.rfc-editor.org/rfc/rfc9110.html#name-delete)
defines DELETE in terms of the resource association. Choose storage-state names
from implemented transitions and persistence behavior.

## Preserve serialized meaning

For a field, establish its type, cardinality, presence rules, and meaning before
choosing a spelling. Google's [AIP-140](https://google.aip.dev/140) uses plural
names for repeated fields, describes fields as state, and normally omits `is`
from boolean names. It permits a state such as `disabled`; positive polarity
and an `is_` prefix are separate choices. Apply the actual boolean truth table.
A field expressing configured retry policy cannot acquire a capability meaning
merely by being called `can_retry`.

[Protobuf's style guide](https://protobuf.dev/programming-guides/style/)
uses snake-case fields and capitalized message names. Inspect generated-language
spellings as part of review. A protobuf field's number serves a binary encoding
role, while its name can matter to generated source and JSON.
[ProtoJSON](https://protobuf.dev/programming-guides/json/#format-description)
has specific name, presence, and default rules. A binary-compatible change needs
separate assessment for JSON readers and stored documents. See
[COMP-004 and COMP-005](evidence.md#comp-004).

Write a small field contract including one populated value, an omitted value,
and any explicit empty or null value the format supports. Read the serializer
and consumer together. A collection `export_operations` and a scalar
`export_operation_count` preserve different information even when their current
values agree. Test round trips and supported old inputs when applying changes;
follow [renaming](renaming.md) for the migration procedure.

## Make database and analytics names answer a specific question

Database and analytics names need the relation's grain as well as its subject.
State what one row represents, which key identifies it, and the time basis of
any measurement. This is local modeling guidance, not a universal SQL naming
standard. Inspect the database project's identifier and quoting conventions.

For an original reporting model, suppose one row records one export attempt and
another groups completed attempts by their completion date in UTC. The names
`export_attempts` and `daily_completed_export_counts` expose those different
purposes. A column `completed_export_count` fits the grouped count; the shorter
`exports` leaves open whether a value is a collection, bytes, or a count. If the
metric measures distinct reports instead, revise the concept and aggregation
before recommending a report-count name.

Validate names against the query's grouping keys, deduplication, filters, time
zone, joins, and null handling. Review dashboards, scheduled queries, extracts
and data dictionaries as consumers. PostgreSQL supports a direct
[column rename](https://www.postgresql.org/docs/current/sql-altertable.html),
but its availability establishes a mechanism; consumer and deployment evidence
still determine the suitable change plan. [Renaming](renaming.md) compares those
choices and their verification needs.

## Give configuration an explicit scope and default

For each key, read its parser, default resolution, and effective use. Establish
whether it configures a process, tenant, request, connection, or operation. A
nested path can carry scope that would otherwise need repeating in every key.
Choose names from the value actually consumed, with a documented precedence
among files, environment variables and command-line flags when those exist.

Original unexecuted configuration pseudocode:

```text
export_worker:
  retry_enabled: false
  retry_delay_seconds: 5
```

In this stipulated contract, omission of `retry_enabled` also resolves to false;
`retry_delay_seconds` is a nonnegative interval between retries and defaults to
5. Enabling retries changes policy. It establishes neither network availability
nor eventual success. The delay key names a duration, and its nesting identifies
the worker scope. These names are a clear fit for the stated parser contract;
verification against an actual parser remains pending.

Check omitted, explicit false, zero, null, and invalid values separately where
the parser accepts or rejects them differently. Keep documented and effective
defaults aligned. [AIP-180's semantic compatibility guidance](https://google.aip.dev/180#semantic-changes)
explains why default semantics can affect compatibility in its API scope;
configuration review adopts the same question as local engineering judgment.

A unit suffix is useful when a raw quantity would otherwise be ambiguous.
[AIP-141](https://google.aip.dev/141#guidance) defines quantity conventions for
Google APIs and also supports specialized messages and variable units. A typed
duration or value such as `5s` may already carry the unit in another configuration
format. Verify dimensions and conversion at the parser; choose `frames` or
`samples` from the audio representation actually used. See
[variables and state](variables-and-state.md) for quantities and state semantics.

Public flags and environment keys deserve consumer review. For example,
[argparse's destination mapping](https://docs.python.org/3/library/argparse.html#dest)
can preserve a flag spelling while selecting an internal attribute name.
[Kubernetes' deprecation policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/)
is a concrete example of configuration and CLI compatibility promises. Apply
the support promise of the project being changed.

## Separate persistent identity, labels, and aliases

An identifier selects an enduring referent under a defined scope. A display label
helps a human recognize it and may change with language or preference. An alias
provides another accepted designation with an explicit mapping. Establish which
role each field serves before judging spelling or mutability.

An original export-template record illustrates the distinction:

| Field | Example value | Contract |
| --- | --- | --- |
| `template_identifier` | `monthly-usage` | Stable identifier unique within the tenant |
| `display_name` | `Monthly usage summary` | Editable human label |
| `display_name_locale` | `en` | Language of that label |
| `aliases` | `["usage-summary"]` | Collection of accepted alternate lookup terms mapping to this template |

Changing the display label to `Usage by month` preserves this template's identity
and saved references to `monthly-usage`. The readable identifier is stable by
contract. An opaque identifier could also fit; opacity alone establishes no
identity policy. The W3C's informative
[Cool URIs note, section 4.5](https://www.w3.org/TR/2008/NOTE-cooluris-20081203/#cooluris)
supports persistent, mnemonic identifiers in its HTTP/RDF setting.
[SKOS](https://www.w3.org/TR/skos-reference/#labels) formally distinguishes lexical
labels from resource identity and constrains preferred labels by language. The
record above is a local software analogy, not a SKOS implementation.

For aliases, establish uniqueness scope, normalization, ambiguity handling and
the canonical spelling emitted by serializers or links. For an old and a new
configuration key accepted together, define conflict behavior explicitly; it
may differ from display-label lookup. A policy that rejects conflicting values
is a candidate, not a universal parser rule. Review alias lifecycle and stored
references through [renaming](renaming.md).

## Record the decision and its verification

Show the chosen name at its actual boundary: operation signature, request,
serialized document, query, or configuration path. Explain its meaning and the
convention it follows. Then separately report which implementation, consumer,
default, state and persistence evidence was inspected. A schema-only review can
confirm declared spellings and types; consumer behavior needs stronger evidence.
Use [contextual validation](contextual-validation.md) for that distinct review.
