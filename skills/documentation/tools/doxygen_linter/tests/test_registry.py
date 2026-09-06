"""Registration and runner policy apply uniformly to independent rule functions."""

from collections.abc import Iterator

import pytest
from doxygen_linter.catalog import RULES
from doxygen_linter.checks import lint
from doxygen_linter.context import CommentContext
from doxygen_linter.models import Finding, Rule, Skip
from doxygen_linter.registry import RegisteredRule, rule_catalog
from doxygen_linter.rules import brief_period

TEST_RULE = Rule("DOX100", "Example description.", "Example correction.", "explicit-brief")


def check_brief(context: CommentContext) -> Iterator[Finding | Skip]:
    for tag in context.tags:
        if tag.name == "brief":
            yield Finding(tag.offset, "Example finding.")
    yield Skip("Example return review.", ":return")


def test_registry_rejects_duplicate_identifiers():
    registration = RegisteredRule(TEST_RULE, check_brief)
    with pytest.raises(ValueError, match="Duplicate rule identifier: DOX100"):
        rule_catalog((registration, registration))


def test_catalog_metadata_comes_from_rule_module():
    assert RULES["DOX003"] is brief_period.RULE


def test_registered_rule_receives_context_and_runner_supplies_report_policy():
    diagnostics, coverage = lint(
        b"/** @brief Example. */",
        "example.hpp",
        "cpp",
        {"DOX100": "error"},
        rules=(RegisteredRule(TEST_RULE, check_brief),),
    )
    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]
    assert (diagnostic.rule, diagnostic.path, diagnostic.line, diagnostic.column) == ("DOX100", "example.hpp", 1, 5)
    assert diagnostic.severity == "error"
    assert diagnostic.explanation == "Example finding."
    assert diagnostic.correction == "Example correction."
    assert diagnostic.source.endswith("#explicit-brief")
    assert [(item.checks, item.reason) for item in coverage] == [("DOX100:return", "Example return review.")]


def test_suppression_filters_findings_and_retains_rule_coverage():
    diagnostics, coverage = lint(
        b"/** @brief Example.\n * doxygen-lint: disable=DOX100 -- Reviewed wording.\n */",
        "example.hpp",
        "cpp",
        rules=(RegisteredRule(TEST_RULE, check_brief),),
    )
    assert diagnostics == []
    assert [(item.checks, item.reason) for item in coverage] == [
        ("DOX100", "Reviewed wording."),
        ("DOX100:return", "Example return review."),
    ]


def test_analysis_scope_reports_new_rules_in_skipped_coverage():
    def check_function(context: CommentContext) -> Iterator[Finding]:
        assert context.declaration.function is not None
        yield Finding()

    diagnostics, coverage = lint(
        b"int value; /**< @brief Example. */",
        "example.hpp",
        "cpp",
        rules=(RegisteredRule(TEST_RULE, check_function, "function"),),
    )
    assert diagnostics == []
    assert [(item.checks, item.status) for item in coverage] == [("DOX100", "skipped")]


def test_diagnostics_are_ordered_by_source_location_then_identifier():
    def check_backwards(context: CommentContext) -> Iterator[Finding]:
        for tag in reversed(context.tags):
            yield Finding(tag.offset)

    diagnostics, _ = lint(
        b"/** @brief Example.\n * @param count Count. */",
        "example.hpp",
        "cpp",
        rules=(
            RegisteredRule(TEST_RULE, check_backwards),
            RegisteredRule(Rule("DOX099", "Description.", "Correction.", "explicit-brief"), check_backwards),
        ),
    )
    assert [(item.line, item.column, item.rule) for item in diagnostics] == [
        (1, 5, "DOX099"),
        (1, 5, "DOX100"),
        (2, 4, "DOX099"),
        (2, 4, "DOX100"),
    ]


def test_source_columns_count_unicode_before_and_inside_comment():
    diagnostics, _ = lint(
        'const char *name = "é"; /** é @brief Example.\r\n * @param count Count. */'.encode(),
        "example.hpp",
        "cpp",
        rules=(RegisteredRule(TEST_RULE, check_brief),),
    )
    assert [(item.line, item.column) for item in diagnostics] == [(1, 31)]
