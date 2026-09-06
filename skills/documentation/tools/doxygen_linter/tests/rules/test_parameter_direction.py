import pytest
from doxygen_linter.models import Finding
from doxygen_linter.rules import parameter_direction


@pytest.mark.parametrize("direction", ["[in]", "[out]", "[in,out]", "[out,in]", "[in, out]"])
def test_accepts_supported_directions(comment_context, direction):
    source = f"/** @param {direction} value The value. */"
    assert list(parameter_direction.check(comment_context(source))) == []


@pytest.mark.parametrize("parameter", ["value The value.", "[sideways] value The value.", "[in]", ""])
def test_reports_missing_or_invalid_directions(comment_context, parameter):
    assert list(parameter_direction.check(comment_context(f"/** @param {parameter} */"))) == [Finding(4)]


def test_template_parameters_have_no_direction_requirement(comment_context):
    assert list(parameter_direction.check(comment_context("/** @tparam Value The type. */"))) == []


def test_masks_parameter_examples(comment_context):
    source = "/** `@param value Example.`\n * @code{.cpp}\n * @param value Example.\n * @endcode\n */"
    assert list(parameter_direction.check(comment_context(source))) == []
