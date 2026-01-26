# Output Patterns

Use these patterns when skills need to produce consistent, high-quality output.

## Template Pattern

Provide templates for output format. Match the level of strictness to your needs.

**For strict requirements (like API responses or data formats):**

```markdown
## Report structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

**For flexible guidance (when adaptation is useful):**

```markdown
## Report structure

Here is a sensible default format, but use your best judgment:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]

Adjust sections as needed for the specific analysis type.
```

## Examples Pattern

For skills where output quality depends on seeing examples, provide input/output pairs:

```markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow this style: type(scope): brief description, then detailed explanation.
```

Examples help Claude understand the desired style and level of detail more clearly than descriptions alone.

## Anti-Patterns to Avoid

These patterns reduce skill effectiveness or cause problems:

### Windows-Style Paths

**Bad:**
```markdown
Run the script at `scripts\process.py`
Store output in `C:\Users\output\`
```

**Good:**
```markdown
Run the script at `scripts/process.py`
Store output in the current working directory
```

Use forward slashes for paths. Avoid hardcoded absolute paths.

### Too Many Options

**Bad:**
```markdown
Choose your preferred approach:
1. Use library A (fast, limited features)
2. Use library B (medium speed, most features)
3. Use library C (slow, all features)
4. Use library D (requires setup, enterprise features)
5. Write custom implementation
6. Use online service
```

**Good:**
```markdown
Use library B for most cases. For simple operations, library A is faster.
See references/alternatives.md if you need enterprise features.
```

Limit choices to 2-3 options. Move edge cases to reference files.

### Time-Sensitive Information

**Bad:**
```markdown
As of January 2024, the API uses v2 endpoints.
The current stable version is 3.2.1.
```

**Good:**
```markdown
Use the latest stable version of the API.
Check the official documentation for current endpoints.
```

Avoid dates, version numbers, or information that will become stale.

### Duplicating Claude's Knowledge

**Bad:**
```markdown
## Python Basics
Python is a programming language. To define a function, use `def`.
Variables don't need type declarations.
```

Claude already knows Python. Only document domain-specific or non-obvious information.

### Over-Documenting the Obvious

**Bad:**
```markdown
## How to Read Files
1. Open the file using the Read tool
2. The file contents will be displayed
3. You can now see what's in the file
```

Trust Claude's existing capabilities. Document what's unique to your skill.
