# Output Patterns

Patterns for producing consistent, high-quality output from skills.

## Template Pattern

Provide templates for output format. Match strictness to requirements.

### Strict Templates

For API responses, data formats, or compliance requirements:

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

### Flexible Templates

When adaptation is useful:

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

### Partial Templates

When only some fields are fixed:

```markdown
## API response format

Always return JSON with this structure:
{
  "status": "success" | "error",
  "data": { ... },        // shape varies by endpoint
  "metadata": {
    "timestamp": "ISO-8601",
    "version": "1.0"
  }
}
```

## Examples Pattern

For output quality that depends on demonstration:

### Input/Output Pairs

```markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation

Follow this style: type(scope): brief description, then detailed explanation.
```

### Before/After Examples

```markdown
## Code refactoring style

**Before:**
function getData(id) {
  const result = db.query('SELECT * FROM users WHERE id = ' + id);
  return result;
}

**After:**
async function getUserById(userId: string): Promise<User | null> {
  const result = await db.query(
    'SELECT * FROM users WHERE id = $1',
    [userId]
  );
  return result.rows[0] ?? null;
}

Key changes: async/await, parameterized query, typed return, null handling.
```

### Progressive Examples

Show increasing complexity:

```markdown
## SQL query examples

**Simple:**
SELECT name FROM users WHERE active = true;

**With joins:**
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.active = true;

**Complex:**
WITH recent_orders AS (
  SELECT user_id, SUM(total) as total_spent
  FROM orders
  WHERE created_at > NOW() - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT u.name, r.total_spent
FROM users u
JOIN recent_orders r ON u.id = r.user_id
ORDER BY r.total_spent DESC
LIMIT 10;
```

## Validation Pattern

Define what makes output valid:

```markdown
## Valid output criteria

Generated code MUST:
- Compile without errors
- Pass all existing tests
- Include type annotations
- Have no linting warnings

Generated code SHOULD:
- Include brief comments for complex logic
- Follow existing patterns in the codebase
- Be no longer than necessary
```

## Tone and Style Pattern

For text output:

```markdown
## Writing style

**Voice:** Professional but approachable
**Perspective:** Second person ("you")
**Length:** Concise - one idea per paragraph

**Do:**
- Use active voice
- Start with the most important information
- Include specific examples

**Don't:**
- Use jargon without explanation
- Write walls of text
- Be overly formal or stiff
```

## Format Selection Pattern

When multiple output formats are valid:

```markdown
## Output format selection

Choose format based on content:

**Use tables for:** Comparisons, specifications, structured data
**Use lists for:** Steps, features, options
**Use prose for:** Explanations, narratives, context
**Use code blocks for:** Examples, commands, output

When combining formats, use the dominant content type as the base
and embed others as needed.
```

## Error Message Pattern

```markdown
## Error message format

Structure error messages as:

[SEVERITY] Short description

Details: What went wrong
Context: What was being attempted
Fix: How to resolve (if known)

Example:
[ERROR] Failed to parse configuration file

Details: Invalid JSON at line 42, column 15
Context: Loading app.config.json during startup
Fix: Check for missing comma or bracket near line 42
```

## Versioned Output Pattern

When output format may evolve:

```markdown
## Response envelope

All responses include version for compatibility:

{
  "version": "2.0",
  "format": "analysis-report",
  "content": { ... }
}

Version history:
- 2.0: Added metadata section
- 1.1: Changed date format to ISO-8601
- 1.0: Initial format
```
