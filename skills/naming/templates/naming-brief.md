# Naming brief

Owner: [elicitation](../references/elicitation.md#capture-the-naming-brief).
Use the core rows below, combining them in compact prose for a small task.
Replace brace-delimited prompts with evidence or an explicit pending status.
Add the conditional details only where they affect the choice.

## Core record

| Field | Record |
| --- | --- |
| Concept and behavior | {Define the thing or operation. Separate observed behavior from intended contract; state the outcomes that distinguish it.} |
| Vocabulary | {Domain and model boundary; established terms, neighboring concepts, and vocabulary sources.} |
| Context | {Artifact kind, audience, scope, language, declaration or description, and representative use.} |
| Evidence | {Inspected paths/symbols, documents/sections and versions, or supplied statements; identify which support each claim.} |
| Constraints | {Required meaning, conventions, compatibility boundaries, preferences, and the change scope already authorized by the request.} |
| Unknowns | {Plausible competing meanings, the next concrete question that separates them, and how each answer changes the name. Record evidence or a person that can resolve it; state when none remain within the examined scope.} |
| Recommendation and rationale | {After selection: selected or retained spelling in context, reasons, assumptions, and proposed/accepted/unresolved status with its basis; link the decision when separate.} |
| Verification | {After contextual review: outcome, examined evidence and limits; link the report when separate. Record pending review explicitly. For edits, add the actual affected-use and behavior results.} |

## Conditional details

| Include when relevant | Record |
| --- | --- |
| Values or predicates | {Types, units, cardinality, defaults, and truth conditions with boundary examples.} |
| Operations or messages | {Inputs, results, mutations, failures, lifecycle transitions, and identity.} |
| Vocabulary uncertainty | {Candidate definitions, accepted local abbreviations, conflicting usage, and the source or expert needed.} |
| Public or persisted names | {Exact external spellings, consumers, support policy, and authorization evidence for any proposed compatibility change.} |
| Conflicting intent and implementation | {Both claims and their evidence; the scope decision required before dependent edits.} |
| Abstract class or component | {What one instance might represent, its relationship to its owner, and one lifecycle or caller scenario that distinguishes the plausible roles. Mark proposed interpretations explicitly.} |
| Related variables | {Each value's role, shared invariants or derived expressions, and how the family reads inside the component and through its parent at an external use site.} |

Continue with [candidate generation](../references/candidate-generation.md),
[comparison](candidate-comparison.md), or direct
[validation](validation-report.md). Record the chosen outcome in a
[decision](naming-decision.md); use a [rename plan](rename-plan.md) for edits
whose scope needs a separate record.
