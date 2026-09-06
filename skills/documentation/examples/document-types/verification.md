# Text Workshop verification record

The checked-in examples were exercised on 2026-09-06 with GNU Bash 5.2.21 and
GNU coreutils wc 9.4. Run commands from this directory. The
[command manifest](commands.json) records repeatable invocations, expected
outputs and statuses for a runner to execute with a five-second timeout.

| Check | Observed result |
| --- | --- |
| bash -n evidence/count_lines.sh | Passed |
| Count sample.txt | 2 |
| Count empty.txt | 0 |
| Count unterminated.txt | 1 |
| Missing argument and extra argument | Usage diagnostic; status 2 |
| Missing file and directory input | Readable-regular-file diagnostic; status 1 |
| cat evidence/sample.txt | alpha and beta on separate lines |
| Byte inspection | sample.txt ends in newline; unterminated.txt ends in beta; empty.txt has zero bytes |
| ShellCheck via shellcheck-py 0.11.0.1 | Passed with -x --severity=warning |

Every executable block in the tutorial, multipart tutorial, how-to, README,
reference and runbook is represented by the count or inspection commands above.
Reference synopsis blocks describe syntax and have explicit placeholder text.
The activities read checked-in files and require no cleanup. Expected counts are
numeric; surrounding whitespace can vary with the installed wc.

The source establishes validation branches, while execution checks their
prepared examples. Permission-denied and mid-read failures were not injected.
This record establishes the local fixture results; other platforms require
their own checks. Human assessment of learning quality, operational usefulness
and the article's reasoning remains a review obligation.

ShellCheck was invoked from the skill repository with the pinned command:

```sh
uvx --from shellcheck-py==0.11.0.1 shellcheck -x --severity=warning skills/documentation/examples/document-types/evidence/count_lines.sh
```

## External guidance

The Diataxis quadrant pages, Google procedures and cross-reference guidance,
Write the Docs beginner's guide, ADR community page, Nygard's ADR article and
Keep a Changelog 1.1.0 were retrieved on 2026-09-06. They are linked from the
templates and base references where applicable.

Attempts to retrieve the POSIX wc page and GNU wc manual page failed through
the web tool. Command claims therefore use the checked-in source and observed
fixture results. This leaves broader wc portability claims unverified.

The release and decision records are explicitly fictional evidence for the
worked prose. They establish no real release, git tag or human approval.
