import pytest
from doxygen_linter.models import Finding
from doxygen_linter.rules import parameter_description


@pytest.mark.parametrize("command", ["param [in]", "tparam"])
@pytest.mark.parametrize("description", ["", "lowercase.", "Missing period", "Wrong punctuation!"])
def test_requires_capitalized_complete_descriptions(comment_context, command, description):
    source = f"/** @{command} value {description} */"
    assert list(parameter_description.check(comment_context(source))) == [Finding(4)]


@pytest.mark.parametrize("command", ["param [in]", "tparam"])
def test_accepts_complete_multiline_descriptions(comment_context, command):
    source = f"/** @{command} value The\n * value to read.\n */"
    assert list(parameter_description.check(comment_context(source))) == []


def test_reports_malformed_parameter_tags(comment_context):
    assert list(parameter_description.check(comment_context("/** @param [in] */"))) == [Finding(4)]


def test_masks_parameter_examples(comment_context):
    source = "/** `@param value lowercase`\n * @code{.cpp}\n * @tparam Value lowercase\n * @endcode\n */"
    assert list(parameter_description.check(comment_context(source))) == []
