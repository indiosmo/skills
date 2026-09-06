# Target-version source packet

Target: the checked-in Text Workshop fixture; review date 2026-09-06. All labeled
roles and historical records in this packet are fictional exercise evidence.

## Accepted specification SPEC-2

The counter accepts one path to a readable regular file and prints its newline
count. The prepared samples demonstrate complete, empty and unterminated text.
The accepted contract specifies no binary-record decoder or Python runtime.

## Proposed issue ISSUE-8

Status: open proposal, target undecided. Request support for two files and a
binary-record decoding mode. No implementation or release approval accompanies
this proposal.

## Invocation schema SCHEMA-2

```json
{"input_paths": {"type": "array", "minItems": 1, "maxItems": 1, "items": {"type": "string"}}}
```

The schema expresses argument cardinality. Filesystem availability is checked
by the implementation.

## Implementation CODE-2

Inspect [the actual counter](../../../examples/document-types/evidence/count_lines.sh).
Its argument-count check and readable-regular-file check establish error paths;
its wc invocation counts newline characters.

## UI/CLI text UI-2

The executable usage string is `Usage: count_lines.sh TEXT_FILE`. Compare it
with the script's actual output before using it as reader-facing evidence.

## Tests TEST-2

[The executable command manifest](../../../examples/document-types/commands.json)
contains prepared counts and error cases. Run selected cases before claiming
observed outcomes; expected data alone represents the test contract.

## Expert note SME-1

The fictional workshop coordinator states: preserve unexpected samples and
escalate a readiness mismatch to the coordinator. The note applies to the
prepared workshop and supplies operational intent. It provides no compatibility
or release evidence.

## Existing documentation DOC-1

`readme-before.md` is from an obsolete draft. Its two-input and released-decoder
claims conflict with SPEC-2, SCHEMA-2, CODE-2 and ISSUE-8.

## Style guide STYLE-2

Use the [house style](../../../references/house-style.md) and actual tool/domain
names. Avoid changing identifiers while editing prose.

## Inaccessible rationale ADR-0

A historical rationale note is unavailable; the packet supplies no URI or copy.
Record this missing evidence explicitly. No supplied source supports a Python
3.15 compatibility rationale. Its absence does not block correcting current
argument usage and providing the verified prepared example.
