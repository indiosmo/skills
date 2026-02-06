#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Render PlantUML diagrams to PNG for visual inspection."""

import subprocess
import sys
from pathlib import Path


def render(puml_path: str, output_dir: str | None = None) -> int:
    path = Path(puml_path)
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        return 1

    cmd = ["plantuml", "-tpng"]
    if output_dir:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        cmd.extend(["-o", str(out.resolve())])
    cmd.append(str(path))

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR rendering {path.name}:")
        print(result.stderr.strip())
        return 1

    # Determine output path
    if output_dir:
        png = Path(output_dir) / path.with_suffix(".png").name
    else:
        png = path.with_suffix(".png")

    if png.exists():
        print(f"OK: {path.name} -> {png}")
    else:
        print(f"WARNING: Render completed but output not found at {png}")
    return 0


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/render.py <file.puml> [file2.puml ...] [-o output_dir]")
        sys.exit(1)

    args = sys.argv[1:]
    output_dir = None
    if "-o" in args:
        idx = args.index("-o")
        if idx + 1 < len(args):
            output_dir = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
        else:
            print("ERROR: -o requires a directory argument")
            sys.exit(1)

    exit_code = 0
    for arg in args:
        if render(arg, output_dir) != 0:
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
