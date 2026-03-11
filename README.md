## Project Overview

This is a **Skills Repository** for Claude Code - a collection of modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. Skills are "onboarding guides" for specific domains that transform Claude into a specialized agent.

## Getting Started

```bash
# Clone the repository
git clone <repo-url> ~/skills

# Install all dependencies (Python + Node.js)
./setup.sh

# Symlink skills you want to use
mkdir -p ~/.claude/skills
ln -s ~/skills/skills/authoring-mermaid-diagrams ~/.claude/skills/
ln -s ~/skills/skills/processing-pdfs ~/.claude/skills/
```

The `setup.sh` script checks for required tools (uv, npm), installs Python dependencies via `uv sync`, and runs `npm install` for any skills with Node.js dependencies.

## Commands

```bash
# Run tests
uv run pytest

# Run a single test
uv run pytest tests/processing-pdfs/test_check_bounding_boxes.py

# Run Python scripts (uses PEP 723 inline dependencies)
uv run scripts/example.py

# Initialize a new skill
uv run skills/creating-skills/scripts/init_skill.py <skill-name> --path <output-directory>

# Package a skill for distribution
uv run skills/creating-skills/scripts/package_skill.py <path/to/skill-folder>
```

## Key Conventions

- **PEP 723**: Python scripts include inline metadata for `uv run` compatibility

## Development Notes

- Python 3.13 required (see `.python-version`)
- Dev dependencies managed via `uv` in `pyproject.toml`
- Skills load from: Enterprise > Personal (`~/.claude/skills/`) > Project (`.claude/skills/`) > Plugin
