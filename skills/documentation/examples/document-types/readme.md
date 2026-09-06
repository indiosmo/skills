# Text Workshop

Text Workshop is a fictional practice project for exploring newline counts in
small text files. A Bash command and prepared samples let terminal users connect
file contents to an observable result.

## Get started

Use Bash 4.4 or later and wc. Open a terminal in this document's directory and run:

```bash
bash evidence/count_lines.sh evidence/sample.txt
```

The command prints a count of 2. The [tutorial](tutorial.md) guides a first
experiment; experienced users can use the [how-to](how-to.md).

## How it fits together

The counter validates its input and passes its contents to wc. Prepared samples
make the results repeatable. Consult the [reference](reference.md) for the
command contract and the [explanation](explanation.md) for newline semantics.

To add an exercise, add a sample with known bytes and verify its expected count.
The [operational check](runbook.md) helps a coordinator assess sample readiness.
The [decision record](adr.md) explains the prepared tool choice.
