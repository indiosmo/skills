# Selecting a document type

Choose a structure from the reader's task before choosing a template. The
[Diataxis compass](https://diataxis.fr/compass/) separates action from
understanding and learning from applying existing skill.

## Route by reader need

| Reader need | Type and upstream guidance | Local template |
| --- | --- | --- |
| Learn by completing a prepared activity | [Tutorial](https://diataxis.fr/tutorials/) | [Tutorial](../templates/tutorial.md) |
| Accomplish a task using existing skills | [How-to](https://diataxis.fr/how-to-guides/) | [How-to](../templates/how-to.md) |
| Look up product facts during work | [Reference](https://diataxis.fr/reference/) | [Reference](../templates/reference.md) |
| Understand concepts and relationships | [Explanation](https://diataxis.fr/explanation/) | [Explanation](../templates/explanation.md) |
| Orient in a repository, module or component | [README guidance](readme.md) | [README](../templates/readme.md) |
| Execute an operational response | [Runbook guidance](runbooks.md) | [Runbook](../templates/runbook.md) |
| Understand a recorded architectural decision | [ADR guidance](adr.md) | [ADR](../templates/adr.md) |
| Assess a release's user impact | [History workflow](changelog-workflow.md) | [Release notes](../templates/release-notes.md) |
| Track user-visible code changes | [History workflow](changelog-workflow.md) | [Code changelog](../templates/code-changelog.md) |
| Track documentation changes | [History workflow](changelog-workflow.md) | [Documentation changelog](../templates/documentation-changelog.md) |
| Follow an attributed argument for a defined audience | [Article guidance](article.md) | [Article](../templates/article.md) |

A README often supplies orientation and routes onward. ADRs record a decision;
release notes communicate the consequences of verified changes. Select their
intent directly instead of forcing them into a quadrant.

## Split mixed purposes

Keep a page centered on one outcome. A how-to can state a short reason needed to
choose a step; a long discussion of design tradeoffs belongs in a linked
explanation. A reference can include a concise usage example that clarifies a
parameter. Its conceptual structure should match the product, and can differ
from the literal file tree. Use the
[reference principles](https://diataxis.fr/reference/#key-principles) when that
boundary is unclear.

For example, split "Set up line counting and understand text processing" into a
prepared learning path and an explanation of newline semantics. Link them at the
point where the reader needs further understanding. A lookup page for arguments
remains useful alongside both.

Choose a [structure](structure.md), load the selected upstream type guidance, and
use only that type's template and completed example. When a source cannot be
accessed, record the URL, the affected decision and the local guidance used;
label unverified source-dependent judgments in the review record.
