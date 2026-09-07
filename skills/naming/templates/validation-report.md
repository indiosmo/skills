# Naming validation report

Owner: [contextual validation](../references/contextual-validation.md).
[Renaming](../references/renaming.md#verify-the-edited-result) owns applied-change
checks. Complete the core assessment and evidence limits. Add change checks for
an applied rename and rechecks for corrected findings. A small review can use
compact prose containing the same evidence and actual statuses.

## Name assessment

- Artifact: {Exact spelling, declaration identity/path or described artifact,
  and reviewed revision or supplied input version.}
- Meaning and selection: {Intended concept and behavior; existing name or
  [decision](naming-decision.md) being reviewed, including its actual status.}
- Examined context: {Declarations, branches, callers, peers, vocabulary,
  documents, tests, and contracts actually inspected; relevant constraints.}
- Findings:

| Finding | Evidence and method | Effect on the assessment | Status |
| --- | --- | --- | --- |
| {Concrete fit or mismatch between the name and behavior/use} | {Path/symbol/section and observation; distinguish static inspection, executed check, and human judgment} | {Supported interpretation or misleading expectation} | {Supported / open / corrected / rechecked, with evidence} |

- Contextual finding: {Supported / rejected / provisional / pending; explain
  the evidence and scope supporting that finding.}
- Recommendation: {Retained or recommended spelling in a representative use,
  rationale, any assumption that makes it provisional, or the concept/selection
  question to revisit.}
- Decision status: {Proposed / accepted / unresolved; record acceptance with
  the authorized person or role and evidence of their actual decision. A supported
  contextual finding supplies grounds for the recommendation.}

## Applied-change checks

Include this section for actual edits. Record the authorized scope, precise
mapping, compatibility policy, and [rename plan](rename-plan.md) link or summary.

| Check and contract exercised | Revision and command or inspection scope | Observed result and diagnostics | Coverage |
| --- | --- | --- | --- |
| {Bindings, imports/keywords, behavior boundaries, preserved spellings, existing clients, schema, or examples} | {Exact command and working directory, or inspected diff/paths/symbols} | {Passed / failed / unavailable / pending; actual output or evidence location} | {Cases established by this check and material remaining uncertainty} |

## Corrections and rechecks

Include for revised findings or names.

| Finding | Correction and affected context | Fresh recheck evidence | Result |
| --- | --- | --- | --- |
| {Finding identity} | {Changed spelling, clarified concept, or scoped edit} | {Command/inspection, revision, and observed evidence} | {Resolved / open / unavailable / pending; reason} |

## Evidence limits and next action

- Confidence scope: {What the inspected evidence establishes about this name.}
- Unknowns and assumptions: {Material contexts awaiting inspection, inaccessible consumers,
  missing implementation, or assumptions and their effect on the result.}
- Tool limitations: {Failed or unavailable command, diagnostics, affected
  coverage, and independent evidence gathered; omit when inapplicable.}
- Human review: {Actual reviewer and judgment if received; pending or outside
  this review's scope otherwise.}
- Next action: {Required evidence or correction, responsible person when known,
  and pending checks; state completion only for the demonstrated scope.}
