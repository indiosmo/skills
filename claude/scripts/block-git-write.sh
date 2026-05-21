#!/usr/bin/env bash
# PreToolUse hook for the Bash tool.
#
# Receives the tool-call JSON on stdin. Blocks any Bash command that contains
# "git commit" or "git push" as a subcommand, including bypass forms the
# prefix-based Bash(git commit:*) / Bash(git push:*) deny rules miss:
#
#   git -C <path> commit ...
#   cd <path> && git push ...
#   GIT_DIR=... git commit ...
#
# Exits 2 with a stderr message to signal "deny" to Claude Code.

set -euo pipefail

command_string=$(jq -r '.tool_input.command // ""')

# Regex breakdown:
#   \bgit\b                       word "git"
#   ([^|&;]*[[:space:]])?         optional args between git and the
#                                 subcommand, but only within one shell
#                                 command (no |, &, ; separators)
#   (commit|push)                 the subcommand we want to catch
#   ([[:space:]]|$)               followed by whitespace or end of string,
#                                 so "commit.py" / "pushed" don't match
pattern='\bgit\b([^|&;]*[[:space:]])?(commit|push)([[:space:]]|$)'

if printf '%s' "$command_string" | grep -qE "$pattern"; then
    cat >&2 <<EOF
Blocked by user policy (PreToolUse hook block-git-write.sh):
bash commands containing 'git commit' or 'git push' are not allowed,
including bypass forms like 'git -C <path> commit' or
'cd <path> && git push'.
EOF
    exit 2
fi

exit 0
