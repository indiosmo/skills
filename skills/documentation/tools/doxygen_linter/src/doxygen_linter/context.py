"""Prepare immutable comment text and declaration facts for rule evaluation."""

import re
from dataclasses import dataclass

from tree_sitter import Node

from .comments import Tag, body, mask_examples, tags
from .models import AnalysisScope, Finding
from .parsing import Comment, descendants, function_declarator


@dataclass(frozen=True, slots=True)
class AnalysisSkip:
    scopes: tuple[AnalysisScope, ...]
    reason: str


@dataclass(frozen=True, slots=True)
class DeclarationContext:
    declaration: Node | None = None
    template: Node | None = None
    function: Node | None = None
    details_only: bool = False
    skips: tuple[AnalysisSkip, ...] = ()


@dataclass(frozen=True, slots=True)
class CommentContext:
    comment: Comment
    undecorated: str
    prose: str
    example_prose: str
    tags: tuple[Tag, ...]
    example_findings: tuple[Finding, ...]
    declaration: DeclarationContext


def analyze_declaration(comment: Comment, comment_tags: tuple[Tag, ...]) -> DeclarationContext:
    declaration = comment.declaration
    contract_scopes: tuple[AnalysisScope, ...] = ("function", "template")
    structural = {"file", "mainpage", "page", "defgroup", "addtogroup", "name", "ingroup"}
    if comment.text.startswith(("/**<", "/*!<", "///<", "//!<")):
        return DeclarationContext(
            skips=(
                AnalysisSkip(
                    contract_scopes, "Trailing documentation uses Doxygen association; inspect generated reference."
                ),
            )
        )
    if (
        declaration is None
        or declaration.type.startswith("preproc")
        or declaration.type in {"comment", "expression_statement"}
    ):
        skips = (
            ()
            if structural.intersection(tag.name for tag in comment_tags)
            else (
                AnalysisSkip(
                    contract_scopes,
                    "No adjacent supported declaration; macros and detached comments need generated-reference review.",
                ),
            )
        )
        return DeclarationContext(skips=skips)
    if declaration.has_error:
        return DeclarationContext(
            skips=(AnalysisSkip(contract_scopes, "Associated declaration has syntax recovery nodes."),)
        )

    template = declaration if declaration.type == "template_declaration" else None
    if template is not None:
        declaration = next(
            (
                child
                for child in template.named_children
                if child.type not in {"template_parameter_list", "comment", "requires_clause"}
            ),
            declaration,
        )
    function = function_declarator(declaration)
    ambiguous_declarators = len(declaration.children_by_field_name("declarator")) > 1
    function_name = function.child_by_field_name("declarator") if function is not None else None
    indirect_function = function_name is not None and function_name.type == "parenthesized_declarator"
    analysis_skips = []
    if ambiguous_declarators or indirect_function:
        analysis_skips.append(
            AnalysisSkip(
                ("function",),
                "Multiple declarators or function-pointer variable requires generated-reference review.",
            )
        )
        function = None
    if function is None:
        if any(node.type in {"operator_cast", "operator_cast_expression"} for node in descendants(declaration)):
            analysis_skips.append(AnalysisSkip(("function",), "Conversion operator requires contract review."))
        elif declaration.type not in {
            "class_specifier",
            "struct_specifier",
            "enum_specifier",
            "declaration",
            "field_declaration",
            "type_definition",
            "alias_declaration",
        }:
            analysis_skips.append(
                AnalysisSkip(contract_scopes, f"Declaration kind {declaration.type} requires review.")
            )
    contract_tags = {tag.name for tag in comment_tags}
    details_only = (
        declaration.type == "function_definition" and "brief" not in contract_tags and "details" in contract_tags
    )
    return DeclarationContext(declaration, template, function, details_only, tuple(analysis_skips))


def prepare_comment(
    comment: Comment,
    suppression_span: tuple[int, int] | None = None,
    *,
    undecorated: str | None = None,
) -> CommentContext:
    if undecorated is None:
        undecorated = body(comment.text)
    example_prose, example_findings = mask_examples(undecorated)
    # Code spans protect literal command demonstrations while retaining source offsets.
    prose = re.sub(r"`[^`\n]*`", lambda match: " " * len(match[0]), example_prose)
    if suppression_span is not None:
        start, end = suppression_span
        prose = prose[:start] + " " * (end - start) + prose[end:]
    comment_tags = tuple(tags(prose))
    return CommentContext(
        comment,
        undecorated,
        prose,
        example_prose,
        comment_tags,
        example_findings,
        analyze_declaration(comment, comment_tags),
    )
