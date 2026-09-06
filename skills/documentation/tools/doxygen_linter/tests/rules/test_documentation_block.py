import pytest
from doxygen_linter.models import Finding
from doxygen_linter.rules import documentation_block


@pytest.mark.parametrize("source", ["/** Description. */", "/**< Description. */"])
def test_accepts_documentation_blocks(comment_context, source):
    assert list(documentation_block.check(comment_context(source))) == []


@pytest.mark.parametrize("source", ["/*! Description. */", "/// Description.", "//! Description."])
def test_reports_alternative_delimiters(comment_context, source):
    assert list(documentation_block.check(comment_context(source))) == [Finding()]
