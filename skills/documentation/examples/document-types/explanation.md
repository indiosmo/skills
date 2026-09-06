# How a final newline affects the count

Text Workshop's fictional exercises distinguish visible text from terminating
newline characters. The counter delegates counting to wc, so its useful model
is a sequence of newline boundaries.

## Compare the prepared inputs

The [sample](evidence/sample.txt) contains alpha, a newline, beta and another
newline. Its count is 2. The unterminated.txt fixture contains the same words
with one newline between them; its count is 1. Both display two words, but the
final boundary differs. The [verification record](verification.md) checks these
exact bytes and results.

An empty file contains zero newline boundaries and produces 0. These observations
explain the fixture's behavior on its prepared ASCII inputs.

## Why this model matters

When a task requires counting records, first establish the record format. In
this workshop, a newline boundary is the measured unit. Applying that count to a
different record format requires evidence that its boundaries match the metric.

The [decision record](adr.md) explains the tool choice. The
[how-to](how-to.md) gives the command for an existing file.
