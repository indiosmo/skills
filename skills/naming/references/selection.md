# Choose a name with evidence

Choose the candidate that fits the established concept and the readers' actual
context. First remove candidates that violate required meaning or contracts.
Then compare the remaining choices on properties that matter to this task.
Record the recommendation and its assumptions, and perform a distinct
[contextual validation](contextual-validation.md) afterward.

This comparison procedure is local policy
([LOCAL-004](evidence.md#local-004)), adapted from the repository's
[decision-matrix workflow](../../decision-matrix/SKILL.md#workflow).
Its scores express judgments grounded in the naming brief and inspected uses.
The [empirical studies](empirical-research.md) support bounded findings about
identifiers; they supply no universal numerical ranking formula for names.

## Apply hard constraints first

A hard constraint determines whether a candidate is eligible. Identify these
from the brief and evidence before assigning preference scores:

- Actual behavior: truth conditions, units, cardinality, results, side effects,
  defaults, and lifecycle must agree with the proposed meaning.
- Required vocabulary: preserve a domain distinction established for this context.
- Validity and binding: the declaration must be legal and resolve correctly in
  its language, scope, generated code, and case-sensitive environment.
- Required conventions: follow the project's applicable rules, including its
  full-word policy and accepted local abbreviation exception.
- Public contracts: honor the authorized compatibility policy for API names,
  serialized fields, configuration, imports, and persisted references.

Record a failure with the exact behavior or contract that contradicts the name.
Keep such candidates in an exclusion note if their rejection helps the reader.
A high readability score cannot compensate for a false predicate or an
unauthorized wire-field change ([COMP-015](evidence.md#comp-015),
[COMP-003](evidence.md#comp-003)). A proposed alias or migration is a distinct
option whose compatibility must first be established; see [renaming](renaming.md).

## Define the comparison before choosing

Turn likely misunderstandings into specific criteria. Use only criteria relevant
to the decision, and avoid counting the same concern in several rows.

| Concern | A criterion grounded in evidence |
| --- | --- |
| Semantic accuracy and domain fit | Readers identify the exact retry bound defined by the contract |
| Call-site readability | The name reads clearly with this receiver, arguments, and result |
| Distinguishability | Readers distinguish this concept from the adjacent timeout policy |
| Conventions | The spelling and grammar match inspected peer declarations |
| Discoverability | A reader searching the documented concept can locate its declaration |
| Maintenance and coupling | The name continues to fit changes permitted by the current abstraction |
| Compatibility and reversibility | The permitted change affects a known set of consumers and can be recovered |

Consider complexity, performance, blast radius, ergonomics, and testability when
the options actually differ on them. A pure local identifier spelling ordinarily
shares the same execution cost across candidates. State that equality when useful
and concentrate the scored comparison on genuine differences. Speculative future
behavior deserves an assumption or question rather than an unsupported score.

Use a consistent direction: larger scores mean better fit. A practical five-point
scale is 1 for a serious weakness, 3 for adequate or mixed fit, and 5 for strong
fit established by the cited evidence; 2 and 4 represent intermediate judgments.
Define concrete anchors for each row, such as "matches the documented term" at
5 and "requires readers to translate a synonym" at 3. Hard constraint violations
remain ineligible regardless of the numeric scale.

Give every scored cell a short reason tied to a use site or source. An unknown
receives `?` and the missing evidence, with its score left empty. Default weights
to 1. Increase a weight only for an explicit task priority, and explain that
priority before calculating totals. Higher weights mean greater decision impact.

## Worked comparison

In this original scenario, a request-delivery module exposes a new internal
integer field. It bounds retries after the initial request. The documentation
calls that bound a "retry limit," adjacent fields are `timeout_limit` and
`redirect_limit`, and configuration examples are often read without a receiver.
Both candidates pass the behavior, spelling, and internal-scope constraints.
This illustrative Python excerpt assumes the application's `delivery` object:

```python
delivery.retry_limit = 3
delivery.maximum_retries = 3
```

These lines show alternative spellings for the same declaration. Both examples
mean three retries after the initial request. The following judgments use the
scenario's stated documentation and neighboring fields as evidence.

| Criterion and anchor | Weight | `retry_limit` | `maximum_retries` |
| --- | --- | --- | --- |
| Documented vocabulary: 5 matches the established phrase; 3 needs a synonym translation | 1 | 5: directly matches "retry limit" | 3: maximum expresses the bound through another phrase |
| Peer consistency: 5 follows the inspected limit family; 3 introduces a second pattern | 1 | 5: follows `timeout_limit` and `redirect_limit` | 3: introduces maximum-plus-plural alongside noun-plus-limit |
| Isolated example clarity: 5 explicitly names a maximum count; 3 leaves the counting convention to prose | 1 | 3: limit needs its numeric contract explained | 5: maximum and plural retries express the count bound directly |
| Weighted total | | 13 | 11 |

Recommend `retry_limit` because the documentation and neighboring configuration
fields provide a coherent vocabulary. `maximum_retries` offers stronger wording
in isolated examples. If those examples are the primary reader context, changing
that row's weight from 1 to 2 produces a tie at 16; weight 3 favors
`maximum_retries` at 21 versus 19. The choice is sensitive to audience priority.
Resolve that priority through an actual use-site sample or a focused question
when it remains material. These scores are explained local judgments.

Selection is followed by validation: inspect the parser, actual comparisons,
zero-limit case, examples, and declaration neighbors. The scenario's supplied
facts support the recommendation; a real repository decision needs those facts
verified at their locations. The [comparison template](../templates/candidate-comparison.md)
and [decision template](../templates/naming-decision.md) capture this evidence.

## Present a portable matrix

When several viable options have meaningful tradeoffs, present the comparison
and produce a self-contained HTML artifact using the
[artifact instructions](../../decision-matrix/references/artifact-template.md).
Inspect the actual [lean example](../../decision-matrix/assets/example-lean.html)
before adapting it: it includes inline styles, option subtitles, sparse cell
coloring, use-site samples, assumptions, open questions, and per-matrix decisions.
Its actual tables also include a Notes column where cross-cutting content earns
that space. Choose optional columns based on the new comparison's content.

Preserve the supported layout and CSS, replace the scenario with original naming
content, and add the grounded scores required by this project's comparisons.
The sibling [full example](../../decision-matrix/assets/example.html) demonstrates
score badges, weights, and a weighted footer. Unknown cells remain unscored.
Keep the artifact portable with embedded CSS and plain-text content. Open the
result from disk and inspect its final visible text, including headings, captions,
notes, and the decision. Check actual candidate names, use-site samples, criteria,
weights, cell reasons, totals, and sensitivity claims against the comparison
record. Cell reasoning must remain intelligible independently of its color.

Adapt every inherited instruction to this decision's evidence. Explain a weight
change through a concrete audience priority or unresolved fact and show its effect
on the result. Replace generic invitations such as "tune weights to taste" with
the supported sensitivity finding or the specific question that would resolve it.
The HTML and accompanying recommendation must agree on the selected name,
decisive criteria, assumptions, and decision status.

Assess cells before drafting the decision. Put assumptions and open questions
above the table. State the result immediately below its matrix and use samples,
with the decisive criteria and the condition that would change the result.
Identify a recommendation as proposed. Record acceptance only with the actual
decision, its authorized person or role, and evidence that it occurred. Contextual
support and matrix scores establish grounds for a recommendation; acceptance is
a separate recorded decision.
The naming-specific [adoption boundaries](sources.md#local-matrix) preserve
proportionate candidate count and this distinction between proposal and decision.

## Record a clear winner directly

An established accurate name can be retained without invented alternatives.
For example: "Retain `retry_count`: the value counts completed retries, the
comparison uses that count, and adjacent code uses the same term. Contextual
review checked its declaration, increment, comparison, and configuration example."
In an actual report, supply those locations and observed results.

For a close comparison, explain the judgment or obtain the missing fact. For
contradictory evidence, return to [elicitation](elicitation.md) or
[candidate generation](candidate-generation.md). Every route ends with an explicit
recommendation, retained name, or unresolved decision, followed by the separate
validation outcome and its coverage limits.
