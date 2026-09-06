# Count newlines in a text file

Use the fictional Text Workshop counter to obtain a newline count for one local
file. You need Bash 4.4 or later, wc and read access to a regular file. Run commands
from this document's directory.

## Count the file

Run the following command for the prepared sample:

```bash
bash evidence/count_lines.sh evidence/sample.txt
```

For another file, replace evidence/sample.txt with its path and quote paths
containing spaces. The command prints the count and returns 0 on success.
The prepared sample prints 2.

## Resolve input errors

If the command prints "Input must be a readable regular file.", check the path,
file type and read access before retrying. If it prints the usage message,
supply exactly one file path. See the [reference](reference.md) for exit statuses
and the [explanation](explanation.md) for how a final newline affects the count.
