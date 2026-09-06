# Text Workshop counter reference

The fictional fixture command counts newline characters in one input file.
This page describes the checked-in [counter source](evidence/count_lines.sh).
The examples were verified on the environment in the [execution record](verification.md).

## Synopsis

```text
bash evidence/count_lines.sh TEXT_FILE
```

Run from this document's directory. Requires Bash 4.4 or later and wc.

## Input

| Argument | Required | Meaning and constraints |
| --- | --- | --- |
| TEXT_FILE | Yes; exactly one argument | Path to a readable regular file |

The prepared exercises use ASCII files. Paths containing spaces require shell
quoting. The script passes the file through standard input to wc.

## Output and status

A successful run prints the newline count and returns 0. Whitespace around the
number follows the installed wc implementation.

| Condition | Status | Diagnostic |
| --- | --- | --- |
| Argument count differs from one | 2 | Usage: count_lines.sh TEXT_FILE |
| Input fails the readable-regular-file check | 1 | Input must be a readable regular file. |

Failures during reading or counting retain the shell or wc diagnostic and status.

## Example

```bash
bash evidence/count_lines.sh evidence/sample.txt
```

The count is 2. Use the [how-to](how-to.md) to perform a count and the
[explanation](explanation.md) to interpret newline counts.
