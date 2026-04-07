---
name: structural-edit
description: >
  Structural code search and refactoring with comby and semgrep. Use this skill whenever you need to
  find or transform code patterns that involve nesting, span multiple lines, or require syntax awareness
  -- especially when grep/sed would be fragile or produce false positives. Also use it when the user asks
  about comby, semgrep, structural search, code patterns, codemod, or large-scale refactoring across files.
  Even simple-sounding requests like "rename this function everywhere" or "find all calls to X with argument Y"
  benefit from this skill if the pattern involves parentheses, braces, or multi-line spans.
---

# Structural Edit

Start with grep. Only escalate when it fails or produces too many false positives. These tools form an escalation ladder based on pattern complexity, not task size.

## Tool availability

Before using comby or semgrep, check that they're installed:

```bash
which comby && comby --version
which semgrep && semgrep --version
```

If missing:
- **comby**: `bash <(curl -sL get.comby.dev)` or `brew install comby`
- **semgrep**: `pip install semgrep` or `brew install semgrep`

## Decision heuristic

Ask yourself: **what makes this pattern hard for regex?**

### Use grep / ag / rg (text search)

The pattern is a literal string or simple regex with no nesting concerns.

- Finding all files that reference a symbol: `rg 'my_function'`
- Counting occurrences: `rg -c 'TODO'`
- Listing files containing a pattern: `rg -l 'some_function'`

These tools are fast, simple, and the right default.

### Use sed / Edit tool (text replacement)

The replacement is line-local and the match is unambiguous.

- Renaming a simple identifier within a file (or use the Edit tool)
- Changing a flag value: `sed -i 's/enabled = false/enabled = true/'`
- Adjusting import paths

**Stop using sed when**: the pattern crosses line boundaries, involves balanced delimiters (parentheses, braces, angle brackets), or when you need to match "everything inside the function call" without knowing how deeply nested it is.

### Use comby (structural matching)

The pattern involves **balanced delimiters** or **spans multiple lines**, but you don't need full AST/semantic understanding.

Comby understands the nesting structure of code -- parentheses, braces, brackets, strings, comments -- without needing a full parser. It's language-aware enough to not match inside strings or comments, but lightweight enough to work on partial/broken code.

**Reach for comby when:**
- Matching function calls with arbitrary arguments: `comby 'foo(:[args])' ...`
- Finding patterns across multiple lines (e.g., a variable declaration followed by its use)
- Swapping arguments: `comby 'swap(:[a], :[b])' 'swap(:[b], :[a])'`
- Matching nested structures where regex would need to count braces
- Working with languages comby supports but semgrep doesn't, or with config files/data formats
- You want a quick one-liner without writing a YAML rule file

**Comby strengths:**
- Simple, intuitive hole syntax (`:[var]` captures anything balanced)
- Works on 50+ languages and data formats (JSON, YAML, HTML, etc.)
- Fast (~2-4x faster than semgrep on equivalent patterns)
- Works on incomplete/partial code fragments
- Powerful rewrite properties (case conversion, position info)
- No setup -- just `comby 'match' 'rewrite' -matcher .py -d src/`

