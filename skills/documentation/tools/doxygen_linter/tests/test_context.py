"""Prepared prose preserves offsets and declaration associations."""

from doxygen_linter.context import prepare_comment
from doxygen_linter.models import Finding
from doxygen_linter.parsing import parse


def test_masked_examples_keep_command_locations_and_line_endings():
    source = b"/**\r\n * @code{.cpp}\r\n * @param example\r\n * @endcode\r\n * @brief Use `@c`.\r\n */"
    _, comments = parse(source, "cpp")
    context = prepare_comment(comments[0])
    assert len(context.prose) == len(context.comment.text)
    assert [index for index, character in enumerate(context.prose) if character in "\r\n"] == [
        index for index, character in enumerate(context.comment.text) if character in "\r\n"
    ]
    assert [(tag.name, tag.offset) for tag in context.tags] == [("brief", source.index(b"@brief"))]
    assert "`@c`" in context.example_prose
    assert "@c" not in context.prose


def test_unclosed_example_records_syntax_finding_and_masks_payload():
    _, comments = parse(b"/** @code{.cpp}\n@param ignored */", "cpp")
    context = prepare_comment(comments[0])
    assert context.example_findings == (Finding(4, "Example block has no matching closer."),)
    assert context.tags == ()


def test_function_template_shares_function_and_template_analysis():
    _, comments = parse(
        b"/** @details\nRead a value. */\ntemplate<class Value> Value read(Value value) { return value; }", "cpp"
    )
    context = prepare_comment(comments[0])
    assert context.declaration.template is not None
    assert context.declaration.template.type == "template_declaration"
    assert context.declaration.function is not None
    assert context.declaration.function.type == "function_declarator"
    assert context.declaration.declaration is not None
    assert context.declaration.declaration.type == "function_definition"
    assert context.declaration.details_only
    assert context.declaration.skips == ()
