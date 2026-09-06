# Compare the unterminated sample

The [previous page](01-complete-sample.md) produced a count of 2. If you arrived
directly, start with the [activity entry page](index.md). Keep using the parent
document-types directory and the prepared samples.

## Count the second sample

Run:

```bash
bash evidence/count_lines.sh evidence/unterminated.txt
```

The count is 1. The sample contains alpha, one newline and beta; beta has no
terminating newline.

## Repeat the comparison

Run the first command again:

```bash
bash evidence/count_lines.sh evidence/sample.txt
```

It still prints 2. You have compared two prepared inputs and observed the effect
of their different endings. The read-only activity leaves both files ready for
another attempt.

Read [how a final newline affects the count](../explanation.md) to connect the
observations to a model, or use the [how-to](../how-to.md) for an existing file.
