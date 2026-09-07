# Elicit the concept and constraints

Before choosing a name, establish enough meaning to distinguish good candidates
from misleading ones. Read the available evidence, ask about material intent,
and capture a brief proportional to the uncertainty. A well-specified local
choice can proceed in a sentence; an ambiguous public operation needs more
context.

This procedure adapts the design skill's
[read-first scenario interview](../../design/SKILL.md#the-interview-resolves-what-discovery-surfaces).
Its naming-specific scope and stopping conditions are local policy
([LOCAL-003](evidence.md#local-003), [adoption](sources.md#local-design)).

## Begin with the supplied input

Each input form offers different evidence. Use what is available before asking
the person to reconstruct it for you.

| Input | Read first | Resolve what remains material |
| --- | --- | --- |
| Idea | The proposed purpose, examples, intended users, and existing conversation constraints | What concrete thing or operation does the proposal describe, and what distinguishes it from neighboring concepts? |
| Description | Stated behavior, outcomes, exclusions, lifecycle, and domain terms | Which statements are requirements, examples, or assumptions; which outcomes change the name? |
| Code excerpt | Declaration, types, branches, values, and visible calls | Which omitted caller, contract, or intent determines meaning? Request targeted context when needed |
| Existing name with surrounding code | Binding, implementation, representative callers, tests, documentation, glossary, and related names | Is the name accurate, and would a change improve a material use site? |

Repository access allows targeted investigation of missing context. Start from
supplied paths and project navigation, then inspect relevant callers and
contracts. If implementation is unavailable, reason from the supplied
description and identify the checks that still need code. A recommendation can
be useful with that coverage limit ([LOCAL-005](evidence.md#local-005)).

## Keep intent and observation distinct

Describe what the artifact currently does and what it is intended to represent.
Use concrete outcomes: inputs, returned values, effects, failure behavior, and
state transitions. For a value, establish units, cardinality, and the condition
under which it exists. Establish an entity's lifecycle and identity. Consult
[foundations](foundations.md) and [domain vocabulary](domain-vocabulary.md) when
these distinctions remain unclear.

Suppose a function called `validate_import` parses rows and commits accepted
records. A caller may rely on those commits even if a description calls the
operation validation. Record the observed effect and ask whether the target is
the existing importing operation or a separately proposed validation-only
operation. The naming recommendation should follow the resolved contract.
Changes to effects or truth conditions require their own scope
([COMP-015](evidence.md#comp-015)).

## Ask questions that separate plausible meanings

A useful question has an answer that changes the definition, candidate set, or
validation plan. Ask one material question at a time when answers depend on one
another. Offer a tentative interpretation and its evidence when that helps the
person respond. Established answers and authorization carry forward.

Use a concrete case that forces a distinction. Instead of asking whether a name
should be "clearer," ask what the operation means when parsing succeeds but a
record fails validation. Instead of asking whether a flag is "positive," ask
whether its truth means configuration permits an action or current conditions
make the action possible. Inspect code for those facts first.

The following is an original, scripted interview example. Its replies establish
the hypothetical scenario; they are not evidence about a real user's system.

> Engineer: I need a name for a boolean that says whether an import worked.
>
> Reviewer: Your description says rows are parsed before validation and commit.
> If every row parses but the transaction fails to commit, should this value be
> true? I would use the commit outcome if this is the completion signal.
>
> Engineer: False. It becomes true only after the transaction commits. A separate
> report contains the rejected rows; the transaction can commit accepted rows.
>
> Reviewer: Then the concept is completion of the commit, even with rejected
> rows. I recommend `import_committed`, shown at the notification call below.
> Implementation and caller checks are pending because this input is a description.

```python
if import_committed:
    send_import_summary(import_report)
```

The answer rules out names that promise every row was accepted. The recommended
name states the supplied outcome without inventing a stronger success condition.
Before applying it, inspect where the boolean is assigned and how each caller
uses it. The interview technique is local judgment; the need for bounded
definitions is supported by [CON-001](evidence.md#con-001) and
[CON-006](evidence.md#con-006).

## Work with sparse or abstract input

When the input is an idea such as "a class that groups related imports," first
separate the plausible meanings. The group might be a temporary selection for
one operation, a saved collection with its own identity, or the imports
participating in one execution. These are hypotheses about responsibilities,
not established facts or interchangeable names. Use only hypotheses that the
supplied description makes plausible, and explain the clue behind each.

Read any available creation sites, operations, examples, and related concepts
to narrow those interpretations. Then choose the one scenario whose answer
would most change the concept. For the hypothetical import group: "After an
import finishes, does this group still exist as something users can retrieve
and edit?" That answer separates a lasting collection from a temporary grouping;
it may leave the execution relationship to resolve next. Ask the next question
only if the remaining distinction changes the naming decision.

For an unclear class or group, request one representative use: who creates it,
what someone does with it, and what happens to it afterward. Focus the request
on the missing relationship or lifetime. For example, whether one import can
belong to several groups may clarify membership; whether the group controls
execution may clarify responsibility. Select the example that tests the live
hypotheses, keeping the effort proportional to this choice.

If intent remains unresolved, make the useful progress explicit: "If this is a
saved collection with editable membership, `ImportCollection` is a candidate;
if it represents one execution and its outcome, `ImportRun` is a candidate.
Which meaning applies remains open." Show the condition that supports each name
and the evidence needed to choose. Record the decision as unresolved; reserve a
final recommendation and dependent edits for the supported interpretation.
This procedure is local engineering guidance under
[LOCAL-003](evidence.md#local-003) and [LOCAL-004](evidence.md#local-004).

## Capture the naming brief

The brief holds the evidence needed by candidate generation, selection, and
contextual validation. Combine fields in short prose for a small choice; expand
them when uncertainty or contract scope requires it. These fields specialize
the shared concept/behavior, evidence, constraints, unknowns, recommendation,
rationale, and distinct verification contract.

| Field | What to record |
| --- | --- |
| Concept and behavior | Definition, purpose, observed behavior versus intended contract, outcomes, units/cardinality, lifecycle, and relevant identity |
| Vocabulary | Domain and model boundary, glossary terms, accepted abbreviations, near-neighbors, and source-backed definitions |
| Context | Artifact kind, audience, scope, types, representative declarations/callers or prose, and related names |
| Evidence | Inspected files, tests, documents, domain sources with versions, and supplied statements; distinguish observations from assumptions |
| Constraints | Hard contractual or project requirements, preferences, public/persisted spellings, compatibility, and authorized change scope |
| Unknowns | Material questions, assumptions with their consequences, and the evidence or person that can resolve them |
| Recommendation and rationale | Selected or retained name in context, decision status, reasons, and remaining assumptions; fill after selection |
| Verification | Distinct contextual review result, evidence and coverage limits; applied changes also record affected-use and behavior checks |

A brief can start with the first six rows and acquire the decision and review as
work proceeds. For example: "Name the local count of rows committed by this
transaction. The implementation increments it after each accepted row; the
transaction result supplies the final committed count. Prefer `committed_row_count`
under the project's full-word convention. Check the summary caller against that
meaning." The final sentence defines pending work until the actual review occurs.

## Decide when enough is known

Proceed when the concept has a supported meaning, material boundaries are clear,
the artifact and reader context are known, and hard constraints can be applied.
A clear local choice needs no ceremonial interview or invented alternatives.
Use [candidate generation](candidate-generation.md) and
[selection](selection.md) for the next decision.

If an unresolved question would change the concept, truth condition, effect, or
public contract, obtain that answer before dependent edits. Continue independent
evidence gathering while it is unresolved. Mixed responsibilities can justify a
design question; preserve naming scope while recording a proposed redesign.

A provisional recommendation is appropriate when the stated assumption supports
a useful choice and the limitation is explicit. State the assumption, show the
name in a representative use, explain what answer would change it, and identify
the pending verification. An unresolved core domain term calls for a source or
focused expert question ([LOCAL-001](evidence.md#local-001)).

Selection produces a recommendation or accepted decision; actual acceptance
comes from the person or authority making it. The distinct
[contextual validation](contextual-validation.md) then checks the name against
behavior, callers, neighboring concepts, and contracts. Its findings can reopen
the brief. [Renaming](renaming.md) adds the checks needed for authorized changes.
