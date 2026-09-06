# Doxygen comment linter

`doxygen-lint` checks C and C++ documentation comments against the adopted
[micro-os-plus style](https://micro-os-plus.github.io/develop/doxygen-style-guide/).
It finds local formatting defects and mismatches between supported function or
template declarations and their parameter documentation. Authors can run it on
one file or recursively over source directories; CI can consume its JSON report.

## Install and run

Prerequisites are Python 3.11 or newer and
[uv](https://docs.astral.sh/uv/getting-started/installation/). In this directory:

```sh
uv sync --locked
uv run doxygen-lint --version
uv run doxygen-lint tests/fixtures/representative.c
```

From the consuming project's directory, substitute this tool's absolute path:

```sh
uv run --locked --project /path/to/documentation/tools/doxygen_linter doxygen-lint include src --format json
uv run --locked --project /path/to/documentation/tools/doxygen_linter doxygen-lint --language c include/api.h
```

`--project` selects the environment while preserving your working directory.
Relative source/configuration paths therefore refer to the consuming project.
The committed lock pins dependencies and hashes; initial synchronization needs
package-index access.

## How it works

Tree-sitter parses written source and locates real comments, including comments
near templates and overloaded functions. The linter preserves source offsets,
removes comment decoration, protects example payloads, checks local style, and
compares parameter tags with adjacent supported declarations. It reports one-based
line/column locations in the original file. Columns count Unicode characters.

The [rule catalog](src/doxygen_linter/catalog.py), also available through
`uv run doxygen-lint --catalog`, names all 12 checks and their upstream sources.
The [adoption map](../../references/doxygen.md) explains the review owners for
every upstream convention. The [design and CLI reference](../../references/doxygen-linter.md)
contains parser comparisons, supported syntax, performance evidence and detailed
configuration semantics.

## Configuration and results

Supply an explicit TOML file with `--config lint.toml`:

```toml
exclude = ["**/vendor/**", "**/generated/**", "**/.git/**"]
extensions = [".h", ".cpp"]

[severity]
DOX003 = "error"
```

The file replaces the listed defaults; `--exclude` adds globs. `.h` defaults to
C++, and `--language c` selects C explicitly. Unknown keys, extensions and rule
IDs are errors. `--format text` is the default; `--format json` supplies status,
diagnostics, coverage records and remaining review requirements. Each diagnostic
includes rule, path, location, severity, explanation, correction and source link.

Exit 0 means the selected mechanical checks satisfy the failure threshold;
exit 1 means findings meet it; exit 2 means invocation, configuration or source
validation is blocked. The default `--fail-on warning` includes warnings and
errors; `--fail-on error` retains warnings in output without failing on them.
Always inspect skipped coverage and human review requirements, including on
exit 0. CLI argument errors use argparse's native stderr text.

## Limits and verification

The fixture-supported baseline is C11/C17 and C++17/C++20. UTF-8 source is
required. Symlinks and excluded files are recorded as skipped. Invalid encoding,
NUL bytes, unreadable files, missing inputs and syntax recovery produce blocked
results. Macros, detached/trailing comments and unsupported declaration shapes
produce scoped skips. Preprocessor configuration, cross-file relationships and
API meaning need the consuming project's Doxygen/compiler checks and review.
Suggested corrections are applied through a reviewed source edit.

Run tests and the reproducible parser/performance experiment from this directory:

```sh
uv run pytest -q
uv run ruff check .
uv run python benchmarks/parser_probe.py
```

Tests include a valid and invalid case for every rule, literal comment delimiters,
templates, overloads, callbacks, macros, exclusions, suppressions, malformed input
and exact diagnostic locations. The probe uses `clang++` when available and
reports its absence explicitly.
