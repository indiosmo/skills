#!/usr/bin/env bash
# Purpose: Count newline characters in one readable regular file.
# Usage: bash evidence/count_lines.sh evidence/sample.txt
# Notes: Requires Bash 4.4 or later and wc.
set -euo pipefail
shopt -s inherit_errexit

main() {
  if (( $# != 1 )); then
    printf '%s\n' 'Usage: count_lines.sh TEXT_FILE' >&2
    return 2
  fi
  local text_file="$1"
  if [[ ! -f "$text_file" || ! -r "$text_file" ]]; then
    printf '%s\n' 'Input must be a readable regular file.' >&2
    return 1
  fi
  # Standard input keeps the filename out of wc's output.
  wc -l < "$text_file"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
