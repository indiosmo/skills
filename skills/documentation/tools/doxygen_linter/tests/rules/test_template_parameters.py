"""Examples of matching template parameter documentation."""

import pytest
from doxygen_linter.models import Finding, Skip
from doxygen_linter.rules import template_parameters


@pytest.mark.parametrize(
    "declaration",
    [
        "template<typename Value> class Store {};",
        "template<typename Value> Value read(Value count);",
        "template<typename... Value> class Store {};",
    ],
    ids=["class", "function", "parameter-pack"],
)
def test_named_template_parameter_matches_documentation(comment_context, declaration):
    context = comment_context("/** @tparam Value The value type. */\n" + declaration)
    assert list(template_parameters.check(context)) == []


def test_default_and_non_type_template_parameters(comment_context):
    context = comment_context(
        "/** @tparam Value The value type.\n@tparam Capacity The capacity. */\n"
        "template<typename Value = int, int Capacity = 3> class Store {};"
    )
    assert list(template_parameters.check(context)) == []


@pytest.mark.parametrize(
    ("documentation", "documented"),
    [
        ("", "[]"),
        ("@tparam Other The type.", "['Other']"),
        ("@tparam Value The type.\n@tparam Value The type.", "['Value', 'Value']"),
    ],
    ids=["missing", "unknown", "duplicate"],
)
def test_mismatch_explains_expected_and_documented_template_names(comment_context, documentation, documented):
    context = comment_context("/** " + documentation + " */\ntemplate<typename Value> class Store {};")
    assert list(template_parameters.check(context)) == [
        Finding(explanation=f"Expected template parameters ['Value']; documented {documented}.")
    ]


@pytest.mark.parametrize(
    "parameters",
    ["typename", "template<typename> class Container"],
    ids=["unnamed", "nested"],
)
def test_unsupported_template_parameters_are_skipped(comment_context, parameters):
    context = comment_context("/** @brief Store. */\ntemplate<" + parameters + "> class Store {};")
    assert list(template_parameters.check(context)) == [Skip("Unnamed or nested template parameter requires review.")]


def test_details_only_template_definition_requires_template_parameter_documentation(comment_context):
    context = comment_context(
        "/** @details\nRead a value. */\ntemplate<typename Value> Value read(Value count) { return count; }"
    )
    assert list(template_parameters.check(context)) == [
        Finding(explanation="Expected template parameters ['Value']; documented [].")
    ]


def test_non_template_has_no_template_parameter_contract(comment_context):
    context = comment_context("/** @brief Read. */\nint read(int count);")
    assert list(template_parameters.check(context)) == []
