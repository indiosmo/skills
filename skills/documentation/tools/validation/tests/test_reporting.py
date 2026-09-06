import json
from pathlib import Path
import subprocess
import sys

import pytest

from documentation_validation import Check, Manifest, validate


def check(name: str, code: str = "print('fixture.py:7:2: evidence')", **options) -> Check:
    return Check(name=name, scope="fixture.py", command=[sys.executable, "-c", code],
                 version_command=[sys.executable, "--version"], **options)


def test_order_and_native_evidence(tmp_path: Path):
    report = validate(Manifest(checks=[check("first"), check("second", depends_on=["first"])]),
                      tmp_path, tmp_path, tmp_path / "report")
    assert report["complete"] and report["exit_status"] == 0
    assert [item["name"] for item in report["checks"]] == ["first", "second"]
    assert all(item["version"].startswith("Python") for item in report["checks"])
    assert "fixture.py:7:2" in Path(report["checks"][0]["log"]).read_text()


def test_failure_skips_dependents_but_runs_independent_checks(tmp_path: Path):
    report = validate(Manifest(checks=[check("fail", "raise SystemExit(1)"),
                                     check("dependent", depends_on=["fail"]),
                                     check("independent"),
                                     check("manual", skip_reason="Browser review pending.")]),
                      tmp_path, tmp_path, tmp_path / "report")
    assert report["exit_status"] == 1 and not report["complete"]
    assert [item["status"] for item in report["checks"]] == ["fail", "skipped", "pass", "skipped"]
    assert report["checks"][1]["reason"] == "Prerequisite checks did not pass: fail"
    assert report["checks"][3]["reason"] == "Browser review pending."


@pytest.mark.parametrize("failure", ["missing-command", "timeout", "declared-blocked-exit", "bad-version"])
def test_blocked_results(tmp_path: Path, failure: str):
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
    assert Path(report["checks"][0]["log"]).is_file()


@pytest.mark.parametrize("checks", [[], [check("same"), check("same")],
                                  [check("future", depends_on=["missing"])]] )
def test_invalid_manifests(checks):
    with pytest.raises(ValueError):
        Manifest(checks=checks)


def test_cli_from_consuming_directory_and_literal_arguments(tmp_path: Path):
    manifest = tmp_path / "checks.toml"
    manifest.write_text('''[[checks]]
name = "literal"
scope = "literal command argument"
command = ["{python}", "-c", "import sys; print(sys.argv[1])", "$HOME; `echo unsafe`"]
version_command = ["{python}", "--version"]
'''.replace("{python}", sys.executable))
    result = subprocess.run(["documentation-validate", str(manifest), "--skill", str(tmp_path),
                             "--output", str(tmp_path / "report")], cwd=tmp_path,
                            text=True, capture_output=True, timeout=20, check=False)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["project"] == str(tmp_path)
    assert Path(report["checks"][0]["log"]).read_text() == "$HOME; `echo unsafe`\n"
