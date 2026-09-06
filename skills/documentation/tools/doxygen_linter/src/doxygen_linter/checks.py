"""Evaluate comment-local style and syntactically supported API contracts."""

from collections import Counter
from dataclasses import dataclass
import re

from .catalog import RULES
from .parsing import (
    Comment,
    descendants,
    function_declarator,
    parameter_names,
    parse,
    template_names,
)


@dataclass(frozen=True, slots=True)
class Diagnostic:
    rule: str
    path: str
    line: int
    column: int
    severity: str
    explanation: str
    correction: str
    source: str


@dataclass(frozen=True, slots=True)
class Coverage:
    path: str
    line: int
    checks: str
    status: str
    reason: str


@dataclass(frozen=True, slots=True)
class Tag:
    name: str
    value: str
    offset: int


def body(text: str) -> str:
    characters = list(text)
    prefix = 4 if text.startswith(("/**<", "/*!<", "///<", "//!<")) else 3
    characters[:prefix] = " " * prefix
    if text.endswith("*/"):
        characters[-2:] = "  "
    undecorated = "".join(characters)
    return re.sub(r"(?m)^(\s*)\*(?=\s|$)", lambda match: match[1] + " ", undecorated)


def mask_examples(text: str) -> tuple[str, list[tuple[int, str]]]:
    characters = list(text)
    active = None
    active_offset = 0
    findings = []
    for match in re.finditer(r"[@\\](code|endcode|verbatim|endverbatim)\b(\{[^\n}]*\})?", text):
        command = match[1]
        if command in {"code", "verbatim"}:
            if active:
                findings.append((match.start(), "Nested example blocks require separate blocks."))
            else:
                active, active_offset = command, match.start()
            if command == "code" and not re.fullmatch(r"\{\.[A-Za-z0-9+_-]+\}", match[2] or ""):
                findings.append((match.start(), "Code block needs an explicit language."))
        elif active != command.removeprefix("end"):
            findings.append((match.start(), "Example closing command has no matching opener."))
        else:
            for index in range(active_offset, match.end()):
                if characters[index] not in "\r\n":
                    characters[index] = " "
            active = None
    if active:
        findings.append((active_offset, "Example block has no matching closer."))
        for index in range(active_offset, len(characters)):
            if characters[index] not in "\r\n":
                characters[index] = " "
    return "".join(characters), findings


def tags(text: str) -> list[Tag]:
    inline_commands = {
        "ref",
        "c",
        "p",
        "a",
        "b",
        "e",
        "em",
        "anchor",
        "link",
        "endlink",
        "cite",
        "emoji",
    }
    block_commands = {
        "brief",
        "details",
        "param",
        "tparam",
        "return",
        "returns",
        "retval",
        "par",
        "file",
        "mainpage",
        "page",
        "defgroup",
        "addtogroup",
        "name",
        "ingroup",
        "headerfile",
        "see",
        "sa",
        "note",
        "warning",
        "attention",
        "remark",
        "remarks",
        "pre",
        "post",
        "invariant",
        "exception",
        "throw",
        "throws",
        "since",
        "deprecated",
        "todo",
        "bug",
        "test",
        "author",
        "authors",
        "version",
        "date",
        "copyright",
        "snippet",
        "include",
        "section",
        "subsection",
        "subsubsection",
    }
    matches = []
    for match in re.finditer(r"(?<![\w@\\])[@\\]([A-Za-z]+)\b", text):
        line_prefix = text[: match.start()].rsplit("\n", 1)[-1]
        if match[1] in block_commands or (
            not line_prefix.strip() and match[1] not in inline_commands
        ):
            matches.append(match)
    return [
        Tag(
            match[1],
            text[
                match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(text)
            ].strip(),
            match.start(),
        )
        for index, match in enumerate(matches)
    ]


def parameter_tag(tag: Tag) -> tuple[str | None, str, bool]:
    match = re.fullmatch(r"(?:\[([^]]*)\]\s*)?([A-Za-z_]\w*)\s*(.*)", tag.value, re.S)
    if not match:
        return None, "", False
    direction = (match[1] or "").replace(" ", "")
    return match[2], match[3].strip(), direction in {"in", "out", "in,out", "out,in"}


def has_return_documentation(prose: str, comment_tags: list[Tag]) -> bool:
    return_values = []
    for index, tag in enumerate(comment_tags):
        if tag.name not in {"return", "retval"}:
            continue
        end = comment_tags[index + 1].offset if index + 1 < len(comment_tags) else len(prose)
        value = prose[tag.offset + len(tag.name) + 1 : end]
        value = re.sub(r"doxygen-lint:\s*disable=[^\n]+", "", value).strip()
        return_values.append(
            bool(value) if tag.name == "return" else bool(re.fullmatch(r"\S+\s+\S.*", value, re.S))
        )
    return bool(return_values) and all(return_values)


