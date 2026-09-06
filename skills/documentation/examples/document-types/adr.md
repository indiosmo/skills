# Use wc for the prepared counting exercises

Status: Accepted in the fictional fixture
Decision date: 2026-09-01
Recorded: 2026-09-01
Owner: Training coordinator

## Context

Text Workshop needs a repeatable newline-counting command for prepared ASCII
samples. The [decision evidence](evidence/README.md) records that the training
environment already includes Bash and wc.

## Alternatives

The coordinator considered a separate counter implementation and a small Bash
wrapper around wc. For the prepared scope, the wrapper was the clear choice:
wc already performs the needed count, and the wrapper provides a consistent input
check. A separate implementation would introduce counting logic to maintain.

## Decision

Use wc through the Bash wrapper. The coordinator selected readable input
validation and a short invocation for the exercises.

## Consequences and confirmation

The prepared environment requires Bash and wc. Environments without those tools
need separate preparation. Confirmation consists of running the sample and
observing 2, as recorded in the [verification results](verification.md).

Changed decisions follow the fixture's documented supersession policy. The
[reference](reference.md) describes the current command contract.
