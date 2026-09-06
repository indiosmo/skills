# Documentation skill acceptance results

The assembled replacement was verified on 2026-09-06. These results establish
implementation and fixture coverage. Human publication and factual approvals
for documents produced with the skill retain their named reviewers and statuses.

## Automated verification

Run commands from the skills repository root after provisioning the documented
tool dependencies. The HTTP fixtures require permission to use loopback sockets.

| Command | Result |
| --- | --- |
| `uv run --project skills/documentation/tools/doxygen_linter --frozen pytest skills/documentation/tools/doxygen_linter/tests -q` | 95 passed |
| `uv run --project skills/documentation/tools/validation --frozen pytest skills/documentation/tools/validation/tests skills/documentation/tests/validation -q` | 19 passed |
| `uv run --project skills/documentation/tests/environment --frozen pytest skills/documentation/tests/environment skills/documentation/tests/acceptance -q` | 80 passed |
| `uv run --project skills/documentation/tests/environment --frozen pytest skills/documentation/tests/style-links -q` | 42 passed |
| `uv run --project skills/documentation/tools/doxygen_linter --frozen ruff check skills/documentation` | Passed |
| Skill frontmatter/format validator | Passed |
| Pinned ShellCheck on Vale setup and example counter | Passed |
| Diff whitespace check | Passed |

Total: 236 automated tests. Each native-tool negative fixture asserts detection
of its planted defect, so a passing suite includes verified failures of bad input.
The tool READMEs document manual invocation and their independent test commands.
The final lychee package sweep checked SKILL.md, references, templates and tool
READMEs: 241 links successful, zero errors, zero exclusions. It followed three
redirects. Local resource tests also cover completed document-type examples.

## Authored outputs and reference usability

Independent authoring/review runs exercised a multipart tutorial, a skeptical
final review with a corrected clean pass, and bounded history with drift and
actual neighboring-page review. Five assertions per case passed for the
replacement: 15/15. The original skill met 11/15; its substantive results were
also strong, with differences mainly in exact findings, quotations and explicit
review records. Three cases with one run each are acceptance observations,
rather than a statistical performance claim. Execution time and token metrics
were unavailable. The replacement's multipart output was revalidated after tool
integration, so the comparison concerns final artifacts.

An additional README-update exercise used accepted specification, proposed issue,
schema, actual code, CLI text, test manifest, attributed fixture notes, obsolete
documentation, style guidance and inaccessible rationale. It separated proposed,
intended, observed and historical claims, verified seven runtime cases, and
preserved source hashes. Unverified release/compatibility claims stayed in the
review record. Native git log/diff commands were separately exercised on a real
read-only repository range; the synthetic history covered mixed commits,
deduplication and full reverts.

Standalone review of the contract, evidence, README and linter references found
them usable without SKILL.md. The reviewer completed an empty-file how-to outline
using the base references directly. All twelve document intents in the examples
index were assessed against their templates and reader outcomes. Multipart
navigation and initial state were checked. A missing Bash minimum in the worked
contract was corrected. The source-comment route was exercised through native
style/generation fixtures and the complete consuming-project validation workflow.

## Audit corrections and retained limits

The independent tool audit exposed and resolved parameter/verbatim masking,
empty return documentation, zero-input/all-excluded link checks and a working-
directory mismatch. Additional review resolved special-file discovery, symlink
ancestor handling, Doxygen tag boundaries and non-function brief-check coverage
wording. Regression tests or direct reproduced checks verify these corrections.

- C11/C17 and C++17/C++20 are the exercised linter baseline. Unsupported syntax,
  macro semantics, cross-file relationships and API meaning retain explicit
  coverage or review owners.
- Vale's tested C/C++ extensions are listed in its reference; `.hxx` remains
  unchecked by that native comment configuration.
- Native HTML assertions verify structure, navigation, symbols and assets.
  Browser layout and client-side diagrams need the consuming project's visual
  review when applicable.
- Deliberately skipped checks and within-tool exclusions remain visible. A native
  zero status is interpreted with its selected inputs and coverage, and human
  review status is recorded separately.
- Fictional decisions, release records and expert notes in examples are labeled
  as training evidence. They establish no real release or human approval.

The [acceptance rubric](README.md) and tool fixtures define the regression scope
for future maintenance. Re-run affected tests and review the relevant source,
reference, routing and examples together when that scope changes.
