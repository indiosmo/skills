# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Mermaid diagram validation and rendering wrapper.

Supports two renderers:
- mmdc (Mermaid CLI) - Full diagram type support
- beautiful-mermaid - Enhanced theming and ASCII output (subset of types)
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

# Diagram types supported by beautiful-mermaid
BEAUTIFUL_SUPPORTED_TYPES = {'flowchart', 'graph', 'sequencediagram', 'statediagram', 'classdiagram', 'erdiagram'}
# Types that require mmdc
MMDC_ONLY_TYPES = {'architecture'}


def check_mmdc_installed() -> bool:
    """Check if mmdc (Mermaid CLI) is available."""
    return shutil.which("mmdc") is not None


def check_beautiful_mermaid_installed() -> tuple[bool, str | None]:
    """
    Check if beautiful-mermaid Node.js wrapper is available.

    Returns:
        tuple of (available, error_message)
    """
    if not shutil.which("node"):
        return False, "Node.js not found. Install Node.js to use beautiful-mermaid."

    script_dir = Path(__file__).parent
    render_script = script_dir / "render_beautiful.js"

    if not render_script.exists():
        return False, f"render_beautiful.js not found at {render_script}"

    node_modules = script_dir / "node_modules" / "beautiful-mermaid"
    if not node_modules.exists():
        return False, f"beautiful-mermaid not installed. Run: cd {script_dir} && npm install"

    return True, None


def detect_diagram_type(content: str) -> str:
    """
    Detect the Mermaid diagram type from content.

    Returns:
        Lowercase diagram type identifier (e.g., 'flowchart', 'architecture')
    """
    lines = content.strip().split('\n')
    for line in lines:
        stripped = line.strip().lower()
        if not stripped or stripped.startswith('%%'):
            continue
        # Extract first word
        first_word = stripped.split()[0] if stripped.split() else ''
        # Handle direction suffix (e.g., 'flowchart-v2' -> 'flowchart')
        first_word = first_word.split('-')[0]
        return first_word
    return 'unknown'


def get_default_config() -> Path | None:
    """Get the default mermaid config file path if it exists."""
    script_dir = Path(__file__).parent
    config_path = script_dir / "mermaid-config.json"
    if config_path.exists():
        return config_path
    return None


