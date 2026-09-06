"""Build parsed comment contexts for direct rule tests."""

from collections.abc import Callable

import pytest
from doxygen_linter.context import CommentContext, prepare_comment
from doxygen_linter.parsing import parse


@pytest.fixture
def comment_context() -> Callable[..., CommentContext]:
    def build(source: str, language: str = "cpp") -> CommentContext:
        _, comments = parse(source.encode("utf-8"), language)
        assert len(comments) == 1, "Rule examples contain exactly one documentation comment"
        return prepare_comment(comments[0])

    return build
