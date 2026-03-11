# just Cross-Platform Patterns

## Contents

- [OS Detection](#os-detection)
- [Platform-Specific Recipes](#platform-specific-recipes)
- [Conditional Variables per OS](#conditional-variables-per-os)
- [Windows Shell Configuration](#windows-shell-configuration)
- [Path Handling](#path-handling)
- [Shebang Recipes on Windows](#shebang-recipes-on-windows)
- [Cross-Platform Justfile Template](#cross-platform-justfile-template)

## OS Detection

```just
system-info:
  @echo "OS: {{os()}} (family: {{os_family()}}, arch: {{arch()}})"
```

- `os()`: `"linux"`, `"macos"`, `"windows"`, `"freebsd"`, `"openbsd"`, etc.
- `os_family()`: `"unix"` or `"windows"`
- `arch()`: `"x86_64"`, `"aarch64"`, `"arm"`, etc.

## Platform-Specific Recipes

Use platform attributes to define OS-specific variants of the same recipe name:

```just
[unix]
install:
  cp bin/app /usr/local/bin/app
  chmod +x /usr/local/bin/app

[windows]
install:
  Copy-Item bin\app.exe C:\Windows\System32\app.exe
```

The recipe is only available when the current OS matches. Multiple platform attributes combine
with OR: the recipe runs if ANY of the specified platforms is active.

```just
[linux]
[macos]
build-native:
  cc main.c -o app
```

`[unix]` includes macOS. Use `[linux]` and `[macos]` separately when they differ.

Available platform attributes: `[linux]`, `[macos]`, `[unix]`, `[windows]`, `[openbsd]`

## Conditional Variables per OS

```just
exe_suffix := if os_family() == "windows" { ".exe" } else { "" }
binary := "myapp" + exe_suffix

pkg_mgr := if os() == "macos" { "brew" } else if os() == "linux" { "apt" } else { "choco" }
```

## Windows Shell Configuration

`just` uses `sh` by default on all platforms. For Windows, configure a different shell:

```just
# Prefer windows-shell over the deprecated windows-powershell setting
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

hello:
  Write-Host "Hello from PowerShell"
```

For cross-platform justfiles, you can set both:

```just
set shell := ["bash", "-uc"]
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# This recipe body must be valid in both bash and PowerShell
info:
  echo "Running on {{os()}}"
```

When recipes differ significantly between platforms, use platform-specific recipe variants
instead of trying to write a single body that works in both shells.

## Path Handling

**Always use the `/` operator for path joining.** The `join()` function uses `\` on Windows,
which breaks many shell commands that expect forward slashes.

```just
# CORRECT -- always produces forward slashes
scripts := justfile_dir() / "scripts"
config  := justfile_dir() / "config" / "app.toml"

# AVOID -- produces \ on Windows
scripts := join(justfile_dir(), "scripts")
```

`clean(path)` normalizes slashes and removes redundant `..` and `//`:

```just
normalized := clean("foo//bar/../baz")  # -> "foo/baz"
```

## Shebang Recipes on Windows

On Windows, shebang interpreter paths containing `/` are passed through `cygpath`. If Cygwin
is not installed, shebang recipes with Unix-style paths fail.

For portable shebang-style recipes, use the `[script("CMD")]` attribute instead:

```just
[script("python3")]
analyze:
  import sys
  print(f"Python {sys.version} on {sys.platform}")
```

Use `[extension("py")]` to set the temp file extension (important on Windows, where `.py`
triggers the correct interpreter):

```just
[script("python3")]
[extension("py")]
analyze:
  import sys
  print(sys.platform)
```

## Cross-Platform Justfile Template

```just
# Settings
set dotenv-load

# Variables
bin      := "myapp" + if os_family() == "windows" { ".exe" } else { "" }
out_dir  := justfile_dir() / "dist"

# Default
default:
  @just --list

# Build -- platform-specific
[unix]
build:
  cc main.c -o {{out_dir / bin}}

[windows]
build:
  cl main.c /Fe:{{out_dir / bin}}

# Test -- same on all platforms
test: build
  {{out_dir / bin}} --test

# Install -- platform-specific
[unix]
install: build
  install -m 755 {{out_dir / bin}} /usr/local/bin/

[windows]
install: build
  Copy-Item {{out_dir / bin}} C:\Windows\System32\
```
