# Naming package checks

Run from the skill repository root using its existing uv development environment.
The test dependencies are pytest, Markdown, PyYAML, and the pinned lychee binary.
The implementation fixtures use the Python standard library; the local rename
fixture's own tests additionally use pytest.

## Assembly and release commands

```sh
uv run --no-sync pytest -q skills/naming/tests/test_package.py skills/naming/tests/test_fixture_contracts.py -k 'not release_required_resources'
uv run --no-sync python skills/creating-skills/scripts/quick_validate.py skills/naming
uv run --no-sync ruff check --config 'include=["skills/naming/**/*.py"]' skills/naming/tests/test_package.py skills/naming/tests/test_fixture_contracts.py
uv run --no-sync pyright skills/naming/tests/test_package.py skills/naming/tests/test_fixture_contracts.py
```

The assembly command requires the guide, entry point, examples, templates,
evaluation definitions, and trusted outcome checker. Missing resources fail with
their paths. The final release inventory also requires the durable evaluation
results; run the full release checks after those results are recorded:

```sh
uv run --no-sync pytest -q skills/naming/tests
```

Explicit file scopes select naming checks despite the repository's default
documentation-tool selection. Set `UV_PROJECT_ENVIRONMENT` to the existing
environment when running from a relocated tree. Tests invoke its Python and
lychee executables directly, with bounded subprocess timeouts.

## What the checks establish

`test_package.py` checks the required artifact inventory, parses entry-point
metadata through the creating-skills validator and PyYAML, checks reference
reachability from navigation and entry-point links, and bounds entry-point size.
Long Markdown resources expose a contents section. Durable files are checked for
temporary build dependencies and machine-specific paths.

Local Markdown and HTML links, including fragments and sibling destinations, use
the documentation skill's pinned lychee configuration in offline mode. Controlled
temporary inputs establish detection of missing resources and broken fragments.
Empty link selection and missing selected files fail before execution. The full
package pass requires positive checked-link coverage. External URLs appear as
excluded in its JSON report; online reachability requires the documented
[link-validation workflow](../../documentation/references/link-validation.md).

The supported skill tree supplies sibling [documentation](../../documentation/SKILL.md),
[design](../../design/SKILL.md), [decision-matrix](../../decision-matrix/SKILL.md),
[glossary](../../glossary/SKILL.md), [creating-skills](../../creating-skills/SKILL.md),
and [verification-before-completion](../../verification-before-completion/SKILL.md)
resources. Local links resolve against that tree. Installation checks exercise the selected
dependencies after relocation; standalone distribution needs the same resources.

Evaluation source definitions use `skill_name` and an `evals` list, with unique
positive `id` values, `prompt`, `expected_output`, `files`, and `expectations`.
Input file paths resolve from the naming skill root and select files under
`tests/fixtures/`. Self-contained prompts can have an empty `files` list; the
evaluation set must include fixture-backed cases. Empty evaluation selection,
missing files, duplicate selections, and paths to evaluator material fail.
Expected outputs and expectations are grader inputs. Execution packets contain
the prompt and selected files; run metadata maps expectations to assertions.
Trigger definitions contain 20 distinct queries, balanced across positive and
negative trigger judgments.

`test_fixture_contracts.py` copies each fixture into a pytest temporary directory
and executes trusted assertions in a fresh Python process. Hashes before and
after execution establish preservation of packaged source files. Its contracts
cover subscription state selection, order, duplicates, object identity, immutable
records, single-pass input, retry-policy truth conditions and boundaries,
importing keyword callers, executable examples, independent same-spelling
symbols, public serialization, defaults, invalid inputs, schema, and existing
clients.

The [rename outcome checker](../evals/README.md) separately evaluates produced
rename checkouts against trusted evidence. Its tests exercise incomplete and
incorrect outputs. Naming quality, source fidelity, meaningful progressive
loading, and human judgments require the documented reviews alongside mechanical
checks.
