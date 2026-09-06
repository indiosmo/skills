from doxygen_linter.models import Finding
from doxygen_linter.rules import command_prefix


def test_reports_each_backslash_command_at_its_offset(comment_context):
    source = r"/** \brief Description with \ref symbol. */"
    assert list(command_prefix.check(comment_context(source))) == [Finding(4), Finding(28)]


def test_accepts_at_sign_commands(comment_context):
    assert list(command_prefix.check(comment_context("/** @brief See @ref symbol. */"))) == []


def test_masks_inline_code_and_example_payloads(comment_context):
    source = "/** `\\brief`\n * @code{.cpp}\n * \\param value\n * @endcode\n */"
    assert list(command_prefix.check(comment_context(source))) == []


def test_checks_example_delimiters_inside_masked_blocks(comment_context):
    source = "/** \\code{.cpp}\n * \\param value\n * \\endcode\n */"
    assert list(command_prefix.check(comment_context(source))) == [Finding(4), Finding(35)]


def test_matches_whole_supported_commands(comment_context):
    assert list(command_prefix.check(comment_context(r"/** \parameter \custom */"))) == []
