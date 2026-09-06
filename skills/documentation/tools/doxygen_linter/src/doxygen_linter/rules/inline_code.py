"""Require backticks for inline code in comment prose."""

import re
from collections.abc import Iterator

from ..context import CommentContext
from ..models import Finding, Rule

RULE = Rule(
    "DOX009",
    "Inline code uses backticks.",
    "Replace @c, @p, or <code> with backticks.",
    "back-apostrophes-for-references-to-code",
)


def check(context: CommentContext) -> Iterator[Finding]:
    for match in re.finditer(r"[@\\](?:c|p)\s+|<code\b", context.prose):
        yield Finding(match.start())
