# Compare names for a download concurrency bound

Recommend `maximum_concurrent_downloads` for the internal setting in this
original example. It makes the bound explicit in isolated configuration examples
and distinguishes the setting from the current number of downloads. The choice
changes if matching the documentation's phrase becomes the leading priority.

## Brief and evidence packet

This fictional download application supplies the following design packet. Its
prose and pseudocode are the evidence for this example; implementation and actual
consumer behavior require subsequent checks.

| Evidence | Supplied content |
| --- | --- |
| E1: behavior contract | The setting is a positive integer bounding simultaneous downloads. Starting a download requires `downloads_in_progress` to be smaller than the bound. The scheduler reserves a slot before starting work and releases it when that download ends. |
| E2: guide terminology | The draft guide heading is "Download concurrency." Its sentence reads: "Set the maximum number of simultaneous downloads; the minimum is one." |
| E3: draft declaration and reader contexts | The unpublished draft uses `download_concurrency`. Engineers read isolated keyword examples during setup and receiver-qualified fields while maintaining the scheduler. Both contexts matter equally for this comparison. |
| E4: neighboring concepts and scope | `downloads_in_progress` counts occupied slots. `download_timeout_seconds` bounds duration. The requested decision selects an internal field name; the draft has no published configuration key or consumers. |

The artifact is an integer configuration field and constructor parameter.
"Download concurrency" is the scenario's documented term for simultaneous
downloads. This local definition supplies the domain meaning; the numerical
scores below express naming judgments under
[selection policy](../references/selection.md), rather than empirical results.

The packet settles the behavior and intended audience. Uncertainty remains about
actual use frequency, collisions, serialization, and the scheduler's enforcement
of the bound. A source tree and representative users would resolve those points.
The recommendation assumes E1-E4 hold when implementation begins.

## Hard constraints before preferences

All eligible options describe the same positive-integer upper bound, use full
words, and follow the draft's underscore-separated convention. E1 permits
overlapping downloads; the setting denotes their permitted simultaneous count.

| Candidate | Meaning and evidence | Eligibility |
| --- | --- | --- |
| `download_concurrency` | Current unpublished draft spelling; E2 supplies its precise bound interpretation. | Eligible, with the contract alongside the field. |
| `concurrent_download_limit` | Names the bounded activity and its limit, agreeing with E1. | Eligible. |
| `maximum_concurrent_downloads` | Expresses the maximum simultaneous count established by E1. | Eligible. |
| `downloads_in_progress` | E4 assigns this spelling to the current occupied-slot count, which varies independently of the bound. | Excluded: conflicting concept and declaration identity. |

These are naming alternatives for one setting. Complexity, execution cost,
coupling, testability, reversibility, and blast radius are equal under E3-E4:
each choice changes the same unpublished field and examples. Those properties
therefore receive no preference scores. Publication would require a new
compatibility assessment.

## Candidates at equivalent use sites

The following is illustrative pseudocode. Each pair represents a separate
alternative for the same declaration and comparison:

```text
DownloadSettings(download_concurrency=4)
downloads_in_progress < settings.download_concurrency

DownloadSettings(concurrent_download_limit=4)
downloads_in_progress < settings.concurrent_download_limit

DownloadSettings(maximum_concurrent_downloads=4)
downloads_in_progress < settings.maximum_concurrent_downloads
```

The guide would read, respectively, "Set `download_concurrency` to 4,"
"Set `concurrent_download_limit` to 4," or
"Set `maximum_concurrent_downloads` to 4." In all three cases the adjacent
sentence defines four simultaneous downloads as the permitted maximum.

## Grounded comparison

Define criteria before scoring: phrase lookup concerns movement from the guide
heading to the declaration; isolated clarity concerns the keyword alone; counter
contrast concerns reading the comparison; qualified rhythm concerns the
receiver-plus-field expression. These are distinct reading tasks. Each weight
is 1 because E3 supplies no priority among them. Scores use 1 for weak fit,
3 for adequate or mixed fit, and 5 for strong fit. The anchors below make those
judgments reviewable.

