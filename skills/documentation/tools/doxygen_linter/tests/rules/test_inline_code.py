import pytest
from doxygen_linter.models import Finding
from doxygen_linter.rules import inline_code


@pytest.mark.parametrize("markup", ["@c value", "@p value", "\\c value", "\\p value", "<code>value</code>"])
def test_reports_inline_markup_at_its_offset(comment_context, markup):
    assert list(inline_code.check(comment_context(f"/** Use {markup}. */"))) == [Finding(8)]


def test_accepts_backticks(comment_context):
    assert list(inline_code.check(comment_context("/** Use `value`. */"))) == []


def test_masks_literal_inline_markup_and_example_payloads(comment_context):
    source = "/** `@c value` and `<code>value</code>`\n * @code{.cpp}\n * @p value\n * @endcode\n */"
    assert list(inline_code.check(comment_context(source))) == []


def test_matches_whole_inline_commands_and_html_tags(comment_context):
    assert list(inline_code.check(comment_context("/** @custom <codeblock> @param */"))) == []
