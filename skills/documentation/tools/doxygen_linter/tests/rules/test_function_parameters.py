"""Examples of matching function parameter documentation."""

import pytest
from doxygen_linter.models import Finding, Skip
from doxygen_linter.rules import function_parameters


@pytest.mark.parametrize(
    "declaration",
    [
        "int read(int count);",
        "int read(int count = 3);",
        "int read(void (*count)(int nested));",
        "template<typename Value> Value read(Value count);",
    ],
    ids=["named", "default", "callback", "template"],
)
def test_named_parameter_matches_declaration(comment_context, declaration):
    context = comment_context("/** @param [in] count Number of values. */\n" + declaration)
    assert list(function_parameters.check(context)) == []


@pytest.mark.parametrize(
    ("documentation", "documented"),
    [
        ("", "[]"),
        ("@param [in] size Number of values.", "['size']"),
        ("@param [in] count Number.\n@param [in] count Number.", "['count', 'count']"),
    ],
    ids=["missing", "unknown", "duplicate"],
)
def test_parameter_mismatch_explains_expected_and_documented_names(comment_context, documentation, documented):
    context = comment_context("/** " + documentation + " */\nint read(int count);")
    assert list(function_parameters.check(context)) == [
        Finding(
            explanation=f"Expected parameters ['count']; documented {documented}; zero parameters use @par Parameters / None."
        )
    ]


@pytest.mark.parametrize("parameters", ["", "void"], ids=["empty", "void"])
def test_zero_parameters_require_explicit_none(comment_context, parameters):
    declaration = f"\nvoid clear({parameters});"
    assert list(function_parameters.check(comment_context("/** @par Parameters\nNone. */" + declaration))) == []
    assert list(function_parameters.check(comment_context("/** @brief Clear. */" + declaration))) == [
        Finding(explanation="Expected parameters []; documented []; zero parameters use @par Parameters / None.")
    ]


@pytest.mark.parametrize("parameters", ["int", "int count, ..."], ids=["unnamed", "variadic"])
@pytest.mark.parametrize("definition", [False, True], ids=["declaration", "details-only-definition"])
def test_unsupported_parameters_are_skipped(comment_context, parameters, definition):
    documentation = "/** @details\nRead a value. */" if definition else "/** @brief Read. */"
    ending = " { return 1; }" if definition else ";"
    context = comment_context(documentation + f"\nint read({parameters})" + ending)
    assert list(function_parameters.check(context)) == [
        Skip("Unnamed, variadic or unsupported parameter requires review.")
    ]


def test_details_only_definition_accepts_parameter_details_in_declaration(comment_context):
    context = comment_context("/** @details\nRead a value. */\nint read(int count) { return count; }")
    assert list(function_parameters.check(context)) == []


def test_non_function_has_no_parameter_contract(comment_context):
    context = comment_context("/** @brief Count. */\nint count;")
    assert list(function_parameters.check(context)) == []
