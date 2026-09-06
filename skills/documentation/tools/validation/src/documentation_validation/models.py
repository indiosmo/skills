"""Validation outcomes and the JSON evidence contract."""

from dataclasses import dataclass
from typing import Literal, TypedDict

VERSION = "0.1.0"

CheckStatus = Literal["skipped", "blocked", "pass", "fail"]


@dataclass(frozen=True, slots=True)
class ValidationOutcome:
    status: CheckStatus
    reason: str | None = None


class CheckResult(TypedDict):
    name: str
    scope: str
    command: list[str]
    version_command: list[str]
    working_directory: str
    status: CheckStatus
    reason: str | None
    version: str | None
    exit_status: int | None
    log: str | None


class ValidationReport(TypedDict):
    version: str
    checked_at: str
    project: str
    checks: list[CheckResult]
    exit_status: int
    complete: bool
