# Rename plan

Owner: [renaming](../references/renaming.md). Fill the core mapping, boundary,
checks, and recovery record. A local rename can use compact prose and a reviewed
diff with equivalent evidence. Add the migration section when public or persisted
representations require staged change.

## Core record

- Naming basis: {Concept and behavior, selected name, rationale, and actual
  [contextual validation](validation-report.md) result or pending findings.}
- Authorization: {Request or prior decision authorizing this action; actual
  authorized edit scope and any pending scope decision.}
- Starting state: {Checkout/revision and existing local changes relevant to this
  edit; baseline behavior and supporting check results.}
- Assumptions and unknowns: {Material questions, consequences, and evidence needed
  before dependent edits.}

## Exact symbol mapping

| Declaration identity and path | Current spelling | Selected spelling | Meaning and preserved behavior |
| --- | --- | --- | --- |
| {Qualified symbol, parameter owner, or schema/configuration location} | {Exact text} | {Exact text} | {Values, truth conditions, effects, defaults, units, or state transitions} |

## Affected boundaries and compatibility

| Surface and location | Referent or representation | Planned action | Compatibility evidence |
| --- | --- | --- | --- |
| {Declaration, import, keyword caller, runtime string, generator, wire field, persisted name, configuration, documentation, or example} | {Binding identity or external contract; classify same-spelling independent symbols} | {Rename / retain / map / alias / regenerate / migrate, with exact spelling} | {Consumers, support policy, preserved spellings and behavior, or pending evidence} |

- Discovery scope: {Symbol-tool query and scoped old/new spelling searches,
  inspected results, collisions, and remaining coverage limits.}
- Chosen approach: {Direct/internal rename, retention, alias, or staged migration;
  rationale and [comparison](candidate-comparison.md) when tradeoffs require it.}
- Edit sequence: {Concrete ordered changes, affected bindings, and regeneration
  commands where relevant.}

## Checks and execution record

| Contract or affected use | Baseline evidence | Planned post-edit check | Actual result |
| --- | --- | --- | --- |
| {Behavior boundaries, imports/keywords, unrelated symbols, retained public spellings, schema, existing clients, or examples} | {Revision, command/inspection scope, observed result} | {Exact command and working directory or diff/inspection scope; expected contract} | {Pending / passed / failed / unavailable; revision, diagnostics and evidence} |

- Final diff review: {Actual inspected paths and binding/contract findings;
  classification of remaining old spellings and new-name collisions.}
- Final name assessment: {Distinct review of the final use sites and actual
  outcome; link the completed [validation report](validation-report.md).}
- Remaining uncertainty: {Dynamic or inaccessible consumers, unavailable checks,
  and follow-up evidence needed.}

## Recovery

- Trigger: {Failure or finding that requires reversal or another migration step.}
- Recovery action: {Focused diff reversal preserving other work, or concrete
  deployed recovery/conversion procedure within the authorized scope.}
- Recovery evidence: {For local edits, reviewed reversal scope; for representation
  changes, previous-reader compatibility or tested conversion and observed result.
  Record pending checks explicitly.}

## Conditional migration record

| Concern | Record |
| --- | --- |
| Supported versions and consumers | {Old/new readers and writers, stored data, dormant/offline clients, and required compatibility combinations.} |
| Aliases or multiple representations | {Exact accepted spellings, conflict precedence, canonical output, source of truth, and support duration.} |
| Rollout | {Ordered steps, deployment authorization/status, owners, backfill/resumption and dual-write failure handling when relevant.} |
| Cutover and retirement | {Evidence gates, observed consumer coverage, persistence window, responsible decision authority, and actual status.} |
| Recovery after cutover | {Values written after transition, previous-version readability, conversion procedure, and actual verification.} |
