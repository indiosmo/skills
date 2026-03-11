#!/bin/bash
#
# Symlinks all skills to ~/.claude/skills/ and ~/.agents/skills/
#

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SOURCE="$REPO_ROOT/skills"

TARGETS=(
    "$HOME/.claude/skills"
    "$HOME/.agents/skills"
)

for target_directory in "${TARGETS[@]}"; do
    mkdir -p "$target_directory"

    for skill_directory in "$SKILLS_SOURCE"/*/; do
        skill_name="$(basename "$skill_directory")"

        # Skip hidden directories (e.g. .claude)
        if [[ "$skill_name" == .* ]]; then
            continue
        fi

        link_path="$target_directory/$skill_name"

        if [[ -L "$link_path" ]]; then
            existing_target="$(readlink -f "$link_path")"
            expected_target="$(readlink -f "$skill_directory")"
            if [[ "$existing_target" == "$expected_target" ]]; then
                echo "[OK] $skill_name -> $target_directory (already linked)"
                continue
            fi
            rm "$link_path"
        elif [[ -e "$link_path" ]]; then
            echo "[SKIP] $link_path exists and is not a symlink"
            continue
        fi

        ln -s "$skill_directory" "$link_path"
        echo "[LINKED] $skill_name -> $target_directory"
    done
done

echo ""
echo "Done."
