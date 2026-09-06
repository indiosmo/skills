# Linter architecture

The linter uses one Python module per rule, an explicit registry, and shared
comment preparation. This guide explains the execution boundaries and extension
contract for maintainers familiar with Python and the [tool usage](README.md).

## Design evidence

The following open source designs informed the architecture:

| Project | Relevant design | Use here |
| --- | --- | --- |
| [Ruff](https://docs.astral.sh/ruff/contributing/#example-adding-a-new-lint-rule) | Rule files contain violation metadata and check functions; analysis stages invoke the appropriate checks. | Keep each rule's metadata and implementation together. |
| [clang-tidy](https://clang.llvm.org/extra/clang-tidy/Contributing.html) | Registered check classes use AST matchers or preprocessor callbacks and emit diagnostics. | Separate source analysis from rule selection and reporting. |
| [ESLint](https://eslint.org/docs/latest/contribute/architecture/) | Command handling, source representation, rule execution, and rule testing have distinct modules. | Give the runner and individual checks separate test boundaries. |
| [Pylint](https://pylint.pycqa.org/en/latest/development_guide/how_tos/custom_checkers.html) | Raw, token, and AST checkers receive suitable inputs; visitor methods support traversal state. | Prepare declaration facts for checks that inspect function or template contracts. |
| [Flake8](https://flake8.pycqa.org/en/latest/plugin-development/registering-plugins.html) | Package entry points register external checks and reporting plugins. | Treat external distribution as the reason to introduce plugin discovery. |
| [markdownlint](https://github.com/DavidAnson/markdownlint/blob/main/doc/CustomRules.md) | Rules combine metadata with a function receiving parsed input and a diagnostic callback. | Use small functions over shared documentation context. |

These are adaptations to this tool's comment-oriented workload. In particular,
markdownlint's [explicit built-in registry](https://github.com/DavidAnson/markdownlint/blob/main/lib/rules.mjs)
provides a concrete example of readable registration at a larger rule count.

The scores below are subjective applicability judgments for this tool, from 1
(least suitable) to 5 (most suitable). For costs and risks, higher scores mean
lower cost or risk. Performance scores concern expected dispatch overhead and
shared preparation, rather than measured runtime differences.

| Criterion | Function registry | Visitor classes | Dynamic plugins |
| --- | ---: | ---: | ---: |
| Complexity | 5 | 3 | 2 |
| Performance | 5 | 4 | 3 |
| Reversibility | 5 | 4 | 3 |
| Blast radius | 5 | 4 | 3 |
| Maintenance cost | 5 | 3 | 2 |
| Ergonomics | 5 | 3 | 3 |
| Testability | 5 | 4 | 3 |
| Coupling | 5 | 3 | 3 |

The function registry fits checks that consume prepared comment facts. Visitor
classes become useful when checks track nested traversal state. Dynamic discovery
becomes useful when rule authors distribute independently installed packages.

## Execution and module map

The execution sequence is source parsing, comment preparation, registered checks,
and source-level reporting. The command-line tool handles file discovery, configuration, output
formatting, and exit status.

| Module | Responsibility |
| --- | --- |
| [parsing.py](src/doxygen_linter/parsing.py) | Parse C/C++ with Tree-sitter, associate documentation comments with declarations, and extract declaration syntax. |
| [comments.py](src/doxygen_linter/comments.py) | Remove decoration, mask examples, recognize tags, and preserve comment character offsets. |
| [context.py](src/doxygen_linter/context.py) | Prepare `CommentContext` and `DeclarationContext`, including scope-specific analysis skips. |
| [models.py](src/doxygen_linter/models.py) | Define rule metadata, findings, skips, diagnostics, and coverage records. |
| [rules/](src/doxygen_linter/rules/) | Implement each lint type in its own module. |
| [registry.py](src/doxygen_linter/registry.py) | Register implementations with metadata and analysis scope; validate unique identifiers. |
| [catalog.py](src/doxygen_linter/catalog.py) | Derive the public rule catalog from registered metadata and describe review coverage. |
| [checks.py](src/doxygen_linter/checks.py) | Execute rules, apply suppressions and severity, translate offsets, and order diagnostics. |
| [cli.py](src/doxygen_linter/cli.py) | Validate inputs and configuration, run the linter, and produce reports. |

`prepare_comment()` runs once per documentation comment. Its context contains
undecorated text, example-masked text, parsed tags, example findings, and declaration
facts. The prose field additionally masks inline code and valid suppression
directives. Masking
preserves character positions so checks can report offsets into the original
comment. DOX008 yields the example syntax findings recorded during normalization;
the same recognition pass identifies payloads that other checks treat as examples.

General analysis skips identify `comment`, `function`, or `template` scopes.
The runner derives each coverage record's rule identifiers from registrations in
those scopes. Registering another function check therefore includes it in coverage
for unsupported function analysis. Individual checks can also yield specific skips.
The runner invokes function and template checks when the corresponding declaration
node exists. Comment checks run for every documentation comment.

## Rule contract

Each module exports `RULE: Rule` and a generator with the contract
`check(context: CommentContext) -> Iterator[Finding | Skip]`. A check that yields
only findings can annotate its return as `Iterator[Finding]`.

- `Rule(identifier, description, correction, section)` supplies catalog and
  diagnostic metadata. `section` identifies an anchor in the adopted style guide.
- `Finding(offset=0, explanation="")` describes a violation. `offset` is a
  zero-based character offset into the original comment. An empty explanation
  selects the rule's description.
- `Skip(reason, suffix="")` records coverage requiring review. A suffix identifies
  a narrower part of the rule's coverage when needed.
- `RegisteredRule(metadata, check, scope="comment")` binds the contract to an
  analysis scope. Function checks use `"function"`; template checks use `"template"`.

The runner attaches the rule identifier, path, correction, source link, configured
severity, and one-based source location. It suppresses requested findings after
validating the directive and sorts diagnostics by line, column, and rule identifier.
Coverage records preserve analysis and rule-specific skips for review.

## Add a lint type

1. Create `src/doxygen_linter/rules/<descriptive_name>.py`. Define its `RULE`
   metadata and `check` generator. Follow
   [brief_period.py](src/doxygen_linter/rules/brief_period.py) for a prose check or
   [function_parameters.py](src/doxygen_linter/rules/function_parameters.py) for
   a declaration check with coverage skips.
2. Import the module in `registry.py` and add a `RegisteredRule` to
   `REGISTERED_RULES`, choosing its scope. The catalog derives the new entry from
   this registration. Duplicate identifiers raise `ValueError`.
3. Add `tests/rules/test_<descriptive_name>.py`. Use the `comment_context` fixture
   from [conftest.py](tests/rules/conftest.py) to parse one documentation comment,
   call the rule directly, and assert findings or skips. Cover valid input,
   violations, relevant syntax boundaries, and literal examples.
4. Exercise integration behavior through
   `lint(source, path, language, severities=None, *, rules=REGISTERED_RULES)`.
   Supply a small `rules` sequence to test registration, suppression, locations,
   severity, and coverage independently. Add command-line tests for changes to public
   configuration or output behavior.
5. Run the following commands from this tool's directory. The suite checks rule
   behavior alongside the public command-line contract.

```sh
uv run pytest -q
uv run ruff check .
uv run doxygen-lint --catalog
```
