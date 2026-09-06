"""Require a blank line before details in comments containing a brief."""

from collections.abc import Iterator

from ..context import CommentContext
from ..models import Finding, Rule

RULE = Rule(
    "DOX005",
    "Brief and details have a blank line between them.",
    "Insert an empty comment line before @details.",
    "extra-line-between-brief-and-details",
)


def check(context: CommentContext) -> Iterator[Finding]:
    if not any(tag.name == "brief" for tag in context.tags):
        return
    for tag in context.tags:
        if tag.name == "details":
            preceding = context.prose[: tag.offset].splitlines()
            if len(preceding) > 1 and preceding[-2].strip():
                yield Finding(tag.offset)
