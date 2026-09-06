# Text Workshop evidence

Text Workshop is a fictional documentation fixture. Its source, sample bytes
and decisions are checked in here so authors can distinguish observed behavior
from invented product history. Commands run from the parent document-types
directory with Bash 4.4 or later and wc installed.

The [counter source](count_lines.sh) defines argument validation and invokes
wc to count newline characters. [sample.txt](sample.txt) contains alpha followed
by a newline and beta followed by a newline. empty.txt has zero bytes.
unterminated.txt contains alpha followed by a newline and beta without a final
newline. The [verification record](../verification.md) records observed results.

## Fictional product contract

The training coordinator maintains the fixture and is the escalation owner for
a changed or unreadable sample. Counting reads a single readable regular file
and prints its newline count. The supported demonstration uses the checked-in
ASCII samples. Usage errors return 2; rejected inputs return 1. A successful
count returns 0. The script delegates counting failures to wc.

The workshop's acceptance check requires sample.txt to produce 2. An unexpected
count means the coordinator must compare the sample with the reviewed checkout
before the exercise resumes. The operator preserves the input for investigation.

## Fictional decision record

On 2026-09-01, the training coordinator accepted using wc behind a small Bash
wrapper. The prepared environment already included Bash and wc. The coordinator
valued readable input validation and a simple invocation. Building a separate
counter was considered unnecessary for the prepared ASCII exercises. Supporting
environments without these tools requires separate preparation.

The ADR convention for this fixture uses descriptive filenames. The coordinator
approves decision changes; corrections retain a dated note, and changed decisions
use a new record with reciprocal supersession links.

## Fictional release evidence

The fixture uses illustrative release events rather than actual repository tags
or commits. The completed changelogs demonstrate prose structure; the separate
history-workflow acceptance fixture verifies real git history collection.

| Event | Revision | Date | Evidence and scope |
| --- | --- | --- | --- |
| F01 | 0.1 | 2026-09-01 | sample.txt and the manual wc exercise are the starting state. |
| F02 | 0.2 | 2026-09-02 | count_lines.sh is added, including explicit argument/input diagnostics; its checked-in source represents this event. |
| F03 | 0.2 | 2026-09-02 | tutorial.md and multipart-tutorial/ are added as learning paths. |
| F04 | 0.2 | 2026-09-02 | reference.md explains the wrapper's input and exit statuses. |

For this fictional release, the coordinator marks 0.2 released on 2026-09-02.
The evidence establishes these events only; broader compatibility, security,
performance and migration claims would need additional evidence.
