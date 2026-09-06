# Validation runner architecture

This guide explains `documentation-validate` 0.1.0 for maintainers adding checks
or outcome policies. The [usage guide](README.md) defines
the manifest and command-line contract. The [decision matrix](architecture-decision.html) records the trade-offs.

## Design and responsibilities

The runner applies two distinct validation policies: a version probe establishes
tool readiness, and a native command establishes its declared check outcome.
Each policy has a Python module and a corresponding test file. Vale, Doxygen,
MkDocs, lychee and example commands express their behavior through manifest
argument arrays and native configuration, as the [fixture](../../tests/validation/fixture.toml)
demonstrates. This makes wrapped commands and project-specific checks ordinary
manifest entries.

All module paths below are relative to `src/documentation_validation/`.

| Module | Responsibility |
| --- | --- |
| `configuration.py` | Validate `Check` and `Manifest`, enforce unique names and preceding dependencies, and resolve placeholders into `ResolvedCheck`. |
| `execution.py` | Execute arguments, working directory, timeout, and standard input through `Executor`. Retain diagnostics and return `ExecutionResult`. |
| `models.py` | Define report fields, check statuses and the immutable `ValidationOutcome`. |
| `validators/version.py` | Classify version-probe return codes and execution errors. |
| `validators/command.py` | Classify native return codes, execution errors, and declared blocked codes. |
| `validators/__init__.py` | Explicitly export the available policy functions as the static registration surface. |
| `orchestration.py` | Resolve checks, apply skips and dependencies, execute probes and commands, and collect results. |
| `reporting.py` | Aggregate outcomes, serialize JSON, and write the report. |
| `cli.py` | Parse arguments, load TOML, invoke validation, and produce command-line output and exit status. |
| `__init__.py` | Export the public Python interface and command-line entry point. |

Configuration flows into orchestration, which supplies resolved process inputs to
execution. Policy functions interpret `ExecutionResult` values and return
`ValidationOutcome` values. Reporting consumes the collected check records.
`validate(..., executor=...)` accepts an executor with the shared callable contract,
so orchestration tests can supply deterministic process results. Executors write
the supplied log path, including version text read by orchestration. Process tests
separately cover literal arguments, diagnostics, and failures.

The two policy functions have different inputs: command classification also accepts
blocked exit codes. Explicit exports and direct calls make that distinction
visible at registration and invocation. Shared process execution and result types
capture the repeated needs of both policies.

## Failure and evidence contract

An explicit skip takes precedence over prerequisites. A prerequisite with any
status other than `pass` skips its dependent. Independent checks continue in
manifest order. A successful version probe enables the native command. A failed
probe produces `blocked` and retains its version log. The reason contains the
execution error or `Version command failed`.

Native exit 0 means `pass`. Another return code means `fail`. Execution errors
and declared blocked exit codes take precedence and produce `blocked`.
Missing tools, inaccessible working directories, and timeouts become execution
errors. Native standard output and standard error share a named log. Timeout applies separately
to the probe and command and terminates the direct process.

The aggregate exit status is 2 for any blocked check, otherwise 1 for any failed
check, otherwise 0. `complete` requires every check to pass. Serialization retains
the JSON field names, indentation, and ASCII escaping. Configuration or output
errors produce a `blocked:` diagnostic on standard error and exit 2.

## Research and rationale

The following adaptations are design judgments based on primary documentation and
implementations consulted on 2026-09-06:

- [Linter architecture](https://eslint.org/docs/latest/contribute/architecture/)
  separates command-line output, engine orchestration, and rule behavior. Those
  boundaries fit this runner's reusable execution and outcome interfaces.
- [pre-commit's registry](https://github.com/pre-commit/pre-commit/blob/main/pre_commit/all_languages.py)
  names modules explicitly. Its [shared protocol](https://github.com/pre-commit/pre-commit/blob/main/pre_commit/lang_base.py)
  defines their contract. Explicit policy exports fit two differing signatures.
  Environment installation and language bootstrapping would add operational scope.
- [Ruff's contribution guide](https://docs.astral.sh/ruff/contributing/#example-adding-a-new-lint-rule)
  pairs individual rule modules with explicit registration and focused tests.
  That pattern fits policy ownership. Generated registries suit a larger rule set.
- [Sphinx's build phases](https://www.sphinx-doc.org/en/master/extdev/index.html#build-phases)
  make prerequisite order explicit. The ordered manifest expresses this runner's
  dependencies directly. Persistent build environments serve incremental builders.
- [MkDocs plugins](https://www.mkdocs.org/dev-guide/plugins/)
  combine validated configuration with lifecycle hooks. Strict configuration fits
  this tool. Package discovery and an event bus would add machinery to two direct
  policy calls. Native tools retain their own diagnostic and coverage settings.

## Add a validation policy

For another native tool, add a `[[checks]]` entry using the
[manifest reference](README.md#manifest). Set command, version probe, and scope.
Declare preceding dependencies and any native blocked exit codes. Add a fixture
that exercises the tool's successful result and a representative defect.

For a distinct outcome policy, create `validators/<policy>.py` and
`tests/validators/test_<policy>.py`. Define explicit typed inputs and return
`ValidationOutcome`. Test successful, failing, and blocked observations at this
boundary. Export the function in `validators/__init__.py` and call it at the
appropriate orchestration stage, with an orchestration test covering dependencies
and execution order. Run the [test suites](README.md#tests), linting, and type
checking. Compare command-line JSON, logs, and exit statuses for affected workflows.
