"""Compare parsing evidence and measure directory checking on a generated fixture corpus."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

from doxygen_linter.checks import lint
from doxygen_linter.cli import Configuration, discover
from doxygen_linter.parsing import parse


fixtures = Path(__file__).resolve().parents[1] / "tests" / "fixtures"
source_file = fixtures / "representative.hpp"
source = source_file.read_bytes()
root, comments = parse(source, "cpp")
report = {
    "fixture": source_file.name,
    "regex_block_matches": len(re.findall(rb"/\*\*.*?\*/", source, re.S)),
    "tree_sitter_comments": len(comments),
    "tree_sitter_syntax_error": root.has_error,
    "comment_start_lines": [comment.node.start_point.row + 1 for comment in comments],
}
compiler = shutil.which("clang++")
if compiler:
    command = [
        compiler,
        "-x",
        "c++",
        "-std=c++20",
        "-fsyntax-only",
        "-Wdocumentation",
        str(source_file),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=30)
    report["compiler"] = {
        "command": command,
        "exit_status": result.returncode,
        "stderr": result.stderr,
    }
    report["dialect_probes"] = []
    for language, standard, filename in [
        ("c", "c11", "representative.c"),
        ("c", "c17", "representative.c"),
        ("c++", "c++17", "representative.hpp"),
        ("c++", "c++20", "representative.hpp"),
    ]:
        dialect_command = [
            compiler,
            "-x",
            language,
            f"-std={standard}",
            "-fsyntax-only",
            str(fixtures / filename),
        ]
        dialect_result = subprocess.run(
            dialect_command, capture_output=True, text=True, check=False, timeout=30
        )
        report["dialect_probes"].append(
            {
                "standard": standard,
                "exit_status": dialect_result.returncode,
                "stderr": dialect_result.stderr,
            }
        )
    invalid_result = subprocess.run(
        command[:-1] + [str(fixtures / "invalid.cpp")],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    report["compiler_house_style_probe"] = {
        "exit_status": invalid_result.returncode,
        "stderr": invalid_result.stderr,
    }
    with tempfile.TemporaryDirectory(prefix="doxygen-parser-probe-") as directory:
        missing_include = Path(directory) / "missing.hpp"
        missing_include.write_bytes(b'#include "generated_dependency.hpp"\n' + source)
        result = subprocess.run(
            command[:-1] + [str(missing_include)],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        report["missing_include"] = {
            "compiler_exit_status": result.returncode,
            "compiler_stderr": result.stderr,
            "tree_sitter_syntax_error": parse(missing_include.read_bytes(), "cpp")[0].has_error,
        }
else:
    report["compiler"] = {"status": "blocked", "reason": "clang++ unavailable"}
with tempfile.TemporaryDirectory(prefix="doxygen-directory-benchmark-") as directory:
    for index in range(500):
        (Path(directory) / f"sample_{index}.hpp").write_bytes(source)
    started = time.perf_counter()
    files, coverage = discover([Path(directory)], Configuration())
    diagnostic_count = 0
    for path in files:
        diagnostics, skipped = lint(path.read_bytes(), str(path), "cpp")
        diagnostic_count += len(diagnostics)
        coverage.extend(skipped)
    report["directory_benchmark"] = {
        "files": len(files),
        "bytes": len(source) * len(files),
        "seconds": round(time.perf_counter() - started, 4),
        "diagnostics": diagnostic_count,
        "coverage_records": len(coverage),
    }
print(json.dumps(report, indent=2))
