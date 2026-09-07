# A guide to naming software

Choose a name by establishing the concept, reading its uses, and checking whether
the words preserve its meaning. This guide supports both naming during code
authoring and direct assistance with a proposed or existing name. It develops
the reasoning through explanations, source evidence, and original examples.

A useful result contains a recommendation or retained name in context, its
rationale, and a distinct verification result. A small established choice can
fit in a few sentences. Material uncertainty calls for a focused question;
genuine tradeoffs call for a comparison; an applied rename adds evidence about
changed bindings and preserved behavior.

## Start with your task

| Your starting point | Reading path | Example and record |
| --- | --- | --- |
| An abstract idea or description with little context | Begin with [sparse input](elicitation.md#work-with-sparse-or-abstract-input), distinguish [competing concepts](foundations.md#separate-competing-concepts-before-comparing-words), then ask a [scenario question](elicitation.md#ask-questions-that-separate-plausible-meanings). Keep [conditional names](candidate-generation.md#condition-candidates-on-unresolved-meaning) explicit while meaning remains unresolved. | [Abstract class](../examples/unclear-abstraction.md), [saved-search dialogue](../examples/eliciting-a-concept.md); [naming brief](../templates/naming-brief.md) |
| A settled concept needing a name | [Generate meaning-preserving candidates](candidate-generation.md#preserve-meaning-while-varying-expression), then [apply hard constraints](selection.md#apply-hard-constraints-first). Compare viable alternatives or [record a clear winner](selection.md#record-a-clear-winner-directly). | [Candidate comparison](../examples/comparing-candidates.md); [comparison template](../templates/candidate-comparison.md) and [decision record](../templates/naming-decision.md) |
| A proposed or existing name to assess | Establish [review scope](contextual-validation.md#establish-the-review-scope), inspect its meaning in use, and [retain, reject, or revisit](contextual-validation.md#retain-reject-or-revisit). | [Contextual rejection](../examples/rejecting-a-plausible-name.md) and [retention](../examples/retaining-an-existing-name.md); [validation report](../templates/validation-report.md) |
| An authorized rename to apply | Establish the [change boundary](renaming.md#establish-the-change-boundary), map bindings and representations, then [verify the edited result](renaming.md#verify-the-edited-result). Carry existing authorization into that scope. | [Boolean rename](../examples/boolean-polarity.md) and [stable JSON contract](../examples/public-contract-rename.md); [rename plan](../templates/rename-plan.md) |

After selection, review the name against implementation, representative callers,
related vocabulary, and the relevant contracts. This separate review can reject
an attractive candidate. Return to discovery when the concept is unclear, or to
selection when the concept is sound but the wording misleads. Recheck the revised
choice and affected findings.

For description-only assistance, establish what the supplied scenarios support
and identify the implementation or consumer evidence still needed. For code
authoring, inspect the surrounding project first and apply the same reasoning to
the declaration and its actual use sites. Scope the work to the task's unresolved
questions and authorized changes.

## Read the foundations in order

1. [Foundations](foundations.md) separates meaning, identity, role, wording, and
   context. It explains why a naming question can expose a design question.
2. [Domain vocabulary](domain-vocabulary.md) establishes practitioner terms,
   neighboring concepts, glossary evidence, and bounded contexts.
3. [Elicitation](elicitation.md) turns supplied evidence and scenario answers
   into a proportionate naming brief.
4. [Candidate generation](candidate-generation.md) develops useful alternatives
   in declarations, calls, and prose. [Selection](selection.md) explains hard
   constraints, criteria, grounded scores, and clear-winner decisions.
5. [Contextual validation](contextual-validation.md) assesses the chosen or
   existing name independently. [Renaming](renaming.md) adds binding, behavior,
   compatibility, and recovery checks for an applied change.

[Empirical research](empirical-research.md) explains what comprehension and
memory studies support, including their differing abbreviation results and
limited transfer. Read it when evaluating a research claim or the rationale for
the guide's conventions. The [evidence register](evidence.md) distinguishes
study results, models, practitioner conventions, and local engineering policy.
The [source register](sources.md) supplies exact adopted sections, access limits,
and attribution.

## Select the artifact guidance you need

| Artifact or distinction | Governing explanation | Worked application |
| --- | --- | --- |
| Variables, parameters, fields, state, time, units, and collections | [Variables and state](variables-and-state.md) | [Audio quantities](../examples/units-and-cardinality.md), [logistics mapping](../examples/bounded-contexts.md) |
| Functions, methods, predicates, return values, effects, and completion | [Functions and methods](functions-and-methods.md) | [Import effects](../examples/functions-and-side-effects.md), [boolean polarity](../examples/boolean-polarity.md) |
| Entities, values, roles, errors, commands, and events | [Types and messages](types-and-messages.md) | [Clinical software roles and messages](../examples/types-roles-and-events.md) |
| Namespaces, modules, packages, paths, imports, and collisions | [Modules, packages, and files](modules-packages-and-files.md) | [Executed import example](../examples/modules-packages-and-files.md) |
| Public operations, serialized fields, database names, configuration, and persistent identity | [APIs, schemas, and configuration](apis-schemas-and-configuration.md) | [Internal field and public key](../examples/public-contract-rename.md) |
| Ecosystem casing, abbreviations, predicates, and conversion grammar | [Language conventions](language-conventions.md) | Select C++, Python, Rust, Swift, or JavaScript/TypeScript after checking project conventions |
| Unfamiliar domain words or conflicting definitions | [Domain vocabulary](domain-vocabulary.md) | [Trading roles](../examples/domain-vocabulary.md), [logistics boundaries](../examples/bounded-contexts.md) |
| Unresolved responsibilities or completion boundaries | [Foundations](foundations.md#recognize-a-design-question) and [elicitation](elicitation.md#keep-intent-and-observation-distinct) | [Unclear abstraction](../examples/unclear-abstraction.md) |

The [example index](../examples/README.md) maps the complete collection to routes,
artifacts, domains, and available checks. Its dialogues and domain scenarios
are explicitly illustrative; runnable fixtures have separate execution evidence.

## Use records proportionately

Use the [brief](../templates/naming-brief.md) to retain meaning, vocabulary,
evidence, constraints, and unknowns. The
[comparison](../templates/candidate-comparison.md) captures genuine tradeoffs,
and the [decision](../templates/naming-decision.md) records the recommendation
or retained name and rationale. The
[validation report](../templates/validation-report.md) separates name assessment
from applied-change checks. The [rename plan](../templates/rename-plan.md)
captures the binding map and compatibility policy when those need a durable record.

Compact prose can carry the same core evidence for a small task. A useful
comparison uses the [portable matrix procedure](selection.md#present-a-portable-matrix)
and the [completed artifact](../examples/candidate-matrix.html). Template fields
help record decisions; the governing explanations establish how to make them.

## Maintain and verify the guide

[Maintenance](maintenance.md) maps source, guidance, fixture, and tool changes to
their dependent resources and checks. [Test documentation](../tests/README.md)
provides the repository commands and supported installation dependencies.
[Evaluation](../evals/README.md) explains paired execution, trusted rename checks,
and actual human review. These provide different evidence: mechanical checks
establish their tested contracts, while naming quality and source fidelity need
contextual review.
