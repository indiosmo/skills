#!/usr/bin/env node
/**
 * CLI wrapper for beautiful-mermaid library.
 *
 * Renders Mermaid diagrams with enhanced theming and ASCII output support.
 * Exit codes:
 *   0 - Success
 *   1 - General error
 *   2 - Unsupported diagram type
 */

import { readFileSync, writeFileSync } from 'fs';
import { renderMermaid, renderMermaidAscii, THEMES } from 'beautiful-mermaid';

const SUPPORTED_TYPES = ['flowchart', 'graph', 'sequenceDiagram', 'stateDiagram', 'classDiagram', 'erDiagram'];
const UNSUPPORTED_TYPES = ['architecture'];

function parseArgs(args) {
  const options = {
    input: null,
    output: null,
    format: 'svg',
    theme: 'github-light',
    bg: null,
    fg: null,
    paddingX: null,
    paddingY: null,
    listThemes: false,
    json: false,
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];

    if (arg === '--list-themes') {
      options.listThemes = true;
    } else if (arg === '--json') {
      options.json = true;
    } else if (arg === '-o' || arg === '--output') {
      options.output = args[++i];
    } else if (arg === '-f' || arg === '--format') {
      options.format = args[++i];
    } else if (arg === '-t' || arg === '--theme') {
      options.theme = args[++i];
    } else if (arg === '--bg') {
      options.bg = args[++i];
    } else if (arg === '--fg') {
      options.fg = args[++i];
    } else if (arg === '--padding-x') {
      options.paddingX = parseInt(args[++i], 10);
    } else if (arg === '--padding-y') {
      options.paddingY = parseInt(args[++i], 10);
    } else if (!arg.startsWith('-')) {
      options.input = arg;
    }
    i++;
  }

  return options;
}

function detectDiagramType(content) {
  const trimmed = content.trim();
  const firstLine = trimmed.split('\n')[0].toLowerCase();

  for (const unsupported of UNSUPPORTED_TYPES) {
    if (firstLine.startsWith(unsupported)) {
      return { type: unsupported, supported: false };
    }
  }

  for (const supported of SUPPORTED_TYPES) {
    if (firstLine.startsWith(supported.toLowerCase())) {
      return { type: supported, supported: true };
    }
  }

  // Default to flowchart if starts with graph keyword
  if (firstLine.startsWith('graph')) {
    return { type: 'flowchart', supported: true };
  }

  return { type: 'unknown', supported: false };
}

function listThemes(jsonOutput) {
  const themeNames = Object.keys(THEMES);

  if (jsonOutput) {
    console.log(JSON.stringify({ themes: themeNames }, null, 2));
  } else {
    console.log('Available themes:');
    console.log('');
    console.log('Light themes:');
    themeNames.filter(t => t.includes('light') || t === 'catppuccin-latte').forEach(t => console.log(`  - ${t}`));
    console.log('');
    console.log('Dark themes:');
    themeNames.filter(t => !t.includes('light') && t !== 'catppuccin-latte').forEach(t => console.log(`  - ${t}`));
  }
}

async function render(options) {
  const content = readFileSync(options.input, 'utf-8');
  const detection = detectDiagramType(content);

  if (!detection.supported) {
    const result = {
      success: false,
      error: `Unsupported diagram type: ${detection.type}`,
      hint: detection.type === 'architecture'
        ? 'Architecture diagrams require mmdc. Use --renderer mmdc or --renderer auto.'
        : 'Unknown diagram type.',
    };

    if (options.json) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.error(`Error: ${result.error}`);
      if (result.hint) console.error(`Hint: ${result.hint}`);
    }
    process.exit(2);
  }

  // Build render options
  const renderOptions = {};

  // Apply theme or custom colors
  if (options.bg && options.fg) {
    renderOptions.bg = options.bg;
    renderOptions.fg = options.fg;
  } else if (options.theme && THEMES[options.theme]) {
    Object.assign(renderOptions, THEMES[options.theme]);
  } else if (options.theme) {
    console.error(`Unknown theme: ${options.theme}. Use --list-themes to see available themes.`);
    process.exit(1);
  }

  // ASCII-specific options
  if (options.format === 'ascii' || options.format === 'unicode') {
    renderOptions.useAscii = options.format === 'ascii';
    if (options.paddingX !== null) renderOptions.paddingX = options.paddingX;
    if (options.paddingY !== null) renderOptions.paddingY = options.paddingY;
  }

  try {
    let output;

    if (options.format === 'ascii' || options.format === 'unicode') {
      output = renderMermaidAscii(content, renderOptions);
    } else {
      output = await renderMermaid(content, renderOptions);
    }

    // Write or print output
    if (options.output) {
      writeFileSync(options.output, output);
    }

    const result = {
      success: true,
      diagramType: detection.type,
      format: options.format,
      theme: options.theme,
      outputPath: options.output || null,
    };

    if (options.json) {
      if (!options.output) result.content = output;
      console.log(JSON.stringify(result, null, 2));
    } else {
      if (options.output) {
        console.log(`Rendered ${detection.type} diagram to ${options.output}`);
      } else {
        console.log(output);
      }
    }

  } catch (err) {
    const result = {
      success: false,
      error: err.message,
    };

    if (options.json) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.error(`Render error: ${err.message}`);
    }
    process.exit(1);
  }
}

function showUsage() {
  console.log(`Usage: node render_beautiful.js <input.mmd> [options]

Options:
  -o, --output <file>     Output file path (prints to stdout if not specified)
  -f, --format <type>     Output format: svg, ascii, unicode (default: svg)
  -t, --theme <name>      Theme name (default: github-light)
  --bg <color>            Custom background color (overrides theme)
  --fg <color>            Custom foreground color (overrides theme)
  --padding-x <n>         ASCII horizontal padding
  --padding-y <n>         ASCII vertical padding
  --list-themes           List available themes and exit
  --json                  Output result as JSON

Exit codes:
  0 - Success
  1 - General error
  2 - Unsupported diagram type (e.g., architecture)

Supported diagram types:
  flowchart, sequence, state, class, ER

Unsupported (use mmdc instead):
  architecture`);
}

// Main
const args = process.argv.slice(2);

if (args.length === 0 || args.includes('-h') || args.includes('--help')) {
  showUsage();
  process.exit(0);
}

const options = parseArgs(args);

if (options.listThemes) {
  listThemes(options.json);
  process.exit(0);
}

if (!options.input) {
  console.error('Error: No input file specified');
  showUsage();
  process.exit(1);
}

render(options);
