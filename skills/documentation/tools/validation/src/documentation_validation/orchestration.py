"""Execute declared checks in order and collect their validation evidence."""

from pathlib import Path

from .configuration import Manifest, resolve_check
from .execution import Executor, execute
from .models import CheckResult, CheckStatus, ValidationReport
from .reporting import build_report
from .validators import validate_command, validate_version


def validate(
    manifest: Manifest,
    project: Path,
    skill: Path,
    output: Path,
    *,
    executor: Executor = execute,
) -> ValidationReport:
    output.mkdir(parents=True, exist_ok=True)
    results: list[CheckResult] = []
    statuses: dict[str, CheckStatus] = {}
    for check in manifest.checks:
        resolved = resolve_check(check, project, skill, output)
        result: CheckResult = {
            "name": check.name,
            "scope": check.scope,
            "command": resolved.command,
            "version_command": resolved.version_command,
            "working_directory": str(resolved.directory),
            "status": "skipped",
            "reason": None,
            "version": None,
            "exit_status": None,
            "log": None,
        }
        dependencies = [name for name in check.depends_on if statuses[name] != "pass"]
        if check.skip_reason:
            result["reason"] = check.skip_reason
        elif dependencies:
            result["reason"] = "Prerequisite checks did not pass: " + ", ".join(dependencies)
        else:
            version_log = output / f"{check.name}.version.log"
            execution = executor(resolved.version_command, resolved.directory, check.timeout_seconds, None, version_log)
            result["version"] = version_log.read_text(encoding="utf-8", errors="replace").strip()
            outcome = validate_version(execution)
            log = version_log
            if outcome.status == "pass":
                log = output / f"{check.name}.log"
                execution = executor(resolved.command, resolved.directory, check.timeout_seconds, resolved.stdin, log)
                outcome = validate_command(execution, check.blocked_exit_codes)
            result.update(
                status=outcome.status,
                reason=outcome.reason,
                log=str(log),
                exit_status=execution.exit_status,
            )
        statuses[check.name] = result["status"]
        results.append(result)
    return build_report(project, results)
