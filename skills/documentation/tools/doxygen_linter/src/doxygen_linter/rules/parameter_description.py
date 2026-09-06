"""Require complete capitalized prose for parameter descriptions."""

from collections.abc import Iterator

from ..comments import parameter_tag
from ..context import CommentContext
from ..models import Finding, Rule

RULE = Rule(
    "DOX007",
    "Parameter prose starts uppercase and ends with a period.",
    "Write a complete capitalized description ending with a period.",
    "use-param-for-function-parameters",
)


def check(context: CommentContext) -> Iterator[Finding]:
    for tag in context.tags:
        if tag.name in {"param", "tparam"}:
            _, description, _ = parameter_tag(tag)
            if not description or not description[0].isupper() or not description.endswith("."):
                yield Finding(tag.offset)
