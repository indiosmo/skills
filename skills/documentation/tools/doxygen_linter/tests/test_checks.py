"""Behavioral examples for every advertised rule and parser boundary."""

import pytest
from doxygen_linter.checks import lint

VALID = """/**
 * @brief Read a value.
 * @param [in] count Number of values.
 * @return The value.
 */
int read(int count);
"""


def findings(source: str, language: str = "cpp"):
    return lint(source.encode(), "fixture.cpp", language)


@pytest.mark.parametrize(
    ("rule", "valid", "invalid"),
    [
        ("DOX001", "/** @file sample.h */", "/// @file sample.h"),
        ("DOX002", "/** @brief Read. */", "/** \\brief Read. */"),
        ("DOX003", "/** @brief Read. */", "/** @brief Read */"),
        ("DOX004", "/** @details\n * Read. */", "/** @details Read. */"),
        (
            "DOX005",
            "/** @brief Read.\n *\n * @details\n * Read. */",
            "/** @brief Read.\n * @details\n * Read. */",
        ),
        ("DOX006", "/** @param [in] count Number. */", "/** @param count Number. */"),
        ("DOX007", "/** @tparam Value The type. */", "/** @tparam Value the type */"),
        (
            "DOX008",
            "/** @code{.cpp}\nint count;\n@endcode */",
            "/** @code\nint count;\n@endcode */",
        ),
        ("DOX009", "/** Use `count`. */", "/** Use @c count. */"),
        ("DOX010", VALID, VALID.replace("[in] count", "[in] size")),
        (
            "DOX011",
            "/** @brief Store.\n@tparam Value The type. */\ntemplate<typename Value> class Store {};",
            "/** @brief Store. */\ntemplate<typename Value> class Store {};",
        ),
        ("DOX012", VALID, VALID.replace(" * @return The value.\n", "")),
    ],
    ids=lambda value: value if isinstance(value, str) and value.startswith("DOX") else None,
)
def test_each_rule_accepts_valid_and_rejects_invalid(rule, valid, invalid):
    assert rule not in {diagnostic.rule for diagnostic in findings(valid)[0]}
    assert rule in {diagnostic.rule for diagnostic in findings(invalid)[0]}


@pytest.mark.parametrize("language", ["c", "cpp"])
def test_valid_function_contract(language):
    assert findings(VALID, language) == ([], [])


@pytest.mark.parametrize(
    "source",
    [
        'const char *literal = "/** @brief invalid */";',
        r"""const char *literal = R"tag(/** @brief invalid */)tag";""",
        "char slash = '/'; // ordinary comment\n",
        'const char *literal = "escaped \\" /**";',
        "// /** @brief ignored */\nint value;",
        "/* /** @brief ignored */\nint value;",
    ],
    ids=["string", "raw-string", "character", "escaped-quote", "line-comment", "ordinary-block"],
)
def test_delimiters_inside_literals_are_not_documentation(source):
    assert findings(source)[0] == []


@pytest.mark.parametrize(
    "source",
    [
        "/** @brief Read.\n * @code{.cpp}\n * @param invalid\n * @endcode\n */",
        "/** @brief Use `@c` to demonstrate a command. */",
        "/** @brief Read @ref Store safely. */",
        "/** @verbatim\n@param invalid\n@endverbatim */",
    ],
)
def test_code_and_inline_references_do_not_create_false_prose_findings(source):
    assert findings(source)[0] == []


@pytest.mark.parametrize(
    "source",
    [
        "/** @endcode */",
        "/** @code{.cpp} */",
        "/** @verbatim @endcode */",
        "/** @code{.cpp} @verbatim @endcode */",
    ],
)
def test_malformed_example_blocks(source):
    assert "DOX008" in {diagnostic.rule for diagnostic in findings(source)[0]}


def test_multiline_parameter_description():
    assert findings(VALID.replace("Number of values.", "Number of\n * values."))[0] == []


def test_original_unicode_and_crlf_positions():
    diagnostics, _ = findings("// cafe\r\n/** @brief Lire.\r\n * @param count invalid\r\n */\r\nint read(int count);")
    parameter = next(diagnostic for diagnostic in diagnostics if diagnostic.rule == "DOX006")
    assert (parameter.line, parameter.column) == (3, 4)
    diagnostics, _ = findings("/** cafe é @param count invalid */")
    parameter = next(diagnostic for diagnostic in diagnostics if diagnostic.rule == "DOX006")
    assert (parameter.line, parameter.column) == (1, 12)


def test_overloads_are_associated_independently():
    diagnostics, coverage = findings(VALID + VALID.replace("int count", "double count"))
    assert diagnostics == []
    assert coverage == []


def test_callback_parameter_is_not_confused_with_nested_parameters():
    source = VALID.replace("int count", "void (*count)(int nested)")
    assert findings(source) == ([], [])


def test_default_argument_and_qualified_method():
    source = "class Store { public:\n" + VALID.replace("int count);", "int count = 3) const;") + "};"
    assert findings(source) == ([], [])


def test_function_template():
    source = VALID.replace(" * @return", " * @tparam Value The value type.\n * @return").replace(
        "int read(int count);", "template<typename Value> Value read(Value count);"
    )
    assert findings(source) == ([], [])


def test_template_defaults_and_non_type_parameters():
    source = "/** @brief Store.\n@tparam Value The type.\n@tparam Capacity The capacity. */\ntemplate<typename Value = int, int Capacity = 3> class Store {};"
    assert findings(source) == ([], [])


