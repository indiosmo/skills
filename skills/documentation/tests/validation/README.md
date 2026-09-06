# Complete validation workflow acceptance

These tests invoke the installed validation CLI from a temporary consuming
project. The input project is copied from the environment fixture. Its parameter
tags receive explicit `[in]` directions so the complete Doxygen house-style
check applies to the baseline. The fixture manifest records all native commands,
dependencies, scope, version probes and the explicit offline skip.

From the skills repository root:

```sh
uv run --project skills/documentation/tools/validation --frozen pytest skills/documentation/tools/validation/tests skills/documentation/tests/validation -q
```

On 2026-09-06 the full command reported `17 passed in 13.50s` before the
empty-selection coverage gate was added. A fresh targeted integration run,
`uv run --project skills/documentation/tools/validation --frozen pytest skills/documentation/tests/validation -q`,
then reported `9 passed in 16.26s`, including the two new coverage cases.
These runs used the runner 0.1.0,
Vale 3.20.0 with Google 0.7.1, Doxygen linter 0.1.0, Doxygen 1.9.8, MkDocs 1.6.1,
lychee 0.24.2 and GCC 13.3.0. Python was 3.13.3.

| Scenario | Expected and observed evidence |
| --- | --- |
| Valid native workflow | All nine executed checks pass; external links remain skipped with a reason; CLI exits 0 and `complete` is false |
| Prose terminology defect | Vale fails on `DoxyGen` |
| Missing parameter direction | Doxygen linter fails on the source comment |
| Unknown symbol reference | Doxygen generation fails; dependent site and link checks are skipped |
| Missing page anchor | MkDocs strict build fails; dependent link check is skipped |
| Missing raw HTML target | lychee fails on the copied HTML link |
| Incorrect gain arithmetic | Example compiles and fails its runtime assertion |
| Unmatched input glob | lychee exits 0 with total 0; the native jq coverage check blocks verification |
| Nonempty input with only excluded links | lychee reports total 1, excludes 1 and successful 0; coverage is blocked |
| Ordered reporting | Records preserve command order, tool version, scope and source-located native log text |
| Explicit and prerequisite skips | Reasons remain visible; independent checks continue |
| Missing tool, timeout, blocked native status, version failure | Each produces blocked status and CLI aggregate status 2 |
| Invalid manifest | Empty manifests, duplicate names and forward/missing dependencies are rejected |
| Consuming-project CLI and literal arguments | Project defaults to invocation directory; shell-looking argument text remains literal |

The native negative cases assert that their owning stage fails, so the passing
test suite establishes defect detection rather than a clean negative fixture.
Native stdout and stderr remain in named logs under each temporary report
directory. The complete workflow integrates the source tools, generation and
examples; browser layout and live external URLs use their separate verification
procedures. Existing CI can run the same CLI command as local users and retain
the report and logs.
