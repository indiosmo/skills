import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest
from documentation_validation import Check, Manifest, validate
from documentation_validation.models import CheckResult, CheckStatus
from documentation_validation.reporting import build_report, serialize_report, write_report


def check(
    name: str,
    code: str = "print('fixture.py:7:2: evidence')",
    *,
    depends_on: list[str] | None = None,
    skip_reason: str | None = None,
) -> Check:
    return Check(
        name=name,
        scope="fixture.py",
        command=[sys.executable, "-c", code],
        version_command=[sys.executable, "--version"],
        depends_on=depends_on if depends_on is not None else [],
        skip_reason=skip_reason,
    )


def test_order_and_native_evidence(tmp_path: Path) -> None:
    report = validate(
        Manifest(checks=[check("first"), check("second", depends_on=["first"])]),
        tmp_path,
        tmp_path,
        tmp_path / "report",
    )
    assert report["complete"] and report["exit_status"] == 0
    assert [item["name"] for item in report["checks"]] == ["first", "second"]
    for item in report["checks"]:
        assert item["version"] is not None
        assert item["version"].startswith("Python")
    log = report["checks"][0]["log"]
    assert log is not None
    assert "fixture.py:7:2" in Path(log).read_text()


def test_failure_skips_dependents_but_runs_independent_checks(tmp_path: Path) -> None:
    report = validate(
        Manifest(
            checks=[
                check("fail", "raise SystemExit(1)"),
                check("dependent", depends_on=["fail"]),
                check("independent"),
                check("manual", skip_reason="Browser review pending."),
            ]
        ),
        tmp_path,
        tmp_path,
        tmp_path / "report",
    )
    assert report["exit_status"] == 1 and not report["complete"]
    assert [item["status"] for item in report["checks"]] == ["fail", "skipped", "pass", "skipped"]
    assert report["checks"][1]["reason"] == "Prerequisite checks did not pass: fail"
    assert report["checks"][3]["reason"] == "Browser review pending."


@pytest.mark.parametrize("failure", ["missing-command", "timeout", "declared-blocked-exit", "bad-version"])
def test_blocked_results(tmp_path: Path, failure: str) -> None:
    selected = check("blocked")
    if failure == "missing-command":
        selected.command = ["documentation-fixture-missing-executable"]
    elif failure == "timeout":
        selected.command = [sys.executable, "-c", "import time; time.sleep(5)"]
        selected.timeout_seconds = 1
    elif failure == "declared-blocked-exit":
        selected.command = [sys.executable, "-c", "raise SystemExit(2)"]
        selected.blocked_exit_codes = [2]
    else:
        selected.version_command = [sys.executable, "-c", "raise SystemExit(1)"]
    report = validate(Manifest(checks=[selected]), tmp_path, tmp_path, tmp_path / "report")
    assert report["exit_status"] == 2
    assert report["checks"][0]["status"] == "blocked"
    log = report["checks"][0]["log"]
    assert log is not None
    assert Path(log).is_file()


@pytest.mark.parametrize("checks", [[], [check("same"), check("same")], [check("future", depends_on=["missing"])]])
def test_invalid_manifests(checks: list[Check]) -> None:
    with pytest.raises(ValueError):
        Manifest(checks=checks)


def test_cli_from_consuming_directory_and_literal_arguments(tmp_path: Path) -> None:
    manifest = tmp_path / "checks.toml"
    manifest.write_text(
        """[[checks]]
name = "literal"
scope = "literal command argument"
command = ["{python}", "-c", "import sys; print(sys.argv[1])", "$HOME; `echo unsafe`"]
version_command = ["{python}", "--version"]
""".replace("{python}", sys.executable)
    )
    result = subprocess.run(
        ["documentation-validate", str(manifest), "--skill", str(tmp_path), "--output", str(tmp_path / "report")],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["project"] == str(tmp_path)
    assert Path(report["checks"][0]["log"]).read_text() == "$HOME; `echo unsafe`\n"


@pytest.mark.parametrize(
    ("statuses", "exit_status", "complete"),
    [
        (["pass", "pass"], 0, True),
        (["skipped"], 0, False),
        (["pass", "skipped"], 0, False),
        (["fail", "skipped"], 1, False),
        (["fail", "blocked"], 2, False),
        (["blocked", "fail"], 2, False),
    ],
)
def test_report_aggregates_status_precedence(
    tmp_path: Path, statuses: list[CheckStatus], exit_status: int, complete: bool
) -> None:
    results: list[CheckResult] = [
        {
            "name": f"check-{index}",
            "scope": "selected files",
            "command": ["tool"],
            "version_command": ["tool", "--version"],
            "working_directory": str(tmp_path),
            "status": status,
            "reason": None,
            "version": None,
            "exit_status": None,
            "log": None,
        }
        for index, status in enumerate(statuses)
    ]
    report = build_report(tmp_path, results)
    assert report["exit_status"] == exit_status
    assert report["complete"] is complete
    assert report["checks"] == results
    assert list(report) == ["version", "checked_at", "project", "checks", "exit_status", "complete"]
    assert report["version"] == "0.1.0"
    assert datetime.fromisoformat(report["checked_at"]).utcoffset() is not None


def test_report_serialization_is_ascii_indented_and_newline_terminated(tmp_path: Path) -> None:
    report = build_report(tmp_path / "caf\u00e9", [])
    report["checked_at"] = "2026-09-06T00:00:00+00:00"
    serialized = serialize_report(report)
    assert serialized == (
        '{\n  "version": "0.1.0",\n  "checked_at": "2026-09-06T00:00:00+00:00",\n'
        f'  "project": "{tmp_path}/caf\\u00e9",\n'
        '  "checks": [],\n  "exit_status": 0,\n  "complete": true\n}\n'
    )
    report_path = tmp_path / "report.json"
    write_report(report, report_path)
    assert report_path.read_bytes() == serialized.encode("ascii")
