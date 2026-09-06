"""Exercise manifest constraints and literal invocation resolution."""

from pathlib import Path

import pytest
from documentation_validation.configuration import Check, Manifest, load_manifest, resolve_check


def check_data(name: str = "fixture", /, **overrides: object) -> dict[str, object]:
    return {
        "name": name,
        "scope": "selected files",
        "command": ["native-tool"],
        "version_command": ["native-tool", "--version"],
        **overrides,
    }


@pytest.mark.parametrize(
    "overrides",
    [
        {"name": "Uppercase"},
        {"scope": ""},
        {"command": []},
        {"version_command": []},
        {"command": [1]},
        {"timeout_seconds": "60"},
        {"timeout_seconds": 0},
        {"skip_reason": ""},
        {"blocked_exit_codes": ["2"]},
        {"unknown": True},
    ],
)
def test_check_rejects_invalid_fields(overrides: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        Check.model_validate(check_data(**overrides))


@pytest.mark.parametrize("dependencies", [["second"], ["first"], ["missing"]])
def test_dependencies_must_precede_check(dependencies: list[str]) -> None:
    with pytest.raises(ValueError, match="Dependencies must precede first"):
        Manifest.model_validate({"checks": [check_data("first", depends_on=dependencies), check_data("second")]})


def test_manifest_preserves_declared_order_and_dependencies(tmp_path: Path) -> None:
    manifest_path = tmp_path / "checks.toml"
    manifest_path.write_text(
        '[[checks]]\nname="first"\nscope="first files"\ncommand=["one"]\nversion_command=["one", "--version"]\n'
        '[[checks]]\nname="second"\nscope="second files"\ncommand=["two"]\nversion_command=["two", "--version"]\n'
        'depends_on=["first"]\n',
        encoding="utf-8",
    )
    manifest = load_manifest(manifest_path)
    assert [check.name for check in manifest.checks] == ["first", "second"]
    assert manifest.checks[1].depends_on == ["first"]
    assert manifest.checks[0].timeout_seconds == 60


@pytest.mark.parametrize("working_directory", ["docs", "{project}/docs"])
def test_resolve_all_invocation_fields_without_changing_configuration(tmp_path: Path, working_directory: str) -> None:
    project = tmp_path / "consumer"
    skill = tmp_path / "skill"
    output = tmp_path / "evidence"
    check = Check.model_validate(
        check_data(
            command=["{skill}/tool", "{project}", "{output}", "$HOME; `echo literal`", "{unknown}"],
            version_command=["{skill}/tool", "--version"],
            working_directory=working_directory,
            stdin="{project}\n{skill}\n{output}",
        )
    )
    resolved = resolve_check(check, project, skill, output)
    assert resolved.command == [str(skill / "tool"), str(project), str(output), "$HOME; `echo literal`", "{unknown}"]
    assert resolved.version_command == [str(skill / "tool"), "--version"]
    assert resolved.directory == project / "docs"
    assert resolved.stdin == f"{project}\n{skill}\n{output}"
    assert check.command[0] == "{skill}/tool"
    assert check.working_directory == working_directory
    assert not output.exists()
