import pytest
from doxygen_linter.models import Finding
from doxygen_linter.rules import example_blocks


@pytest.mark.parametrize("block", ["@code{.cpp}\n * int value;\n * @endcode", "@verbatim\n * Text\n * @endverbatim"])
def test_accepts_balanced_examples(comment_context, block):
    assert list(example_blocks.check(comment_context(f"/** {block}\n */"))) == []


@pytest.mark.parametrize("opener", ["@code", "@code{cpp}", "@code{}"])
def test_requires_an_explicit_dotted_language(comment_context, opener):
    source = f"/** {opener}\n * @endcode\n */"
    assert list(example_blocks.check(comment_context(source))) == [Finding(4, "Code block needs an explicit language.")]


def test_reports_an_unmatched_closing_command(comment_context):
    assert list(example_blocks.check(comment_context("/** @endcode */"))) == [
        Finding(4, "Example closing command has no matching opener.")
    ]


def test_reports_an_unclosed_block(comment_context):
    assert list(example_blocks.check(comment_context("/** @code{.cpp}\n * int value;\n */"))) == [
        Finding(4, "Example block has no matching closer.")
    ]


def test_reports_nested_blocks_at_the_nested_opener(comment_context):
    source = "/** @code{.cpp}\n * @verbatim\n * @endcode\n */"
    assert list(example_blocks.check(comment_context(source))) == [
        Finding(19, "Nested example blocks require separate blocks.")
    ]


def test_reports_mismatched_closers_and_the_unclosed_opener(comment_context):
    source = "/** @code{.cpp}\n * @endverbatim\n */"
    assert list(example_blocks.check(comment_context(source))) == [
        Finding(19, "Example closing command has no matching opener."),
        Finding(4, "Example block has no matching closer."),
    ]
