# Agent Prompt Templates

Detailed prompt templates for the exploration and synthesis agents.

## Exploration Agent Prompt

Use this template for each documentation section agent:

```
You are exploring the "{section-name}" section of {library-name} documentation.

Starting URL: {section-url}

## Your Task

Systematically explore this documentation section and extract knowledge that helps developers use {library-name} correctly and idiomatically.

## Process

1. **Fetch the starting page** using WebFetch
2. **Identify sub-pages** within this section from navigation links
3. **For each page**, extract:
   - Key concepts explained
   - Code examples (keep the best/most illustrative ones)
   - Warnings, notes, or "gotchas" mentioned
   - Best practices recommended
   - Common mistakes warned against
4. **Navigate to related pages** within this section
5. **Compile findings** into the output file

## Output Format

Write your findings to: {scratchpad}/findings/{section-name}.md

Use this structure:

```markdown
# {Section Name}

> Summary: [1-2 sentence summary of what this section covers]

## Core Concepts

### [Concept 1]
[Explanation in your own words, synthesized from docs]

### [Concept 2]
[Explanation]

## Best Practices

- **[Practice name]**: [Why and how]
- **[Practice name]**: [Why and how]

## Common Pitfalls

### [Pitfall 1]
**Problem**: [What goes wrong]
**Solution**: [How to avoid/fix]

### [Pitfall 2]
**Problem**: [What goes wrong]
**Solution**: [How to avoid/fix]

## Code Patterns

### [Pattern name]
```python
# [Description of what this pattern does]
[code example]
```

### [Pattern name]
```python
[code example]
```

## Key APIs

| Function/Class | Purpose | Key Parameters |
|---------------|---------|----------------|
| `name()` | [What it does] | `param1`, `param2` |

## Notes

[Any other important information that doesn't fit above categories]
```

## Guidelines

- **Be selective**: Don't copy everything, extract the most valuable insights
- **Synthesize**: Combine information from multiple pages when relevant
- **Code quality**: Only include code examples that are clear and instructive
- **Practical focus**: Prioritize information that helps write real code
- **Cite specifics**: If something is version-specific or has caveats, note them
```

## Synthesis Agent Prompt

Use this template for the final synthesis agent:

```
You are synthesizing documentation findings into a comprehensive "{skill-name}" skill for {library-name}.

## Input

Read all markdown files in: {scratchpad}/findings/

These contain findings from parallel agents that explored different documentation sections.

## Your Task

1. **Analyze all findings** - Identify themes, overlaps, and dependencies
2. **Create the skill** - Initialize and write a comprehensive skill
3. **Organize logically** - Structure content for progressive learning

## Process

### Step 1: Read and Analyze

Read each file in {scratchpad}/findings/. Take notes on:
- Concepts that appear in multiple sections (these are fundamental)
- Dependencies between concepts (what must be learned first)
- The most common patterns and pitfalls
- Unique insights from each section

### Step 2: Initialize Skill

```bash
python3 /home/msi/workspace/skills/.claude/skills/skill-creator/scripts/init_skill.py {skill-name} --path /home/msi/workspace/skills/.claude/skills
```

### Step 3: Write SKILL.md

Create a SKILL.md that synthesizes all findings. Structure:

```markdown
---
name: {skill-name}
description: Comprehensive guide for using {library-name}. Covers [main capabilities]. Use when building [typical use cases]. Includes setup, core concepts, common patterns, pitfalls to avoid, and API reference.
---

# Using {Library Name}

[library-name] is [one sentence description]. Use it for [primary use cases].

## Quick Start

[Minimal complete example that works - ~10-20 lines]

## Mental Model

[How to think about this library - the key abstractions and how they relate]

## Core Concepts

### [Concept 1 - most fundamental]
[Explanation with brief code example]

### [Concept 2]
[Explanation with brief code example]

[Continue for 3-5 core concepts]

## Common Patterns

### [Pattern 1 - most frequent use case]
```python
[Idiomatic code]
```

[Continue for 4-6 common patterns]

## Pitfalls & Caveats

### [Pitfall 1]
**Wrong**: [What people do wrong]
**Right**: [What to do instead]
**Why**: [Brief explanation]

[Continue for 3-5 major pitfalls]

## Best Practices

- **[Practice]**: [Explanation]
[Continue for 5-8 best practices]

## API Quick Reference

### [Category 1]
- `function()` - [What it does]
- `Class` - [What it does]

[Continue for main API surface]
```

### Step 4: Handle Large Content

If SKILL.md exceeds ~400 lines, split into references:

- `references/patterns.md` - Extended code patterns and examples
- `references/api.md` - Detailed API documentation
- `references/advanced.md` - Advanced topics and edge cases

Reference these from SKILL.md: "For more patterns, see [references/patterns.md](references/patterns.md)"

### Step 5: Clean Up

Delete unused files from the initialized skill:
- `scripts/example.py`
- `assets/example_asset.txt`
- `references/api_reference.md`

## Quality Checklist

Before finishing, verify:
- [ ] SKILL.md frontmatter has comprehensive description
- [ ] Quick Start example actually works (syntactically correct)
- [ ] Core concepts are ordered from fundamental to advanced
- [ ] Common patterns cover the most frequent use cases
- [ ] Pitfalls include the most impactful mistakes to avoid
- [ ] No duplicate information between sections
- [ ] References linked from SKILL.md if they exist
```

## Section Discovery Patterns

When discovering documentation structure, look for these common patterns:

### Framework Documentation (React, Vue, etc.)
- Getting Started / Installation
- Tutorial / Learn
- API Reference
- Guides / How-to
- Examples / Recipes

### Library Documentation (requests, pandas, etc.)
- Quickstart
- User Guide
- API Reference
- Advanced Usage
- FAQ / Troubleshooting

### Tool Documentation (Docker, Git, etc.)
- Getting Started
- Concepts
- Reference / Commands
- Tutorials
- Best Practices

Map discovered sections to exploration agents. Aim for 4-8 parallel agents for good coverage without overwhelming.