| Criterion and anchors | Weight | `download_concurrency` | `concurrent_download_limit` | `maximum_concurrent_downloads` |
| --- | --- | --- | --- | --- |
| Guide phrase lookup: 5 repeats E2's phrase; 3 changes its grammatical form; 1 loses its subject | 1 | 5: repeats "Download concurrency." | 3: changes concurrency to concurrent and reorders the subject. | 3: changes concurrency to concurrent and introduces maximum. |
| Isolated bound clarity: 5 explicitly states a maximum count; 3 needs E2's counting sentence; 1 suggests current occupancy | 1 | 3: concurrency needs the bound definition. | 3: limit names a bound; E2 establishes its count meaning. | 5: maximum plus plural downloads states the count bound. |
| Contrast with occupied slots: 5 pairs the current count with an explicit maximum; 3 distinguishes the setting through its defined term; 1 repeats E4's counter | 1 | 3: comparison relies on concurrency's defined meaning. | 3: comparison names a limit through its defined term. | 5: `downloads_in_progress` reads directly against a maximum. |
| Qualified expression rhythm: 5 supplies the concept in two words after the receiver; 3 adds a third qualifier useful mainly in isolation; 1 repeats the entire receiver name | 1 | 5: `settings.download_concurrency` supplies the two-word concept. | 3: `settings.concurrent_download_limit` adds the bound qualifier. | 3: `settings.maximum_concurrent_downloads` adds the bound qualifier. |
| Weighted total | | 16 | 12 | 16 |

The totals tie the current draft and `maximum_concurrent_downloads`. The
recommendation favors the explicit maximum because the two contexts most exposed
to a mistaken count interpretation are the isolated keyword and the comparison
with occupied slots. This is a stated judgment at equal weights, subject to
reader review; the arithmetic establishes a tie rather than an automatic winner.
`concurrent_download_limit` is viable but offers neither exact phrase matching
nor the strongest count wording under these anchors.

Sensitivity: raising isolated-bound clarity to weight 2 yields 19, 15, and 21,
favoring `maximum_concurrent_downloads`. Raising guide phrase lookup to weight 2
instead yields 21, 15, and 19, favoring the current `download_concurrency`.
The [completed HTML matrix](candidate-matrix.html) preserves these cells,
weights, samples, and conditions. Its totals and source structure were checked;
visual inspection remains pending because the available browser failed during
sandboxed startup with a crashpad `setsockopt` error.

## Decision and distinct contextual review

Selection status: proposed `maximum_concurrent_downloads`. No actual stakeholder
acceptance is recorded. The comparison supports a choice with an explicit
tradeoff; reader priorities can reopen it.

The review then checks the proposed name against E1-E4 independently of scores:

| Review finding | Evidence and method | Outcome |
| --- | --- | --- |
| A maximum simultaneous count agrees with the intended admission boundary. | Static reading of E1: with bound 4, occupied counts 0 and 3 permit admission; 4 requires waiting for a released slot. | Description-level fit supported. |
| The bound is distinct from a duration and from current occupancy. | Compare proposed uses with both E4 neighbors and E2's unit-free integer definition. | Naming distinction supported. |
| Keyword and receiver contexts retain the same meaning. | Inspect all six pseudocode lines and the guide sentence above. | Static use-site fit supported. |
| Actual scheduling and public-contract behavior remain open. | Evidence packet comprises a design description and unpublished draft statements. | Implementation, binding, serialization, and execution checks pending. |

Outcome: the supplied design packet supports the proposed name. The minimum
of one belongs to the setting's contract and validation. The name expresses the
maximum role; enforcement requires parser tests for zero and negative values and
scheduler tests at the admission boundary. Inspect slot reservation and release,
including failure paths, before claiming simultaneous downloads stay bounded.
Actual human judgment and observed reader priorities remain pending.

This record completes the core [brief](../templates/naming-brief.md),
[comparison](../templates/candidate-comparison.md),
[decision](../templates/naming-decision.md), and
[validation report](../templates/validation-report.md). Applying a rename in a
real project would add the [rename plan](../templates/rename-plan.md).
The matrix adapts the sibling decision-matrix skill's
[lean artifact](../../decision-matrix/assets/example-lean.html) and
[scoring styles](../../decision-matrix/assets/example.html), preserving its
inline palette and page chrome.
