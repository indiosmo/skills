# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Mermaid diagram validation wrapper for mmdc (Mermaid CLI).

Validates Mermaid diagram syntax and optionally renders to SVG/PNG.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def check_mmdc_installed() -> bool:
    """Check if mmdc (Mermaid CLI) is available."""
    return shutil.which("mmdc") is not None


def validate_mermaid(
    input_file: Path,
    output_file: Path | None = None,
    output_format: str = "svg",
) -> dict:
    """
    Validate a Mermaid diagram file.

    Args:
        input_file: Path to the .mmd or .mermaid file
        output_file: Optional output path for rendered diagram
        output_format: Output format ('svg' or 'png')

    Returns:
        dict with keys:
            - success: bool
            - errors: list of error messages
            - output_path: path to rendered file (if successful)
    """
    result = {
        "success": False,
        "errors": [],
        "output_path": None,
    }

    # Check input file exists
    if not input_file.exists():
        result["errors"].append(f"Input file not found: {input_file}")
        return result

    # Check mmdc is installed
    if not check_mmdc_installed():
        result["errors"].append(
            "mmdc not found. Install with: npm install -g @mermaid-js/mermaid-cli"
        )
        return result

    # Determine output path
    if output_file is None:
        output_file = input_file.with_suffix(f".{output_format}")

    # Build mmdc command
    cmd = [
        "mmdc",
        "-i", str(input_file),
        "-o", str(output_file),
    ]

    # Run mmdc
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if proc.returncode == 0:
            result["success"] = True
            result["output_path"] = str(output_file)
        else:
            # Parse error output
            error_text = proc.stderr or proc.stdout
            if error_text:
                result["errors"].append(error_text.strip())
            else:
                result["errors"].append(f"mmdc exited with code {proc.returncode}")

    except subprocess.TimeoutExpired:
        result["errors"].append("Validation timed out after 30 seconds")
    except Exception as e:
        result["errors"].append(f"Unexpected error: {e}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate Mermaid diagram syntax"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input .mmd or .mermaid file",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output file path (default: input file with .svg extension)",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["svg", "png"],
        default="svg",
        help="Output format (default: svg)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON",
    )

    args = parser.parse_args()

    result = validate_mermaid(
        input_file=args.input,
        output_file=args.output,
        output_format=args.format,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print(f"Validation successful: {result['output_path']}")
        else:
            print("Validation failed:")
            for error in result["errors"]:
                print(f"  - {error}")

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
