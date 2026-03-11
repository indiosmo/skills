---
name: writing-bash-scripts
description: >-
  Write reliable, maintainable Bash scripts with proper error handling, quoting,
  and defensive patterns. Use when creating new Bash scripts, reviewing existing
  ones, fixing shell scripting bugs, or adding tests to shell scripts. Covers
  strict mode with caveats, trap-based cleanup, ShellCheck integration, and
  BATS testing. Triggers on: bash scripts, shell scripts, .sh files, shellcheck,
  bats tests, shell scripting best practices, debugging a pipeline failure in a
  shell script, writing a CI/CD step that runs shell commands, wrapping a CLI
  tool in a script, quoting/word-splitting issues.
---

# Writing Bash Scripts

## Script Template

Every script starts from this skeleton:

```bash
#!/usr/bin/env bash
# Purpose: <one-line summary of what this script does>
# Usage:   <script-name> [options] <required-args>
#          Example: deploy.sh --env staging v1.2.3
# Notes:   <any important caveats, dependencies, or side effects>
set -euo pipefail
shopt -s inherit_errexit

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Helper functions: die writes to stderr and exits; log writes timestamped
# messages to stderr so they don't pollute stdout captures.
die() { printf '%s\n' "$*" >&2; exit 1; }
log() { printf '%s %s\n' "$(date '+%H:%M:%S')" "$*" >&2; }

# Cleanup: runs on every exit (normal, error, or signal) to remove temp files.
cleanup() {
  local exit_code=$?
  rm -f "${TMPFILE:-}"
  exit "$exit_code"
}
trap cleanup EXIT

main() {
  local target="${1:?Usage: $0 <target>}"
  log "Starting"
  # ...
  log "Done"
}

# Entry point guard: allows script to be sourced by tests without running main.
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
```

Key elements:
- `#!/usr/bin/env bash` -- always target bash, not sh
- `set -euo pipefail` + `shopt -s inherit_errexit` -- strict mode (see caveats below)
- All logic in named functions; `main "$@"` guarded by `BASH_SOURCE` check
- `die` and `log` helpers; errors always to stderr
- `trap cleanup EXIT` for resource cleanup
- `readonly` for constants

## Comments

Bash is dense and non-obvious. Comments are not optional.

**Top-level header (required on every script):**

```bash
#!/usr/bin/env bash
# Purpose: Deploys a service to the target environment.
# Usage:   deploy.sh [--dry-run] <environment> <version>
#          Example: deploy.sh --dry-run staging v1.2.3
# Notes:   Requires AWS credentials in environment. Modifies ECS task definitions.
```

**Section comments:** Add a one-line comment before each logical section explaining
its purpose. Bash constructs like traps, pipefail interactions, and associative
arrays are not self-documenting.

```bash
# Parse flags before positional arguments to handle mixed argument order.
while [[ $# -gt 0 ]]; do ...

# Validate all inputs up front before making any changes.
validate_inputs "$environment" "$version"

# Build the image tag and push to ECR before updating the task definition.
push_image "$version"
```

Comment the "why", not the "what":

```bash
# GOOD: explains the non-obvious reason
# Use || true to prevent pipefail from exiting when grep finds no matches.
grep "ERROR" "$logfile" | wc -l || true

# BAD: restates the code
# Increment count
(( ++count ))
```

## Strict Mode Caveats

`set -euo pipefail` is mandatory, but understand where it breaks:

**`set -e` does NOT trigger in conditional contexts:**

```bash
# The entire function body ignores errexit when called from if/&&/||
risky() { false; echo "this runs anyway"; }
if risky; then echo "ok"; fi     # "this runs anyway" prints
risky && echo "ok"               # same -- errexit suppressed inside risky
```

Fix: check return values explicitly for critical operations inside conditionals.

**`set -e` exits on zero arithmetic:**

```bash
count=0
(( count++ ))  # exits! post-increment returns 0 (old value) which is falsy
```

Fix: use `(( ++count ))` (pre-increment) or `(( count++ )) || true`.

**`local` masks exit codes:**

```bash
local output=$(failing_command)   # $? is 0 -- local succeeded
```

Fix: always separate declaration from assignment:

```bash
local output
output=$(failing_command)         # $? reflects the command's exit code
```

**`set -u` and optional variables:**

```bash
echo "$OPTIONAL_VAR"              # error: unbound variable
echo "${OPTIONAL_VAR:-}"          # safe: defaults to empty
echo "${OPTIONAL_VAR:-fallback}"  # safe: defaults to "fallback"
```

Use `${var:-}` for every variable that may legitimately be unset. This includes
optional positional parameters: `local verbose="${2:-false}"`.

**`pipefail` + `grep` interaction:**

```bash
grep "ERROR" logfile | wc -l     # exits if grep finds nothing (exit code 1)
```

Fix: assign first and avoid the pipeline:

```bash
local errors
errors=$(grep "ERROR" logfile || true)
```

`shopt -s inherit_errexit` (already in the template) propagates errexit into
command substitutions. Without it, `var=$(failing_cmd)` silently succeeds inside
a substitution even with `set -e` active.

