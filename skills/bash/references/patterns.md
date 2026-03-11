# Bash Patterns Reference

Detailed patterns and examples. Load this file when the main SKILL.md needs
deeper coverage on a specific topic.

## Table of Contents

- [Eval: Dangerous, Safe, and Legitimate](#eval-dangerous-safe-and-legitimate)
- [Advanced BATS Testing](#advanced-bats-testing)
- [Antipatterns Catalog](#antipatterns-catalog)
- [Modern Bash Features](#modern-bash-features)
- [Logging Patterns](#logging-patterns)
- [Argument Parsing](#argument-parsing)
- [Common Recipes](#common-recipes)

---

## Eval: Dangerous, Safe, and Legitimate

### Why eval is dangerous

`eval` parses its argument twice -- one layer of quoting is stripped before
execution. Untrusted input becomes code:

```bash
# DANGEROUS: user controls what gets executed
user_input='$(rm -rf /)'
eval "echo $user_input"   # executes the rm command

# DANGEROUS: injection through variable names
key='x; rm -rf /'
eval "$key=value"
```

### Safe alternatives

**Indirect expansion `${!var}` -- read a variable by name:**

```bash
config_host="localhost"
config_port="8080"

lookup() {
  local key="config_$1"
  printf '%s\n' "${!key}"
}

lookup host   # prints: localhost
```

**Namerefs `declare -n` (bash 4.3+) -- read/write a variable by name:**

```bash
set_value() {
  local -n target="$1"
  target="$2"
}

my_var="old"
set_value my_var "new"
echo "$my_var"  # prints: new
```

Namerefs work with arrays too:

```bash
sum_array() {
  local -n arr="$1"
  local total=0
  for n in "${arr[@]}"; do (( total += n )); done
  echo "$total"
}

declare -a numbers=(10 20 30)
sum_array numbers  # prints: 60
```

Nameref caveat -- no circular references:

```bash
declare -n ref1=ref2
declare -n ref2=ref1   # undefined behavior
```

**`printf -v` -- assign to a variable by name:**

```bash
varname="result"
printf -v "$varname" '%s' "hello world"
echo "$result"  # prints: hello world
```

**Arrays for command construction -- replaces eval for building commands:**

```bash
# WRONG: eval to handle complex commands
eval "$cmd $args"

# CORRECT: array preserves argument boundaries
local -a cmd_parts=(rsync --archive --verbose --exclude='*.tmp')
cmd_parts+=("$source" "$dest")
"${cmd_parts[@]}"
```

### Legitimate eval use cases

Some tools are *designed* to produce eval-safe output. These are acceptable:

```bash
eval "$(ssh-agent -s)"
eval "$(direnv export bash)"
eval "$(rbenv init -)"
eval "$(pyenv init -)"
```

These are safe because the output comes from trusted programs, not user input.
If in doubt, inspect the output first: `ssh-agent -s` to see what it generates.

---

## Advanced BATS Testing

### Project structure

```
project/
  scripts/
    deploy.sh
    backup.sh
  tests/
    test_helper/
      bats-support/    (git submodule or subtree)
      bats-assert/     (git submodule or subtree)
      bats-file/       (optional: filesystem assertions)
      mocks/
        curl           (stub for curl)
        docker         (stub for docker)
    deploy.bats
    backup.bats
```

### Making scripts testable

Guard `main` so BATS can source the script and call individual functions:

```bash
# In deploy.sh
main() {
  local env="$1"
  validate_env "$env"
  run_deploy "$env"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
```

```bash
# In deploy.bats
setup() {
  source "${BATS_TEST_DIRNAME}/../scripts/deploy.sh"
}

@test "validate_env rejects invalid environment" {
  run validate_env "invalid"
  assert_failure
}
```

### Mocking external commands

Create stub scripts in `tests/test_helper/mocks/` and prepend to PATH:

```bash
# tests/test_helper/mocks/curl
#!/usr/bin/env bash
# Stub curl that records calls and returns canned responses
echo "curl called with: $*" >> "${MOCK_LOG:-/dev/null}"
echo '{"status": "ok"}'
exit 0
```

```bash
# In the test file
setup() {
  export PATH="${BATS_TEST_DIRNAME}/test_helper/mocks:${PATH}"
  export MOCK_LOG=$(mktemp)
  source "${BATS_TEST_DIRNAME}/../scripts/deploy.sh"
}

teardown() {
  rm -f "$MOCK_LOG"
}

@test "deploy calls curl with correct URL" {
  run run_deploy staging
  assert_success
  run grep "https://staging.example.com" "$MOCK_LOG"
  assert_success
}
```

### Useful assertions

```bash
# Exit code
assert_success                     # exit code 0
assert_failure                     # exit code non-zero
assert_failure 2                   # exit code exactly 2

# Output
assert_output "exact match"
assert_output --partial "substring"
refute_output --partial "should not appear"
assert_output --regexp '^[0-9]+ files'

# Lines
assert_line --index 0 "first line"
assert_line --partial "appears on some line"
assert_equal "$actual" "$expected"

# With bats-file (if installed)
assert_file_exists "$path"
assert_dir_exists "$path"
assert_file_contains "$path" "expected content"
```

### Lifecycle hooks

```bash
setup_file() {
  # Runs once before all tests in the file
  export TEST_TMPDIR=$(mktemp -d)
  # Build binaries, start services, etc.
}

teardown_file() {
  # Runs once after all tests in the file
  rm -rf "$TEST_TMPDIR"
}

setup() {
  # Runs before each @test
}

teardown() {
  # Runs after each @test
}
```

### Test tags (bats-core 1.7+)

```bash
# bats file_tags=unit

# bats test_tags=smoke
@test "basic functionality" { ... }

# bats test_tags=integration,slow
@test "full pipeline test" { ... }
```

Run filtered: `bats --filter-tags smoke tests/`

---

## Antipatterns Catalog

### Parsing ls output

```bash
# WRONG: breaks on spaces, globs, newlines in filenames
for f in $(ls *.mp3); do echo "$f"; done

# CORRECT: shell globbing
for f in *.mp3; do
  [[ -e "$f" ]] || continue   # handle no-match case
  echo "$f"
done
```

### Unquoted variables

```bash
file="my file.txt"
cat $file     # WRONG: word-splits into "my" and "file.txt"
cat "$file"   # CORRECT
```

### local var=$(cmd) masking exit status

```bash
local output=$(failing_cmd)   # WRONG: exit code masked by local
local output                  # CORRECT: separate
output=$(failing_cmd)         # $? reflects the real exit code
```

### Pipeline variable loss

```bash
count=0
cat file | while IFS= read -r line; do (( ++count )); done
echo "$count"   # WRONG: 0 -- subshell

count=0
while IFS= read -r line; do (( ++count )); done < file
echo "$count"   # CORRECT
```

### Useless use of cat

```bash
cat file | grep "pattern"     # unnecessary process
grep "pattern" file           # direct

# Exception: cat is acceptable for readability in long pipelines:
cat data.csv |
  grep -v '^#' |
  cut -d',' -f2 |
  sort -u
```

### Useless use of echo in pipes

```bash
echo "$var" | grep "pattern"  # unnecessary
grep "pattern" <<< "$var"     # here-string
```

### Useless use of grep | awk

```bash
grep "error" log.txt | awk '{print $2}'   # redundant grep
awk '/error/{print $2}' log.txt           # awk has regex built in
```

### In-place file clobber

```bash
sed 's/foo/bar/g' file > file           # WRONG: clobbers before reading
sed 's/foo/bar/g' file > tmp && mv tmp file   # CORRECT
sed -i 's/foo/bar/g' file              # CORRECT (GNU sed)
```

### Storing lists in strings

```bash
# WRONG: breaks on spaces, can't handle empty elements
files="file one.txt file two.txt"
for f in $files; do echo "$f"; done

# CORRECT: array
files=("file one.txt" "file two.txt")
for f in "${files[@]}"; do echo "$f"; done
```

### read without -r

```bash
read line <<< "path\\to\\file"     # WRONG: backslashes interpreted
read -r line <<< "path\\to\\file"  # CORRECT: raw mode
```

---

## Modern Bash Features

### Associative arrays (bash 4.0+)

```bash
declare -A config=(
  [host]="localhost"
  [port]="8080"
  [protocol]="https"
)

for key in "${!config[@]}"; do
  printf '%s = %s\n' "$key" "${config[$key]}"
done

# Check key existence (bash 4.2+)
if [[ -v config[host] ]]; then echo "set"; fi
```

### mapfile / readarray (bash 4.0+)

Read lines from a file or command into an array without a loop:

```bash
mapfile -t lines < file.txt
mapfile -t users < <(getent passwd | cut -d: -f1)

for line in "${lines[@]}"; do
  echo "$line"
done
```

### Parameter expansion

```bash
${var:-default}        # use default if unset/empty
${var:=default}        # assign default if unset/empty
${var:?error message}  # exit with error if unset/empty
${var:+replacement}    # use replacement if set and non-empty

${var#pattern}         # remove shortest prefix match
${var##pattern}        # remove longest prefix match
${var%pattern}         # remove shortest suffix match
${var%%pattern}        # remove longest suffix match

${var/pattern/replace}   # replace first match
${var//pattern/replace}  # replace all matches

${var:0:5}             # substring: first 5 chars
${#var}                # string length
${#array[@]}           # array length
```

### Parallel job management (bash 4.3+)

```bash
max_jobs=4
for task in "${tasks[@]}"; do
  process_task "$task" &
  if (( $(jobs -r | wc -l) >= max_jobs )); then
    wait -n   # wait for any one job to finish
  fi
done
wait  # wait for remaining
```

### Heredocs

```bash
# Variable expansion (unquoted delimiter)
cat <<EOF
Hello, $USER. Today is $(date).
EOF

# No expansion (quoted delimiter)
cat <<'EOF'
This $var is literal. No $(expansion).
EOF

# Strip leading tabs (<<-)
if true; then
	cat <<-EOF
		Indented with tabs; tabs are stripped.
	EOF
fi

# Assign to variable
read -r -d '' help_text <<'EOF' || true
Usage: script.sh [OPTIONS]
  -h    Show this help
  -v    Enable verbose mode
EOF
```

---

## Logging Patterns

Simple structured logging to stderr:

```bash
readonly LOG_LEVEL="${LOG_LEVEL:-INFO}"

_log() {
  local level="$1"; shift
  printf '%s [%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$level" "$*" >&2
}

log_debug() { [[ "$LOG_LEVEL" == "DEBUG" ]] && _log DEBUG "$@" || true; }
log_info()  { _log INFO "$@"; }
log_warn()  { _log WARN "$@"; }
log_error() { _log ERROR "$@"; }
die()       { log_error "$@"; exit 1; }
```

Usage: `LOG_LEVEL=DEBUG ./script.sh` for verbose output.

---

## Argument Parsing

### Short options with getopts

```bash
usage() { die "Usage: $0 [-v] [-t timeout] target"; }

verbose=false
timeout=30

while getopts ':vt:h' opt; do
  case "$opt" in
    v) verbose=true ;;
    t) timeout="$OPTARG" ;;
    h) usage ;;
    :) die "Option -$OPTARG requires an argument" ;;
    ?) die "Unknown option: -$OPTARG" ;;
  esac
done
shift $((OPTIND - 1))

target="${1:?$(usage)}"
```

### Long options with while/case

```bash
while (( $# > 0 )); do
  case "$1" in
    --verbose) verbose=true; shift ;;
    --timeout) timeout="${2:?--timeout requires a value}"; shift 2 ;;
    --) shift; break ;;
    -*) die "Unknown option: $1" ;;
    *) break ;;
  esac
done
```

### Parameter expansion defaults

```bash
local config="${CONFIG_FILE:-config.yaml}"
local port="${PORT:-8080}"
local env="${1:?Usage: $0 <environment>}"   # required, exits if missing
```

---

## Common Recipes

### Safe file iteration with find

```bash
# WRONG: breaks on spaces/newlines in filenames
for f in $(find . -name '*.log'); do echo "$f"; done

# CORRECT: null-delimited
while IFS= read -r -d '' file; do
  echo "$file"
done < <(find . -name '*.log' -print0)

# CORRECT: find -exec
find . -name '*.log' -exec process {} \;

# CORRECT: find + xargs (null-delimited)
find . -name '*.log' -print0 | xargs -0 process
```

### Atomic lock file with flock

```bash
exec 200>/var/lock/myscript.lock
if ! flock -n 200; then
  die "Another instance is already running"
fi
# Lock is held for the duration of the script
# Released automatically when fd 200 is closed (script exits)
```

### Retry with backoff

```bash
retry() {
  local max_attempts="${1:?}"
  local delay="${2:?}"
  shift 2
  local attempt=1
  while (( attempt <= max_attempts )); do
    if "$@"; then return 0; fi
    log_warn "Attempt $attempt/$max_attempts failed. Retrying in ${delay}s..."
    sleep "$delay"
    (( ++attempt ))
    (( delay *= 2 ))
  done
  return 1
}

retry 5 2 curl --fail --silent "$url"
```

### Check command existence

```bash
require_cmd() {
  if ! command -v "$1" &>/dev/null; then
    die "'$1' is required but not installed"
  fi
}

require_cmd docker
require_cmd jq
require_cmd shellcheck
```

### Cross-platform sed in-place

macOS sed requires `sed -i ''` while GNU sed uses `sed -i`. Avoid the issue:

```bash
sed_inplace() {
  local expr="$1" file="$2"
  sed "$expr" "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
}

sed_inplace 's/old/new/g' config.txt
```
