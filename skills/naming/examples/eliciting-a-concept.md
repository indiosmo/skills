# Elicit the meaning of a saved search flag

Recommend `has_unread_matches` for the boolean described here. A scenario question
establishes that it represents the reader's progress through search results.
The recommendation is provisional to the description.

For a class whose purpose is still abstract, start with
[a sparse abstraction](unclear-abstraction.md#separate-two-plausible-concepts).
That example establishes identity, lifetime, and ownership before proposing a
class name. This example begins with a known artifact kind and application,
then resolves the boolean's condition.

## Context and available evidence

This original, scripted dialogue illustrates direct naming assistance. The
engineer's statements define a fictional saved-search application; they are
neither a real user interview nor observed implementation behavior.

The initial request is: "Name the flag that tells us whether a saved search has
updates." The supplied description says that searches collect matching articles,
readers open articles individually, and the result list has a badge. The engineer
supplies proposed peer names `match_count` and `last_checked_at`. No source tree,
tests, deployed interface, or glossary accompanies the request.

The read-first step extracts three established concepts: a saved search, its
matching articles, and a reader. "Updates" could mean newly collected matches,
changed article text, or matches that the reader has yet to read. That ambiguity
changes the predicate and must be resolved before selection.

## Scripted dialogue

**Assistant:** A search collects one matching article. The reader opens it, and
the next search run finds the same article with edited text. Should the flag
be true after collection, after reading, and after the edit?

**Engineer:** True after collection, false after reading, and false after the
edit. An edited article keeps its read status. We call results "matches" and
articles the reader has yet to open "unread matches."

**Assistant:** If the reader opens one of two unread matches, should the badge
remain visible? Is read status shared among readers?

**Engineer:** Yes, it remains until both are read. Read status belongs to each
reader. A search with zero matches has no badge. This is a proposed internal
view-model field; it will be computed for the signed-in reader.

**Assistant:** `has_unread_matches` expresses that existential condition. The
field is true when at least one match is unread by the signed-in reader. Its
receiver needs to carry that reader-specific view.

**Engineer:** That is the intended condition. Keep the name as a proposal until
we have the view-model implementation to review.

## Completed naming brief

| Field | Record |
| --- | --- |
| Concept and behavior | A boolean for a reader's saved-search view: true exactly when at least one matching article is unread by that reader. Reading the last unread match clears it; an edit preserves read status. |
| Vocabulary | The scripted engineer establishes "match" and "unread match" for this application's boundary. `match_count` counts all matches; `last_checked_at` records a search check. |
| Context | Proposed internal view-model field, read by engineers implementing a per-reader result badge. Python-like spelling follows the supplied peer names. |
| Evidence | Initial description and the two scenario answers above; all are supplied scenario facts. |
| Constraints | Preserve reader scope, existential cardinality, read status, and full words. The request authorizes a naming recommendation. |
| Unknowns | Implementation of read status and the receiver's reader scope await code. Actual public exposure and naming collisions await contract and reference inspection. |
| Recommendation | Proposed `has_unread_matches`; the scripted engineer confirms intent and leaves selection provisional. |
| Verification | Description-level review below supports the predicate; implementation and actual caller checks remain pending. |

## Candidates and representative uses

These equivalent alternatives are illustrative pseudocode, each showing a
possible condition for the same view model:

```text
if reader_search_view.has_updates: show_unread_badge()
if reader_search_view.has_new_matches: show_unread_badge()
if reader_search_view.has_unread_matches: show_unread_badge()
```

`has_updates` leaves the event and reader relationship ambiguous.
`has_new_matches` invites a collection-time interpretation, while the scenario
turns the flag off when the reader opens the final unread match.
`has_unread_matches` directly matches the engineer's term and the badge's
condition. It is the clear winner after elicitation, so a scored matrix would
add little. The neighboring `match_count` still denotes the total collection.

## Distinct contextual review

Review the proposed name afresh against each supplied scenario, rather than
treating the engineer's confirmation as an implementation check:

| Case | Described result | Finding |
| --- | --- | --- |
| Zero matches | false | The plural object with `has` expresses existence, including the empty case. |
| One unread match | true | "Unread" identifies the condition that produces the badge. |
| Two unread matches, one opened | true | Existence remains true while one qualifying match remains. |
| Last unread match opened | false | Reader progress determines the result. |
| Read article edited | false | The specified read-status contract agrees with `unread`. |
| Same match read by one reader only | false for that reader, true for the other | `reader_search_view` supplies the reader scope assumed by the field. |

Outcome: the description supports `has_unread_matches` as a provisional
recommendation.
Static review covers the dialogue, the proposed condition, peer spellings, and
the case table. These expected results have not been executed against software.
The name uses full words and reads as a boolean predicate. A global
`saved_search.has_unread_matches` would reopen the receiver-scope question.

Next, inspect the read-status representation, view construction, badge caller,
and exposed schema. Execute the six cases above against that implementation.
Actual user review of the naming judgment remains pending; the scripted reply
is evidence within the example only.

This example instantiates the [brief](../templates/naming-brief.md),
[decision](../templates/naming-decision.md), and
[validation report](../templates/validation-report.md) in compact form. Its
procedure follows [elicitation](../references/elicitation.md) and
[contextual validation](../references/contextual-validation.md); vocabulary
comes from the scenario's explicit local definitions.
