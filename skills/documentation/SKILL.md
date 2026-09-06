---
name: documentation
description: Create, update, review, and check drift in a document or related group, including tutorials, how-to guides, reference, explanations, READMEs, runbooks, ADRs, articles, release notes, changelogs, and Doxygen source comments. Use for evidence-based documentation authoring and verification in an existing MkDocs, Doxygen, or CI environment.
---

# Documentation

Produce a document or related group from verified evidence. Deliver the changes,
traceable review findings and repeatable validation results. Use the consuming
project's existing documentation environment and conventions.

## Establish scope and select a route

Read the selected document, applicable project instructions, its parent
navigation and the user's request. Explicit user instructions determine scope
and authorization. Infer known answers from the project before asking for gaps.
Read [the document contract](references/document-contract.md#establish-the-task)
and complete [a contract](templates/document-contract.md), proportionate to the
change. Resolve missing facts that determine audience, target behavior, structure
or safe execution; record other uncertainty in the draft and evidence register.

| Request | Read next | Concrete output |
| --- | --- | --- |
| Create a page or multipart group | [Document types](references/document-types.md#route-by-reader-need), then [structure](references/structure.md#decide-page-boundaries) | Selected type's outline, document(s), examples and necessary navigation |
| Update a page | [Evidence](references/evidence.md#resolve-conflicts-by-version-and-claim-kind), then the selected type's reference/template | Focused changes with preserved claim provenance |
| Review existing documentation | [Editorial review](references/editorial-review.md), then [contextual review](references/contextual-review.md) | Located findings, evidence and proposed corrections; apply authorized fixes |
| Analyze drift | [Drift analysis](references/drift-analysis.md) | Exact affected claims, current evidence, impact and corrections |
| Write/review source comments | [Doxygen adoption](references/doxygen.md), then [linter](references/doxygen-linter.md) | Supported-language comment changes and structural/prose validation |
| Write code/docs changelogs or release notes | [Changelog workflow](references/changelog-workflow.md), then the selected template | Distinct verified outputs for the requested revision range |

Load only the selected route's resources. Consult the upstream sections linked by
that reference when needed; record unavailable sources and the affected
judgment. The [source register](references/sources.md) identifies adoption and
reuse decisions. Human references hold substantive guidance; this entry point
adds route selection, ordering and transition checks.

## Gather evidence and outline

Use [claim traceability](references/evidence.md#choose-evidence-for-the-claim) and
[the register](templates/evidence-register.md) to distinguish observed behavior,
intended contracts, historical rationale and inference. Check target revisions,
resolve conflicting sources and record inaccessible evidence. A passing test
supports its exercised behavior; examine its scope before extending a claim.

For authoring, create [an outline](templates/outline.md) from the contract and
load the chosen type's upstream guidance, local template and example. Make
sections conditional on reader need. Keep multipart pages ordered by their
starting states and outcomes. Record the contract, evidence, outline, pending
questions and last completed stage in the project's designated task workspace
or scratch space. On resumption inspect current files and rerun affected checks.
Keep published references linked to durable sources.

## Draft and review

Write from supported claims, labeling unresolved assumptions. Apply
[house style](references/house-style.md) and the relevant Google guidance linked
there. Preserve exact commands and required values where the reader needs them.
Use the project's domain vocabulary; consult its glossary, domain sources or
available glossary skill for unresolved terms. Use available writing, diagram
and language skills when their guidance helps the actual edit.

Treat examples as artifacts using [example verification](references/examples.md).
Check their meaning after changes to quoting, flags, indentation and identifiers.
For source comments, follow the upstream Doxygen guide through the adoption
reference; verify meaningful preconditions, lifetime, ownership, errors and
concurrency against evidence.

Perform the [editorial pass](references/editorial-review.md), followed by the
[context pass](references/contextual-review.md). Inspect relevant parent,
sibling, child and reference pages. Make evidence-backed related edits within
the authorized scope; record larger follow-up work with its reader impact.

## Validate the change

Read [validation](references/validation.md) to choose checks and record their
commands, versions, scope and diagnostics. Inspect the project's actual build
configuration before assuming syntax, anchors or warnings are covered. Try the
documented project setup and invocation before classifying a tool as unavailable;
record the actual setup or execution failure when it prevents the check.

- For prose and source comments, use [Vale](references/vale.md).
- For source-comment structure, use [the Doxygen linter](references/doxygen-linter.md).
  For rendering, symbols or cross-references, use
  [generated-reference validation](references/generated-reference-validation.md).
- For pages in an existing site, use [MkDocs authoring](references/mkdocs-authoring.md).
- For local, external and rendered links, use [link validation](references/link-validation.md).
- Run the applicable [example checks](references/examples.md) before relying on
  their documented results.

Run checks in dependency order so generated references exist before site and
built-link checks. Preserve relevant project settings when using supplied
assets or temporary output. Report each check as pass, fail, skipped or blocked;
include the reason and affected scope for unavailable tools or evidence. Repeat
checks affected by later edits. Use the project's existing CI verification jobs
for integration of these commands.

## Final verification and delivery

Run [final verification](references/final-verification.md) as a skeptical
developer and technical editor. Its output contains only the eight specified
finding categories, with `[]` as the clean result. Keep tool reports and delivery
summaries in separate records.

Record human review for factual claims, security guidance, migrations,
destructive operations, compatibility and release-sensitive information using
[the human-review record](templates/human-review.md). Identify the reviewer,
evidence, unresolved findings and status; automation cannot supply human approval.
Existing authorization controls execution, and human review status controls the
claim of readiness.

Deliver the changed documents or findings, the validation report, supporting
review records and pending human review. State what was verified and what remains
unresolved. Consult [maintenance](references/maintenance.md) when updating this
skill's sources, routing, tools or fixtures.
