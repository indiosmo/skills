---
name: authoring-just-recipes
description: >
  Write, review, and debug just (https://github.com/casey/just) command runner recipes and
  justfiles. Covers recipe syntax, parameters, dependencies, attributes, variables, settings,
  cross-platform patterns, shebang recipes, imports, and modules. Use when creating or modifying
  justfiles, writing just recipes, reviewing justfiles for correctness and best practices,
  debugging just invocations, or organizing justfile repositories with imports/modules.
  Triggers on: justfile, .justfile, just recipes, just command runner, just tasks.
---

# Authoring just Recipes

`just` is a command runner (not a build system). All recipes are always "phony" -- no file
dependency tracking. It replaces a Makefile full of `.PHONY` targets.

## Quick Start

```just
# Default recipe: runs when user types `just` with no args
default:
  @just --list

# Doc comment immediately above the recipe appears in `just --list`
# Build the project
build:
  cargo build

# Parameters after recipe name, before colon
deploy env:
  ./deploy.sh {{env}}

# Variadic: one-or-more (+), zero-or-more (*)
push *FLAGS:
  git push {{FLAGS}}

# Parameter with default value
test suite="all":
  ./run-tests --suite {{suite}}
```

## Critical Pitfalls (Read These First)

### 1. Unquoted parameters with spaces split into multiple shell words

```just
# WRONG -- spaces in FILE create multiple shell args
open file:
  cat {{file}}

# CORRECT -- quote the interpolation
open file:
  cat '{{file}}'

# BEST -- export as shell variable (handles all values including single quotes)
open $file:
  cat "$file"
```

### 2. Shell variables don't persist between recipe lines

Each line runs in a separate shell. Use backslash continuation or a shebang recipe:

```just
# WRONG -- $x is gone on the next line
bad:
  x=hello
  echo $x    # empty!

# CORRECT -- shebang recipe (single shell instance)
good:
  #!/usr/bin/env bash
  x=hello
  echo $x
```

### 3. `[script]` uses `script-interpreter`, NOT `set shell`

```just
set shell := ["bash", "-uc"]        # affects recipe lines and backticks only
set script-interpreter := ["bash"]  # ONLY affects [script] recipes (default: sh -eu)

[script]
hello:
  echo "uses script-interpreter, not shell"
```

### 4. `&&` / `||` string coalescing requires `set unstable`

```just
set unstable  # required, or this is a parse error
foo := env('FOO', '') || 'default'
```

### 5. Dotenv variables are env vars, not just variables

```just
set dotenv-load

serve:
  ./server --port $PORT     # correct: shell env var syntax
  ./server --port {{PORT}}  # WRONG: PORT is not a just variable
```

To use a dotenv variable in a just expression: `port := env('PORT', '8080')`

### 6. `justfile_dir()` vs `source_dir()` in imports/modules

`justfile_dir()` always returns the ROOT justfile directory. Inside an imported file or
submodule, use `source_dir()` to get the directory of the current file.

## Recipe Body Essentials

- Indent with spaces OR tabs (not mixed within the same recipe)
- Line prefixes: `@` suppresses echo, `-` ignores exit code, `@-` both
- `@` on recipe name makes all lines quiet by default
- Shebang recipes (`#!/usr/bin/env ...`) run as a single script (quiet by default)

## Safe Bash Shebang Pattern

```just
build:
  #!/usr/bin/env bash
  set -euo pipefail
  # Avoid -x (xtrace) in production -- it prints every command and can leak secrets in CI
  cargo build --release
```

Use `set -euo pipefail` (-e exit on error, -u undefined vars are errors, -o pipefail pipe failures
are errors). Add `-x` only when debugging locally.

## Common Patterns

```just
# Confirmation before destructive action
[confirm("Delete everything?")]
nuke:
  rm -rf dist/

# Private helper (hidden from --list)
[private]
_setup:
  mkdir -p dist/

# Grouped recipes in --list output
[group('build')]
build:
  cargo build

[group('test')]
test:
  cargo test

# Wrapper recipe suppressing just's error footer
[no-exit-message]
git *args:
  @git {{args}}

# Require a tool to be installed before any recipe runs
docker := require("docker")

deploy:
  {{docker}} build -t myapp .
```

## Overriding Variables

```just
version := "1.0.0"

build:
  echo "Building {{version}}"
```

```
just version=2.0.0 build      # inline syntax
just --set version 2.0.0 build  # --set flag
```

## Debugging

```
just --show RECIPE    # print recipe body without running
just --evaluate       # print all variable values
just --dry-run        # print commands without executing
just --dump           # print justfile after parsing/imports
just --fmt --unstable # format justfile in place (--check for CI)
```

## References

Load these as needed:

- **[references/recipes.md](references/recipes.md)** -- Full recipe syntax: parameters, all
  attributes, dependencies, shebang/script recipes, multi-line patterns, default recipes
- **[references/variables-and-settings.md](references/variables-and-settings.md)** -- Variables,
  string types, backticks, all built-in functions, all settings, import/mod system
- **[references/cross-platform.md](references/cross-platform.md)** -- OS detection, platform
  attributes, Windows shell, path handling across OSes
