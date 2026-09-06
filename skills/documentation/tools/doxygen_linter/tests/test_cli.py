"""Exercise discovery and machine-readable command contracts."""

import json
import os

import pytest
from doxygen_linter.catalog import RULES
from doxygen_linter.cli import main


def run(capsys, *arguments):
    status = main(["--format", "json", *map(str, arguments)])
    return status, json.loads(capsys.readouterr().out)


def test_directory_discovery_exclusions_and_duplicate_paths(tmp_path, capsys):
    source = tmp_path / "valid.c"
    source.write_text("/** @file valid.c */\nint count;")
    generated = tmp_path / "generated"
    generated.mkdir()
    (generated / "invalid.c").write_text("/** @brief Invalid */")
    (tmp_path / "readme.md").write_text("Ignored prose")
    status, report = run(capsys, tmp_path, source)
    assert status == 0
    assert report["checked_files"] == 1
    assert report["coverage"][0]["status"] == "skipped"


def test_symlinks_are_skipped_including_directory_cycle(tmp_path, capsys):
    (tmp_path / "valid.c").write_text("int count;")
    (tmp_path / "cycle").symlink_to(tmp_path, target_is_directory=True)
    (tmp_path / "link.c").symlink_to(tmp_path / "valid.c")
    status, report = run(capsys, tmp_path)
    assert status == 0
    assert report["checked_files"] == 1
    assert len(report["coverage"]) == 2


@pytest.mark.parametrize(
    "filename,content",
    [("bad.c", b"\xff"), ("nul.c", b"\x00"), ("bad.rs", b""), ("broken.c", b"int read(;")],
)
def test_uncheckable_inputs_are_blocked(tmp_path, capsys, filename, content):
    source = tmp_path / filename
    source.write_bytes(content)
    status, report = run(capsys, source)
    assert status == 2
    assert report["status"] == "blocked"


def test_missing_and_empty_input(tmp_path, capsys):
    assert run(capsys, tmp_path / "missing.c")[0] == 2
    assert run(capsys, tmp_path)[0] == 2
    assert run(capsys)[0] == 2


def test_rule_severity_and_failure_threshold(tmp_path, capsys):
    source = tmp_path / "bad.c"
    source.write_text("/** @brief Invalid */\nint count;")
    configuration = tmp_path / "lint.toml"
    configuration.write_text('[severity]\nDOX003 = "error"\n')
    assert run(capsys, source)[0] == 1
    assert run(capsys, source, "--fail-on", "error")[0] == 0
    status, report = run(capsys, source, "--config", configuration, "--fail-on", "error")
    assert status == 1
    assert report["diagnostics"][0]["severity"] == "error"


@pytest.mark.parametrize(
    "configuration",
    [
        "unknown = true",
        '[severity]\nDOX999 = "error"',
        'extensions = [".rs"]',
        "exclude = 42",
        "invalid TOML",
    ],
)
def test_invalid_configuration_is_structured(tmp_path, capsys, configuration):
    configuration_file = tmp_path / "lint.toml"
    configuration_file.write_text(configuration)
    status, report = run(capsys, tmp_path, "--config", configuration_file)
    assert status == 2
    assert report["coverage"][0]["checks"] == "configuration"


def test_explicit_language_and_extensions(tmp_path, capsys):
    source = tmp_path / "valid.h"
    source.write_text("int count;")
    assert run(capsys, source, "--language", "c", "--extensions", ".h")[0] == 0
    assert run(capsys, source, "--extensions", ".cpp")[0] == 2


def test_additional_exclusion(tmp_path, capsys):
    (tmp_path / "valid.c").write_text("int count;")
    (tmp_path / "bad.c").write_text("/** @brief Invalid */")
    assert run(capsys, tmp_path, "--exclude", "**/bad.c")[0] == 0


def test_text_output_and_catalog(tmp_path, capsys):
    source = tmp_path / "bad.c"
    source.write_text("/** @brief Invalid */\nint count;")
    assert main([str(source)]) == 1
    output = capsys.readouterr().out
    assert ":1:5: warning DOX003:" in output
    assert "Correction:" in output
    assert main(["--catalog"]) == 0
    catalog = json.loads(capsys.readouterr().out)
    assert catalog.keys() == RULES.keys()
    assert catalog["DOX003"]["source"].endswith("#explicit-brief")


def test_fifo_source_is_blocked_without_opening(tmp_path, capsys):
    source = tmp_path / "pipe.hpp"
    os.mkfifo(source)
    (tmp_path / "valid.c").write_text("int count;")
    status, report = run(capsys, tmp_path)
    assert status == 2
    assert report["checked_files"] == 1
    assert any("regular file" in item["reason"] for item in report["coverage"])
    assert run(capsys, source)[0] == 2


def test_explicit_source_through_symlink_ancestor_is_skipped(tmp_path, capsys):
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "valid.c").write_text("int count;")
    linked_directory = tmp_path / "linked"
    linked_directory.symlink_to(source_directory, target_is_directory=True)
    status, report = run(capsys, linked_directory / "valid.c")
    assert status == 2
    assert report["checked_files"] == 0
    assert any(item["status"] == "skipped" and "Symlinks" in item["reason"] for item in report["coverage"])
