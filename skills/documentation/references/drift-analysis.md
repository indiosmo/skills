# Checking a document for drift

Drift analysis starts with a selected page and asks which of its current claims
still match the product and surrounding documentation. Record the page revision,
target product version and scope, then map its claims to relevant files, symbols,
schemas, tests, linked pages and executable examples. Use
[the drift-report template](../templates/drift-report.md).

## Compare claims with current evidence

Read the current sources and available history for each mapped claim. Reproduce
behavior where practical and reuse [link validation](link-validation.md) and
[example checks](examples.md). Inspect the claim's exact words before deciding
that a source change affects it. A refactor that preserves behavior is not itself
a documentation defect.

| Classification | Evidence to record |
| --- | --- |
| Factual mismatch | Exact claim and conflicting target-version behavior or accepted contract |
| Broken link | Link text/destination and definitive file, anchor or response failure |
| Stale example | Sample and a reproducible difference in behavior or expected output |
| Terminology change | Old term, current domain/interface term and source for the mapping |
| Contradiction | Both page locations, their scopes/versions and evidence resolving the disagreement |
| Unverifiable claim | Exact claim, missing/inaccessible evidence and what would resolve it |
| Unchanged | Claim and current evidence confirming its relevant meaning |

Distinguish an unavailable network/source from a definitive broken link. An
unchanged claim is useful audit evidence but does not appear as a defect in the
final findings-only pass. When historical rationale is still accurately dated,
a later design change calls for a supersession link or current explanation,
rather than rewriting the historical reason.

## Propose a correction

For each defect, record the exact affected text, current evidence and revision,
reader impact, proposed replacement and checks needed after editing. Apply
corrections within the authorized task and inspect relevant neighboring pages
using [contextual review](contextual-review.md). Renew human review when factual
meaning or consequential instructions change.

For a selected page, a small claim-to-source table and native git history are
sufficient dependency tracking. Investigate automation only when actual repeated
mapping work demonstrates a gap. The
[before/after fixture](../tests/editorial/drift/README.md) exercises every class,
including unchanged claims and unavailable evidence, with explicit corrections.
