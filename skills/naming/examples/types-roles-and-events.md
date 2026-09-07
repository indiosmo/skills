# Clinical software: a record, a role, a request, and an occurrence

A developer describes an encounter workspace and asks whether its types can all
use `EncounterStatus`: one stores the encounter, another identifies the operator
allowed to close the workspace, and two more travel through its message handler.
The first task is to establish what each instance represents.

This original example uses FHIR R5's
[Encounter vocabulary](../references/sources.md#con-fhir-encounter) for a modeled
healthcare interaction. FHIR's [Observation vocabulary](../references/sources.md#con-fhir-observation)
also supplies a neighboring distinction: a laboratory observation can be a
`lab_result`, while a `diagnostic_report` requires the report's grouping and
context. The example's authorization rules, workspace states, and messages below
are explicitly local software contracts. They describe an application workflow.

## Elicit what changes and what persists

The scenario owner supplies these answers:

- An encounter record keeps its identifier while its local workspace state
  changes from `open` to `closed`.
- A staff account can hold a revocable assignment permitting closure for one
  encounter. The account persists after that assignment ends.
- A close request enters a handler with the encounter identifier, requesting
  account, and request time.
- The handler accepts a request only when the workspace is open and the account
  holds that encounter's closure assignment. An accepted transaction stores the
  closed state and a transition record; the event becomes available after commit.
- A rejected request returns a reason. A request against an already closed
  workspace is rejected under this local contract.

The available evidence is this description and the accepted terminology sources.
Application code, FHIR serialization, and real clinical workflows have not been
inspected. The modeled state `closed` is a local workspace state; its spelling
asserts no mapping to FHIR's enumerated encounter statuses.

## Select names for established concepts

| Artifact | Plausible candidates | Decision and decisive evidence |
| --- | --- | --- |
| Persistent encounter record | `Encounter`, `EncounterStatus` | Recommend `Encounter`; identifier and workspace state are fields of the represented interaction |
| Encounter-specific closure assignment | `EncounterCloser`, `Clinician` | Recommend `EncounterCloser`; the established membership rule is a revocable software permission |
| Request message | `CloseEncounter`, `EncounterClosed` | Recommend `CloseEncounter`; it requests a transition that can be rejected |
| Committed transition message | `EncounterClosed`, `CloseEncounter` | Recommend `EncounterClosed`; it records the accepted transition under the stated publication contract |
| Failed request result | `EncounterCloseRejected`, `EncounterClosed` | Recommend `EncounterCloseRejected`; its payload records why the precondition failed |

These are clear-winner decisions after separating the contracts. `Clinician`
would assert professional membership requiring its own evidence. A closure
assignment establishes the software role precisely, and the identifier binding
establishes which encounter it concerns. Command and event grammar follows the
qualified conventions in [types and messages](../references/types-and-messages.md),
with persistence behavior supplied by this scenario.

Illustrative type and call-site pseudocode:

```text
Encounter(identifier, workspace_state)
EncounterCloser(account_identifier, encounter_identifier)
CloseEncounter(encounter_identifier, requested_by, requested_at)
EncounterClosed(encounter_identifier, closed_at)
EncounterCloseRejected(encounter_identifier, reason)

request = CloseEncounter(encounter.identifier, account.identifier, request_time)
outcome = encounter_service.handle(request)
if outcome is EncounterClosed:
    show_workspace_closed(outcome.closed_at)
if outcome is EncounterCloseRejected:
    show_closure_rejection(outcome.reason)
```

## Review the recommendation separately

The review tests the chosen message names against successful and rejected
requests, using the complete local precondition table:

| Workspace state | Requesting account has closure assignment | Handler result | State after handling |
| --- | --- | --- | --- |
| `open` | Yes | `EncounterClosed` after commit | `closed` |
| `open` | No | `EncounterCloseRejected` | `open` |
| `closed` | Yes | `EncounterCloseRejected` | `closed` |
| `closed` | No | `EncounterCloseRejected` | `closed` |

Independent Boolean enumeration confirms that only the open-and-assigned row
satisfies the stipulated acceptance predicate. Static review then traces the
state and event consequences from the supplied contract. Naming the request
`EncounterClosed` would misstate three of the four outcomes. The selected event
fits the accepted row and the separate post-commit publication assumption.

The role review checks revocation: ending an `EncounterCloser` assignment leaves
the underlying account and encounter records identifiable. The timestamp review
checks `requested_at` against request creation and `closed_at` against the
recorded transition. The neighboring-type review keeps a single `lab_result`
distinct from a report containing results and context; a collection alone cannot
establish report semantics.

Outcome: recommend the five selected names within this local model. The truth
predicate was enumerated independently; the message pseudocode remains
illustrative. Acceptance behavior, revocation, transaction rollback, event
publication, and any FHIR mapping require implementation and consumer evidence
before applying names to a real system. Human acceptance remains pending.
