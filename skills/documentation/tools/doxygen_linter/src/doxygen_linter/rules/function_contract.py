"""Check supported functions for a brief and a return contract."""

import re
from collections.abc import Iterator

from ..comments import Tag
from ..context import CommentContext
from ..models import Finding, Rule, Skip

RULE = Rule(
    "DOX012",
    "Supported function documentation states a brief and return contract.",
    "Add @brief and a nonempty @return description or @retval value and description; use @par Returns followed by Nothing. for void.",
    "use-brief-with-declarations-and-details-with-definitions",
)


def has_return_documentation(prose: str, comment_tags: tuple[Tag, ...]) -> bool:
    return_values = []
    for index, tag in enumerate(comment_tags):
        if tag.name not in {"return", "retval"}:
            continue
        end = comment_tags[index + 1].offset if index + 1 < len(comment_tags) else len(prose)
        value = prose[tag.offset + len(tag.name) + 1 : end]
        value = re.sub(r"doxygen-lint:\s*disable=[^\n]+", "", value).strip()
        return_values.append(bool(value) if tag.name == "return" else bool(re.fullmatch(r"\S+\s+\S.*", value, re.S)))
    return bool(return_values) and all(return_values)


def check(context: CommentContext) -> Iterator[Finding | Skip]:
    function = context.declaration.function
    declaration = context.declaration.declaration
    if function is None or context.declaration.details_only:
        return
    assert declaration is not None, "Supported functions have an associated declaration"
    return_type = declaration.child_by_field_name("type")
    return_documented = has_return_documentation(context.example_prose, context.tags)
    trailing_return = next(
        (node for node in function.named_children if node.type == "trailing_return_type"),
        None,
    )
    if trailing_return is not None or (return_type is not None and return_type.text in {b"auto", b"decltype(auto)"}):
        yield Skip("Trailing or deduced return type requires contract review.", suffix=":return")
        return_valid = True
    elif return_type is None:
        return_valid = True
    elif return_type.text == b"void" and declaration.child_by_field_name("declarator") == function:
        return_valid = any(
            tag.name == "par" and re.fullmatch(r"Returns\s+Nothing\.", tag.value) for tag in context.tags
        )
    else:
        return_valid = return_documented
    if not any(tag.name == "brief" for tag in context.tags) or not return_valid:
        yield Finding()
