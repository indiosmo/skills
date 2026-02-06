#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Validate PlantUML syntax by running plantuml -syntax on a .puml file."""

import subprocess
import sys
from pathlib import Path


def validate(puml_path: str) -> int:
    path = Path(puml_path)
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        return 1

    content = path.read_text()

    result = subprocess.run(
        ["plantuml", "-syntax"],
        input=content,
        capture_output=True,
        text=True,
    )

    # Combine stdout and stderr
    output = (result.stdout + "\n" + result.stderr).strip()
    lines = output.splitlines()

    if not lines:
        print(f"ERROR: No output from plantuml for {path.name}")
        return 1

    if lines[0] == "ERROR":
        line_num = lines[1] if len(lines) > 1 else "?"
        description = lines[2] if len(lines) > 2 else "Unknown error"
        print(f"SYNTAX ERROR in {path.name} at line {line_num}: {description}")
        for extra in lines[3:]:
            print(f"  {extra}")
        return 1

    diagram_type = lines[0]
    info = lines[1] if len(lines) > 1 else ""
    print(f"OK: {path.name} -- {diagram_type} {info}")
    return 0


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/validate.py <file.puml> [file2.puml ...]")
        sys.exit(1)

    exit_code = 0
    for arg in sys.argv[1:]:
        if validate(arg) != 0:
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
