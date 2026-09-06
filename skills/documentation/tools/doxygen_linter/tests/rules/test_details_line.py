import pytest
from doxygen_linter.models import Finding
from doxygen_linter.rules import details_line


@pytest.mark.parametrize("command", ["@details", "\\details"])
def test_reports_prose_on_the_command_line(comment_context, command):
    source = f"/** {command} Read a value. */"
    assert list(details_line.check(comment_context(source))) == [Finding(4)]


def test_accepts_prose_below_the_command(comment_context):
    source = "/** @details\n * Read a value.\n */"
    assert list(details_line.check(comment_context(source))) == []


def test_masks_literal_details_examples(comment_context):
    source = "/** `@details Inline text`\n * @code{.cpp}\n * @details Inline text\n * @endcode\n */"
    assert list(details_line.check(comment_context(source))) == []


def test_accepts_a_command_with_only_inline_code_on_its_line(comment_context):
    assert list(details_line.check(comment_context("/** @details `literal` */"))) == []
