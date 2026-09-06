from doxygen_linter.models import Finding
from doxygen_linter.rules import brief_details_spacing


def test_reports_details_directly_after_brief(comment_context):
    source = "/** @brief Read.\n * @details\n * Read the next value.\n */"
    assert list(brief_details_spacing.check(comment_context(source))) == [Finding(20)]


def test_accepts_an_empty_decorated_line(comment_context):
    source = "/** @brief Read.\n *\n * @details\n * Read the next value.\n */"
    assert list(brief_details_spacing.check(comment_context(source))) == []


def test_accepts_details_without_a_brief(comment_context):
    source = "/** Implementation.\n * @details\n * Read the next value.\n */"
    assert list(brief_details_spacing.check(comment_context(source))) == []


def test_masks_brief_commands_in_examples(comment_context):
    source = "/** `@brief Example.`\n * @details\n * Read the next value.\n */"
    assert list(brief_details_spacing.check(comment_context(source))) == []


def test_reports_a_filled_line_immediately_before_details(comment_context):
    source = "/** @brief Read.\n *\n * More prose.\n * @details\n * Read the next value.\n */"
    assert list(brief_details_spacing.check(comment_context(source))) == [Finding(38)]
