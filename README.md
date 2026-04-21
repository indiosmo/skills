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
ln -s ~/skills/skills/mermaid ~/.claude/skills/
ln -s ~/skills/skills/pdf ~/.claude/skills/
```

The `setup.sh` script checks for required tools (uv, npm), installs Python dependencies via `uv sync`, and runs `npm install` for any skills with Node.js dependencies.

## Commands

```bash
# Run tests
uv run pytest

# Run a single test
uv run pytest tests/pdf/test_check_bounding_boxes.py

# Run Python scripts (uses PEP 723 inline dependencies)
uv run scripts/example.py

# Initialize a new skill
uv run skills/creating-skills/scripts/init_skill.py <skill-name> --path <output-directory>

# Package a skill for distribution
uv run skills/creating-skills/scripts/package_skill.py <path/to/skill-folder>
```

## Key Conventions

- **PEP 723**: Python scripts include inline metadata for `uv run` compatibility
- **Commit messages**: name the affected skill in the subject as prose (e.g. "Add X to ansible skill", "Remove Y from writing-commit-messages skill"). Omit the scope only when the change spans the whole repository.

## Development Notes

- Python 3.13 required (see `.python-version`)
- Dev dependencies managed via `uv` in `pyproject.toml`
- Skills load from: Enterprise > Personal (`~/.claude/skills/`) > Project (`.claude/skills/`) > Plugin
