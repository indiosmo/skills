"""Run ordered project checks and retain native diagnostics."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tomllib

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
    def ordered_dependencies(self):
        preceding = set()
        for check in self.checks:
            if check.name in preceding:
                raise ValueError(f"Duplicate check: {check.name}")
            if not set(check.depends_on) <= preceding:
                raise ValueError(f"Dependencies must precede {check.name}")
            preceding.add(check.name)
        return self


def substitute(value: str, paths: dict[str, str]) -> str:
    for name, path in paths.items():
        value = value.replace("{" + name + "}", path)
    return value


def execute(command: list[str], directory: Path, timeout: int,
            stdin: str | None, log: Path) -> tuple[int | None, str | None]:
    try:
        with log.open("w", encoding="utf-8") as output:
            completed = subprocess.run(command, cwd=directory, input=stdin, text=True,
                                       stdout=output, stderr=subprocess.STDOUT,
                                       timeout=timeout, check=False)
        return completed.returncode, None
    except (OSError, subprocess.TimeoutExpired) as error:
        with log.open("a", encoding="utf-8") as output:
            output.write(f"\n{type(error).__name__}: {error}\n")
        return None, str(error)


def validate(manifest: Manifest, project: Path, skill: Path, output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    paths = {"project": str(project), "skill": str(skill), "output": str(output)}
    results = []
    statuses = {}
    for check in manifest.checks:
        command = [substitute(argument, paths) for argument in check.command]
        version_command = [substitute(argument, paths) for argument in check.version_command]
        directory = (project / substitute(check.working_directory, paths)).resolve()
        result = {"name": check.name, "scope": check.scope, "command": command,
                  "version_command": version_command, "working_directory": str(directory),
                  "status": "skipped", "reason": None, "version": None,
                  "exit_status": None, "log": None}
        dependencies = [name for name in check.depends_on if statuses[name] != "pass"]
        if check.skip_reason:
            result["reason"] = check.skip_reason
        elif dependencies:
            result["reason"] = "Prerequisite checks did not pass: " + ", ".join(dependencies)
        else:
            version_log = output / f"{check.name}.version.log"
            version_exit, version_error = execute(version_command, directory,
                                                 check.timeout_seconds, None, version_log)
            result["version"] = version_log.read_text(encoding="utf-8", errors="replace").strip()
            if version_exit != 0:
                result.update(status="blocked", reason=version_error or "Version command failed",
                              log=str(version_log), exit_status=version_exit)
            else:
                log = output / f"{check.name}.log"
                stdin = substitute(check.stdin, paths) if check.stdin is not None else None
                exit_status, error = execute(command, directory, check.timeout_seconds, stdin, log)
                status = ("blocked" if error or exit_status in check.blocked_exit_codes
                          else "pass" if exit_status == 0 else "fail")
                result.update(status=status, reason=error, log=str(log), exit_status=exit_status)
        statuses[check.name] = result["status"]
        results.append(result)
    exit_status = 2 if "blocked" in statuses.values() else 1 if "fail" in statuses.values() else 0
    return {"version": "0.1.0", "checked_at": datetime.now(timezone.utc).isoformat(),
            "project": str(project), "checks": results, "exit_status": exit_status,
            "complete": all(status == "pass" for status in statuses.values())}


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--skill", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version", action="version", version="0.1.0")
    options = parser.parse_args(arguments)
    try:
        manifest = Manifest.model_validate(tomllib.loads(options.manifest.read_text(encoding="utf-8")))
        report = validate(manifest, options.project.resolve(), options.skill.resolve(),
                          options.output.resolve())
        report_path = options.output.resolve() / "report.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"blocked: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return report["exit_status"]
