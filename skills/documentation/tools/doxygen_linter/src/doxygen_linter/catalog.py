"""Stable checks and correction text for the adopted Doxygen style."""

from dataclasses import dataclass

UPSTREAM = "https://micro-os-plus.github.io/develop/doxygen-style-guide/"


@dataclass(frozen=True, slots=True)
class Rule:
    identifier: str
    description: str
    correction: str
    section: str

    @property
    def source(self) -> str:
        return UPSTREAM + "#" + self.section


RULES = {
    rule.identifier: rule
    for rule in (
        Rule(
            "DOX001", "Documentation uses a /** block.", "Use /** ... */.", "--comments-instead-of-"
        ),
        Rule(
            "DOX002",
            "Doxygen commands use @.",
            "Replace the command prefix with @.",
            "-commands-instead-of-",
        ),
        Rule(
            "DOX003", "A brief ends with a period.", "End @brief with a period.", "explicit-brief"
        ),
        Rule(
            "DOX004",
            "Details start on a separate line.",
            "Put prose below @details.",
            "explicit-details",
        ),
        Rule(
            "DOX005",
            "Brief and details have a blank line between them.",
            "Insert an empty comment line before @details.",
            "extra-line-between-brief-and-details",
        ),
        Rule(
            "DOX006",
            "A parameter has an explicit direction.",
            "Use @param [in], [out], or [in,out].",
            "use-param-for-function-parameters",
        ),
        Rule(
            "DOX007",
            "Parameter prose starts uppercase and ends with a period.",
            "Write a complete capitalized description ending with a period.",
            "use-param-for-function-parameters",
        ),
        Rule(
            "DOX008",
            "Code and verbatim blocks balance; code declares a language.",
            "Pair @code{.language}/@endcode or @verbatim/@endverbatim.",
            "use-code-for-sequences-of-source-lines",
        ),
        Rule(
            "DOX009",
            "Inline code uses backticks.",
            "Replace @c, @p, or <code> with backticks.",
            "back-apostrophes-for-references-to-code",
        ),
        Rule(
            "DOX010",
            "Documented function parameters match the declaration.",
            "Document each named parameter once and remove unknown names.",
            "use-param-for-function-parameters",
        ),
        Rule(
            "DOX011",
            "Template parameter documentation matches the declaration.",
            "Document each named template parameter once with @tparam.",
            "use-tparam-for-template-parameters",
        ),
        Rule(
            "DOX012",
            "Supported function documentation states a brief and return contract.",
            "Add @brief and a nonempty @return description or @retval value and description; use @par Returns followed by Nothing. for void.",
            "use-brief-with-declarations-and-details-with-definitions",
        ),
    )
}

MANUAL_COVERAGE = [
    "Brief presence and contract completeness on non-function declarations: human review.",
    "Cross-file declaration/definition placement and duplicate details: human review.",
    "API meaning, direction correctness, ownership, lifetime, errors and concurrency: human review.",
    "Header paths, grouping and generated symbol resolution: Doxygen generation and human review.",
    "Lists, tables, links, emphasis, alignment and visual spacing: rendered review.",
    "Prose style: Vale Google package and editorial review.",
]
