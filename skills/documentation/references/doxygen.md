# Writing and reviewing Doxygen comments

Use the [micro-os-plus Doxygen style guide](https://micro-os-plus.github.io/develop/doxygen-style-guide/)
as the shared reference for authors and reviewers. This page identifies enforcement
owners and the adaptations needed for C and C++ projects. Read the linked section
when changing that kind of comment; use the [linter guide](doxygen-linter.md) for
repeatable checks and [generation validation](generated-reference-validation.md)
for rendered API reference.

## Enforcement map

The rows cover every normative section and sample convention in the upstream
guide, inspected 2026-09-06. C means custom linter, D means Doxygen generation,
H means human review. Vale owns general prose style across these rows. Rule
definitions and diagnostic corrections live in the tool's [catalog](../tools/doxygen_linter/src/doxygen_linter/catalog.py)
and [positive/negative tests](../tools/doxygen_linter/tests/test_checks.py).

| Upstream section or convention | Owner |
| --- | --- |
| [Block comments; separate objects](https://micro-os-plus.github.io/develop/doxygen-style-guide/#--comments-instead-of-) | C DOX001; D/H association |
| [Command prefix](https://micro-os-plus.github.io/develop/doxygen-style-guide/#-commands-instead-of-) | C DOX002 |
| [Explicit brief, period, spacing](https://micro-os-plus.github.io/develop/doxygen-style-guide/#explicit-brief) | C DOX003/012; H nonfunction briefs/spacing |
| [Explicit details, placement, duplication](https://micro-os-plus.github.io/develop/doxygen-style-guide/#explicit-details) | C DOX004; H placement/duplication |
| [Declaration/definition split](https://micro-os-plus.github.io/develop/doxygen-style-guide/#use-brief-with-declarations-and-details-with-definitions) | C DOX012 locally; H cross-file |
| [Inline code](https://micro-os-plus.github.io/develop/doxygen-style-guide/#back-apostrophes-for-references-to-code) | C DOX009 |
| [Italics](https://micro-os-plus.github.io/develop/doxygen-style-guide/#underscores-for-italics) | H |
| [Bold](https://micro-os-plus.github.io/develop/doxygen-style-guide/#double-asterisks-for-bold) | H |
| [Code blocks, language, spacing](https://micro-os-plus.github.io/develop/doxygen-style-guide/#use-code-for-sequences-of-source-lines) | C DOX008; H spacing |
| [Verbatim blocks](https://micro-os-plus.github.io/develop/doxygen-style-guide/#use-verbatim-for-other-pre-formatted-lines) | C DOX008; H classification |
| [Lists and indentation](https://micro-os-plus.github.io/develop/doxygen-style-guide/#lists) | D/H |
| [Tables and alignment](https://micro-os-plus.github.io/develop/doxygen-style-guide/#tables) | D/H |
| [External links](https://micro-os-plus.github.io/develop/doxygen-style-guide/#external-links) | D/H; lychee |
| [Template parameters and prose](https://micro-os-plus.github.io/develop/doxygen-style-guide/#use-tparam-for-template-parameters) | C DOX007/011 |
| [Parameters, direction, prose, tabs, None](https://micro-os-plus.github.io/develop/doxygen-style-guide/#use-param-for-function-parameters) | C DOX006/007/010; H direction/tabs |
| [Return variants, spacing, Nothing](https://micro-os-plus.github.io/develop/doxygen-style-guide/#use-return-or-retval-for-the-returned-result) | C DOX012; H meaning/spacing |
| [Header names, paths, association](https://micro-os-plus.github.io/develop/doxygen-style-guide/#use-headerfile-to-define-the-header-full-path) | D/H |
| [Member groups, continuity, closing names, spacing, nosubgrouping, nesting](https://micro-os-plus.github.io/develop/doxygen-style-guide/#use-of-name-to-define-custom-member-grouping) | D/H |
| [Template sample](https://micro-os-plus.github.io/develop/doxygen-style-guide/#template-sample) | C/H preceding rules |
| [Module groups, separate blocks, spacing, placement within name](https://micro-os-plus.github.io/develop/doxygen-style-guide/#ingroup) | D/H |
| [Named sections, separate blocks, recommended names](https://micro-os-plus.github.io/develop/doxygen-style-guide/#name) | D/H |
| [Plural typedef/using descriptions](https://micro-os-plus.github.io/develop/doxygen-style-guide/#typedefs-or-using) | H |
| [Brief/details separation](https://micro-os-plus.github.io/develop/doxygen-style-guide/#extra-line-between-brief-and-details) | C DOX005 |

## House adaptations and supported scope

Apply the consuming project's instructions first. The automated baseline checks
existing documentation comments in C11/C17 and C++17/C++20 source syntax exercised
by the fixtures. The parser accepts a broader grammar; that fact alone does not
establish support for every dialect feature. Use explicit `--language c` for C
headers because `.h` defaults to C++. Treat C23, C++23/26, Objective-C, CUDA,
compiler extensions and other languages as requiring a separate support review.

The tool recognizes `/**`, `/*!`, `///`, `//!` and their trailing variants;
DOX001 expresses the adopted preferred form. Function contract checks apply to
an adjacent documented declaration, including members and ordinary overloads.
Templates support named type and non-type parameters. Code and verbatim payloads
are protected from prose checks; additional Doxygen commands remain available to
the project's generation configuration. The catalog identifies the finite
command-prefix vocabulary checked by DOX002 in its implementation.

Several rules have intentional review ownership. API direction and scalar versus
discrete return meaning need evidence from the implementation. Group design,
emphasis and whitespace need rendered inspection. Header paths depend on the
project's include conventions. Compare the upstream `@nosubgrouping` observation
with the project's actual Doxygen version before changing working configuration.
Spacing examples and verbal prescriptions differ in places: preserve a coherent
project convention and inspect its rendering. DOX005 enforces an empty line
between brief and details; further spacing remains editorial.

For constructors and destructors, the linter checks parameter documentation and
the brief; their contract review covers lifetime effects. Definitions with only
`@details` are checked for local style, and the reviewer follows the declaration
for the brief, parameter and return contract. Unnamed parameters, variadics,
trailing/deduced return types, nested template parameters, macro-generated
declarations, detached/trailing comments and ambiguous declarators produce
explicit coverage records as described in the linter guide.

## Contract review

For a changed API, connect each material sentence to code, tests or an accepted
specification using the [evidence workflow](evidence.md). Check the valid input
domain and preconditions, ownership transfer, object and buffer lifetime,
observable state changes, errors and recovery, concurrency and ordering, and
return-value meaning. Include the parts the reader needs to use this API safely.

For example, a buffer parameter described as "Data." leaves important questions
open. Establish whether the function reads or writes the buffer, whether it
retains a reference, which length applies and what happens on an error. Then
write the supported contract and verify parameter names and generated links.
Lint success is evidence about the implemented checks; combine it with Vale,
Doxygen generation and factual review before reporting overall validation.
