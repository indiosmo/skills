"""Require details prose to begin below its command."""

from collections.abc import Iterator

from ..context import CommentContext
from ..models import Finding, Rule

RULE = Rule(
    "DOX004",
    "Details start on a separate line.",
    "Put prose below @details.",
    "explicit-details",
)


def check(context: CommentContext) -> Iterator[Finding]:
    for tag in context.tags:
        if tag.name == "details":
            after_command = context.prose[tag.offset + len("@details") :].split("\n", 1)[0]
            if after_command.strip():
                yield Finding(tag.offset)
