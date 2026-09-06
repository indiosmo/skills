"""Match documented function parameters to their declaration."""

import re
from collections import Counter
from collections.abc import Iterator

from ..comments import parameter_tag
from ..context import CommentContext
from ..models import Finding, Rule, Skip
from ..parsing import parameter_names

RULE = Rule(
    "DOX010",
    "Documented function parameters match the declaration.",
    "Document each named parameter once and remove unknown names.",
    "use-param-for-function-parameters",
)


def check(context: CommentContext) -> Iterator[Finding | Skip]:
    function = context.declaration.function
    if function is None:
        return
    parameters = function.child_by_field_name("parameters")
    assert parameters is not None, "Function declarators contain a parameter list"
    expected, unsupported = parameter_names(parameters)
    if unsupported:
        yield Skip("Unnamed, variadic or unsupported parameter requires review.")
        return
    if context.declaration.details_only:
        return
    documented = [parameter_tag(tag)[0] for tag in context.tags if tag.name == "param"]
    empty_parameters = any(
        tag.name == "par" and re.fullmatch(r"Parameters\s+None\.", tag.value) for tag in context.tags
    )
    if Counter(expected) != Counter(documented) or (not expected and not empty_parameters):
        yield Finding(
            explanation=f"Expected parameters {expected}; documented {documented}; zero parameters use @par Parameters / None."
        )
