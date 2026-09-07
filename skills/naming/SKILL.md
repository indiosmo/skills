---
name: naming
description: Choose, review, and apply software names using concepts, behavior, domain vocabulary, and actual use sites. Use for abstract or underspecified naming requests that need context elicited, class names derived from semantics and usage, related variables across a component and its parent, and naming during code authoring. Covers variables, parameters, fields, functions, methods, types, messages, modules, packages, files, API operations, schemas, and configuration, including candidate tradeoffs, existing-name validation and retention, and authorized renames with compatibility checks.
---

# Naming software

Produce a recommendation or retained name in context, its rationale, and a
distinct verification result. Use the [human guide](references/README.md) for
the reasoning. Load the selected route and relevant artifact sections below;
keep the work proportionate to the actual uncertainty and change boundary.

## Establish the starting point

Read applicable project instructions and the supplied description or code first.
Identify the artifact, its concept and behavior, reader context, domain words,
relevant contracts, existing authorization, and material unknowns. Follow
[read-first discovery](references/elicitation.md#begin-with-the-supplied-input).

During code authoring, inspect neighboring declarations and representative uses
before introducing names. For direct assistance, use the supplied code or
description to choose a route. A description supports a provisional recommendation
with explicit implementation and caller checks still needed.

| Starting task | Read first | Continue when |
| --- | --- | --- |
| Clarify an uncertain or abstract concept | [Sparse input](references/elicitation.md#work-with-sparse-or-abstract-input), [intent and observation](references/elicitation.md#keep-intent-and-observation-distinct), then [scenario questions](references/elicitation.md#ask-questions-that-separate-plausible-meanings) | The material distinction is settled; continue to selection. Keep unanswered intent visible and make conditional progress. |
| Generate or choose names for a settled concept | [Meaning-preserving generation](references/candidate-generation.md#preserve-meaning-while-varying-expression), then [hard constraints](references/selection.md#apply-hard-constraints-first) | A viable choice or comparison is ready; perform contextual validation. |
| Validate a proposed or existing name | [Review scope](references/contextual-validation.md#establish-the-review-scope), then [contexts that establish meaning](references/contextual-validation.md#inspect-the-contexts-that-establish-meaning) | Evidence supports retaining, rejecting, or revisiting the name; report the finding and recheck any revision. |
| Apply an authorized rename | [Change boundary](references/renaming.md#establish-the-change-boundary), then [bindings and representations](references/renaming.md#trace-bindings-and-representations) | The mapping and compatibility policy are established; edit and verify within the authorized scope. |

## Resolve meaning and vocabulary

For sparse input, follow [competing concepts](references/foundations.md#separate-competing-concepts-before-comparing-words)
to expose the distinction that needs evidence. Ask the next scenario question
that changes the represented concept. Use
[conditional candidates](references/candidate-generation.md#condition-candidates-on-unresolved-meaning)
when an answer remains unavailable; keep their assumptions and status explicit.

When neighboring concepts or responsibilities are unclear, read
[definitions and distinctions](references/foundations.md#define-the-concept-with-the-distinctions-readers-need).
Establish the actual truth conditions, state, quantity, cardinality, effects,
and completion boundary relevant to the artifact.

For unfamiliar domain language, read
[vocabulary evidence](references/domain-vocabulary.md#build-a-small-evidence-trail)
and [boundary distinctions](references/domain-vocabulary.md#preserve-near-neighbors-and-boundaries).
Consult the project glossary and an authoritative source governing the concept.
Resolve observable facts from available evidence; ask a focused scenario question
when intent or core meaning remains material. Record unavailable sources and
their affected uncertainty while continuing supported work.

Use full words with established domain abbreviations in appropriate local scope,
following [abbreviation guidance](references/domain-vocabulary.md#use-accepted-abbreviations-in-their-context).
If naming exposes a possible redesign, keep that proposal distinct from the
established behavior and authorized edit. Follow
[design questions](references/foundations.md#recognize-a-design-question).

Capture a [naming brief](templates/naming-brief.md) when several facts or unknowns
need tracking. A small task can retain the same core evidence in concise prose.

## Select artifact and ecosystem guidance

Read the rows relevant to the target; their sections own the detailed criteria.

| Target | Selected explanation |
| --- | --- |
| Variable, parameter, or field | [Available context](references/variables-and-state.md#fit-the-available-context); for a group, [related variables across component and parent](references/variables-and-state.md#review-related-variables-as-a-family); select [cardinality](references/variables-and-state.md#cardinality-optional-values-and-keys), [units and time](references/variables-and-state.md#units-instants-dates-and-durations), or [boolean polarity](references/variables-and-state.md#boolean-meaning-and-polarity) as needed |
| Function or method | [Operation contract](references/functions-and-methods.md#start-with-the-operations-contract), [complete calls](references/functions-and-methods.md#parameters-cardinality-and-complete-calls), and relevant [completion boundaries](references/functions-and-methods.md#async-work-and-completion-boundaries) |
| Type, role, error, command, or event | [Entity, value, and role](references/types-and-messages.md#entity-value-and-role), [errors](references/types-and-messages.md#errors-and-outcomes), or [message lifecycle](references/types-and-messages.md#commands-events-and-lifecycle) |
| Module, package, namespace, or file | [Capability boundary](references/modules-packages-and-files.md#start-with-the-boundary), [complete import](references/modules-packages-and-files.md#read-the-complete-import), and [collisions](references/modules-packages-and-files.md#check-collisions-at-each-resolution-boundary) |
| API, schema, database, or configuration name | [Operation paradigm](references/apis-schemas-and-configuration.md#match-operation-names-to-the-api-paradigm), [serialized meaning](references/apis-schemas-and-configuration.md#preserve-serialized-meaning), [database questions](references/apis-schemas-and-configuration.md#make-database-and-analytics-names-answer-a-specific-question), or [configuration scope/default](references/apis-schemas-and-configuration.md#give-configuration-an-explicit-scope-and-default) |
| Persistent identifier, label, or alias | [Identity and resolution](references/apis-schemas-and-configuration.md#separate-persistent-identity-labels-and-aliases) |

Read [project convention discovery](references/language-conventions.md#establish-the-projects-convention),
then only the applicable section:
[C++](references/language-conventions.md#c-distinguish-the-language-from-an-adopted-style-guide),
[Python](references/language-conventions.md#python-use-pep-8-with-project-and-protocol-context),
[Rust](references/language-conventions.md#rust-name-ownership-and-method-category-accurately),
[Swift](references/language-conventions.md#swift-judge-the-full-call-and-its-argument-labels), or
[JavaScript/TypeScript](references/language-conventions.md#javascript-and-typescript-identify-the-organization-and-framework).
For another ecosystem, follow
[additional-language review](references/language-conventions.md#additional-languages-and-final-review).
Keep concept fidelity and ecosystem spelling as separate decisions.

## Choose and review the name

Read [comparison criteria](references/selection.md#define-the-comparison-before-choosing)
when several viable options have meaningful tradeoffs. Define criteria and
disqualifying constraints, show equivalent use sites, score against the actual
evidence, and present the matrix with a reasoned recommendation. Use the
[comparison template](templates/candidate-comparison.md) when a record helps.
For a portable HTML artifact, follow
[matrix preparation](references/selection.md#present-a-portable-matrix), which
selects the sibling decision-matrix instructions and actual assets.

When one choice clearly fits, follow
[the clear-winner path](references/selection.md#record-a-clear-winner-directly).
State the decisive evidence directly. An adequate existing name can be retained.

After selection, perform a distinct
[contextual review](references/contextual-validation.md#inspect-the-contexts-that-establish-meaning).
Inspect the declaration, implementation, representative callers, related names,
glossary, prose, examples, tests, and applicable public representations. Assess
the selected name against that evidence independently of the initial preference.

If context rejects the wording, return to selection; if it exposes unsettled
meaning, return to elicitation. Follow
[retain, reject, or revisit](references/contextual-validation.md#retain-reject-or-revisit),
then recheck the changed choice and affected findings. The
[validation report](templates/validation-report.md) records inspected evidence,
findings, corrections, and remaining uncertainty.

## Apply and verify the authorized change

Carry existing task and session authorization into the established rename scope.
A request to apply a scoped rename authorizes its reversible edits and checks.
Use the [rename plan](templates/rename-plan.md) when the mapping or compatibility
boundary needs a record. Read
[predicate and effect preservation](references/renaming.md#preserve-predicates-and-effects)
and [compatibility choices](references/renaming.md#choose-compatibility-deliberately)
for the affected contracts.

Map declaration identities, bound references, imports, keyword calls, dynamic
uses, documentation, tests, and external representations as applicable. Prefer
language-aware edits where available, supplemented by scoped searches. Preserve
unrelated same-spelling symbols and the selected behavior/wire policy. If the
inventory exposes a material additional contract decision, prepare that concrete
choice and continue independent authorized work.

Follow [edited-result verification](references/renaming.md#verify-the-edited-result):
inspect the diff, recheck affected uses, and execute appropriate behavior and
compatibility checks. Use independent contract evidence when edited tests could
repeat the same mistake. Record actual commands, scope, outcomes, and recovery
under [evidence and recovery](references/renaming.md#record-evidence-and-recovery).

## Deliver the result

Give the selected or retained name in a representative expression, the decisive
rationale and relevant tradeoff, and a separate verification outcome. Distinguish
description-level assessment, static source review, executed checks, and remaining
uncertainty using [precise evidence reporting](references/contextual-validation.md#report-evidence-and-limits-precisely).
For applied edits, include the actual mapping and behavior/compatibility results.
A [decision record](templates/naming-decision.md) can link substantial supporting
artifacts; small tasks can use a concise answer with equivalent evidence.

For a worked application, select the matching [example](examples/README.md).
For a research-dependent claim, consult the
[study synthesis](references/empirical-research.md), [evidence register](references/evidence.md),
and [inspected sources](references/sources.md). Package maintainers use
[maintenance](references/maintenance.md), [tests](tests/README.md), and
[evaluation](evals/README.md) for changes to this skill and its acceptance evidence.