## Error Handling

### `set -E` (errtrace)

Add `set -E` when using ERR traps. Without it, ERR traps are not inherited by
functions, command substitutions, or subshells -- so errors inside them silently
bypass the trap. With `set -E`, the ERR trap fires wherever an error occurs,
making it useful for logging the exact failure point:

```bash
set -eEuo pipefail

trap 'echo "Error at ${BASH_SOURCE}:${LINENO}" >&2' ERR
```

`set -E` is not in the default template because the template uses an EXIT trap,
which already fires on all exits. Add `set -E` when you need an ERR trap for
diagnostics or when functions must propagate ERR handling to their callers.

### Trap and Cleanup

Trap only `EXIT`. It fires on normal exit, `exit` calls, and signals (in bash).
Trapping `INT TERM` separately causes double-execution of cleanup:

```bash
# CORRECT: single EXIT trap covers all cases in bash
cleanup() {
  local exit_code=$?
  rm -f "${TMPFILE:-}"
  rm -rf "${TMPDIR_WORK:-}"
  exit "$exit_code"
}
trap cleanup EXIT
```

If signal-specific behavior is needed (e.g., printing a message on Ctrl+C):

```bash
trap cleanup EXIT
trap 'echo "Interrupted" >&2; exit 130' INT
trap 'echo "Terminated" >&2; exit 143' TERM
```

Note: the EXIT trap still fires after the INT/TERM handler calls `exit`.

### Temporary Files

Always use `mktemp`. Never use predictable names (symlink attack risk):

```bash
TMPFILE=$(mktemp) || die "Failed to create temp file"
TMPDIR_WORK=$(mktemp -d) || die "Failed to create temp directory"
# cleanup() handles removal via trap
```

### PIPESTATUS

Check individual pipeline stages when a pipeline failure needs diagnosis:

```bash
tar -cf - ./* | gzip > archive.tar.gz
local -a pipe_status=("${PIPESTATUS[@]}")
if (( pipe_status[0] != 0 )); then die "tar failed"; fi
if (( pipe_status[1] != 0 )); then die "gzip failed"; fi
```

### Return Codes

Use meaningful exit codes: 0 for success, 1 for general errors, 2 for usage
errors. For critical operations, check explicitly:

```bash
if ! cp -- "$src" "$dest"; then
  die "Failed to copy $src to $dest"
fi
```

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Script files | lower_snake.sh | `deploy_service.sh` |
| Functions | lower_snake | `validate_input()` |
| Local variables | lower_snake | `local file_count=0` |
| Constants | UPPER_SNAKE + readonly | `readonly MAX_RETRIES=3` |
| Environment vars | UPPER_SNAKE | `export APP_ENV="prod"` |

Prefix project-specific constants to avoid collision with system env vars:
`readonly MYAPP_TIMEOUT=30` not `readonly TIMEOUT=30`.

Functions use POSIX syntax: `name() { }` not `function name() { }`. The
`function` keyword is a bashism that is not portable to POSIX shells (dash, sh),
while the `()` syntax works in all Bourne-family shells.

## Quoting

**Default: quote everything.** The exceptions are explicit:

```bash
"$var"             # always
"${var}_suffix"    # braces needed when adjacent to identifier chars
"$(command)"       # always quote command substitutions
"${array[@]}"      # always -- preserves element boundaries
```

**When NOT to quote:**

```bash
(( count > 10 ))               # arithmetic context -- no quoting
[[ $input =~ ^[0-9]+$ ]]       # regex on right side of =~ must be unquoted
for f in *.txt; do              # intentional globbing
local -a files=(*.log)          # intentional globbing into array
```

**Never store command arguments in strings. Use arrays:**

```bash
# WRONG
flags="--verbose --timeout 30"
curl $flags "$url"

# CORRECT
local -a flags=(--verbose --timeout 30)
curl "${flags[@]}" "$url"
```

## Control Flow

Use `[[ ]]` for tests (no word splitting, supports `&&`/`||`/regex):

```bash
if [[ -z "$var" ]]; then ...           # empty check
if [[ "$var" == pattern* ]]; then ...  # glob match (unquoted right side)
if [[ "$var" =~ ^[0-9]+$ ]]; then ... # regex (unquoted right side)
```

Use `(( ))` for arithmetic:

```bash
if (( retries < max_retries )); then ...
(( ++count ))
result=$(( width * height ))
```

Use `$(cmd)` for command substitution, never backticks.

Use `printf` for formatted or potentially unsafe output. `echo` is fine for
simple fixed messages like `echo "Done"`.

### Process Substitution

Avoid piping into `while read` -- variables set inside the loop are lost
(subshell). Use process substitution or redirection:

```bash
# WRONG: count is lost after the loop
count=0
some_cmd | while IFS= read -r line; do (( ++count )); done
echo "$count"  # 0

# CORRECT: process substitution keeps the loop in the current shell
count=0
while IFS= read -r line; do (( ++count )); done < <(some_cmd)
echo "$count"  # correct value

# CORRECT: reading from a file
while IFS= read -r line; do ...  done < "$file"
```

