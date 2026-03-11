---
name: searching-docs
description: "Search library/API documentation using Context7 and Ref MCP tools. Use whenever Claude needs to look up anything about a library, framework, or API -- even if it seems simple. Triggers include: (1) Look up API syntax, method signatures, or code snippets, (2) Search library documentation or changelogs, (3) Research implementation patterns or best practices, (4) Debug issues or error messages using docs, (5) Explore unfamiliar libraries or frameworks, (6) Verify whether a method, parameter, or feature exists, (7) Confirm behavior that Claude is uncertain about. Also use this skill when the user asks things like 'how do I use X library', 'what's the syntax for Y', 'show me examples of Z', 'does this method accept a callback', or when the user is confused about how a library works, needs to check if a method exists, wants to understand error messages from a framework, or is asking about version-specific behavior."
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
| Version-specific behavior | Both | Context7 for latest docs, Ref to find version-specific pages |
| Multi-library question | Both | Resolve each library separately, then combine findings |

## Decision Flow

1. Is the library well-known (React, Python stdlib, popular npm packages)?
   - Yes: Start with Context7 -- it is faster and returns structured results.
   - No: Start with Ref -- it has broader coverage of niche and less popular libraries.

2. Do you need code snippets or API signatures?
   - Yes: Prefer Context7.
   - No (need explanations, tutorials, or community discussion): Prefer Ref.

3. Is the question version-specific (e.g., "I'm using React 17, not 18")?
   - If Context7 returns docs for the wrong version, fall back to Ref and search for version-specific documentation pages. Include the version number in your Ref query (e.g., "react 17 lifecycle methods").
   - Context7 typically serves the latest version of a library's docs. If the user is on an older version, verify that the API you found actually existed in their version.

4. Does the question span multiple libraries (e.g., "how to use pandas with SQLAlchemy")?
   - Resolve each library separately in Context7 (call `resolve-library-id` for each), then query each one.
   - Alternatively, use Ref with a combined query since it can search across sources.

5. Are you unsure which tool to use?
   - Try Context7 first since it is faster and returns structured results. If it returns insufficient results, fall back to Ref.

6. Did the first tool return insufficient results?
   - Yes: Try the other tool. See "Error Handling and Fallbacks" below.

## Crafting Effective Queries

Good queries are specific and include the library name, the function or concept, and the action. Avoid vague natural-language questions.

**For Context7 `resolve-library-id`:**
- Use the library's canonical name. Keep it short.
- Good: `pandas`, `react`, `fastapi`, `express`
- Poor: `the python data analysis library`, `facebook's frontend framework`

**For Context7 `query-docs`:**
- Be specific about the function, class, or concept. Include the action you want.
- Good: `read_csv skip rows` -- names the function and the parameter concern
- Good: `useEffect cleanup function` -- names the hook and the specific aspect
- Good: `Router middleware order of execution` -- names the component and the behavior
- Poor: `how to skip rows` -- too vague, missing function name
- Poor: `how does useEffect work` -- too broad, will return too much
- Poor: `middleware` -- too generic

**For Ref `ref_search_documentation`:**
- Include the language or framework name in the query. Be descriptive but not conversational.
- Good: `python pandas read_csv skiprows parameter`
- Good: `express.js error handling middleware next function`
- Good: `rust serde deserialize enum variants`
- Poor: `how to skip rows in a csv file` -- missing library name
- Poor: `error handling` -- far too vague
- Poor: `why doesn't my middleware work` -- conversational, not searchable

## Tool Usage

**Context7 workflow:**
1. Call `resolve-library-id` with the library name to get the Context7 library ID.
   - Example: resolve-library-id with query `pandas`
   - Example: resolve-library-id with query `react`
   - If multiple candidates are returned, pick the one with the highest snippet count and trust score. A library with 5000 snippets is almost certainly the correct one over a library with 12 snippets.
2. Call `query-docs` with the returned library ID and a specific query.
   - Example: query-docs with library ID `/python/pandas` and query `read_csv skiprows parameter`
   - Example: query-docs with library ID `/facebook/react` and query `useEffect cleanup return function`

**Ref workflow:**
1. Call `ref_search_documentation` with a descriptive query including the language/framework name.
   - Example: `python pandas read_csv skip rows`
   - Example: `express.js middleware error handling next`
   - Example: `rust tokio spawn blocking vs spawn`
2. Call `ref_read_url` with the exact URL from results (include the #hash portion if present).
   - Always use the full URL including any fragment identifier -- these point to the specific section relevant to the query.

## Error Handling and Fallbacks

**When a tool returns no results:**
- Rephrase the query. Remove overly specific terms and try broader keywords.
- Switch to the other tool. If Context7 found nothing, try Ref, and vice versa.
- For Context7: verify that `resolve-library-id` returned the correct library. Some libraries have non-obvious IDs.

**When a tool returns too many results or irrelevant results:**
- Narrow the query. Add the specific function name, class name, or parameter.
- For Ref: add the language name to disambiguate (e.g., `python requests timeout` instead of `requests timeout`).

**When `resolve-library-id` returns multiple candidates:**
- Compare the snippet count and trust/reputation score.
- The candidate with significantly more snippets is almost always the correct one.
- If two candidates have similar snippet counts, prefer the one whose name or description most closely matches the user's context (e.g., the Python `requests` library vs. an unrelated npm package also called `requests`).

**When results seem outdated or conflict with what you know:**
- Flag this to the user. State which version the documentation appears to cover.
- Use Ref to search for the specific version's documentation or changelog.
- Do not silently use outdated information -- always note version discrepancies.

## Synthesizing Results

When combining information from multiple sources or tool calls:

1. Prioritize official documentation over community answers. Official docs are the ground truth for API signatures, parameter names, and return types.
2. Note version discrepancies. If Context7 returns docs for v3 but the user is on v2, say so explicitly. Do not present v3 APIs as if they work on v2.
3. Flag deprecated APIs. If the documentation marks something as deprecated, warn the user and suggest the recommended replacement.
4. When official docs and community answers disagree, trust the official docs for "what the API does" and community answers for "practical workarounds and edge cases."
5. If you found information from multiple sources, briefly mention where key facts came from so the user can follow up.

## Version-Specific Lookups

Libraries change between major versions. When the user specifies a version (or when their code implies one):

- Context7 typically returns documentation for the latest stable version. If the user is on an older version, the APIs shown may not exist or may behave differently.
- Use Ref to search for version-specific documentation. Many libraries host versioned docs (e.g., `https://reactjs.org/docs/` vs. `https://legacy.reactjs.org/`). Include the version number in your Ref search query.
- When you cannot find version-specific docs, note this clearly: "I found documentation for version X, but you are using version Y. The behavior may differ."
- Pay special attention to migration guides and changelogs -- these are the best source for understanding what changed between versions.

## Combining Tools

For comprehensive research, use both tools:
1. Context7 for official API documentation and code examples.
2. Ref for community solutions, tutorials, and edge cases.

When both tools return results, synthesize findings into actionable guidance. Do not dump raw documentation at the user -- extract the relevant parts and explain how they apply to the user's specific question.
