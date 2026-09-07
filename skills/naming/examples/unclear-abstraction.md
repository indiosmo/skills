# Give a sparse abstraction a testable meaning

An engineer asks: "I need a class for keeping things together while someone is
working. What should I call it?" That sentence is the complete starting input
for this original, scripted example. The artifact is a class; its purpose is
broad. Domain, members, ownership, persistence, and callers are open questions.

## Separate two plausible concepts

"Keeping things together" admits at least two distinct concepts:

| Tentative concept | Distinguishing question | Conditional name |
| --- | --- | --- |
| A durable collection of work someone can return to | Does the same collection remain meaningful after work stops? | `Workspace`, if that is the local term for the collection |
| One period of active work with temporary state | Does stopping end this instance's identity and lifetime? | `WorkSession`, if the domain describes that interval as a session |

These are hypotheses about meaning. Neither the original phrase nor the word
"class" establishes either definition. Comparing their spellings numerically
would hide the unresolved identity boundary. First ask a case whose answer
separates them, using the
[identity and lifetime distinctions](../references/foundations.md#separate-meaning-identity-and-wording).

## Ask for one concrete scenario

Every line of the following dialogue is an original scripted example. The
replies supply fictional facts for demonstration; actual user input remains
the evidence needed in a real naming request.

**Assistant:** Someone stops working and comes back tomorrow. Should they return
to the same thing this class represents, or start a new one while their work
remains somewhere else? What are they working on in this example?

**Engineer:** They are reviewing a document. The document remains tomorrow, but
this object represents one review session and ends when they leave. It keeps
their current position in the document and their unsaved annotations.

That answer narrows the target to a review session and separates its lifetime
from the document's. It supplies only two possible members. An additional
ownership question matters because a document-wide session and a reviewer's
session would give the same member access different meanings.

**Assistant:** Two reviewers open the same document. If one changes position or
adds an unsaved annotation, should the other see that change in this object?

**Engineer:** Each reviewer has their own review session. Position and unsaved
annotations belong to that reviewer's session. The editor holds the active
session. The local terms are document, review session, and annotation.

## Read the narrowed name with its parent and members

Recommend `ReviewSession` within this scripted branch. The supplied local term
and session lifetime make it a clear choice; `Workspace` would emphasize the
durable-collection hypothesis. The containing editor supplies active-session
context, while the members state what the session holds.

Illustrative pseudocode for the described relationships and a consuming call:

```text
class ReviewSession:
    document
    current_position
    unsaved_annotations

class DocumentEditor:
    review_session: ReviewSession

document_view.show(
    editor.review_session.document,
    editor.review_session.current_position,
    editor.review_session.unsaved_annotations,
)
```

The proposed expression `editor.review_session.current_position` ties the
position to this reviewer's active session. By comparison,
`document.current_position` suggests document-wide state. Naming the parent
relationship exposes that distinction without specifying storage or constructors.
`unsaved_annotations` uses the reply's stated condition; the saving operation
and its failure behavior remain unknown.

## Keep the unanswered branch conditional

If the engineer has yet to answer the first question, record both definitions
and the question as pending. Offer `Workspace` only under the durable-collection
assumption and `WorkSession` only under the temporary-interval assumption. Keep
dependent member and caller recommendations pending. A reply describing a
different concept reopens the candidates.

The scripted replies above support a description-level proposal, with a small
set of explicit facts. They leave how leaving affects unsaved annotations,
whether sessions can resume after interruption, and how the editor associates a
session with a reviewer open for implementation review. Those facts may refine
the lifetime definition and name. Ask about any of them when the proposed API
makes that distinction material.

## Distinct review of the session proposal

| Supplied fact | Contextual finding |
| --- | --- |
| One document review interval ends when the reviewer leaves | `ReviewSession` expresses the stated unit and lifetime |
| The document persists beyond that interval | A `document` member keeps the enduring work separate from session state |
| Two reviewers hold separate positions and unsaved annotations | The editor's `review_session` supplies the scope of the member reads |
| The local phrase is "review session" | The class preserves the supplied vocabulary in full words |

Static review compares the scripted facts, candidate definitions, and proposed
expressions. Pseudocode has no execution result. Actual declarations, ownership,
session lifecycle, caller behavior, and collisions await implementation and
real-user review. Carry this provisional result in the
[naming brief](../templates/naming-brief.md).

## A described operation with an unresolved effect boundary

An engineer asks: "What should I call `ImportManager`? It previews catalog rows,
stores valid rows, and emails the summary." This original description-only
scenario concerns an internal administrative tool. The supplied description and
the sketch below are the entire evidence packet. No implementation, caller
inventory, retry policy, or failure test is available.

The words `preview`, `import`, and `summary` describe local software operations.
The open question is their relationship: a preview may mean a calculation of
potential changes, or the screen may display the outcome of an already committed
import. Establishing that relationship follows
[elicitation](../references/elicitation.md#keep-intent-and-observation-distinct),
and the concern about cohesion follows
[module boundaries](../references/modules-packages-and-files.md#start-with-the-boundary).
The broad existing name is evidence of uncertainty, rather than proof that the
class must be split.

### Capture the evidence without filling its gaps

Illustrative pseudocode, with order transcribed from the supplied description:

```text
ImportManager.run(rows):
    preview = prepare_preview(rows)
    stored_rows = store_valid_rows(rows)
    email_summary(preview, stored_rows)
    return preview

preview = import_manager.run(uploaded_rows)
display_preview(preview)
```

This sketch puts storage before the returned preview. It leaves transaction
boundaries, mail failures, retry effects, and the meaning of "valid" unspecified.
Those are recorded unknowns. In particular, a normal return's implications for
email delivery cannot be inferred from `email_summary` alone.

A material scenario question for the engineer is:

> When the user opens the preview and then cancels, should the catalog already
> contain the accepted rows, or should storage happen only after confirmation?

This is a scripted question in a worked example. The engineer's answer is
pending; the example supplies no invented reply. The answer changes the operation
being named and which effects belong at the preview call site.

### Separate conditional names from a redesign

Three initial candidates test different definitions:

| Candidate and illustrative use | Contract needed | Current assessment |
| --- | --- | --- |
| `CatalogImportPreview`; `preview = catalog_import_preview.prepare(rows)` | Preparing a preview computes the proposed outcome | The storage step contradicts that reading of the supplied sketch |
| `CatalogImport`; `import_report = catalog_import.run(rows)` | A run performs one catalog import with a documented completion boundary | Provisional candidate if the engineer confirms storage is intended at this point |
| `CatalogImportWorkflow`; `import_report = catalog_import_workflow.run(rows)` | Preview preparation, commit, and summary dispatch are one named workflow | Provisional candidate if the engineer confirms that unified lifecycle |

The candidates represent competing meanings with unresolved hard constraints.
Numeric scores would imply a settled concept. Gather the answer before comparing
viable spellings for a single definition. The eventual comparison may favor
`CatalogImport` when its context already establishes orchestration, or
`CatalogImportWorkflow` when a neighboring import value requires a distinction.
That neighboring type inventory is also missing.

For the present request, recommend deferring the replacement and retaining
`ImportManager` as the current binding while the question is resolved. Retention
here is a temporary scope decision, with naming fitness unresolved. A provisional
phrase for the observed sequence is "catalog import and summary workflow";
it supports discussion without inventing a completion guarantee.

Separately, a possible redesign would expose a preview-producing query, a
commit operation, and a summary-dispatch operation. That proposal changes entry
points and failure handling. Its value depends on the cancellation answer and
retry requirements. Record it as a design proposal for review. The naming task
provides no authorization to implement that behavioral change.

### Distinct contextual review

Review the provisional recommendation against the supplied sketch and caller:

| Evidence | Finding | Result |
| --- | --- | --- |
| `store_valid_rows` precedes return | The described sequence has a storage effect | A preview-only name fails the observed sequence |
| Caller assigns and displays `preview` | The caller emphasizes a computed presentation result | The intended relation between presentation and commit needs elicitation |
| `email_summary` follows storage | At least two effect boundaries appear | A workflow name requires an explicit failure/completion contract |
| Description returns only `preview` | Naming the result `import_report` assumes broader content | Keep `preview` in the current sketch until its actual fields are known |

Assessment: revisit the concept. Conditional candidates remain suggestions;
none has passed complete contextual validation. Inspect the actual caller that
handles cancellation, then the operation's transaction and mail-failure paths.
Ask whether a retry after mail failure can write the rows again. Those facts
will settle the boundary and distinguish a naming change from a behavior fix.

Static review establishes a real tension within the supplied description. It
does not establish production side effects, safe retries, or a necessary class
decomposition. Implementation and caller checks remain pending. Carry those
limits in the [naming brief](../templates/naming-brief.md), then return to
[selection](../references/selection.md) after the material answer.
