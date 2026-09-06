import pytest
from doxygen_linter.models import Finding
from doxygen_linter.rules import brief_period


@pytest.mark.parametrize("description", ["", "Missing punctuation", "Wrong punctuation!"])
def test_requires_a_nonempty_brief_ending_in_a_period(comment_context, description):
    source = f"/** @brief {description} */"
    assert list(brief_period.check(comment_context(source))) == [Finding(4)]


def test_accepts_a_complete_multiline_brief(comment_context):
    source = "/** @brief Read the\n * next value.\n */"
    assert list(brief_period.check(comment_context(source))) == []


def test_masks_literal_brief_examples(comment_context):
    source = "/** `@brief Missing period`\n * @code{.cpp}\n * @brief Example\n * @endcode\n */"
    assert list(brief_period.check(comment_context(source))) == []


def test_stops_brief_at_the_next_block_command(comment_context):
    source = "/** @brief Missing period\n * @note A complete note.\n */"
    assert list(brief_period.check(comment_context(source))) == [Finding(4)]
