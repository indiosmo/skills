"""Locate comments and nearby declarations using the C and C++ concrete syntax trees."""

from dataclasses import dataclass

from tree_sitter import Language, Node, Parser
import tree_sitter_c
import tree_sitter_cpp


@dataclass(frozen=True, slots=True)
class Comment:
    node: Node
    text: str
    declaration: Node | None


def descendants(node: Node):
    pending = [node]
    while pending:
        current = pending.pop()
        yield current
        pending.extend(reversed(current.named_children))


def parse(source: bytes, language: str) -> tuple[Node, list[Comment]]:
    grammar = tree_sitter_c.language() if language == "c" else tree_sitter_cpp.language()
    root = Parser(Language(grammar)).parse(source).root_node
    comments = []
    for node in descendants(root):
        if node.type != "comment":
            continue
        text = source[node.start_byte : node.end_byte].decode("utf-8")
        if not text.startswith(("/**", "/*!", "///", "//!")):
            continue
        following = node.next_named_sibling
        if following is not None and source[node.end_byte : following.start_byte].strip():
            following = None
        comments.append(Comment(node, text, following))
    return root, comments


def declarator_name(node: Node | None) -> str | None:
    if node is None:
        return None
    if node.type in {"identifier", "field_identifier", "type_identifier"}:
        return node.text.decode("utf-8")
    declarator = node.child_by_field_name("declarator")
    if declarator is not None:
        return declarator_name(declarator)
    if node.type in {"parenthesized_declarator", "variadic_declarator"}:
        return next(
            (name for child in node.named_children if (name := declarator_name(child))), None
        )
    return None


def function_declarator(declaration: Node) -> Node | None:
    declarator = declaration.child_by_field_name("declarator")
    while declarator is not None:
        if declarator.type == "function_declarator":
            return declarator
        declarator = declarator.child_by_field_name("declarator")
    return None


def parameter_names(parameters: Node) -> tuple[list[str], bool]:
    names = []
    unsupported = any(child.type == "..." for child in parameters.children)
    for parameter in parameters.named_children:
        if parameter.type == "comment":
            continue
        name = declarator_name(parameter.child_by_field_name("declarator"))
        if name:
            names.append(name)
        elif parameter.type == "variadic_parameter":
            unsupported = True
        elif parameter.text != b"void":
            unsupported = True
    return names, unsupported


def template_names(template: Node) -> tuple[list[str], bool]:
    parameters = template.child_by_field_name("parameters")
    names = []
    unsupported = False
    for parameter in parameters.named_children if parameters else []:
        name = declarator_name(parameter.child_by_field_name("declarator"))
        if name is None and parameter.type in {
            "type_parameter_declaration",
            "variadic_type_parameter_declaration",
            "optional_type_parameter_declaration",
        }:
            name = next(
                (
                    child.text.decode("utf-8")
                    for child in parameter.named_children
                    if child.type == "type_identifier"
                ),
                None,
            )
        if name:
            names.append(name)
        else:
            unsupported = True
    return names, unsupported