def lint(
    source: bytes, path: str, language: str, severities: dict[str, str] | None = None
) -> tuple[list[Diagnostic], list[Coverage]]:
    severities = severities or {}
    root, comments = parse(source, language)
    diagnostics = []
    coverage = []

    def emit(comment: Comment, identifier: str, offset: int = 0, explanation: str = ""):
        rule = RULES[identifier]
        prefix = source[: comment.node.start_byte].decode("utf-8") + comment.text[:offset]
        diagnostics.append(
            Diagnostic(
                identifier,
                path,
                prefix.count("\n") + 1,
                len(prefix.rsplit("\n", 1)[-1]) + 1,
                severities.get(identifier, "warning"),
                explanation or rule.description,
                rule.correction,
                rule.source,
            )
        )

    if root.has_error:
        coverage.append(
            Coverage(
                path,
                1,
                "syntax",
                "blocked",
                "Source contains ERROR or missing syntax nodes; repair source or review dialect support.",
            )
        )
    for comment in comments:
        line = comment.node.start_point.row + 1
        undecorated = body(comment.text)
        prose, block_findings = mask_examples(undecorated)
        example_prose = prose
        # Code spans protect literal command demonstrations while retaining source offsets.
        prose = re.sub(r"`[^`\n]*`", lambda match: " " * len(match[0]), prose)
        comment_tags = tags(prose)
        suppression = re.search(r"doxygen-lint:\s*disable=([^\n]+)", undecorated)
        suppressed = set()
        if suppression:
            requested, separator, reason = suppression[1].partition(" -- ")
            suppressed = set(requested.strip().split(","))
            if not separator or not reason.strip() or not suppressed <= RULES.keys():
                coverage.append(
                    Coverage(
                        path,
                        line,
                        "suppression",
                        "blocked",
                        "Use disable=DOX001,DOX002 -- a nonempty reason with known rule IDs.",
                    )
                )
                suppressed = set()
            else:
                coverage.append(
                    Coverage(path, line, ",".join(sorted(suppressed)), "skipped", reason.strip())
                )
                prose = (
                    prose[: suppression.start()]
                    + " " * (suppression.end() - suppression.start())
                    + prose[suppression.end() :]
                )
                comment_tags = tags(prose)
        first_diagnostic = len(diagnostics)
        if not comment.text.startswith("/**"):
            emit(comment, "DOX001")
        for match in re.finditer(
            r"\\(?:brief|details|param|tparam|return|retval|ref|ingroup|name|headerfile|par|code|endcode|verbatim|endverbatim|c|p)\b",
            undecorated,
        ):
            # Example payloads are masked, but their command delimiters are also checked.
            if prose[match.start() : match.end()].strip() or match[0][1:] in {
                "code",
                "endcode",
                "verbatim",
                "endverbatim",
            }:
                emit(comment, "DOX002", match.start())
        for offset, explanation in block_findings:
            emit(comment, "DOX008", offset, explanation)
        for match in re.finditer(r"[@\\](?:c|p)\s+|<code\b", prose):
            emit(comment, "DOX009", match.start())
        for tag in comment_tags:
            if tag.name == "brief" and (not tag.value or not tag.value.endswith(".")):
                emit(comment, "DOX003", tag.offset)
            if tag.name == "details":
                after_command = prose[tag.offset + len("@details") :].split("\n", 1)[0]
                if after_command.strip():
                    emit(comment, "DOX004", tag.offset)
                preceding = prose[: tag.offset].splitlines()
                if (
                    any(previous.name == "brief" for previous in comment_tags)
                    and len(preceding) > 1
                    and preceding[-2].strip()
                ):
                    emit(comment, "DOX005", tag.offset)
            if tag.name in {"param", "tparam"}:
                name, description, direction = parameter_tag(tag)
                if tag.name == "param" and not direction:
                    emit(comment, "DOX006", tag.offset)
                if not description or not description[0].isupper() or not description.endswith("."):
                    emit(comment, "DOX007", tag.offset)
        structural = {"file", "mainpage", "page", "defgroup", "addtogroup", "name", "ingroup"}
        declaration = comment.declaration
        if comment.text.startswith(("/**<", "/*!<", "///<", "//!<")):
            coverage.append(
                Coverage(
                    path,
                    line,
                    "DOX010,DOX011,DOX012",
                    "skipped",
                    "Trailing documentation uses Doxygen association; inspect generated reference.",
                )
            )
        elif (
            declaration is None
            or declaration.type.startswith("preproc")
            or declaration.type in {"comment", "expression_statement"}
        ):
            if not structural.intersection(tag.name for tag in comment_tags):
                coverage.append(
                    Coverage(
                        path,
                        line,
                        "DOX010,DOX011,DOX012",
                        "skipped",
                        "No adjacent supported declaration; macros and detached comments need generated-reference review.",
                    )
                )
        elif declaration.has_error:
            coverage.append(
                Coverage(
                    path,
                    line,
                    "DOX010,DOX011,DOX012",
                    "skipped",
                    "Associated declaration has syntax recovery nodes.",
                )
            )
        else:
            template = declaration if declaration.type == "template_declaration" else None
            if template is not None:
                expected, unsupported = template_names(template)
                if unsupported:
                    coverage.append(
                        Coverage(
                            path,
                            line,
                            "DOX011",
                            "skipped",
                            "Unnamed or nested template parameter requires review.",
                        )
                    )
                else:
                    documented = [
                        parameter_tag(tag)[0] for tag in comment_tags if tag.name == "tparam"
                    ]
                    if Counter(expected) != Counter(documented):
                        emit(
                            comment,
                            "DOX011",
                            explanation=f"Expected template parameters {expected}; documented {documented}.",
                        )
                declaration = next(
                    (
                        child
                        for child in template.named_children
                        if child.type
                        not in {"template_parameter_list", "comment", "requires_clause"}
                    ),
                    declaration,
                )
            function = function_declarator(declaration)
            ambiguous_declarators = len(declaration.children_by_field_name("declarator")) > 1
            indirect_function = (
                function is not None
                and function.child_by_field_name("declarator").type == "parenthesized_declarator"
            )
            if ambiguous_declarators or indirect_function:
                coverage.append(
                    Coverage(
                        path,
                        line,
                        "DOX010,DOX012",
                        "skipped",
                        "Multiple declarators or function-pointer variable requires generated-reference review.",
                    )
                )
                function = None
            if function is not None:
                parameters = function.child_by_field_name("parameters")
                expected, unsupported = parameter_names(parameters)
                definition = declaration.type == "function_definition"
                contract_tags = {tag.name for tag in comment_tags}
                details_only = (
                    definition and "brief" not in contract_tags and "details" in contract_tags
                )
                if unsupported:
                    coverage.append(
                        Coverage(
                            path,
                            line,
                            "DOX010",
                            "skipped",
                            "Unnamed, variadic or unsupported parameter requires review.",
                        )
                    )
                elif not details_only:
                    documented = [
                        parameter_tag(tag)[0] for tag in comment_tags if tag.name == "param"
                    ]
                    empty_parameters = any(
                        tag.name == "par" and re.fullmatch(r"Parameters\s+None\.", tag.value)
                        for tag in comment_tags
                    )
                    if Counter(expected) != Counter(documented) or (
                        not expected and not empty_parameters
                    ):
                        emit(
                            comment,
                            "DOX010",
                            explanation=f"Expected parameters {expected}; documented {documented}; zero parameters use @par Parameters / None.",
                        )
                if not details_only:
                    return_type = declaration.child_by_field_name("type")
                    return_documented = has_return_documentation(example_prose, comment_tags)
                    trailing_return = next(
                        (
                            node
                            for node in function.named_children
                            if node.type == "trailing_return_type"
                        ),
                        None,
                    )
                    if trailing_return is not None or (
                        return_type is not None and return_type.text in {b"auto", b"decltype(auto)"}
                    ):
                        coverage.append(
                            Coverage(
                                path,
                                line,
                                "DOX012:return",
                                "skipped",
                                "Trailing or deduced return type requires contract review.",
                            )
                        )
                        return_valid = True
                    elif return_type is None:
                        return_valid = True
                    elif (
                        return_type.text == b"void"
                        and declaration.child_by_field_name("declarator").type
                        == "function_declarator"
                    ):
                        return_valid = any(
                            tag.name == "par" and re.fullmatch(r"Returns\s+Nothing\.", tag.value)
                            for tag in comment_tags
                        )
                    else:
                        return_valid = return_documented
                    if "brief" not in contract_tags or not return_valid:
                        emit(comment, "DOX012")
            elif any(
                node.type in {"operator_cast", "operator_cast_expression"}
                for node in descendants(declaration)
            ):
                coverage.append(
                    Coverage(
                        path,
                        line,
                        "DOX010,DOX012",
                        "skipped",
                        "Conversion operator requires contract review.",
                    )
                )
            elif declaration.type not in {
                "class_specifier",
                "struct_specifier",
                "enum_specifier",
                "declaration",
                "field_declaration",
                "type_definition",
                "alias_declaration",
            }:
                coverage.append(
                    Coverage(
                        path,
                        line,
                        "DOX010,DOX011,DOX012",
                        "skipped",
                        f"Declaration kind {declaration.type} requires review.",
                    )
                )
        diagnostics[first_diagnostic:] = [
            diagnostic
            for diagnostic in diagnostics[first_diagnostic:]
            if diagnostic.rule not in suppressed
        ]
    return diagnostics, coverage
