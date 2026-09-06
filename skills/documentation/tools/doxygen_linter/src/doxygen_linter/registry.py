"""Explicit registration of rule implementations and their analysis scopes."""

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass

from .context import CommentContext
from .models import AnalysisScope, Finding, Rule, Skip
from .rules import (
    brief_details_spacing,
    brief_period,
    command_prefix,
    details_line,
    documentation_block,
    example_blocks,
    function_contract,
    function_parameters,
    inline_code,
    parameter_description,
    parameter_direction,
    template_parameters,
)


@dataclass(frozen=True, slots=True)
class RegisteredRule:
    metadata: Rule
    check: Callable[[CommentContext], Iterator[Finding | Skip]]
    scope: AnalysisScope = "comment"


REGISTERED_RULES = (
    RegisteredRule(documentation_block.RULE, documentation_block.check),
    RegisteredRule(command_prefix.RULE, command_prefix.check),
    RegisteredRule(brief_period.RULE, brief_period.check),
    RegisteredRule(details_line.RULE, details_line.check),
    RegisteredRule(brief_details_spacing.RULE, brief_details_spacing.check),
    RegisteredRule(parameter_direction.RULE, parameter_direction.check),
    RegisteredRule(parameter_description.RULE, parameter_description.check),
    RegisteredRule(example_blocks.RULE, example_blocks.check),
    RegisteredRule(inline_code.RULE, inline_code.check),
    RegisteredRule(function_parameters.RULE, function_parameters.check, "function"),
    RegisteredRule(template_parameters.RULE, template_parameters.check, "template"),
    RegisteredRule(function_contract.RULE, function_contract.check, "function"),
)


def rule_catalog(rules: Iterable[RegisteredRule]) -> dict[str, Rule]:
    catalog = {}
    for registration in rules:
        identifier = registration.metadata.identifier
        if identifier in catalog:
            raise ValueError(f"Duplicate rule identifier: {identifier}")
        catalog[identifier] = registration.metadata
    return catalog
