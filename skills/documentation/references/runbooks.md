# Writing an operational runbook

A runbook guides an operator through a specific operational task or closely
related group. Use the [runbook template](../templates/runbook.md) and
[worked example](../examples/document-types/runbook.md). Apply Google's
[procedure guidance](https://developers.google.com/style/procedures) and the
[Diataxis how-to guidance](https://diataxis.fr/how-to-guides/).

## Establish the operating conditions

State the outcome, target environment/version, required access, tools, starting
state and operator role. Give enough mechanism-level context to understand the
consequences. Use project evidence for risk, automation behavior, recovery and
escalation contacts. Even a single command can require a runbook when its
preconditions and consequences need careful handling.

## Write the procedure

Use ordered actions with exact commands or clearly described interactive steps.
Explain how to replace placeholders before execution. Show checkpoints with
expected output or state. Put consequential warnings before the action, including
the condition that triggers the risk and the operator's response.

Provide branches and manual alternatives only when supported by evidence.
Explain how automated reconciliation affects manual changes when applicable.
Include verified recovery steps, stop conditions, cleanup and an escalation path.
A missing recovery procedure is a review finding that needs an owner.

Keep one procedure or a cohesive group in scope; link independently useful
subprocedures. Name the page after the task and follow existing site placement.
A short list of operational files can help troubleshooting when each link has
a clear purpose.

## Review

An operator should be able to confirm prerequisites, execute each step, detect
failure and know when to stop. Verify the procedure in a representative safe
environment or record the execution limit. Have the relevant human reviewer
check factual, security, migration, destructive and compatibility claims.
See the [evidence guidance](evidence.md) for traceability.
