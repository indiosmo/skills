# Validate a name in its surroundings

Contextual validation asks whether the name gives readers accurate expectations
where the software uses and documents it. Perform it after selecting a candidate,
or enter here directly to assess an existing or proposed name. An existing name
can pass. A new candidate can fail despite fluent grammar and familiar words.

This distinct review is local engineering policy
([LOCAL-005](evidence.md#local-005), [LOCAL-007](evidence.md#local-007)).
Use-site clarity has practitioner support in
[Swift's guidance](sources.md#lang-swift); naming and documentation disagreements
are review prompts in [LANG-14](evidence.md#lang-14). Research findings retain the
conditions described in [empirical research](empirical-research.md).

## Establish the review scope

Record the name, declaration identity or described artifact, proposed meaning,
input evidence, and relevant revision. Read the behavior before adopting the
candidate author's interpretation. Start with the paths supplied by the request
and follow actual references to callers, contracts, and related concepts.
Scoped text search helps locate uses; language-aware references help distinguish
bindings that share a spelling. Record the scope each technique covers.

A brief can summarize the intended meaning. Validation compares that intention
with implementation and surrounding evidence. A selected candidate's winning
score supplies a hypothesis to check. It supplies no evidence about uninspected
callers or serialization behavior.

## Inspect the contexts that establish meaning

| Context | Questions to resolve | Concrete evidence to record |
| --- | --- | --- |
| Declaration and behavior | What values, units, counts, states, results, effects, and failures does it represent? | Symbol and path; branch, return, mutation, parser, or state transition |
| Representative callers | What can readers infer from receiver, arguments, return handling, conditions, and error paths? | Ordinary call, boundary use, keyword call, and materially different consumer |
| Related names and scope | Which nearby concept could be confused with this one? Does qualification help? | Peer declarations, imports, namespaces, collisions, and search terms |
| Vocabulary and conventions | Does this term mean the same thing in this bounded context? Is its spelling appropriate here? | Glossary entry, applicable style rule, practitioner source, and inspected peers |
| Prose and examples | Do documented promises and examples agree with the proposed meaning? | Heading or example location and the supported behavior it describes |
| Tests | Which claims have actual executed checks? Are boundary conditions represented? | Test identity, command, observed result, and exercised cases |
| Contracts | Is a spelling part of an API, schema, generated interface, configuration, registry, or stored record? | Contract field, generated name, parser key, serializer mapping, or compatibility rule |

Apply the relevant rows in proportion to the artifact. For a local integer,
declaration, reads, units, and nearby names may establish enough context. A public
operation expands the review to consumers and published contracts. Follow
[API and schema guidance](apis-schemas-and-configuration.md) for those surfaces.
For abbreviations, check audience recognition and the project's
[full-word policy](evidence.md#local-002). A familiar short term can be appropriate
within its local scope; measured benefits from particular studies keep their
task-specific limits ([EMP-002](evidence.md#emp-002)).

Record disagreements explicitly. When documentation and code conflict, identify
both claims and resolve the intended contract through evidence or a focused
question. Naming the implementation accurately may expose a behavior defect that
needs a separate decision. Preserve the observed behavior while determining scope.

## Reject a plausible name with use-site evidence

Consider this original subscription example, shown as an illustrative Python
excerpt with application objects supplied by the surrounding program. The operation
counts subscriptions in either the `trial` or `paid` state. The documentation
defines both states as eligible for the application's access summary.

```python
def count_access_subscriptions(subscriptions):
    return sum(
        subscription.state in {"trial", "paid"}
        for subscription in subscriptions
    )

access_summary.subscription_count = count_access_subscriptions(subscriptions)
```

Suppose a proposal calls this operation `count_paid_subscriptions`. Its action,
object, and plural count read naturally. Validation rejects it: the function's
membership expression counts `trial`, and the caller presents an access summary
covering both states. The supplied documentation agrees with that broader scope.
The word `paid` would give a reader the wrong expectation about the result.

Retain `count_access_subscriptions` under this scenario's vocabulary. Recheck the
membership expression, the access-summary call, and the definition of access
eligibility. Exercise an empty collection, a trial subscription, a paid
subscription, and an ineligible state in the real implementation. Expected counts
for those single-state cases are 0, 1, 1, and 0. Report execution only after those
checks actually run. These are original software states, with their meanings
defined by the scenario.

This review has changed the recommendation through contextual evidence. Merely
repeating that the proposed name is specific or uses full words would miss the
scope error. The [rejection example](../examples/rejecting-a-plausible-name.md)
develops the route further.

## Retain, reject, or revisit

Record the contextual finding separately from the proposed action:

- **Supported:** inspected behavior, representative uses, vocabulary, and
  applicable contracts support retaining or adopting the name within the reported
  scope.
- **Rejected:** a concrete mismatch contradicts the name. State the evidence and
  the expectation that the name would create; offer a supported alternative.
- **Provisional:** the available evidence supports a scoped interpretation while
  material contexts or assumptions await resolution. Identify the evidence needed.

Recommend revisiting the concept when contradictory or incomplete evidence leaves
the thing itself unclear. Return to [elicitation](elicitation.md) with the material
question. Recommend revisiting selection when meaning is settled but another
expression fits the actual callers or neighboring concepts better; reopen the
relevant comparison criteria.

Record decision status separately: proposed, accepted, or unresolved. Acceptance
requires an actual decision by the person or role authorized to choose the name;
identify that authority and the recorded decision. An agent's supported contextual
finding remains a recommendation until that acceptance occurs. Human naming
judgment and executed behavior checks each retain their own evidence and scope.

Retention can be appropriate even when an alternative has a stylistic advantage.
A stable public spelling and existing consumer expectations may outweigh that
advantage ([COMP-003](evidence.md#comp-003)). Record the accurate interpretation
and the compatibility evidence. Substantive misrepresentation still needs a
finding and a scope-appropriate correction or migration recommendation.

For a revision, recheck the failed finding and contexts its correction affects.
Changing a qualifier may alter neighboring distinctions; changing a predicate
can invert callers. Recheck those uses and record the final outcome. Authorized
applied changes also follow [renaming](renaming.md), including binding identity,
affected references, truth conditions, and public compatibility.

## Report evidence and limits precisely

A useful report names the artifact and outcome, identifies examined paths and
symbols or documentation sections, links each finding to evidence, and records
checks with their observed results. Separate static inspection, executed behavior,
and human judgment. Give remaining uncertainties and the next evidence needed.
Use the [validation report](../templates/validation-report.md) for a substantial
review; a small review can express the same information in a paragraph.

For description-only input, an appropriate result is: "`retry_limit` fits the
supplied definition: the maximum number of retries after the initial request.
The description supports its numeric meaning and distinction from attempts.
Implementation, caller, and public-contract fit remain unverified; the parser,
retry comparison, representative calls, and exposed configuration schema would
establish those properties." Keep the recommendation provisional to that scope.

A failed or unavailable tool belongs in the report with its affected coverage.
Continue independent inspection that remains possible. Passing tests substantiate
their exercised paths; a scoped search substantiates occurrences within its
searched files. State the scope that the evidence actually proves.
