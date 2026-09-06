"""Run ordered project checks and retain native diagnostics."""

import argparse
import sys
from pathlib import Path

from .configuration import load_manifest
from .models import VERSION
from .orchestration import validate
from .reporting import serialize_report, write_report


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--skill", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version", action="version", version=VERSION)
    options = parser.parse_args(arguments)
    try:
        manifest = load_manifest(options.manifest)
        report = validate(manifest, options.project.resolve(), options.skill.resolve(), options.output.resolve())
        write_report(report, options.output.resolve() / "report.json")
    except (OSError, ValueError) as error:
        print(f"blocked: {error}", file=sys.stderr)
        return 2
    print(serialize_report(report), end="")
    return report["exit_status"]
