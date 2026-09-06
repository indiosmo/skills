"""Require a period at the end of brief descriptions."""

from collections.abc import Iterator

from ..context import CommentContext
from ..models import Finding, Rule

RULE = Rule("DOX003", "A brief ends with a period.", "End @brief with a period.", "explicit-brief")


def check(context: CommentContext) -> Iterator[Finding]:
    for tag in context.tags:
        if tag.name == "brief" and (not tag.value or not tag.value.endswith(".")):
            yield Finding(tag.offset)
