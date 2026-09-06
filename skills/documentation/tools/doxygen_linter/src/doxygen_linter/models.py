"""Rule metadata, comment-relative findings, and source-level reports."""

from dataclasses import dataclass
from typing import Literal

UPSTREAM = "https://micro-os-plus.github.io/develop/doxygen-style-guide/"
AnalysisScope = Literal["comment", "function", "template"]


@dataclass(frozen=True, slots=True)
class Rule:
    identifier: str
    description: str
    correction: str
    section: str

    @property
    def source(self) -> str:
        return UPSTREAM + "#" + self.section


@dataclass(frozen=True, slots=True)
class Finding:
    offset: int = 0
    explanation: str = ""


@dataclass(frozen=True, slots=True)
class Skip:
    reason: str
    suffix: str = ""


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
