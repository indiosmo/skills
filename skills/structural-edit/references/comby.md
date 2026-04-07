# Comby Reference

Complete syntax and usage reference for comby. See https://comby.dev/docs/ for upstream docs.

## Table of Contents

1. [Command syntax](#command-syntax)
2. [Hole types](#hole-types)
3. [Rewrite properties](#rewrite-properties)
4. [Rules](#rules)
5. [Matchers](#matchers)
6. [Common flags](#common-flags)
7. [Patterns cookbook](#patterns-cookbook)

## Command syntax

```
comby 'MATCH_TEMPLATE' 'REWRITE_TEMPLATE' [OPTIONS]
```

- First argument: the match template (pattern to find)
- Second argument: the rewrite template (replacement text, use `''` with `-match-only`)
- Everything else in the match template is literal -- only `:[hole]` syntax is special
- Whitespace handling: a single space in the template matches *any amount* of whitespace (spaces, tabs, newlines), but requires at least some whitespace at that position. So `f(:[a], :[b])` matches `f(x,  y)` but not `f(x,y)`.

## Hole types

Holes are the capture mechanism. They match code fragments and bind them to names for use in the rewrite template.

| Syntax | Name | Matches |
|--------|------|---------|
| `:[var]` | Universal | Zero or more characters, lazy, balanced. When inside delimiters (e.g., `{...}`, `(...)`), matches within that group including newlines. Outside delimiters, stops at a newline or the start of a code block, whichever comes first (use `-match-newline-at-toplevel` to override). |
| `:[[var]]` | Alphanum | One or more alphanumeric characters and `_`. Think: identifier. |
| `:[var:e]` | Expression | A single balanced expression: non-whitespace chars, or a balanced delimited block. Language-dependent. |
| `:[var~regex]` | Regex-constrained | Content matching a PCRE regex. Avoid regex special chars like `)` and `.*` -- keep patterns simple. |
| `:[var\n]` | Line | Zero or more characters up to and including the next newline. |
| `:[ var]` | Whitespace | Whitespace characters only, excluding newlines. |
| `:[var.]` | Punctuation | One or more alphanumeric characters plus punctuation (`.`, `;`, `-`) that do not affect balanced syntax. Language-dependent. |

**Anonymous holes**: Replace `var` with `_` to match without capturing: `:[_]`, `:[[_]]`, `:[_:e]`, `:[_~regex]`.

**`...` shorthand**: The literal `...` is an alias for `:[_]` (anonymous universal hole). Use it for concise patterns where you don't need to capture.

**Repeated holes**: Using the same name twice in a match template requires textual equality (both positions must match the same text).

## Rewrite properties

In the rewrite template, reference captured holes and apply transformations:

### String converters
| Property | Effect | Example: `:[var]` = `myVarName` |
|----------|--------|----------------------------------|
| `:[var].lowercase` | all lowercase | `myvarname` |
| `:[var].UPPERCASE` | ALL CAPS | `MYVARNAME` |
| `:[var].Capitalize` | First letter caps | `Myvarname` |
| `:[var].uncapitalize` | First letter lowercase | `myVarName` (unchanged if already lowercase) |
| `:[var].lower_snake_case` | snake_case | `my_var_name` |
| `:[var].UPPER_SNAKE_CASE` | UPPER_SNAKE | `MY_VAR_NAME` |
| `:[var].lowerCamelCase` | camelCase | `myVarName` |
| `:[var].UpperCamelCase` | PascalCase | `MyVarName` |

### Size and position
| Property | Value |
|----------|-------|
| `:[var].length` | Character count |
| `:[var].lines` | Line count |
| `:[var].line` / `:[var].line.start` | Starting line number |
| `:[var].line.end` | Ending line number |
| `:[var].column` / `:[var].column.start` | Starting column number |
| `:[var].column.end` | Ending column number |
| `:[var].offset` / `:[var].offset.start` | Starting byte offset |
| `:[var].offset.end` | Ending byte offset |
| `:[var].file` / `:[var].file.path` | Full file path |
| `:[var].file.name` | File name only |
| `:[var].file.directory` | Directory only |

### Identity
| Property | Value |
|----------|-------|
| `:[var].value` | The matched text unchanged (same as `:[var]`) |

### Fresh identifiers

Use `:[id()]` in a rewrite template to generate a random alphanumeric identifier. To reuse the same fresh identifier in multiple places, pass a label: `:[id(my_label)]`.

```bash
# Generate unique variable names during a refactor
comby 'var :[left] = :[[right]] + 1' 'var a_:[id()] = :[left] + :[[right]] + 1' -matcher .js -d src/ -diff
```

## Rules

Rules add conditions to matches using the `-rule` flag. Rules are written in a simple expression language.

### Where clauses

Filter matches by constraining hole values:

```bash
# Only match when the argument contains "None"
comby 'if :[cond]:' '' -match-only -rule 'where match :[cond] { | ":[_]None:[_]" -> true }' -matcher .py -d src/

# Equality constraint on a hole
comby 'foo(:[arg])' '' -match-only -rule 'where :[arg] == "bar"' -matcher .py -d src/

# Inequality constraint
comby '$X = :[val]' '' -match-only -rule 'where :[val] != "None"' -matcher .py -d src/

# Multiple conditions (comma = logical AND)
comby ':[fn](:[a], :[b])' '' -match-only -rule 'where :[a] != :[b], :[a] != "0"' -matcher .py -d src/
```

### Rewrite rules

Apply a rewrite within a matched hole:

```bash
# Match a block and rewrite part of it
comby 'config {:[body]}' '' -rule 'where rewrite :[body] { "timeout = :[v]" -> "timeout = 30" }' -matcher .generic -d .
```

## Matchers

Comby has built-in parsers for balanced delimiters per language. Specify with `-matcher` or `-m`:

```bash
comby 'pattern' 'rewrite' -matcher .py -d src/
```

Common matchers: `.c`, `.cpp`, `.h`, `.hpp`, `.py`, `.go`, `.rs`, `.java`, `.js`, `.ts`, `.json`, `.yaml`, `.html`, `.xml`, `.sh`, `.generic`

The matcher determines:
- What counts as a string literal (and thus skipped during matching)
- What counts as a comment
- What balanced delimiters to recognize

Use `-list` to see all supported languages: `comby -list`

## Common flags

| Flag | Effect |
|------|--------|
| `-match-only` | Only show matches, don't rewrite. Second arg is ignored but required (use `''`). |
| `-d PATH` | Search recursively in directory (default: current dir) |
| `-in-place` | Modify files on disk |
| `-diff` | Output a unified diff (preview changes without writing) |
| `-matcher EXT` / `-m` | Force this language matcher for all files |
| `-match-newline-at-toplevel` | Allow `:[hole]` to match across newlines at the top level |
| `-exclude PREFIXES` | Comma-separated file/path prefixes to skip |
| `-exclude-dir PREFIXES` | Comma-separated directory prefixes to skip (default: `.`) |
| `-extensions EXTS` | Only process files with these extensions |
| `-count` | Just show match count per file |
| `-json-lines` | Output as JSON (useful for programmatic processing) |
| `-stdin` | Read input from stdin instead of files |
| `-rule RULE` | Apply a rule expression to filter/transform matches |
| `-bound-count N` | Stop after finding at least N matches |
| `-jobs N` | Number of parallel workers (default: 4) |
| `-sequential` | Run single-threaded |

## Patterns cookbook

### Find function calls with specific structure
```bash
# Python: find all calls to json.loads with a single argument
comby 'json.loads(:[arg])' '' -match-only -matcher .py -d src/

# C++: all calls to make_leaf_error with two args
comby 'make_leaf_error(:[a], :[b])' '' -match-only -matcher .cpp -d src/

# Go: find all defer statements closing something
comby 'defer :[x].Close()' '' -match-only -matcher .go -d .
```

### Swap arguments
```bash
# Python
comby 'assertEqual(:[a], :[b])' 'assertEqual(:[b], :[a])' -matcher .py -d tests/ -diff

# C++
comby 'std::pair(:[a], :[b])' 'std::pair(:[b], :[a])' -matcher .cpp -d src/ -diff
```

### Wrap a call
```bash
# Python: wrap open() with Path()
comby 'open(:[args])' 'Path(:[args]).open()' -matcher .py -d src/ -diff

# C++: wrap raw pointer returns with unique_ptr
comby 'return new :[type](:[args]);' 'return std::make_unique<:[type]>(:[args]);' -matcher .cpp -d src/ -diff
```

### Rename with case conversion
```bash
# Convert camelCase function names to snake_case (in specific pattern)
comby 'def :[[name]](:[args]):' 'def :[name].lower_snake_case(:[args]):' -matcher .py -d src/ -diff
```

### Extract identifiers matching a regex
```bash
# Find all TypeVar instantiations with their names
comby 'TypeVar(":[name~[A-Z][a-zA-Z]*]")' '' -match-only -matcher .py -d src/
```

### Multi-line patterns
```bash
# Find if-else chains (needs -match-newline-at-toplevel)
comby 'if (:[c1]) {:[_]} else if (:[c2]) {:[_]}' '' \
  -match-only -matcher .cpp -match-newline-at-toplevel -d src/

# Find try/except blocks in Python
comby 'try::[body]except :[exc]:' '' \
  -match-only -matcher .py -match-newline-at-toplevel -d src/
```

### Config / data file patterns
```bash
# Find JSON objects with a specific key
comby '{"name": :[val], :[rest]}' '' -match-only -matcher .json -d config/

# Find YAML values
comby 'timeout: :[val]' '' -match-only -matcher .yaml -d config/
```