**Comby limitations:**
- No semantic understanding (doesn't know types, scopes, or data flow)
- Limited support for indentation-sensitive languages (Python blocks are tricky since comby relies on delimiters, not indentation)
- Whitespace in templates is flexible but not AST-aware: a space in the template matches *any amount* of whitespace, but requires *at least some*. So `foo(:[a], :[b])` matches `foo(x,  y)` but not `foo(x,y)`. Write the template to match the dominant formatting, or run two patterns.

### Use semgrep (AST-aware matching)

The pattern requires **semantic understanding** -- you care about what the code *means*, not just how it looks.

Semgrep parses code into an AST and matches against the tree structure. This means `foo(a, b)` and `foo(a,\n  b)` are the same pattern. It understands scope, types (in some languages), and data flow.

**Reach for semgrep when:**
- Matching must be formatting-independent (same pattern matches regardless of whitespace/newlines)
- You need type-aware matching (e.g., "find all calls where the argument is a specific type")
- You need to enforce that the same expression appears in multiple places (`$X` reuse)
- Pattern logic requires negation ("match X but not when Y")
- Writing persistent lint rules that live in the repo
- You need taint/data-flow analysis

**Semgrep strengths:**
- True AST matching -- immune to formatting differences
- Metavariable identity (`$X == $X` catches `a == a` but not `a == b`)
- Ellipsis operator for flexible matching (`foo(...)`, `if (...) { ... }`)
- YAML rules support complex logic (pattern-either, pattern-not, metavariable conditions)
- Autofix with `--autofix` flag
- Rich ecosystem of community rules

**Semgrep limitations:**
- Requires language support (check `semgrep --show-supported-languages`)
- Slower than comby for simple structural patterns
- Inline CLI patterns (`-e`) are limited -- complex rules need YAML files
- Cannot match across file boundaries (single-file analysis by default)
- No support for arbitrary data formats (unlike comby)
- Sends telemetry by default -- use `--metrics off` in air-gapped or privacy-sensitive environments

## Quick reference

### comby

```bash
# Search only (no rewrite)
comby 'pattern' '' -match-only -matcher .py -d src/

# Search and preview diff
comby 'match' 'rewrite' -matcher .py -d src/ -diff

# Search and replace in-place
comby 'match' 'rewrite' -matcher .py -d src/ -in-place

# Exclude files/dirs
comby 'match' 'rewrite' -matcher .py -d src/ -exclude 'test,vendor'

# Multi-line matching (:[hole] spans newlines at top level)
comby 'if (:[cond]) {:[body]}' 'rewrite' -match-newline-at-toplevel -matcher .cpp -d src/

# Stdin mode (for piping or testing patterns)
comby 'swap(:[a], :[b])' 'swap(:[b], :[a])' -stdin .py <<< 'swap(x, y)'
```

**Hole types** (see `references/comby.md` for full details):
| Syntax | Matches |
|--------|---------|
| `:[var]` | Anything (balanced, lazy, stops at newline unless `-match-newline-at-toplevel`) |
| `:[[var]]` | Alphanumeric + underscore (identifier-like) |
| `:[var:e]` | A single balanced expression |
| `:[var~regex]` | Content matching a PCRE regex |
| `:[var\n]` | Everything up to and including newline |
| `:[ var]` | Whitespace only (no newlines) |
| `:[_]` | Any of the above, but don't capture (just match) |

### semgrep

```bash
# Inline pattern search
semgrep -e 'pattern' --lang python src/ --metrics off

# Inline pattern with autofix
semgrep -e 'foo($X, $Y)' --autofix 'bar($Y, $X)' --lang python src/ --metrics off

# Dry-run autofix (preview changes)
semgrep -e 'foo($X, $Y)' --autofix 'bar($Y, $X)' --lang python src/ --dryrun --metrics off

# Using a YAML rule file
semgrep --config rules/my-rule.yaml src/ --metrics off

# Multiple patterns (use YAML for complex logic)
semgrep --config - --metrics off <<'EOF'
rules:
  - id: my-rule
    patterns:
      - pattern: dangerous_func($X)
      - pattern-not: dangerous_func("safe_value")
    message: "Avoid dangerous_func with non-safe values"
    languages: [python]
    severity: WARNING
    fix: safe_func($X)
EOF
```

**Metavariable types** (see `references/semgrep.md` for full details):
| Syntax | Matches |
|--------|---------|
| `$X` | Any single expression, statement, or identifier |
| `$...X` | Zero or more arguments/statements (variadic) |
| `$_` | Any single thing (anonymous, don't bind) |
| `...` | Zero or more of anything (ellipsis operator) |
| `"$X"` | String literal content |

## Using both tools together

The escalation ladder suggests picking one tool per task, but sometimes **using both comby and semgrep together gives the best coverage**. Each tool has blind spots the other fills.

**When to combine them:** When the pattern involves repeated subexpressions (the "same thing appears twice" family of checks). Comby checks textual (byte-identical) equality, while semgrep checks AST-based (formatting-independent) equality. And they differ in how far they can "reach": comby's `:[_]` can span arbitrary intermediate blocks, while semgrep's `...` doesn't easily bridge nested AST levels.

**Example: duplicate conditions in if/else-if chains**

Consider `if (a) {} else if (b) {} else if (a) {}` — the first and third conditions are duplicates, but separated by an intermediate else-if block (the condition is "transitive" across intermediate blocks).

Run comby to catch transitive duplicates across intermediate else-if blocks:
```bash
comby 'if (:[c]) {:[_]}:[_]else if (:[c]) {:[_]}' '' \
  -match-only -matcher .cpp -match-newline-at-toplevel -d src/
```

Run semgrep to catch direct duplicates that differ only in formatting:
```bash
semgrep -e 'if ($COND) { ... } else if ($COND) { ... }' --lang cpp src/ --metrics off
```

Neither tool alone catches everything. Comby finds the transitive case but requires byte-identical conditions. Semgrep handles formatting differences but can't bridge across nested else-if levels. Use both and union the results.

**Rule of thumb:** If a task involves "find where the same X appears in two places" and the two places can be separated by arbitrary code, consider running both tools.

## Worked examples

### Example 1: Find all calls with a specific argument pattern (comby)

Python — find all `logging.warning()` calls that use %-formatting instead of lazy formatting:
```bash
comby 'logging.warning(:[msg] % :[args])' '' -match-only -matcher .py -d src/
```

C++ — find all `make_leaf_error` calls with two arguments:
```bash
comby 'make_leaf_error(:[a], :[b])' '' -match-only -matcher .cpp -d src/
```

Comby is the right choice: the pattern involves balanced parentheses and we don't care about types or semantics.

### Example 2: Enforce identity check pattern (semgrep)

Finding `x == x` comparisons (likely bugs) — works across languages:

```bash
# Python
semgrep -e '$X == $X' --lang python src/ --metrics off

# C++
semgrep -e '$X == $X' --lang cpp src/ --metrics off
```

Semgrep is the right choice: metavariable identity (`$X` must be the *same expression* in both positions) is a semantic concept that comby can only approximate with textual equality.

### Example 3: Replace a deprecated API call (comby rewrite)

Python — replace old-style string formatting in logging calls:
```bash
comby \
  'logger.info(":[msg]" % :[args])' \
  'logger.info(":[msg]", :[args])' \
  -matcher .py -d src/ -diff
```

C++ — wrap raw `new` with `make_unique`:
```bash
comby \
  'return new :[type](:[args]);' \
  'return std::make_unique<:[type]>(:[args]);' \
  -matcher .cpp -d src/ -diff
```

Review with `-diff` first, then re-run with `-in-place` when satisfied.

### Example 4: Lint rule with autofix (semgrep YAML)

Python — catch bare `except:` clauses:
```yaml
rules:
  - id: no-bare-except
    pattern: |
      try:
          ...
      except:
          ...
    fix: |
      try:
          ...
      except Exception:
          ...
    message: "Use 'except Exception' instead of bare 'except'"
    languages: [python]
    severity: WARNING
```

```bash
semgrep --config rule.yaml src/ --autofix --dryrun --metrics off
```

### Example 5: Find patterns in config/data files (comby)

Comby works on non-code formats that semgrep doesn't support:

```bash
# Find all JSON objects with a "deprecated" key
comby '{"deprecated": :[_], :[rest]}' '' -match-only -matcher .json -d config/

# Find HTML divs with a specific class
comby '<div class="legacy-:[name]">:[content]</div>' '' -match-only -matcher .html -d templates/

# Find YAML blocks with a specific structure
comby 'timeout: :[val]' '' -match-only -matcher .yaml -d config/
```

## Reference docs

For full syntax details, read the reference files:
- `references/comby.md` -- complete hole syntax, rewrite properties, rules, and flags
- `references/semgrep.md` -- metavariables, pattern operators, YAML rule structure, autofix

Read these when you need syntax details beyond what's in the quick reference above.
