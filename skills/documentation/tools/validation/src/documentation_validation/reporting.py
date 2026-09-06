"""Aggregate check evidence and serialize the public report."""

import json
from datetime import UTC, datetime
from pathlib import Path

from .models import VERSION, CheckResult, ValidationReport


def build_report(project: Path, results: list[CheckResult]) -> ValidationReport:
    statuses = [result["status"] for result in results]
    return {
        "version": VERSION,
        "checked_at": datetime.now(UTC).isoformat(),
        "project": str(project),
        "checks": results,
        "exit_status": 2 if "blocked" in statuses else 1 if "fail" in statuses else 0,
        "complete": all(status == "pass" for status in statuses),
    }


def serialize_report(report: ValidationReport) -> str:
    return json.dumps(report, indent=2, ensure_ascii=True) + "\n"


def write_report(report: ValidationReport, path: Path) -> None:
    path.write_text(serialize_report(report), encoding="utf-8")
