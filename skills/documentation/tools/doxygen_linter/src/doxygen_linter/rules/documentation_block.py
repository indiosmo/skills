"""Require the adopted documentation block delimiter."""

from collections.abc import Iterator

from ..context import CommentContext
from ..models import Finding, Rule

RULE = Rule("DOX001", "Documentation uses a /** block.", "Use /** ... */.", "--comments-instead-of-")


def check(context: CommentContext) -> Iterator[Finding]:
    if not context.comment.text.startswith("/**"):
        yield Finding()
