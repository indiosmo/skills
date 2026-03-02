# just Recipes: Full Reference

## Contents

- [Recipe Declaration](#recipe-declaration)
- [Parameters](#parameters)
- [Parameter Constraints and Named Flags](#parameter-constraints-and-named-flags--1450)
- [Dependencies](#dependencies)
- [Attributes](#attributes)
- [Doc Comments and --list](#doc-comments-and---list)
- [Default Recipe](#default-recipe)
- [Shebang Recipes](#shebang-recipes)
- [Multi-Line Shell Constructs in Linewise Recipes](#multi-line-shell-constructs-in-linewise-recipes)
- [Aliases](#aliases)
- [Choosing Interactively](#choosing-interactively)

## Recipe Declaration

```
NAME PARAMS* ':' DEPENDENCIES? eol BODY?
```

Recipe names: `[a-zA-Z_][a-zA-Z0-9_-]*` (kebab-case is convention)

## Parameters

```just
# Positional -- accessed via {{name}} in body
build target:
  cc {{target}}

# Exported -- accessible as $name in shell
test $RUST_BACKTRACE="1":
  cargo test

# Variadic one-or-more (+)
backup +FILES:
  scp {{FILES}} server:~

# Variadic zero-or-more (*)
push *FLAGS:
  git push {{FLAGS}}

# Default value (can be any expression)
deploy env="staging":
  ./deploy.sh {{env}}
```

All parameters with defaults must follow parameters without defaults.

Variadic `+` requires at least one argument. `*` accepts zero (expands to empty string).

## Parameter Constraints and Named Flags (>= 1.45.0)

```just
# Regex-constrained parameter
[arg('env', pattern='^(staging|production)$')]
deploy env:
  ./deploy.sh {{env}}

# Named/flag parameters (>= 1.46.0)
[arg('verbose', long='verbose', short='v')]
[arg('target', long='target')]
build verbose='false' target='debug':
  @echo "verbose={{verbose}} target={{target}}"
```

## Dependencies

```just
# Prior dependencies (run before recipe body)
test: build lint
  ./run-tests

# Passing arguments to a dependency
push target: (build target)
  git push

# Subsequent dependencies (run after recipe body, since 1.17.0)
release: build && publish notify

# Deduplication: same recipe + same args runs only once per invocation
```

Mid-recipe dependency invocation is not supported natively. Call `just` recursively
(caveat: new process, all assignments re-evaluated, command-line vars not propagated).

## Attributes

Place immediately before the recipe, one per line (or comma-separated on one line since 1.14.0):

```just
[private]
[no-cd]
helper:
  echo "private and no-cd"

# Equivalent:
[private, no-cd]
helper:
  echo "private and no-cd"
```

### Full Attribute Reference

| Attribute | Min Ver | Description |
|-----------|---------|-------------|
| `[private]` | 1.10.0 | Hide from `--list`/`--summary`. Also works on aliases and variables |
| `[no-exit-message]` | 1.7.0 | Suppress "Recipe X failed" error line on non-zero exit |
| `[unix]` | 1.8.0 | Enable only on Unix (includes macOS) |
| `[linux]` | 1.8.0 | Enable only on Linux |
| `[macos]` | 1.8.0 | Enable only on macOS |
| `[windows]` | 1.8.0 | Enable only on Windows |
| `[openbsd]` | 1.38.0 | Enable only on OpenBSD |
| `[confirm]` | 1.17.0 | Prompt for confirmation before running |
| `[confirm("PROMPT")]` | 1.23.0 | Prompt with custom message |
| `[doc("TEXT")]` | 1.27.0 | Override doc comment in `--list` |
| `[doc]` | 1.27.0 | Suppress doc comment in `--list` |
| `[no-cd]` | 1.9.0 | Don't change to justfile directory before running |
| `[no-quiet]` | 1.23.0 | Always echo lines even when `set quiet` is active |
| `[positional-arguments]` | 1.29.0 | Pass args as `$0`, `$1`, etc. to shell |
| `[parallel]` | 1.42.0 | Run dependencies in parallel |
| `[default]` | 1.43.0 | Mark as default recipe (alternative to first-recipe convention) |
| `[group("NAME")]` | 1.27.0 | Assign to named group in `--list` |
| `[env("NAME", "VALUE")]` | - | Set an environment variable for this recipe only |
| `[script]` | 1.33.0 | Execute body as script using `set script-interpreter` (NOT `set shell`) |
| `[script("CMD")]` | 1.32.0 | Execute body as script using CMD (requires `set unstable`) |
| `[extension("EXT")]` | 1.32.0 | Set temp file extension for shebang recipe (important on Windows) |
| `[working-directory('PATH')]` | 1.38.0 | Set working directory for this recipe |
| `[metadata("DATA")]` | 1.42.0 | Attach arbitrary metadata string |
| `[arg('NAME', pattern=...)]` | 1.45.0 | Regex-constrain a parameter |
| `[arg('NAME', long=..., short=...)]` | 1.46.0 | Named/flag parameter |

Platform attributes combine with OR: `[linux]` + `[macos]` means "Linux or macOS".

### `[env]` attribute example

```just
# Inject env var for this recipe only (cleaner than global export)
[env('RUST_BACKTRACE', '1')]
test:
  cargo test
```

## Doc Comments and `--list`

```just
# This comment becomes the doc (must be immediately above -- no blank line)
build:
  cargo build

# Explicitly set or suppress
[doc('Run all tests')]
test:
  cargo test

[doc]
_hidden-but-unlisted:
  echo "shown in --list without doc"
```

## Default Recipe

```just
# Convention 1: first recipe is default (position matters)
default:
  @just --list

# Convention 2: explicit default attribute (>= 1.43.0)
[default]
test:
  cargo test
```

## Shebang Recipes

First body line starting with `#!` makes the recipe a shebang recipe. The full body is
written to a temp file and executed. Quiet by default (no line echo).

```just
# Python
analyze:
  #!/usr/bin/env python3
  import sys
  print(f"Running on {sys.platform}")

# Node
gen-config:
  #!/usr/bin/env node
  const fs = require('fs');
  fs.writeFileSync('config.json', JSON.stringify({version: '{{version}}'}));

# Safe bash
build:
  #!/usr/bin/env bash
  set -euo pipefail
  cargo build --release
```

`{{expr}}` interpolation happens before the script is written to disk.

On Windows, shebang paths containing `/` go through `cygpath`. For portability, prefer
`[script("interpreter")]` which avoids shebang parsing entirely.

`[extension("py")]` sets the temp file extension (useful on Windows where `.py` triggers Python).

## Multi-Line Shell Constructs in Linewise Recipes

Linewise recipes cannot have extra indentation in `if`/`for`/`while` blocks. Options:

```just
# One-liner
check:
  if test -f config.json; then echo "found"; fi

# Backslash continuation
check:
  if test -f config.json; then \
    echo "found"; \
  fi

# Shebang (cleanest for complex logic)
check:
  #!/usr/bin/env sh
  if test -f config.json; then
    echo "found"
  fi
```

## Aliases

```just
alias b := build
alias t := test

# Private alias (hidden from --list)
[private]
alias bld := build

# Alias into submodule (requires mod to exist)
mod deploy
alias d := deploy::run
```

## Choosing Interactively

```just
default:
  @just --choose   # launches fzf; skip in CI (requires TTY)
```

`JUST_CHOOSER` env var or `--chooser` flag sets the chooser program. Recipes with
required parameters are excluded from the chooser.
