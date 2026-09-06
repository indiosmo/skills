"""Exercise the installed command's input and evidence contracts."""

import json
import subprocess
import sys
from pathlib import Path

import pytest


def invoke(*arguments: str, directory: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["documentation-validate", *arguments],
        cwd=directory,
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )


def manifest_text(command: str) -> str:
    return "\n".join(
        [
            "[[checks]]",
            'name = "fixture"',
            'scope = "CLI fixture"',
            f"command = {json.dumps([sys.executable, '-c', command])}",
            f"version_command = {json.dumps([sys.executable, '--version'])}",
        ]
    )


@pytest.mark.parametrize("option", ["--help", "--version"])
def test_information_options_need_no_manifest(tmp_path: Path, option: str) -> None:
    result = invoke(option, directory=tmp_path)
    assert result.returncode == 0
    assert result.stderr == ""
    if option == "--version":
        assert result.stdout == "0.1.0\n"
    else:
        assert "Run ordered project checks and retain native diagnostics." in result.stdout
        assert "--project" in result.stdout
        assert "--skill" in result.stdout
        assert "--output" in result.stdout
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("invalid_suffix", ["\ninvalid = [", "\nunknown_field = true"])
def test_invalid_manifest_prevents_execution(tmp_path: Path, invalid_suffix: str) -> None:
    manifest = tmp_path / "checks.toml"
    manifest.write_text(
        manifest_text("from pathlib import Path; Path('executed').touch()") + invalid_suffix,
        encoding="utf-8",
    )
    output = tmp_path / "report"
    result = invoke(str(manifest), "--skill", str(tmp_path), "--output", str(output), directory=tmp_path)
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.startswith("blocked: ")
    assert not (tmp_path / "executed").exists()
    assert not output.exists()


def test_output_file_blocks_execution(tmp_path: Path) -> None:
    manifest = tmp_path / "checks.toml"
    manifest.write_text(manifest_text("from pathlib import Path; Path('executed').touch()"), encoding="utf-8")
    output = tmp_path / "report"
    output.write_text("existing content", encoding="utf-8")
    result = invoke(str(manifest), "--skill", str(tmp_path), "--output", str(output), directory=tmp_path)
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.startswith("blocked: ")
    assert output.read_text(encoding="utf-8") == "existing content"
    assert not (tmp_path / "executed").exists()


@pytest.mark.parametrize(
    ("native_exit", "extra_fields", "expected_exit", "expected_status", "complete"),
    [
        (0, "", 0, "pass", True),
        (1, "", 1, "fail", False),
        (2, "\nblocked_exit_codes = [2]", 2, "blocked", False),
        (1, '\nskip_reason = "Manual review pending."', 0, "skipped", False),
    ],
)
def test_cli_exit_and_report_agree(
    tmp_path: Path,
    native_exit: int,
    extra_fields: str,
    expected_exit: int,
    expected_status: str,
    complete: bool,
) -> None:
    manifest = tmp_path / "checks.toml"
    manifest.write_text(manifest_text(f"print('native evidence'); raise SystemExit({native_exit})") + extra_fields)
    output = tmp_path / "report"
    result = invoke(str(manifest), "--skill", str(tmp_path), "--output", str(output), directory=tmp_path)
    assert result.returncode == expected_exit
    assert result.stderr == ""
    assert result.stdout == (output / "report.json").read_text(encoding="utf-8")
    assert result.stdout.endswith("\n")
    report = json.loads(result.stdout)
    assert report["exit_status"] == expected_exit
    assert report["complete"] is complete
    assert report["checks"][0]["status"] == expected_status
    if expected_status == "skipped":
        assert report["checks"][0]["log"] is None
        assert list(output.iterdir()) == [output / "report.json"]
    else:
        assert Path(report["checks"][0]["log"]).read_text(encoding="utf-8") == "native evidence\n"
