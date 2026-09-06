"""Examples of supported function briefs and return contracts."""

import pytest
from doxygen_linter.models import Finding, Skip
from doxygen_linter.rules import function_contract


@pytest.mark.parametrize(
    "return_documentation",
    [
        "@return The value.",
        "@return\nThe value.",
        "@return `count`.",
        "@retval 0 Success.",
        "@retval `0` Success.",
        "@retval 0 Success.\n@retval -1 Failure.",
    ],
    ids=["return", "multiline", "code-span", "retval", "retval-code-span", "multiple-retval"],
)
def test_nonempty_return_description_is_accepted(comment_context, return_documentation):
    context = comment_context("/** @brief Read.\n" + return_documentation + " */\nint read(int count);")
    assert list(function_contract.check(context)) == []


@pytest.mark.parametrize(
    "return_documentation",
    [
        "",
        "@return",
        "@return   ",
        "@retval",
        "@retval 0",
        "@retval 0 Success.\n@retval 1",
        "@return The value.\n@retval",
        "@return\n@note Additional context.",
        "@return\n@code{.cpp}\nreturn count;\n@endcode",
        "@return\ndoxygen-lint: disable=DOX010 -- Parameter contract reviewed.",
    ],
    ids=[
        "missing",
        "empty-return",
        "blank-return",
        "empty-retval",
        "retval-value-only",
        "incomplete-second-retval",
        "incomplete-retval-after-return",
        "different-command",
        "example-only",
        "suppression-only",
    ],
)
def test_incomplete_return_contract_is_rejected(comment_context, return_documentation):
    context = comment_context("/** @brief Read.\n" + return_documentation + " */\nint read(int count);")
    assert list(function_contract.check(context)) == [Finding()]


def test_return_contract_requires_brief(comment_context):
    context = comment_context("/** @return The value. */\nint read(int count);")
    assert list(function_contract.check(context)) == [Finding()]


def test_void_return_requires_explicit_nothing(comment_context):
    valid = comment_context("/** @brief Clear.\n@par Returns\nNothing. */\nvoid clear();")
    invalid = comment_context("/** @brief Clear.\n@return Nothing. */\nvoid clear();")
    assert list(function_contract.check(valid)) == []
    assert list(function_contract.check(invalid)) == [Finding()]


def test_void_pointer_requires_value_description(comment_context):
    valid = comment_context("/** @brief Read.\n@return A pointer. */\nvoid *read();")
    invalid = comment_context("/** @brief Read.\n@par Returns\nNothing. */\nvoid *read();")
    assert list(function_contract.check(valid)) == []
    assert list(function_contract.check(invalid)) == [Finding()]


@pytest.mark.parametrize(
    "declaration",
    ["auto read() -> int;", "auto read() { return 1; }", "decltype(auto) read() { return 1; }"],
    ids=["trailing", "auto", "decltype-auto"],
)
def test_deduced_return_contract_is_skipped_and_brief_still_required(comment_context, declaration):
    skip = Skip("Trailing or deduced return type requires contract review.", suffix=":return")
    assert list(function_contract.check(comment_context("/** @brief Read. */\n" + declaration))) == [skip]
    assert list(function_contract.check(comment_context("/** @return The value. */\n" + declaration))) == [
        skip,
        Finding(),
    ]


def test_constructor_requires_brief_without_return_description(comment_context):
    context = comment_context("class Store { public:\n/** @brief Construct. */\nStore(); };")
    assert list(function_contract.check(context)) == []


def test_details_only_definition_accepts_contract_in_declaration(comment_context):
    context = comment_context("/** @details\nRead a value. */\nint read(int count) { return count; }")
    assert list(function_contract.check(context)) == []


def test_non_function_has_no_function_contract(comment_context):
    context = comment_context("/** @brief Count. */\nint count;")
    assert list(function_contract.check(context)) == []
