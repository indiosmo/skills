# Agreeing on a document contract

A document contract lets an author and reviewer agree on what a page helps its
reader accomplish. Use it for a new page or record the changed fields when
updating an existing page. For related pages, share the audience and target
version, then give each page its own outcome.

## Establish the task

Read the request, selected page, parent navigation and relevant project
instructions. Infer answers that the evidence supplies. Ask a focused question
when a missing answer changes the audience, intended behavior, scope, destination
or safety of a procedure. Record the source of inferred answers so a reviewer can
correct them.

Capture the reader's role and prior knowledge, the task or question, document
intent, success condition, scope and target product version. Use the
[Diataxis compass](https://diataxis.fr/compass/) to distinguish learning,
performing a task, looking up information and understanding a concept. Other
intents, such as an ADR or release note, keep their own structure.

List available source material and its revision: code, specification, schema,
issues, tests, UI copy, expert notes and existing documentation. Identify the
destination and navigation, single-page or multipart structure, prerequisites,
access, environment, publication conventions, domain terms and review owner.
The [contract template](../templates/document-contract.md) keeps these answers
in one short record.

## Resolve uncertainty before drafting

Resolve facts that determine which behavior to describe or whether a procedure
can be executed safely. For example, an unknown deployment target blocks writing
production restart instructions. An unknown rationale can remain labeled
`Unverified: rationale awaiting maintainer review` in a draft explanation. Give
unresolved items an owner and a concrete evidence request. A polished sentence
must not disguise an assumption as verified behavior.

## Worked single-page contract

The [Text Workshop fixture](../examples/document-types/evidence/README.md)
provides `evidence/count_lines.sh`, which counts newline characters in a readable
regular file. Its prepared sample contains two newline characters.

| Field | Agreement |
| --- | --- |
| Reader and prior knowledge | Maintainer who can run a terminal command and has Bash 4.4 or later and wc available |
| Task and intent | Count newline characters in a text file; how-to |
| Success | Running the documented command against the fixture prints `2` |
| Scope and version | Local readable regular files; checked-out fixture revision |
| Evidence | Script argument checks, wc invocation and recorded fixture commands |
| Destination and structure | Existing tools guide; prerequisites, command, expected output and input errors |
| Environment and access | Repository checkout; read permission on the sample file |
| Terminology | `text file`, `newline count`, matching the fixture |
| Review | Tool maintainer checks behavior; editor checks clarity |

The literal command and expected value are useful because the task depends on
them. Link their checked-in source or test in the evidence register.

## Worked multipart tutorial contract

For the same fixture, a tutorial teaches a developer to predict the newline
count of complete and unterminated text. The reader can use a terminal but has
not inspected newline counts. The target is the fixture revision, with Bash 4.4 or later,
wc and cat available before starting.

1. Inspect and count the complete sample. Outcome: the command prints `2`, and
   the reader connects the displayed lines to their newline characters.
2. Inspect and count the unterminated sample. Outcome: the command prints `1`,
   and the reader can explain why its final visible line adds no newline.

Each page links backward and forward, states its starting files, and names its
observable outcome. The group uses read-only commands and ends with a link to the operational
how-to. The reviewer checks that the complete learning path
runs from a fresh checkout and that each page teaches one step in that path.
