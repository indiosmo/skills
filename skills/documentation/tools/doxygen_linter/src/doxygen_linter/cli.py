"""Read files and configuration, then report diagnostics for local or CI use."""

import argparse
from dataclasses import asdict
import fnmatch
import json
import os
from pathlib import Path
import sys
import tomllib
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from .catalog import MANUAL_COVERAGE, RULES
from .checks import Coverage, lint

VERSION = "0.1.0"
LANGUAGES = {
    ".c": "c",
    ".h": "cpp",
    ".cc": "cpp",
    ".cpp": "cpp",
    ".cxx": "cpp",
    ".hpp": "cpp",
    ".hh": "cpp",
    ".hxx": "cpp",
    ".ipp": "cpp",
    ".tpp": "cpp",
}


class Configuration(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    exclude: list[str] = Field(
        default_factory=lambda: [
            "**/vendor/**",
            "**/third_party/**",
            "**/generated/**",
            "**/.git/**",
            "**/.venv/**",
            "**/build/**",
        ]
    )
    extensions: list[str] = Field(default_factory=lambda: list(LANGUAGES))
    severity: dict[str, Literal["warning", "error"]] = Field(default_factory=dict)

    @field_validator("severity")
    @classmethod
    def known_rules(cls, values):
        if not values.keys() <= RULES.keys():
            raise ValueError("Severity overrides require known rule identifiers")
        return values

    @field_validator("extensions")
    @classmethod
    def known_extensions(cls, values):
        if not values or not set(values) <= LANGUAGES.keys():
            raise ValueError(
                "Extensions must be a nonempty selection from supported C/C++ extensions"
            )
        return values


def discover(inputs: list[Path], configuration: Configuration) -> tuple[list[Path], list[Coverage]]:
    files = set()
    coverage = []

    def include(path: Path, explicit: bool = False) -> bool:
        normalized = path.as_posix()
        if any(
            fnmatch.fnmatch(normalized, pattern) or fnmatch.fnmatch("/" + normalized, pattern)
            for pattern in configuration.exclude
        ):
            coverage.append(Coverage(str(path), 1, "file", "skipped", "Path matches an exclusion."))
            return False
        if path.is_symlink() or any(parent.is_symlink() for parent in path.absolute().parents):
            coverage.append(
                Coverage(
                    str(path),
                    1,
                    "file",
                    "skipped",
                    "Symlinks are excluded from traversal and reads.",
                )
            )
            return False
        if not path.is_file() and not path.is_dir():
            if explicit or path.suffix in configuration.extensions:
                coverage.append(
                    Coverage(
                        str(path),
                        1,
                        "file",
                        "blocked",
                        "Input is missing or is not a regular file/directory.",
                    )
                )
            return False
        if path.is_file() and path.suffix not in configuration.extensions:
            if explicit:
                coverage.append(
                    Coverage(
                        str(path),
                        1,
                        "file",
                        "blocked",
                        "Input extension is unsupported or disabled.",
                    )
                )
            return False
        return True

    for path in inputs:
        if not include(path, explicit=True):
            continue
        if path.is_file():
            files.add(path.absolute())
        elif path.is_dir():

            def walk_error(error):
                coverage.append(
                    Coverage(error.filename or str(path), 1, "file", "blocked", str(error))
                )

            for directory, directories, filenames in os.walk(
                path, followlinks=False, onerror=walk_error
            ):
                directories[:] = sorted(
                    name for name in directories if include(Path(directory, name))
                )
                for filename in sorted(filenames):
                    candidate = Path(directory, filename)
                    if include(candidate):
                        files.add(candidate.absolute())
        else:
            coverage.append(
                Coverage(
                    str(path),
                    1,
                    "file",
                    "blocked",
                    "Input does not exist or is not a regular file/directory.",
                )
            )
    return sorted(files), coverage


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check C/C++ Doxygen comments; findings retain source locations."
    )
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--config", type=Path, help="Explicit TOML configuration")
    parser.add_argument("--language", choices=["auto", "c", "cpp"], default="auto")
    parser.add_argument("--extensions", nargs="+", help="Supported suffixes including the dot")
    parser.add_argument("--exclude", action="append", default=[], help="Additional whole-path glob")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--fail-on", choices=["warning", "error"], default="warning")
    parser.add_argument("--catalog", action="store_true", help="Print the rule catalog as JSON")
    parser.add_argument("--version", action="version", version=VERSION)
    options = parser.parse_args(arguments)
    if options.catalog:
        print(
            json.dumps(
                {
                    identifier: asdict(rule) | {"source": rule.source}
                    for identifier, rule in RULES.items()
                },
                indent=2,
            )
        )
        return 0
    diagnostics = []
    coverage = []
    files = []
    checked = 0
    try:
        raw_configuration = (
            tomllib.loads(options.config.read_text(encoding="utf-8")) if options.config else {}
        )
        if options.extensions:
            raw_configuration["extensions"] = options.extensions
        configuration = Configuration.model_validate(raw_configuration)
        configuration.exclude.extend(options.exclude)
        if not options.paths:
            raise ValueError("Provide at least one source file or directory")
        files, coverage = discover(options.paths, configuration)
        for path in files:
            try:
                source = path.read_bytes()
                source.decode("utf-8")
                if b"\x00" in source:
                    raise ValueError("Source contains a NUL byte")
                language = (
                    LANGUAGES[path.suffix] if options.language == "auto" else options.language
                )
                file_diagnostics, file_coverage = lint(
                    source, str(path), language, configuration.severity
                )
                diagnostics.extend(file_diagnostics)
                coverage.extend(file_coverage)
                checked += 1
            except (OSError, UnicodeError, ValueError) as error:
                coverage.append(Coverage(str(path), 1, "file", "blocked", str(error)))
    except (OSError, UnicodeError, ValueError, ValidationError) as error:
        coverage.append(
            Coverage(str(options.config or "<input>"), 1, "configuration", "blocked", str(error))
        )
    if not checked:
        coverage.append(
            Coverage("<input>", 1, "file", "blocked", "No supported source files were checked.")
        )
    diagnostics.sort(
        key=lambda diagnostic: (
            diagnostic.path,
            diagnostic.line,
            diagnostic.column,
            diagnostic.rule,
        )
    )
    blocked = any(item.status == "blocked" for item in coverage)
    failed = any(
        options.fail_on == "warning" or diagnostic.severity == "error" for diagnostic in diagnostics
    )
    exit_status = 2 if blocked else 1 if failed else 0
    report = {
        "version": VERSION,
        "status": "blocked" if blocked else "fail" if failed else "pass",
        "checked_files": checked,
        "diagnostics": [asdict(diagnostic) for diagnostic in diagnostics],
        "coverage": [asdict(item) for item in coverage],
        "review_required": MANUAL_COVERAGE,
        "exit_status": exit_status,
    }
    if options.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        for diagnostic in diagnostics:
            print(
                f"{diagnostic.path}:{diagnostic.line}:{diagnostic.column}: {diagnostic.severity} {diagnostic.rule}: {diagnostic.explanation} Correction: {diagnostic.correction}"
            )
        for item in coverage:
            print(f"{item.path}:{item.line}:1: {item.status} {item.checks}: {item.reason}")
        print(
            f"{report['status']}: checked {checked} files; {len(diagnostics)} findings; {len(coverage)} coverage records"
        )
        for item in MANUAL_COVERAGE:
            print("review: " + item)
    return exit_status


if __name__ == "__main__":
    sys.exit(main())
