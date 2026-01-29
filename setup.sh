#!/bin/bash
#
# Setup script for skills repository
# Installs all Python and Node.js dependencies
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Skills Repository Setup"
echo "======================="
echo ""

# Track if we can proceed
can_proceed=true

# Check for uv
if command -v uv &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} uv found: $(uv --version)"
else
    echo -e "${RED}[MISSING]${NC} uv not found"
    echo "    Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "    Or see: https://docs.astral.sh/uv/getting-started/installation/"
    can_proceed=false
fi

# Check for npm
if command -v npm &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} npm found: $(npm --version)"
else
    echo -e "${YELLOW}[MISSING]${NC} npm not found (optional, needed for some skills)"
    echo "    Install Node.js from: https://nodejs.org/"
    echo "    Or with nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash"
fi

echo ""

if [ "$can_proceed" = false ]; then
    echo -e "${RED}Cannot proceed: required tools missing${NC}"
    exit 1
fi

# Get script directory (repo root)
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_ROOT"

# Run uv sync for Python dependencies
echo "Installing Python dependencies..."
if [ -f "pyproject.toml" ]; then
    uv sync
    echo -e "${GREEN}[OK]${NC} Python dependencies installed"
else
    echo -e "${YELLOW}[SKIP]${NC} No pyproject.toml found"
fi

echo ""

# Find and install npm dependencies in skills
echo "Installing Node.js dependencies for skills..."
npm_found=false

for package_json in skills/*/scripts/package.json; do
    if [ -f "$package_json" ]; then
        npm_found=true
        dir=$(dirname "$package_json")
        skill_name=$(basename "$(dirname "$dir")")

        if ! command -v npm &> /dev/null; then
            echo -e "${YELLOW}[SKIP]${NC} $skill_name - npm not available"
            continue
        fi

        echo "  Installing deps for: $skill_name"
        (cd "$dir" && npm install --silent)
        echo -e "  ${GREEN}[OK]${NC} $skill_name"
    fi
done

if [ "$npm_found" = false ]; then
    echo -e "${YELLOW}[SKIP]${NC} No skills with npm dependencies found"
fi

echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "To use skills with Claude Code, symlink them to ~/.claude/skills/"
echo "Example:"
echo "  mkdir -p ~/.claude/skills"
echo "  ln -s $REPO_ROOT/skills/authoring-mermaid-diagrams ~/.claude/skills/"
