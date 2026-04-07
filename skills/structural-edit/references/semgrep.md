# Semgrep Reference

Complete syntax and usage reference for semgrep. See https://semgrep.dev/docs/ for upstream docs.

Note: semgrep sends telemetry by default. Use `--metrics off` to disable, especially in air-gapped or privacy-sensitive environments.

## Table of Contents

1. [Command syntax](#command-syntax)
2. [Pattern syntax](#pattern-syntax)
3. [Metavariables](#metavariables)
4. [Ellipsis operator](#ellipsis-operator)
5. [YAML rule structure](#yaml-rule-structure)
6. [Pattern operators](#pattern-operators)
7. [Autofix](#autofix)
8. [Common flags](#common-flags)
9. [Patterns cookbook](#patterns-cookbook)

## Command syntax

### Inline patterns (quick searches)

```bash
# Basic search
semgrep -e 'PATTERN' --lang LANG [PATH] --metrics off

# Apply fixes from a YAML rule file
semgrep --config rules.yaml --autofix [PATH] --metrics off

# Dry-run autofix (preview without modifying)
semgrep --config rules.yaml --autofix --dryrun [PATH] --metrics off
```

### YAML rules (complex logic)

```bash
# From a file
semgrep --config rules.yaml [PATH] --metrics off

# From stdin (here-doc)
semgrep --config - --metrics off <<'EOF'
rules:
  - id: rule-name
    pattern: 'PATTERN'
    message: "Description"
    languages: [python]
    severity: WARNING
EOF
```

Use inline `-e` for quick one-off searches. Use YAML rules when you need pattern composition (pattern-not, pattern-either), metavariable conditions, or persistent lint rules.

## Pattern syntax

Semgrep patterns look like the target language's code, with metavariables and ellipses for flexibility. Patterns match on the AST, so formatting differences (whitespace, newlines, trailing commas) are ignored.

```
foo(1, 2)          -- matches foo(1, 2) and foo(1,\n  2) and foo( 1 , 2 )
foo($X, $Y)        -- matches foo with any two arguments, captures them
foo(...)           -- matches foo with any number of arguments
```

**Key principle**: write the code you want to find, then replace the varying parts with metavariables or ellipses.

## Metavariables

Metavariables capture parts of the matched code for use in messages, conditions, or fixes.

| Syntax | Name | Matches |
|--------|------|---------|
| `$X` | Named | Any single expression, statement, identifier, or type |
| `$_` | Anonymous | Any single node (matches but doesn't bind) |
| `$...X` | Ellipsis (named) | Zero or more items in a sequence (args, statements, etc.) |
| `$...` | Ellipsis (anon) | Same as `...` but in metavariable position |
| `"$X"` | String content | Content of a string literal |
| `/$X/` | Regex content | Content of a regex literal |

### Metavariable identity

Using the same metavariable name twice requires both positions to match the **same AST node** (not just same text):

```
$X == $X     -- matches: a == a, f(x) == f(x)
             -- does NOT match: a == b
```

This is one of semgrep's most powerful features and something comby can only approximate.

### Typed metavariables (language-dependent)

```
(int $X)           -- matches any expression of type int (C/C++, Java, Go)
(str $S)           -- matches any str expression (Python, with type annotations)
```

Typed metavariables are supported in Java, Go, C/C++, and TypeScript (with varying coverage). Python support requires type annotations.

```
# TypeScript
($X: DomSanitizer).sanitize(...)

# Go (note colon syntax inside parens)
($READER : *zip.Reader).Open($INPUT)
```

## Ellipsis operator

The `...` operator matches zero or more items in a list or sequence.

### In argument lists
```
foo(...)              -- foo with any arguments
foo(1, ...)           -- foo where first arg is 1
foo(..., 1)           -- foo where last arg is 1
foo($X, ..., $Y)     -- first and last args captured
```

### In code blocks
```
if (...) { ... }      -- any if statement
{  ...  foo();  ... } -- block containing foo() somewhere
```

### In data structures
```
{..., "key": $VALUE, ...}   -- object/dict containing "key"
[..., 10]                    -- array ending with 10
```

### Method chaining
```
$O.foo(). ... .bar()  -- matches chains like obj.foo().other(1).again(2).bar()
```

### Deep expression matching
```
<... $X ...>          -- $X anywhere inside a nested expression
if (<... is_admin ...>) { ... }  -- if condition that mentions is_admin somewhere
```

### Semantic equivalences (automatic)

Semgrep automatically matches semantically equivalent code:
- **Import aliasing**: `subprocess.Popen(...)` matches `import subprocess.Popen as sp` followed by `sp(...)`
- **Constant propagation**: `set_password("password")` matches even when the string is assigned to a variable first
- **Associative/commutative operators**: `A | B | C` matches any permutation like `B | C | A`

These can be disabled per-rule via `options: {constant_propagation: false, ac_matching: false}`.

## YAML rule structure

```yaml
rules:
  - id: unique-rule-id           # Required. Identifier for the rule.
    message: "Human-readable"     # Required. Shown when rule matches.
    languages: [python]           # Required. List of target languages.
    severity: WARNING             # Required. LOW, MEDIUM, HIGH, or CRITICAL (legacy: ERROR→HIGH, WARNING→MEDIUM, INFO→LOW).

    # Pattern (one of these is required):
    pattern: 'code pattern'       # Simple pattern
    patterns: [...]               # AND composition
    pattern-either: [...]         # OR composition
    pattern-regex: 'regex'        # Regex fallback

    # Optional:
    fix: 'replacement code'       # Autofix template
    fix-regex:                    # Regex-based fix
      regex: 'pattern'
      replacement: 'text'
      count: 1                   # Limit replacements (optional)
    options:                      # Matching behavior flags
      constant_propagation: true  # Track constant values (default: true)
      ac_matching: true           # Associative/commutative matching (default: true)
    paths:                        # File filtering at rule level
      include: ['src/**/*.py']
      exclude: ['*_test.py']
    metadata:                     # Arbitrary data (CVEs, category, etc.)
      category: security
```

## Pattern operators

Use these in YAML rules under `patterns:` or at rule top level.

### AND (patterns)
All must match on the same code region. Metavariable conditions (`metavariable-regex`, `metavariable-pattern`, `metavariable-comparison`) go inside `patterns:` as sibling items:
```yaml
patterns:
  - pattern: foo($X)
  - metavariable-regex:
      metavariable: $X
      regex: '^user_'
```

### OR (pattern-either)
Any one must match:
```yaml
pattern-either:
  - pattern: dangerous_func($X)
  - pattern: unsafe_func($X)
```

### NOT (pattern-not)
Exclude matches:
```yaml
patterns:
  - pattern: eval($X)
  - pattern-not: eval("literal_string")
```

### Inside (pattern-inside)
Match must be inside another pattern:
```yaml
patterns:
  - pattern: $X = $Y
  - pattern-inside: |
      if ...:
          ...
```

### NOT inside (pattern-not-inside)
Match must not be inside:
```yaml
patterns:
  - pattern: os.system($X)
  - pattern-not-inside: |
      if is_safe($X):
          ...
```

### Regex (pattern-regex / pattern-not-regex)
PCRE2 regex matching (multiline mode). Named capture groups create metavariables:
```yaml
patterns:
  - pattern-regex: 'password\s*=\s*(?P<VALUE>"[^"]+")'
  - pattern-not-regex: 'password\s*=\s*os\.environ'
```

### Focus (focus-metavariable)
Narrow the match region to a specific metavariable (useful for precise reporting/fixing):
```yaml
patterns:
  - pattern: |
      def $FUNC(..., $ARG : bad, ...):
        ...
  - focus-metavariable: $ARG
```

### Metavariable conditions

These go inside `patterns:` as sibling items alongside pattern operators:

```yaml
patterns:
  - pattern: set_port($ARG)
  # Regex filter (left-anchored by default; use .* prefix for unanchored)
  - metavariable-regex:
      metavariable: $ARG
      regex: '^(80|443)$'
  # Sub-pattern matching on a captured metavariable
  - metavariable-pattern:
      metavariable: $ARG
      pattern: 'int($X)'
  # Comparison with arithmetic and functions (int(), str(), re.match(), today(), etc.)
  - metavariable-comparison:
      metavariable: $ARG
      comparison: '$ARG < 1024 and $ARG % 2 == 0'
```

## Autofix

### Simple replacement (fix)
```yaml
fix: 'safe_exit($X)'     # Use captured metavariables
```

### Regex replacement (fix-regex)
```yaml
fix-regex:
  regex: '(.*)\)'
  replacement: '\1, timeout=30)'
  count: 1                # Optional: only replace first occurrence
```

### Deletion
```yaml
fix: ''                   # Empty fix removes the matched code
```

### CLI autofix
```bash
# Apply fixes in-place
semgrep --config rule.yaml --autofix src/ --metrics off

# Preview without writing
semgrep --config rule.yaml --autofix --dryrun src/ --metrics off
```

## Common flags

| Flag | Effect |
|------|--------|
| `-e PATTERN` | Inline pattern (no YAML needed) |
| `--lang LANG` | Language for inline patterns (cpp, python, go, java, js, ts, etc.) |
| `--config FILE` | YAML rule file (or `-` for stdin) |
| `--autofix` | Apply fixes defined in rules |
| `--dryrun` | Preview autofix without modifying files |
| `--json` | Output results as JSON |
| `--verbose` | Detailed output |
| `--include GLOB` | Only scan matching files |
| `--exclude GLOB` | Skip matching files |
| `--max-target-bytes N` | Skip files larger than N bytes |
| `--metrics off` | Disable telemetry (recommended) |
| `--no-git-ignore` | Don't respect .gitignore |

### Generic mode

For unsupported languages or config files, use `--lang generic` (internally called "spacegrep"). Key differences:
- `...` spans up to 10 lines (use multiple `...` for wider spans, or set `options: {generic_ellipsis_max_span: N}`)
- `$X` captures single words only (`[A-Za-z0-9_]+`), not multi-token sequences
- Indentation defines nesting scope (braces provide secondary nesting within lines)
- Use `generic_ellipsis_max_span: 0` to restrict `...` to single-line matching (useful for key-value configs)

## Patterns cookbook

### Find identical subexpressions (any language)
```bash
semgrep -e '$X == $X' --lang python src/ --metrics off
semgrep -e '$X and $X' --lang python src/ --metrics off
semgrep -e '$X || $X' --lang cpp src/ --metrics off
```

### Find unchecked return values (C++)
```yaml
rules:
  - id: unchecked-result
    patterns:
      - pattern: $F(...)
      - pattern-not: $X = $F(...)
      - pattern-not: return $F(...)
      - metavariable-regex:
          metavariable: $F
          regex: '^(validate|check|verify)_'
    message: "Unchecked call to $F"
    languages: [cpp]
    severity: WARNING
```

### Find hardcoded credentials (Python)
```yaml
rules:
  - id: hardcoded-secret
    pattern-either:
      - pattern: 'password = "$X"'
      - pattern: 'secret = "$X"'
      - pattern: 'api_key = "$X"'
    message: "Possible hardcoded credential"
    languages: [python]
    severity: ERROR
```

### Replace deprecated API (C++)
```yaml
rules:
  - id: replace-deprecated
    pattern: old_api::connect($HOST, $PORT)
    fix: new_api::connect({.host = $HOST, .port = $PORT})
    message: "old_api::connect is deprecated, use new_api::connect"
    languages: [cpp]
    severity: WARNING
```

### Catch bare except in Python
```yaml
rules:
  - id: no-bare-except
    pattern: |
      try:
          ...
      except:
          ...
    message: "Use 'except Exception' instead of bare 'except'"
    languages: [python]
    severity: WARNING
```

### Find missing null checks (Go)
```yaml
rules:
  - id: unchecked-error
    patterns:
      - pattern: '$X, _ := $F(...)'
    message: "Error from $F is ignored"
    languages: [go]
    severity: WARNING
```

### Find SQL injection risks (Python)
```yaml
rules:
  - id: sql-injection
    patterns:
      - pattern: 'cursor.execute($QUERY % $X)'
    message: "Use parameterized queries instead of string formatting"
    languages: [python]
    severity: ERROR
```
