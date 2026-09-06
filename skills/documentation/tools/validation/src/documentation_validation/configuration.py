"""Parse ordered check manifests and resolve their invocation paths."""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Check(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str = Field(pattern=r"^[a-z][a-z0-9-]*$")
    scope: str = Field(min_length=1)
    command: list[str] = Field(min_length=1)
    version_command: list[str] = Field(min_length=1)
    depends_on: list[str] = Field(default_factory=list)
    working_directory: str = "."
    timeout_seconds: int = Field(default=60, ge=1)
    stdin: str | None = None
    skip_reason: str | None = Field(default=None, min_length=1)
    blocked_exit_codes: list[int] = Field(default_factory=list)


class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    checks: list[Check] = Field(min_length=1)

    @model_validator(mode="after")
    def ordered_dependencies(self) -> Self:
        preceding: set[str] = set()
        for check in self.checks:
            if check.name in preceding:
                raise ValueError(f"Duplicate check: {check.name}")
            if not set(check.depends_on) <= preceding:
                raise ValueError(f"Dependencies must precede {check.name}")
            preceding.add(check.name)
        return self


@dataclass(frozen=True, slots=True)
class ResolvedCheck:
    command: list[str]
    version_command: list[str]
    directory: Path
    stdin: str | None


def load_manifest(path: Path) -> Manifest:
    return Manifest.model_validate(tomllib.loads(path.read_text(encoding="utf-8")))


def substitute(value: str, paths: dict[str, str]) -> str:
    for name, path in paths.items():
        value = value.replace("{" + name + "}", path)
    return value


def resolve_check(check: Check, project: Path, skill: Path, output: Path) -> ResolvedCheck:
    paths = {"project": str(project), "skill": str(skill), "output": str(output)}
    return ResolvedCheck(
        command=[substitute(argument, paths) for argument in check.command],
        version_command=[substitute(argument, paths) for argument in check.version_command],
        directory=(project / substitute(check.working_directory, paths)).resolve(),
        stdin=substitute(check.stdin, paths) if check.stdin is not None else None,
    )
