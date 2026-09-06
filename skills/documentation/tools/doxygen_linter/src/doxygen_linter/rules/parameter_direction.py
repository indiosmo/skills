"""Require an explicit direction on function parameter tags."""

from collections.abc import Iterator

from ..comments import parameter_tag
from ..context import CommentContext
from ..models import Finding, Rule

RULE = Rule(
    "DOX006",
    "A parameter has an explicit direction.",
    "Use @param [in], [out], or [in,out].",
    "use-param-for-function-parameters",
)


def check(context: CommentContext) -> Iterator[Finding]:
    for tag in context.tags:
        if tag.name == "param":
            _, _, direction = parameter_tag(tag)
            if not direction:
                yield Finding(tag.offset)