def list_beautiful_themes() -> dict:
    """Get list of available beautiful-mermaid themes."""
    available, error = check_beautiful_mermaid_installed()
    if not available:
        return {"success": False, "error": error, "themes": []}

    script_dir = Path(__file__).parent
    render_script = script_dir / "render_beautiful.js"

    try:
        proc = subprocess.run(
            ["node", str(render_script), "--list-themes", "--json"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc.returncode == 0:
            data = json.loads(proc.stdout)
            return {"success": True, "themes": data.get("themes", [])}
        return {"success": False, "error": proc.stderr or "Failed to list themes", "themes": []}
    except Exception as e:
        return {"success": False, "error": str(e), "themes": []}


def render_with_beautiful_mermaid(
    input_file: Path,
    output_file: Path | None = None,
    output_format: str = "svg",
    theme: str | None = None,
    bg_color: str | None = None,
    fg_color: str | None = None,
    padding_x: int | None = None,
    padding_y: int | None = None,
) -> dict:
    """
    Render diagram using beautiful-mermaid.

    Returns:
        dict with keys: success, errors, output_path, diagram_type
    """
    result = {
        "success": False,
        "errors": [],
        "output_path": None,
        "diagram_type": None,
        "renderer": "beautiful-mermaid",
    }

    # Check installation
    available, error = check_beautiful_mermaid_installed()
    if not available:
        result["errors"].append(error)
        return result

    # Read and detect type
    content = input_file.read_text()
    diagram_type = detect_diagram_type(content)
    result["diagram_type"] = diagram_type

    # Check if type is supported
    if diagram_type in MMDC_ONLY_TYPES:
        result["errors"].append(
            f"Diagram type '{diagram_type}' is not supported by beautiful-mermaid. "
            "Use --renderer mmdc or --renderer auto."
        )
        return result

    if diagram_type not in BEAUTIFUL_SUPPORTED_TYPES and diagram_type != 'unknown':
        result["errors"].append(
            f"Unknown diagram type '{diagram_type}'. beautiful-mermaid supports: "
            f"{', '.join(sorted(BEAUTIFUL_SUPPORTED_TYPES))}"
        )

    script_dir = Path(__file__).parent
    render_script = script_dir / "render_beautiful.js"

    # Build command
    cmd = ["node", str(render_script), str(input_file), "--json"]

    if output_file:
        cmd.extend(["-o", str(output_file)])

    cmd.extend(["-f", output_format])

    if theme:
        cmd.extend(["-t", theme])

    if bg_color:
        cmd.extend(["--bg", bg_color])

    if fg_color:
        cmd.extend(["--fg", fg_color])

    if padding_x is not None:
        cmd.extend(["--padding-x", str(padding_x)])

    if padding_y is not None:
        cmd.extend(["--padding-y", str(padding_y)])

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Parse JSON output
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError:
            data = {}

        if proc.returncode == 0 and data.get("success"):
            result["success"] = True
            result["output_path"] = data.get("outputPath") or str(output_file)
            result["diagram_type"] = data.get("diagramType", diagram_type)
        elif proc.returncode == 2:
            # Unsupported diagram type
            result["errors"].append(data.get("error", "Unsupported diagram type"))
            if data.get("hint"):
                result["errors"].append(f"Hint: {data['hint']}")
        else:
            error_text = data.get("error") or proc.stderr or proc.stdout
            if error_text:
                result["errors"].append(error_text.strip())
            else:
                result["errors"].append(f"Render failed with code {proc.returncode}")

    except subprocess.TimeoutExpired:
        result["errors"].append("Rendering timed out after 30 seconds")
    except Exception as e:
        result["errors"].append(f"Unexpected error: {e}")

    return result


def render_with_mmdc(
    input_file: Path,
    output_file: Path | None = None,
    output_format: str = "svg",
    config_file: Path | None = None,
) -> dict:
    """
    Render diagram using mmdc (Mermaid CLI).

    Returns:
        dict with keys: success, errors, output_path
    """
    result = {
        "success": False,
        "errors": [],
        "output_path": None,
        "renderer": "mmdc",
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

    # Use default config if none specified
    if config_file is None:
        config_file = get_default_config()

    # Build mmdc command
    cmd = [
        "mmdc",
        "-i", str(input_file),
        "-o", str(output_file),
    ]

    # Add config file if available
    if config_file is not None:
        cmd.extend(["-c", str(config_file)])

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


def validate_mermaid(
    input_file: Path,
    output_file: Path | None = None,
    output_format: str = "svg",
    config_file: Path | None = None,
    renderer: str = "auto",
    theme: str | None = None,
    bg_color: str | None = None,
    fg_color: str | None = None,
    padding_x: int | None = None,
    padding_y: int | None = None,
) -> dict:
    """
    Validate and render a Mermaid diagram file.

    Args:
        input_file: Path to the .mmd or .mermaid file
        output_file: Optional output path for rendered diagram
        output_format: Output format ('svg', 'png', 'ascii', 'unicode')
        config_file: Optional mermaid config JSON file (mmdc only)
        renderer: 'auto', 'mmdc', or 'beautiful'
        theme: beautiful-mermaid theme name
        bg_color: Custom background color
        fg_color: Custom foreground color
        padding_x: ASCII horizontal padding
        padding_y: ASCII vertical padding

    Returns:
        dict with keys: success, errors, output_path, renderer
    """
    # Check input file exists
    if not input_file.exists():
        return {
            "success": False,
            "errors": [f"Input file not found: {input_file}"],
            "output_path": None,
        }

    # Determine output path
    if output_file is None:
        ext = "txt" if output_format in ("ascii", "unicode") else output_format
        output_file = input_file.with_suffix(f".{ext}")

    # ASCII/Unicode formats require beautiful-mermaid
    if output_format in ("ascii", "unicode"):
        if renderer == "mmdc":
            return {
                "success": False,
                "errors": ["ASCII/Unicode output requires beautiful-mermaid (--renderer beautiful or auto)"],
                "output_path": None,
            }
        renderer = "beautiful"

    # Theme options require beautiful-mermaid
    if theme or bg_color or fg_color:
        if renderer == "mmdc":
            return {
                "success": False,
                "errors": ["Theme options require beautiful-mermaid (--renderer beautiful or auto)"],
                "output_path": None,
            }
        if renderer == "auto":
            renderer = "beautiful"

    # Auto-detect renderer based on diagram type
    if renderer == "auto":
        content = input_file.read_text()
        diagram_type = detect_diagram_type(content)

        if diagram_type in MMDC_ONLY_TYPES:
            renderer = "mmdc"
        else:
            # Check if beautiful-mermaid is available
            available, _ = check_beautiful_mermaid_installed()
            renderer = "beautiful" if available else "mmdc"

    # Dispatch to appropriate renderer
    if renderer == "beautiful":
        return render_with_beautiful_mermaid(
            input_file=input_file,
            output_file=output_file,
            output_format=output_format,
            theme=theme,
            bg_color=bg_color,
            fg_color=fg_color,
            padding_x=padding_x,
            padding_y=padding_y,
        )
    else:
        return render_with_mmdc(
            input_file=input_file,
            output_file=output_file,
            output_format=output_format,
            config_file=config_file,
        )


def main():
    parser = argparse.ArgumentParser(
        description="Validate and render Mermaid diagrams"
    )
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        help="Input .mmd or .mermaid file",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output file path (default: input file with appropriate extension)",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["svg", "png", "ascii", "unicode"],
        default="svg",
        help="Output format (default: svg)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON",
    )
    parser.add_argument(
        "-c", "--config",
        type=Path,
        default=None,
        help="Mermaid config JSON file for mmdc (uses built-in default if not specified)",
    )
    parser.add_argument(
        "--no-config",
        action="store_true",
        help="Disable default config file (mmdc only)",
    )

    # Renderer selection
    parser.add_argument(
        "--renderer",
        choices=["auto", "mmdc", "beautiful"],
        default="auto",
        help="Renderer selection: auto (default), mmdc, or beautiful",
    )

    # beautiful-mermaid specific options
    parser.add_argument(
        "-t", "--theme",
        default=None,
        help="beautiful-mermaid theme (e.g., tokyo-night, dracula, github-dark)",
    )
    parser.add_argument(
        "--ascii",
        action="store_true",
        help="ASCII text output (shortcut for --format ascii)",
    )
    parser.add_argument(
        "--unicode",
        action="store_true",
        help="Unicode text output (shortcut for --format unicode)",
    )
    parser.add_argument(
        "--bg",
        default=None,
        help="Custom background color (overrides theme)",
    )
    parser.add_argument(
        "--fg",
        default=None,
        help="Custom foreground color (overrides theme)",
    )
    parser.add_argument(
        "--padding-x",
        type=int,
        default=None,
        help="ASCII horizontal padding",
    )
    parser.add_argument(
        "--padding-y",
        type=int,
        default=None,
        help="ASCII vertical padding",
    )
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="List available beautiful-mermaid themes and exit",
    )

    args = parser.parse_args()

    # Handle --list-themes
    if args.list_themes:
        themes_result = list_beautiful_themes()
        if args.json:
            print(json.dumps(themes_result, indent=2))
        else:
            if themes_result["success"]:
                print("Available themes:")
                print("")
                print("Light themes:")
                for t in themes_result["themes"]:
                    if "light" in t or t == "catppuccin-latte":
                        print(f"  - {t}")
                print("")
                print("Dark themes:")
                for t in themes_result["themes"]:
                    if "light" not in t and t != "catppuccin-latte":
                        print(f"  - {t}")
            else:
                print(f"Error: {themes_result['error']}")
        sys.exit(0 if themes_result["success"] else 1)

    # Require input file for all other operations
    if not args.input:
        parser.error("Input file is required")

    # Handle format shortcuts
    output_format = args.format
    if args.ascii:
        output_format = "ascii"
    elif args.unicode:
        output_format = "unicode"

    # Determine config file
    config_file = args.config
    if args.no_config:
        config_file = None
    elif config_file is None and args.renderer != "beautiful":
        config_file = get_default_config()

    result = validate_mermaid(
        input_file=args.input,
        output_file=args.output,
        output_format=output_format,
        config_file=config_file,
        renderer=args.renderer,
        theme=args.theme,
        bg_color=args.bg,
        fg_color=args.fg,
        padding_x=args.padding_x,
        padding_y=args.padding_y,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            renderer_info = f" [{result.get('renderer', 'unknown')}]"
            print(f"Validation successful{renderer_info}: {result['output_path']}")
        else:
            print("Validation failed:")
            for error in result["errors"]:
                print(f"  - {error}")

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
