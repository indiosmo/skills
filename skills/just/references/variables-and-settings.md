# just Variables, Expressions, Settings, and Modules

## Contents

- [Variables](#variables)
- [String Types](#string-types)
- [Backtick Evaluation](#backtick-evaluation)
- [Expressions](#expressions)
- [Built-in Functions](#built-in-functions)
- [Settings](#settings)
- [Exporting Variables](#exporting-variables)
- [Imports and Modules](#imports-and-modules)
- [set fallback behavior](#set-fallback-behavior)

## Variables

```just
name    := "world"
version := `git describe --tags --abbrev=0`   # backtick: capture shell stdout
home    := env('HOME')                         # read from environment (aborts if missing)
port    := env('PORT', '8080')                 # with fallback default
```

Only `:=` is supported (no `?=` like make). Variables are order-independent at parse time.
To allow later definitions to win: `set allow-duplicate-variables`.

Variables cannot be defined inside a recipe body. Use shell variables there instead.

### Overriding from the command line

```
just version=2.0.0 build
just --set version 2.0.0 build
```

## String Types

| Type | Syntax | Notes |
|------|--------|-------|
| Single-quoted | `'raw string'` | No escape processing |
| Double-quoted | `"processed \n string"` | `\n` `\t` `\r` `\\` `\"` `\u{XXXX}` (>= 1.36.0) |
| Triple single | `'''...'''` | Strips common leading whitespace, no escapes |
| Triple double | `"""..."""` | Strips common leading whitespace + processes escapes |
| Shell-expanded | `x'~/.config'` | Expands `~`, `$VAR`, `${VAR:-DEFAULT}` at parse time |
| Format string | `f'Hello {{name}}!'` | `{{expr}}` interpolation in string literal (>= 1.44.0) |

Shell-expanded strings (`x'...'`) expand at justfile parse time, before recipe execution.
Environment variables must already be set before `just` is invoked. Dotenv variables and
exported just variables are NOT available -- this is by design.

## Backtick Evaluation

```just
date := `date +%Y-%m-%d`

# Triple backtick -- strips common leading whitespace
stuff := ```
  echo foo
  echo bar
```
```

Trailing newlines are stripped. The shell used is controlled by `set shell`.

**Critical:** Exported just variables are NEVER visible inside backtick expressions, even with
`set export`. This applies at file scope regardless of the export mechanism used.

Use `shell(command, args...)` (>= 1.27.0) for more control:
```just
file  := '/sys/class/power_supply/BAT0/status'
status := shell('cat "$1"', file)   # passes file as $1, safe for paths with spaces
```

## Expressions

```just
# Concatenation
greeting := "Hello" + ", " + name + "!"

# Path joining (always uses /, even on Windows -- prefer over join())
config_path := justfile_dir() / "config" / "app.toml"

# Conditional
profile := if os() == "macos" { "darwin" } else { "linux" }
build_type := if env('CI', '') != "" { "release" } else { "debug" }

# Regex match (Rust regex crate syntax)
is_tag := if version =~ '^v\d+\.\d+\.\d+$' { "true" } else { "false" }

# Chained conditional
pkg_mgr := if os() == "macos" { "brew" } else if os() == "linux" { "apt" } else { "choco" }

# Error on missing condition
api_key := if env('API_KEY', '') == "" { error("API_KEY must be set") } else { env('API_KEY') }
```

**Note:** `&&` and `||` string coalescing operators require `set unstable`:
```just
set unstable
foo := env('FOO', '') || 'default'
```

## Built-in Functions

### Environment
```just
env('KEY')                   # abort if not set
env('KEY', 'default')        # return default if not set
```
`env_var()` and `env_var_or_default()` are deprecated aliases; use `env()`.

### System info
```just
os()           # "linux", "macos", "windows", "freebsd", etc.
os_family()    # "unix" or "windows"
arch()         # "x86_64", "aarch64", "arm", etc.
num_cpus()     # number of CPUs as string
```

### Justfile paths
```just
justfile()            # absolute path to root justfile (always root, even in imports)
justfile_dir()        # directory of root justfile (always root)
source_file()         # path to current source file (import/mod aware)
source_dir()          # directory of current source file (import/mod aware)
invocation_directory()         # cwd when just was invoked
invocation_directory_native()  # cwd verbatim (no Cygwin normalization)
```

### String manipulation
```just
replace(s, from, to)         # replace all occurrences
replace_regex(s, re, repl)   # Rust regex replace
trim(s)                      # strip leading+trailing whitespace
trim_start(s) / trim_end(s)  # strip one side
trim_start_match(s, sub)     # remove prefix once
trim_end_match(s, sub)       # remove suffix once
trim_start_matches(s, sub)   # remove prefix repeatedly
trim_end_matches(s, sub)     # remove suffix repeatedly
quote(s)                     # single-quote for shell safety (handles embedded quotes)
append(suffix, s)            # append to each whitespace-separated word in s
prepend(prefix, s)           # prepend to each whitespace-separated word in s
encode_uri_component(s)      # percent-encode like JS encodeURIComponent
uppercase(s) / lowercase(s)
capitalize(s) / titlecase(s)
snakecase(s) / kebabcase(s) / uppercamelcase(s) / lowercamelcase(s)
shoutysnakecase(s) / shoutykebabcase(s)
```

### Path functions
```just
clean(path)                   # normalize: remove .., extra slashes
absolute_path(path)           # resolve relative to cwd
extension(path)               # file extension ("txt")
file_name(path)               # filename with extension ("bar.txt")
file_stem(path)               # filename without extension ("bar")
parent_directory(path)        # parent directory
without_extension(path)       # path minus extension
canonicalize(path)            # resolve symlinks (path must exist)
join(a, b, ...)               # join paths (uses \ on Windows -- prefer / operator)
```

**Prefer the `/` operator over `join()`** for cross-platform justfiles. `join()` uses
backslash on Windows, which breaks many shell commands.

### Filesystem and tools
```just
path_exists(path)   # "true" or "false" (does not abort)
read(path)          # read file as string (>= 1.39.0)
require("tool")     # find tool in PATH; abort with clear error if missing (>= 1.39.0)
which("tool")       # find tool in PATH; return "" if missing (requires set unstable)
error(message)      # abort evaluation with message
```

### Hashing, UUID, datetime
```just
uuid()                       # random UUID
sha256("string")             # hex SHA-256
sha256_file("path")          # hex SHA-256 of file
blake3("string")             # hex BLAKE3 (>= 1.25.0)
blake3_file("path")          # hex BLAKE3 of file (>= 1.25.0)
datetime("%Y-%m-%d")         # local datetime (strftime format, >= 1.30.0)
datetime_utc("%Y%m%dT%H%M%SZ") # UTC datetime (>= 1.30.0)
semver_matches(ver, req)     # "true"/"false" (>= 1.16.0)
just_executable()            # path to the just binary
just_pid()                   # PID of just process
is_dependency()              # "true" if running as a dependency of another recipe
```

## Settings

```just
set export                          # export all just vars as env vars to recipes
set dotenv-load                     # load .env from cwd or ancestor directories
set dotenv-filename := ".env.local" # load file with this name instead of .env
set dotenv-path := ".env.prod"      # load from exact path (errors if missing)
set dotenv-required                 # error if no .env file found
set dotenv-override                 # .env values override existing env vars
set shell := ["bash", "-uc"]        # shell for recipe lines and backticks
set script-interpreter := ["bash"]  # interpreter for [script] recipes (default: sh -eu)
set positional-arguments            # pass args as $0, $1, $2... to shell
set quiet                           # suppress echoing recipe lines globally
set working-directory := "frontend" # change working dir for all recipes
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]  # Windows shell
set fallback                        # search parent dirs if recipe not found
set ignore-comments                 # silently ignore # lines in recipe body
set allow-duplicate-recipes         # later recipe definitions override earlier ones
set allow-duplicate-variables       # later variable definitions override earlier ones
set unstable                        # enable unstable/experimental features
set tempdir := "/tmp/just"          # directory for temp files
```

`set windows-powershell := true` is deprecated; use `windows-shell` instead.

### dotenv: key points

Dotenv variables become environment variables, not just variables:
```just
set dotenv-load

serve:
  echo $SERVER_PORT    # correct: shell env var
  echo {{SERVER_PORT}} # WRONG: not a just variable

# To use in just expressions:
port := env('SERVER_PORT', '3000')
```

## Exporting Variables

```just
# Export one variable
export RUST_BACKTRACE := "1"

# Export all variables
set export
db_host := "localhost"

# Export via parameter prefix
test $RUST_BACKTRACE="full":
  cargo test

# Export for one recipe only
[env('RUST_BACKTRACE', '1')]
test:
  cargo test

# Unexport (remove from environment, >= 1.29.0)
unexport SECRET_KEY
safe-recipe:
  ./untrusted-tool   # SECRET_KEY not available
```

## Imports and Modules

### `import` -- flat inclusion, shared namespace

```just
import 'common.just'         # merge all recipes/vars into this namespace
import? 'local.just'         # optional (no error if missing)
import '~/shared/tools.just' # ~ expands to home directory
```

Override semantics: shallower definitions override deeper ones (root justfile overrides
imported files). Among same-depth imports, the earlier import wins. This is non-obvious
and known to be confusing -- avoid relying on import order for override behavior.

### `mod` -- namespaced submodule (>= 1.31.0; requires `--unstable` on 1.19.0-1.30.x)

```just
mod build            # looks for build.just, build/mod.just, build/justfile, build/.justfile
mod? optional        # optional module (no error if not found)
mod foo 'path/to/custom.just'   # explicit path
```

Invoke: `just build compile` or `just build::compile`

Module isolation:
- Own namespace: recipes, aliases, and variables are not shared between modules
- Own settings (including `set shell`)
- Own working directory (submodule's directory, unless `[no-cd]`)
- `justfile()` / `justfile_dir()` return ROOT path; use `source_file()` / `source_dir()` for module-local paths
- Dotenv is only loaded by root justfile; env vars flow to submodules as environment vars

### Global/user justfile

`just` loads `~/.user.justfile` (or `~/.justfile`) as a global justfile. Recipes defined
there are available from any directory. Useful for user-level utilities accessible project-wide.

## `set fallback` behavior

When a recipe is not found in the current justfile, `just` searches parent directories for
a justfile containing that recipe. Only activates for the first recipe on the command line.
Useful for monorepo layouts where a root justfile provides common recipes.
