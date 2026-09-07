# Candidate comparison

Owner: [selection](../references/selection.md). Candidate formation belongs to
[candidate generation](../references/candidate-generation.md).
Complete the core record and hard constraints before scoring eligible options.
For a clear winner, use compact prose with the same decision evidence and the
reason it wins. Expand the matrix when viable options have meaningful tradeoffs.

## Core record

- Brief: {Link or summarize the concept, behavior, vocabulary, audience, scope,
  evidence, and constraints from the [naming brief](naming-brief.md).}
- Assumptions and unknowns: {State each assumption, its evidence, and what answer
  would change eligibility or preference; record none when supported.}
- Candidates in context: {Show each spelling at equivalent declarations,
  representative calls/imports/conditions, and relevant prose.}

## Hard constraints

| Candidate | Required meaning or contract | Evidence | Eligibility |
| --- | --- | --- | --- |
| {Spelling} | {Behavior, vocabulary, binding, convention, or compatibility requirement} | {Exact use or source supporting the assessment} | {Eligible / excluded / unresolved; reason} |

Resolve material eligibility unknowns before a dependent decision. Excluded
candidates retain their evidence in this table.

## Conditional matrix: competing viable options

Define relevant criteria and anchors before scoring. Use 1 for weak fit, 3 for
adequate or mixed fit, and 5 for strong fit, with larger values always better.
Give each cell a score and evidence-based reason. Use `?` with missing evidence
for unknowns; leave their numeric contribution unassigned. Weights default to 1;
record the task priority supporting any other weight.

| Criterion and concrete score anchors | Weight and priority | {Candidate spelling} | {Candidate spelling} |
| --- | --- | --- | --- |
| {Relevant distinction; meaning of 1, 3, and 5} | {Weight; evidence for priority} | {Score: reason and use/source} | {Score: reason and use/source} |
| Weighted total | {Sum of weight times score; state incomplete when cells remain unknown} | {Total or incomplete} | {Total or incomplete} |

- Result: {Recommended spelling, decisive criteria, and the main tradeoff.}
- Sensitivity: {Whether a plausible change in priority or unresolved evidence
  changes the result, with recalculated totals where relevant.}
- Presented matrix: {Path/link to the self-contained HTML artifact and actual
  inspection results for final visible decision text, criteria, weights, reasons,
  arithmetic, and consistency with this recommendation, following
  [portable matrix guidance](../references/selection.md#present-a-portable-matrix).}

Adapt inherited captions and decision text to the actual evidence. Ground any
weight adjustment in a task priority and its calculated effect; state the relevant
sensitivity finding or open question in the HTML as well as this record.

## Decision and separate review

- Selection status: {Proposed / accepted / unresolved; actual decision authority
  and evidence of that person's or role's decision when accepted.}
- Rationale: {Why this name fits; remaining assumptions and condition that would
  reopen the comparison. Link the [decision](naming-decision.md) if separate.}
- Verification: {Pending or actual [contextual validation](validation-report.md)
  finding: supported / rejected / provisional; evidence and coverage limits,
  distinguishing naming judgment from executed behavior checks.}
