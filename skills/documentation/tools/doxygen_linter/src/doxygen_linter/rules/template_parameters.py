"""Match documented template parameters to their declaration."""

from collections import Counter
from collections.abc import Iterator

from ..comments import parameter_tag
from ..context import CommentContext
from ..models import Finding, Rule, Skip
from ..parsing import template_names

RULE = Rule(
    "DOX011",
    "Template parameter documentation matches the declaration.",
    "Document each named template parameter once with @tparam.",
    "use-tparam-for-template-parameters",
)


def check(context: CommentContext) -> Iterator[Finding | Skip]:
    template = context.declaration.template
    if template is None:
        return
    expected, unsupported = template_names(template)
    if unsupported:
        yield Skip("Unnamed or nested template parameter requires review.")
        return
    documented = [parameter_tag(tag)[0] for tag in context.tags if tag.name == "tparam"]
    if Counter(expected) != Counter(documented):
        yield Finding(explanation=f"Expected template parameters {expected}; documented {documented}.")
