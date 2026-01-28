---
name: searching-docs
description: "Search library/API documentation using Context7 and Ref MCP tools. Use when Claude needs to: (1) Look up API syntax or code snippets, (2) Search library documentation, (3) Research implementation patterns, (4) Debug issues using docs, or (5) Explore unfamiliar libraries or frameworks."
---

## Tool Selection

| Scenario | Tool | Reason |
|----------|------|--------|
| Known library, need code examples | Context7 | Optimized for retrieving code snippets |
| General API reference lookup | Context7 | Fast, structured documentation access |
| Obscure/niche library | Ref | Broader search across multiple sources |
| Concept explanation or tutorials | Ref | Better for prose and explanatory content |
| Debugging with error messages | Ref | Can search Stack Overflow, GitHub issues |
| Cross-library comparison | Ref | Searches across multiple documentation sources |

## Decision Flow

1. Is the library well-known (React, Python stdlib, popular npm packages)?
   - Yes: Start with Context7
   - No: Start with Ref

2. Do you need code snippets or API signatures?
   - Yes: Prefer Context7
   - No (need explanations/tutorials): Prefer Ref

3. Did the first tool return insufficient results?
   - Yes: Try the other tool as fallback

## Combining Tools

For comprehensive research, use both tools:
1. Context7 for official API documentation and code examples
2. Ref for community solutions, tutorials, and edge cases

When the agent returns, synthesize findings into actionable guidance for the user.

## Tool Usage Examples

**Context7 workflow:**
1. Call `resolve-library-id` with the library name to get the Context7 library ID
2. Call `query-docs` with the returned library ID and your specific question

**Ref workflow:**
1. Call `ref_search_documentation` with a descriptive query including language/framework names
2. Call `ref_read_url` with the exact URL from results (include the #hash portion)
