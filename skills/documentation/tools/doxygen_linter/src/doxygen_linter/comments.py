"""Parse Doxygen prose while preserving character offsets in the source comment."""

import re
from dataclasses import dataclass

from .models import Finding


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


def mask_examples(text: str) -> tuple[str, tuple[Finding, ...]]:
    characters = list(text)
    active = None
    active_offset = 0
    findings = []
    for match in re.finditer(r"[@\\](code|endcode|verbatim|endverbatim)\b(\{[^\n}]*\})?", text):
        command = match[1]
        if command in {"code", "verbatim"}:
            if active:
                findings.append(Finding(match.start(), "Nested example blocks require separate blocks."))
            else:
                active, active_offset = command, match.start()
            if command == "code" and not re.fullmatch(r"\{\.[A-Za-z0-9+_-]+\}", match[2] or ""):
                findings.append(Finding(match.start(), "Code block needs an explicit language."))
        elif active != command.removeprefix("end"):
            findings.append(Finding(match.start(), "Example closing command has no matching opener."))
        else:
            for index in range(active_offset, match.end()):
                if characters[index] not in "\r\n":
                    characters[index] = " "
            active = None
    if active:
        findings.append(Finding(active_offset, "Example block has no matching closer."))
        for index in range(active_offset, len(characters)):
            if characters[index] not in "\r\n":
                characters[index] = " "
    return "".join(characters), tuple(findings)


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
        if match[1] in block_commands or (not line_prefix.strip() and match[1] not in inline_commands):
            matches.append(match)
    return [
        Tag(
            match[1],
            text[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(text)].strip(),
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
