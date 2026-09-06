# Writing a README

A README helps a newcomer identify a project or component, run an initial task,
and find deeper documentation. Use the [README template](../templates/readme.md)
and [worked example](../examples/document-types/readme.md). Write the Docs'
[writing guide](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/)
provides the broader audience and usefulness principles.

## Choose the scope

A root README introduces the project, prerequisites, first useful command, and
major concepts. A module README explains its role in that project and how its
parts relate. A component README provides the context needed to understand or
extend that component. Give each enough context for someone arriving directly.
Link to the parent for broader orientation and to children for deeper tasks.

Use the project's naming and placement conventions. Add a page when a reader
needs orientation that existing navigation cannot supply. Include sections only
when they help that reader.

## Keep information maintainable

Describe patterns and link shared rationale to its owning explanation or ADR.
Definitions and schemas own configuration facts; generated reference can expose
them completely. Include exact commands and required inputs in a getting-started
procedure when readers need them, and verify those examples against the target
revision. An orientation page benefits from a short path into the reference
rather than a copied inventory of every field.

Explain cross-tool ordering, access requirements, conditional dependencies and
surprising operational effects when they matter to the reader. Verify them
against project evidence. Native dependency declarations help establish facts;
readers still need the prerequisites for the documented task.

## Review

Check that a newcomer can identify the scope, execute the first task, and reach
the relevant reference. Verify commands and relative links. Check parent and
neighboring pages for contradictory or repeated explanations. Review exact
configuration names and values against their definitions when examples use them.
