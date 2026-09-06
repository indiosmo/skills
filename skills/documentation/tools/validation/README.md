# Documentation validation runner

`documentation-validate` executes a consuming project's ordered checks and writes
a JSON evidence record. It suits projects that have native lint/build commands
but need one report containing pass, fail, skipped and blocked outcomes, tool
versions, checked scope and native diagnostic logs.

## Install and run

Provide Python 3.11 or later and uv. From any working directory:

```sh
uv sync --project "$documentation_skill/tools/validation" --frozen
uv run --project "$documentation_skill/tools/validation" --frozen documentation-validate ./documentation-checks.toml --skill "$documentation_skill" --output "$validation_output"
```

Set `documentation_skill` to the absolute installed skill directory and
`validation_output` to a fresh absolute scratch directory. Run from the consuming
project root, or set `--project` explicitly. The manifest path is resolved from
the invocation directory. `--version` prints the runner version. Tool binaries,
project dependencies and assets are prepared with their existing setup commands;
the [validation workflow](../../references/validation.md) gives the order.

## How it works

The runner validates a TOML manifest, checks that dependencies precede each check,
then executes argument arrays sequentially with the specified working directory.
It substitutes `{project}`, `{skill}` and `{output}` literally in command arguments,
working directories and optional standard input. Commands execute directly through
Python's subprocess API, preserving literal shell metacharacters in arguments.

Each executed check first probes its version, then runs its native command. The
runner combines native stdout and stderr in a named log and records its path;
source locations and tool-specific JSON remain in that log. A failed prerequisite
skips its dependents, while independent checks still run. The final record is
written to `report.json` and printed as JSON. Each run should use fresh output so
the files retain one invocation's evidence.

## Manifest

```toml
[[checks]]
name = "site"
scope = "mkdocs.yml navigation and selected docs"
command = ["mkdocs", "build", "--strict", "--site-dir", "{output}/site"]
version_command = ["mkdocs", "--version"]
working_directory = "."
timeout_seconds = 60
```

`name`, `scope`, `command` and `version_command` are required. Names use lowercase
letters, digits and hyphens, starting with a letter. Optional `depends_on` names
earlier checks that must pass. `skip_reason` explicitly leaves a check unexecuted;
use it for a documented scope or environment limit. Optional `stdin` supplies
literal standard input, for example a Doxygen output override. Optional
`blocked_exit_codes` identifies native exit codes that represent an incomplete
check, such as the Doxygen linter's status 2. Unknown fields, duplicate names and
forward or missing dependencies reject the manifest before execution.

Use the [complete fixture manifest](../../tests/validation/fixture.toml) as a worked
example, then replace its fixture commands with the consuming project's commands.
Review executable paths, side effects and output paths in that manifest as code.
Keep credentials in the project's approved environment mechanism; record commands
and logs without secrets. Timeout applies separately to the version probe and
the command. It terminates the direct process; project commands that spawn
detached services need their own lifecycle and cleanup controls.

## Outcomes and diagnostics

| Observation | Status |
| --- | --- |
| Native command exits 0 | pass for the recorded command scope |
| Native command exits nonzero | fail, or blocked when declared in `blocked_exit_codes` |
| Missing executable/directory, permission failure, timeout or failed version probe | blocked |
| Explicit reason or prerequisite did not pass | skipped, with its reason |

Exit status is 2 if any check is blocked, otherwise 1 if any fails, otherwise 0.
The report's `complete` field is true only when every declared check passes. A
zero exit status with skipped checks is an incomplete scoped run. Existing CI can
require `complete` as a separate gate when all declared checks are mandatory.
Malformed manifests or unwritable output produce a `blocked:` stderr diagnostic
and status 2; a report cannot be promised when its destination is unwritable.

Inspect native reports for within-tool exclusions, unsupported syntax and network
limits. A native exit code cannot establish that all links or source constructs
were checked. Preserve those details in the human
[validation report](../../templates/validation-report.md). Tool-specific diagnostics
retain their original source paths and lines; use those to correct the source and
rerun the check and affected dependents.

The fixture manifest demonstrates a native coverage gate: `lychee --dump-inputs`
records the input inventory, lychee writes a separate JSON report, and `jq -e`
checks that its expected link scope contains a successful check. Empty selections
and selections with only excluded links produce blocked verification. Inspect
remaining exclusions separately; a successful local target establishes only
that target's coverage. Projects adapt this expectation to their selected input.

## Tests

From the skills repository root:

```sh
uv run --project skills/documentation/tools/validation --frozen pytest skills/documentation/tools/validation/tests skills/documentation/tests/validation -q
```

Runner tests cover ordered execution, diagnostics, literal arguments, failures,
skips, timeout, missing tools, declared blocked statuses and invalid manifests.
The integration suite copies the environment fixture into a temporary consuming
project and invokes the CLI there through its installed uv entry point. It runs
Vale, the custom linter, Doxygen, MkDocs, lychee and C++ compilation/execution,
including a planted defect for each validation stage. It keeps external-link
execution explicitly skipped for the offline fixture run. Empty-selection and
all-excluded cases assert blocked verification. Provide Doxygen, jq, a C++
compiler and the prepared Vale assets; MkDocs and lychee use the locked
environment fixture project.

For module responsibilities, design rationale and extension steps, read the
[architecture guide](ARCHITECTURE.md) and [decision matrix](architecture-decision.html).

Run linting and type checking from the skills repository root using its locked
development environment:

```sh
uv run --frozen ruff check skills/documentation/tools/validation
uv run --frozen pyright skills/documentation/tools/validation
```
