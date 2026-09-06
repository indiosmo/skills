# Checking C and C++ Doxygen comments

The `doxygen-lint` command checks local comment style and supported declaration
contracts. Use it for changed source comments or recursively over a selected
source directory. The [adoption map](doxygen.md#enforcement-map) assigns each
upstream convention to a check or a review owner.

## Installation and invocation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) through the
project's approved setup. From this skill checkout, synchronize the committed
lock and run its tests:

```sh
uv sync --locked --project skills/documentation/tools/doxygen_linter
uv run --directory skills/documentation/tools/doxygen_linter pytest -q
```

From a consuming project's directory, point `--project` at the tool's absolute
location. Relative source and configuration paths resolve from the current
directory, so source selection remains in the consuming project:

```sh
uv run --locked --project /path/to/skills/documentation/tools/doxygen_linter doxygen-lint include src --format json
uv run --locked --project /path/to/skills/documentation/tools/doxygen_linter doxygen-lint --language c include/api.h
```

Replace `/path/to` with the checkout location. `--project` selects the Python
environment; `--directory` changes the working directory. Keep that distinction
when running the tool's own tests versus checking a consuming project.

The package pins tree-sitter 0.26.0, C grammar 0.24.2, C++ grammar 0.23.4 and
Pydantic 2.12.5 in `pyproject.toml`; `uv.lock` includes resolved packages and
hashes. Python 3.11 or newer is required. A first synchronization needs package
index access; record it as blocked when dependencies are unavailable.

## CLI and configuration

Inputs are one or more files/directories; directories are recursive. Defaults
include `.c`, `.h`, `.cc`, `.cpp`, `.cxx`, `.hpp`, `.hh`, `.hxx`, `.ipp`, `.tpp`.
Only `.c` selects C automatically. `--language c|cpp|auto` overrides this mapping.
`--extensions .c .h` restricts discovery to supported suffixes. Place positional
paths before `--extensions`, whose values consume following arguments.

`--exclude` adds a whole-path glob and can repeat. An explicit `--config` loads
TOML; unknown keys, rule IDs or extensions are errors. Configuration is supplied
deliberately, so different working directories have predictable behavior:

```toml
exclude = ["**/vendor/**", "**/generated/**", "**/.git/**"]
extensions = [".h", ".cpp"]

[severity]
DOX003 = "error"
```

Setting `exclude` replaces the default list. The defaults skip `vendor`,
`third_party`, `generated`, `.git`, `.venv` and `build` directory contents.
Review project-generated locations and add matching exclusions. Every matched
path emits a skipped record; generation markers inside files have ordinary
source semantics. All symbolic links are skipped, including directory cycles
and explicit file paths through a symbolic-link ancestor. Special files such as
FIFOs produce blocked coverage before any source read.
Duplicate paths are checked once. Source must be UTF-8 without NUL bytes; I/O,
decoding and syntax recovery errors produce blocked records. A directory with
zero selected source files is blocked. Unsupported explicit files are blocked;
other file types encountered during directory traversal are outside selection.

Every diagnostic has a stable rule identifier, path, one-based line/column,
severity, explanation, suggested correction and upstream source link. Columns
count Unicode characters, with tabs counting as one character. The command
provides `--format text|json`, `--catalog` and `--version`. JSON includes
`status`, `checked_files`, `diagnostics`, `coverage`, `review_required` and
`exit_status`. Text uses plain characters and retains correction text.

| Exit | Meaning |
| --- | --- |
| 0 | Selected mechanical checks satisfy the failure threshold; inspect coverage and review requirements |
| 1 | At least one diagnostic meets the failure threshold |
| 2 | Invalid invocation/configuration or a blocked input/check |

Rules default to warning. `--fail-on warning` fails on both warnings and errors;
`--fail-on error` preserves warnings in output while only errors fail the run.
A blocked result takes precedence over findings. Argparse invocation errors use
its native text and exit 2, even when JSON was requested. Automated consumers
should capture stderr as well as stdout.

## Rules and explicit coverage limits

Get the machine-readable definitions with `doxygen-lint --catalog`. DOX001-009
inspect comment form, known command prefixes, brief punctuation, details layout,
brief/details separation, parameter directions and prose, example delimiters and
inline code markup. DOX010 compares named function parameters and the empty
parameter paragraph. DOX011 compares named template parameters. DOX012 checks a
brief and return documentation for supported functions. Each `@return` needs a
nonempty description; each `@retval` needs a value and description. Review the
meaning against implementation evidence. Missing, extra and
duplicate parameter names are findings.

The tool recognizes paragraph commands and line-start custom aliases as tag
boundaries while retaining inline references in their prose sentence.
It walks real syntax trees, excludes literal comment delimiters and
associates only adjacent syntax siblings separated by whitespace. An intervening
ordinary comment, detached documentation or a macro declaration records a skip.
Trailing member comments use Doxygen's association and receive a skip rather
than attaching to the next method. Multiple declarators, function-pointer
variables, unnamed/variadic parameters, conversion operators and nested template
parameters receive scoped skips. Trailing or deduced return types skip return
checking. Recovered syntax blocks the file result and skips affected contracts;
well-formed comments elsewhere still produce findings.

The linter examines written syntax across preprocessor branches. Use the
project's Doxygen/compiler configuration for active-branch and macro semantics.
Cross-file declaration/definition correspondence, undocumented APIs, inferred
types and contract meaning retain their owners in the adoption map. Automatic
fixes are outside the command's scope; suggested corrections support a reviewed
source edit.

A suppression applies only to its documentation block and records its reason:

```cpp
/**
 * @brief Preserve upstream title
 * doxygen-lint: disable=DOX003 -- Match the externally specified title.
 */
int title;
```

Comma-separated IDs must be known and the ` -- ` reason must be nonempty.
Invalid suppressions are blocked. The suppression line is tooling metadata;
place it where the project's Doxygen configuration permits such internal notes,
or prefer an external exclusion when modifying upstream source is inappropriate.

## Parser choice and reproducible evidence

The implementation uses tree-sitter comment extraction and declaration structure,
then applies local rules to the exact source slices. This adds syntax evidence
without requiring a buildable consuming project. Python bindings expose node
positions and grammar packages as dependencies: see [py-tree-sitter](https://tree-sitter.github.io/py-tree-sitter/).
Compiler-backed tooling can resolve richer semantics but requires the correct
[compilation database](https://clang.llvm.org/docs/JSONCompilationDatabase.html).
Use Doxygen generation for the rendering and symbol checks described in its
[warning configuration](https://www.doxygen.nl/manual/config.html).

Scores are local engineering judgments, 1 unfavorable to 5 favorable, equal
weights. Reversibility measures replacement cost; blast radius measures changes
needed in consuming projects. The candidate must first satisfy accurate comment
extraction and supported declaration association on the fixture inventory.

| Approach | Complexity | Performance | Reversibility | Blast radius | Maintenance | Ergonomics | Testability | Coupling | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Doxygen diagnostics alone | 5 | 3 | 5 | 4 | 5 | 4 | 4 | 3 | 33 |
| Custom lexical scanner/regex | 3 | 5 | 4 | 5 | 2 | 5 | 4 | 5 | 33 |
| Tree-sitter plus local checks | 4 | 5 | 4 | 5 | 4 | 5 | 5 | 4 | 36 |
| Clang semantic tooling plus local checks | 2 | 3 | 3 | 3 | 3 | 2 | 4 | 2 | 22 |

Doxygen alone lacks the house-style diagnostics; lexical-only extraction does
not meet the association gate. A fully correct C/C++ lexer plus declaration
parser would duplicate established grammar work. Clang is viable when semantic
coverage justifies build coupling. Tree-sitter meets the selected checks with
explicit boundaries and is the minimum sufficient choice for this tool.

Run the experiment from the skills repository root:

```sh
uv run --directory skills/documentation/tools/doxygen_linter python benchmarks/parser_probe.py
```

On 2026-09-06, the representative C++ fixture produced nine naive regex block
matches, including two strings, and seven tree-sitter documentation comments at
lines 1, 6, 13, 20, 26, 36 and 39. Clang accepted the fixtures under C11, C17,
C++17 and C++20. Its `-Wdocumentation` check accepted the planted house-style
defects with no warnings, demonstrating the need for the local rules. Adding a missing
generated include made Clang exit 1; tree-sitter still parsed written syntax.
These results justify the boundary, not a claim of universal C++ conformance.

The directory probe checked 500 copies, 459,000 bytes, in 0.204 seconds on this
Linux workspace, excluding corpus creation and Python startup. It found zero
style findings and 500 explicit macro-association skips. This is a small repeated
fixture corpus, not a production throughput guarantee; benchmark the target
project when its size or syntax differs materially.

The fixtures exercise C and C++, strings/raw strings, multiline comments,
templates, overloads, callbacks, default arguments and macros. Regression tests
also cover Unicode/CRLF positions, exclusions, symlinks, malformed input,
suppressions and CLI status. Review [tests](../tools/doxygen_linter/tests/)
alongside the catalog when extending the scope. Keep grammar versions, source
links, fixtures and the coverage map synchronized.
