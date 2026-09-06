# Final verification and human review

The final pass checks a draft as a skeptical developer and technical editor. Read
the document contract, current draft, supplied source material, review findings
and validation results. Verify each claim and action against its evidence rather
than treating a clean linter run as proof of factual correctness.

## Findings-only output

Return a JSON array. Each finding has `category`, `location`, `text`, `problem`
and `evidence_needed` fields. Category is exactly one of these eight labels:

1. Unsupported claims
2. Missing prerequisites
3. Ambiguous actions
4. Steps unverifiable from the supplied source material
5. Inconsistent product terminology
6. Content belonging in another Diataxis quadrant
7. Google-style issues in titles, headings, voice, and word choice
8. Risks of changing meaning in code samples

For unsupported claims, `text` contains the exact sentence and `evidence_needed`
names the missing support. For other categories, quote the relevant text or
identify the missing step at a precise location and explain the evidence needed
to settle the issue. Classify a finding by its principal problem; keep separate
findings when independent corrections are required. Use the
[final-findings template](../templates/final-findings.md).

A clean pass returns exactly `[]`. Keep commands, execution reports, approval
status and delivery summaries outside this array. The category list is fixed by
this workflow's review contract; it is not a claim that these labels exhaust all
possible project concerns. Record other project concerns in their own review
records.

For example:

```json
[
  {
    "category": "Unsupported claims",
    "location": "guide.md:12",
    "text": "The counter accepts every file format.",
    "problem": "The supplied implementation only demonstrates UTF-8 text input.",
    "evidence_needed": "A supported-format contract and tests for the claimed formats."
  }
]
```

## Human review record

Use [the human-review template](../templates/human-review.md) to name the factual
reviewer and any specialist required for security guidance, migrations,
destructive operations, compatibility or release-sensitive information. For
each applicable class, record the claims/changes, evidence, unresolved findings,
reviewer, status and approval reference. Use `pending`, `changes requested`,
`approved` or `not applicable` with a reason. Actual human confirmation is needed
for `approved`; automated output can support that review.

A factual reviewer might be the component maintainer; security guidance needs the
project's security owner, a migration needs its operational/data owner, and a
release claim needs the release maintainer. Infer ownership from project records
or ask for the missing owner. One qualified reviewer can cover several classes.

Renew review when a reviewed claim's meaning, target version, procedure, sample,
compatibility promise or supporting evidence changes. Record the reviewed
revision so later edits cannot inherit stale approval. A pending review is a
visible delivery state. Complete the authorized drafting and verification work
and present the concrete result for review according to the user's request.
