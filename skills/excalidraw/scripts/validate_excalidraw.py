#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Excalidraw JSON Validator

Validates .excalidraw files for common issues before rendering.

Usage:
    uv run validate_excalidraw.py <file.excalidraw>
    uv run validate_excalidraw.py diagram.excalidraw --verbose
"""

import argparse
import json
import sys
from pathlib import Path


class ValidationError:
    def __init__(self, level: str, message: str, element_id: str | None = None):
        self.level = level  # "error" or "warning"
        self.message = message
        self.element_id = element_id

    def __str__(self):
        prefix = f"[{self.element_id}] " if self.element_id else ""
        return f"{self.level.upper()}: {prefix}{self.message}"


def validate_excalidraw(data: dict, verbose: bool = False) -> list[ValidationError]:
    """Validate an Excalidraw JSON structure."""
    errors = []

    # 1. Check top-level structure
    required_fields = ["type", "version", "elements"]
    for field in required_fields:
        if field not in data:
            errors.append(ValidationError("error", f"Missing required field: {field}"))

    if data.get("type") != "excalidraw":
        errors.append(ValidationError("error", f"Invalid type: expected 'excalidraw', got '{data.get('type')}'"))

    elements = data.get("elements", [])
    if not isinstance(elements, list):
        errors.append(ValidationError("error", "elements must be a list"))
        return errors

    # Build lookup maps
    elements_by_id = {}
    ids = []
    for el in elements:
        el_id = el.get("id")
        if el_id:
            ids.append(el_id)
            elements_by_id[el_id] = el

    # 2. Check for duplicate IDs
    seen = set()
    for el_id in ids:
        if el_id in seen:
            errors.append(ValidationError("error", f"Duplicate ID: {el_id}"))
        seen.add(el_id)

    # 3. Validate each element
    for el in elements:
        el_id = el.get("id", "unknown")
        el_type = el.get("type")

        # Check required properties
        required_props = ["id", "type", "x", "y"]
        for prop in required_props:
            if prop not in el:
                errors.append(ValidationError("error", f"Missing required property: {prop}", el_id))

        # Check for diamond shapes (known broken)
        if el_type == "diamond":
            errors.append(ValidationError("error", "Diamond shapes have broken arrow connections. Use styled rectangles instead.", el_id))

        # Check shape elements
        if el_type in ["rectangle", "ellipse"]:
            if "width" not in el or "height" not in el:
                errors.append(ValidationError("error", "Shape missing width/height", el_id))

            # Check boundElements/text pairing
            bound_elements = el.get("boundElements") or []
            for binding in bound_elements:
                if binding.get("type") == "text":
                    text_id = binding.get("id")
                    text_el = elements_by_id.get(text_id)
                    if text_el is None:
                        errors.append(ValidationError("error", f"boundElements references missing text element: {text_id}", el_id))
                    elif text_el.get("containerId") != el_id:
                        errors.append(ValidationError("error", f"Text element {text_id} containerId doesn't match shape id", el_id))

        # Check text elements
        if el_type == "text":
            container_id = el.get("containerId")
            if container_id:
                container = elements_by_id.get(container_id)
                if container is None:
                    errors.append(ValidationError("error", f"containerId references missing shape: {container_id}", el_id))
                else:
                    # Check that container has boundElements referencing this text
                    bound_elements = container.get("boundElements") or []
                    text_refs = [b.get("id") for b in bound_elements if b.get("type") == "text"]
                    if el_id not in text_refs:
                        errors.append(ValidationError("warning", f"Container {container_id} missing boundElements reference to this text", el_id))

            if "text" not in el:
                errors.append(ValidationError("error", "Text element missing 'text' property", el_id))

        # Check arrow elements
        if el_type == "arrow":
            points = el.get("points", [])

            if len(points) < 2:
                errors.append(ValidationError("error", "Arrow must have at least 2 points", el_id))

            # Check elbow arrow properties for multi-point arrows
            if len(points) > 2:
                if el.get("elbowed") != True:
                    errors.append(ValidationError("warning", "Multi-point arrow missing 'elbowed: true' - will render curved", el_id))
                if el.get("roundness") is not None:
                    errors.append(ValidationError("warning", "Elbow arrow should have 'roundness: null' for sharp corners", el_id))
                if el.get("roughness", 1) != 0:
                    errors.append(ValidationError("warning", "Elbow arrow should have 'roughness: 0' for clean lines", el_id))

            # Check bounding box matches points
            if points:
                max_x = max(abs(p[0]) for p in points)
                max_y = max(abs(p[1]) for p in points)
                width = el.get("width", 0)
                height = el.get("height", 0)

                if width < max_x - 1:  # Allow 1px tolerance
                    errors.append(ValidationError("warning", f"Arrow width ({width}) smaller than points bounding box ({max_x})", el_id))
                if height < max_y - 1:
                    errors.append(ValidationError("warning", f"Arrow height ({height}) smaller than points bounding box ({max_y})", el_id))

            # Check arrow endpoints near shapes
            if verbose:
                arrow_x = el.get("x", 0)
                arrow_y = el.get("y", 0)

                start_near_shape = find_shape_near(elements, arrow_x, arrow_y)
                if not start_near_shape:
                    errors.append(ValidationError("warning", f"Arrow start ({arrow_x}, {arrow_y}) not near any shape edge", el_id))

                if points:
                    end_x = arrow_x + points[-1][0]
                    end_y = arrow_y + points[-1][1]
                    end_near_shape = find_shape_near(elements, end_x, end_y)
                    if not end_near_shape:
                        errors.append(ValidationError("warning", f"Arrow end ({end_x}, {end_y}) not near any shape edge", el_id))

    return errors


def find_shape_near(elements: list, x: float, y: float, tolerance: float = 20) -> dict | None:
    """Find a shape whose edge is near the given point."""
    for el in elements:
        if el.get("type") not in ["rectangle", "ellipse"]:
            continue

        el_x = el.get("x", 0)
        el_y = el.get("y", 0)
        width = el.get("width", 0)
        height = el.get("height", 0)

        # Calculate edge points
        edges = [
            (el_x + width / 2, el_y),              # top
            (el_x + width / 2, el_y + height),     # bottom
            (el_x, el_y + height / 2),             # left
            (el_x + width, el_y + height / 2),     # right
        ]

        for edge_x, edge_y in edges:
            if abs(edge_x - x) < tolerance and abs(edge_y - y) < tolerance:
                return el

    return None


def main():
    parser = argparse.ArgumentParser(description="Validate Excalidraw JSON files")
    parser.add_argument("file", help="Path to .excalidraw file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose checks (arrow endpoint validation)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    errors = validate_excalidraw(data, verbose=args.verbose)

    if args.json:
        result = {
            "valid": len([e for e in errors if e.level == "error"]) == 0,
            "errors": [{"level": e.level, "message": e.message, "element_id": e.element_id} for e in errors]
        }
        print(json.dumps(result, indent=2))
    else:
        error_count = len([e for e in errors if e.level == "error"])
        warning_count = len([e for e in errors if e.level == "warning"])

        if errors:
            for error in errors:
                print(str(error))
            print()

        if error_count == 0 and warning_count == 0:
            print(f"Valid: {file_path.name} passed all checks")
            sys.exit(0)
        elif error_count == 0:
            print(f"Valid with warnings: {warning_count} warning(s)")
            sys.exit(0)
        else:
            print(f"Invalid: {error_count} error(s), {warning_count} warning(s)")
            sys.exit(1)


if __name__ == "__main__":
    main()
