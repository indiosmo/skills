# A visible second line can change what you expect to count

By the Text Workshop example author, 2026-09-02.
This article addresses documentation authors choosing expected outputs for
terminal examples. The fictional fixture suggests a useful practice: inspect
the bytes that make an example's assertion true.

## One small observation

The workshop's two samples contain alpha and beta. One has a newline after each
word; the other has a newline only between them. The
[recorded checks](verification.md) produce counts of 2 and 1 respectively.

A reader can recognize two displayed words in each sample while expecting the
same line count. The command's measured unit provides the missing distinction:
it counts newline characters. The [explanation](explanation.md) connects that
unit to the fixture bytes.

## What the observation supports

For this example, checking the final newline is necessary to reproduce the
expected output. This supports keeping executable sample files alongside
documentation and testing the result after edits. The small observation does
not establish how every text-processing tool defines a line; that claim would
need evidence for each tool.

When choosing an expected output, identify the measured unit and verify the input
that produces it. The [fixture evidence](evidence/README.md) lets a reviewer
repeat this particular comparison.
