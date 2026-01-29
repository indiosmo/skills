# Mermaid Theming Guide

Comprehensive reference for styling Mermaid diagrams using beautiful-mermaid themes.

## Overview

beautiful-mermaid uses a two-color foundation system that derives all diagram colors from background (bg) and foreground (fg) colors. This ensures consistent, harmonious diagrams.

## Color System

### Foundation Colors (Required)

| Color | Role | Maps To |
|-------|------|---------|
| `bg` | Background | Diagram background, node fills |
| `fg` | Foreground | Text, primary lines |

### Enrichment Colors (Optional)

Additional colors that enhance the theme when provided:

| Color | Role | Derivation if Missing |
|-------|------|----------------------|
| `line` | Connectors, arrows | Mixed from fg (70%) and bg (30%) |
| `accent` | Highlights, selections | Derived from fg with saturation boost |
| `muted` | Secondary text, labels | Mixed from fg (50%) and bg (50%) |
| `surface` | Node backgrounds | Slight tint of bg |
| `border` | Node borders | Mixed from fg (30%) and bg (70%) |

## Built-in Themes

### Light Themes

| Theme | Background | Foreground | Character |
|-------|------------|------------|-----------|
| `tokyo-night-light` | `#d5d6db` | `#343b58` | Soft blue undertones |
| `catppuccin-latte` | `#eff1f5` | `#4c4f69` | Warm, creamy pastels |
| `nord-light` | `#eceff4` | `#2e3440` | Arctic, cool blue-gray |
| `github-light` | `#ffffff` | `#24292f` | GitHub documentation style |
| `solarized-light` | `#fdf6e3` | `#657b83` | Classic warm light |

### Dark Themes

| Theme | Background | Foreground | Character |
|-------|------------|------------|-----------|
| `zinc-dark` | `#18181b` | `#fafafa` | Clean, neutral dark |
| `tokyo-night` | `#1a1b26` | `#c0caf5` | Popular VS Code theme |
| `tokyo-night-storm` | `#24283b` | `#c0caf5` | Deeper variant |
| `catppuccin-mocha` | `#1e1e2e` | `#cdd6f4` | Rich, warm dark |
| `nord` | `#2e3440` | `#eceff4` | Arctic dark palette |
| `dracula` | `#282a36` | `#f8f8f2` | Purple-accented dark |
| `github-dark` | `#0d1117` | `#c9d1d9` | GitHub dark mode |
| `solarized-dark` | `#002b36` | `#839496` | Classic dark theme |
| `one-dark` | `#282c34` | `#abb2bf` | Atom editor style |

## Usage Examples

### Using Built-in Themes

```bash
# List all available themes
uv run scripts/validate_mermaid.py --list-themes

# Apply a theme
uv run scripts/validate_mermaid.py diagram.mmd --theme dracula -o diagram.svg

# JSON output for scripting
uv run scripts/validate_mermaid.py --list-themes --json
```

### Custom Two-Color Theme

Create a custom theme with just background and foreground:

```bash
# Corporate blue theme
uv run scripts/validate_mermaid.py diagram.mmd --bg "#f0f4f8" --fg "#1e3a5f" -o diagram.svg

# High contrast
uv run scripts/validate_mermaid.py diagram.mmd --bg "#000000" --fg "#ffffff" -o diagram.svg

# Sepia/document style
uv run scripts/validate_mermaid.py diagram.mmd --bg "#f5f1e8" --fg "#3d3429" -o diagram.svg
```

## Theme Selection Guide

### By Context

| Context | Recommended Theme |
|---------|------------------|
| Technical documentation | `github-light` |
| Dark mode UI | `tokyo-night` or `github-dark` |
| Print/PDF export | `github-light` (high contrast) |
| Presentation slides | `dracula` or `nord` (dark) |
| README files | `github-light` or `github-dark` |
| Code editor integration | Match your editor theme |

### By Preference

| Style | Light | Dark |
|-------|-------|------|
| Minimal | `github-light` | `zinc-dark` |
| Warm | `catppuccin-latte` | `catppuccin-mocha` |
| Cool | `nord-light` | `nord` |
| Classic | `solarized-light` | `solarized-dark` |
| Modern | `github-light` | `tokyo-night` |

## ASCII/Unicode Theming

When using ASCII or Unicode output, theming affects character weight and spacing:

```bash
# Unicode with theme (affects rendering style)
uv run scripts/validate_mermaid.py diagram.mmd --unicode --theme tokyo-night -o diagram.txt

# With custom padding
uv run scripts/validate_mermaid.py diagram.mmd --unicode --padding-x 2 --padding-y 1 -o diagram.txt
```

Note: Color information is not applicable to text output, but theme selection may influence character choices in some renderers.

## Programmatic Access

The Node.js wrapper exposes themes directly:

```javascript
import { THEMES } from 'beautiful-mermaid';

// List theme names
console.log(Object.keys(THEMES));

// Access theme colors
const tokyoNight = THEMES['tokyo-night'];
console.log(tokyoNight.bg);  // "#1a1b26"
console.log(tokyoNight.fg);  // "#c0caf5"
```

## Creating Custom Themes

For advanced use cases, create a theme object with the full color set:

```javascript
const customTheme = {
  bg: '#1a1b26',      // Background
  fg: '#c0caf5',      // Foreground
  line: '#565f89',    // Connectors (optional)
  accent: '#7aa2f7',  // Highlights (optional)
  muted: '#565f89',   // Secondary text (optional)
  surface: '#24283b', // Node backgrounds (optional)
  border: '#414868',  // Node borders (optional)
};
```

## Limitations

### Diagram Type Support

beautiful-mermaid themes work with:
- Flowcharts (all directions)
- Sequence diagrams
- State diagrams
- Class diagrams
- ER diagrams

**Not supported**: Architecture diagrams (use mmdc with CSS styling instead)

### Two-Step Workflow

For best results, use a two-step approach:

1. **Syntax validation**: Always validate with `--renderer mmdc` first (authoritative parser)
2. **Final rendering**: Render with `--renderer beautiful` for theming (when available)

```bash
# Step 1: Validate syntax
uv run scripts/validate_mermaid.py diagram.mmd --renderer mmdc -o diagram-check.svg

# Step 2: Render with theme
uv run scripts/validate_mermaid.py diagram.mmd --renderer beautiful --theme dracula -o diagram.svg
```

**Note:** Architecture diagrams only support mmdc (skip Step 2).

## Troubleshooting

### Theme Not Applied

1. Check renderer selection: `--renderer beautiful` or `--renderer auto`
2. Verify beautiful-mermaid is installed: `cd scripts && npm install`
3. Ensure diagram type is supported (not architecture)

### Colors Look Different

1. SVG rendering may vary by viewer
2. Check if transparent background is affecting display
3. Verify monitor color profile

### Custom Colors Not Working

1. Use valid hex colors: `#rrggbb` or `#rgb`
2. Both `--bg` and `--fg` should be specified together
3. Custom colors override theme selection
