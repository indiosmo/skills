"""Run the complete native-tool workflow against a consuming-project copy."""

import json
from pathlib import Path
import shutil
import subprocess

import pytest


SKILL = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("defect,expected", [
    ("valid", None), ("vale", "vale"), ("comment", "doxygen-style"),
    ("symbol", "reference"), ("page", "site"), ("link", "local-links"),
    ("example", "run-example"),
    ("empty-selection", "link-coverage"), ("all-excluded", "link-coverage"),
])
def test_native_workflow(tmp_path: Path, defect: str, expected: str | None):
    project = Path(shutil.copytree(SKILL / "tests/environment/fixture", tmp_path / "consumer"))
    header = project / "include/gain.hpp"
    header.write_text(header.read_text().replace("@param ", "@param [in] "))
    if defect == "vale":
        with (project / "docs/gain.md").open("a") as page:
            page.write("\nWe use DoxyGen.\n")
    elif defect == "comment":
        header.write_text(header.read_text().replace("@param [in] gain", "@param gain"))
    elif defect == "symbol":
        header.write_text(header.read_text().replace("@see apply_gain(float)", "@see @ref missing_symbol"))
    elif defect == "page":
        page = project / "docs/index.md"
        page.write_text(page.read_text().replace("#verify-the-result", "#missing-anchor"))
    elif defect == "link":
        # Raw HTML is copied into the generated site and checked by lychee.
        (project / "docs/broken.html").write_text('<a href="missing.html">Reference</a>')
    elif defect == "example":
        header.write_text(header.read_text().replace("sample * gain", "sample + gain"))
    manifest = project / "checks.toml"
    manifest_text = (SKILL / "tests/validation/fixture.toml").read_text()
    if defect == "empty-selection":
        manifest_text = manifest_text.replace("{output}/site/**/*.html", "{output}/missing/**/*.html")
    elif defect == "all-excluded":
        (project / "docs/unverified.html").write_text(
            '<a href="https://example.invalid/private">Unverified</a>')
        manifest_text = manifest_text.replace("{output}/site/**/*.html", "{project}/docs/unverified.html")
    manifest.write_text(manifest_text)
    output = tmp_path / "validation"
    result = subprocess.run(
        ["uv", "run", "--project", str(SKILL / "tools/validation"), "--frozen",
         "documentation-validate", str(manifest),
         "--skill", str(SKILL), "--output", str(output)],
        cwd=project, text=True, capture_output=True, timeout=60, check=False,
    )
    report = json.loads(result.stdout)
    statuses = {check["name"]: check["status"] for check in report["checks"]}
    assert statuses["external-links"] == "skipped"
    assert not report["complete"]
    if expected is None:
        assert result.returncode == 0, result.stdout + result.stderr
        assert set(statuses.values()) == {"pass", "skipped"}
    elif defect in {"empty-selection", "all-excluded"}:
        assert result.returncode == 2, result.stdout + result.stderr
        assert statuses[expected] == "blocked", result.stdout
        native_report = json.loads((output / "local-links.json").read_text())
        assert native_report["successful"] == 0
        if defect == "empty-selection":
            assert native_report["total"] == 0
        else:
            assert native_report["total"] == native_report["excludes"] == 1
    else:
        assert result.returncode == 1, result.stdout + result.stderr
        assert statuses[expected] == "fail", result.stdout
    assert (output / "report.json").is_file()
    for check in report["checks"]:
        if check["status"] in {"pass", "fail"}:
            assert check["version"] and Path(check["log"]).is_file()
    if defect == "valid":
        assert "index.html" in (output / "link-inputs.log").read_text()
