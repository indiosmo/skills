# Fixture-v2 evidence

- The argument contract and current test specify UTF-8 input.
- The documentation tree contains `formats.md`; `formats-old.md` was removed.
- The executable empty-file test expects stdout `0` and exit status 0.
- The CLI help and domain glossary name the tool `counter`.
- The parent guide still says empty files raise an error; its claim conflicts
  with the target-version test and contract.
- The design note is inaccessible. No evidence establishes a data-loss guarantee.
- The command accepts exactly one local path, matching the original guide.
