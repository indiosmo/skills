# Maintain the naming guide and skill

Begin a change at the reference that owns its reasoning, then inspect the
templates, examples, routing, and checks that depend on it. Preserve the guide's
independent reading path and the entry point's selective loading. This page
adapts the repository's [documentation maintenance workflow](../../documentation/references/maintenance.md)
to software naming.

## Refresh sources and claims together

Use the [source register](sources.md) to locate the author, version, inspected
section, access date, adoption decision, and reuse conditions. Reopen the primary
source before changing a source-dependent recommendation. Record what was
actually accessible; a preview or abstract supports the inspected content.

Update the corresponding [evidence record](evidence.md), its owning explanation,
and any example relying on that claim. Preserve stable source and claim anchors
or update their incoming links in the same change. If sources disagree, retain
their populations, tasks, definitions, and conditions before drawing a conclusion.
Keep empirical results, formal models, ecosystem conventions, and local policy
distinct. [Empirical research](empirical-research.md) owns the readable study
synthesis, including abbreviation and recall limitations.

For domain terminology, verify the actual protocol or vocabulary version and
its applicability to the represented concept. Recheck local definitions,
neighboring terms, and boundary mappings. A source refresh may change the naming
rationale without changing a fixture's deliberately stipulated software contract.
Record that distinction through [domain vocabulary](domain-vocabulary.md).

Maintain attribution beside the adopted source and preserve applicable notices
when copying licensed material. Check exact quotations and copied examples
against their recorded reuse conditions. Original scenario behavior should
remain identifiable as scenario evidence.

## Follow the owning explanation

| Change | Owning reference | Dependent resources to review |
| --- | --- | --- |
| Concept, identity, role, definition, or domain boundary | [Foundations](foundations.md), [domain vocabulary](domain-vocabulary.md) | Brief, domain examples, glossary contributions, and related claim records |
| Discovery or question strategy | [Elicitation](elicitation.md) | Brief fields, scripted dialogue, uncertain-concept evaluation, and route transitions |
| Candidate generation or decision criteria | [Candidate generation](candidate-generation.md), [selection](selection.md) | Comparison and decision templates, HTML matrix, clear-winner behavior, and tradeoff cases |
| Value, operation, type, module, or external-contract advice | The matching [artifact reference](README.md#select-the-artifact-guidance-you-need) | Use-site examples, language sections, affected fixture contracts, and expanded evaluation cases |
| Contextual review or confidence | [Contextual validation](contextual-validation.md) | Validation report, rejection/retention examples, and evidence expectations |
| Binding edits, compatibility, or recovery | [Renaming](renaming.md) | Rename plan, public/internal examples, fixtures, trusted checker, and mutation tests |

Read revised prose as a first-time reader. It should describe the concept,
conditions, rationale, and relevant evidence clearly. Source and claim registers
support deeper inspection. Keep long references navigable with a contents list;
split a reference when each resulting page has a distinct reader purpose.

## Recheck language and tool changes

When an official language guide changes, inspect its precise revised section
and the affected [language guidance](language-conventions.md). Distinguish the
language, an organization's adopted style, project overrides, and public protocol
spellings. Verify runnable syntax with the supported environment; label
illustrative sketches and their remaining checks explicitly.

Use the existing native tools documented in [tests](../tests/README.md). Changes
to Markdown parsing, metadata validation, or lychee need valid and broken input
checks, including missing resources, fragments, empty selection, and relative
fixture paths. Inspect native diagnostics and actual checked coverage. Review
Vale findings in context, preserving verified source names, code identifiers,
and domain vocabulary. An unavailable online source or renderer leaves its
specific check pending while supported independent checks continue.

The trusted [rename checker](../evals/check_rename_outcomes.py) has a bounded
fixture contract. A changed fixture requires reviewing its declaration mapping,
allowed edits, immutable files, executable assertions, and documentation uses.
Recheck both valid target spellings and failure cases: missed bindings, changed
polarity or boundaries, weakened assertions, unrelated edits, altered wire keys,
defaults, invalid values, missing output, runtime failures, and unavailable checks.
Trusted expectations remain outside the checkout an execution agent can edit.

Run fixture exercises in disposable copies and verify packaged input preservation.
Keep the fixture README, executable contract, worked example, reviewer notes,
checker, and tests in agreement. A deliberately changed behavior contract needs
new independently justified expectations and a clearly identified input revision.

## Refresh evaluations from observed problems

Follow the [evaluation protocol](../evals/README.md) for native source/run schemas,
packet separation, paired configurations, grading, benchmark aggregation, and
the existing viewer. Review concrete pilot prompts with the user before running
them. Preserve simulated clarification replies before observing executor output.

After actual output feedback, revise the owning explanation first and update its
dependents. Look for general failure mechanisms, excessive work, weak assertions,
and evidence contamination. Expand across the declared scenario and artifact
coverage, rerun both configurations on the same inputs, and present the results
with previous-iteration context. Record actual human judgments separately from
deterministic passes and retain unavailable metric status.

Add a runtime helper when repeated observed work demonstrates a gap in the native
tools or existing package. Compare viable approaches, declare the new files and
input/output contract, and test meaningful failure paths. Description optimization
uses the reviewed trigger set and the sibling creating-skills tools when that
optional work is selected and its execution environment is available.

## Check installation and release evidence

The supported installation is a repository skill tree containing naming and the
documented siblings: documentation, design, decision-matrix, glossary,
creating-skills, and verification-before-completion. These supply selected
guidance, matrix assets, validation tools, and development evaluation consumers.
Their adoption boundaries are recorded in the [source register](sources.md#adopted-local-resources).
Naming's brief and clear-winner policy govern proportionate naming tasks.

Exercise a relocated copy of that tree with the existing development environment.
Resolve the entry-point routes, human navigation, templates, examples, and selected
sibling resources there. Run package/fixture/checker checks against the relocated
package. Inspect any transitive sibling links actually loaded by those routes.
A standalone naming archive needs those referenced resources supplied alongside
it; validate its contents and dependency layout before describing it as installable.
The sibling creating-skills packager archives one skill directory and excludes
its root evaluation directory. Distribution of this documented development tree
requires preserving the evaluation resources and sibling layout as well as the
ordinary guide. Review the actual archive inventory against that intended scope.

Run the assembly checks after guide and entry-point integration. Run the full
release suite against the agreed delivery scope, recording completed evaluation
and any evaluation explicitly deferred to field use. The
durable result summary should identify the evaluated revision, input provenance,
objective results, human review, changes, and bounded limitations. Evidence from
source review, execution, installation, and user judgment supports separate
claims; audit the task's required outcomes before reporting completion.