## Functions

- All logic in named functions. Keep `main` as the entry point.
- Declare variables `local` to prevent namespace leakage.
- Name positional parameters for readability:

```bash
deploy() {
  local environment="$1"
  local version="$2"
  local dry_run="${3:-false}"
  # ...
}
```

- Extract complex conditionals into named predicates:

```bash
is_installed() { command -v "$1" &>/dev/null; }
is_root() { [[ $EUID -eq 0 ]]; }

if ! is_installed docker; then
  die "docker is required"
fi
```

- Make scripts testable with BATS by guarding direct execution:

```bash
main() { ... }

# Only execute main when run directly, not when sourced by tests
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
```

## Argument Parsing

Use `getopts` for short options or a manual `while/case` loop for long options.
When implementing argument parsing, load
[references/patterns.md](references/patterns.md) and consult the "Argument
Parsing" section for full examples of both patterns including `usage()`,
`OPTARG` handling, and `shift` logic.

## Security

- Use `--` before filenames to prevent option injection: `rm -- "$file"`
- Validate untrusted input with whitelist patterns:

```bash
validate_name() {
  local input="$1"
  if [[ ! "$input" =~ ^[a-zA-Z0-9_.-]+$ ]]; then
    die "Invalid name: contains disallowed characters"
  fi
}
```

- Never pass untrusted input to `eval`, `bash -c`, or unquoted expansions
- Use `mktemp` for temp files (prevents predictable-name attacks)
- Lock `PATH` in privileged scripts: `export PATH="/usr/local/bin:/usr/bin:/bin"`
- Use `flock` for atomic lock files instead of test-then-create patterns
- When dealing with dynamic variable names or command construction, load
  [references/patterns.md](references/patterns.md) and consult the "Eval:
  Dangerous, Safe, and Legitimate" section for safe alternatives

## ShellCheck

Run `shellcheck` on every script. Enforce in CI:

```bash
shellcheck -x --severity=warning script.sh
```

Flags:
- `-x` -- follow `source` statements
- `--severity=warning` -- skip style-only hints
- `-f diff` -- output as a patch (useful for auto-fix)

Suppress intentional violations inline:

```bash
# shellcheck disable=SC2086
echo $intentionally_unquoted
```

Specify shell for files without shebang:

```bash
# shellcheck shell=bash
```

## Testing with BATS

Use [bats-core](https://github.com/bats-core/bats-core) with
[bats-assert](https://github.com/bats-core/bats-assert) and
[bats-support](https://github.com/bats-core/bats-support).

```bash
#!/usr/bin/env bats

load 'test_helper/bats-support/load'
load 'test_helper/bats-assert/load'

setup() {
  source "${BATS_TEST_DIRNAME}/../my_script.sh"
  TEST_DIR=$(mktemp -d)
}

teardown() {
  rm -rf "$TEST_DIR"
}

@test "validates input rejects special characters" {
  run validate_name "foo;bar"
  assert_failure
  assert_output --partial "disallowed characters"
}
```

Core assertions: `run` captures exit code in `$status` and output in
`$output`/`${lines[@]}`. Use `assert_success`/`assert_failure` for exit codes
and `assert_output --partial "substring"` for output checks.

When writing BATS tests beyond this basic pattern -- lifecycle hooks
(`setup_file`/`teardown_file`), test tags, mocking external commands, or the
full assertions list -- load [references/patterns.md](references/patterns.md)
and consult the "Advanced BATS Testing" section.

## When to Use a Different Language

Bash is the right tool for orchestrating other commands, glue scripts, and
lightweight automation. Switch to Python, Go, or another language when:

- The script needs non-trivial data structures (nested maps, objects)
- You need to parse JSON/XML/YAML beyond simple `jq`/`yq` calls
- Complex string manipulation dominates the logic
- The script exceeds ~300 lines and is still growing
- Cross-platform portability beyond Linux is required
- Error handling requirements exceed what trap/set -e can provide

## Debugging

Enable trace output for a script or a section:

```bash
export PS4='+${BASH_SOURCE}:${LINENO}: '
set -x   # trace every command with file:line prefix
# ... section to debug ...
set +x   # disable tracing
```

Run from outside: `TRACE=1 ./script.sh` with this preamble:

```bash
if [[ "${TRACE:-0}" == "1" ]]; then set -o xtrace; fi
```

Syntax-check without executing: `bash -n script.sh`

## Portability Note

This skill targets **bash 4.4+**. macOS ships bash 3.2 (GPLv2). If targeting
macOS, either require `brew install bash` or avoid: associative arrays,
namerefs (`declare -n`), `mapfile`/`readarray`, `inherit_errexit`, `wait -n`.

## Reference

Load [references/patterns.md](references/patterns.md) when you need:
- Eval alternatives and safe indirect variable access
- Advanced BATS testing (mocking, lifecycle hooks, test tags, full assertion list)
- Antipatterns catalog (parsing ls, pipeline variable loss, in-place clobber)
- Modern bash features (associative arrays, mapfile, namerefs, parallel jobs)
- Logging patterns, argument parsing templates, and common recipes
