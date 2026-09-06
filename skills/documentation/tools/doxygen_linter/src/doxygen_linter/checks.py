"""Run registered rules and translate their findings into source-level reports."""

import re
from collections.abc import Mapping, Sequence

from .comments import body
from .context import prepare_comment
from .models import Coverage as Coverage
from .models import Diagnostic as Diagnostic
from .models import Skip
from .parsing import parse
from .registry import REGISTERED_RULES, RegisteredRule, rule_catalog


def lint(
    source: bytes,
    path: str,
    language: str,
    severities: Mapping[str, str] | None = None,
    *,
    rules: Sequence[RegisteredRule] = REGISTERED_RULES,
) -> tuple[list[Diagnostic], list[Coverage]]:
    severities = severities or {}
    catalog = rule_catalog(rules)
    root, comments = parse(source, language)
    diagnostics = []
    coverage = []
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
        line_start = comment.node.start_byte - comment.node.start_point.column
        comment_column = len(source[line_start : comment.node.start_byte].decode("utf-8")) + 1
        undecorated = body(comment.text)
        suppression = re.search(r"doxygen-lint:\s*disable=([^\n]+)", undecorated)
        suppressed = set()
        suppression_span = None
        if suppression:
            requested, separator, reason = suppression[1].partition(" -- ")
            suppressed = set(requested.strip().split(","))
            if not separator or not reason.strip() or not suppressed <= catalog.keys():
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
                coverage.append(Coverage(path, line, ",".join(sorted(suppressed)), "skipped", reason.strip()))
                suppression_span = suppression.span()
        context = prepare_comment(comment, suppression_span, undecorated=undecorated)
        for analysis_skip in context.declaration.skips:
            identifiers = sorted(rule.metadata.identifier for rule in rules if rule.scope in analysis_skip.scopes)
            if identifiers:
                coverage.append(Coverage(path, line, ",".join(identifiers), "skipped", analysis_skip.reason))
        for registration in rules:
            if registration.scope == "function" and context.declaration.function is None:
                continue
            if registration.scope == "template" and context.declaration.template is None:
                continue
            rule = registration.metadata
            for result in registration.check(context):
                if isinstance(result, Skip):
                    coverage.append(Coverage(path, line, rule.identifier + result.suffix, "skipped", result.reason))
                elif rule.identifier not in suppressed:
                    prefix = comment.text[: result.offset]
                    diagnostics.append(
                        Diagnostic(
                            rule.identifier,
                            path,
                            line + prefix.count("\n"),
                            len(prefix.rsplit("\n", 1)[-1]) + 1 + (comment_column - 1 if "\n" not in prefix else 0),
                            severities.get(rule.identifier, "warning"),
                            result.explanation or rule.description,
                            rule.correction,
                            rule.source,
                        )
                    )
    diagnostics.sort(key=lambda diagnostic: (diagnostic.line, diagnostic.column, diagnostic.rule))
    return diagnostics, coverage
