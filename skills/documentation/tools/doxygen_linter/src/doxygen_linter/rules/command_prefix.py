"""Require at-sign prefixes for supported Doxygen commands."""

import re
from collections.abc import Iterator

from ..context import CommentContext
from ..models import Finding, Rule

RULE = Rule(
    "DOX002",
    "Doxygen commands use @.",
    "Replace the command prefix with @.",
    "-commands-instead-of-",
)

COMMAND = re.compile(
    r"\\(?:brief|details|param|tparam|return|retval|ref|ingroup|name|headerfile|par|code|endcode|verbatim|endverbatim|c|p)\b"
)
EXAMPLE_DELIMITERS = {"code", "endcode", "verbatim", "endverbatim"}


def check(context: CommentContext) -> Iterator[Finding]:
    for match in COMMAND.finditer(context.undecorated):
        # Example delimiters are checked alongside prose commands.
        if context.prose[match.start() : match.end()].strip() or match[0][1:] in EXAMPLE_DELIMITERS:
            yield Finding(match.start())
