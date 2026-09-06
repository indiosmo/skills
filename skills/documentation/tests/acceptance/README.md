# Skill acceptance

Acceptance combines automated package/tool checks with authored outputs and
editorial review. A successful command proves the exercised contract; it does
not establish human approval or the quality of every document route.

Run package structure and local resource links with the environment test project:

```sh
uv run --project skills/documentation/tests/environment --frozen pytest skills/documentation/tests/acceptance -q
```

## Scenario rubric

| Scenario | Required output and review |
| --- | --- |
| Tutorial | Prepared environment, learning outcome, observable progression, runnable example and next step |
| Multipart tutorial | Shared contract, separate page outcomes, starting state, previous/next navigation and complete path from fresh inputs |
| How-to/runbook | Operational prerequisites, ordered actions, evidence-backed branches, verification, recovery and applicable escalation |
| Explanation | Supported concepts, relationships and rationale; illustrations serve understanding |
| Generated reference | Correct comments and signatures, overload/parameter/example rendering, symbol resolution and native diagnostics |
| README update | Orientation, verified setup, useful links and consistency with neighboring pages |
| ADR | Evidenced context, alternatives, decision, consequences, project status and supersession conventions |
| Article | Defined audience, argument, attribution, fact checking and suitable conclusion |
| Release notes | Reader impact from verified final changes, bounded release claims and human review record |
| Code changelog | User-visible code changes, grouped/deduplicated, reverts accounted for and history links |
| Documentation changelog | Reader-guidance changes from the same range, separately supported |
| Drift review | Exact text, all six defect classes, evidence, impact and corrections; unchanged and inaccessible evidence distinguished |
| Missing/conflicting evidence | Target version resolved where possible; unresolved claims visible without fabricated support |
| Missing tools/unavailable links | Skipped/blocked validation with concrete cause and scope; no false pass |
| Existing site/source styles | Project settings preserved, nav/rendering checked; structural and prose diagnostics distinguish code tokens |
| Final pass | Only the eight categories in the array; exact unsupported sentences and missing evidence; clean output `[]` |

For each scenario retain the prompt, input revision, loaded resources, output,
checks, findings and reviewer assessment. Test the smallest justified resource
selection. Review a base reference directly without SKILL.md and separately
exercise a route through SKILL.md; both should lead to consistent substantive
guidance. Human references should state their purpose, supply enough context,
read coherently and contain useful examples and source links.

The document-type examples, editorial history/drift fixtures, and native-tool
fixtures provide inputs and expected results. Representative independent agent
runs and their grading form the end-to-end execution record. Review all goal
coverage obligations before marking the assembled package complete.

## Recorded results

See [the assembled acceptance results](results.md) for commands, authored
scenario assessments, corrected audit findings and explicit verification limits.