def test_zero_parameters_and_void_return():
    source = "/** @brief Clear.\n@par Parameters\nNone.\n@par Returns\nNothing. */\nvoid clear(void);"
    assert findings(source) == ([], [])


def test_void_pointer_requires_return_contract():
    source = "/** @brief Read.\n@par Parameters\nNone.\n@return A pointer. */\nvoid *read();"
    assert findings(source) == ([], [])


def test_details_only_definition():
    assert findings("/** @details\nRead one value. */\nint read(int count) { return count; }") == (
        [],
        [],
    )


@pytest.mark.parametrize("declaration", ["DECLARE(read);", "#define DECLARE(name) int name(int count)", ""])
def test_macro_or_detached_contract_has_visible_skipped_association(declaration):
    _, coverage = findings("/** @brief Read. */\n" + declaration)
    assert any(item.status == "skipped" for item in coverage)


def test_malformed_source_is_blocked():
    _, coverage = findings("/** @brief Read. */\nint read(int {")
    assert any(item.status == "blocked" for item in coverage)


@pytest.mark.parametrize("parameters", ["int", "int count, ..."])
def test_unnamed_or_variadic_parameters_report_skip(parameters):
    _, coverage = findings(VALID.replace("int count", parameters))
    assert any(item.checks == "DOX010" and item.status == "skipped" for item in coverage)


def test_trailing_comment_has_visible_skip():
    _, coverage = findings("int count; /**< @brief Count. */")
    assert any("Trailing" in item.reason for item in coverage)


def test_duplicate_parameter_tag_is_rejected():
    assert "DOX010" in {
        item.rule for item in findings(VALID.replace(" * @return", " * @param [in] count Number.\n * @return"))[0]
    }


def test_reasoned_suppression_has_narrow_scope():
    source = "/** @brief Invalid\n * doxygen-lint: disable=DOX003 -- Upstream spelling retained.\n */\nint value;\n/** @brief Invalid */\nint second;"
    diagnostics, coverage = findings(source)
    assert len([item for item in diagnostics if item.rule == "DOX003"]) == 1
    assert any(item.checks == "DOX003" and item.status == "skipped" for item in coverage)


@pytest.mark.parametrize("suppression", ["DOX003", "DOX999 -- Reason.", "DOX003 -- "])
def test_bad_suppression_is_blocked(suppression):
    _, coverage = findings("/** @brief Invalid\n * doxygen-lint: disable=" + suppression + "\n */")
    assert any(item.status == "blocked" for item in coverage)


def test_ordinary_comment_between_documentation_and_function_is_visible():
    diagnostics, coverage = findings(VALID.replace("int read", "// adapter declaration\nint read"))
    assert diagnostics == []
    assert any(item.status == "skipped" for item in coverage)


@pytest.mark.parametrize("declaration", ["int (*reader)(int count);", "int read(int count), read_more(int count);"])
def test_ambiguous_declarators_are_skipped(declaration):
    diagnostics, coverage = findings(VALID.replace("int read(int count);", declaration))
    assert diagnostics == []
    assert any("declarators" in item.reason for item in coverage)


def test_operator_overload_has_parameter_contract():
    source = "class Store { public:\n" + VALID.replace("int read(int count);", "int operator+(int count) const;") + "};"
    assert findings(source) == ([], [])


def test_trailing_return_is_explicitly_skipped():
    diagnostics, coverage = findings(VALID.replace("int read(int count);", "auto read(int count) -> int;"))
    assert diagnostics == []
    assert any(item.checks == "DOX012:return" for item in coverage)


def test_member_trailing_comment_is_not_attached_to_next_method():
    source = "struct Store { int count; /**< @brief Count. */\nint read(int wrong); };"
    diagnostics, coverage = findings(source)
    assert diagnostics == []
    assert any("Trailing" in item.reason for item in coverage)


def test_preprocessor_continuation_comments_remain_in_macro_scope():
    source = "#define DECLARE(name) \\\n int name(int count)\n/** @brief Read. */\nDECLARE(read);"
    diagnostics, coverage = findings(source)
    assert diagnostics == []
    assert any("macros" in item.reason for item in coverage)


@pytest.mark.parametrize(
    "command",
    [
        "see function()",
        "note Additional context",
        "snippet sample.cpp example",
        "projectalias Custom text",
    ],
)
def test_block_commands_terminate_brief_and_parameter_descriptions(command):
    source = "/** @brief Read.\n * @" + command + "\n */"
    assert findings(source)[0] == []
    source = "/** @param [in] count Number.\n * @" + command + "\n */"
    assert findings(source)[0] == []


def test_inline_ref_at_line_start_preserves_brief_sentence():
    assert findings("/** @brief Read\n * @ref Store safely. */")[0] == []


@pytest.mark.parametrize(
    "return_documentation",
    [
        "@return",
        "@return   ",
        "@retval",
        "@retval 0",
        "@retval 0 Success.\n * @retval 1",
        "@return The value.\n * @retval",
        "@return\n * @note Additional context.",
    ],
)
def test_empty_return_contract_is_rejected(return_documentation):
    source = VALID.replace("@return The value.", return_documentation)
    assert "DOX012" in {diagnostic.rule for diagnostic in findings(source)[0]}


@pytest.mark.parametrize(
    "return_documentation",
    [
        "@return The value.",
        "@return\n * The value.",
        "@retval 0 Success.",
        "@retval 0 Success.\n * @retval -1 Failure.",
        "@retval `0` Success.",
        "@return `count`.",
    ],
)
def test_nonempty_return_contract_is_accepted(return_documentation):
    source = VALID.replace("@return The value.", return_documentation)
    assert findings(source) == ([], [])
