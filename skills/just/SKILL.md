---
name: just
description: >
  Write, review, and debug just (https://github.com/casey/just) command runner recipes and
  justfiles. Covers recipe syntax, parameters, dependencies, attributes, variables, settings,
  cross-platform patterns, shebang recipes, imports, and modules. Use when creating or modifying
  justfiles, writing just recipes, reviewing justfiles for correctness and best practices,
  debugging just invocations, or organizing justfile repositories with imports/modules.
  Triggers on: justfile, .justfile, just recipes, just command runner, just tasks, task runner,
  Makefile alternative, project commands, justfile syntax errors, command runner. Even if the user
  just says "task runner" or "command runner" in a context where just is being used, consult this
  skill. Always load this skill when a justfile is present in the project or the user mentions just
  in the context of running tasks.
---

# Authoring just Recipes

`just` is a command runner (not a build system). Recipes describe actions to perform, not
artifacts to produce -- there is no concept of an output file being "up to date." All recipes are
always "phony" -- no file dependency tracking. It replaces a Makefile full of `.PHONY` targets.

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

## Error Handling

In linewise recipes (the default), each line runs in its own shell, and `just` aborts the recipe
if any line exits with a non-zero status. This means linewise recipes already behave like
`set -e` -- you do not need to add it. However, a single line containing a pipeline like
`cmd1 | cmd2` only checks the exit code of the last command unless the shell has `pipefail` set.

In shebang and `[script]` recipes, the entire body runs as one script. The default
`script-interpreter` is `sh -eu`, so `[script]` recipes exit on the first error by default.
For shebang recipes, you control error handling yourself -- always include `set -euo pipefail`
in bash shebangs.

The `-` line prefix tells `just` to ignore a non-zero exit code for that line. Use it only for
commands where failure is expected and acceptable, such as cleanup steps or optional checks:

```just
clean:
  -rm -rf dist/
  -rm -rf tmp/
  mkdir -p dist/
```

Do not blanket-prefix lines with `-` to suppress errors -- that hides real failures.

## `[script]` vs Shebang Recipes

Both `[script]` and shebang recipes run the body as a single script (solving the
line-independence problem), but they differ in important ways:

- `[script]` uses the `script-interpreter` setting (default: `sh -eu`). Use it when you want a
  uniform interpreter controlled at the justfile level and sensible defaults without boilerplate.
- Shebang recipes (`#!/usr/bin/env bash`) let each recipe pick its own interpreter and flags.
  Use them when a recipe needs a specific shell (bash, python, node) or specific flags like
  `set -o pipefail` that go beyond the `script-interpreter` default.

Prefer `[script]` for straightforward multi-line recipes that just need line persistence.
Prefer shebangs when you need bash-specific features, a non-shell interpreter, or per-recipe
control over error behavior.

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

Load the appropriate reference file based on the task at hand:

- **[references/recipes.md](references/recipes.md)** -- Load when writing or reviewing recipe
  definitions: parameters, attributes (like `[confirm]`, `[group]`, `[no-cd]`), dependencies,
  shebang/script recipe syntax, multi-line constructs, or default recipe selection. This is the
  first file to consult for any recipe authoring question.
- **[references/variables-and-settings.md](references/variables-and-settings.md)** -- Load when
  the task involves variables, string interpolation, backtick expressions, built-in functions
  (like `env()`, `arch()`, `justfile_dir()`), justfile settings (like `set shell`, `set dotenv-load`),
  or the import/mod system. Consult this whenever the user asks about configuring justfile behavior.
- **[references/cross-platform.md](references/cross-platform.md)** -- Load when the justfile
  must work across operating systems, when using `os()` or `os_family()` conditionals, when
  setting platform-specific shells (especially Windows), or when handling path separators.
  Always consult this if the user mentions Windows, cross-platform, or portable recipes.
