# Expected drift findings

| Exact text | Class | Evidence and impact | Proposed correction |
| --- | --- | --- | --- |
| The default input encoding is ASCII. | Factual mismatch | UTF-8 contract/test; reader may prepare wrong input | State UTF-8. |
| Read [input formats](formats-old.md). | Broken link | Removed file; reader cannot reach the reference | Link `formats.md` and validate the destination. |
| For an empty file, the command prints `1`. | Stale example | Empty-file test expects `0`; verification gives a false alarm | Replace expected output with `0` and rerun the example. |
| The processor accepts the input path. | Terminology change | CLI/glossary use counter; competing terms confuse readers | Use counter. |
| The parent guide says that empty files produce an error. | Contradiction | Parent conflicts with current test; reader gets incompatible advice | Correct parent to return `0` and link the empty-file example. |
| The design eliminates all possible data loss. | Unverifiable claim | Inaccessible rationale and no guarantee evidence | Remove the guarantee or keep it explicitly unverified in review material pending evidence. |
| The command reads one local input file. | Unchanged | Current argument contract; claim remains valid | Retain it. |
