#!/usr/bin/env bash
# Blocks git operations that create commits, mutate remotes, or rewrite history.

set -euo pipefail

payload=$(cat)
command_string=$(jq -r '.command // .tool_input.command // ""' <<<"$payload")

git_write_pattern='\bgit\b([^|&;]*[[:space:]])?(commit|push|reset|rebase)([[:space:]]|$)'
bypass_flag_pattern='(^|[[:space:]])--no-(verify|gpg-sign)([[:space:]]|$)'

if printf '%s' "$command_string" | grep -qE "$git_write_pattern"; then
    cat >&2 <<'EOF'
Blocked by user policy:
git commit, push, reset, and rebase are not allowed from Cursor Agent.
EOF
    exit 2
fi

if printf '%s' "$command_string" | grep -qE "$bypass_flag_pattern"; then
    cat >&2 <<'EOF'
Blocked by user policy:
commands using --no-verify or --no-gpg-sign are not allowed from Cursor Agent.
EOF
    exit 2
fi

exit 0
