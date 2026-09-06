# Validate a documentation change

Use the consuming project's checks to verify the selected page or related group.
Record the revision, changed inputs, existing configuration, command, working
directory, tool version and result with the
[validation-report template](../templates/validation-report.md). Review factual
support and example meaning alongside mechanical checks.

## Select scope and prepare tools

Inspect existing project commands and their dependency locks before invoking
tools. A wording edit usually starts with the changed Markdown or source comment
and its linked neighbors. A heading change adds incoming links; a symbol rename
adds source references, generated symbol consumers and site links. Changes to
navigation, configuration, shared terminology, snippets or generator dependencies
require the affected site or reference scope to be rebuilt. Record why each check
applies and why any check is skipped.

Use the project's approved versions and settings. The skill's baseline setup is:
Vale's [setup script](../assets/vale/setup.sh), the uv-managed
[Doxygen linter](../tools/doxygen_linter/README.md), the project's Doxygen and
MkDocs installation, and pinned lychee through the
[link-validation procedure](link-validation.md). The
[environment fixture](../tests/environment/README.md) provides a locked test
environment; its versions establish regression coverage, and consuming projects
retain their own generation setup.

## Run in dependency order

| Stage | Invocation and evidence |
| --- | --- |
| Prose and comment style | `vale --no-global --config=<project-config> --output=JSON <selected-paths>`; retain source locations and inspect false positives |
| Doxygen style | `uv run --project <skill>/tools/doxygen_linter --frozen doxygen-lint --format json <selected-sources>`; record findings and coverage |
| Generated API reference | Existing Doxygen command with temporary output; inspect signatures, overloads, parameters, examples and symbol links |
| Site build | Existing MkDocs command with `--strict` and temporary site output, after generated dependencies exist |
| Links | lychee source and built-site checks with appropriate root, index files and fragments; run external URLs online and record exclusions |
| Examples | Existing build/test targets or native compilation followed by assertions for the taught behavior |

Replace command placeholders with recorded absolute paths or project-relative
inputs. Set `documentation_skill` to the installed skill's absolute path when
using commands from its references. Preserve project configuration, including
relative inputs, plugins and filters. Follow the specific
[reference-generation](generated-reference-validation.md),
[MkDocs](mkdocs-authoring.md), [link](link-validation.md) and
[example](examples.md) procedures for detailed inspection and limits. Lint checks
are independent of generation unless project policy requires a preceding pass;
site generation depends on reference artifacts and built-link checks depend on
the site. Example execution depends on its setup or compilation.

## Repeat locally and in existing CI

Use an existing project orchestrator if it already captures the required record.
Otherwise the small [validation runner](../tools/validation/README.md) executes a
reviewed project manifest and saves native output plus JSON outcomes. Its
[scored decision matrix](../tools/validation/validation-decision.html) explains why
the reporting gap merits this optional adapter.

From the consuming project root, after setting the two absolute paths:

```sh
uv run --project "$documentation_skill/tools/validation" --frozen documentation-validate ./documentation-checks.toml --skill "$documentation_skill" --output "$validation_output"
```

An existing CI verification job can run exactly that command and retain
`report.json` plus its named logs as review artifacts. Use a fresh temporary output
directory per run. Adapt the [worked manifest](../tests/validation/fixture.toml)
to existing project commands and declare prerequisite checks with `depends_on`.
The fixture directs reference output inside its isolated copied project because
MkDocs consumes that path; production projects should use their existing
temporary-output mechanism. Keep native commands available for focused debugging.

## Interpret results and retry

Pass means the named command completed successfully for its stated scope. Fail
means it reported a finding or build/example error. Blocked identifies a missing
dependency, invalid setup, timeout or other prevented check. Skipped records a
deliberate omission or an unmet prerequisite. Retain the reason, owner and next
action for every incomplete check. A zero command status can still contain
excluded URLs or unsupported constructs; inspect tool coverage and native logs.

Establish the selected link inputs with `lychee --dump-inputs` before interpreting
its result. An unmatched glob can exit 0 with no checked files. The worked
manifest saves that inventory and a separate lychee JSON report, then uses native
`jq -e '.total > 0 and .successful > 0'` to verify this fixture's expectation of
checked links. A false predicate is blocked verification. An empty selection and
a nonempty selection whose links are all excluded both remain incomplete.
Inspect the inventory to distinguish a real page with no links from no selected
pages, and record an explicit scope decision for the former. Retain excluded
URLs as unchecked even when other links pass. The runner executes these native
checks and preserves their output; the manifest owns the coverage expectation.

Fix findings at their editable source location, then rerun that check and its
affected dependents. For an unavailable tool or source, preserve the actual
diagnostic and obtain the required environment. For transient network failures,
follow lychee's retry and classification procedure. Inspect existing warnings
separately from new findings; preserve project policy when deciding whether they
block the change.

Review generated content and example meaning after tooling passes. Record browser
and human observations explicitly. Keep final editorial findings and human review
status separate from the execution report so a passing build cannot imply factual
approval.

## Acceptance evidence

The [runner tests](../tools/validation/README.md#tests) exercise four result states
and preserved diagnostics. The integration fixture invokes the same installed
command from a separate consuming-project directory and runs the full native
sequence. Each planted prose, source-comment, generated-symbol, page-anchor,
built-link and arithmetic defect must make its owning stage fail; the offline
external-link check remains visibly skipped. The
[environment tests](../tests/environment/README.md) add direct rendering and
navigation coverage, and the link/style suites exercise their native tool rules.
