# Generate names from the concept

A useful candidate gives readers a truthful way to recognize the concept at its
use sites. Start with the naming brief: concept and behavior, audience, context,
vocabulary, constraints, evidence, and unknowns. A settled local choice may fit
in one sentence. Uncertainty about a state transition or a domain term merits
further [elicitation](elicitation.md) before a name implies that meaning.

The procedure here is local engineering guidance
([LOCAL-003](evidence.md#local-003), [LOCAL-004](evidence.md#local-004)).
Practitioner guidance from [Google](sources.md#lang-google-cpp) and
[Swift](sources.md#lang-swift) informs role, scope, and use-site reasoning.
Their language conventions apply within their stated contexts.

## Condition candidates on unresolved meaning

For sparse input, begin with the
[competing concepts](foundations.md#separate-competing-concepts-before-comparing-words)
and the evidence that distinguishes them. A candidate list becomes useful when
each name has a stated meaning. If responsibility is still open, write a small
conditional set: "If this object records one execution and its outcome,
`ImportRun` fits that interpretation; if it stores a reusable arrangement of
future imports, `ImportPlan` fits that interpretation." These are original
hypothetical contracts. Each condition requires confirmation from the supplied
intent or implementation.

Use these candidates to reveal the decision: show a representative operation
under each interpretation and ask the discriminating question described in
[elicitation](elicitation.md#work-with-sparse-or-abstract-input). Label invented
use sites as hypothetical, and connect each to the responsibility it tests.
Carry the unresolved condition into the brief and any selection output. A
wording preference cannot establish which responsibility the system has, so
keep the final choice open until that meaning is supported. Once it is settled,
vary expression within that concept using the moves below.

## Preserve meaning while varying expression

Write the behavior in ordinary words first. Identify the actor or entity, action
or role, result, and distinctions that matter to readers. Copy the current name
into the candidate set when it accurately denotes that behavior. Then vary one
useful dimension at a time:

| Starting point | Candidate-making move | Evidence that makes the move truthful |
| --- | --- | --- |
| Practitioner term | Use the term in the project's bounded context | Glossary, domain source, expert usage, and matching behavior |
| Role | Name the purpose a value serves in this operation | Declaration and reads showing how the value participates |
| Action and object | Express the operation and its target | Results, mutation, and failure behavior |
| State | Add the state that separates neighboring sets or transitions | Predicate, state machine, or actual filter |
| Context | Add a qualifier needed outside the receiver or module | Representative imports, calls, and collisions |
| Units | Express a quantity's actual unit when spelling carries it | Parser, type, arithmetic, and examples |
| Cardinality | Distinguish one item, a collection, and a count | Return type, iteration, indexing, and counting |
| Related family | Extend a meaningful pattern used for peer concepts | Neighboring declarations and their contracts |

These are ways to express established distinctions. A modifier such as `active`,
`validated`, or `cached` makes a behavioral promise. Establish the filter,
validation, or caching behavior before using it. A capability, a permission,
and a policy recommendation likewise need their own truth conditions; see
[variables and state](variables-and-state.md).

## Work through declarations, calls, and prose

The Python excerpts on this page illustrate naming choices with application
objects supplied by surrounding code.

Consider an original configuration example. A parser reads a nonnegative integer
as the number of retry attempts allowed after the initial request. The value is
compared with `retry_count`, which starts at zero. Its naming brief says that the
readers maintain request delivery code and the project uses full snake-case words.

```python
def should_retry(retry_count: int, retry_limit: int) -> bool:
    return retry_count < retry_limit

if should_retry(retry_count=retry_count, retry_limit=delivery.retry_limit):
    schedule_retry(request)
```

`retry_limit` expresses the policy bound; `maximum_retries` expresses the same
count with an explicit maximum. Both merit consideration if the neighboring
configuration keys leave that choice open. `attempt_limit` introduces ambiguity
about the initial request, so it requires a different contract or clearer
qualification. `retry_enabled` describes a boolean and loses the numeric bound.

Read candidate prose as well: "Set `retry_limit` to zero to allow zero retries"
and "Set `maximum_retries` to zero to allow zero retries." These sentences test
whether documentation can explain the field consistently with its comparison.
They also expose the distinction between attempts and retries. Preserve that
distinction in [selection](selection.md) and the later validation pass.

For a role-based value, compare its actual receiver and use:

```python
resting_price = resting_order.price
crosses = aggressor_price >= resting_price
```

Here the scenario establishes a buy aggressor compared with a resting sell
order. `resting_price` identifies the price's role. Calling it `best_ask` would
add a top-of-book claim requiring evidence about how the resting order was
selected. Trading term support and its scope are recorded in
[CON-009](evidence.md#con-009); the comparison is an original software scenario.

## Keep enough context to recognize the thing

Qualification earns its place when it resolves an ambiguity the reader actually
faces. `delivery.retry_limit` receives delivery context from the receiver.
A free configuration field imported beside several retry policies may need
`delivery_retry_limit`. Assess both the declaration and the least-informed
representative use site; an isolated identifier and a qualified expression give
readers different information ([LANG-01](evidence.md#lang-01),
[LANG-02](evidence.md#lang-02)).

Words such as `data`, `info`, `manager`, and `helper` need a concrete role behind
them. Ask what the object stores or coordinates and which distinction that suffix
communicates. An established framework name can accurately express its role;
retain it when evidence supports that convention. Treat naming smells as prompts
for inspection ([LANG-14](evidence.md#lang-14)). A suffix alone cannot establish
a design defect.

Default to full words under the project's
[abbreviation policy](evidence.md#local-002). Retain familiar domain abbreviations
when appropriate to their local scope and preserve contractual spellings.
The [empirical research](empirical-research.md#full-words-and-familiar-abbreviations)
explains why mechanically shortened words and familiar abbreviations need separate
judgments. A character count supplies little evidence about a candidate's meaning.

## Stop when the useful alternatives are represented

Candidate count follows the uncertainty. One accurate conventional name may be a
clear winner. Two names can expose a real tradeoff. Add candidates when they
offer a distinct truthful expression, rather than filling a quota with arbitrary
synonyms. Retaining a good existing name is a legitimate result. The local
[matrix adoption](sources.md#local-matrix) sets this boundary for naming work.

If every candidate needs an expanding list of unrelated actions, examine the
concept again. For example, an operation that parses configuration and sends a
request needs both effects represented in its brief. Determine whether that
combination is the intended operation. Describe the current behavior accurately;
record any proposed separation as a design proposal with its own scope. Naming
difficulty is an inquiry signal, with bounded supporting practitioner evidence
in [LANG-15](evidence.md#lang-15).

Bring viable candidates, representative uses, hard constraints, and unresolved
assumptions to [selection](selection.md). A direct validation request can proceed
straight to [contextual validation](contextual-validation.md) with its existing
name and evidence.
