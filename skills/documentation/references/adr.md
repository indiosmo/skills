# Recording an architectural decision

An architectural decision record (ADR) preserves the context, alternatives,
decision and consequences of one significant choice. A future maintainer should
understand why the choice made sense from the evidence available at the time.
Use the [ADR template](../templates/adr.md) and
[worked example](../examples/document-types/adr.md).

[Michael Nygard's original guidance](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
explains the core structure. The [ADR community resources](https://adr.github.io/)
link other formats for projects with different needs.

## Capture the decision

Identify the decision owner, date, status and evidence. Describe the forces
without implying a conclusion, then state the chosen option and its reasons.
Record plausible alternatives and their tradeoffs. When several options remain
viable, compare them against the decision's actual criteria. Consequences include
costs, benefits and observable confirmation conditions.

Follow the project's directory, numbering, title and review conventions. Keep
the record focused on one coherent decision with enough context to evaluate it.
Link durable specifications, discussions, related decisions and evidence.

## Preserve history

Follow the project's correction and supersession policy. Preserve the historical
meaning of an accepted decision. A changed decision generally needs a new record
with reciprocal supersession links; factual or editorial corrections should be
traceable under the local policy. Record status changes explicitly.

For reconstructed decisions, distinguish the date of the decision from the
recording date, attribute the evidence and mark uncertain rationale. Determine
acceptance from the project's actual decision process.

## Review

Check alternatives, rationale, consequences and confirmation against dated
evidence. Verify status and supersession links. Keep changing prices, forecasts
and compatibility claims scoped to their evidence and version. The decision
owner reviews those claims; an editor checks that a future reader can understand
the record independently.
