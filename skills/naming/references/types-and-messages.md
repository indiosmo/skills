# Naming types, roles and messages

A type name tells readers what its instances represent and which expectations
travel with them. Establish identity, membership, supported operations and
lifecycle before choosing a noun or suffix. The modeling questions in this page
are local engineering guidance; formal ontology and framework conventions retain
the scopes recorded in the [evidence register](evidence.md#con-005).

## Entity, value and role

For an abstract class description, begin with what one instance represents to
its callers. A few method names may suggest a mutable session, a reusable policy,
or a result value. Use [elicitation](elicitation.md) to distinguish those roles
with a caller or lifecycle scenario before committing to a type name. Label
proposed uses as hypotheses until the supplied behavior supports them.

Ask what makes two instances the same thing, what can change while that identity
persists, and what conditions make an instance a member of the type. These
questions help distinguish the following original software contracts:

| Contract | Candidate type | Evidence to inspect |
| --- | --- | --- |
| Record of a particular specimen, tracked through updates by identifier | `Specimen` | Identifier allocation, lookup, and update behavior |
| Parsed identifier value compared by its specified components | `SpecimenIdentifier` | Parsing, equality, and representation rules |
| Receipt record linking a specimen to a recorded receipt instant | `SpecimenReceipt` | Record identity, linked specimen, and timestamp |
| Object acting as the receiver in a defined transfer operation | `Receiver` | Membership conditions and the operations required by that role |

FHIR supplies the [specimen concept](sources.md#con-fhir-specimen); the software
identity, receipt, and role contracts above are example assumptions. A name such
as `SpecimenIdentifier` describes a key value, while `Specimen` describes the
modeled material sample through its record. The identity behavior still requires
implementation evidence.

A role can be acquired or lost while an underlying entity continues to exist.
A relationship alone may leave the intended role uncertain: determine what a
`Receiver` receives and under which contract. Read the local glossary and actual
membership conditions before adding professional or organizational titles.
A healthcare employment relationship, for example, supplies insufficient evidence
for naming a type after a clinical credential. Keep assertions bounded to the
observed software model ([CON-005](evidence.md#con-005),
[LOCAL-001](evidence.md#local-001)).

OntoClean's role analysis offers a useful conceptual check, with a specific
constraint direction: an anti-rigid parent property constrains its children to
be anti-rigid. In its illustrative taxonomy, placing Human under Student violates
that constraint; Student under Human is permitted by that constraint
([CON-004](evidence.md#con-004)). Applying this to software is an analogy.
Inheritance, interfaces, composition, and persistence each require their own
language and behavioral contracts. A naming review can identify a disputed
membership rule and request evidence without deciding a replacement hierarchy.

## Capabilities and policy

Name an interface or protocol for the responsibility its implementations provide
when that is the organizing concept. A protocol supporting serialization may use
a capability name under its ecosystem's convention. Swift explicitly discusses
capability protocol suffixes; other ecosystems have different grammar
([LANG-02](evidence.md#lang-02)). See
[language conventions](language-conventions.md) for the applicable spelling rules.

Distinguish providing an operation from deciding whether it should be used.
Under an original retry contract, `RetryPolicy` evaluates configured retry rules,
while `RetryExecutor` performs an accepted retry request. These candidates fit
only if inspection establishes those respective responsibilities. Implementing
an execution method establishes an interface capability; policy permission,
current resources and execution success have their own predicates and evidence.
Use [variables and state](variables-and-state.md#boolean-meaning-and-polarity)
to review those distinctions at use sites.

A generic-looking type can be precise in a framework. Assess `Handler`, `Factory`,
`Adapter`, `Repository` or `Manager` against its documented role and actual
clients. For example, `SpecimenReceiptHandler` can be informative where a
framework binds handlers to specific messages and the implementation handles
specimen receipts. A custom `SpecimenManager` with unrelated operations needs
closer inquiry into the shared responsibility. The noun alone establishes
neither a sound abstraction nor a defect.

Peter Hilton's [Naming smells](sources.md#lang-hilton-smells) provides review
prompts for vague names, and Steve Yegge's
[Execution in the Kingdom of Nouns](sources.md#b20) offers an attributed critique
of excessive action wrappers. These are practitioner perspectives
([LANG-14](evidence.md#lang-14), [LANG-15](evidence.md#lang-15)). Use them to ask
what responsibility holds the type together; a rename and an architecture change
remain separately scoped decisions.

## Collections as abstractions

Plural values can represent ordinary collections. A richer type name should
correspond to richer established behavior: membership rules, ordering,
aggregation, permitted operations, or lifecycle. A class wrapping a list does
not by itself establish a new domain concept.

For example, `List<Observation>` is an illustrative type sketch for a list of
observations. A `DiagnosticReport` requires the actual report context and
relationships supported by the modeled report. FHIR R5 distinguishes
[Observation and DiagnosticReport](sources.md#con-fhir-observation);
counting the elements alone cannot establish report semantics
([CON-013](evidence.md#con-013)). Equally, a `Shipment` and a `Consignment` need
their own modeled boundaries under the scoped
[UN/CEFACT vocabulary](sources.md#con-uncefact-vocabulary). Grouping records into
a container cannot supply a transport contract.

Review the abstraction's construction and public operations. If its guarantees
justify a domain name, define those guarantees. If it represents an ordinary
sequence, a collection type and a plural value name can communicate that directly.
See [cardinality and keys](variables-and-state.md#cardinality-optional-values-and-keys).

## Errors and outcomes

Name an error for the failure condition a reader needs to recognize or handle.
Inspect the operation that produces it and the caller's recovery branch.
A hypothetical `SpecimenIdentifierParseError` can represent failure to parse an
identifier under a defined syntax; it establishes a software representation
failure. A type implying a clinical assessment would require a separate domain
contract and evidence.

Use the language's exception and result conventions. PEP 8 recommends `Error`
for error exception names, with signaling exceptions providing an important
boundary ([LANG-03](evidence.md#lang-03)). A result type such as `ReceiptResult`
needs explicit variants or fields for its possible outcomes; broad words like
`result` can be useful within a precise operation context. Compare `ReceiptRecorded`
and `ReceiptRejected` only after establishing what those outcomes mean and when
they become observable.

A diagnostic message, an exception type, a command rejection, and an event can
serve different contracts even when they describe related failures. Give each
its actual role, then inspect stable serialized discriminators and public
handling before a rename. See [APIs, schemas and configuration](apis-schemas-and-configuration.md).

## Commands, events and lifecycle

A command requests an action. An event records an occurrence under its publication
contract. A state describes an entity at a particular point. Imperative commands
and past-tense events are common DDD conventions in Microsoft's domain-event
guide and Peter Vogel's CQRS discussion, with queue and framework qualifications
([LANG-13](evidence.md#lang-13)). Grammar helps readers; dispatch and persistence
behavior establish the distinction.

Consider this original software example, using the
[FHIR Encounter concept](sources.md#con-fhir-encounter) as vocabulary for a
healthcare interaction. The state names and transitions below belong to the
example's local model. They are stipulated software behavior, separate from
FHIR's enumerated status codes or a clinical workflow recommendation.

| Artifact | Example name | Stipulated contract |
| --- | --- | --- |
| Command | `StartEncounter` | Requests changing the record from `planned` to `started` |
| Current state value | `started` | Stored state after that transition |
| Event | `EncounterStarted` | Records the accepted transition and its recorded timestamp |
| Rejection result | `EncounterStartRejected` | Reports failure to satisfy the transition's preconditions |

Illustrative message and use-site pseudocode:

```text
command = StartEncounter(encounter_identifier, requested_at)
result = encounter_service.handle(command)

if result is EncounterStarted:
    display_started_time(result.started_at)
if result is EncounterStartRejected:
    display_rejection_reason(result.reason)
```

In this example, the handler returns `EncounterStarted` only after its local
transaction commits, and its fields contain the recorded transition time.
That is an explicit example contract to verify in code. The same past-tense name
in a different system could be emitted before commit or in memory; publication,
rollback and delivery guarantees must be inspected separately. A past-tense name
alone establishes neither successful persistence nor transaction commit.

A cancellation request likewise needs a name describing the request; a completed
cancellation outcome requires evidence of completion. A queued `StartEncounter`
may remain pending before processing, and failure handling needs its own result.
Separate request time from transition time when the software represents both.
Existing framework lifecycle callbacks can retain their prescribed grammar,
with documentation explaining the actual trigger boundary.

## Verify the type in use

1. State what an instance represents, how equality or identity works, and what
   grants or ends membership in the type.
2. Inspect construction, public operations, and representative consumers. Check
   that a capability, pattern, or collection name matches its actual guarantees.
3. For messages and states, trace dispatch, transition, failure, publication and
   persistence boundaries. Match timestamps and result variants to those facts.
4. Compare neighboring types, domain vocabulary, and framework conventions.
   Record unresolved modeling questions separately from the proposed name.
5. Make a distinct verification pass against the evidence, reporting the examined
   contracts and missing implementation checks. Apply an authorized rename through
   [renaming](renaming.md) when the decision changes an existing symbol.

Use [foundations](foundations.md) for scoped concepts,
[domain vocabulary](domain-vocabulary.md) for practitioner terms, and
[contextual validation](contextual-validation.md) for an independent name review.
