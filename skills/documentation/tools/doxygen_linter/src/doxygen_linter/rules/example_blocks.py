"""Report malformed code and verbatim blocks discovered during normalization."""

from collections.abc import Iterator

from ..context import CommentContext
from ..models import Finding, Rule

RULE = Rule(
    "DOX008",
    "Code and verbatim blocks balance; code declares a language.",
    "Pair @code{.language}/@endcode or @verbatim/@endverbatim.",
    "use-code-for-sequences-of-source-lines",
)


def check(context: CommentContext) -> Iterator[Finding]:
    yield from context.example_findings
