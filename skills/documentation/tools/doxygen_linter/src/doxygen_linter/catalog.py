"""Registered rule metadata and review coverage for the adopted Doxygen style."""

from .models import UPSTREAM as UPSTREAM
from .models import Rule as Rule
from .registry import REGISTERED_RULES, rule_catalog

RULES = rule_catalog(REGISTERED_RULES)

MANUAL_COVERAGE = [
    "Brief presence and contract completeness on non-function declarations: human review.",
    "Cross-file declaration/definition placement and duplicate details: human review.",
    "API meaning, direction correctness, ownership, lifetime, errors and concurrency: human review.",
    "Header paths, grouping and generated symbol resolution: Doxygen generation and human review.",
    "Lists, tables, links, emphasis, alignment and visual spacing: rendered review.",
    "Prose style: Vale Google package and editorial review.",
]
