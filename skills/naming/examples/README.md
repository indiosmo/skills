# Worked naming decisions

These examples show how behavior, vocabulary, scope, and use sites affect a
naming decision. Each establishes its scenario, considers names in context,
explains a recommendation or retained name, and reports a distinct verification
result. Begin with the [human guide](../references/README.md) for the underlying
reasoning and use these examples to see it applied.

## Choose a reading path

For a sparse class or component idea, start with
[an unclear abstraction](unclear-abstraction.md). A concrete scenario separates
two possible concepts and narrows the name through scripted replies; an
unanswered branch keeps the choice conditional. For an ambiguous condition in a
known application, read [eliciting a concept](eliciting-a-concept.md). Continue
with [comparing candidates](comparing-candidates.md) once meaning is established. The
[portable matrix](candidate-matrix.html) makes the second decision reviewable.
For a proposed or existing name, start with
[rejecting a plausible name](rejecting-a-plausible-name.md) or
[retaining an existing name](retaining-an-existing-name.md). For an authorized
edit, follow [boolean polarity](boolean-polarity.md) and
[a public-contract rename](public-contract-rename.md).

The same reasoning supports direct naming assistance and naming during code
authoring. A small established choice can use concise prose; a material unknown
or public boundary needs more evidence. The
[templates](../templates/naming-brief.md) capture that evidence when a separate
record is useful.

## Example coverage

| Example | Artifact and domain | Route and important distinction |
| --- | --- | --- |
| [Eliciting a concept](eliciting-a-concept.md) | Reader-specific saved-search boolean field | Scenario questions resolve material intent; description-level verification stays explicit |
| [Comparing candidates](comparing-candidates.md) and [matrix](candidate-matrix.html) | Names read in declarations and use sites | Hard constraints, grounded scores, audience tradeoff, recommendation, and separate review |
| [Rejecting a plausible name](rejecting-a-plausible-name.md) | Subscription-selection function | Callers and documentation expose active-only wording that excludes grace-period behavior |
| [Retaining an existing name](retaining-an-existing-name.md) | Published retry configuration key | Accurate interpretation and an existing consumer justify retention |
| [Boolean polarity](boolean-polarity.md) | Retry-policy function and parameter | Authorized binding changes preserve truth conditions, keyword calls, imports, and an unrelated symbol |
| [Units and cardinality](units-and-cardinality.md) | Audio variables and fields | Frames, channel samples, sample rate, buffer duration, and measured latency |
| [Domain vocabulary](domain-vocabulary.md) | Trading price roles | Practitioner terms preserve bid/ask and incoming/resting distinctions |
| [Bounded contexts](bounded-contexts.md) | Logistics records and mappings | Shipment, consignment and one-to-many relationships within explicit models |
| [Functions and side effects](functions-and-side-effects.md) | Functions, methods, parameters, and results | Returned value, mutation, and failure determine reader expectations |
| [Types, roles, and events](types-roles-and-events.md) | Clinical software types and messages | Entity, role, command, occurrence, state, and publication boundary |
| [Modules, packages, and files](modules-packages-and-files.md) | Namespaces, imports, and paths | Capability scope, redundant qualification, and resolution collisions |
| [Public-contract rename](public-contract-rename.md) | Adapter API, schema field, and configuration | Internal naming improves while public JSON spelling, defaults, and clients retain their contract |
| [Unclear abstraction](unclear-abstraction.md) | Sparse class purpose and an operation with unsettled responsibilities | Scenario replies narrow identity, lifetime, ownership, and member context; unanswered questions preserve conditional names and redesign boundaries |

## Read verification according to its evidence

Domain sources establish the terminology they define. Each original scenario
establishes its own software behavior. An illustrative or pseudocode example
supports reasoning under those stated assumptions. Its verification identifies
the implementation or callers needed to assess a real project. A scripted
dialogue supplies hypothetical replies for demonstration.

The runnable examples use these input fixtures:

- [Subscription review](../tests/fixtures/contextual-review/README.md) supplies
  code, consumers, a glossary, and an executable contract example.
- [Internal rename](../tests/fixtures/local-rename/README.md) supplies the retry
  predicate, worker caller, usage example, behavior tests, and an independent
  same-spelling operation.
- [Public contract](../tests/fixtures/public-contract/README.md) supplies the
  adapter, existing consumer, JSON schema, defaults, and compatibility tests.

Use a disposable copy for an applied-rename exercise, preserving the packaged
input. Fixture READMEs specify the supported environment and authorized files.
[Test documentation](../tests/README.md) gives the project commands and coverage;
the [evaluation protocol](../evals/README.md) explains independent outcome checks
and human review. Passing an example's behavior checks and judging the selected
name are separate results.

For additional source scope and attribution, consult the
[source register](../references/sources.md). Follow
[contextual validation](../references/contextual-validation.md) to assess a name
in your project, and [renaming](../references/renaming.md) to verify its affected
uses when you apply it.
